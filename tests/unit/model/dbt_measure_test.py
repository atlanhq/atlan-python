"""Regression tests for SHA-887 — DbtMeasure must extend SemanticMeasure, not Dbt.

The Atlas typedef for DbtMeasure declares ``superTypes=["Dbt", "SemanticMeasure"]``.
Without an override, the class generator would pick ``Dbt`` (super_types[0]) and
publish-app would order ``DbtMeasure`` after ``DbtSemanticModel`` instead of
recognising the parent → child relationship via the SemanticMeasure edge.

The override lives in ``pyatlan/generator/class_generator.py`` (_SUPERCLASS_OVERRIDES)
and is consumed by both ``AssetInfo.super_class`` / ``.import_super_class`` and the
Jinja module template. These tests guard the *generated* output so a future
regeneration that drops the override fails CI rather than silently regressing
publish ordering.
"""

import pytest

from pyatlan.model.assets import Dbt, DbtMeasure, SemanticMeasure


def test_dbt_measure_extends_semantic_measure():
    """DbtMeasure must inherit from SemanticMeasure for publish-ordering."""
    assert issubclass(DbtMeasure, SemanticMeasure)


def test_dbt_measure_does_not_extend_dbt():
    """Negative guard: extending Dbt re-introduces the SHA-887 ordering bug."""
    assert not issubclass(DbtMeasure, Dbt)


def test_dbt_measure_direct_parent_is_semantic_measure():
    """The Python parent (not just an ancestor) must be SemanticMeasure."""
    assert DbtMeasure.__bases__[0] is SemanticMeasure


def test_dbt_measure_type_name():
    """Ensure the wire ``type_name`` is preserved despite the parent change."""
    sut = DbtMeasure()
    assert sut.type_name == "DbtMeasure"


def test_dbt_measure_type_name_is_immutable():
    sut = DbtMeasure()
    with pytest.raises(TypeError):
        sut.type_name = "NotDbtMeasure"


def test_dbt_attributes_round_trip():
    """Dbt-specific fields are still declared inline on DbtMeasure.Attributes."""
    sut = DbtMeasure()
    sut.attributes = DbtMeasure.Attributes(dbt_alias="x", dbt_unique_id="y")
    assert sut.attributes.dbt_alias == "x"
    assert sut.attributes.dbt_unique_id == "y"


def test_semantic_attributes_round_trip():
    """Semantic-specific fields inherited via SemanticMeasure are accessible."""
    sut = DbtMeasure()
    sut.attributes = DbtMeasure.Attributes(semantic_expression="sum(x)")
    assert sut.attributes.semantic_expression == "sum(x)"
