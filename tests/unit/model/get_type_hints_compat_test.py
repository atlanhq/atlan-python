"""Regression tests for SHA-887 follow-up — ``typing.get_type_hints()`` must
work for every core asset's ``Attributes`` inner class.

Five core asset modules gate cross-module relationship-type imports under
``if TYPE_CHECKING:`` to avoid circular imports at module load time. With
``from __future__ import annotations`` (PEP 563), all field annotations are
stored as strings, and ``typing.get_type_hints`` evaluates them against the
defining class's module ``__dict__``. That namespace doesn't see
TYPE_CHECKING-only names, so calls fail with ``NameError`` (e.g.
``name 'DbtTest' is not defined`` for ``Table.Attributes``).

Pydantic v1 already resolves these forward refs internally via
``update_forward_refs(**localns)`` in ``core/__init__.py``, but
``typing.get_type_hints`` is a separate code path used by reflection-based
tools (notably ``atlan-publish-app``'s publish-ordering graph). To make
``get_type_hints`` work without a caller-supplied ``localns``,
``core/__init__.py`` injects each TYPE_CHECKING-only target back into the
defining module's ``__dict__`` after every asset has loaded.

The injection list is generated from
``class_generator._RUNTIME_INJECTION_OVERRIDES``. These tests guard every
entry — if a future regeneration drops the shim, or if pyatlan adds a new
TYPE_CHECKING-only relationship import without updating the override map,
CI fails here rather than silently regressing every downstream consumer.
"""

from typing import get_type_hints

import pytest

from pyatlan.model.assets.core.data_product import DataProduct
from pyatlan.model.assets.core.data_quality_rule import DataQualityRule
from pyatlan.model.assets.core.process import Process
from pyatlan.model.assets.core.s_q_l import SQL
from pyatlan.model.assets.core.schema import Schema


@pytest.mark.parametrize(
    "cls",
    [SQL, Schema, DataProduct, DataQualityRule, Process],
    ids=["SQL", "Schema", "DataProduct", "DataQualityRule", "Process"],
)
def test_get_type_hints_resolves_for_core_attributes(cls):
    """``get_type_hints`` on each affected ``Attributes`` class must succeed
    without a caller-supplied ``localns`` — the runtime injection shim in
    ``core/__init__.py`` makes the TYPE_CHECKING-only names visible."""
    hints = get_type_hints(cls.Attributes)
    assert hints, f"{cls.__name__}.Attributes returned no hints"


def test_sql_attributes_dbt_tests_resolves_to_dbt_test():
    """Concrete spot-check: the field that originally tripped publish-app
    (``SQL.Attributes.dbt_tests``) must resolve to the real ``DbtTest``
    class rather than raising ``NameError`` on the forward ref."""
    import typing

    from pyatlan.model.assets.core.dbt_test import DbtTest

    hints = get_type_hints(SQL.Attributes)
    dbt_tests_hint = hints.get("dbt_tests")
    assert dbt_tests_hint is not None, "dbt_tests field missing from SQL hints"
    # The resolved hint is ``Optional[List[DbtTest]]``. Walk the generic
    # arg tree to confirm the leaf is the actual class, not a string.
    leaves = []
    stack = [dbt_tests_hint]
    while stack:
        node = stack.pop()
        args = typing.get_args(node)
        if args:
            stack.extend(args)
        else:
            leaves.append(node)
    assert DbtTest in leaves, (
        f"DbtTest not present in resolved leaves: {leaves} "
        f"(full hint: {dbt_tests_hint!r})"
    )
