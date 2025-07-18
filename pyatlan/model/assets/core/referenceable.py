# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from json import JSONDecodeError, loads
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional, Union

from pydantic.v1 import Field, PrivateAttr, root_validator

from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject, AtlanTag, Meaning
from pyatlan.model.custom_metadata import CustomMetadataDict, CustomMetadataProxy
from pyatlan.model.enums import EntityStatus, SaveSemantic
from pyatlan.model.fields.atlan_fields import (
    InternalKeywordField,
    InternalKeywordTextField,
    InternalNumericField,
    KeywordField,
    KeywordTextField,
    NumericField,
    TextField,
)
from pyatlan.model.lineage_ref import LineageRef

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient


class Referenceable(AtlanObject):
    """Description"""

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["attributes", "type_name"])

    @root_validator(pre=True)
    def parse_custom_attributes(cls, values):
        if "attributes" in values:
            attributes = values["attributes"]
            if "__customAttributes" in attributes:
                # Pop the __customAttributes from attributes
                custom_attributes = attributes.pop("__customAttributes")
                try:
                    # Try to parse the JSON string if it's a string
                    if isinstance(custom_attributes, str):
                        custom_attributes = loads(custom_attributes)
                    # Add the parsed custom attributes to the Column
                    values["custom_attributes"] = custom_attributes
                except JSONDecodeError:
                    pass
        return values

    def json(self, *args, **kwargs) -> str:
        if not self._metadata_proxy and kwargs.get("client"):
            self._metadata_proxy = CustomMetadataProxy(
                client=kwargs.get("client"),  # type: ignore[arg-type]
                business_attributes=self.business_attributes,
            )
            self.business_attributes = self._metadata_proxy.business_attributes
        return super().json(**kwargs)

    def validate_required(self):
        if not self.create_time or self.created_by:
            self.attributes.validate_required()

    def get_custom_metadata(self, client: AtlanClient, name: str) -> CustomMetadataDict:
        if not self._metadata_proxy:
            self._metadata_proxy = CustomMetadataProxy(
                business_attributes=self.business_attributes, client=client
            )
        return self._metadata_proxy.get_custom_metadata(name=name)

    def set_custom_metadata(
        self, client: AtlanClient, custom_metadata: CustomMetadataDict
    ):
        if not self._metadata_proxy:
            self._metadata_proxy = CustomMetadataProxy(
                business_attributes=self.business_attributes, client=client
            )
        return self._metadata_proxy.set_custom_metadata(custom_metadata=custom_metadata)

    def flush_custom_metadata(self, client: AtlanClient):
        if not self._metadata_proxy:
            self._metadata_proxy = CustomMetadataProxy(
                business_attributes=self.business_attributes, client=client
            )
        self.business_attributes = self._metadata_proxy.business_attributes

    @classmethod
    def __get_validators__(cls):
        yield cls._convert_to_real_type_

    @classmethod
    def _convert_to_real_type_(cls, data):
        return Asset._convert_to_real_type_(data)

    @classmethod
    def can_be_archived(self) -> bool:
        """
        Indicates if an asset can be archived via the asset.delete_by_guid method.
        :returns: True if archiving is supported
        """
        return True

    @property
    def atlan_tag_names(self) -> List[str]:
        return self.classification_names or []

    def __setattr__(self, name, value):
        if name in Referenceable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[List[str]] = [
        "qualified_name",
        "user_def_relationship_to",
        "user_def_relationship_from",
        "assigned_terms",
    ]

    @property
    def qualified_name(self) -> Optional[str]:
        return (
            self.unique_attributes.get("qualifiedName")
            if self.unique_attributes
            else (self.attributes.qualified_name if self.attributes else None)
        )

    @qualified_name.setter
    def qualified_name(self, qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qualified_name = qualified_name

    @property
    def user_def_relationship_to(self) -> Optional[List[Referenceable]]:
        return (
            None
            if self.attributes is None
            else self.attributes.user_def_relationship_to
        )

    @user_def_relationship_to.setter
    def user_def_relationship_to(
        self, user_def_relationship_to: Optional[List[Referenceable]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.user_def_relationship_to = user_def_relationship_to

    @property
    def user_def_relationship_from(self) -> Optional[List[Referenceable]]:
        return (
            None
            if self.attributes is None
            else self.attributes.user_def_relationship_from
        )

    @user_def_relationship_from.setter
    def user_def_relationship_from(
        self, user_def_relationship_from: Optional[List[Referenceable]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.user_def_relationship_from = user_def_relationship_from

    @property
    def assigned_terms(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.meanings

    @assigned_terms.setter
    def assigned_terms(self, assigned_terms: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = assigned_terms

    class Attributes(AtlanObject):
        qualified_name: Optional[str] = Field(default="", description="")
        user_def_relationship_to: Optional[List[Referenceable]] = Field(
            default=None, description=""
        )  # relationship
        user_def_relationship_from: Optional[List[Referenceable]] = Field(
            default=None, description=""
        )  # relationship
        meanings: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        relationship_attributes: Optional[
            Union[RelationshipAttributes, Dict[str, Any]]
        ] = Field(
            default=None,
            description="Map of relationships for the entity. The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema.",
        )

        def validate_required(self):
            pass

    TYPE_NAME: ClassVar[KeywordTextField] = InternalKeywordTextField(
        "typeName", "__typeName.keyword", "__typeName", "__typeName"
    )
    """Type of the asset. For example Table, Column, and so on."""

    GUID: ClassVar[KeywordField] = InternalKeywordField("guid", "__guid", "__guid")
    """Globally unique identifier (GUID) of any object in Atlan."""

    CREATED_BY: ClassVar[KeywordField] = InternalKeywordField(
        "createdBy", "__createdBy", "__createdBy"
    )
    """Atlan user who created this asset."""

    UPDATED_BY: ClassVar[KeywordField] = InternalKeywordField(
        "updatedBy", "__modifiedBy", "__modifiedBy"
    )
    """Atlan user who last updated the asset."""

    STATUS: ClassVar[KeywordField] = InternalKeywordField(
        "status", "__state", "__state"
    )
    """Asset status in Atlan (active vs deleted)."""

    ATLAN_TAGS: ClassVar[KeywordTextField] = InternalKeywordTextField(
        "classificationNames",
        "__traitNames",
        "__classificationsText",
        "__classificationNames",
    )
    """
    All directly-assigned Atlan tags that exist on an asset, searchable by internal hashed-string ID of the Atlan tag.
    """

    PROPAGATED_ATLAN_TAGS: ClassVar[KeywordTextField] = InternalKeywordTextField(
        "classificationNames",
        "__propagatedTraitNames",
        "__classificationsText",
        "__propagatedClassificationNames",
    )
    """All propagated Atlan tags that exist on an asset, searchable by internal hashed-string ID of the Atlan tag."""

    ASSIGNED_TERMS: ClassVar[KeywordTextField] = InternalKeywordTextField(
        "meanings", "__meanings", "__meaningsText", "__meanings"
    )
    """All terms attached to an asset, searchable by the term's qualifiedName."""

    SUPER_TYPE_NAMES: ClassVar[KeywordTextField] = InternalKeywordTextField(
        "typeName", "__superTypeNames.keyword", "__superTypeNames", "__superTypeNames"
    )
    """All super types of an asset."""

    CREATE_TIME: ClassVar[NumericField] = InternalNumericField(
        "createTime", "__timestamp", "__timestamp"
    )
    """Time (in milliseconds) when the asset was created."""

    UPDATE_TIME: ClassVar[NumericField] = InternalNumericField(
        "updateTime", "__modificationTimestamp", "__modificationTimestamp"
    )
    """Time (in milliseconds) when the asset was last updated."""

    QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "qualifiedName", "qualifiedName", "qualifiedName.text"
    )

    """Unique fully-qualified name of the asset in Atlan."""
    CUSTOM_ATTRIBUTES: ClassVar[TextField] = TextField(
        "__customAttributes", "__customAttributes"
    )
    """
    Any source-provided custom information.
    NOTE: This is NOT the same as custom metadata (user-managed),
    but is an entirely different area of source-managed custom information.
    """

    type_name: str = Field(
        default="Referenceable",
        description="Name of the type definition that defines this instance.",
    )
    _metadata_proxy: CustomMetadataProxy = PrivateAttr(default=None)
    attributes: Referenceable.Attributes = Field(
        default_factory=lambda: Referenceable.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary "
        "by type, so are described in the sub-types of this schema.",
    )
    business_attributes: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Map of custom metadata attributes and values defined on the entity.",
    )
    created_by: Optional[str] = Field(
        default=None,
        description="Username of the user who created the object.",
        example="jsmith",
    )
    create_time: Optional[int] = Field(
        default=None,
        description="Time (epoch) at which this object was created, in milliseconds.",
        example=1648852296555,
    )
    delete_handler: Optional[str] = Field(
        default=None,
        description="Details on the handler used for deletion of the asset.",
        example="Hard",
    )
    guid: str = Field(
        default=None,
        description="Unique identifier of the entity instance.",
        example="917ffec9-fa84-4c59-8e6c-c7b114d04be3",
    )
    is_incomplete: Optional[bool] = Field(default=None, description="", example=True)
    labels: Optional[List[str]] = Field(
        default=None, description="Arbitrary textual labels for the asset."
    )
    relationship_attributes: Optional[Union[RelationshipAttributes, Dict[str, Any]]] = (
        Field(
            default=None,
            description="Map of relationships for the entity. The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema.",
        )
    )
    status: Optional[EntityStatus] = Field(
        default=None, description="Status of the entity", example=EntityStatus.ACTIVE
    )
    updated_by: Optional[str] = Field(
        default=None,
        description="Username of the user who last assets_updated the object.",
        example="jsmith",
    )
    update_time: Optional[int] = Field(
        default=None,
        description="Time (epoch) at which this object was last assets_updated, in milliseconds.",
        example=1649172284333,
    )
    version: Optional[int] = Field(
        default=None, description="Version of this object.", example=2
    )
    atlan_tags: Optional[List[AtlanTag]] = Field(
        default=None,
        description="Atlan tags",
    )
    classification_names: Optional[List[str]] = Field(
        default=None,
        description="The names of the classifications that exist on the asset.",
    )
    display_text: Optional[str] = Field(
        default=None,
        description="Human-readable name of the entity..",
    )
    entity_status: Optional[str] = Field(
        default=None,
        description="Status of the entity (if this is a related entity).",
    )
    relationship_guid: Optional[str] = Field(
        default=None,
        description="Unique identifier of the relationship (when this is a related entity).",
    )
    relationship_status: Optional[str] = Field(
        default=None,
        description="Status of the relationship (when this is a related entity).",
    )
    relationship_type: Optional[str] = Field(
        default=None,
        description="Status of the relationship (when this is a related entity).",
    )
    meaning_names: Optional[List[str]] = Field(
        default=None,
        description="Names of assigned_terms that have been linked to this asset.",
    )
    meanings: Optional[List[Meaning]] = Field(default=None, description="")
    custom_attributes: Optional[Dict[str, Any]] = Field(default=None, description="")
    scrubbed: Optional[bool] = Field(default=None, description="")
    pending_tasks: Optional[List[str]] = Field(default=None)

    unique_attributes: Optional[Dict[str, Any]] = Field(default=None)

    append_relationship_attributes: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Map of append relationship attributes.",
    )
    remove_relationship_attributes: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Map of remove relationship attributes.",
    )
    add_or_update_classifications: Optional[List[AtlanTag]] = Field(
        default=None,
        description="Map of add/update classifcations of atlan tag.",
    )
    remove_classifications: Optional[List[AtlanTag]] = Field(
        default=None,
        description="Map of remove classifcations of atlan tag.",
    )
    semantic: Optional[SaveSemantic] = Field(
        default=None,
        exclude=True,
        description=(
            "Semantic for how this relationship should be saved, "
            "if used in an asset request on which `.save()` is called."
        ),
    )
    depth: Optional[int] = Field(
        default=None,
        description=(
            "Depth of this asset within lineage. "
            "Note: this will only be available in assets "
            "retrieved via lineage, and will vary even for "
            "the same asset depending on the starting point "
            "of the lineage requested."
        ),
    )
    immediate_upstream: Optional[List[LineageRef]] = Field(
        default=None,
        description=(
            "Reference details about the asset(s) that are "
            "immediately upstream of this asset within lineage. "
            "Note: this will only be available in assets retrieved "
            "via lineage when `immediate_upstream` is `True` "
            "and could vary even for the same asset depending "
            "on the starting point and depth of the lineage requested."
        ),
    )
    immediate_downstream: Optional[List[LineageRef]] = Field(
        default=None,
        description=(
            "Reference details about the asset(s) that are "
            "immediately downstream of this asset within lineage. "
            "Note: this will only be available in assets retrieved via "
            "lineage when `immediate_downstream` is `True` "
            "and could vary even for the same asset depending "
            "on the starting point and depth of the lineage requested."
        ),
    )


# Imports required for fixing circular dependencies:
from .asset import Asset  # noqa: I001, E402, F401


from .atlas_glossary_term import AtlasGlossaryTerm  # noqa: E402, F401
