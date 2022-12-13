from pydantic import BaseModel, Extra, Field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass
from pydantic.generics import GenericModel
from typing import Optional, TypeVar, Generic, Any
from pyatlan.model.enums import EntityStatus, AnnouncementType
from datetime import datetime

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


class AtlanObject(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel_case
        extra = Extra.forbid
        json_encoders = {datetime: lambda v: int(v.timestamp() * 1000)}


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


class MutatedEntities(AtlanObject, GenericModel, Generic[T]):
    CREATE: Optional[list[T]] = Field(
        None,
        description="Assets that were created. The detailed properties of the returned asset will vary based on the "
        "type of asset, but listed in the example are the common set of properties across assets.",
        alias="CREATE",
    )
    UPDATE: Optional[list[T]] = Field(
        None,
        description="Assets that were updated. The detailed properties of the returned asset will vary based on the "
        "type of asset, but listed in the example are the common set of properties across assets.",
        alias="UPDATE",
    )
    DELETE: Optional[list[T]] = Field(
        None,
        description="Assets that were deleted. The detailed properties of the returned asset will vary based on the "
        "type of asset, but listed in the example are the common set of properties across assets.",
        alias="DELETE",
    )


class AssetMutationResponse(AtlanObject, GenericModel, Generic[T]):
    guid_assignments: dict[str, Any] = Field(
        None, description="Map of assigned unique identifiers for the changed assets."
    )
    mutated_entities: Optional[MutatedEntities] = Field(
        None, description="Assets that were changed."
    )
