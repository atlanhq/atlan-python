"""Regression tests for SHA-887 follow-up — DbtProcess must extend Process, not Dbt.

The Atlas typedef for DbtProcess declares ``superTypes=["Dbt", "Process"]``.
Without an override the class generator picks ``Dbt`` (``super_types[0]``)
and publish-app's ``issubclass(cls, Process)`` check — which decides whether
a type is a "lineage type" that must publish after the entities it references
— returns False. DbtProcess then lands in Batch 1 and ATLAS-404s when
referencing later-batch entities (DbtModel, Column, etc.).

The override lives in ``pyatlan/generator/class_generator.py``
(``_SUPERCLASS_OVERRIDES``). These tests guard the generated output so a
future regeneration that drops the override fails CI rather than silently
regressing publish ordering.
"""

import pytest

from pyatlan.model.assets import Dbt, DbtProcess, Process


def test_dbt_process_extends_process():
    """DbtProcess must inherit from Process so publish-app treats it as a
    lineage type (publish-after-references)."""
    assert issubclass(DbtProcess, Process)


def test_dbt_process_does_not_extend_dbt():
    """Negative guard: extending Dbt re-introduces the Batch-1 ordering bug."""
    assert not issubclass(DbtProcess, Dbt)


def test_dbt_process_direct_parent_is_process():
    """The Python parent (not just an ancestor) must be Process."""
    assert DbtProcess.__bases__[0] is Process


def test_dbt_process_type_name():
    """Ensure the wire ``type_name`` is preserved despite the parent change."""
    sut = DbtProcess()
    assert sut.type_name == "DbtProcess"


def test_dbt_process_type_name_is_immutable():
    sut = DbtProcess()
    with pytest.raises(TypeError):
        sut.type_name = "NotDbtProcess"


def test_dbt_attributes_round_trip():
    """Dbt-specific fields are still declared inline on DbtProcess.Attributes."""
    sut = DbtProcess()
    sut.attributes = DbtProcess.Attributes(dbt_alias="x", dbt_unique_id="y")
    assert sut.attributes.dbt_alias == "x"
    assert sut.attributes.dbt_unique_id == "y"


def test_process_attributes_round_trip():
    """Process-specific fields inherited via Process.Attributes are accessible."""
    sut = DbtProcess()
    sut.attributes = DbtProcess.Attributes(code="select * from foo")
    assert sut.attributes.code == "select * from foo"
