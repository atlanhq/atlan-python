from typing import TYPE_CHECKING

from pydantic import BaseModel, Extra, Field, validator

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass

from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pydantic.generics import GenericModel

from pyatlan.model.enums import AnnouncementType, EntityStatus

CAMEL_CASE_OVERRIDES = {
    "IndexTypeEsFields": "IndexTypeESFields",
    "sourceUrl": "sourceURL",
    "sourceEmbedUrl": "sourceEmbedURL",
}


def to_camel_case(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Value must be a string")
    value = "".join(word.capitalize() for word in value.split("_"))
    if value in CAMEL_CASE_OVERRIDES:
        value = CAMEL_CASE_OVERRIDES[value]
    if value.startswith("__"):
        value = value[2:]
    return f"{value[0].lower()}{value[1:]}"


def to_snake_case(str):
    if str.startswith("__"):
        str = str[2:]
    res = [str[0].lower()]
    for c in str.replace("URL", "Url")[1:]:
        if c in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            res.append("_")
            res.append(c.lower())
        else:
            res.append(c)
    return "".join(res)


def encode_classification(v: "Classification"):
    from pyatlan.cache.classification_cache import ClassificationCache

    if v.type_name:
        ret_value = v.dict()
        ret_value["type_name"] = ClassificationCache.get_id_for_name(v.type_name)
        return ret_value
    return v.dict()


class AtlanObject(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel_case
        extra = Extra.forbid
        json_encoders = {
            datetime: lambda v: int(v.timestamp() * 1000),
            "Classification": encode_classification,
        }
        validate_assignment = True


@dataclass
class Announcement:
    announcement_title: str
    announcement_message: Optional[str]
    announcement_type: AnnouncementType


class Classification(AtlanObject):
    type_name: Optional[str] = Field(
        None,
        description="Name of the type definition that defines this instance.\n",
        alias="typeName",
    )
    entity_guid: Optional[str] = Field(
        None,
        description="Unique identifier of the entity instance.\n",
        example="917ffec9-fa84-4c59-8e6c-c7b114d04be3",
        alias="entityGuid",
    )
    entity_status: Optional[EntityStatus] = Field(
        None,
        description="Status of the entity",
        example=EntityStatus.ACTIVE,
        alias="entityStatus",
    )
    propagate: Optional[bool] = Field(None, description="")
    remove_propagations_on_entity_delete: Optional[bool] = Field(
        None, description="", alias="removePropagationsOnEntityDelete"
    )
    restrict_propagation_through_lineage: Optional[bool] = Field(
        None, description="", alias="restrictPropagationThroughLineage"
    )
    validity_peridos: Optional[list[str]] = Field(None, alias="validityPeriods")

    @classmethod
    def __get_validators__(cls):
        yield cls._map_type_name

    @classmethod
    def _map_type_name(cls, data):
        from pyatlan.cache.classification_cache import ClassificationCache

        if "typeName" in data and data["typeName"]:
            type_name = data["typeName"]
            data["typeName"] = ClassificationCache.get_name_for_id(type_name)
        return cls(**data)

    @validator("type_name")
    def valid_classification_name(cls, v):
        from pyatlan.cache.classification_cache import ClassificationCache

        id = ClassificationCache.get_id_for_name(v)
        if id:
            return v
        raise ValueError(f"{v} is not a valid classification")


class Meaning(AtlanObject):
    term_guid: str = Field(
        description="Unique identifier (GUID) of the related term.",
        example="917ffec9-fa84-4c59-8e6c-c7b114d04be3",
        alias="termGuid",
    )
    relation_guid: str = Field(
        description="Unique identifier (GUID) of the relationship itself.",
        example="917ffec9-fa84-4c59-8e6c-c7b114d04be3",
        alias="relationGuid",
    )
    display_text: str = Field(
        description="Human-readable display name of the related term.",
        example="Company",
        alias="displayText",
    )
    confidence: int = Field(description="Unused", example=1)


T = TypeVar("T")


class AssetResponse(AtlanObject, GenericModel, Generic[T]):
    entity: T
    referredEntities: Optional[dict[str, Any]] = Field(
        None,
        description="Map of related entities keyed by the GUID of the related entity. The values will be the detailed "
        "entity object of the related entity.\n",
    )


class AssetRequest(AtlanObject, GenericModel, Generic[T]):
    entity: T


class BulkRequest(AtlanObject, GenericModel, Generic[T]):
    entities: list[T]
