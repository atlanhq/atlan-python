"""LMDB-based checkpoint storage for scalable diff computation.

Provides simple dictionary-like access to LMDB for storing
qualified_name+type_name -> hash mappings. This enables memory-efficient
comparison of large datasets across pipeline runs.

The module supports failure-resilient checkpointing via copy-then-modify:
- Copy existing checkpoint to a working copy
- Modify the copy in place (only writing actual changes)
- Atomically swap on success

This is faster than writing all records to a new checkpoint because
unchanged records don't require any writes.

For high-volume workloads (100M+ records), use batch_transaction() and
epoch-based deletion instead of individual get/put calls.

Example usage (basic):
    from pyatlan_v9.checkpoint import CheckpointStore, compute_content_hash

    with CheckpointStore("/path/to/checkpoint") as store:
        # Check if record exists
        old_hash = store.get("Table", "conn/db/schema/table")

        # Compute hash of current record
        new_hash = compute_content_hash({"name": "table", "description": "..."})

        if old_hash is None:
            print("NEW record")
        elif old_hash != new_hash:
            print("UPDATED record")
        else:
            print("UNCHANGED record")

        # Store new hash
        store.put("Table", "conn/db/schema/table", new_hash)

Example usage (batch - for 100M+ records):
    import time
    from pyatlan_v9.checkpoint import CheckpointStore, compute_content_hash

    current_epoch = int(time.time())

    with CheckpointStore("/path/to/checkpoint") as store:
        # Process records in a single transaction
        with store.batch_transaction(write=True) as batch:
            for record in records:
                old_value = batch.get(type_name, qualified_name)
                old_hash = parse_epoch_value(old_value)[1] if old_value else None

                new_hash = compute_content_hash(record)
                new_value = f"{current_epoch}:{new_hash}"

                if old_hash != new_hash:
                    # Record is new or changed
                    pass

                batch.put(type_name, qualified_name, new_value)

                # Periodic flush for memory efficiency
                if len(batch._pending_puts) >= 10000:
                    batch.flush_puts()

            batch.flush_puts()

        # Detect deletions via epoch (cursor-based, no memory overhead)
        for type_name, qn in store.delete_stale_epochs(current_epoch):
            print(f"Deleted: {type_name}/{qn}")
"""

from __future__ import annotations

import shutil
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, cast

import lmdb  # type: ignore[import-untyped]
import xxhash

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator


def checkpoint_exists(checkpoint_dir: str | Path) -> bool:
    """Check if a checkpoint database exists.

    Args:
        checkpoint_dir: Directory path for the checkpoint.

    Returns:
        True if a valid checkpoint exists, False otherwise.
    """
    path = Path(checkpoint_dir)
    # LMDB creates data.mdb when it has data
    return (path / "data.mdb").exists()


def swap_checkpoints(new_checkpoint: str | Path, target_checkpoint: str | Path) -> None:
    """Atomically swap a new checkpoint to become the target checkpoint.

    This removes the old target checkpoint (if any) and renames the new
    checkpoint to take its place. This is the commit step after a
    successful diff operation.

    Args:
        new_checkpoint: Path to the newly created checkpoint.
        target_checkpoint: Path where the checkpoint should live.
    """
    new_path = Path(new_checkpoint)
    target_path = Path(target_checkpoint)

    # Remove old checkpoint if it exists
    if target_path.exists():
        shutil.rmtree(target_path)

    # Rename new checkpoint to target
    new_path.rename(target_path)


def copy_checkpoint(source: str | Path, target: str | Path) -> None:
    """Copy a checkpoint directory to create a working copy.

    This is used for the copy-then-modify pattern where we copy the
    existing checkpoint and modify it in place, rather than creating
    a new checkpoint from scratch.

    Args:
        source: Path to the source checkpoint.
        target: Path for the copy.
    """
    source_path = Path(source)
    target_path = Path(target)

    # Remove target if it exists (from a previous failed run)
    if target_path.exists():
        shutil.rmtree(target_path)

    # Copy the checkpoint directory
    shutil.copytree(source_path, target_path)


def cleanup_incomplete_checkpoint(checkpoint_dir: str | Path) -> None:
    """Remove an incomplete checkpoint from a failed run.

    Args:
        checkpoint_dir: Directory path for the incomplete checkpoint.
    """
    path = Path(checkpoint_dir)
    if path.exists():
        shutil.rmtree(path)


def parse_epoch_value(value: str) -> tuple[int | None, str]:
    """Parse a checkpoint value into epoch and hash components.

    Handles both legacy format (just hash) and new format (epoch:hash).

    Args:
        value: The stored checkpoint value.

    Returns:
        Tuple of (epoch, hash). Epoch is None for legacy values.
    """
    if ":" in value:
        epoch_str, hash_str = value.split(":", 1)
        return int(epoch_str), hash_str
    return None, value


