# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
PyTest configuration and fixtures for pyatlan_v9 unit tests.
These fixtures provide test utilities for msgspec-based models.

This module also applies compatibility patches that allow v9 msgspec models
to work seamlessly with the legacy Pydantic-based client layer.  The patches
MUST run at module load time (before any client classes are imported) so that
Pydantic's cached validators pick up the patched behaviour.
"""

# ---------------------------------------------------------------------------
# v9 ↔ legacy compatibility patches  (executed at import time)
# ---------------------------------------------------------------------------

import msgspec
from pydantic.v1.json import ENCODERS_BY_TYPE
from pydantic.v1.main import ModelMetaclass

from pyatlan.model.assets.core.asset import Asset as _LegacyAsset
from pyatlan_v9.model.assets import Asset as _V9Asset

# ---------- Patch 1: Pydantic isinstance ---------------------------------
# Pydantic's ModelMetaclass (which extends ABCMeta) overrides
# ``__instancecheck__`` and short-circuits with a
# ``hasattr(instance, '__post_root_validators__')`` guard that always rejects
# msgspec Structs.  We relax that guard so that a v9 model whose *class name*
# appears in the MRO of the checked type is accepted.
_original_instancecheck = ModelMetaclass.__instancecheck__


def _v9_instancecheck(self, instance):
    """Accept v9 msgspec models where MRO names match."""
    if _original_instancecheck(self, instance):
        return True
    if isinstance(instance, msgspec.Struct):
        v9_mro_names = {cls.__name__ for cls in type(instance).__mro__}
        if self.__name__ in v9_mro_names:
            return True
    return False


ModelMetaclass.__instancecheck__ = _v9_instancecheck

# ---------- Patch 2: Pydantic JSON encoder --------------------------------
# Register ``msgspec.Struct`` so that Pydantic's json-serialisation path
# (used by BulkRequest.json() and AtlanRequest.json()) can serialise v9
# models without raising ``TypeError: not JSON serializable``.
ENCODERS_BY_TYPE[msgspec.Struct] = lambda o: msgspec.to_builtins(o)

# ---------- Patch 3: Asset._convert_to_real_type_ -------------------------
# The legacy @validate_arguments decorator calls
# ``Asset._convert_to_real_type_(data)`` when validating Union[Asset, …]
# parameters.  This patch makes it accept v9 Struct instances as-is.
_original_convert = _LegacyAsset._convert_to_real_type_.__func__


@classmethod  # type: ignore[misc]
def _convert_to_real_type_v9_compat(cls, data):
    """Accept v9 msgspec models in legacy Pydantic validation."""
    if isinstance(data, _V9Asset):
        return data
    return _original_convert(cls, data)


_LegacyAsset._convert_to_real_type_ = _convert_to_real_type_v9_compat  # type: ignore[assignment]

# ---------- Patch 4: BulkRequest.process_attributes -----------------------
# The legacy BulkRequest validator tries to access Pydantic-specific
# attributes (``remove_relationship_attributes``, ``attributes.__fields_set__``,
# ``.dict()``) on every entity.  v9 Struct models don't have those.
# We monkey-patch the validator's *code object* so that any reference captured
# in Pydantic's lambda closures automatically gets the updated behaviour.
from pyatlan.model import core as _core_module  # noqa: E402

_core_module.msgspec = msgspec  # inject into module globals

from pyatlan.model.core import BulkRequest  # noqa: E402

_original_process_func = BulkRequest.process_attributes.__func__


def _new_process_attributes(cls, asset):
    """BulkRequest validator that skips v9 models."""
    if isinstance(asset, msgspec.Struct):
        return asset
    # --- original legacy logic (inlined) ---
    from pyatlan.model.assets import Asset  # noqa: F811

    if not isinstance(asset, Asset):
        return asset

    exclude_attributes = set()
    asset.remove_relationship_attributes = {}
    asset.append_relationship_attributes = {}
    for attribute in asset.attributes.__fields_set__:
        exclude_attributes.update(cls.process_relationship_attributes(asset, attribute))
    exclude_relationship_attributes = {
        key: True
        for key in [
            "remove_relationship_attributes",
            "append_relationship_attributes",
        ]
        if not getattr(asset, key)
    }
    if exclude_attributes:
        exclude_relationship_attributes = {
            **{"attributes": exclude_attributes},
            **exclude_relationship_attributes,
        }
    return asset.__class__(
        **asset.dict(
            by_alias=True,
            exclude_unset=True,
            exclude=exclude_relationship_attributes,
        )
    )


_original_process_func.__code__ = _new_process_attributes.__code__

# ---------------------------------------------------------------------------
# NOW import the client (triggers AssetClient import with @validate_arguments)
# ---------------------------------------------------------------------------
from json import load  # noqa: E402
from pathlib import Path  # noqa: E402
from unittest.mock import patch  # noqa: E402

import pytest  # noqa: E402

from pyatlan.client.atlan import AtlanClient  # noqa: E402
from pyatlan_v9.model.serde import Serde, get_serde  # noqa: E402

# Use the same test data directory as the original tests
TEST_DATA_DIR = Path(__file__).parent.parent.parent / "tests" / "unit" / "data"


@pytest.fixture()
def serde():
    """Provides a Serde instance for msgspec serialization/deserialization."""
    return Serde()


@pytest.fixture()
def shared_serde():
    """Provides the shared singleton Serde instance."""
    return get_serde()


def load_json(responses_dir: Path, filename: str):
    """Load JSON test data from file."""
    with (responses_dir / filename).open() as input_file:
        return load(input_file)


@pytest.fixture()
def mock_role_cache():
    """Mock the role cache on AtlanClient for validation testing."""
    with patch.object(AtlanClient, "role_cache") as cache:
        yield cache


@pytest.fixture()
def mock_user_cache():
    """Mock the user cache on AtlanClient for validation testing."""
    with patch.object(AtlanClient, "user_cache") as cache:
        yield cache


@pytest.fixture()
def mock_group_cache():
    """Mock the group cache on AtlanClient for validation testing."""
    with patch.object(AtlanClient, "group_cache") as cache:
        yield cache


@pytest.fixture()
def mock_custom_metadata_cache():
    """Mock the custom metadata cache on AtlanClient for badge testing."""
    with patch.object(AtlanClient, "custom_metadata_cache") as cache:
        yield cache


@pytest.fixture()
def glossary_json():
    """Load glossary test data."""
    return load_json(TEST_DATA_DIR, "glossary.json")


@pytest.fixture()
def glossary_term_json():
    """Load glossary term test data."""
    return load_json(TEST_DATA_DIR, "glossary_term.json")


@pytest.fixture()
def glossary_category_json():
    """Load glossary category test data."""
    return load_json(TEST_DATA_DIR, "glossary_category.json")
