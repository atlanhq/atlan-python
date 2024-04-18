# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from abc import ABC
from typing import TYPE_CHECKING

from pydantic.v1 import BaseModel, Extra, Field, PrivateAttr, root_validator, validator

from pyatlan.model.utils import encoders, to_camel_case

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.v1.dataclasses import dataclass

from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic.v1.generics import GenericModel

from pyatlan.model.constants import DELETED_, DELETED_SENTINEL
from pyatlan.model.enums import AnnouncementType, EntityStatus, SaveSemantic
from pyatlan.model.structs import SourceTagAttachment


class AtlanTagName:
    _sentinel: Optional["AtlanTagName"] = None

    def __new__(cls, *args, **kwargs):
        if args and args[0] == DELETED_SENTINEL and cls._sentinel:
            return cls._sentinel
        obj = super().__new__(cls)
        if args and args[0] == DELETED_SENTINEL:
            obj._display_text = DELETED_
            cls._sentinel = obj
        return obj

    def __init__(self, display_text: str):
        from pyatlan.cache.atlan_tag_cache import AtlanTagCache

        if not (id := AtlanTagCache.get_id_for_name(display_text)):
            raise ValueError(f"{display_text} is not a valid Classification")
        self._display_text = display_text
        self._id = id

    @property
    def id(self):
        return self._id

    @classmethod
    def get_deleted_sentinel(cls) -> "AtlanTagName":
        """Will return an AtlanTagName that is a sentinel object to represent deleted tags."""
        return cls._sentinel or cls.__new__(
            cls, DELETED_SENTINEL
        )  # Because __new__ is being invoked directly __init__ won't be

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

    @staticmethod
    def json_encode_atlan_tag(atlan_tag_name: "AtlanTagName"):
        from pyatlan.cache.atlan_tag_cache import AtlanTagCache

        return AtlanTagCache.get_id_for_name(atlan_tag_name._display_text)


class AtlanObject(BaseModel):
    __atlan_extra__: Dict[str, Any] = Field(
        default_factory=dict,
        description="Contains extra fields from the Atlan API response.",
    )

    class Config:
        extra = Extra.ignore
        json_encoders = encoders()
        validate_assignment = True
        alias_generator = to_camel_case
        allow_population_by_field_name = True

    @classmethod
    def _populate_extra_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Helper method to populate extra fields from the API response.
        """
        extra: Dict[str, Any] = {}
        # Collect all required field names
        all_required_field_names = {field.alias for field in cls.__fields__.values()}
        # Populate extra fields not defined in the model
        for field_name, value in values.items():
            if field_name not in all_required_field_names:
                extra[field_name] = value
        return extra

    @root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Populates extra fields from the API response.
        """
        extra = cls._populate_extra_fields(values)
        cls.__atlan_extra__ = extra
        return values


class SearchRequest(AtlanObject, ABC):
    attributes: Optional[List[str]] = Field(
        default_factory=list,
        description="List of attributes to be returned for each result.",
    )
    offset: Optional[int] = Field(
        default=None, description="Starting point for pagination.", alias="from"
    )
    size: Optional[int] = Field(
        default=None, description="How many results to include in each page of results."
    )


@dataclass
class Announcement:
    announcement_title: str
    announcement_type: AnnouncementType
    announcement_message: Optional[str] = Field(default=None)


class AtlanTag(AtlanObject):
    class Config:
        extra = "forbid"

    type_name: Optional[AtlanTagName] = Field(
        default=None,
        description="Name of the type definition that defines this instance.\n",
        alias="typeName",
    )
    entity_guid: Optional[str] = Field(
        default=None,
        description="Unique identifier of the entity instance.\n",
        example="917ffec9-fa84-4c59-8e6c-c7b114d04be3",
        alias="entityGuid",
    )
    entity_status: Optional[EntityStatus] = Field(
        default=None,
        description="Status of the entity",
        example=EntityStatus.ACTIVE,
        alias="entityStatus",
    )
    propagate: Optional[bool] = Field(default=None, description="")
    remove_propagations_on_entity_delete: Optional[bool] = Field(
        default=None, description="", alias="removePropagationsOnEntityDelete"
    )
    restrict_propagation_through_lineage: Optional[bool] = Field(
        default=None, description="", alias="restrictPropagationThroughLineage"
    )
    restrict_propagation_through_hierarchy: Optional[bool] = Field(
        default=None,
        description=(
            "Whether to prevent this Atlan tag from propagating through "
            "hierarchy (True) or allow it to propagate through hierarchy (False)"
        ),
        alias="restrictPropagationThroughHierarchy",
    )
    validity_periods: Optional[List[str]] = Field(default=None, alias="validityPeriods")
    _source_tag_attachements: List[SourceTagAttachment] = PrivateAttr(
        default_factory=list
    )

    attributes: Optional[Dict[str, Any]] = None

    @property
    def source_tag_attachements(self) -> List[SourceTagAttachment]:
        return self._source_tag_attachements

    @validator("type_name", pre=True)
    def type_name_is_tag_name(cls, value):
        if isinstance(value, AtlanTagName):
            return value
        try:
            value = AtlanTagName._convert_to_display_text(value)
        except ValueError:
            value = AtlanTagName.get_deleted_sentinel()
        return value

    def __init__(self, *args, **kwargs):
        from pyatlan.cache.atlan_tag_cache import AtlanTagCache

        super().__init__(*args, **kwargs)
        if self.type_name != AtlanTagName.get_deleted_sentinel():
            attr_id = AtlanTagCache.get_source_tags_attr_id(self.type_name.id)
        if self.attributes and attr_id in self.attributes:
            self._source_tag_attachements = [
                SourceTagAttachment(**source_tag["attributes"])
                for source_tag in self.attributes[attr_id]
            ]


