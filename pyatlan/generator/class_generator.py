import datetime
import json
import os
from enum import Enum
from pathlib import Path
from typing import Optional

import networkx as nx
from jinja2 import Environment, PackageLoader

from pyatlan.model.core import to_snake_case
from pyatlan.model.typedef import EntityDef, TypeDefResponse

REFERENCEABLE = "Referenceable"
TYPE_DEF_FILE = Path(os.getenv("TMPDIR", "/tmp")) / "typedefs.json"
TYPE_REPLACEMENTS = [
    ("array<string>", "set[string]"),
    ("array<date>", "set[date]"),
    ("array<boolean>", "set[bool]"),
    ("array<int>", "set[int]"),
    ("array<float>", "set[float]"),
    ("array<long>", "set[int]"),
    ("icon_type", "IconType"),
    ("string", "str"),
    ("date", "datetime"),
    ("array", "list"),
    ("boolean", "bool"),
    ("float", "float"),
    ("long", "int"),
    ("__internal", "Internal"),
    ("certificate_status", "CertificateStatus"),
    ("map", "dict"),
    (">", "]"),
    ("<", "["),
    ("query_username_strategy", "QueryUsernameStrategy"),
    ("google_datastudio_asset_type", "GoogleDatastudioAssetType"),
    ("powerbi_endorsement", "PowerbiEndorsement"),
    ("kafka_topic_compression_type", "KafkaTopicCompressionType"),
    ("kafka_topic_cleanup_policy", "PowerbiEndorsement"),
    ("quick_sight_folder_type", "QuickSightFolderType"),
    ("quick_sight_dataset_field_type", "QuickSightDatasetFieldType"),
    ("quick_sight_analysis_status", "QuickSightAnalysisStatus"),
    ("quick_sight_dataset_import_mode", "QuickSightDatasetImportMode"),
    ("file_type", "FileType"),
]
ARRAY_REPLACEMENTS = [("array<string>", "set{string}")]
ADDITIONAL_IMPORTS = {
    "datetime": "from datetime import datetime",
    "CertificateStatus": "from .enums import CertificateStatus",
    "SourceCostUnitType": "from .enums import SourceCostUnitType",
    "PopularityInsights": "from .structs import PopularityInsights",
}
PARENT = Path(__file__).parent
ASSETS_DIR = PARENT.parent / "model" / "assets"
STRUCTS_DIR = PARENT.parent / "model"


def get_type(type_: str):
    ret_value = type_
    for field, replacement in TYPE_REPLACEMENTS:
        ret_value = ret_value.replace(field, replacement)
    return ret_value


def get_type_defs() -> TypeDefResponse:
    if (
        TYPE_DEF_FILE.exists()
        and datetime.date.fromtimestamp(os.path.getmtime(TYPE_DEF_FILE))
        >= datetime.date.today()
    ):
        with TYPE_DEF_FILE.open() as input_file:
            return TypeDefResponse(**json.load(input_file))
    else:
        raise (Exception("Need Type_Def"))


class ModuleStatus(str, Enum):
    ACTIVE = "A"
    MERGED = "M"


class ModuleInfo:
    count: int = 0
    modules: set["ModuleInfo"] = set()
    modules_by_asset_name: dict[str, str] = {}

    @classmethod
    def update_all_external_dependencies(cls):
        for module in cls.modules:
            module.update_external_dependencies(
                modules_by_asset_name=cls.modules_by_asset_name
            )

    @classmethod
    def check_for_circular_module_dependencies(cls):
        while True:
            circular_dependency_found = False
            for module in sorted(cls.modules, key=lambda m: m.order):
                for external_module in module.external_module_dependencies:
                    if module in external_module.external_module_dependencies:
                        module.merge_with(external_module)
                        circular_dependency_found = True
                        break
                if circular_dependency_found:
                    break
            else:
                return

    def __init__(self, asset_info: "AssetInfo"):
        self.order = ModuleInfo.count
        self._name = f"asset{ModuleInfo.count:02d}"
        self.asset_infos: set["AssetInfo"] = set()
        self.add_asset_info(asset_info=asset_info)
        self.status: ModuleStatus = ModuleStatus.ACTIVE
        ModuleInfo.modules.add(self)
        ModuleInfo.count += 1

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        return isinstance(other, ModuleInfo) and self._name == other._name

    @property
    def name(self):
        return self._name

    @property
    def ordered_asset_infos(self):
        return sorted(list(self.asset_infos), key=lambda a: a.order)

    @property
    def external_asset_dependencies(self):
        return {
            external_asset
            for asset_info in self.asset_infos
            for external_asset in asset_info.required_asset_infos
            if external_asset not in self.asset_infos
        }

    @property
    def external_module_dependencies(self):
        return {
            asset_info.module_info for asset_info in self.external_asset_dependencies
        }

    @property
    def imports(self):
        return sorted(
            [
                f"from. {ModuleInfo.modules_by_asset_name[external_asset.name]} import {external_asset.name}"
                for external_asset in self.external_asset_dependencies
            ]
        )

    def add_asset_info(self, asset_info: "AssetInfo"):
        if asset_info in self.asset_infos:
            return
        assert asset_info.module_info is None
        self.asset_infos.add(asset_info)
        asset_info.module_info = self
        self.modules_by_asset_name[asset_info.name] = self.name
        self.check_for_circular_dependencies(asset_info=asset_info)

    def check_for_circular_dependencies(self, asset_info: "AssetInfo"):
        for circular_dependency in asset_info.circular_dependencies:
            self.add_asset_info(circular_dependency)

    def merge_with(self, other: "ModuleInfo"):
        self.asset_infos.update(other.asset_infos)
        for asset_info in other.asset_infos:
            asset_info.module_info = self
            ModuleInfo.modules_by_asset_name[asset_info.name] = self.name
        other.status = ModuleStatus.MERGED


