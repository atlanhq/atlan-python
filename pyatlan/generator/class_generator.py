# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
"""
This script can be used to generate the source code for pyatlan.model.assets, pyatlan.model.structs.py and part of
pyatlan.model.enums. This script depends upon the presence of a JSON file containing typedefs downloaded from
an Atlan instance. The script create_typedefs_file.py can be used to produce this file.
"""
import datetime
import enum
import json
import os
import re
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Set

import networkx as nx
from jinja2 import Environment, PackageLoader

from pyatlan.model.typedef import EntityDef, EnumDef, TypeDefResponse
from pyatlan.model.utils import to_snake_case

REFERENCEABLE = "Referenceable"
TYPE_DEF_FILE = Path(os.getenv("TMPDIR", "/tmp")) / "typedefs.json"
TYPE_REPLACEMENTS = [
    ("array<string>", "Set[string]"),
    ("array<date>", "Set[date]"),
    ("array<boolean>", "Set[bool]"),
    ("array<int>", "Set[int]"),
    ("array<float>", "Set[float]"),
    ("array<long>", "Set[int]"),
    ("icon_type", "IconType"),
    ("string", "str"),
    ("date", "datetime"),
    ("array", "List"),
    ("boolean", "bool"),
    ("float", "float"),
    ("long", "int"),
    ("__internal", "Internal"),
    ("certificate_status", "CertificateStatus"),
    ("map", "Dict"),
    (">", "]"),
    ("<", "["),
    ("query_username_strategy", "QueryUsernameStrategy"),
    ("google_datastudio_asset_type", "GoogleDatastudioAssetType"),
    ("powerbi_endorsement", "PowerbiEndorsement"),
    ("kafka_topic_compression_type", "KafkaTopicCompressionType"),
    ("kafka_topic_cleanup_policy", "KafkaTopicCleanupPolicy"),
    ("quick_sight_folder_type", "QuickSightFolderType"),
    ("quick_sight_dataset_field_type", "QuickSightDatasetFieldType"),
    ("quick_sight_analysis_status", "QuickSightAnalysisStatus"),
    ("quick_sight_dataset_import_mode", "QuickSightDatasetImportMode"),
    ("file_type", "FileType"),
    ("atlas_operation", "AtlasOperation"),
    ("matillion_job_type", "MatillionJobType"),
]
PRIMITIVE_MAPPINGS = {
    "string": "str",
    "boolean": "bool",
    "int": "int",
    "long": "int",
    "date": "int",
    "float": "float",
    "string,string": "str, str",
    "string,long": "str, int",
}
ARRAY_REPLACEMENTS = [("array<string>", "Set{string}")]
ADDITIONAL_IMPORTS = {
    "datetime": "from datetime import datetime",
    "CertificateStatus": "from .enums import CertificateStatus",
    "SourceCostUnitType": "from .enums import SourceCostUnitType",
    "PopularityInsights": "from .structs import PopularityInsights",
}
# The resolve() method ensures
# the retrieval of the absolute path for the file,
# helping to prevent inconsistencies
# across Python versions (e.g: 3.8 and 3.9).
PARENT = Path(__file__).resolve().parent
ASSETS_DIR = PARENT.parent / "model" / "assets"
MODEL_DIR = PARENT.parent / "model"
DOCS_DIR = PARENT.parent / "documentation"
SPHINX_DIR = PARENT.parent.parent / "docs"
TEMPLATES_DIR = PARENT / "templates"


def get_type(type_: str):
    ret_value = type_
    for field, replacement in TYPE_REPLACEMENTS:
        ret_value = ret_value.replace(field, replacement)
    return ret_value


def get_type_defs() -> TypeDefResponse:
    if (
        not TYPE_DEF_FILE.exists()
        or datetime.date.fromtimestamp(os.path.getmtime(TYPE_DEF_FILE))
        < datetime.date.today()
    ):
        raise ClassGenerationError(
            "File containing typedefs does not exist or is not current."
            f" Please run create_typedefs_file to create {TYPE_DEF_FILE}."
        )
    with TYPE_DEF_FILE.open() as input_file:
        return TypeDefResponse(**json.load(input_file))


