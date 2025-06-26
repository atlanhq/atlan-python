from __future__ import annotations

import importlib
from typing import Optional

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject
from pyatlan.model.utils import to_python_class_name


class RelationshipAttributes(AtlanObject):
    type_name: Optional[str] = Field(
        default=None,
        description="Name of the relationship type that defines the relationship.",
    )

    @classmethod
    def __get_validators__(cls):
        yield cls._parse_relationship_attributes

    @classmethod
    def _parse_relationship_attributes(cls, data):
        if isinstance(data, RelationshipAttributes):
            return data

        if isinstance(data, list):  # Recursively process lists
            return [cls._parse_relationship_attributes(item) for item in data]

        type_name = (
            data.get("type_name") if "type_name" in data else data.get("typeName")
        )
        relationship_attribute_cls = getattr(
            importlib.import_module("pyatlan.model.assets.relations"),
            to_python_class_name(type_name),
            RelationshipAttributes,
        )
        return relationship_attribute_cls(**data)