class AtlanTags(AtlanObject):
    __root__: List[AtlanTag] = Field(
        default_factory=list, description="classifications"
    )


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
    referredEntities: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Map of related entities keyed by the GUID of the related entity. The values will be the detailed "
        "entity object of the related entity.\n",
    )


class AssetRequest(AtlanObject, GenericModel, Generic[T]):
    entity: T

    @validator("entity")
    def flush_custom_metadata(cls, v):
        from pyatlan.model.assets import Asset

        if isinstance(v, Asset):
            v.flush_custom_metadata()
        return v


class BulkRequest(AtlanObject, GenericModel, Generic[T]):
    entities: List[T]

    @validator("entities", each_item=True)
    def process_attributes_and_flush_cm(cls, asset):
        from pyatlan.model.assets import Asset

        if not isinstance(asset, Asset):
            return asset

        # Initialize set for attributes to exclude from serialization
        exclude_attributes = set()
        # Manually need to set these to "{}" so that we can exclude
        # them from the request playload when they're not set by the user
        asset.remove_relationship_attributes = {}
        asset.append_relationship_attributes = {}
        # Process relationship attributes set by the user and update exclusion set
        for attribute in asset.attributes.__fields_set__:
            exclude_attributes.update(
                cls.process_relationship_attributes(asset, attribute)
            )
        # Determine relationship attributes to exclude
        # https://docs.pydantic.dev/1.10/usage/exporting_models/#advanced-include-and-exclude
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
        asset.flush_custom_metadata()
        return asset.__class__(
            **asset.dict(
                by_alias=True,
                exclude_unset=True,
                exclude=exclude_relationship_attributes,
            )
        )

    @classmethod
    def process_relationship_attributes(cls, asset, attribute):
        from pyatlan.model.assets import Asset

        append_attributes = []
        remove_attributes = []
        replace_attributes = []
        exclude_attributes = set()

        attribute_name, attribute_value = attribute, getattr(asset, attribute, None)

        # Process list of relationship attributes
        if attribute_value and isinstance(attribute_value, list):
            for value in attribute_value:
                if value and isinstance(value, Asset):
                    if value.semantic == SaveSemantic.REMOVE:
                        remove_attributes.append(value)
                    elif value.semantic == SaveSemantic.APPEND:
                        append_attributes.append(value)
                    else:
                        replace_attributes.append(value)

            # Update asset based on processed relationship attributes
            if remove_attributes:
                asset.remove_relationship_attributes.update(
                    {to_camel_case(attribute_name): remove_attributes}
                )
            if append_attributes:
                asset.append_relationship_attributes.update(
                    {to_camel_case(attribute_name): append_attributes}
                )
            if replace_attributes:
                setattr(asset, attribute_name, replace_attributes)

            # If 'remove', 'append', or both attributes are present and there are no 'replace' attributes,
            # add the attribute to the set to exclude it from the bulk request payload.
            # This prevents including unwanted 'replace' attributes that could alter the request behavior.
            if (remove_attributes or append_attributes) and not replace_attributes:
                exclude_attributes.add(attribute_name)

        # Process single relationship attribute
        elif attribute_value and isinstance(attribute_value, Asset):
            if attribute_value.semantic == SaveSemantic.REMOVE:
                # Add the replace attribute to the set to exclude it
                # from the "attributes" property in the request payload.
                # We only want to include this attribute under
                # "remove_relationship_attributes", not both.
                exclude_attributes.add(attribute_name)
                asset.remove_relationship_attributes = {
                    to_camel_case(attribute_name): attribute_value
                }
            elif attribute_value.semantic == SaveSemantic.APPEND:
                # Add the replace attribute to the set to exclude it
                # from the "attributes" property in the request payload.
                # We only want to include this attribute under
                # "append_relationship_attributes", not both.
                exclude_attributes.add(attribute_name)
                asset.append_relationship_attributes = {
                    to_camel_case(attribute_name): attribute_value
                }
        return exclude_attributes