@dataclass
class BatchContext:
    """Context for batch LMDB operations within a single transaction.

    This class enables high-performance batch operations by:
    - Keeping a single transaction open for multiple reads
    - Batching writes with putmulti() for efficient commits
    - Avoiding transaction open/close overhead per operation

    Usage:
        with store.batch_transaction(write=True) as batch:
            for record in records:
                old_val = batch.get(type_name, qn)
                batch.put(type_name, qn, new_val)
                if len(batch._pending_puts) >= 10000:
                    batch.flush_puts()
            batch.flush_puts()
    """

    _txn: lmdb.Transaction
    _cursor: lmdb.Cursor
    _make_key: Callable[[str, str], bytes]
    _pending_puts: list[tuple[bytes, bytes]] = field(default_factory=list)

    def put(self, type_name: str, qualified_name: str, value: str) -> None:
        """Queue a put operation for batch write.

        Args:
            type_name: The asset type (e.g., "Table", "Column").
            qualified_name: The qualified name of the asset.
            value: The value to store (typically "epoch:hash").
        """
        self._pending_puts.append(
            (
                self._make_key(type_name, qualified_name),
                value.encode("utf-8"),
            )
        )

    def flush_puts(self) -> int:
        """Flush queued puts using putmulti.

        Returns:
            Number of items written.
        """
        if not self._pending_puts:
            return 0
        _consumed, added = self._cursor.putmulti(self._pending_puts)
        self._pending_puts.clear()
        return cast(int, added)

    def get(self, type_name: str, qualified_name: str) -> str | None:
        """Single get within transaction (avoids reopening).

        Args:
            type_name: The asset type.
            qualified_name: The qualified name of the asset.

        Returns:
            The stored value, or None if not found.
        """
        value = self._txn.get(self._make_key(type_name, qualified_name))
        return value.decode("utf-8") if value else None

    def delete(self, type_name: str, qualified_name: str) -> bool:
        """Delete within transaction.

        Args:
            type_name: The asset type.
            qualified_name: The qualified name of the asset.

        Returns:
            True if the entry existed and was deleted, False otherwise.
        """
        return cast(bool, self._txn.delete(self._make_key(type_name, qualified_name)))