class ClassGenerationError(Exception):
    pass


class ModuleStatus(str, Enum):
    ACTIVE = "A"
    MERGED = "M"


class ModuleInfo:
    count: int = 0
    modules: Set["ModuleInfo"] = set()
    modules_by_asset_name: Dict[str, str] = {}
    assets: Dict[str, "AssetInfo"] = {}

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
        self.asset_infos: Set["AssetInfo"] = set()
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
    asset_info_by_name: Dict[str, "AssetInfo"] = {}
    hierarchy_graph: nx.DiGraph = nx.DiGraph()
    super_type_names_to_ignore: Set[str] = set()
    entity_defs_by_name: Dict[str, EntityDef] = {}
    sub_type_names_to_ignore: Set[str] = set()

    def __init__(self, name: str, entity_def: EntityDef):
        self._name = name
        self.entity_def: EntityDef = entity_def
        self.update_attribute_defs()
        self.module_info: Optional[ModuleInfo] = None
        self.required_asset_infos: Set["AssetInfo"] = set()
        self.circular_dependencies: Set["AssetInfo"] = set()
        self.order: int = 0
        self.module_name = to_snake_case(name)
        self.super_type: Optional[AssetInfo] = None

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

    @property
    def import_super_class(self):
        if self._name == REFERENCEABLE:
            return ""
        super_type = AssetInfo.asset_info_by_name[self.entity_def.super_types[0]]
        return f"from .{super_type.module_name} import {super_type.name}"

    @property
    def imports_for_referenced_assets(self):
        return [
            f"from .{required_asset.module_name} import {required_asset.name} # noqa"
            for required_asset in self.required_asset_infos
        ]

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
                (
                    ancestor_entity_def.super_types[0]
                    if ancestor_entity_def.super_types
                    else ""
                ),
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

    def update_required_asset_names(self) -> None:
        attributes_to_remove: Set[str] = set()
        attribute_defs = self.entity_def.attribute_defs or []
        relationship_attribute_defs = self.entity_def.relationship_attribute_defs or []
        for attribute in attribute_defs + relationship_attribute_defs:
            type_name = attribute["typeName"].replace("array<", "").replace(">", "")
            if type_name == self._name:
                continue
            if type_name in AssetInfo.super_type_names_to_ignore:
                attributes_to_remove.add(attribute["name"])
            elif type_name in AssetInfo.asset_info_by_name:
                self.required_asset_infos.add(AssetInfo.asset_info_by_name[type_name])
        self.entity_def.attribute_defs = [
            a for a in attribute_defs if a["name"] not in attributes_to_remove
        ]
        self.entity_def.relationship_attribute_defs = [
            a
            for a in relationship_attribute_defs
            if a["name"] not in attributes_to_remove
        ]

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
    def set_entity_defs(cls, entity_defs: List[EntityDef]):
        cls.entity_defs_by_name = {
            entity_def.name: entity_def for entity_def in entity_defs
        }
        entity_defs = sorted(entity_defs, key=lambda e: ",".join(e.super_types or []))
        for entity_def in entity_defs:
            name = entity_def.name
            if name == "Purpose" and entity_def.attribute_defs:
                for attribute in entity_def.attribute_defs:
                    if attribute["name"] == "purposeClassifications":
                        attribute["typeName"] = "array<AtlanTagName>"

            if (not entity_def.super_types and name != REFERENCEABLE) or any(
                super_type in cls.super_type_names_to_ignore
                for super_type in (entity_def.super_types or [])
            ):
                cls.super_type_names_to_ignore.add(name)
                continue
            for asset_name in entity_def.sub_types or []:
                if asset_name not in AssetInfo.sub_type_names_to_ignore:
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

                ModuleInfo.assets[asset_name] = asset_info


