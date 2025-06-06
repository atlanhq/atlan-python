# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

import json
from abc import ABC
from typing import TYPE_CHECKING

import yaml  # type: ignore[import-untyped]
from pydantic.v1 import BaseModel, Extra, Field, root_validator, validator

from pyatlan.model.utils import encoders, to_camel_case

if TYPE_CHECKING:
    from dataclasses import dataclass

    from pyatlan.client.atlan import AtlanClient
else:
    from pydantic.v1.dataclasses import dataclass

from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic.v1.generics import GenericModel

from pyatlan.errors import ErrorCode
from pyatlan.model.constants import DELETED_, DELETED_SENTINEL
from pyatlan.model.enums import AnnouncementType, EntityStatus, SaveSemantic
from pyatlan.model.retranslators import AtlanTagRetranslator
from pyatlan.model.structs import SourceTagAttachment
from pyatlan.model.translators import AtlanTagTranslator


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
        self._display_text = display_text

    @classmethod
    def get_deleted_sentinel(cls) -> "AtlanTagName":
        """Will return an AtlanTagName that is a sentinel object to represent deleted tags."""
        return cls._sentinel or cls.__new__(
            cls, DELETED_SENTINEL
        )  # Because __new__ is being invoked directly __init__ won't be

    @classmethod
    def __get_validators__(cls):
        yield cls._convert_to_tag_name

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
    def _convert_to_tag_name(cls, data):
        if isinstance(data, AtlanTagName):
            return data
        return AtlanTagName(data) if data else cls.get_deleted_sentinel()


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


class AtlanYamlModel(BaseModel):
    """
    A model class for working with YAML data.
    """

    class Config:
        # Allow extra fields for contracts
        # if they are not defined in the model
        extra = Extra.allow
        validate_assignment = True
        allow_population_by_field_name = True

    def to_yaml(
        self, by_alias: bool = True, exclude_unset: bool = True, sort_keys: bool = False
    ) -> str:
        """
        Serialize the Pydantic model instance to a YAML string.
        """

        return yaml.dump(
            json.loads(self.json(by_alias=by_alias, exclude_unset=exclude_unset)),
            sort_keys=sort_keys,
        )

    @classmethod
    def from_yaml(cls, yaml_str: str):
        """
        Create an instance of the class from a YAML string.

        :param yaml_str: YAML string to parse.

        :returns: an instance of the class
        with attributes populated from the YAML data.
        """
        data = yaml.safe_load(yaml_str)
        return cls(**data)


class AtlanResponse:
    """
    A wrapper class to handle and translate raw JSON responses
    from the Atlan API into human-readable formats using registered translators.
    """

    def __init__(self, raw_json: Dict[str, Any], client: AtlanClient):
        """
        Initialize the AtlanResponse with raw JSON and client.
        Automatically applies translations to the raw JSON.
        """
        self.raw_json = raw_json
        self.client = client
        self.translators = [
            AtlanTagTranslator(client),
            # Register more translators here
        ]
        self.translated = self._deep_translate(self.raw_json)

    def _deep_translate(
        self, data: Union[Dict[str, Any], List[Any], Any]
    ) -> Union[Dict[str, Any], List[Any], Any]:
        """
        Recursively translate fields in a JSON structure using registered translators.
        """
        if isinstance(data, dict):
            # Apply translators to this dict if any apply
            for translator in self.translators:
                if translator.applies_to(data):
                    data = translator.translate(data)

            # Recursively apply to each value
            return {key: self._deep_translate(value) for key, value in data.items()}

        elif isinstance(data, list):
            return [self._deep_translate(item) for item in data]

        else:
            return data

    def to_dict(self) -> Union[Dict[str, Any], List[Any], Any]:
        """
        Returns the translated version of the raw JSON response.
        """
        return self.translated


