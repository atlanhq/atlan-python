import ast
import importlib
from types import SimpleNamespace

import pytest
from jinja2 import Environment, PackageLoader

from pyatlan.generator.class_generator import to_snake_case
from pyatlan.model.assets import (
    __PYATLAN_ASSETS__,
    __PYATLAN_SUPER_TYPES__,
    ColumnProcess,
    DbtProcess,
    Process,
    SAPColumnProcess,
    SAPProcess,
    Table,
)
from pyatlan.model.type_hierarchy import (
    get_all_super_types,
    get_super_types,
    is_subtype_of,
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


def _asset_classes():
    for module, names in __PYATLAN_ASSETS__.items():
        for name in names:
            if name == "IndistinctAsset":
                continue
            path = (
                f"pyatlan.model.assets.core.{to_snake_case(name)}"
                if module == "core"
                else f"pyatlan.model.assets.{module}"
            )
            yield name, getattr(importlib.import_module(path), name)


def test_every_generated_asset_has_super_types():
    names = {name for name, _ in _asset_classes()}
    assert names - set(__PYATLAN_SUPER_TYPES__) == set()


def test_python_parent_is_one_of_the_atlas_super_types():
    mismatched = [
        (name, cls.__bases__[0].__name__, __PYATLAN_SUPER_TYPES__[name])
        for name, cls in _asset_classes()
        if name != "Referenceable"
        and cls.__bases__[0].__name__ not in __PYATLAN_SUPER_TYPES__[name]
    ]
    assert mismatched == []


def test_referenceable_has_no_super_types():
    assert get_super_types("Referenceable") == ()


@pytest.mark.parametrize("type_name, lineage_type", LINEAGE_TYPES_WITH_A_SECOND_PARENT)
def test_lineage_parent_is_kept(type_name, lineage_type):
    assert lineage_type in get_all_super_types(type_name)
    assert is_subtype_of(type_name, lineage_type)


def test_sap_process_is_both_sap_and_process():
    assert get_super_types(SAPProcess) == ("SAP", "Process")
    assert not issubclass(SAPProcess, Process)
    assert is_subtype_of(SAPProcess, Process)
    assert is_subtype_of(SAPProcess, "SAP")
    assert is_subtype_of(SAPProcess, "Catalog")
    assert is_subtype_of(SAPProcess, "Asset")


def test_transitive_through_any_parent():
    assert is_subtype_of(SAPColumnProcess, ColumnProcess)
    assert is_subtype_of(SAPColumnProcess, Process)
    assert is_subtype_of(DbtProcess, "Dbt")


def test_unrelated_and_unknown_types():
    assert not is_subtype_of(Table, Process)
    assert is_subtype_of(Process, Process)
    assert get_super_types("NotAType") == ()
    assert get_all_super_types("NotAType") == frozenset()
    assert not is_subtype_of("NotAType", "Asset")


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