class AttributeType(Enum):
    PRIMITIVE = "PRIMITIVE"
    ENUM = "ENUM"
    STRUCT = "STRUCT"
    ASSET = "ASSET"


class MappedType:
    original_base: str
    name: str
    container: str
    attr_type: AttributeType


def get_cached_type(type_name: str) -> Optional[MappedType]:
    for enum_def in type_defs.enum_defs:
        if enum_def.name == type_name:
            mt = MappedType()
            mt.attr_type = AttributeType.ENUM
            mt.name = enum_def.name
            return mt
    for struct_def in type_defs.struct_defs:
        if struct_def.name == type_name:
            mt = MappedType()
            mt.attr_type = AttributeType.STRUCT
            mt.name = struct_def.name
            return mt
    for entity_def in type_defs.entity_defs:
        if entity_def.name == type_name:
            mt = MappedType()
            mt.attr_type = AttributeType.ASSET
            mt.name = entity_def.name
            return mt
    return None


def get_embedded_type(attr_type: str) -> str:
    return attr_type[attr_type.index("<") + 1 : attr_type.index(">")]  # noqa: E203


def get_mapped_type(type_name: str) -> MappedType:
    base_type = type_name
    container = None
    if "<" in type_name:
        if type_name.startswith("array<"):
            if type_name.startswith("array<map<"):
                base_type = get_embedded_type(type_name[len("array<") :])  # noqa: E203
                container = "List[Dict["
            else:
                base_type = get_embedded_type(type_name)
                container = "Set["
        elif type_name.startswith("map<"):
            base_type = get_embedded_type(type_name)
            container = "Dict["
    builder = MappedType()
    builder.original_base = base_type
    if primitive_name := PRIMITIVE_MAPPINGS.get(base_type):
        builder.attr_type = AttributeType.PRIMITIVE
        builder.name = primitive_name
    else:
        if mapped_type := get_cached_type(base_type):
            base_type_of_mapped = mapped_type.attr_type
            builder.attr_type = base_type_of_mapped
            builder.name = mapped_type.name
            if base_type_of_mapped == AttributeType.STRUCT:
                # If the referred object is a struct, change the container to a list rather than a set
                container = "List["
        else:
            # Failing any cached type, fallback to just the name of the object
            builder.attr_type = AttributeType.ASSET
            builder.name = base_type
    if container:
        builder.container = container
    return builder


def get_class_var_for_attr(attr_name: str) -> str:
    replace1 = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", attr_name.replace("_", ""))
    replace2 = re.sub(r"([a-z])([A-Z])", r"\1_\2", replace1)
    return replace2.upper()


class IndexType(Enum):
    KEYWORD = enum.auto()
    TEXT = enum.auto()
    RANK_FEATURE = enum.auto()
    BOOLEAN = enum.auto()
    NUMERIC = enum.auto()
    STEMMED = enum.auto()
    RELATION = enum.auto()


class SearchType:
    name: str
    args: Optional[str]

    def __init__(self, name: str, args: Optional[str] = None):
        self.name = name
        self.args = args


