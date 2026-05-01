"""Regression tests for SHA-887 follow-up — DbtColumnProcess must extend
ColumnProcess, not Dbt.

The Atlas typedef for DbtColumnProcess declares
``superTypes=["Dbt", "ColumnProcess"]``. Without an override the class
generator picks ``Dbt`` (``super_types[0]``) and publish-app's
``issubclass(cls, ColumnProcess)`` check — used to identify column-level
lineage types — returns False. DbtColumnProcess then lands in the wrong
publish batch and ATLAS-404s on the columns it references.

The override lives in ``pyatlan/generator/class_generator.py``
(``_SUPERCLASS_OVERRIDES``). These tests guard the generated output so a
future regeneration that drops the override fails CI rather than silently
regressing publish ordering.
"""

import pytest

from pyatlan.model.assets import ColumnProcess, Dbt, DbtColumnProcess


def test_dbt_column_process_extends_column_process():
    """DbtColumnProcess must inherit from ColumnProcess so publish-app
    treats it as a column-level lineage type."""
    assert issubclass(DbtColumnProcess, ColumnProcess)


def test_dbt_column_process_does_not_extend_dbt():
    """Negative guard: extending Dbt re-introduces the wrong-batch ordering bug."""
    assert not issubclass(DbtColumnProcess, Dbt)


def test_dbt_column_process_direct_parent_is_column_process():
    """The Python parent (not just an ancestor) must be ColumnProcess."""
    assert DbtColumnProcess.__bases__[0] is ColumnProcess


def test_dbt_column_process_type_name():
    """Ensure the wire ``type_name`` is preserved despite the parent change."""
    sut = DbtColumnProcess()
    assert sut.type_name == "DbtColumnProcess"


def test_dbt_column_process_type_name_is_immutable():
    sut = DbtColumnProcess()
    with pytest.raises(TypeError):
        sut.type_name = "NotDbtColumnProcess"


def test_dbt_attributes_round_trip():
    """Dbt-specific fields are still declared inline on
    DbtColumnProcess.Attributes."""
    sut = DbtColumnProcess()
    sut.attributes = DbtColumnProcess.Attributes(dbt_alias="x", dbt_unique_id="y")
    assert sut.attributes.dbt_alias == "x"
    assert sut.attributes.dbt_unique_id == "y"


def test_column_process_attributes_round_trip():
    """ColumnProcess-specific fields inherited via ColumnProcess.Attributes
    are accessible."""
    sut = DbtColumnProcess()
    sut.attributes = DbtColumnProcess.Attributes(code="cast(foo as int)")
    assert sut.attributes.code == "cast(foo as int)"
