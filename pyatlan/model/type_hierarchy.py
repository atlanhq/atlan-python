# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Atlas type hierarchy of asset types.

A generated asset class has exactly one Python parent: the first supertype its Atlas
typedef lists (see ``pyatlan.generator.class_generator``). An Atlas type can have several.
``SAPProcess`` is both an ``SAP`` and a ``Process`` in Atlas, but its class is
``class SAPProcess(SAP)``, so ``issubclass(SAPProcess, Process)`` is ``False`` even though
the class carries every ``Process`` attribute.

These helpers answer from the full Atlas supertype list instead, so code that needs to know
"is this a Process?" gets the same answer Atlas would give.

Example::

    from pyatlan.model.assets import Process, SAPProcess
    from pyatlan.model.type_hierarchy import is_subtype_of

    issubclass(SAPProcess, Process)       # False
    is_subtype_of(SAPProcess, Process)    # True
    is_subtype_of("SAPProcess", "SAP")    # True
"""

from functools import lru_cache
from typing import Dict, FrozenSet, List, Tuple, Type, Union

TypeOrName = Union[str, Type]


def _super_types() -> Dict[str, List[str]]:
    # Imported lazily: pyatlan.model.assets loads asset classes on demand, and some asset
    # modules import pyatlan.model helpers at import time.
    from pyatlan.model.assets import __PYATLAN_SUPER_TYPES__

    return __PYATLAN_SUPER_TYPES__


def _name(type_or_name: TypeOrName) -> str:
    if isinstance(type_or_name, str):
        return type_or_name
    return type_or_name.__name__


def get_super_types(type_or_name: TypeOrName) -> Tuple[str, ...]:
    """Direct Atlas supertypes of a type, in typedef order.

    :param type_or_name: asset class (e.g. ``SAPProcess``) or type name (``"SAPProcess"``)
    :returns: the type's direct supertypes; empty for ``Referenceable`` and unknown types
    """
    return tuple(_super_types().get(_name(type_or_name), ()))


@lru_cache(maxsize=None)
def _ancestors(type_name: str) -> FrozenSet[str]:
    super_types = _super_types()
    seen: set = set()
    pending = list(super_types.get(type_name, ()))
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)
        pending.extend(super_types.get(current, ()))
    return frozenset(seen)


def get_all_super_types(type_or_name: TypeOrName) -> FrozenSet[str]:
    """Every Atlas ancestor of a type, following all supertypes at every level.

    :param type_or_name: asset class or type name
    :returns: all ancestors (not including the type itself); empty for unknown types
    """
    return _ancestors(_name(type_or_name))


def is_subtype_of(type_or_name: TypeOrName, super_type: TypeOrName) -> bool:
    """Whether a type is, or inherits from, ``super_type`` in Atlas.

    Unlike ``issubclass``, this follows every Atlas supertype, not only the one the
    generated Python class extends.

    :param type_or_name: asset class or type name to check
    :param super_type: asset class or type name of the expected ancestor
    :returns: ``True`` if the types are the same or ``super_type`` is an ancestor
    """
    name, target = _name(type_or_name), _name(super_type)
    return name == target or target in _ancestors(name)
