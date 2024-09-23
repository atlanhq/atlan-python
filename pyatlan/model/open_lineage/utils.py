from __future__ import annotations

import secrets
import time
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from datetime import datetime


def _build_uuidv7(timestamp: int, node: int) -> UUID:
    # merge timestamp and node into 128-bit UUID
    # timestamp is first 48 bits, node is last 80 bits
    uuid_int = (timestamp & 0xFFFFFFFFFFFF) << 80
    uuid_int |= node & 0xFFFFFFFFFFFFFFFFFFFF

    # Set the version number (4 bit).
    version = 7
    uuid_int &= ~(0xF000 << 64)
    uuid_int |= version << 76

    # Set the variant (2 bit) to RFC 4122.
    uuid_int &= ~(0xC000 << 48)
    uuid_int |= 0x8000 << 48

    return UUID(int=uuid_int)


def generate_new_uuid(instant: datetime | None = None) -> UUID:
    """Generate new UUID for an instant of time. Each function call returns a new UUID value.

    UUID version is an implementation detail, and **should not** be relied on.
    For now it is [UUIDv7](https://datatracker.ietf.org/doc/rfc9562/), so for increasing instant values,
    returned UUID is always greater than previous one.

    Using uuid6 lib implementation (MIT License), with few changes:
    * https://github.com/oittaa/uuid6-python/blob/4f879849178b8a7a564f7cb76c3f7a6e5228d9ed/src/uuid6/__init__.py#L128-L147 # noqa
    * https://github.com/oittaa/uuid6-python/blob/4f879849178b8a7a564f7cb76c3f7a6e5228d9ed/src/uuid6/__init__.py#L46-L51


    :param instant: instant of time used to generate UUID. If not provided, current time is used.
    :return: UUID
    """

    timestamp_ms = (
        int(instant.timestamp() * 1000) if instant else time.time_ns() // 10**6
    )
    node = secrets.randbits(76)
    return _build_uuidv7(timestamp_ms, node)