def get_search_type(attr_def: Dict[str, Any]) -> SearchType:
    def get_default_index_for_type(base_type: str) -> IndexType:
        if base_type in {"date", "float", "double", "int", "long"}:
            to_use = IndexType.NUMERIC
        elif base_type == "boolean":
            to_use = IndexType.BOOLEAN
        else:
            to_use = IndexType.KEYWORD
        return to_use

    def get_embedded_type(attr_type: str) -> str:
        return attr_type[attr_type.index("<") + 1 : attr_type.index(">")]  # noqa: E203

    def get_base_type() -> str:
        type_name = str(attr_def.get("typeName"))
        base_type = type_name
        if "<" in type_name:
            if type_name.startswith("array<"):
                if type_name.startswith("array<map<"):
                    base_type = get_embedded_type(
                        type_name[len("array<") :]  # noqa: E203
                    )
                else:
                    base_type = get_embedded_type(type_name)
            elif type_name.startswith("map<"):
                base_type = get_embedded_type(type_name)
        return base_type

    def get_indexes_for_attribute() -> Dict[IndexType, str]:
        searchable: Dict[IndexType, str] = {}
        config = attr_def.get("indexTypeESConfig")
        attr_name = str(attr_def.get("name"))
        if "relationshipTypeName" in attr_def:
            searchable[IndexType.RELATION] = attr_name
        else:
            base_type = get_base_type()
            # Default index
            if config and (analyzer := config.get("analyzer")):
                if analyzer == "atlan_text_analyzer":
                    if attr_name.endswith(".stemmed"):
                        searchable[IndexType.STEMMED] = attr_name
                    else:
                        searchable[IndexType.TEXT] = attr_name
            else:
                def_index = get_default_index_for_type(base_type)
                searchable[def_index] = attr_name
            # Additional indexes
            if fields := attr_def.get("indexTypeESFields"):
                for field_suffix in fields:
                    field_name = f"{attr_name}.{field_suffix}"
                    if index_type := fields.get(field_suffix).get("type"):
                        if index_type == "keyword":
                            searchable[IndexType.KEYWORD] = field_name
                        elif index_type == "text":
                            if field_name.endswith(".stemmed"):
                                searchable[IndexType.STEMMED] = field_name
                            else:
                                searchable[IndexType.TEXT] = field_name
                        elif index_type == "rank_feature":
                            searchable[IndexType.RANK_FEATURE] = field_name
                    else:
                        def_index = get_default_index_for_type(base_type)
                        searchable[def_index] = field_name
        return searchable

    search_map = get_indexes_for_attribute()
    indices = search_map.keys()
    if indices == {IndexType.KEYWORD}:
        return SearchType(
            name="KeywordField", args=f'"{search_map.get(IndexType.KEYWORD)}"'
        )
    elif indices == {IndexType.TEXT}:
        return SearchType(name="TextField", args=f'"{search_map.get(IndexType.TEXT)}"')
    elif indices == {IndexType.NUMERIC}:
        return SearchType(
            name="NumericField", args=f'"{search_map.get(IndexType.NUMERIC)}"'
        )
    elif indices == {IndexType.BOOLEAN}:
        return SearchType(
            name="BooleanField", args=f'"{search_map.get(IndexType.BOOLEAN)}"'
        )
    elif indices == {IndexType.NUMERIC, IndexType.RANK_FEATURE}:
        return SearchType(
            name="NumericRankField",
            args=f'"{search_map.get(IndexType.NUMERIC)}", '
            f'"{search_map.get(IndexType.RANK_FEATURE)}"',
        )
    elif indices == {IndexType.KEYWORD, IndexType.TEXT}:
        return SearchType(
            name="KeywordTextField",
            args=f'"{search_map.get(IndexType.KEYWORD)}", '
            f'"{search_map.get(IndexType.TEXT)}"',
        )
    elif indices == {IndexType.KEYWORD, IndexType.TEXT, IndexType.STEMMED}:
        return SearchType(
            name="KeywordTextStemmedField",
            args=f'"{search_map.get(IndexType.KEYWORD)}", '
            f'"{search_map.get(IndexType.TEXT)}", '
            f'"{search_map.get(IndexType.STEMMED)}"',
        )
    return SearchType(name="RelationField")