class AssetInfo:
    asset_info_by_name: dict[str, "AssetInfo"] = {}
    hierarchy_graph: nx.DiGraph = nx.DiGraph()
    super_type_names_to_ignore: set[str] = set()
    entity_defs_by_name: dict[str, EntityDef] = {}

    def __init__(self, name: str, entity_def: EntityDef):
        self._name = name
        self.entity_def: EntityDef = entity_def
        self.update_attribute_defs()
        self.module_info: Optional[ModuleInfo] = None
        self.required_asset_infos: set["AssetInfo"] = set()
        self.circular_dependencies: set["AssetInfo"] = set()
        self.order: int = 0

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        return isinstance(other, ModuleInfo) and self._name == other._name

    @property
    def name(self):
        return self._name

    @property
    def super_class(self):
        if self._name == REFERENCEABLE:
            return "AtlanObject"
        else:
            return self.entity_def.super_types[0]

    def update_attribute_defs(self):
        def get_ancestor_relationship_defs(
            ancestor_name: str, ancestor_relationship_defs
        ):
            ancestor_entity_def = self.entity_defs_by_name[ancestor_name]
            if not ancestor_entity_def.super_types or not ancestor_name:
                return ancestor_relationship_defs
            for relationship_def in (
                ancestor_entity_def.relationship_attribute_defs or []
            ):
                ancestor_relationship_defs.add(relationship_def["name"])
            return get_ancestor_relationship_defs(
                ancestor_entity_def.super_types[0]
                if ancestor_entity_def.super_types
                else "",
                ancestor_relationship_defs,
            )

        entity_def = self.entity_def
        if len(entity_def.super_types) > 1:
            entity_def.attribute_defs = self.merge_attributes(entity_def)
        names = {attribute_def["name"] for attribute_def in entity_def.attribute_defs}
        super_type_relationship_defs = (
            get_ancestor_relationship_defs(entity_def.super_types[0], set())
            if entity_def.super_types
            else set()
        )
        entity_def.relationship_attribute_defs = list(
            {
                relationship_def["name"]: relationship_def
                for relationship_def in entity_def.relationship_attribute_defs
                if relationship_def["name"] not in names
                and relationship_def["name"] not in super_type_relationship_defs
            }.values()
        )

    def update_required_asset_names(self):
        attributes_to_remove: set[str] = set()
        for attribute in (
            self.entity_def.attribute_defs + self.entity_def.relationship_attribute_defs
        ):
            type_name = attribute["typeName"].replace("array<", "").replace(">", "")
            if type_name == self._name:
                continue
            if type_name in AssetInfo.super_type_names_to_ignore:
                attributes_to_remove.add(attribute["name"])
            elif type_name in AssetInfo.asset_info_by_name:
                self.required_asset_infos.add(AssetInfo.asset_info_by_name[type_name])
        self.entity_def.attribute_defs = [
            a
            for a in self.entity_def.attribute_defs
            if a["name"] not in attributes_to_remove
        ]
        self.entity_def.relationship_attribute_defs = [
            a
            for a in self.entity_def.relationship_attribute_defs
            if a["name"] not in attributes_to_remove
        ]
        if self.entity_def.super_types:
            self.required_asset_infos.add(
                AssetInfo.asset_info_by_name[self.entity_def.super_types[0]]
            )

    def merge_attributes(self, entity_def):
        def merge_them(s, a):
            if s != "Asset":
                entity = self.entity_defs_by_name[s]
                for attribute in entity.attribute_defs:
                    if attribute["name"] not in a:
                        a[attribute["name"]] = attribute
                for s_type in entity.super_types:
                    merge_them(s_type, a)

        attributes = {
            attribute["name"]: attribute for attribute in entity_def.attribute_defs
        }

        for super_type in entity_def.super_types:
            merge_them(super_type, attributes)
        return list(attributes.values())

    def update_circular_dependencies(self):
        for required_asset_info in self.required_asset_infos:
            if self in required_asset_info.required_asset_infos:
                self.circular_dependencies.add(required_asset_info)
        if self.entity_def.super_types:
            super_type = self.asset_info_by_name[self.entity_def.super_types[0]]
            if self in super_type.required_asset_infos:
                self.circular_dependencies.add(super_type)

    @classmethod
    def set_entity_defs(cls, entity_defs: list[EntityDef]):
        cls.entity_defs_by_name = {
            entity_def.name: entity_def for entity_def in entity_defs
        }
        entity_defs = sorted(entity_defs, key=lambda e: ",".join(e.super_types))
        for entity_def in entity_defs:
            name = entity_def.name
            if (not entity_def.super_types and name != REFERENCEABLE) or any(
                super_type in cls.super_type_names_to_ignore
                for super_type in entity_def.super_types
            ):
                cls.super_type_names_to_ignore.add(name)
                continue
            for asset_name in entity_def.sub_types:
                AssetInfo.hierarchy_graph.add_edge(name, asset_name)
            asset_info = AssetInfo(name=name, entity_def=entity_def)
            AssetInfo.asset_info_by_name[name] = asset_info
        for asset_info in AssetInfo.asset_info_by_name.values():
            asset_info.update_required_asset_names()

    @classmethod
    def update_all_circular_dependencies(cls):
        for asset_info in cls.asset_info_by_name.values():
            asset_info.update_circular_dependencies()

    @classmethod
    def create_modules(cls):
        order = 0
        for parent_name, successors in nx.bfs_successors(
            cls.hierarchy_graph, REFERENCEABLE
        ):
            for asset_name in [parent_name] + successors:
                asset_info = cls.asset_info_by_name[asset_name]
                asset_info.order = order
                order += 1
                if asset_info.module_info is None:
                    ModuleInfo(asset_info=asset_info)
                else:
                    asset_info.module_info.add_asset_info(asset_info=asset_info)


