# Auto-generated support module for PythonMsgspecRenderer.pkl
"""Serialization/deserialization utilities using msgspec."""

from __future__ import annotations

import datetime
from enum import Enum
from typing import Any, TypeVar

import msgspec

T = TypeVar("T")


def _enc_hook(obj: Any) -> Any:
    """Handle custom types that msgspec cannot natively encode."""
    if obj.__class__.__name__ == "AtlanTagName":
        return str(obj)
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, datetime.date):
        dt = datetime.datetime.combine(obj, datetime.time.min)
        return int(dt.timestamp() * 1000)
    if isinstance(obj, datetime.datetime):
        return int(obj.timestamp() * 1000)
    if hasattr(obj, "dict") and hasattr(obj, "__fields__"):
        return obj.dict(by_alias=True, exclude_none=True)
    raise NotImplementedError(f"Cannot serialize {type(obj)}")


class Serde:
    """
    Serialization/deserialization helper using msgspec encoders/decoders.

    Reuses encoder/decoder instances for better performance.
    """

    def __init__(self) -> None:
        self._encoder = msgspec.json.Encoder(enc_hook=_enc_hook)
        self._decoders: dict[type[Any], msgspec.json.Decoder[Any]] = {}

    def encode(self, obj: Any) -> bytes:
        """Encode an object to JSON bytes."""
        return self._encoder.encode(obj)

    def decode(self, data: bytes, type_: type[T]) -> T:
        """Decode JSON bytes to the specified type."""
        if type_ not in self._decoders:
            self._decoders[type_] = msgspec.json.Decoder(type_)
        return self._decoders[type_].decode(data)  # type: ignore[no-any-return]


# Singleton instance
_serde: Serde | None = None


def get_serde() -> Serde:
    """Get the shared Serde singleton instance."""
    global _serde
    if _serde is None:
        _serde = Serde()
    return _serde
