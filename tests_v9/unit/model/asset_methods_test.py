# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Every generated asset keeps its validate/minimize/relate methods."""

import pytest

import pyatlan_v9.model.assets as assets
from pyatlan_v9.model.assets import ADLSAccount, Asset

ASSET_CLASSES = sorted(
    (
        getattr(assets, name)
        for name in dir(assets)
        if isinstance(getattr(assets, name), type)
        and issubclass(getattr(assets, name), Asset)
    ),
    key=lambda cls: cls.__name__,
)


def test_many_asset_classes_are_exported():
    """A broken regeneration that drops most assets fails here."""
    assert len(ASSET_CLASSES) > 400


@pytest.mark.parametrize("asset_cls", ASSET_CLASSES, ids=lambda cls: cls.__name__)
def test_asset_keeps_lifecycle_methods(asset_cls):
    """validate, minimize and relate survive on every asset after generation."""
    for method in ("validate", "minimize", "relate"):
        assert callable(getattr(asset_cls, method, None)), (
            f"{asset_cls.__name__} is missing {method}()"
        )


def test_validate_rejects_missing_required_fields():
    """validate() raises when a required field is unset."""
    with pytest.raises(ValueError, match="qualified_name is required"):
        ADLSAccount(name="acc").validate()


def test_minimize_returns_minimal_copy():
    """minimize() returns a copy with only the updater-required fields."""
    minimal = ADLSAccount(name="acc", qualified_name="default/adls/123/acc").minimize()
    assert isinstance(minimal, ADLSAccount)
    assert minimal.name == "acc"
    assert minimal.qualified_name == "default/adls/123/acc"


def test_relate_returns_related_wrapper():
    """relate() returns the RelatedADLSAccount wrapper for this asset."""
    related = ADLSAccount(name="acc", qualified_name="default/adls/123/acc").relate()
    assert type(related).__name__ == "RelatedADLSAccount"
