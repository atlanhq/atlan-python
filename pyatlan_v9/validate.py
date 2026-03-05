# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
Custom ``validate_arguments`` decorator for pyatlan_v9.

This decorator validates function arguments against their type annotations
and supports **both** Pydantic ``BaseModel`` and ``msgspec.Struct`` model
instances.  Used only by pyatlan_v9; legacy pyatlan uses pydantic.v1.validate_arguments.
"""

from __future__ import annotations

import functools
import inspect
import typing
from enum import Enum
from typing import Any, Callable, Dict, Optional, Tuple, Union

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
    if isinstance(value, expected_type):
        return True
    if isinstance(value, msgspec.Struct):
        v9_mro_names = {cls.__name__ for cls in type(value).__mro__}
        if expected_type.__name__ in v9_mro_names:
            return True
    if PydanticBaseModel is not None and isinstance(value, PydanticBaseModel):
        pydantic_mro_names = {cls.__name__ for cls in type(value).__mro__}
        if expected_type.__name__ in pydantic_mro_names:
            return True
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
    value_mro_names = {cls.__name__ for cls in type(value).__mro__}
    if expected_type.__name__ in value_mro_names:
        return True
    return False


def _is_model_subclass(value: type, expected_type: type) -> bool:
    try:
        if issubclass(value, expected_type):
            return True
    except TypeError:
        pass
    value_mro_names = {cls.__name__ for cls in value.__mro__}
    if expected_type.__name__ in value_mro_names:
        return True
    return False


def _validate_constrained_str(value: Any, hint: type) -> Tuple[Any, Optional[str]]:
    if not _HAS_PYDANTIC_TYPES or ConstrainedStr is None:
        if value is None:
            return value, "none is not an allowed value"
        if not isinstance(value, str):
            return value, "str type expected"
        return value, None
    if not isinstance(hint, type) or not issubclass(hint, ConstrainedStr):
        return value, None
    if value is None:
        return value, "none is not an allowed value"
    strict = getattr(hint, "strict", False)
    if strict and not isinstance(value, str):
        return value, "str type expected"
    if not isinstance(value, str):
        try:
            value = str(value)
        except (ValueError, TypeError):
            return value, "str type expected"
    if getattr(hint, "strip_whitespace", False):
        value = value.strip()
    min_length = getattr(hint, "min_length", None)
    if min_length is not None and len(value) < min_length:
        return value, f"ensure this value has at least {min_length} characters"
    max_length = getattr(hint, "max_length", None)
    if max_length is not None and len(value) > max_length:
        return value, f"ensure this value has at most {max_length} characters"
    regex = getattr(hint, "regex", None)
    if regex is not None:
        import re
        if not re.match(regex, value):
            return value, f"string does not match regex '{regex}'"
    return value, None


def _check_type(value: Any, hint: Any) -> Tuple[Any, Optional[str]]:
    if isinstance(hint, typing.TypeVar):
        bound = hint.__bound__
        if bound is not None:
            return _check_type(value, bound)
        constraints = hint.__constraints__
        if constraints:
            for c in constraints:
                result, err = _check_type(value, c)
                if err is None:
                    return result, None
            return value, f"value does not match any constraint of TypeVar {hint}"
        return value, None
    if hint is type(None):
        if value is None:
            return value, None
        return value, "none is not an allowed value"
    if hint is typing.Any:
        return value, None
    origin = typing.get_origin(hint)
    args = typing.get_args(hint)
    if origin is Union:
        has_none_type = type(None) in args
        if value is None and not has_none_type:
            return value, "none is not an allowed value"
        last_errors: list = []
        for arg in args:
            result, err = _check_type(value, arg)
            if err is None:
                return result, None
            last_errors.append((arg, err))
        non_none_args = [a for a in args if a is not type(None)]
        non_none_errors = [(a, e) for a, e in last_errors if a is not type(None)]
        if len(non_none_args) == 1:
            return value, non_none_errors[0][1]
        for _, err in non_none_errors:
            if err.startswith("-> "):
                return value, err
        type_names = []
        for arg in args:
            if arg is type(None):
                type_names.append("None")
            elif isinstance(arg, type):
                type_names.append(arg.__name__)
            else:
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
                    type_names.append(str(arg).replace("typing.", ""))
        return value, f"value is not a valid {' or '.join(type_names)}"
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
                    return value, f"-> {i}\n  {err}"
                transformed.append(item_result)
            return transformed, None
        return value, None
    if origin is set:
        if not isinstance(value, (set, frozenset)):
            return value, "value is not a valid set"
        if args:
            for item in value:
                _, err = _check_type(item, args[0])
                if err is not None:
                    return value, f"set item: {err}"
        return value, None
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
    if origin is tuple:
        if not isinstance(value, tuple):
            return value, "value is not a valid tuple"
        return value, None
    if origin is type:
        if value is None:
            return value, "none is not an allowed value"
        if not isinstance(value, type):
            return value, "a class is expected"
        if args:
            expected = args[0]
            if isinstance(expected, typing.TypeVar):
                expected = expected.__bound__ if expected.__bound__ else object
            if not _is_model_subclass(value, expected):
                return value, f"value is not a subclass of {expected.__name__}"
        return value, None
    if origin is not None and (
        str(origin).startswith("typing.Callable")
        or str(hint).startswith("typing.Callable")
    ):
        if callable(value):
            return value, None
        return value, "value is not callable"
    if isinstance(hint, type):
        if value is None and hint is not type(None):
            return value, "none is not an allowed value"
        if _HAS_PYDANTIC_TYPES and ConstrainedStr and issubclass(hint, ConstrainedStr):
            return _validate_constrained_str(value, hint)
        if _HAS_PYDANTIC_TYPES and hint is StrictStr:
            if isinstance(value, str):
                return value, None
            return value, "str type expected"
        if _HAS_PYDANTIC_TYPES and hint is StrictBool:
            if isinstance(value, bool):
                return value, None
            return value, "value is not a valid boolean"
        if _HAS_PYDANTIC_TYPES and hint is StrictInt:
            if isinstance(value, bool):
                return value, "value is not a valid integer"
            if isinstance(value, int):
                return value, None
            return value, "value is not a valid integer"
        if _HAS_PYDANTIC_TYPES and ConstrainedInt and issubclass(hint, ConstrainedInt):
            if isinstance(value, bool):
                return value, "value is not a valid integer"
            if isinstance(value, int):
                return value, None
            return value, "value is not a valid integer"
        if hint is str:
            if isinstance(value, str):
                return value, None
            return value, "str type expected"
        if hint is bool:
            if isinstance(value, bool):
                return value, None
            if isinstance(value, int):
                return bool(value), None
            return value, "value is not a valid boolean"
        if isinstance(hint, type) and issubclass(hint, Enum):
            if isinstance(value, hint):
                return value, None
            try:
                return hint(value), None
            except (ValueError, KeyError):
                return (
                    value,
                    f"value is not a valid enumeration member; permitted: {[e.value for e in hint]}",
                )
        if _is_model_instance(value, hint):
            return value, None
        if isinstance(value, hint):
            return value, None
        _builtin_types = (str, int, float, bytes, bytearray, memoryview)
        if hint not in _builtin_types:
            return value, f"instance of {hint.__name__} expected"
        return value, f"value is not a valid {hint.__name__}"
    return value, None


def validate_arguments(
    func: Optional[Callable] = None,
    *,
    config: Optional[Dict[str, Any]] = None,
) -> Callable:
    """Decorator that validates function arguments against their type annotations (v9 only)."""

    def decorator(fn: Callable) -> Callable:
        try:
            hints = typing.get_type_hints(fn)
        except Exception:
            hints = getattr(fn, "__annotations__", {}).copy()
        sig = inspect.signature(fn)
        param_hints = {k: v for k, v in hints.items() if k != "return"}
        pascal_name = "".join(part.capitalize() for part in fn.__name__.split("_"))

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                bound = sig.bind_partial(*args, **kwargs)
            except TypeError as e:
                raise ValueError(f"1 validation error for {pascal_name}\n{e}") from None
            bound.apply_defaults()
            errors = []
            transformed = dict(bound.arguments)
            has_transforms = False
            for name, value in bound.arguments.items():
                if name in ("self", "cls"):
                    continue
                if name not in param_hints:
                    continue
                hint = param_hints[name]
                result, err = _check_type(value, hint)
                if err is not None:
                    errors.append((name, err))
                elif result is not value:
                    transformed[name] = result
                    has_transforms = True
            if errors:
                count = len(errors)
                suffix = "s" if count > 1 else ""
                lines = [f"{count} validation error{suffix} for {pascal_name}"]
                for field_name, err_msg in errors:
                    if err_msg.startswith("-> "):
                        lines.append(f"{field_name} {err_msg}")
                    else:
                        lines.append(field_name)
                        lines.append(f"  {err_msg}")
                raise ValueError("\n".join(lines))
            try:
                sig.bind(*args, **kwargs)
            except TypeError as e:
                raise ValueError(f"1 validation error for {pascal_name}\n{e}") from None
            if has_transforms:
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

        wrapper.__wrapped__ = fn  # type: ignore[attr-defined]
        return wrapper

    if func is not None:
        return decorator(func)
    return decorator