class Generator:
    def __init__(self) -> None:
        self.environment = Environment(
            loader=PackageLoader("pyatlan.generator", "templates")
        )
        self.environment.filters["to_snake_case"] = to_snake_case
        self.environment.filters["get_type"] = get_type
        self.environment.filters["get_search_type"] = get_search_type
        self.environment.filters["get_mapped_type"] = get_mapped_type
        self.environment.filters["get_class_var_for_attr"] = get_class_var_for_attr

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
        ancestor_entity_def = AssetInfo.entity_defs_by_name[ancestor_name]
        if not ancestor_entity_def.super_types or not ancestor_name:
            return ancestor_relationship_defs
        for relationship_def in ancestor_entity_def.relationship_attribute_defs or []:
            ancestor_relationship_defs.add(relationship_def["name"])
        return self.get_ancestor_relationship_defs(
            (
                ancestor_entity_def.super_types[0]
                if ancestor_entity_def.super_types
                else ""
            ),
            ancestor_relationship_defs,
        )

    def render_modules(self, modules: List[ModuleInfo]):
        self.render_init(modules)  # type: ignore

    def render_module(self, asset_info: AssetInfo, enum_defs: List["EnumDefInfo"]):
        template = self.environment.get_template("module.jinja2")
        content = template.render(
            {
                "asset_info": asset_info,
                "existz": os.path.exists,
                "enum_defs": enum_defs,
                "templates_path": TEMPLATES_DIR.absolute().as_posix(),
            }
        )
        with (ASSETS_DIR / f"{asset_info.module_name}.py").open("w") as script:
            script.write(content)

    def render_init(self, assets: List[AssetInfo]):
        asset_names = [asset.name for asset in assets]
        asset_imports = [
            f"from .{asset.module_name} import {asset.name}" for asset in assets
        ]

        template = self.environment.get_template("init.jinja2")
        content = template.render(
            {"asset_imports": asset_imports, "asset_names": asset_names}
        )

        init_path = ASSETS_DIR / "__init__.py"
        with init_path.open("w") as script:
            script.write(content)

    def render_structs(self, struct_defs):
        template = self.environment.get_template("structs.jinja2")
        content = template.render({"struct_defs": struct_defs})
        with (MODEL_DIR / "structs.py").open("w") as script:
            script.write(content)

    def render_enums(self, enum_defs: List["EnumDefInfo"]):
        template = self.environment.get_template("enums.jinja2")
        content = template.render({"enum_defs": enum_defs})
        start_of_generated_section_found = False
        existing_enums = MODEL_DIR / "enums.py"
        new_enums = MODEL_DIR / "new_enum"
        with existing_enums.open("r+") as current_file, new_enums.open("w") as new_file:
            while not start_of_generated_section_found:
                line = current_file.readline()
                new_file.write(line)
                if line.startswith("# CODE BELOW IS GENERATED NOT MODIFY  **"):
                    line = current_file.readline()
                    new_file.write(line)
                    start_of_generated_section_found = True
            new_file.write(content)
        new_enums.replace(existing_enums)

    def render_docs_struct_snippets(self, struct_defs):
        template = self.environment.get_template(
            "documentation/struct_attributes.jinja2"
        )
        for struct_def in struct_defs:
            content = template.render({"struct_def": struct_def})
            with (DOCS_DIR / f"{struct_def.name.lower()}-properties.md").open(
                "w"
            ) as doc:
                doc.write(content)

    def render_docs_entity_properties(self, entity_defs):
        template = self.environment.get_template(
            "documentation/entity_attributes.jinja2"
        )
        for entity_def in entity_defs:
            attr_def_alpha = sorted(entity_def.attribute_defs, key=lambda x: x["name"])
            content = template.render(
                {
                    "entity_def_name": entity_def.name,
                    "attribute_defs": attr_def_alpha,
                }
            )
            with (DOCS_DIR / f"{entity_def.name.lower()}-properties.md").open(
                "w"
            ) as doc:
                doc.write(content)

    def render_docs_entity_relationships(self, entity_defs):
        template = self.environment.get_template(
            "documentation/entity_relationships.jinja2"
        )
        for entity_def in entity_defs:
            attr_def_alpha = sorted(
                entity_def.relationship_attribute_defs, key=lambda x: x["name"]
            )
            content = template.render(
                {
                    "entity_def_name": entity_def.name,
                    "attribute_defs": attr_def_alpha,
                }
            )
            with (DOCS_DIR / f"{entity_def.name.lower()}-relationships.md").open(
                "w"
            ) as doc:
                doc.write(content)

    def render_sphinx_docs(self, entity_defs):
        template = self.environment.get_template(
            "documentation/sphinx_asset_index.jinja2"
        )
        to_include = []
        for entity_def in entity_defs:
            if (
                not entity_def.name.startswith("__")
                and not entity_def.name == "AtlasServer"
            ):
                to_include.append(entity_def)
        sorted_defs = sorted(to_include, key=(lambda x: x.name))
        content = template.render(
            {
                "entity_defs": sorted_defs,
            }
        )
        with (SPHINX_DIR / "assets.rst").open("w") as doc:
            doc.write(content)

        template = self.environment.get_template("documentation/sphinx_asset.jinja2")
        for entity_def in sorted_defs:
            content = template.render(
                {
                    "entity_def_name": entity_def.name,
                    "title_underline": "=" * len(entity_def.name),
                }
            )
            with (SPHINX_DIR / "asset" / f"{entity_def.name.lower()}.rst").open(
                "w"
            ) as doc:
                doc.write(content)