class CheckpointStore:
    """LMDB-based key-value store for checkpoint data.

    Keys are composite: f"{type_name}:{qualified_name}"
    Values are content hashes (SHA256 truncated to 16 chars).

    The store is designed for memory-efficient storage and retrieval
    of large numbers of records, making it suitable for diffing
    datasets with millions of rows.

    Args:
        path: Directory path for the LMDB database.
        map_size: Maximum size of the database in bytes (default 1GB).
    """

    def __init__(
        self, path: str | Path, map_size: int = 107_374_182_400
    ) -> None:  # 100GB default
        """Initialize LMDB checkpoint store.

        Args:
            path: Directory path for the LMDB database.
            map_size: Maximum size of the database in bytes (default 100GB).
                      LMDB uses sparse files on most systems, so this doesn't
                      allocate space upfront. For 100M+ records, 100GB provides
                      headroom for keys (~100 bytes) and values (~50 bytes).
        """
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self._env = lmdb.open(str(self.path), map_size=map_size)

    @staticmethod
    def make_key(type_name: str, qualified_name: str) -> bytes:
        """Create composite key from type_name and qualified_name.

        Args:
            type_name: The asset type (e.g., "Table", "Column").
            qualified_name: The qualified name of the asset.

        Returns:
            UTF-8 encoded key in format "type_name:qualified_name".
        """
        return f"{type_name}:{qualified_name}".encode()

    @staticmethod
    def parse_key(key: bytes) -> tuple[str, str]:
        """Parse composite key back to type_name and qualified_name.

        Args:
            key: UTF-8 encoded key in format "type_name:qualified_name".

        Returns:
            Tuple of (type_name, qualified_name).
        """
        key_str = key.decode("utf-8")
        type_name, qualified_name = key_str.split(":", 1)
        return type_name, qualified_name

    def get(self, type_name: str, qualified_name: str) -> str | None:
        """Get hash for a type_name + qualified_name pair.

        Args:
            type_name: The asset type.
            qualified_name: The qualified name of the asset.

        Returns:
            The stored hash, or None if not found.
        """
        with self._env.begin() as txn:
            value = txn.get(self.make_key(type_name, qualified_name))
            return value.decode("utf-8") if value else None

    def put(self, type_name: str, qualified_name: str, content_hash: str) -> None:
        """Store hash for a type_name + qualified_name pair.

        Args:
            type_name: The asset type.
            qualified_name: The qualified name of the asset.
            content_hash: The content hash to store.
        """
        with self._env.begin(write=True) as txn:
            txn.put(
                self.make_key(type_name, qualified_name),
                content_hash.encode("utf-8"),
            )

    def delete(self, type_name: str, qualified_name: str) -> bool:
        """Delete entry for a type_name + qualified_name pair.

        Args:
            type_name: The asset type.
            qualified_name: The qualified name of the asset.

        Returns:
            True if the entry existed and was deleted, False otherwise.
        """
        with self._env.begin(write=True) as txn:
            return cast(bool, txn.delete(self.make_key(type_name, qualified_name)))

    @contextmanager
    def batch_transaction(self, write: bool = False) -> Iterator[BatchContext]:
        """Context manager for batched operations within a single transaction.

        This provides significant performance improvement for high-volume
        workloads by avoiding transaction open/close overhead per operation.

        Args:
            write: Whether this transaction needs write access.

        Yields:
            BatchContext for performing batched get/put operations.

        Example:
            with store.batch_transaction(write=True) as batch:
                for record in records:
                    old_val = batch.get(type_name, qn)
                    batch.put(type_name, qn, new_val)
                    if len(batch._pending_puts) >= 10000:
                        batch.flush_puts()
                batch.flush_puts()
        """
        with self._env.begin(write=write) as txn:
            cursor = txn.cursor()
            yield BatchContext(txn, cursor, self.make_key)

    def delete_stale_epochs(self, current_epoch: int) -> Iterator[tuple[str, str]]:
        """Delete entries with epoch < current_epoch.

        Scans all entries to identify stale ones, then deletes them.
        Memory usage is proportional to the number of deletions, not total entries.

        Args:
            current_epoch: The current epoch timestamp. Entries with
                          older epochs will be deleted.

        Yields:
            Tuples of (type_name, qualified_name) for each deleted entry.
        """
        # First pass: collect keys to delete (iterating while deleting causes issues)
        keys_to_delete: list[tuple[bytes, str, str]] = []
        with self._env.begin() as txn:
            cursor = txn.cursor()
            for key, value in cursor.iternext(keys=True, values=True):
                value_str = value.decode("utf-8")
                epoch, _ = parse_epoch_value(value_str)
                # Delete if epoch is older than current, or if legacy (no epoch)
                if epoch is None or epoch < current_epoch:
                    type_name, qualified_name = self.parse_key(key)
                    keys_to_delete.append((key, type_name, qualified_name))

        # Second pass: delete collected keys
        with self._env.begin(write=True) as txn:
            for key, type_name, qualified_name in keys_to_delete:
                txn.delete(key)
                yield type_name, qualified_name

    def keys(self) -> Iterator[tuple[str, str]]:
        """Iterate all (type_name, qualified_name) pairs in the store.

        Yields:
            Tuples of (type_name, qualified_name).
        """
        with self._env.begin() as txn:
            cursor = txn.cursor()
            for key in cursor.iternext(keys=True, values=False):
                yield self.parse_key(key)

    def items(self) -> Iterator[tuple[str, str, str]]:
        """Iterate all (type_name, qualified_name, hash) tuples in the store.

        Yields:
            Tuples of (type_name, qualified_name, content_hash).
        """
        with self._env.begin() as txn:
            cursor = txn.cursor()
            for key, value in cursor.iternext(keys=True, values=True):
                type_name, qualified_name = self.parse_key(key)
                yield type_name, qualified_name, value.decode("utf-8")

    def __len__(self) -> int:
        """Return the number of entries in the store."""
        with self._env.begin() as txn:
            return cast(int, txn.stat()["entries"])

    def close(self) -> None:
        """Close the LMDB environment."""
        self._env.close()

    def __enter__(self) -> CheckpointStore:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


def compute_content_hash(data: dict[str, str | None]) -> str:
    """Compute xxHash3_128 hash of sorted column values.

    This function creates a deterministic hash of a record's content,
    suitable for detecting changes between pipeline runs.

    Uses xxHash3_128 which is ~54x faster than SHA256 while providing
    128 bits of output (zero practical collision risk at 100M+ records).

    Args:
        data: Dictionary of field names to values. None values are
              converted to empty strings.

    Returns:
        32-character hexadecimal hash string (128 bits).

    Example:
        >>> compute_content_hash({"name": "foo", "description": "bar"})
        'a1b2c3d4e5f67890abcdef1234567890'
    """
    # Sort keys for deterministic hashing
    items = sorted(data.items())
    # Convert None to empty string for consistent hashing
    content = "|".join(f"{k}={v if v is not None else ''}" for k, v in items)
    return xxhash.xxh3_128_hexdigest(content.encode("utf-8"))
