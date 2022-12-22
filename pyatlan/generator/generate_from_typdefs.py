import datetime
import json
import os
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.typedef import TypeDefClient
from pyatlan.model.core import to_snake_case
from pyatlan.model.typedef import EntityDef, TypeDefResponse

PARENT = Path(__file__).parent
DICT_BY_STRING = dict[str, Any]
LIST_DICT_BY_STRING = list[DICT_BY_STRING]
TEMPLATES_DIR = PARENT.parent / "templates"
TYPE_DEF_FILE = Path(os.getenv("TMPDIR", "/tmp")) / "typedefs.json"
TYPE_REPLACEMENTS = [
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
]


def get_type(type_: str):
    ret_value = type_
    for (field, replacement) in TYPE_REPLACEMENTS:
        ret_value = ret_value.replace(field, replacement)
    return ret_value


def to_dict(entity_defs: list[EntityDef]) -> dict[str, EntityDef]:
    return {entity_def.name: entity_def for entity_def in entity_defs}


def get_type_defs() -> TypeDefResponse:
    if (
        TYPE_DEF_FILE.exists()
        and datetime.date.fromtimestamp(os.path.getmtime(TYPE_DEF_FILE))
        >= datetime.date.today()
    ):
        with TYPE_DEF_FILE.open() as input_file:
            return TypeDefResponse(**json.load(input_file))
    else:
        client = TypeDefClient(AtlanClient())
        type_defs = client.get_all_typedefs()
        with TYPE_DEF_FILE.open("w") as output_file:
            output_file.write(type_defs.json())
        return type_defs


class Generator:
    def __init__(self) -> None:
        self.type_defs = get_type_defs()
        self.entity_defs = to_dict(self.type_defs.entity_defs)
        self.environment = Environment(
            loader=PackageLoader("pyatlan.generator", "templates")
        )
        self.environment.filters["to_snake_case"] = to_snake_case
        self.environment.filters["get_type"] = get_type
        self.template = self.environment.get_template("entity.jinja2")
        self.processed: set[str] = set()

    def render(self, name: str) -> None:
        entity_defs: list[EntityDef] = []
        i = 0
        self.add_entity_def(entity_defs, name)
        while True:
            self.add_children(i, entity_defs)
            i = i + 1
            if i >= len(entity_defs):
                break
        content = self.template.render(
            {"struct_defs": self.type_defs.struct_defs, "entity_defs": entity_defs}
        )
        with (PARENT.parent / "model" / "assets.py").open("w") as script:
            script.write(content)

    def add_children(self, i, entity_defs):
        entity_def = entity_defs[i]
        for name in entity_def.sub_types:
            if name in self.processed:
                continue
            self.add_entity_def(entity_defs, name)

    def add_entity_def(self, entity_defs, name):
        entity_def = self.entity_defs[name]
        names = set()
        for attribute_def in entity_def.attribute_defs:
            names.add(attribute_def["name"])
        entity_def.relationship_attribute_defs = [
            relationship_def
            for relationship_def in entity_def.relationship_attribute_defs
            if relationship_def["name"] not in names
        ]
        for parent in entity_def.super_types:
            if parent not in self.processed:
                return
        entity_defs.append(entity_def)
        self.processed.add(name)


def main():
    generator = Generator()
    generator.render("Referenceable")


if __name__ == "__main__":
    main()
