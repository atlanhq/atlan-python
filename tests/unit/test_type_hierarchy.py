import ast
import importlib
from types import SimpleNamespace

import pytest
from jinja2 import Environment, PackageLoader

from pyatlan.generator.class_generator import to_snake_case
from pyatlan.model import type_hierarchy
from pyatlan.model.assets import (
    Asset,
    Catalog,
    ColumnProcess,
    Process,
    SAPProcess,
    Table,
)
from pyatlan.model.type_hierarchy import (
    get_all_super_types,
    get_super_types,
    is_subtype_of,
)

ASSETS = importlib.import_module("pyatlan.model.assets")
GENERATED_SUPER_TYPES = getattr(ASSETS, "__PYATLAN_SUPER_TYPES__", {})
requires_generated_models = pytest.mark.skipif(
    not GENERATED_SUPER_TYPES,
    reason="models not regenerated yet: run ./generator to emit __PYATLAN_SUPER_TYPES__",
)

# Atlas lineage types whose first-listed supertype is not the lineage one, so the generated
# Python class does not extend it.
LINEAGE_TYPES_WITH_A_SECOND_PARENT = [
    ("SAPProcess", "Process"),
    ("SAPColumnProcess", "ColumnProcess"),
    ("SapDatasphereReplicationFlow", "FlowControlOperation"),
    ("FlowDatasetOperation", "Process"),
    ("FlowFieldOperation", "ColumnProcess"),
    ("DbtProcess", "Process"),
    ("DbtColumnProcess", "ColumnProcess"),
]

# A slice of the real Atlas hierarchy, used to test the helpers independently of whether
# the generated models carry the supertype list yet.
ATLAS_SLICE = {
    "Referenceable": [],
    "Asset": ["Referenceable"],
    "Catalog": ["Asset"],
    "SAP": ["Catalog"],
    "Process": ["Asset"],
    "ColumnProcess": ["Process"],
    "SAPProcess": ["SAP", "Process"],
    "SAPColumnProcess": ["SAP", "ColumnProcess"],
    "Table": ["SQL"],
    "SQL": ["Catalog"],
}


@pytest.fixture
def atlas_slice(monkeypatch):
    monkeypatch.setattr(type_hierarchy, "_super_types", lambda: ATLAS_SLICE)
    type_hierarchy._ancestors.cache_clear()
    yield
    type_hierarchy._ancestors.cache_clear()


@pytest.fixture
def no_generated_super_types(monkeypatch):
    monkeypatch.setattr(type_hierarchy, "_super_types", lambda: {})
    type_hierarchy._ancestors.cache_clear()
    yield
    type_hierarchy._ancestors.cache_clear()


def _asset_classes():
    for module, names in getattr(ASSETS, "__PYATLAN_ASSETS__").items():
        for name in names:
            if name == "IndistinctAsset":
                continue
            path = (
                f"pyatlan.model.assets.core.{to_snake_case(name)}"
                if module == "core"
                else f"pyatlan.model.assets.{module}"
            )
            yield name, getattr(importlib.import_module(path), name)


# ---- helpers, against a fixed slice of the Atlas hierarchy ----


def test_follows_every_parent(atlas_slice):
    assert get_super_types(SAPProcess) == ("SAP", "Process")
    assert not issubclass(SAPProcess, Process)
    assert is_subtype_of(SAPProcess, Process)
    assert is_subtype_of("SAPProcess", "SAP")
    assert is_subtype_of(SAPProcess, Catalog)
    assert is_subtype_of(SAPProcess, Asset)


def test_transitive_through_any_parent(atlas_slice):
    assert is_subtype_of("SAPColumnProcess", ColumnProcess)
    assert is_subtype_of("SAPColumnProcess", Process)
    assert get_all_super_types("SAPColumnProcess") == {
        "SAP",
        "Catalog",
        "Asset",
        "Referenceable",
        "ColumnProcess",
        "Process",
    }


def test_unrelated_same_and_unknown_types(atlas_slice):
    assert not is_subtype_of(Table, Process)
    assert is_subtype_of(Process, Process)
    assert get_super_types("Referenceable") == ()
    assert get_super_types("NotAType") == ()
    assert get_all_super_types("NotAType") == frozenset()
    assert not is_subtype_of("NotAType", "Asset")


# ---- fallback before models are regenerated ----


@pytest.mark.parametrize(
    "cls, base",
    [
        (SAPProcess, Process),
        (ColumnProcess, Process),
        (Table, Catalog),
        (Table, Process),
        (Process, Asset),
    ],
)
def test_without_generated_list_matches_issubclass(no_generated_super_types, cls, base):
    assert is_subtype_of(cls, base) == issubclass(cls, base)


# ---- generator template ----


def test_init_template_renders_every_super_type():
    def asset(name, super_types):
        return SimpleNamespace(
            name=name,
            module_name=to_snake_case(name),
            is_core_asset=False,
            _CORE_ASSETS=set(),
            entity_def=SimpleNamespace(super_types=super_types),
        )

    env = Environment(loader=PackageLoader("pyatlan.generator", "templates"))
    rendered = env.get_template("init.jinja2").render(
        {
            "assets": [
                asset("SAPProcess", ["SAP", "Process"]),
                asset("Referenceable", []),
            ]
        }
    )
    assignments = {
        node.targets[0].id: ast.literal_eval(node.value)
        for node in ast.parse(rendered).body
        if isinstance(node, ast.Assign)
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id.startswith("__PYATLAN")
    }
    assert assignments["__PYATLAN_SUPER_TYPES__"] == {
        "Referenceable": [],
        "SAPProcess": ["SAP", "Process"],
    }


def test_mypy_init_template_declares_super_types():
    env = Environment(loader=PackageLoader("pyatlan.generator", "templates"))
    rendered = env.get_template("mypy_init.jinja2").render({"assets": []})
    assert "__PYATLAN_SUPER_TYPES__: Dict[str, List[str]]" in rendered
    assert "__PYATLAN_ASSETS__: Dict[str, List[str]]" in rendered


# ---- generated models (run once ./generator has emitted the list) ----


@requires_generated_models
def test_every_generated_asset_has_super_types():
    names = {name for name, _ in _asset_classes()}
    assert names - set(GENERATED_SUPER_TYPES) == set()


@requires_generated_models
def test_python_parent_is_one_of_the_atlas_super_types():
    mismatched = [
        (name, cls.__bases__[0].__name__, GENERATED_SUPER_TYPES[name])
        for name, cls in _asset_classes()
        if name != "Referenceable"
        and cls.__bases__[0].__name__ not in GENERATED_SUPER_TYPES[name]
    ]
    assert mismatched == []


@requires_generated_models
@pytest.mark.parametrize("type_name, lineage_type", LINEAGE_TYPES_WITH_A_SECOND_PARENT)
def test_lineage_parent_is_kept(type_name, lineage_type):
    assert is_subtype_of(type_name, lineage_type)
