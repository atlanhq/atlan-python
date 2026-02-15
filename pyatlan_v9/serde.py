# Auto-generated support module for PythonMsgspecRenderer.pkl
"""Serialization/deserialization utilities using msgspec."""

from __future__ import annotations

from typing import Any, TypeVar

import msgspec

T = TypeVar("T")


class Serde:
    """
    Serialization/deserialization helper using msgspec encoders/decoders.

    Reuses encoder/decoder instances for better performance.
    """

    def __init__(self) -> None:
        self._encoder = msgspec.json.Encoder()
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