class Generator:
    def __init__(self) -> None:
        self.environment = Environment(
            loader=PackageLoader("pyatlan.generator", "templates")
        )
        self.environment.filters["to_snake_case"] = to_snake_case
        self.environment.filters["get_type"] = get_type

    def merge_attributes(self, entity_def):
        def merge_them(s, a):
            if s != "Asset":
                entity = self.entity_defs[s]
                for attribute in entity.attribute_defs:
                    if attribute["name"] not in a:
                        a[attribute["name"]] = attribute
                for s_type in entity.super_types:
                    merge_them(s_type, a)

        attributes = {
            attribute["name"]: attribute for attribute in entity_def.attribute_defs
        }

        for super_type in entity_def.super_types:
            merge_them(super_type, attributes)
        return list(attributes.values())

    def get_ancestor_relationship_defs(
        self, ancestor_name: str, ancestor_relationship_defs
    ):
        ancestor_entity_def = self.entity_defs[ancestor_name]
        if not ancestor_entity_def.super_types or not ancestor_name:
            return ancestor_relationship_defs
        for relationship_def in ancestor_entity_def.relationship_attribute_defs or []:
            ancestor_relationship_defs.add(relationship_def["name"])
        return self.get_ancestor_relationship_defs(
            ancestor_entity_def.super_types[0]
            if ancestor_entity_def.super_types
            else "",
            ancestor_relationship_defs,
        )

    def render_modules(self, modules: set[ModuleInfo]):
        for module in modules:
            self.render_module(module)
        self.render_init(modules)

    def render_module(self, module: ModuleInfo):
        template = self.environment.get_template("module.jinja2")
        content = template.render(
            {
                "module": module,
                "existz": os.path.exists,
                "module_name": module.name,
                "modules_by_asset_name": ModuleInfo.modules_by_asset_name,
            }
        )
        with (ASSETS_DIR / f"{module.name}.py").open("w") as script:
            script.write(content)

    def render_init(self, modules: set[ModuleInfo]):
        imports = sorted(
            {
                f"from .{asset_info.module_info.name} import {asset_info.name}"
                for module in modules
                if module.status == ModuleStatus.ACTIVE
                for asset_info in module.asset_infos
            }
        )
        template = self.environment.get_template("init.jinja2")
        content = template.render(
            {
                "imports": imports,
            }
        )
        with (ASSETS_DIR / "__init__.py").open("w") as script:
            script.write(content)

    def render_structs(self, struct_defs):
        template = self.environment.get_template("structs.jinja2")
        content = template.render({"struct_defs": struct_defs})
        with (STRUCTS_DIR / "structs.py").open("w") as script:
            script.write(content)


if __name__ == "__main__":
    for file in (ASSETS_DIR).glob("*.py"):
        file.unlink()
    for file in (STRUCTS_DIR).glob("structs.py"):
        file.unlink()
    type_defs = get_type_defs()
    AssetInfo.set_entity_defs(type_defs.entity_defs)
    AssetInfo.update_all_circular_dependencies()
    AssetInfo.create_modules()
    ModuleInfo.check_for_circular_module_dependencies()
    generator = Generator()
    generator.render_modules(
        [m for m in ModuleInfo.modules if m.status == ModuleStatus.ACTIVE]
    )
    generator.render_structs(type_defs.struct_defs)
