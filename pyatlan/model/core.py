# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from abc import ABC
from typing import TYPE_CHECKING, List, Literal, Union
from typing_extensions import Annotated

from pydantic import (
    field_serializer,
    field_validator,
    model_serializer,
    ConfigDict,
    BaseModel,
    Field,
    validator,
    RootModel,
    SerializerFunctionWrapHandler,
)
from pydantic.functional_serializers import WrapSerializer

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass

from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pyatlan.model.enums import AnnouncementType, EntityStatus

CAMEL_CASE_OVERRIDES = {
    "IndexTypeEsFields": "IndexTypeESFields",
    "sourceUrl": "sourceURL",
    "sourceEmbedUrl": "sourceEmbedURL",
    "sql_dbt_sources": "sqlDBTSources",
    "purpose_atlan_tags": "purposeClassifications",
    "mapped_atlan_tag_name": "mappedClassificationName",
}


def to_camel_case(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Value must be a string")
    if value == "__root__":
        return value
    value = "".join(word.capitalize() for word in value.split("_"))
    if value in CAMEL_CASE_OVERRIDES:
        value = CAMEL_CASE_OVERRIDES[value]
    if value.startswith("__"):
        value = value[2:]
    return f"{value[0].lower()}{value[1:]}"


def to_snake_case(value):
    if value.startswith("__"):
        value = value[2:]
    if value == "purposeClassifications":
        return "purpose_atlan_tags"
    elif value == "mappedClassificationName":
        return "mapped_atlan_tag_name"
    res = [value[0].lower()]
    for c in (
        value.replace("URL", "Url").replace("DBT", "Dbt").replace("GDPR", "Gdpr")[1:]
    ):
        if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            res.append("_")
            res.append(c.lower())
        else:
            res.append(c)
    return "".join(res).replace(" _", "_").replace(" ", "_")


class AtlanTagName:
    def __init__(self, display_text: str):
        from pyatlan.cache.atlan_tag_cache import AtlanTagCache

        if not AtlanTagCache.get_id_for_name(display_text):
            raise ValueError(f"{display_text} is not a valid Classification")
        self._display_text = display_text

    @classmethod
    def __get_validators__(cls):
        yield cls._convert_to_display_text

    def __str__(self):
        return self._display_text

    def __repr__(self):
        return f"AtlanTagName({self._display_text.__repr__()})"

    def __hash__(self):
        return self._display_text.__hash__()

    def __eq__(self, other):
        return (
            isinstance(other, AtlanTagName)
            and self._display_text == other._display_text
        )

    @classmethod
    def _convert_to_display_text(cls, data):
        from pyatlan.cache.atlan_tag_cache import AtlanTagCache

        if isinstance(data, AtlanTagName):
            return data
        if display_text := AtlanTagCache.get_name_for_id(data):
            return AtlanTagName(display_text)
        else:
            raise ValueError(f"{data} is not a valid AtlanTag")

    @model_serializer
    def ser_model(self) -> str:
        from pyatlan.cache.atlan_tag_cache import AtlanTagCache

        return AtlanTagCache.get_id_for_name(self._display_text) or ""

    if TYPE_CHECKING:
        # Ensure type checkers see the correct return type
        def model_dump(
            self,
            *,
            mode: Union[Literal["json", "python"], str] = "python",
            include: Any = None,
            exclude: Any = None,
            by_alias: bool = False,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            round_trip: bool = False,
            warnings: bool = True,
        ) -> str:
            ...

    @staticmethod
    def json_encode_atlan_tag(atlan_tag_name: "AtlanTagName"):
        from pyatlan.cache.atlan_tag_cache import AtlanTagCache

        return AtlanTagCache.get_id_for_name(atlan_tag_name._display_text)


class AtlanObject(BaseModel):
    # TODO[pydantic]: The following keys were removed: `json_encoders`.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel_case,
        extra="ignore",
        validate_assignment=True,
    )


class SearchRequest(AtlanObject, ABC):
    attributes: Optional[List[str]] = Field(
        description="List of attributes to be returned for each result.",
        default_factory=list,
    )
    offset: Optional[int] = Field(
        description="Starting point for pagination.", alias="from"
    )
    size: Optional[int] = Field(
        description="How many results to include in each page of results."
    )


@dataclass
class Announcement:
    announcement_title: str
    announcement_message: Optional[str]
    announcement_type: AnnouncementType


class AtlanTag(AtlanObject):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    type_name: Optional[AtlanTagName] = Field(
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
    validity_periods: Optional[list[str]] = Field(None, alias="validityPeriods")


AtlanTags = RootModel[list[AtlanObject]]


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


class AssetResponse(AtlanObject, BaseModel, Generic[T]):
    entity: T
    referredEntities: Optional[dict[str, Any]] = Field(
        None,
        description="Map of related entities keyed by the GUID of the related entity. The values will be the detailed "
        "entity object of the related entity.\n",
    )


class AssetRequest(AtlanObject, BaseModel, Generic[T]):
    entity: T

    @field_validator("entity")
    @classmethod
    def flush_custom_metadata(cls, v):
        from pyatlan.model.assets import Asset

        if isinstance(v, Asset):
            v.flush_custom_metadata()
        return v


class BulkRequest(AtlanObject, BaseModel, Generic[T]):
    entities: list[T]

    # TODO[pydantic]: We couldn't refactor the `validator`, please replace it by `field_validator` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-validators for more information.
    @validator("entities", each_item=True)
    def flush_custom_metadata(cls, v):
        from pyatlan.model.assets import Asset

        if isinstance(v, Asset):
            v.flush_custom_metadata()
        return v
