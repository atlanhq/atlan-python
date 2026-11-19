# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
"""Lenient coercion of values destined for ``str``-typed model slots.

Hand-maintained: unlike its neighbours, this module is **not** emitted by
``PythonMsgspecRenderer.pkl``.

Why this exists
---------------
Atlas's ``string`` type accepts anything and stores its stringification.  From
``AtlasBuiltInTypes.AtlasStringType`` in ``atlas-metastore``::

    public boolean isValidValue(Object obj) { return true; }
    public String getNormalizedValue(Object obj) {
        if (obj != null) { return obj.toString(); }
        return null;
    }

The generated models mirror the *declared* Atlas type — a typedef attribute of
type ``map<string,string>`` becomes ``Dict[str, str]``, and the entity-header
``customAttributes`` (``Map<String, String>`` on ``AtlasEntity``) becomes
``Dict[str, str]`` — but they cannot mirror that leniency, because ``msgspec``
enforces ``str`` exactly.  ``strict=False`` does not help: lax mode coerces
``str`` -> ``int``, never ``int`` -> ``str``.  A ``dec_hook`` does not help
either; it fires only for types ``msgspec`` cannot natively handle, so a
``str``/``int`` mismatch raises before any hook runs.

The result is a decoder that is stricter than the server it models.  A producer
that emits ``{"ordinal_position": 1}`` in ``customAttributes`` has its **whole
record** rejected here, while Atlas accepts it and stores ``"1"``.

So this module restores the server's leniency, opt-in, for callers decoding
payloads that have not yet been through Atlas's normalisation.

What it does
------------
The coercion plan is derived from the model itself via :mod:`msgspec.inspect`,
so it covers every ``str``-typed slot — plain ``str`` fields, ``Dict[str, str]``,
``List[Dict[str, str]]``, ``List[str]``, and the same shapes on nested related
structs — with no hand-maintained list of field names to fall behind.

Values are coerced to their **compact JSON text**, which matches
``getNormalizedValue`` for scalars (``1`` -> ``"1"``, ``true`` -> ``"true"``).
For a container in a string slot it does not: Atlas would store Java's
``Object.toString()`` (``{a=b}``); this emits ``{"a":"b"}``.  JSON is chosen
deliberately — it is the honest serialisation of a JSON value, and it round
trips.

``None`` is dropped from a slot that cannot hold it (``Dict[str, str]`` values,
and non-optional fields), and preserved where the model declares
``Optional``.  Dropping rather than stringifying is deliberate: a literal
``"None"``/``"null"`` is a value the producer never wrote.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

import msgspec
import msgspec.inspect as _inspect

__all__ = ["coerce_string_slots"]

_Coercer = Callable[[Any], Any]


class _Drop:
    """Sentinel: remove the key rather than decode a value it cannot hold."""

    __slots__ = ()

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return "<drop>"


_DROP = _Drop()

# One plan per model class, keyed by encoded (camelCase) field name.  Built
# lazily; entries are inserted *before* the class is walked so a cyclic type
# graph (``Related*`` structs reference each other) terminates.
_plans: Dict[type, Dict[str, _Coercer]] = {}


def _to_str(value: Any) -> Any:
    """Stringify one value the way Atlas's ``string`` type would."""
    if isinstance(value, str):
        return value
    return msgspec.json.encode(value).decode()


def _coerce_str_map(value: Any) -> Any:
    """Coerce a ``Dict[str, str]`` payload, dropping null values.

    A non-mapping payload is returned untouched: there is no sane coercion, and
    letting ``msgspec`` reject it keeps a genuine producer-side format change
    visible instead of inventing a value.
    """
    if not isinstance(value, dict):
        return value
    return {key: _to_str(item) for key, item in value.items() if item is not None}


def _coerce_sequence(inner: _Coercer) -> _Coercer:
    def coerce(value: Any) -> Any:
        if not isinstance(value, list):
            return value
        return [inner(item) for item in value]

    return coerce


def _coerce_struct(cls: type) -> _Coercer:
    def coerce(value: Any) -> Any:
        if isinstance(value, dict):
            coerce_string_slots(value, cls)
        return value

    return coerce


def _value_coercer(field_type: _inspect.Type) -> Optional[_Coercer]:
    """Build a coercer for one type, or ``None`` if it holds no ``str`` slot."""
    if isinstance(field_type, _inspect.StrType):
        return _to_str
    if isinstance(field_type, _inspect.DictType):
        if isinstance(field_type.value_type, _inspect.StrType):
            return _coerce_str_map
        return None
    if isinstance(field_type, (_inspect.ListType, _inspect.SetType)):
        inner = _value_coercer(field_type.item_type)
        return _coerce_sequence(inner) if inner is not None else None
    if isinstance(field_type, _inspect.StructType):
        # Resolved at call time, not build time, so a cyclic type graph is fine.
        return _coerce_struct(field_type.cls)
    if isinstance(field_type, _inspect.UnionType):
        for member in field_type.types:
            coercer = _value_coercer(member)
            if coercer is not None:
                return coercer
    return None


def _field_coercer(field_type: _inspect.Type) -> Optional[_Coercer]:
    inner = _value_coercer(field_type)
    if inner is None:
        return None
    nullable = isinstance(field_type, _inspect.UnionType) and any(
        isinstance(member, _inspect.NoneType) for member in field_type.types
    )

    def coerce(value: Any) -> Any:
        if value is None:
            return None if nullable else _DROP
        return inner(value)

    return coerce


def _plan_for(cls: type) -> Dict[str, _Coercer]:
    plan = _plans.get(cls)
    if plan is not None:
        return plan
    plan = {}
    # Publish before walking: a self-referential type graph resolves to this
    # same (eventually populated) dict instead of recursing forever.
    _plans[cls] = plan
    info = _inspect.type_info(cls)
    for field in getattr(info, "fields", ()):
        coercer = _field_coercer(field.type)
        if coercer is not None:
            plan[field.encode_name] = coercer
    return plan


def coerce_string_slots(data: Dict[str, Any], cls: type) -> Dict[str, Any]:
    """Coerce, in place, every value in ``data`` bound for a ``str`` slot of ``cls``.

    Args:
        data: A flattened entity dict, keyed by Atlas (camelCase) field names.
        cls: The model class ``data`` is about to be converted into.

    Returns:
        The same dict, mutated.
    """
    plan = _plan_for(cls)
    if not plan:
        return data
    for key in list(data):
        coercer = plan.get(key)
        if coercer is None:
            continue
        coerced = coercer(data[key])
        if coerced is _DROP:
            del data[key]
        else:
            data[key] = coerced
    return data
