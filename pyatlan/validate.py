# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
Custom ``validate_arguments`` decorator that replaces Pydantic v1's
``@validate_arguments`` with a lightweight, framework-agnostic version.

This decorator validates function arguments against their type annotations
and supports **both** Pydantic ``BaseModel`` and ``msgspec.Struct`` model
instances.  It also handles Pydantic constrained types (``constr``,
``StrictStr``) for backward compatibility.
"""

from __future__ import annotations

import functools
import inspect
import typing
from enum import Enum
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

import msgspec

# ---------------------------------------------------------------------------
# Pydantic constrained-type detection (for backward compat with constr, etc.)
# ---------------------------------------------------------------------------
try:
    from pydantic.v1 import ConstrainedStr
    from pydantic.v1.types import (  # noqa: F401
        ConstrainedInt,
        StrictBool,
        StrictInt,
        StrictStr,
    )

    _HAS_PYDANTIC_TYPES = True
except ImportError:  # pragma: no cover
    _HAS_PYDANTIC_TYPES = False
    ConstrainedStr = None  # type: ignore[assignment, misc]
    ConstrainedInt = None  # type: ignore[assignment, misc]
    StrictBool = None  # type: ignore[assignment, misc]
    StrictInt = None  # type: ignore[assignment, misc]

try:
    from pydantic.v1 import BaseModel as PydanticBaseModel
except ImportError:  # pragma: no cover
    PydanticBaseModel = None  # type: ignore[assignment, misc]


# ---------------------------------------------------------------------------
# Helper: model-compatible isinstance check
# ---------------------------------------------------------------------------
def _is_model_instance(value: Any, expected_type: type) -> bool:
    """
    Check if *value* is an instance of *expected_type*, accepting both
    Pydantic BaseModel and msgspec.Struct instances whose MRO includes a
    class with the same name as *expected_type*.
    """
    # Standard isinstance first
    if isinstance(value, expected_type):
        return True

    # For msgspec.Struct, match by class name in MRO
    if isinstance(value, msgspec.Struct):
        v9_mro_names = {cls.__name__ for cls in type(value).__mro__}
        if expected_type.__name__ in v9_mro_names:
            return True

    # For Pydantic BaseModel, also match by name (reverse direction)
    if PydanticBaseModel is not None and isinstance(value, PydanticBaseModel):
        pydantic_mro_names = {cls.__name__ for cls in type(value).__mro__}
        if expected_type.__name__ in pydantic_mro_names:
            return True

    # For unittest.mock.Mock objects with a spec, check the spec class MRO
    spec_class = getattr(value, "_spec_class", None)
    if spec_class is not None:
        try:
            if issubclass(spec_class, expected_type):
                return True
        except TypeError:
            pass
        spec_mro_names = {cls.__name__ for cls in spec_class.__mro__}
        if expected_type.__name__ in spec_mro_names:
            return True

    # Generic fallback: match by class name in MRO for any class
    # (handles dataclasses, plain classes, etc. with identical names
    # across legacy and v9 modules)
    value_mro_names = {cls.__name__ for cls in type(value).__mro__}
    if expected_type.__name__ in value_mro_names:
        return True

    return False


def _is_model_subclass(value: type, expected_type: type) -> bool:
    """
    Check if *value* (a class) is a subclass of *expected_type*, accepting
    both Pydantic and msgspec model hierarchies via MRO name matching.
    """
    try:
        if issubclass(value, expected_type):
            return True
    except TypeError:
        pass

    # Cross-framework subclass check by name
    value_mro_names = {cls.__name__ for cls in value.__mro__}
    if expected_type.__name__ in value_mro_names:
        return True

    return False


# ---------------------------------------------------------------------------
# Constrained string validation
# ---------------------------------------------------------------------------
def _validate_constrained_str(value: Any, hint: type) -> Tuple[Any, Optional[str]]:
    """
    Validate and optionally transform a value against a Pydantic ConstrainedStr
    type (``constr``, ``StrictStr``).

    Returns ``(transformed_value, error_message_or_None)``.
    """
    if not _HAS_PYDANTIC_TYPES or ConstrainedStr is None:
        # No pydantic constrained types available — just check str
        if value is None:
            return value, "none is not an allowed value"
        if not isinstance(value, str):
            return value, "str type expected"
        return value, None

    if not isinstance(hint, type) or not issubclass(hint, ConstrainedStr):
        return value, None  # Not a constrained str type

    # None is never a valid constrained string
    if value is None:
        return value, "none is not an allowed value"

    # Strict check
    strict = getattr(hint, "strict", False)
    if strict and not isinstance(value, str):
        return value, "str type expected"

    # Coerce to str if not strict
    if not isinstance(value, str):
        try:
            value = str(value)
        except (ValueError, TypeError):
            return value, "str type expected"

    # strip_whitespace
    if getattr(hint, "strip_whitespace", False):
        value = value.strip()

    # min_length
    min_length = getattr(hint, "min_length", None)
    if min_length is not None and len(value) < min_length:
        return value, f"ensure this value has at least {min_length} characters"

    # max_length
    max_length = getattr(hint, "max_length", None)
    if max_length is not None and len(value) > max_length:
        return value, f"ensure this value has at most {max_length} characters"

    # regex
    regex = getattr(hint, "regex", None)
    if regex is not None:
        import re

        if not re.match(regex, value):
            return value, f"string does not match regex '{regex}'"

    return value, None


# ---------------------------------------------------------------------------
# Core type checker
# ---------------------------------------------------------------------------
def _check_type(value: Any, hint: Any) -> Tuple[Any, Optional[str]]:
    """
    Check if *value* matches the type *hint*.

    Returns ``(possibly_transformed_value, error_message_or_None)``.
    Transformation happens for constrained string types (strip_whitespace).
    """
    # Handle TypeVar — resolve to its bound (or Any if unbound)
    if isinstance(hint, typing.TypeVar):
        bound = hint.__bound__
        if bound is not None:
            return _check_type(value, bound)
        constraints = hint.__constraints__
        if constraints:
            # Check against each constraint as a Union
            for c in constraints:
                result, err = _check_type(value, c)
                if err is None:
                    return result, None
            return value, f"value does not match any constraint of TypeVar {hint}"
        # Unbound TypeVar — accept anything
        return value, None

    # Handle None type
    if hint is type(None):
        if value is None:
            return value, None
        return value, "none is not an allowed value"

    # Handle typing.Any
    if hint is typing.Any:
        return value, None

    # Handle Union[X, Y, ...] including Optional[X]
    origin = typing.get_origin(hint)
    args = typing.get_args(hint)

    if origin is Union:
        # Quick None check: if None is not in the Union, reject it directly
        has_none_type = type(None) in args
        if value is None and not has_none_type:
            return value, "none is not an allowed value"

        # Try each member; return on first success
        last_errors: list = []
        for arg in args:
            result, err = _check_type(value, arg)
            if err is None:
                return result, None
            last_errors.append((arg, err))

        non_none_args = [a for a in args if a is not type(None)]
        non_none_errors = [(a, e) for a, e in last_errors if a is not type(None)]

        # For Optional[X] (Union[X, None]) where value is not None,
        # report the error from the non-None branch directly (matches Pydantic)
        if len(non_none_args) == 1:
            return value, non_none_errors[0][1]

        # If any branch produced a "partial match" error (list item error),
        # report that specific error instead of the generic Union message.
        # This handles Union[Asset, List[Asset]] with [123] → "-> 0\n  ..."
        for _, err in non_none_errors:
            if err.startswith("-> "):
                return value, err

        # For general Union, report what was expected using short type names
        type_names = []
        for arg in args:
            if arg is type(None):
                type_names.append("None")
            elif isinstance(arg, type):
                type_names.append(arg.__name__)
            else:
                # Simplify generic types: typing.List[module.Asset] → List[Asset]
                inner_args = typing.get_args(arg)
                inner_origin = typing.get_origin(arg)
                if inner_origin is list and inner_args:
                    inner_name = (
                        inner_args[0].__name__
                        if isinstance(inner_args[0], type)
                        else str(inner_args[0])
                    )
                    type_names.append(f"List[{inner_name}]")
                else:
                    arg_str = str(arg).replace("typing.", "")
                    type_names.append(arg_str)
        return value, f"value is not a valid {' or '.join(type_names)}"

    # Handle List[X]
    if origin is list:
        if value is None:
            return value, "none is not an allowed value"
        if not isinstance(value, list):
            return value, "value is not a valid list"
        if args:
            transformed = []
            for i, item in enumerate(value):
                item_result, err = _check_type(item, args[0])
                if err is not None:
                    # Use Pydantic's "-> N" format for list item errors
                    return value, f"-> {i}\n  {err}"
                transformed.append(item_result)
            return transformed, None
        return value, None

    # Handle Set[X]
    if origin is set:
        if not isinstance(value, (set, frozenset)):
            return value, "value is not a valid set"
        if args:
            for item in value:
                _, err = _check_type(item, args[0])
                if err is not None:
                    return value, f"set item: {err}"
        return value, None

    # Handle Dict[K, V]
    if origin is dict:
        if value is None:
            return value, "none is not an allowed value"
        if not isinstance(value, dict):
            return value, "value is not a valid dict"
        if args and len(args) >= 2:
            key_hint, value_hint = args
            for k, v in value.items():
                _, err_k = _check_type(k, key_hint)
                if err_k is not None:
                    return value, f"-> __key__\n  {err_k}"
                _, err_v = _check_type(v, value_hint)
                if err_v is not None:
                    return value, f"-> {k}\n  {err_v}"
        return value, None

    # Handle Tuple[X, ...]
    if origin is tuple:
        if not isinstance(value, tuple):
            return value, "value is not a valid tuple"
        return value, None

    # Handle Type[X] — checking that value is a class and a subclass of X
    if origin is type:
        if value is None:
            return value, "none is not an allowed value"
        if not isinstance(value, type):
            return value, "a class is expected"
        if args:
            expected = args[0]
            # Resolve TypeVar to its bound
            if isinstance(expected, typing.TypeVar):
                expected = expected.__bound__ if expected.__bound__ else object
            if not _is_model_subclass(value, expected):
                return value, f"value is not a subclass of {expected.__name__}"
        return value, None

    # Handle Callable
    if origin is not None and (
        str(origin).startswith("typing.Callable")
        or str(hint).startswith("typing.Callable")
    ):
        if callable(value):
            return value, None
        return value, "value is not callable"

    # Handle plain types (int, str, bool, float, Enum, model classes, etc.)
    if isinstance(hint, type):
        # None is never valid for a non-NoneType hint (matches Pydantic behaviour)
        if value is None and hint is not type(None):
            return value, "none is not an allowed value"

        # Check for Pydantic constrained string types first
        if _HAS_PYDANTIC_TYPES and ConstrainedStr and issubclass(hint, ConstrainedStr):
            return _validate_constrained_str(value, hint)

        # StrictStr — must be exactly str
        if _HAS_PYDANTIC_TYPES and hint is StrictStr:
            if isinstance(value, str):
                return value, None
            return value, "str type expected"

        # StrictBool — must be exactly bool (no int coercion)
        if _HAS_PYDANTIC_TYPES and hint is StrictBool:
            if isinstance(value, bool):
                return value, None
            return value, "value is not a valid boolean"

        # StrictInt — must be exactly int (no float coercion)
        if _HAS_PYDANTIC_TYPES and hint is StrictInt:
            if isinstance(value, bool):
                return value, "value is not a valid integer"
            if isinstance(value, int):
                return value, None
            return value, "value is not a valid integer"

        # ConstrainedInt — accept int values
        if _HAS_PYDANTIC_TYPES and ConstrainedInt and issubclass(hint, ConstrainedInt):
            if isinstance(value, bool):
                return value, "value is not a valid integer"
            if isinstance(value, int):
                return value, None
            return value, "value is not a valid integer"

        # str check — Pydantic says "str type expected" for non-str values
        if hint is str:
            if isinstance(value, str):
                return value, None
            return value, "str type expected"

        # Bool check — accept bool and int (Pydantic coerces int → bool)
        if hint is bool:
            if isinstance(value, bool):
                return value, None
            if isinstance(value, int):
                return bool(value), None
            return value, "value is not a valid boolean"

        # Enum check
        if isinstance(hint, type) and issubclass(hint, Enum):
            if isinstance(value, hint):
                return value, None
            # Try coercion from value
            try:
                return hint(value), None
            except (ValueError, KeyError):
                return (
                    value,
                    f"value is not a valid enumeration member; permitted: {[e.value for e in hint]}",
                )

        # Model instance check (Pydantic + msgspec compatible)
        if _is_model_instance(value, hint):
            return value, None

        # Standard isinstance for everything else (str, int, float, etc.)
        if isinstance(value, hint):
            return value, None

        # Use Pydantic's "instance of X expected" for non-builtin types
        _builtin_types = (str, int, float, bytes, bytearray, memoryview)
        if hint not in _builtin_types:
            return value, f"instance of {hint.__name__} expected"

        return value, f"value is not a valid {hint.__name__}"

    # For anything we can't resolve (forward refs, complex generics), pass through
    return value, None


# ---------------------------------------------------------------------------
# The decorator
# ---------------------------------------------------------------------------
def validate_arguments(
    func: Optional[Callable] = None,
    *,
    config: Optional[Dict[str, Any]] = None,
) -> Callable:
    """
    Decorator that validates function arguments against their type annotations.

    Compatible with both Pydantic ``BaseModel`` and ``msgspec.Struct`` model
    instances.  Replaces ``pydantic.v1.validate_arguments`` with a
    framework-agnostic implementation.

    Supports:
    - Basic types: ``str``, ``int``, ``float``, ``bool``
    - Container types: ``List[X]``, ``Set[X]``, ``Dict[K,V]``, ``Optional[X]``, ``Union[X,Y]``
    - ``Type[X]`` (subclass checks)
    - ``Enum`` subclasses
    - Pydantic constrained types: ``constr``, ``StrictStr``
    - Model types: accepts both Pydantic and msgspec instances via MRO name matching
    - ``config=dict(arbitrary_types_allowed=True)`` is accepted but is a no-op

    Usage::

        @validate_arguments
        def my_func(name: str, count: int = 0) -> str:
            ...

        @validate_arguments(config=dict(arbitrary_types_allowed=True))
        def my_func(entity: Asset) -> None:
            ...
    """

    def decorator(fn: Callable) -> Callable:
        # Resolve type hints once at decoration time
        try:
            hints = typing.get_type_hints(fn)
        except Exception:
            hints = getattr(fn, "__annotations__", {}).copy()

        sig = inspect.signature(fn)
        # Filter out 'return' from hints
        param_hints = {k: v for k, v in hints.items() if k != "return"}

        # Pre-compute PascalCase name (matching Pydantic's convention)
        pascal_name = "".join(
            part.capitalize() for part in fn.__name__.split("_")
        )

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Use bind_partial to validate provided args even when some
            # are missing (matches Pydantic's validate-then-report behaviour)
            try:
                bound = sig.bind_partial(*args, **kwargs)
            except TypeError as e:
                raise ValueError(
                    f"1 validation error for {pascal_name}\n{e}"
                ) from None
            bound.apply_defaults()

            errors = []
            transformed = dict(bound.arguments)
            has_transforms = False

            for name, value in bound.arguments.items():
                # Skip 'self' and 'cls'
                if name in ("self", "cls"):
                    continue
                if name not in param_hints:
                    continue

                hint = param_hints[name]
                result, err = _check_type(value, hint)

                if err is not None:
                    # Match Pydantic v1 error format exactly:
                    # "N validation error for PascalName\nfield\n  message"
                    errors.append((name, err))
                elif result is not value:
                    # Value was transformed (e.g., enum coercion, strip_whitespace)
                    transformed[name] = result
                    has_transforms = True

            if errors:
                count = len(errors)
                suffix = "s" if count > 1 else ""
                lines = [
                    f"{count} validation error{suffix} for {pascal_name}"
                ]
                for field_name, err_msg in errors:
                    if err_msg.startswith("-> "):
                        # List item error: "-> 0\n  actual_error"
                        # Format as: "field -> 0\n  actual_error"
                        lines.append(f"{field_name} {err_msg}")
                    else:
                        lines.append(field_name)
                        lines.append(f"  {err_msg}")
                raise ValueError("\n".join(lines))

            # After validation, check for missing required args
            # (bind_partial doesn't complain about missing args)
            try:
                sig.bind(*args, **kwargs)
            except TypeError as e:
                raise ValueError(
                    f"1 validation error for {pascal_name}\n{e}"
                ) from None

            # Re-bind with potentially transformed values
            if has_transforms:
                # Rebuild args/kwargs with transformed values
                new_args = []
                new_kwargs = {}
                for param_name, param in sig.parameters.items():
                    if param_name in transformed:
                        if param.kind in (
                            inspect.Parameter.POSITIONAL_ONLY,
                            inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        ):
                            new_args.append(transformed[param_name])
                        else:
                            new_kwargs[param_name] = transformed[param_name]
                return fn(*new_args, **new_kwargs)

            return fn(*args, **kwargs)

        # Store original function for introspection
        wrapper.__wrapped__ = fn  # type: ignore[attr-defined]
        return wrapper

    if func is not None:
        # Called as @validate_arguments (without parentheses)
        return decorator(func)

    # Called as @validate_arguments(...) (with config or parentheses)
    return decorator