class KeyValue(NamedTuple):
    key: str
    value: str


class EnumDefInfo:
    enum_def_info: List["EnumDefInfo"] = []

    def __init__(self, enum_def: EnumDef):
        self.name = get_type(enum_def.name)
        self.element_defs: List[KeyValue] = [
            self.get_key_value(e)
            for e in sorted(enum_def.element_defs, key=lambda e: e.ordinal or 0)
        ]

    def get_key_value(self, element_def: EnumDef.ElementDef):
        value = element_def.value
        key = value
        while match := re.search("[a-z][A-Z]", key):
            pos = match.regs[0][0] + 1
            key = f"{key[:pos]}_{key[pos:]}"
        key = key.upper().replace(".", "_").replace("-", "_")
        return KeyValue(key, value)

    @classmethod
    def create(cls, enum_defs):
        for enum_def in enum_defs:
            # Only pick `atlas_core` enums, not user-created ones.
            if enum_def.service_type == "atlas_core":
                cls.enum_def_info.append(EnumDefInfo(enum_def))
        cls.enum_def_info = sorted(cls.enum_def_info, key=lambda e: e.name)


def filter_attributes_of_custom_entity_type():
    for entity_def in type_defs.reserved_entity_defs:
        if entity_def.attribute_defs:
            filtered_attribute_defs = [
                attribute_def
                for attribute_def in entity_def.attribute_defs
                if not type_defs.is_custom_entity_def_name(attribute_def["typeName"])
            ]
            entity_def.attribute_defs = filtered_attribute_defs
        if entity_def.relationship_attribute_defs:
            filtered_relationship_attribute_defs = [
                relationship_attribute_def
                for relationship_attribute_def in entity_def.relationship_attribute_defs
                if not type_defs.is_custom_entity_def_name(
                    relationship_attribute_def["typeName"]
                )
            ]
            entity_def.relationship_attribute_defs = (
                filtered_relationship_attribute_defs
            )


if __name__ == "__main__":
    type_defs = get_type_defs()
    filter_attributes_of_custom_entity_type()
    AssetInfo.sub_type_names_to_ignore = type_defs.custom_entity_def_names
    AssetInfo.set_entity_defs(type_defs.reserved_entity_defs)
    AssetInfo.update_all_circular_dependencies()
    AssetInfo.create_modules()
    for file in (ASSETS_DIR).glob("*.py"):
        file.unlink()
    generator = Generator()
    EnumDefInfo.create(type_defs.enum_defs)
    for asset_info in ModuleInfo.assets.values():
        generator.render_module(asset_info, EnumDefInfo.enum_def_info)
    generator.render_init(ModuleInfo.assets.values())  # type: ignore
    generator.render_structs(type_defs.struct_defs)
    generator.render_enums(EnumDefInfo.enum_def_info)
    generator.render_docs_struct_snippets(type_defs.struct_defs)
    generator.render_docs_entity_properties(type_defs.reserved_entity_defs)
    generator.render_docs_entity_relationships(type_defs.reserved_entity_defs)
    generator.render_sphinx_docs(type_defs.reserved_entity_defs)