class AtlanRequest:
    """
    A wrapper class to handle and retranslate an AtlanObject instance
    into a backend-compatible JSON format by applying retranslators.
    """

    def __init__(self, instance: AtlanObject, client: AtlanClient):
        """
        Initialize an AtlanRequest for a given asset/model instance.

        Serializes the instance to JSON, applies retranslation logic, and prepares
        a structure compatible with Atlan's API (e.g: converts tag names back to hashed IDs).
        """
        self.client = client
        self.instance = instance
        self.retranslators = [
            AtlanTagRetranslator(client),
            # add others...
        ]
        # Do: instance.json() → parse → translate → store
        try:
            raw_json = self.instance.json(
                by_alias=True, exclude_unset=True, client=self.client
            )
        except TypeError:
            raw_json = self.instance.json(
                by_alias=True,
                exclude_unset=True,
            )
        parsed = json.loads(raw_json)
        self.translated = self._deep_retranslate(parsed)

    def _deep_retranslate(self, data: Any) -> Any:
        """
        Recursively traverse and apply retranslators to JSON-like data.
        """
        if isinstance(data, dict):
            for retranslator in self.retranslators:
                if retranslator.applies_to(data):
                    data = retranslator.retranslate(data)
            return {key: self._deep_retranslate(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._deep_retranslate(item) for item in data]
        return data

    def json(self, **kwargs) -> str:
        """
        Returns the fully retranslated JSON string, suitable for API calls.
        """
        return json.dumps(self.translated, **kwargs)


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
    propagate: Optional[bool] = Field(
        default=False,
        description="whether to propagate the Atlan tag (True) or not (False)",
    )
    remove_propagations_on_entity_delete: Optional[bool] = Field(
        default=True,
        description=(
            "whether to remove the propagated Atlan tags when the Atlan tag "
            "is removed from this asset (True) or not (False)"
        ),
        alias="removePropagationsOnEntityDelete",
    )
    restrict_propagation_through_lineage: Optional[bool] = Field(
        default=False,
        description="whether to avoid propagating through lineage (True) or do propagate through lineage (False)",
        alias="restrictPropagationThroughLineage",
    )
    restrict_propagation_through_hierarchy: Optional[bool] = Field(
        default=False,
        description=(
            "Whether to prevent this Atlan tag from propagating through "
            "hierarchy (True) or allow it to propagate through hierarchy (False)"
        ),
        alias="restrictPropagationThroughHierarchy",
    )
    validity_periods: Optional[List[str]] = Field(default=None, alias="validityPeriods")
    source_tag_attachments: List[SourceTagAttachment] = Field(
        default_factory=list, exclude=True
    )

    attributes: Optional[Dict[str, Any]] = None
    tag_id: Optional[str] = Field(default=None, exclude=True)

    @classmethod
    def of(
        cls,
        atlan_tag_name: AtlanTagName,
        entity_guid: Optional[str] = None,
        source_tag_attachment: Optional[SourceTagAttachment] = None,
        client: Optional[AtlanClient] = None,
    ) -> AtlanTag:
        """
        Construct an Atlan tag assignment for a specific entity.

        :param atlan_tag_name: human-readable name of the Atlan tag
        :param entity_guid: unique identifier (GUID) of the entity to which the Atlan tag is to be assigned
        :param source_tag_attachment: (optional) source-specific details for the tag
        :param client: (optional) client instance used for translating source-specific details
        :return: an Atlan tag assignment with default settings for propagation and a specific entity assignment
        :raises InvalidRequestError: if client is not provided and source_tag_attachment is specified
        """
        tag = AtlanTag(type_name=atlan_tag_name)  # type: ignore[call-arg]
        if entity_guid:
            tag.entity_guid = entity_guid
            tag.entity_status = EntityStatus.ACTIVE
        if source_tag_attachment:
            if not client:
                raise ErrorCode.NO_ATLAN_CLIENT.exception_with_parameters()
            tag_id = client.atlan_tag_cache.get_id_for_name(str(atlan_tag_name))
            source_tag_attr_id = client.atlan_tag_cache.get_source_tags_attr_id(
                tag_id or ""
            )
            tag.attributes = {source_tag_attr_id: [source_tag_attachment]}  # type: ignore[dict-item]
            tag.source_tag_attachments.append(source_tag_attachment)
        return tag


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


class BulkRequest(AtlanObject, GenericModel, Generic[T]):
    entities: List[T]

    @validator("entities", each_item=True)
    def process_attributes(cls, asset):
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

        # Updated to use `asset.attribute` instead of `asset` to align with the API.
        # This change ensures the correct value is retrieved regardless of the naming conventions.
        attribute_name, attribute_value = (
            attribute,
            getattr(asset.attributes, attribute, None),
        )

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
                # Updated to use `asset.attribute` instead of `asset` to align with the API.
                # This change ensures the correct value is retrieved regardless of the naming conventions.
                setattr(asset.attributes, attribute_name, replace_attributes)

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
