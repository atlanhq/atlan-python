# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

import hashlib
import sys
import uuid
from datetime import datetime
from io import StringIO
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Type, TypeVar
from urllib.parse import quote, unquote

from pydantic.v1 import Field, PrivateAttr, StrictStr, root_validator, validator

from pyatlan.errors import ErrorCode
from pyatlan.model.core import Announcement, AtlanObject, AtlanTag, Meaning
from pyatlan.model.custom_metadata import CustomMetadataDict, CustomMetadataProxy
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    AtlanIcon,
    AtlasGlossaryCategoryType,
    AtlasGlossaryTermType,
    AtlasGlossaryType,
    CertificateStatus,
    DataProductCriticality,
    DataProductSensitivity,
    DataProductStatus,
    EntityStatus,
    FileType,
    IconType,
    MatillionJobType,
    OpenLineageRunState,
    SaveSemantic,
    SchemaRegistrySchemaCompatibility,
    SchemaRegistrySchemaType,
    SourceCostUnitType,
)
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    InternalKeywordField,
    InternalKeywordTextField,
    InternalNumericField,
    KeywordField,
    KeywordTextField,
    KeywordTextStemmedField,
    NumericField,
    NumericRankField,
    RelationField,
    TextField,
)
from pyatlan.model.search import IndexSearchRequest
from pyatlan.model.structs import (
    ColumnValueFrequencyMap,
    DbtMetricFilter,
    Histogram,
    MCRuleComparison,
    MCRuleSchedule,
    PopularityInsights,
    SourceTagAttribute,
    StarredDetails,
)
from pyatlan.utils import (
    init_guid,
    move_struct,
    next_id,
    to_camel_case,
    validate_required_fields,
)


def validate_single_required_field(field_names: list[str], values: list[Any]):
    indexes = [idx for idx, value in enumerate(values) if value is not None]
    if not indexes:
        raise ValueError(
            f"One of the following parameters are required: {', '.join(field_names)}"
        )
    if len(indexes) > 1:
        names = [field_names[idx] for idx in indexes]
        raise ValueError(
            f"Only one of the following parameters are allowed: {', '.join(names)}"
        )


SelfAsset = TypeVar("SelfAsset", bound="Asset")


class Referenceable(AtlanObject):
    """Description"""

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["attributes", "type_name"])
        __pydantic_self__._metadata_proxy = CustomMetadataProxy(
            __pydantic_self__.business_attributes
        )

    def json(self, *args, **kwargs) -> str:
        self.business_attributes = self._metadata_proxy.business_attributes
        return super().json(**kwargs)

    def validate_required(self):
        if not self.create_time or self.created_by:
            self.attributes.validate_required()

    def get_custom_metadata(self, name: str) -> CustomMetadataDict:
        return self._metadata_proxy.get_custom_metadata(name=name)

    def set_custom_metadata(self, custom_metadata: CustomMetadataDict):
        return self._metadata_proxy.set_custom_metadata(custom_metadata=custom_metadata)

    def flush_custom_metadata(self):
        self.business_attributes = self._metadata_proxy.business_attributes

    @classmethod
    def can_be_archived(self) -> bool:
        """
        Indicates if an asset can be archived via the asset.delete_by_guid method.
        :returns: True if archiving is supported
        """
        return True

    @property
    def atlan_tag_names(self) -> list[str]:
        from pyatlan.cache.atlan_tag_cache import AtlanTagCache
        from pyatlan.model.constants import DELETED_

        if self.classification_names:
            return [
                AtlanTagCache.get_name_for_id(tag_id) or DELETED_
                for tag_id in self.classification_names
            ]
        return []

    def __setattr__(self, name, value):
        if name in Referenceable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[list[str]] = [
        "qualified_name",
        "assigned_terms",
    ]

    @property
    def qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qualified_name

    @qualified_name.setter
    def qualified_name(self, qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qualified_name = qualified_name

    @property
    def assigned_terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.meanings

    @assigned_terms.setter
    def assigned_terms(self, assigned_terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = assigned_terms

    class Attributes(AtlanObject):
        qualified_name: Optional[str] = Field(default="", description="")
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship

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

    type_name: str = Field(
        default="Referenceable",
        description="Name of the type definition that defines this instance.",
    )
    _metadata_proxy: CustomMetadataProxy = PrivateAttr()
    attributes: Referenceable.Attributes = Field(
        default_factory=lambda: Referenceable.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary "
        "by type, so are described in the sub-types of this schema.",
    )
    business_attributes: Optional[dict[str, Any]] = Field(
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
        default="",
        description="Unique identifier of the entity instance.",
        example="917ffec9-fa84-4c59-8e6c-c7b114d04be3",
    )
    is_incomplete: Optional[bool] = Field(default=True, description="", example=True)
    labels: Optional[list[str]] = Field(default=None, description="Internal use only.")
    relationship_attributes: Optional[dict[str, Any]] = Field(
        default=None,
        description="Map of relationships for the entity. The specific keys of this map will vary by type, "
        "so are described in the sub-types of this schema.",
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
    atlan_tags: Optional[list[AtlanTag]] = Field(
        default=None, description="Atlan tags", alias="classifications"
    )
    classification_names: Optional[list[str]] = Field(
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
    meaning_names: Optional[list[str]] = Field(
        default=None,
        description="Names of assigned_terms that have been linked to this asset.",
    )
    meanings: Optional[list[Meaning]] = Field(
        default=None, description="", alias="meanings"
    )
    custom_attributes: Optional[dict[str, Any]] = Field(
        default=None, description="", alias="customAttributes"
    )
    scrubbed: Optional[bool] = Field(
        default=None, description="", alias="fields removed from results"
    )
    pending_tasks: Optional[list[str]] = Field(default=None)

    unique_attributes: Optional[dict[str, Any]] = Field(default=None)

    append_relationship_attributes: Optional[dict[str, Any]] = Field(
        default=None,
        description="Map of append relationship attributes.",
    )
    remove_relationship_attributes: Optional[dict[str, Any]] = Field(
        default=None,
        description="Map of remove relationship attributes.",
    )
    semantic: Optional[SaveSemantic] = Field(
        default=None,
        exclude=True,
        description=(
            "Semantic for how this relationship should be saved, "
            "if used in an asset request on which `.save()` is called."
        ),
    )


class Asset(Referenceable):
    """Description"""

    _subtypes_: dict[str, type] = dict()

    def __init_subclass__(cls, type_name=None):
        cls._subtypes_[type_name or cls.__name__.lower()] = cls

    def trim_to_required(self: SelfAsset) -> SelfAsset:
        return self.create_for_modification(
            qualified_name=self.qualified_name or "", name=self.name or ""
        )

    def trim_to_reference(self: SelfAsset) -> SelfAsset:
        if self.guid and self.guid.strip():
            return self.ref_by_guid(self.guid)
        if self.qualified_name and self.qualified_name.strip():
            return self.ref_by_qualified_name(self.qualified_name)
        if (
            self.unique_attributes
            and (qualified_name := self.unique_attributes.get("qualified_name"))
            and qualified_name.strip()
        ):
            return self.ref_by_qualified_name(qualified_name)
        raise ErrorCode.MISSING_REQUIRED_RELATIONSHIP_PARAM.exception_with_parameters(
            self.type_name, "guid, qualifiedName"
        )

    @classmethod
    @init_guid
    def create(cls: Type[SelfAsset], *args, **kwargs) -> SelfAsset:
        raise NotImplementedError(
            "Create has not been implemented for this class. Please submit an enhancement"
            "request if you need it implemented."
        )

    @classmethod
    def create_for_modification(
        cls: type[SelfAsset], qualified_name: str = "", name: str = ""
    ) -> SelfAsset:
        if cls.__name__ == "Asset":
            raise ErrorCode.METHOD_CAN_NOT_BE_INVOKED_ON_ASSET.exception_with_parameters()
        validate_required_fields(
            ["name", "qualified_name"],
            [name, qualified_name],
        )
        return cls(attributes=cls.Attributes(qualified_name=qualified_name, name=name))

    @classmethod
    def ref_by_guid(
        cls: type[SelfAsset], guid: str, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> SelfAsset:
        retval: SelfAsset = cls(attributes=cls.Attributes())
        retval.guid = guid
        retval.semantic = semantic
        return retval

    @classmethod
    def ref_by_qualified_name(
        cls: type[SelfAsset],
        qualified_name: str,
        semantic: SaveSemantic = SaveSemantic.REPLACE,
    ) -> SelfAsset:
        ret_value: SelfAsset = cls(
            attributes=cls.Attributes(name="", qualified_name=qualified_name)
        )
        ret_value.unique_attributes = {"qualifiedName": qualified_name}
        ret_value.semantic = semantic
        return ret_value

    @classmethod
    def __get_validators__(cls):
        yield cls._convert_to_real_type_

    @classmethod
    def _convert_to_real_type_(cls, data):
        if isinstance(data, Asset):
            return data

        # Handle the case where asset data is a list
        if isinstance(data, list):
            return [cls._convert_to_real_type_(item) for item in data]

        data_type = (
            data.get("type_name") if "type_name" in data else data.get("typeName")
        )

        if data_type is None:
            if issubclass(cls, Asset):
                return cls(**data)
            raise ValueError("Missing 'type' in Asset")

        sub = cls._subtypes_.get(data_type)
        if sub is None:
            sub = getattr(sys.modules["pyatlan.model.assets"], data_type)

        if sub is None:
            raise TypeError(f"Unsupport sub-type: {data_type}")

        move_struct(data)
        return sub(**data)

    if TYPE_CHECKING:
        from pyatlan.model.lineage import FluentLineage

    @classmethod
    def lineage(cls, guid: str, include_archived: bool = False) -> "FluentLineage":
        """
        Start a FluentLineage that can be used to get a LineageListRequest that can be used to retrieve all downstream
        assets. Additional conditions can be chained onto the returned FluentLineage before any asset retrieval is
        attempted, ensuring all conditions are pushed-down for optimal retrieval. (To change the default direction of
        downstream chain a .direction() call

        :param guid: unique identifier (GUID) for the starting point of lineage
        :param include_archived: when True, archived (soft-deleted) assets in lineage will be included
        :returns: a FluentLineage that can be used to get a LineageListRequest that can be used to retrieve all
        downstream assets
        """
        from pyatlan.model.lineage import FluentLineage

        if not include_archived:
            return FluentLineage(
                starting_guid=guid,
                where_assets=FluentLineage.ACTIVE,
                where_relationships=FluentLineage.ACTIVE,
                includes_in_results=FluentLineage.ACTIVE,
            )
        return FluentLineage(starting_guid=guid)

    def has_announcement(self) -> bool:
        return bool(
            self.attributes
            and (
                self.attributes.announcement_title or self.attributes.announcement_type
            )
        )

    def set_announcement(self, announcement: Announcement) -> None:
        self.attributes.announcement_type = announcement.announcement_type.value
        self.attributes.announcement_title = announcement.announcement_title
        self.attributes.announcement_message = announcement.announcement_message

    def get_announcment(self) -> Optional[Announcement]:
        if self.attributes.announcement_type and self.attributes.announcement_title:
            return Announcement(
                announcement_type=AnnouncementType[
                    self.attributes.announcement_type.upper()
                ],
                announcement_title=self.attributes.announcement_title,
                announcement_message=self.attributes.announcement_message,
            )
        return None

    def remove_announcement(self):
        self.attributes.remove_announcement()

    def remove_description(self):
        self.attributes.remove_description()

    def remove_user_description(self):
        self.attributes.remove_user_description()

    def remove_owners(self):
        self.attributes.remove_owners()

    def remove_certificate(self):
        self.attributes.remove_certificate()

    type_name: str = Field(default="Asset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Asset":
            raise ValueError("must be Asset")
        return v

    def __setattr__(self, name, value):
        if name in Asset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    NAME: ClassVar[KeywordTextStemmedField] = KeywordTextStemmedField(
        "name", "name.keyword", "name", "name.stemmed"
    )
    """
    Name of this asset. Fallback for display purposes, if displayName is empty.
    """
    DISPLAY_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "displayName", "displayName.keyword", "displayName"
    )
    """
    Human-readable name of this asset used for display purposes (in user interface).
    """
    DESCRIPTION: ClassVar[KeywordTextField] = KeywordTextField(
        "description", "description.keyword", "description"
    )
    """
    Description of this asset, for example as crawled from a source. Fallback for display purposes, if userDescription is empty.
    """  # noqa: E501
    USER_DESCRIPTION: ClassVar[KeywordTextField] = KeywordTextField(
        "userDescription", "userDescription.keyword", "userDescription"
    )
    """
    Description of this asset, as provided by a user. If present, this will be used for the description in user interface.
    """  # noqa: E501
    TENANT_ID: ClassVar[KeywordField] = KeywordField("tenantId", "tenantId")
    """
    Name of the Atlan workspace in which this asset exists.
    """
    CERTIFICATE_STATUS: ClassVar[KeywordTextField] = KeywordTextField(
        "certificateStatus", "certificateStatus", "certificateStatus.text"
    )
    """
    Status of this asset's certification.
    """
    CERTIFICATE_STATUS_MESSAGE: ClassVar[KeywordField] = KeywordField(
        "certificateStatusMessage", "certificateStatusMessage"
    )
    """
    Human-readable descriptive message used to provide further detail to certificateStatus.
    """
    CERTIFICATE_UPDATED_BY: ClassVar[KeywordField] = KeywordField(
        "certificateUpdatedBy", "certificateUpdatedBy"
    )
    """
    Name of the user who last updated the certification of this asset.
    """
    CERTIFICATE_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "certificateUpdatedAt", "certificateUpdatedAt"
    )
    """
    Time (epoch) at which the certification was last updated, in milliseconds.
    """
    ANNOUNCEMENT_TITLE: ClassVar[KeywordField] = KeywordField(
        "announcementTitle", "announcementTitle"
    )
    """
    Brief title for the announcement on this asset. Required when announcementType is specified.
    """
    ANNOUNCEMENT_MESSAGE: ClassVar[KeywordField] = KeywordField(
        "announcementMessage", "announcementMessage"
    )
    """
    Detailed message to include in the announcement on this asset.
    """
    ANNOUNCEMENT_TYPE: ClassVar[KeywordField] = KeywordField(
        "announcementType", "announcementType"
    )
    """
    Type of announcement on this asset.
    """
    ANNOUNCEMENT_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "announcementUpdatedAt", "announcementUpdatedAt"
    )
    """
    Time (epoch) at which the announcement was last updated, in milliseconds.
    """
    ANNOUNCEMENT_UPDATED_BY: ClassVar[KeywordField] = KeywordField(
        "announcementUpdatedBy", "announcementUpdatedBy"
    )
    """
    Name of the user who last updated the announcement.
    """
    OWNER_USERS: ClassVar[KeywordField] = KeywordField("ownerUsers", "ownerUsers")
    """
    List of users who own this asset.
    """
    OWNER_GROUPS: ClassVar[KeywordField] = KeywordField("ownerGroups", "ownerGroups")
    """
    List of groups who own this asset.
    """
    ADMIN_USERS: ClassVar[KeywordField] = KeywordField("adminUsers", "adminUsers")
    """
    List of users who administer this asset. (This is only used for certain asset types.)
    """
    ADMIN_GROUPS: ClassVar[KeywordField] = KeywordField("adminGroups", "adminGroups")
    """
    List of groups who administer this asset. (This is only used for certain asset types.)
    """
    VIEWER_USERS: ClassVar[KeywordField] = KeywordField("viewerUsers", "viewerUsers")
    """
    List of users who can view assets contained in a collection. (This is only used for certain asset types.)
    """
    VIEWER_GROUPS: ClassVar[KeywordField] = KeywordField("viewerGroups", "viewerGroups")
    """
    List of groups who can view assets contained in a collection. (This is only used for certain asset types.)
    """
    CONNECTOR_NAME: ClassVar[KeywordField] = KeywordField(
        "connectorName", "connectorName"
    )
    """
    Type of the connector through which this asset is accessible.
    """
    CONNECTION_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "connectionName", "connectionName", "connectionName.text"
    )
    """
    Simple name of the connection through which this asset is accessible.
    """
    CONNECTION_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "connectionQualifiedName",
        "connectionQualifiedName",
        "connectionQualifiedName.text",
    )
    """
    Unique name of the connection through which this asset is accessible.
    """
    HAS_LINEAGE: ClassVar[BooleanField] = BooleanField("__hasLineage", "__hasLineage")
    """
    Whether this asset has lineage (true) or not (false).
    """
    IS_DISCOVERABLE: ClassVar[BooleanField] = BooleanField(
        "isDiscoverable", "isDiscoverable"
    )
    """
    Whether this asset is discoverable through the UI (true) or not (false).
    """
    IS_EDITABLE: ClassVar[BooleanField] = BooleanField("isEditable", "isEditable")
    """
    Whether this asset can be edited in the UI (true) or not (false).
    """
    SUB_TYPE: ClassVar[KeywordField] = KeywordField("subType", "subType")
    """
    Subtype of this asset.
    """
    VIEW_SCORE: ClassVar[NumericRankField] = NumericRankField(
        "viewScore", "viewScore", "viewScore.rank_feature"
    )
    """
    View score for this asset.
    """
    POPULARITY_SCORE: ClassVar[NumericRankField] = NumericRankField(
        "popularityScore", "popularityScore", "popularityScore.rank_feature"
    )
    """
    Popularity score for this asset.
    """
    SOURCE_OWNERS: ClassVar[KeywordField] = KeywordField("sourceOwners", "sourceOwners")
    """
    List of owners of this asset, in the source system.
    """
    SOURCE_CREATED_BY: ClassVar[KeywordField] = KeywordField(
        "sourceCreatedBy", "sourceCreatedBy"
    )
    """
    Name of the user who created this asset, in the source system.
    """
    SOURCE_CREATED_AT: ClassVar[NumericField] = NumericField(
        "sourceCreatedAt", "sourceCreatedAt"
    )
    """
    Time (epoch) at which this asset was created in the source system, in milliseconds.
    """
    SOURCE_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "sourceUpdatedAt", "sourceUpdatedAt"
    )
    """
    Time (epoch) at which this asset was last updated in the source system, in milliseconds.
    """
    SOURCE_UPDATED_BY: ClassVar[KeywordField] = KeywordField(
        "sourceUpdatedBy", "sourceUpdatedBy"
    )
    """
    Name of the user who last updated this asset, in the source system.
    """
    SOURCE_URL: ClassVar[KeywordField] = KeywordField("sourceURL", "sourceURL")
    """
    URL to the resource within the source application, used to create a button to view this asset in the source application.
    """  # noqa: E501
    SOURCE_EMBED_URL: ClassVar[KeywordField] = KeywordField(
        "sourceEmbedURL", "sourceEmbedURL"
    )
    """
    URL to create an embed for a resource (for example, an image of a dashboard) within Atlan.
    """
    LAST_SYNC_WORKFLOW_NAME: ClassVar[KeywordField] = KeywordField(
        "lastSyncWorkflowName", "lastSyncWorkflowName"
    )
    """
    Name of the crawler that last synchronized this asset.
    """
    LAST_SYNC_RUN_AT: ClassVar[NumericField] = NumericField(
        "lastSyncRunAt", "lastSyncRunAt"
    )
    """
    Time (epoch) at which this asset was last crawled, in milliseconds.
    """
    LAST_SYNC_RUN: ClassVar[KeywordField] = KeywordField("lastSyncRun", "lastSyncRun")
    """
    Name of the last run of the crawler that last synchronized this asset.
    """
    ADMIN_ROLES: ClassVar[KeywordField] = KeywordField("adminRoles", "adminRoles")
    """
    List of roles who administer this asset. (This is only used for Connection assets.)
    """
    SOURCE_READ_COUNT: ClassVar[NumericField] = NumericField(
        "sourceReadCount", "sourceReadCount"
    )
    """
    Total count of all read operations at source.
    """
    SOURCE_READ_USER_COUNT: ClassVar[NumericField] = NumericField(
        "sourceReadUserCount", "sourceReadUserCount"
    )
    """
    Total number of unique users that read data from asset.
    """
    SOURCE_LAST_READ_AT: ClassVar[NumericField] = NumericField(
        "sourceLastReadAt", "sourceLastReadAt"
    )
    """
    Timestamp of most recent read operation.
    """
    LAST_ROW_CHANGED_AT: ClassVar[NumericField] = NumericField(
        "lastRowChangedAt", "lastRowChangedAt"
    )
    """
    Time (epoch) of the last operation that inserted, updated, or deleted rows, in milliseconds.
    """
    SOURCE_TOTAL_COST: ClassVar[NumericField] = NumericField(
        "sourceTotalCost", "sourceTotalCost"
    )
    """
    Total cost of all operations at source.
    """
    SOURCE_COST_UNIT: ClassVar[KeywordField] = KeywordField(
        "sourceCostUnit", "sourceCostUnit"
    )
    """
    The unit of measure for sourceTotalCost.
    """
    SOURCE_READ_QUERY_COST: ClassVar[NumericField] = NumericField(
        "sourceReadQueryCost", "sourceReadQueryCost"
    )
    """
    Total cost of read queries at source.
    """
    SOURCE_READ_RECENT_USER_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadRecentUserList", "sourceReadRecentUserList"
    )
    """
    List of usernames of the most recent users who read this asset.
    """
    SOURCE_READ_RECENT_USER_RECORD_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadRecentUserRecordList", "sourceReadRecentUserRecordList"
    )
    """
    List of usernames with extra insights for the most recent users who read this asset.
    """
    SOURCE_READ_TOP_USER_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadTopUserList", "sourceReadTopUserList"
    )
    """
    List of usernames of the users who read this asset the most.
    """
    SOURCE_READ_TOP_USER_RECORD_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadTopUserRecordList", "sourceReadTopUserRecordList"
    )
    """
    List of usernames with extra insights for the users who read this asset the most.
    """
    SOURCE_READ_POPULAR_QUERY_RECORD_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadPopularQueryRecordList", "sourceReadPopularQueryRecordList"
    )
    """
    List of the most popular queries that accessed this asset.
    """
    SOURCE_READ_EXPENSIVE_QUERY_RECORD_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadExpensiveQueryRecordList", "sourceReadExpensiveQueryRecordList"
    )
    """
    List of the most expensive queries that accessed this asset.
    """
    SOURCE_READ_SLOW_QUERY_RECORD_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadSlowQueryRecordList", "sourceReadSlowQueryRecordList"
    )
    """
    List of the slowest queries that accessed this asset.
    """
    SOURCE_QUERY_COMPUTE_COST_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceQueryComputeCostList", "sourceQueryComputeCostList"
    )
    """
    List of most expensive warehouse names.
    """
    SOURCE_QUERY_COMPUTE_COST_RECORD_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceQueryComputeCostRecordList", "sourceQueryComputeCostRecordList"
    )
    """
    List of most expensive warehouses with extra insights.
    """
    DBT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtQualifiedName", "dbtQualifiedName", "dbtQualifiedName.text"
    )
    """
    Unique name of this asset in dbt.
    """
    ASSET_DBT_ALIAS: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtAlias", "assetDbtAlias.keyword", "assetDbtAlias"
    )
    """
    Alias of this asset in dbt.
    """
    ASSET_DBT_META: ClassVar[KeywordField] = KeywordField(
        "assetDbtMeta", "assetDbtMeta"
    )
    """
    Metadata for this asset in dbt, specifically everything under the 'meta' key in the dbt object.
    """
    ASSET_DBT_UNIQUE_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtUniqueId", "assetDbtUniqueId.keyword", "assetDbtUniqueId"
    )
    """
    Unique identifier of this asset in dbt.
    """
    ASSET_DBT_ACCOUNT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtAccountName", "assetDbtAccountName.keyword", "assetDbtAccountName"
    )
    """
    Name of the account in which this asset exists in dbt.
    """
    ASSET_DBT_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtProjectName", "assetDbtProjectName.keyword", "assetDbtProjectName"
    )
    """
    Name of the project in which this asset exists in dbt.
    """
    ASSET_DBT_PACKAGE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtPackageName", "assetDbtPackageName.keyword", "assetDbtPackageName"
    )
    """
    Name of the package in which this asset exists in dbt.
    """
    ASSET_DBT_JOB_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtJobName", "assetDbtJobName.keyword", "assetDbtJobName"
    )
    """
    Name of the job that materialized this asset in dbt.
    """
    ASSET_DBT_JOB_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobSchedule", "assetDbtJobSchedule"
    )
    """
    Schedule of the job that materialized this asset in dbt.
    """
    ASSET_DBT_JOB_STATUS: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobStatus", "assetDbtJobStatus"
    )
    """
    Status of the job that materialized this asset in dbt.
    """
    ASSET_DBT_TEST_STATUS: ClassVar[KeywordField] = KeywordField(
        "assetDbtTestStatus", "assetDbtTestStatus"
    )
    """
    All associated dbt test statuses.
    """
    ASSET_DBT_JOB_SCHEDULE_CRON_HUMANIZED: ClassVar[TextField] = TextField(
        "assetDbtJobScheduleCronHumanized", "assetDbtJobScheduleCronHumanized"
    )
    """
    Human-readable cron schedule of the job that materialized this asset in dbt.
    """
    ASSET_DBT_JOB_LAST_RUN: ClassVar[NumericField] = NumericField(
        "assetDbtJobLastRun", "assetDbtJobLastRun"
    )
    """
    Time (epoch) at which the job that materialized this asset in dbt last ran, in milliseconds.
    """
    ASSET_DBT_JOB_LAST_RUN_URL: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunUrl", "assetDbtJobLastRunUrl"
    )
    """
    URL of the last run of the job that materialized this asset in dbt.
    """
    ASSET_DBT_JOB_LAST_RUN_CREATED_AT: ClassVar[NumericField] = NumericField(
        "assetDbtJobLastRunCreatedAt", "assetDbtJobLastRunCreatedAt"
    )
    """
    Time (epoch) at which the job that materialized this asset in dbt was last created, in milliseconds.
    """
    ASSET_DBT_JOB_LAST_RUN_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "assetDbtJobLastRunUpdatedAt", "assetDbtJobLastRunUpdatedAt"
    )
    """
    Time (epoch) at which the job that materialized this asset in dbt was last updated, in milliseconds.
    """
    ASSET_DBT_JOB_LAST_RUN_DEQUED_AT: ClassVar[NumericField] = NumericField(
        "assetDbtJobLastRunDequedAt", "assetDbtJobLastRunDequedAt"
    )
    """
    Time (epoch) at which the job that materialized this asset in dbt was dequeued, in milliseconds.
    """
    ASSET_DBT_JOB_LAST_RUN_STARTED_AT: ClassVar[NumericField] = NumericField(
        "assetDbtJobLastRunStartedAt", "assetDbtJobLastRunStartedAt"
    )
    """
    Time (epoch) at which the job that materialized this asset in dbt was started running, in milliseconds.
    """
    ASSET_DBT_JOB_LAST_RUN_TOTAL_DURATION: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunTotalDuration", "assetDbtJobLastRunTotalDuration"
    )
    """
    Total duration of the last run of the job that materialized this asset in dbt.
    """
    ASSET_DBT_JOB_LAST_RUN_TOTAL_DURATION_HUMANIZED: ClassVar[
        KeywordField
    ] = KeywordField(
        "assetDbtJobLastRunTotalDurationHumanized",
        "assetDbtJobLastRunTotalDurationHumanized",
    )
    """
    Human-readable total duration of the last run of the job that materialized this asset in dbt.
    """
    ASSET_DBT_JOB_LAST_RUN_QUEUED_DURATION: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunQueuedDuration", "assetDbtJobLastRunQueuedDuration"
    )
    """
    Total duration the job that materialized this asset in dbt spent being queued.
    """
    ASSET_DBT_JOB_LAST_RUN_QUEUED_DURATION_HUMANIZED: ClassVar[
        KeywordField
    ] = KeywordField(
        "assetDbtJobLastRunQueuedDurationHumanized",
        "assetDbtJobLastRunQueuedDurationHumanized",
    )
    """
    Human-readable total duration of the last run of the job that materialized this asset in dbt spend being queued.
    """
    ASSET_DBT_JOB_LAST_RUN_RUN_DURATION: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunRunDuration", "assetDbtJobLastRunRunDuration"
    )
    """
    Run duration of the last run of the job that materialized this asset in dbt.
    """
    ASSET_DBT_JOB_LAST_RUN_RUN_DURATION_HUMANIZED: ClassVar[
        KeywordField
    ] = KeywordField(
        "assetDbtJobLastRunRunDurationHumanized",
        "assetDbtJobLastRunRunDurationHumanized",
    )
    """
    Human-readable run duration of the last run of the job that materialized this asset in dbt.
    """
    ASSET_DBT_JOB_LAST_RUN_GIT_BRANCH: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtJobLastRunGitBranch",
        "assetDbtJobLastRunGitBranch",
        "assetDbtJobLastRunGitBranch.text",
    )
    """
    Branch in git from which the last run of the job that materialized this asset in dbt ran.
    """
    ASSET_DBT_JOB_LAST_RUN_GIT_SHA: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunGitSha", "assetDbtJobLastRunGitSha"
    )
    """
    SHA hash in git for the last run of the job that materialized this asset in dbt.
    """
    ASSET_DBT_JOB_LAST_RUN_STATUS_MESSAGE: ClassVar[
        KeywordTextField
    ] = KeywordTextField(
        "assetDbtJobLastRunStatusMessage",
        "assetDbtJobLastRunStatusMessage.keyword",
        "assetDbtJobLastRunStatusMessage",
    )
    """
    Status message of the last run of the job that materialized this asset in dbt.
    """
    ASSET_DBT_JOB_LAST_RUN_OWNER_THREAD_ID: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunOwnerThreadId", "assetDbtJobLastRunOwnerThreadId"
    )
    """
    Thread ID of the owner of the last run of the job that materialized this asset in dbt.
    """
    ASSET_DBT_JOB_LAST_RUN_EXECUTED_BY_THREAD_ID: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunExecutedByThreadId", "assetDbtJobLastRunExecutedByThreadId"
    )
    """
    Thread ID of the user who executed the last run of the job that materialized this asset in dbt.
    """
    ASSET_DBT_JOB_LAST_RUN_ARTIFACTS_SAVED: ClassVar[BooleanField] = BooleanField(
        "assetDbtJobLastRunArtifactsSaved", "assetDbtJobLastRunArtifactsSaved"
    )
    """
    Whether artifacts were saved from the last run of the job that materialized this asset in dbt (true) or not (false).
    """
    ASSET_DBT_JOB_LAST_RUN_ARTIFACT_S3PATH: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunArtifactS3Path", "assetDbtJobLastRunArtifactS3Path"
    )
    """
    Path in S3 to the artifacts saved from the last run of the job that materialized this asset in dbt.
    """
    ASSET_DBT_JOB_LAST_RUN_HAS_DOCS_GENERATED: ClassVar[BooleanField] = BooleanField(
        "assetDbtJobLastRunHasDocsGenerated", "assetDbtJobLastRunHasDocsGenerated"
    )
    """
    Whether docs were generated from the last run of the job that materialized this asset in dbt (true) or not (false).
    """
    ASSET_DBT_JOB_LAST_RUN_HAS_SOURCES_GENERATED: ClassVar[BooleanField] = BooleanField(
        "assetDbtJobLastRunHasSourcesGenerated", "assetDbtJobLastRunHasSourcesGenerated"
    )
    """
    Whether sources were generated from the last run of the job that materialized this asset in dbt (true) or not (false).
    """  # noqa: E501
    ASSET_DBT_JOB_LAST_RUN_NOTIFICATIONS_SENT: ClassVar[BooleanField] = BooleanField(
        "assetDbtJobLastRunNotificationsSent", "assetDbtJobLastRunNotificationsSent"
    )
    """
    Whether notifications were sent from the last run of the job that materialized this asset in dbt (true) or not (false).
    """  # noqa: E501
    ASSET_DBT_JOB_NEXT_RUN: ClassVar[NumericField] = NumericField(
        "assetDbtJobNextRun", "assetDbtJobNextRun"
    )
    """
    Time (epoch) when the next run of the job that materializes this asset in dbt is scheduled.
    """
    ASSET_DBT_JOB_NEXT_RUN_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtJobNextRunHumanized",
        "assetDbtJobNextRunHumanized.keyword",
        "assetDbtJobNextRunHumanized",
    )
    """
    Human-readable time when the next run of the job that materializes this asset in dbt is scheduled.
    """
    ASSET_DBT_ENVIRONMENT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtEnvironmentName",
        "assetDbtEnvironmentName.keyword",
        "assetDbtEnvironmentName",
    )
    """
    Name of the environment in which this asset is materialized in dbt.
    """
    ASSET_DBT_ENVIRONMENT_DBT_VERSION: ClassVar[KeywordField] = KeywordField(
        "assetDbtEnvironmentDbtVersion", "assetDbtEnvironmentDbtVersion"
    )
    """
    Version of the environment in which this asset is materialized in dbt.
    """
    ASSET_DBT_TAGS: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtTags", "assetDbtTags", "assetDbtTags.text"
    )
    """
    List of tags attached to this asset in dbt.
    """
    ASSET_DBT_SEMANTIC_LAYER_PROXY_URL: ClassVar[KeywordField] = KeywordField(
        "assetDbtSemanticLayerProxyUrl", "assetDbtSemanticLayerProxyUrl"
    )
    """
    URL of the semantic layer proxy for this asset in dbt.
    """
    ASSET_DBT_SOURCE_FRESHNESS_CRITERIA: ClassVar[KeywordField] = KeywordField(
        "assetDbtSourceFreshnessCriteria", "assetDbtSourceFreshnessCriteria"
    )
    """
    Freshness criteria for the source of this asset in dbt.
    """
    SAMPLE_DATA_URL: ClassVar[KeywordTextField] = KeywordTextField(
        "sampleDataUrl", "sampleDataUrl", "sampleDataUrl.text"
    )
    """
    URL for sample data for this asset.
    """
    ASSET_TAGS: ClassVar[KeywordTextField] = KeywordTextField(
        "assetTags", "assetTags", "assetTags.text"
    )
    """
    List of tags attached to this asset.
    """
    ASSET_MC_INCIDENT_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "assetMcIncidentNames", "assetMcIncidentNames.keyword", "assetMcIncidentNames"
    )
    """
    List of Monte Carlo incident names attached to this asset.
    """
    ASSET_MC_INCIDENT_QUALIFIED_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "assetMcIncidentQualifiedNames",
        "assetMcIncidentQualifiedNames",
        "assetMcIncidentQualifiedNames.text",
    )
    """
    List of unique Monte Carlo incident names attached to this asset.
    """
    ASSET_MC_MONITOR_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "assetMcMonitorNames", "assetMcMonitorNames.keyword", "assetMcMonitorNames"
    )
    """
    List of Monte Carlo monitor names attached to this asset.
    """
    ASSET_MC_MONITOR_QUALIFIED_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "assetMcMonitorQualifiedNames",
        "assetMcMonitorQualifiedNames",
        "assetMcMonitorQualifiedNames.text",
    )
    """
    List of unique Monte Carlo monitor names attached to this asset.
    """
    ASSET_MC_MONITOR_STATUSES: ClassVar[KeywordField] = KeywordField(
        "assetMcMonitorStatuses", "assetMcMonitorStatuses"
    )
    """
    Statuses of all associated Monte Carlo monitors.
    """
    ASSET_MC_MONITOR_TYPES: ClassVar[KeywordField] = KeywordField(
        "assetMcMonitorTypes", "assetMcMonitorTypes"
    )
    """
    Types of all associated Monte Carlo monitors.
    """
    ASSET_MC_MONITOR_SCHEDULE_TYPES: ClassVar[KeywordField] = KeywordField(
        "assetMcMonitorScheduleTypes", "assetMcMonitorScheduleTypes"
    )
    """
    Schedules of all associated Monte Carlo monitors.
    """
    ASSET_MC_INCIDENT_TYPES: ClassVar[KeywordField] = KeywordField(
        "assetMcIncidentTypes", "assetMcIncidentTypes"
    )
    """
    List of Monte Carlo incident types associated with this asset.
    """
    ASSET_MC_INCIDENT_SUB_TYPES: ClassVar[KeywordField] = KeywordField(
        "assetMcIncidentSubTypes", "assetMcIncidentSubTypes"
    )
    """
    List of Monte Carlo incident sub-types associated with this asset.
    """
    ASSET_MC_INCIDENT_SEVERITIES: ClassVar[KeywordField] = KeywordField(
        "assetMcIncidentSeverities", "assetMcIncidentSeverities"
    )
    """
    List of Monte Carlo incident severities associated with this asset.
    """
    ASSET_MC_INCIDENT_STATES: ClassVar[KeywordField] = KeywordField(
        "assetMcIncidentStates", "assetMcIncidentStates"
    )
    """
    List of Monte Carlo incident states associated with this asset.
    """
    ASSET_MC_LAST_SYNC_RUN_AT: ClassVar[NumericField] = NumericField(
        "assetMcLastSyncRunAt", "assetMcLastSyncRunAt"
    )
    """
    Time (epoch) at which this asset was last synced from Monte Carlo.
    """
    STARRED_BY: ClassVar[KeywordField] = KeywordField("starredBy", "starredBy")
    """
    Users who have starred this asset.
    """
    STARRED_DETAILS_LIST: ClassVar[KeywordField] = KeywordField(
        "starredDetailsList", "starredDetailsList"
    )
    """
    List of usernames with extra information of the users who have starred an asset.
    """
    STARRED_COUNT: ClassVar[NumericField] = NumericField("starredCount", "starredCount")
    """
    Number of users who have starred this asset.
    """
    ASSET_SODA_DQ_STATUS: ClassVar[KeywordField] = KeywordField(
        "assetSodaDQStatus", "assetSodaDQStatus"
    )
    """
    Status of data quality from Soda.
    """
    ASSET_SODA_CHECK_COUNT: ClassVar[NumericField] = NumericField(
        "assetSodaCheckCount", "assetSodaCheckCount"
    )
    """
    Number of checks done via Soda.
    """
    ASSET_SODA_LAST_SYNC_RUN_AT: ClassVar[NumericField] = NumericField(
        "assetSodaLastSyncRunAt", "assetSodaLastSyncRunAt"
    )
    """

    """
    ASSET_SODA_LAST_SCAN_AT: ClassVar[NumericField] = NumericField(
        "assetSodaLastScanAt", "assetSodaLastScanAt"
    )
    """

    """
    ASSET_SODA_CHECK_STATUSES: ClassVar[KeywordField] = KeywordField(
        "assetSodaCheckStatuses", "assetSodaCheckStatuses"
    )
    """
    All associated Soda check statuses.
    """
    ASSET_SODA_SOURCE_URL: ClassVar[KeywordField] = KeywordField(
        "assetSodaSourceURL", "assetSodaSourceURL"
    )
    """

    """
    ASSET_ICON: ClassVar[KeywordField] = KeywordField("assetIcon", "assetIcon")
    """
    Name of the icon to use for this asset. (Only applies to glossaries, currently.)
    """
    IS_PARTIAL: ClassVar[BooleanField] = BooleanField("isPartial", "isPartial")
    """
    TBC
    """
    IS_AI_GENERATED: ClassVar[BooleanField] = BooleanField(
        "isAIGenerated", "isAIGenerated"
    )
    """

    """
    ASSET_COVER_IMAGE: ClassVar[KeywordField] = KeywordField(
        "assetCoverImage", "assetCoverImage"
    )
    """
    TBC
    """
    ASSET_THEME_HEX: ClassVar[KeywordField] = KeywordField(
        "assetThemeHex", "assetThemeHex"
    )
    """
    Color (in hexadecimal RGB) to use to represent this asset.
    """

    SCHEMA_REGISTRY_SUBJECTS: ClassVar[RelationField] = RelationField(
        "schemaRegistrySubjects"
    )
    """
    TBC
    """
    MC_MONITORS: ClassVar[RelationField] = RelationField("mcMonitors")
    """
    TBC
    """
    OUTPUT_PORT_DATA_PRODUCTS: ClassVar[RelationField] = RelationField(
        "outputPortDataProducts"
    )
    """
    TBC
    """
    FILES: ClassVar[RelationField] = RelationField("files")
    """
    TBC
    """
    MC_INCIDENTS: ClassVar[RelationField] = RelationField("mcIncidents")
    """
    TBC
    """
    LINKS: ClassVar[RelationField] = RelationField("links")
    """
    TBC
    """
    METRICS: ClassVar[RelationField] = RelationField("metrics")
    """
    TBC
    """
    README: ClassVar[RelationField] = RelationField("readme")
    """
    TBC
    """
    SODA_CHECKS: ClassVar[RelationField] = RelationField("sodaChecks")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "name",
        "display_name",
        "description",
        "user_description",
        "tenant_id",
        "certificate_status",
        "certificate_status_message",
        "certificate_updated_by",
        "certificate_updated_at",
        "announcement_title",
        "announcement_message",
        "announcement_type",
        "announcement_updated_at",
        "announcement_updated_by",
        "owner_users",
        "owner_groups",
        "admin_users",
        "admin_groups",
        "viewer_users",
        "viewer_groups",
        "connector_name",
        "connection_name",
        "connection_qualified_name",
        "has_lineage",
        "is_discoverable",
        "is_editable",
        "sub_type",
        "view_score",
        "popularity_score",
        "source_owners",
        "source_created_by",
        "source_created_at",
        "source_updated_at",
        "source_updated_by",
        "source_url",
        "source_embed_url",
        "last_sync_workflow_name",
        "last_sync_run_at",
        "last_sync_run",
        "admin_roles",
        "source_read_count",
        "source_read_user_count",
        "source_last_read_at",
        "last_row_changed_at",
        "source_total_cost",
        "source_cost_unit",
        "source_read_query_cost",
        "source_read_recent_user_list",
        "source_read_recent_user_record_list",
        "source_read_top_user_list",
        "source_read_top_user_record_list",
        "source_read_popular_query_record_list",
        "source_read_expensive_query_record_list",
        "source_read_slow_query_record_list",
        "source_query_compute_cost_list",
        "source_query_compute_cost_record_list",
        "dbt_qualified_name",
        "asset_dbt_alias",
        "asset_dbt_meta",
        "asset_dbt_unique_id",
        "asset_dbt_account_name",
        "asset_dbt_project_name",
        "asset_dbt_package_name",
        "asset_dbt_job_name",
        "asset_dbt_job_schedule",
        "asset_dbt_job_status",
        "asset_dbt_test_status",
        "asset_dbt_job_schedule_cron_humanized",
        "asset_dbt_job_last_run",
        "asset_dbt_job_last_run_url",
        "asset_dbt_job_last_run_created_at",
        "asset_dbt_job_last_run_updated_at",
        "asset_dbt_job_last_run_dequed_at",
        "asset_dbt_job_last_run_started_at",
        "asset_dbt_job_last_run_total_duration",
        "asset_dbt_job_last_run_total_duration_humanized",
        "asset_dbt_job_last_run_queued_duration",
        "asset_dbt_job_last_run_queued_duration_humanized",
        "asset_dbt_job_last_run_run_duration",
        "asset_dbt_job_last_run_run_duration_humanized",
        "asset_dbt_job_last_run_git_branch",
        "asset_dbt_job_last_run_git_sha",
        "asset_dbt_job_last_run_status_message",
        "asset_dbt_job_last_run_owner_thread_id",
        "asset_dbt_job_last_run_executed_by_thread_id",
        "asset_dbt_job_last_run_artifacts_saved",
        "asset_dbt_job_last_run_artifact_s3_path",
        "asset_dbt_job_last_run_has_docs_generated",
        "asset_dbt_job_last_run_has_sources_generated",
        "asset_dbt_job_last_run_notifications_sent",
        "asset_dbt_job_next_run",
        "asset_dbt_job_next_run_humanized",
        "asset_dbt_environment_name",
        "asset_dbt_environment_dbt_version",
        "asset_dbt_tags",
        "asset_dbt_semantic_layer_proxy_url",
        "asset_dbt_source_freshness_criteria",
        "sample_data_url",
        "asset_tags",
        "asset_mc_incident_names",
        "asset_mc_incident_qualified_names",
        "asset_mc_monitor_names",
        "asset_mc_monitor_qualified_names",
        "asset_mc_monitor_statuses",
        "asset_mc_monitor_types",
        "asset_mc_monitor_schedule_types",
        "asset_mc_incident_types",
        "asset_mc_incident_sub_types",
        "asset_mc_incident_severities",
        "asset_mc_incident_states",
        "asset_mc_last_sync_run_at",
        "starred_by",
        "starred_details_list",
        "starred_count",
        "asset_soda_d_q_status",
        "asset_soda_check_count",
        "asset_soda_last_sync_run_at",
        "asset_soda_last_scan_at",
        "asset_soda_check_statuses",
        "asset_soda_source_url",
        "asset_icon",
        "is_partial",
        "is_a_i_generated",
        "asset_cover_image",
        "asset_theme_hex",
        "schema_registry_subjects",
        "mc_monitors",
        "output_port_data_products",
        "files",
        "mc_incidents",
        "links",
        "metrics",
        "readme",
        "soda_checks",
        "assigned_terms",
    ]

    @property
    def name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.name

    @name.setter
    def name(self, name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.name = name

    @property
    def display_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.display_name

    @display_name.setter
    def display_name(self, display_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.display_name = display_name

    @property
    def description(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.description

    @description.setter
    def description(self, description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.description = description

    @property
    def user_description(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.user_description

    @user_description.setter
    def user_description(self, user_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.user_description = user_description

    @property
    def tenant_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.tenant_id

    @tenant_id.setter
    def tenant_id(self, tenant_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tenant_id = tenant_id

    @property
    def certificate_status(self) -> Optional[CertificateStatus]:
        return None if self.attributes is None else self.attributes.certificate_status

    @certificate_status.setter
    def certificate_status(self, certificate_status: Optional[CertificateStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certificate_status = certificate_status

    @property
    def certificate_status_message(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.certificate_status_message
        )

    @certificate_status_message.setter
    def certificate_status_message(self, certificate_status_message: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certificate_status_message = certificate_status_message

    @property
    def certificate_updated_by(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.certificate_updated_by
        )

    @certificate_updated_by.setter
    def certificate_updated_by(self, certificate_updated_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certificate_updated_by = certificate_updated_by

    @property
    def certificate_updated_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.certificate_updated_at
        )

    @certificate_updated_at.setter
    def certificate_updated_at(self, certificate_updated_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certificate_updated_at = certificate_updated_at

    @property
    def announcement_title(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.announcement_title

    @announcement_title.setter
    def announcement_title(self, announcement_title: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.announcement_title = announcement_title

    @property
    def announcement_message(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.announcement_message

    @announcement_message.setter
    def announcement_message(self, announcement_message: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.announcement_message = announcement_message

    @property
    def announcement_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.announcement_type

    @announcement_type.setter
    def announcement_type(self, announcement_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.announcement_type = announcement_type

    @property
    def announcement_updated_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.announcement_updated_at
        )

    @announcement_updated_at.setter
    def announcement_updated_at(self, announcement_updated_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.announcement_updated_at = announcement_updated_at

    @property
    def announcement_updated_by(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.announcement_updated_by
        )

    @announcement_updated_by.setter
    def announcement_updated_by(self, announcement_updated_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.announcement_updated_by = announcement_updated_by

    @property
    def owner_users(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.owner_users

    @owner_users.setter
    def owner_users(self, owner_users: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.owner_users = owner_users

    @property
    def owner_groups(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.owner_groups

    @owner_groups.setter
    def owner_groups(self, owner_groups: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.owner_groups = owner_groups

    @property
    def admin_users(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.admin_users

    @admin_users.setter
    def admin_users(self, admin_users: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.admin_users = admin_users

    @property
    def admin_groups(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.admin_groups

    @admin_groups.setter
    def admin_groups(self, admin_groups: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.admin_groups = admin_groups

    @property
    def viewer_users(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.viewer_users

    @viewer_users.setter
    def viewer_users(self, viewer_users: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.viewer_users = viewer_users

    @property
    def viewer_groups(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.viewer_groups

    @viewer_groups.setter
    def viewer_groups(self, viewer_groups: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.viewer_groups = viewer_groups

    @property
    def connector_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.connector_name

    @connector_name.setter
    def connector_name(self, connector_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connector_name = connector_name

    @property
    def connection_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.connection_name

    @connection_name.setter
    def connection_name(self, connection_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connection_name = connection_name

    @property
    def connection_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.connection_qualified_name
        )

    @connection_qualified_name.setter
    def connection_qualified_name(self, connection_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connection_qualified_name = connection_qualified_name

    @property
    def has_lineage(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.has_lineage

    @has_lineage.setter
    def has_lineage(self, has_lineage: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.has_lineage = has_lineage

    @property
    def is_discoverable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_discoverable

    @is_discoverable.setter
    def is_discoverable(self, is_discoverable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_discoverable = is_discoverable

    @property
    def is_editable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_editable

    @is_editable.setter
    def is_editable(self, is_editable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_editable = is_editable

    @property
    def sub_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sub_type

    @sub_type.setter
    def sub_type(self, sub_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sub_type = sub_type

    @property
    def view_score(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.view_score

    @view_score.setter
    def view_score(self, view_score: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_score = view_score

    @property
    def popularity_score(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.popularity_score

    @popularity_score.setter
    def popularity_score(self, popularity_score: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.popularity_score = popularity_score

    @property
    def source_owners(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_owners

    @source_owners.setter
    def source_owners(self, source_owners: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_owners = source_owners

    @property
    def source_created_by(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_created_by

    @source_created_by.setter
    def source_created_by(self, source_created_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_created_by = source_created_by

    @property
    def source_created_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.source_created_at

    @source_created_at.setter
    def source_created_at(self, source_created_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_created_at = source_created_at

    @property
    def source_updated_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.source_updated_at

    @source_updated_at.setter
    def source_updated_at(self, source_updated_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_updated_at = source_updated_at

    @property
    def source_updated_by(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_updated_by

    @source_updated_by.setter
    def source_updated_by(self, source_updated_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_updated_by = source_updated_by

    @property
    def source_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_url

    @source_url.setter
    def source_url(self, source_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_url = source_url

    @property
    def source_embed_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_embed_url

    @source_embed_url.setter
    def source_embed_url(self, source_embed_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_embed_url = source_embed_url

    @property
    def last_sync_workflow_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.last_sync_workflow_name
        )

    @last_sync_workflow_name.setter
    def last_sync_workflow_name(self, last_sync_workflow_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_sync_workflow_name = last_sync_workflow_name

    @property
    def last_sync_run_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.last_sync_run_at

    @last_sync_run_at.setter
    def last_sync_run_at(self, last_sync_run_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_sync_run_at = last_sync_run_at

    @property
    def last_sync_run(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.last_sync_run

    @last_sync_run.setter
    def last_sync_run(self, last_sync_run: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_sync_run = last_sync_run

    @property
    def admin_roles(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.admin_roles

    @admin_roles.setter
    def admin_roles(self, admin_roles: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.admin_roles = admin_roles

    @property
    def source_read_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_read_count

    @source_read_count.setter
    def source_read_count(self, source_read_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_count = source_read_count

    @property
    def source_read_user_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.source_read_user_count
        )

    @source_read_user_count.setter
    def source_read_user_count(self, source_read_user_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_user_count = source_read_user_count

    @property
    def source_last_read_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.source_last_read_at

    @source_last_read_at.setter
    def source_last_read_at(self, source_last_read_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_last_read_at = source_last_read_at

    @property
    def last_row_changed_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.last_row_changed_at

    @last_row_changed_at.setter
    def last_row_changed_at(self, last_row_changed_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_row_changed_at = last_row_changed_at

    @property
    def source_total_cost(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.source_total_cost

    @source_total_cost.setter
    def source_total_cost(self, source_total_cost: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_total_cost = source_total_cost

    @property
    def source_cost_unit(self) -> Optional[SourceCostUnitType]:
        return None if self.attributes is None else self.attributes.source_cost_unit

    @source_cost_unit.setter
    def source_cost_unit(self, source_cost_unit: Optional[SourceCostUnitType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_cost_unit = source_cost_unit

    @property
    def source_read_query_cost(self) -> Optional[float]:
        return (
            None if self.attributes is None else self.attributes.source_read_query_cost
        )

    @source_read_query_cost.setter
    def source_read_query_cost(self, source_read_query_cost: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_query_cost = source_read_query_cost

    @property
    def source_read_recent_user_list(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_recent_user_list
        )

    @source_read_recent_user_list.setter
    def source_read_recent_user_list(
        self, source_read_recent_user_list: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_recent_user_list = source_read_recent_user_list

    @property
    def source_read_recent_user_record_list(self) -> Optional[list[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_recent_user_record_list
        )

    @source_read_recent_user_record_list.setter
    def source_read_recent_user_record_list(
        self, source_read_recent_user_record_list: Optional[list[PopularityInsights]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_recent_user_record_list = (
            source_read_recent_user_record_list
        )

    @property
    def source_read_top_user_list(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_top_user_list
        )

    @source_read_top_user_list.setter
    def source_read_top_user_list(self, source_read_top_user_list: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_top_user_list = source_read_top_user_list

    @property
    def source_read_top_user_record_list(self) -> Optional[list[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_top_user_record_list
        )

    @source_read_top_user_record_list.setter
    def source_read_top_user_record_list(
        self, source_read_top_user_record_list: Optional[list[PopularityInsights]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_top_user_record_list = (
            source_read_top_user_record_list
        )

    @property
    def source_read_popular_query_record_list(
        self,
    ) -> Optional[list[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_popular_query_record_list
        )

    @source_read_popular_query_record_list.setter
    def source_read_popular_query_record_list(
        self, source_read_popular_query_record_list: Optional[list[PopularityInsights]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_popular_query_record_list = (
            source_read_popular_query_record_list
        )

    @property
    def source_read_expensive_query_record_list(
        self,
    ) -> Optional[list[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_expensive_query_record_list
        )

    @source_read_expensive_query_record_list.setter
    def source_read_expensive_query_record_list(
        self,
        source_read_expensive_query_record_list: Optional[list[PopularityInsights]],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_expensive_query_record_list = (
            source_read_expensive_query_record_list
        )

    @property
    def source_read_slow_query_record_list(self) -> Optional[list[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_slow_query_record_list
        )

    @source_read_slow_query_record_list.setter
    def source_read_slow_query_record_list(
        self, source_read_slow_query_record_list: Optional[list[PopularityInsights]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_slow_query_record_list = (
            source_read_slow_query_record_list
        )

    @property
    def source_query_compute_cost_list(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_query_compute_cost_list
        )

    @source_query_compute_cost_list.setter
    def source_query_compute_cost_list(
        self, source_query_compute_cost_list: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_query_compute_cost_list = source_query_compute_cost_list

    @property
    def source_query_compute_cost_record_list(
        self,
    ) -> Optional[list[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_query_compute_cost_record_list
        )

    @source_query_compute_cost_record_list.setter
    def source_query_compute_cost_record_list(
        self, source_query_compute_cost_record_list: Optional[list[PopularityInsights]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_query_compute_cost_record_list = (
            source_query_compute_cost_record_list
        )

    @property
    def dbt_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_qualified_name

    @dbt_qualified_name.setter
    def dbt_qualified_name(self, dbt_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_qualified_name = dbt_qualified_name

    @property
    def asset_dbt_alias(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.asset_dbt_alias

    @asset_dbt_alias.setter
    def asset_dbt_alias(self, asset_dbt_alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_alias = asset_dbt_alias

    @property
    def asset_dbt_meta(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.asset_dbt_meta

    @asset_dbt_meta.setter
    def asset_dbt_meta(self, asset_dbt_meta: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_meta = asset_dbt_meta

    @property
    def asset_dbt_unique_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.asset_dbt_unique_id

    @asset_dbt_unique_id.setter
    def asset_dbt_unique_id(self, asset_dbt_unique_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_unique_id = asset_dbt_unique_id

    @property
    def asset_dbt_account_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.asset_dbt_account_name
        )

    @asset_dbt_account_name.setter
    def asset_dbt_account_name(self, asset_dbt_account_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_account_name = asset_dbt_account_name

    @property
    def asset_dbt_project_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.asset_dbt_project_name
        )

    @asset_dbt_project_name.setter
    def asset_dbt_project_name(self, asset_dbt_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_project_name = asset_dbt_project_name

    @property
    def asset_dbt_package_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.asset_dbt_package_name
        )

    @asset_dbt_package_name.setter
    def asset_dbt_package_name(self, asset_dbt_package_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_package_name = asset_dbt_package_name

    @property
    def asset_dbt_job_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.asset_dbt_job_name

    @asset_dbt_job_name.setter
    def asset_dbt_job_name(self, asset_dbt_job_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_name = asset_dbt_job_name

    @property
    def asset_dbt_job_schedule(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.asset_dbt_job_schedule
        )

    @asset_dbt_job_schedule.setter
    def asset_dbt_job_schedule(self, asset_dbt_job_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_schedule = asset_dbt_job_schedule

    @property
    def asset_dbt_job_status(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.asset_dbt_job_status

    @asset_dbt_job_status.setter
    def asset_dbt_job_status(self, asset_dbt_job_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_status = asset_dbt_job_status

    @property
    def asset_dbt_test_status(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.asset_dbt_test_status
        )

    @asset_dbt_test_status.setter
    def asset_dbt_test_status(self, asset_dbt_test_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_test_status = asset_dbt_test_status

    @property
    def asset_dbt_job_schedule_cron_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_schedule_cron_humanized
        )

    @asset_dbt_job_schedule_cron_humanized.setter
    def asset_dbt_job_schedule_cron_humanized(
        self, asset_dbt_job_schedule_cron_humanized: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_schedule_cron_humanized = (
            asset_dbt_job_schedule_cron_humanized
        )

    @property
    def asset_dbt_job_last_run(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.asset_dbt_job_last_run
        )

    @asset_dbt_job_last_run.setter
    def asset_dbt_job_last_run(self, asset_dbt_job_last_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run = asset_dbt_job_last_run

    @property
    def asset_dbt_job_last_run_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_url
        )

    @asset_dbt_job_last_run_url.setter
    def asset_dbt_job_last_run_url(self, asset_dbt_job_last_run_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_url = asset_dbt_job_last_run_url

    @property
    def asset_dbt_job_last_run_created_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_created_at
        )

    @asset_dbt_job_last_run_created_at.setter
    def asset_dbt_job_last_run_created_at(
        self, asset_dbt_job_last_run_created_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_created_at = (
            asset_dbt_job_last_run_created_at
        )

    @property
    def asset_dbt_job_last_run_updated_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_updated_at
        )

    @asset_dbt_job_last_run_updated_at.setter
    def asset_dbt_job_last_run_updated_at(
        self, asset_dbt_job_last_run_updated_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_updated_at = (
            asset_dbt_job_last_run_updated_at
        )

    @property
    def asset_dbt_job_last_run_dequed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_dequed_at
        )

    @asset_dbt_job_last_run_dequed_at.setter
    def asset_dbt_job_last_run_dequed_at(
        self, asset_dbt_job_last_run_dequed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_dequed_at = (
            asset_dbt_job_last_run_dequed_at
        )

    @property
    def asset_dbt_job_last_run_started_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_started_at
        )

    @asset_dbt_job_last_run_started_at.setter
    def asset_dbt_job_last_run_started_at(
        self, asset_dbt_job_last_run_started_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_started_at = (
            asset_dbt_job_last_run_started_at
        )

    @property
    def asset_dbt_job_last_run_total_duration(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_total_duration
        )

    @asset_dbt_job_last_run_total_duration.setter
    def asset_dbt_job_last_run_total_duration(
        self, asset_dbt_job_last_run_total_duration: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_total_duration = (
            asset_dbt_job_last_run_total_duration
        )

    @property
    def asset_dbt_job_last_run_total_duration_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_total_duration_humanized
        )

    @asset_dbt_job_last_run_total_duration_humanized.setter
    def asset_dbt_job_last_run_total_duration_humanized(
        self, asset_dbt_job_last_run_total_duration_humanized: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_total_duration_humanized = (
            asset_dbt_job_last_run_total_duration_humanized
        )

    @property
    def asset_dbt_job_last_run_queued_duration(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_queued_duration
        )

    @asset_dbt_job_last_run_queued_duration.setter
    def asset_dbt_job_last_run_queued_duration(
        self, asset_dbt_job_last_run_queued_duration: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_queued_duration = (
            asset_dbt_job_last_run_queued_duration
        )

    @property
    def asset_dbt_job_last_run_queued_duration_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_queued_duration_humanized
        )

    @asset_dbt_job_last_run_queued_duration_humanized.setter
    def asset_dbt_job_last_run_queued_duration_humanized(
        self, asset_dbt_job_last_run_queued_duration_humanized: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_queued_duration_humanized = (
            asset_dbt_job_last_run_queued_duration_humanized
        )

    @property
    def asset_dbt_job_last_run_run_duration(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_run_duration
        )

    @asset_dbt_job_last_run_run_duration.setter
    def asset_dbt_job_last_run_run_duration(
        self, asset_dbt_job_last_run_run_duration: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_run_duration = (
            asset_dbt_job_last_run_run_duration
        )

    @property
    def asset_dbt_job_last_run_run_duration_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_run_duration_humanized
        )

    @asset_dbt_job_last_run_run_duration_humanized.setter
    def asset_dbt_job_last_run_run_duration_humanized(
        self, asset_dbt_job_last_run_run_duration_humanized: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_run_duration_humanized = (
            asset_dbt_job_last_run_run_duration_humanized
        )

    @property
    def asset_dbt_job_last_run_git_branch(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_git_branch
        )

    @asset_dbt_job_last_run_git_branch.setter
    def asset_dbt_job_last_run_git_branch(
        self, asset_dbt_job_last_run_git_branch: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_git_branch = (
            asset_dbt_job_last_run_git_branch
        )

    @property
    def asset_dbt_job_last_run_git_sha(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_git_sha
        )

    @asset_dbt_job_last_run_git_sha.setter
    def asset_dbt_job_last_run_git_sha(
        self, asset_dbt_job_last_run_git_sha: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_git_sha = asset_dbt_job_last_run_git_sha

    @property
    def asset_dbt_job_last_run_status_message(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_status_message
        )

    @asset_dbt_job_last_run_status_message.setter
    def asset_dbt_job_last_run_status_message(
        self, asset_dbt_job_last_run_status_message: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_status_message = (
            asset_dbt_job_last_run_status_message
        )

    @property
    def asset_dbt_job_last_run_owner_thread_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_owner_thread_id
        )

    @asset_dbt_job_last_run_owner_thread_id.setter
    def asset_dbt_job_last_run_owner_thread_id(
        self, asset_dbt_job_last_run_owner_thread_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_owner_thread_id = (
            asset_dbt_job_last_run_owner_thread_id
        )

    @property
    def asset_dbt_job_last_run_executed_by_thread_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_executed_by_thread_id
        )

    @asset_dbt_job_last_run_executed_by_thread_id.setter
    def asset_dbt_job_last_run_executed_by_thread_id(
        self, asset_dbt_job_last_run_executed_by_thread_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_executed_by_thread_id = (
            asset_dbt_job_last_run_executed_by_thread_id
        )

    @property
    def asset_dbt_job_last_run_artifacts_saved(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_artifacts_saved
        )

    @asset_dbt_job_last_run_artifacts_saved.setter
    def asset_dbt_job_last_run_artifacts_saved(
        self, asset_dbt_job_last_run_artifacts_saved: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_artifacts_saved = (
            asset_dbt_job_last_run_artifacts_saved
        )

    @property
    def asset_dbt_job_last_run_artifact_s3_path(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_artifact_s3_path
        )

    @asset_dbt_job_last_run_artifact_s3_path.setter
    def asset_dbt_job_last_run_artifact_s3_path(
        self, asset_dbt_job_last_run_artifact_s3_path: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_artifact_s3_path = (
            asset_dbt_job_last_run_artifact_s3_path
        )

    @property
    def asset_dbt_job_last_run_has_docs_generated(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_has_docs_generated
        )

    @asset_dbt_job_last_run_has_docs_generated.setter
    def asset_dbt_job_last_run_has_docs_generated(
        self, asset_dbt_job_last_run_has_docs_generated: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_has_docs_generated = (
            asset_dbt_job_last_run_has_docs_generated
        )

    @property
    def asset_dbt_job_last_run_has_sources_generated(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_has_sources_generated
        )

    @asset_dbt_job_last_run_has_sources_generated.setter
    def asset_dbt_job_last_run_has_sources_generated(
        self, asset_dbt_job_last_run_has_sources_generated: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_has_sources_generated = (
            asset_dbt_job_last_run_has_sources_generated
        )

    @property
    def asset_dbt_job_last_run_notifications_sent(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_last_run_notifications_sent
        )

    @asset_dbt_job_last_run_notifications_sent.setter
    def asset_dbt_job_last_run_notifications_sent(
        self, asset_dbt_job_last_run_notifications_sent: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_notifications_sent = (
            asset_dbt_job_last_run_notifications_sent
        )

    @property
    def asset_dbt_job_next_run(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.asset_dbt_job_next_run
        )

    @asset_dbt_job_next_run.setter
    def asset_dbt_job_next_run(self, asset_dbt_job_next_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_next_run = asset_dbt_job_next_run

    @property
    def asset_dbt_job_next_run_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_job_next_run_humanized
        )

    @asset_dbt_job_next_run_humanized.setter
    def asset_dbt_job_next_run_humanized(
        self, asset_dbt_job_next_run_humanized: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_next_run_humanized = (
            asset_dbt_job_next_run_humanized
        )

    @property
    def asset_dbt_environment_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_environment_name
        )

    @asset_dbt_environment_name.setter
    def asset_dbt_environment_name(self, asset_dbt_environment_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_environment_name = asset_dbt_environment_name

    @property
    def asset_dbt_environment_dbt_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_environment_dbt_version
        )

    @asset_dbt_environment_dbt_version.setter
    def asset_dbt_environment_dbt_version(
        self, asset_dbt_environment_dbt_version: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_environment_dbt_version = (
            asset_dbt_environment_dbt_version
        )

    @property
    def asset_dbt_tags(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.asset_dbt_tags

    @asset_dbt_tags.setter
    def asset_dbt_tags(self, asset_dbt_tags: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_tags = asset_dbt_tags

    @property
    def asset_dbt_semantic_layer_proxy_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_semantic_layer_proxy_url
        )

    @asset_dbt_semantic_layer_proxy_url.setter
    def asset_dbt_semantic_layer_proxy_url(
        self, asset_dbt_semantic_layer_proxy_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_semantic_layer_proxy_url = (
            asset_dbt_semantic_layer_proxy_url
        )

    @property
    def asset_dbt_source_freshness_criteria(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_source_freshness_criteria
        )

    @asset_dbt_source_freshness_criteria.setter
    def asset_dbt_source_freshness_criteria(
        self, asset_dbt_source_freshness_criteria: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_source_freshness_criteria = (
            asset_dbt_source_freshness_criteria
        )

    @property
    def sample_data_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sample_data_url

    @sample_data_url.setter
    def sample_data_url(self, sample_data_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sample_data_url = sample_data_url

    @property
    def asset_tags(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.asset_tags

    @asset_tags.setter
    def asset_tags(self, asset_tags: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_tags = asset_tags

    @property
    def asset_mc_incident_names(self) -> Optional[set[str]]:
        return (
            None if self.attributes is None else self.attributes.asset_mc_incident_names
        )

    @asset_mc_incident_names.setter
    def asset_mc_incident_names(self, asset_mc_incident_names: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_incident_names = asset_mc_incident_names

    @property
    def asset_mc_incident_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_incident_qualified_names
        )

    @asset_mc_incident_qualified_names.setter
    def asset_mc_incident_qualified_names(
        self, asset_mc_incident_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_incident_qualified_names = (
            asset_mc_incident_qualified_names
        )

    @property
    def asset_mc_monitor_names(self) -> Optional[set[str]]:
        return (
            None if self.attributes is None else self.attributes.asset_mc_monitor_names
        )

    @asset_mc_monitor_names.setter
    def asset_mc_monitor_names(self, asset_mc_monitor_names: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_monitor_names = asset_mc_monitor_names

    @property
    def asset_mc_monitor_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_monitor_qualified_names
        )

    @asset_mc_monitor_qualified_names.setter
    def asset_mc_monitor_qualified_names(
        self, asset_mc_monitor_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_monitor_qualified_names = (
            asset_mc_monitor_qualified_names
        )

    @property
    def asset_mc_monitor_statuses(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_monitor_statuses
        )

    @asset_mc_monitor_statuses.setter
    def asset_mc_monitor_statuses(self, asset_mc_monitor_statuses: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_monitor_statuses = asset_mc_monitor_statuses

    @property
    def asset_mc_monitor_types(self) -> Optional[set[str]]:
        return (
            None if self.attributes is None else self.attributes.asset_mc_monitor_types
        )

    @asset_mc_monitor_types.setter
    def asset_mc_monitor_types(self, asset_mc_monitor_types: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_monitor_types = asset_mc_monitor_types

    @property
    def asset_mc_monitor_schedule_types(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_monitor_schedule_types
        )

    @asset_mc_monitor_schedule_types.setter
    def asset_mc_monitor_schedule_types(
        self, asset_mc_monitor_schedule_types: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_monitor_schedule_types = (
            asset_mc_monitor_schedule_types
        )

    @property
    def asset_mc_incident_types(self) -> Optional[set[str]]:
        return (
            None if self.attributes is None else self.attributes.asset_mc_incident_types
        )

    @asset_mc_incident_types.setter
    def asset_mc_incident_types(self, asset_mc_incident_types: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_incident_types = asset_mc_incident_types

    @property
    def asset_mc_incident_sub_types(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_incident_sub_types
        )

    @asset_mc_incident_sub_types.setter
    def asset_mc_incident_sub_types(
        self, asset_mc_incident_sub_types: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_incident_sub_types = asset_mc_incident_sub_types

    @property
    def asset_mc_incident_severities(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_incident_severities
        )

    @asset_mc_incident_severities.setter
    def asset_mc_incident_severities(
        self, asset_mc_incident_severities: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_incident_severities = asset_mc_incident_severities

    @property
    def asset_mc_incident_states(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_incident_states
        )

    @asset_mc_incident_states.setter
    def asset_mc_incident_states(self, asset_mc_incident_states: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_incident_states = asset_mc_incident_states

    @property
    def asset_mc_last_sync_run_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_last_sync_run_at
        )

    @asset_mc_last_sync_run_at.setter
    def asset_mc_last_sync_run_at(self, asset_mc_last_sync_run_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_last_sync_run_at = asset_mc_last_sync_run_at

    @property
    def starred_by(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.starred_by

    @starred_by.setter
    def starred_by(self, starred_by: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.starred_by = starred_by

    @property
    def starred_details_list(self) -> Optional[list[StarredDetails]]:
        return None if self.attributes is None else self.attributes.starred_details_list

    @starred_details_list.setter
    def starred_details_list(
        self, starred_details_list: Optional[list[StarredDetails]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.starred_details_list = starred_details_list

    @property
    def starred_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.starred_count

    @starred_count.setter
    def starred_count(self, starred_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.starred_count = starred_count

    @property
    def asset_soda_d_q_status(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.asset_soda_d_q_status
        )

    @asset_soda_d_q_status.setter
    def asset_soda_d_q_status(self, asset_soda_d_q_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_soda_d_q_status = asset_soda_d_q_status

    @property
    def asset_soda_check_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.asset_soda_check_count
        )

    @asset_soda_check_count.setter
    def asset_soda_check_count(self, asset_soda_check_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_soda_check_count = asset_soda_check_count

    @property
    def asset_soda_last_sync_run_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_soda_last_sync_run_at
        )

    @asset_soda_last_sync_run_at.setter
    def asset_soda_last_sync_run_at(
        self, asset_soda_last_sync_run_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_soda_last_sync_run_at = asset_soda_last_sync_run_at

    @property
    def asset_soda_last_scan_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.asset_soda_last_scan_at
        )

    @asset_soda_last_scan_at.setter
    def asset_soda_last_scan_at(self, asset_soda_last_scan_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_soda_last_scan_at = asset_soda_last_scan_at

    @property
    def asset_soda_check_statuses(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_soda_check_statuses
        )

    @asset_soda_check_statuses.setter
    def asset_soda_check_statuses(self, asset_soda_check_statuses: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_soda_check_statuses = asset_soda_check_statuses

    @property
    def asset_soda_source_url(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.asset_soda_source_url
        )

    @asset_soda_source_url.setter
    def asset_soda_source_url(self, asset_soda_source_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_soda_source_url = asset_soda_source_url

    @property
    def asset_icon(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.asset_icon

    @asset_icon.setter
    def asset_icon(self, asset_icon: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_icon = asset_icon

    @property
    def is_partial(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_partial

    @is_partial.setter
    def is_partial(self, is_partial: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_partial = is_partial

    @property
    def is_a_i_generated(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_a_i_generated

    @is_a_i_generated.setter
    def is_a_i_generated(self, is_a_i_generated: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_a_i_generated = is_a_i_generated

    @property
    def asset_cover_image(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.asset_cover_image

    @asset_cover_image.setter
    def asset_cover_image(self, asset_cover_image: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_cover_image = asset_cover_image

    @property
    def asset_theme_hex(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.asset_theme_hex

    @asset_theme_hex.setter
    def asset_theme_hex(self, asset_theme_hex: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_theme_hex = asset_theme_hex

    @property
    def schema_registry_subjects(self) -> Optional[list[SchemaRegistrySubject]]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subjects
        )

    @schema_registry_subjects.setter
    def schema_registry_subjects(
        self, schema_registry_subjects: Optional[list[SchemaRegistrySubject]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subjects = schema_registry_subjects

    @property
    def mc_monitors(self) -> Optional[list[MCMonitor]]:
        return None if self.attributes is None else self.attributes.mc_monitors

    @mc_monitors.setter
    def mc_monitors(self, mc_monitors: Optional[list[MCMonitor]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitors = mc_monitors

    @property
    def output_port_data_products(self) -> Optional[list[DataProduct]]:
        return (
            None
            if self.attributes is None
            else self.attributes.output_port_data_products
        )

    @output_port_data_products.setter
    def output_port_data_products(
        self, output_port_data_products: Optional[list[DataProduct]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_port_data_products = output_port_data_products

    @property
    def files(self) -> Optional[list[File]]:
        return None if self.attributes is None else self.attributes.files

    @files.setter
    def files(self, files: Optional[list[File]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.files = files

    @property
    def mc_incidents(self) -> Optional[list[MCIncident]]:
        return None if self.attributes is None else self.attributes.mc_incidents

    @mc_incidents.setter
    def mc_incidents(self, mc_incidents: Optional[list[MCIncident]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incidents = mc_incidents

    @property
    def links(self) -> Optional[list[Link]]:
        return None if self.attributes is None else self.attributes.links

    @links.setter
    def links(self, links: Optional[list[Link]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.links = links

    @property
    def metrics(self) -> Optional[list[Metric]]:
        return None if self.attributes is None else self.attributes.metrics

    @metrics.setter
    def metrics(self, metrics: Optional[list[Metric]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metrics = metrics

    @property
    def readme(self) -> Optional[Readme]:
        return None if self.attributes is None else self.attributes.readme

    @readme.setter
    def readme(self, readme: Optional[Readme]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.readme = readme

    @property
    def soda_checks(self) -> Optional[list[SodaCheck]]:
        return None if self.attributes is None else self.attributes.soda_checks

    @soda_checks.setter
    def soda_checks(self, soda_checks: Optional[list[SodaCheck]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.soda_checks = soda_checks

    @property
    def assigned_terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.meanings

    @assigned_terms.setter
    def assigned_terms(self, assigned_terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = assigned_terms

    class Attributes(Referenceable.Attributes):
        name: Optional[str] = Field(default=None, description="")
        display_name: Optional[str] = Field(default=None, description="")
        description: Optional[str] = Field(default=None, description="")
        user_description: Optional[str] = Field(default=None, description="")
        tenant_id: Optional[str] = Field(default=None, description="")
        certificate_status: Optional[CertificateStatus] = Field(
            default=None, description=""
        )
        certificate_status_message: Optional[str] = Field(default=None, description="")
        certificate_updated_by: Optional[str] = Field(default=None, description="")
        certificate_updated_at: Optional[datetime] = Field(default=None, description="")
        announcement_title: Optional[str] = Field(default=None, description="")
        announcement_message: Optional[str] = Field(default=None, description="")
        announcement_type: Optional[str] = Field(default=None, description="")
        announcement_updated_at: Optional[datetime] = Field(
            default=None, description=""
        )
        announcement_updated_by: Optional[str] = Field(default=None, description="")
        owner_users: Optional[set[str]] = Field(default=None, description="")
        owner_groups: Optional[set[str]] = Field(default=None, description="")
        admin_users: Optional[set[str]] = Field(default=None, description="")
        admin_groups: Optional[set[str]] = Field(default=None, description="")
        viewer_users: Optional[set[str]] = Field(default=None, description="")
        viewer_groups: Optional[set[str]] = Field(default=None, description="")
        connector_name: Optional[str] = Field(default=None, description="")
        connection_name: Optional[str] = Field(default=None, description="")
        connection_qualified_name: Optional[str] = Field(default=None, description="")
        has_lineage: Optional[bool] = Field(default=None, description="")
        is_discoverable: Optional[bool] = Field(default=None, description="")
        is_editable: Optional[bool] = Field(default=None, description="")
        sub_type: Optional[str] = Field(default=None, description="")
        view_score: Optional[float] = Field(default=None, description="")
        popularity_score: Optional[float] = Field(default=None, description="")
        source_owners: Optional[str] = Field(default=None, description="")
        source_created_by: Optional[str] = Field(default=None, description="")
        source_created_at: Optional[datetime] = Field(default=None, description="")
        source_updated_at: Optional[datetime] = Field(default=None, description="")
        source_updated_by: Optional[str] = Field(default=None, description="")
        source_url: Optional[str] = Field(default=None, description="")
        source_embed_url: Optional[str] = Field(default=None, description="")
        last_sync_workflow_name: Optional[str] = Field(default=None, description="")
        last_sync_run_at: Optional[datetime] = Field(default=None, description="")
        last_sync_run: Optional[str] = Field(default=None, description="")
        admin_roles: Optional[set[str]] = Field(default=None, description="")
        source_read_count: Optional[int] = Field(default=None, description="")
        source_read_user_count: Optional[int] = Field(default=None, description="")
        source_last_read_at: Optional[datetime] = Field(default=None, description="")
        last_row_changed_at: Optional[datetime] = Field(default=None, description="")
        source_total_cost: Optional[float] = Field(default=None, description="")
        source_cost_unit: Optional[SourceCostUnitType] = Field(
            default=None, description=""
        )
        source_read_query_cost: Optional[float] = Field(default=None, description="")
        source_read_recent_user_list: Optional[set[str]] = Field(
            default=None, description=""
        )
        source_read_recent_user_record_list: Optional[list[PopularityInsights]] = Field(
            default=None, description=""
        )
        source_read_top_user_list: Optional[set[str]] = Field(
            default=None, description=""
        )
        source_read_top_user_record_list: Optional[list[PopularityInsights]] = Field(
            default=None, description=""
        )
        source_read_popular_query_record_list: Optional[
            list[PopularityInsights]
        ] = Field(default=None, description="")
        source_read_expensive_query_record_list: Optional[
            list[PopularityInsights]
        ] = Field(default=None, description="")
        source_read_slow_query_record_list: Optional[list[PopularityInsights]] = Field(
            default=None, description=""
        )
        source_query_compute_cost_list: Optional[set[str]] = Field(
            default=None, description=""
        )
        source_query_compute_cost_record_list: Optional[
            list[PopularityInsights]
        ] = Field(default=None, description="")
        dbt_qualified_name: Optional[str] = Field(default=None, description="")
        asset_dbt_alias: Optional[str] = Field(default=None, description="")
        asset_dbt_meta: Optional[str] = Field(default=None, description="")
        asset_dbt_unique_id: Optional[str] = Field(default=None, description="")
        asset_dbt_account_name: Optional[str] = Field(default=None, description="")
        asset_dbt_project_name: Optional[str] = Field(default=None, description="")
        asset_dbt_package_name: Optional[str] = Field(default=None, description="")
        asset_dbt_job_name: Optional[str] = Field(default=None, description="")
        asset_dbt_job_schedule: Optional[str] = Field(default=None, description="")
        asset_dbt_job_status: Optional[str] = Field(default=None, description="")
        asset_dbt_test_status: Optional[str] = Field(default=None, description="")
        asset_dbt_job_schedule_cron_humanized: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run: Optional[datetime] = Field(default=None, description="")
        asset_dbt_job_last_run_url: Optional[str] = Field(default=None, description="")
        asset_dbt_job_last_run_created_at: Optional[datetime] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_updated_at: Optional[datetime] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_dequed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_started_at: Optional[datetime] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_total_duration: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_total_duration_humanized: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_queued_duration: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_queued_duration_humanized: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_run_duration: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_run_duration_humanized: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_git_branch: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_git_sha: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_status_message: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_owner_thread_id: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_executed_by_thread_id: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_artifacts_saved: Optional[bool] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_artifact_s3_path: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_has_docs_generated: Optional[bool] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_has_sources_generated: Optional[bool] = Field(
            default=None, description=""
        )
        asset_dbt_job_last_run_notifications_sent: Optional[bool] = Field(
            default=None, description=""
        )
        asset_dbt_job_next_run: Optional[datetime] = Field(default=None, description="")
        asset_dbt_job_next_run_humanized: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_environment_name: Optional[str] = Field(default=None, description="")
        asset_dbt_environment_dbt_version: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_tags: Optional[set[str]] = Field(default=None, description="")
        asset_dbt_semantic_layer_proxy_url: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_source_freshness_criteria: Optional[str] = Field(
            default=None, description=""
        )
        sample_data_url: Optional[str] = Field(default=None, description="")
        asset_tags: Optional[set[str]] = Field(default=None, description="")
        asset_mc_incident_names: Optional[set[str]] = Field(
            default=None, description=""
        )
        asset_mc_incident_qualified_names: Optional[set[str]] = Field(
            default=None, description=""
        )
        asset_mc_monitor_names: Optional[set[str]] = Field(default=None, description="")
        asset_mc_monitor_qualified_names: Optional[set[str]] = Field(
            default=None, description=""
        )
        asset_mc_monitor_statuses: Optional[set[str]] = Field(
            default=None, description=""
        )
        asset_mc_monitor_types: Optional[set[str]] = Field(default=None, description="")
        asset_mc_monitor_schedule_types: Optional[set[str]] = Field(
            default=None, description=""
        )
        asset_mc_incident_types: Optional[set[str]] = Field(
            default=None, description=""
        )
        asset_mc_incident_sub_types: Optional[set[str]] = Field(
            default=None, description=""
        )
        asset_mc_incident_severities: Optional[set[str]] = Field(
            default=None, description=""
        )
        asset_mc_incident_states: Optional[set[str]] = Field(
            default=None, description=""
        )
        asset_mc_last_sync_run_at: Optional[datetime] = Field(
            default=None, description=""
        )
        starred_by: Optional[set[str]] = Field(default=None, description="")
        starred_details_list: Optional[list[StarredDetails]] = Field(
            default=None, description=""
        )
        starred_count: Optional[int] = Field(default=None, description="")
        asset_soda_d_q_status: Optional[str] = Field(default=None, description="")
        asset_soda_check_count: Optional[int] = Field(default=None, description="")
        asset_soda_last_sync_run_at: Optional[datetime] = Field(
            default=None, description=""
        )
        asset_soda_last_scan_at: Optional[datetime] = Field(
            default=None, description=""
        )
        asset_soda_check_statuses: Optional[str] = Field(default=None, description="")
        asset_soda_source_url: Optional[str] = Field(default=None, description="")
        asset_icon: Optional[str] = Field(default=None, description="")
        is_partial: Optional[bool] = Field(default=None, description="")
        is_a_i_generated: Optional[bool] = Field(default=None, description="")
        asset_cover_image: Optional[str] = Field(default=None, description="")
        asset_theme_hex: Optional[str] = Field(default=None, description="")
        schema_registry_subjects: Optional[list[SchemaRegistrySubject]] = Field(
            default=None, description=""
        )  # relationship
        mc_monitors: Optional[list[MCMonitor]] = Field(
            default=None, description=""
        )  # relationship
        output_port_data_products: Optional[list[DataProduct]] = Field(
            default=None, description=""
        )  # relationship
        files: Optional[list[File]] = Field(
            default=None, description=""
        )  # relationship
        mc_incidents: Optional[list[MCIncident]] = Field(
            default=None, description=""
        )  # relationship
        links: Optional[list[Link]] = Field(
            default=None, description=""
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            default=None, description=""
        )  # relationship
        readme: Optional[Readme] = Field(default=None, description="")  # relationship
        soda_checks: Optional[list[SodaCheck]] = Field(
            default=None, description=""
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship

        def remove_description(self):
            self.description = None

        def remove_user_description(self):
            self.user_description = None

        def remove_owners(self):
            self.owner_groups = None
            self.owner_users = None

        def remove_certificate(self):
            self.certificate_status = None
            self.certificate_status_message = None

        def remove_announcement(self):
            self.announcement_message = None
            self.announcement_title = None
            self.announcement_type = None

    attributes: "Asset.Attributes" = Field(
        default_factory=lambda: Asset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AtlasGlossaryCategory(Asset, type_name="AtlasGlossaryCategory"):
    """Description"""

    @classmethod
    def can_be_archived(self) -> bool:
        """
        Indicates if an asset can be archived via the asset.delete_by_guid method.
        :returns: True if archiving is supported
        """
        return False

    @root_validator()
    def _set_qualified_name_fallback(cls, values):
        if (
            "attributes" in values
            and values["attributes"]
            and not values["attributes"].qualified_name
        ):
            values["attributes"].qualified_name = values["guid"]
        return values

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(
        cls,
        *,
        name: StrictStr,
        anchor: AtlasGlossary,
        parent_category: Optional[AtlasGlossaryCategory] = None,
    ) -> AtlasGlossaryCategory:
        validate_required_fields(["name", "anchor"], [name, anchor])
        return cls(
            attributes=AtlasGlossaryCategory.Attributes.create(
                name=name, anchor=anchor, parent_category=parent_category
            )
        )

    def trim_to_required(self) -> AtlasGlossaryCategory:
        if self.anchor is None or not self.anchor.guid:
            raise ValueError("anchor.guid must be available")
        return self.create_for_modification(
            qualified_name=self.qualified_name or "",
            name=self.name or "",
            glossary_guid=self.anchor.guid,
        )

    @classmethod
    def create_for_modification(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = "",
        glossary_guid: str = "",
    ) -> SelfAsset:
        validate_required_fields(
            ["name", "qualified_name", "glossary_guid"],
            [name, qualified_name, glossary_guid],
        )
        glossary = AtlasGlossary()
        glossary.guid = glossary_guid
        return cls(
            attributes=cls.Attributes(
                qualified_name=qualified_name, name=name, anchor=glossary
            )
        )

    ANCHOR: ClassVar[KeywordField] = KeywordField("anchor", "__glossary")
    """Glossary in which the category is contained, searchable by the qualifiedName of the glossary."""

    PARENT_CATEGORY: ClassVar[KeywordField] = KeywordField(
        "parentCategory", "__parentCategory"
    )
    """Parent category in which a subcategory is contained, searchable by the qualifiedName of the category."""

    type_name: str = Field(default="AtlasGlossaryCategory", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlasGlossaryCategory":
            raise ValueError("must be AtlasGlossaryCategory")
        return v

    def __setattr__(self, name, value):
        if name in AtlasGlossaryCategory._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SHORT_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "shortDescription", "shortDescription"
    )
    """
    Unused. Brief summary of the category. See 'description' and 'userDescription' instead.
    """
    LONG_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "longDescription", "longDescription"
    )
    """
    Unused. Detailed description of the category. See 'readme' instead.
    """
    ADDITIONAL_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "additionalAttributes", "additionalAttributes"
    )
    """
    Unused. Arbitrary set of additional attributes associated with the category.
    """
    CATEGORY_TYPE: ClassVar[KeywordField] = KeywordField("categoryType", "categoryType")
    """
    TBC
    """

    TERMS: ClassVar[RelationField] = RelationField("terms")
    """
    TBC
    """
    CHILDREN_CATEGORIES: ClassVar[RelationField] = RelationField("childrenCategories")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "short_description",
        "long_description",
        "additional_attributes",
        "category_type",
        "terms",
        "anchor",
        "parent_category",
        "children_categories",
    ]

    @property
    def short_description(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.short_description

    @short_description.setter
    def short_description(self, short_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.short_description = short_description

    @property
    def long_description(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.long_description

    @long_description.setter
    def long_description(self, long_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.long_description = long_description

    @property
    def additional_attributes(self) -> Optional[dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.additional_attributes
        )

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.additional_attributes = additional_attributes

    @property
    def category_type(self) -> Optional[AtlasGlossaryCategoryType]:
        return None if self.attributes is None else self.attributes.category_type

    @category_type.setter
    def category_type(self, category_type: Optional[AtlasGlossaryCategoryType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.category_type = category_type

    @property
    def terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.terms

    @terms.setter
    def terms(self, terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.terms = terms

    @property
    def anchor(self) -> Optional[AtlasGlossary]:
        return None if self.attributes is None else self.attributes.anchor

    @anchor.setter
    def anchor(self, anchor: Optional[AtlasGlossary]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anchor = anchor

    @property
    def parent_category(self) -> Optional[AtlasGlossaryCategory]:
        return None if self.attributes is None else self.attributes.parent_category

    @parent_category.setter
    def parent_category(self, parent_category: Optional[AtlasGlossaryCategory]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_category = parent_category

    @property
    def children_categories(self) -> Optional[list[AtlasGlossaryCategory]]:
        return None if self.attributes is None else self.attributes.children_categories

    @children_categories.setter
    def children_categories(
        self, children_categories: Optional[list[AtlasGlossaryCategory]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.children_categories = children_categories

    class Attributes(Asset.Attributes):
        short_description: Optional[str] = Field(default=None, description="")
        long_description: Optional[str] = Field(default=None, description="")
        additional_attributes: Optional[dict[str, str]] = Field(
            default=None, description=""
        )
        category_type: Optional[AtlasGlossaryCategoryType] = Field(
            default=None, description=""
        )
        terms: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        anchor: Optional[AtlasGlossary] = Field(
            default=None, description=""
        )  # relationship
        parent_category: Optional[AtlasGlossaryCategory] = Field(
            default=None, description=""
        )  # relationship
        children_categories: Optional[list[AtlasGlossaryCategory]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls,
            *,
            name: StrictStr,
            anchor: AtlasGlossary,
            parent_category: Optional[AtlasGlossaryCategory] = None,
        ) -> AtlasGlossaryCategory.Attributes:
            validate_required_fields(["name", "anchor"], [name, anchor])
            return AtlasGlossaryCategory.Attributes(
                name=name,
                anchor=anchor,
                parent_category=parent_category,
                qualified_name=next_id(),
            )

    attributes: "AtlasGlossaryCategory.Attributes" = Field(
        default_factory=lambda: AtlasGlossaryCategory.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AtlasGlossary(Asset, type_name="AtlasGlossary"):
    """Description"""

    @root_validator()
    def _set_qualified_name_fallback(cls, values):
        if (
            "attributes" in values
            and values["attributes"]
            and not values["attributes"].qualified_name
        ):
            values["attributes"].qualified_name = values["guid"]
        return values

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(
        cls, *, name: StrictStr, icon: Optional[AtlanIcon] = None
    ) -> AtlasGlossary:
        validate_required_fields(["name"], [name])
        return AtlasGlossary(
            attributes=AtlasGlossary.Attributes.create(name=name, icon=icon)
        )

    type_name: str = Field(default="AtlasGlossary", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlasGlossary":
            raise ValueError("must be AtlasGlossary")
        return v

    def __setattr__(self, name, value):
        if name in AtlasGlossary._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SHORT_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "shortDescription", "shortDescription"
    )
    """
    Unused. A short definition of the glossary. See 'description' and 'userDescription' instead.
    """
    LONG_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "longDescription", "longDescription"
    )
    """
    Unused. A longer description of the glossary. See 'readme' instead.
    """
    LANGUAGE: ClassVar[KeywordField] = KeywordField("language", "language")
    """
    Unused. Language of the glossary's contents.
    """
    USAGE: ClassVar[KeywordField] = KeywordField("usage", "usage")
    """
    Unused. Inteded usage for the glossary.
    """
    ADDITIONAL_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "additionalAttributes", "additionalAttributes"
    )
    """
    Unused. Arbitrary set of additional attributes associated with this glossary.
    """
    GLOSSARY_TYPE: ClassVar[KeywordField] = KeywordField("glossaryType", "glossaryType")
    """
    TBC
    """

    TERMS: ClassVar[RelationField] = RelationField("terms")
    """
    TBC
    """
    CATEGORIES: ClassVar[RelationField] = RelationField("categories")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "short_description",
        "long_description",
        "language",
        "usage",
        "additional_attributes",
        "glossary_type",
        "terms",
        "categories",
    ]

    @property
    def short_description(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.short_description

    @short_description.setter
    def short_description(self, short_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.short_description = short_description

    @property
    def long_description(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.long_description

    @long_description.setter
    def long_description(self, long_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.long_description = long_description

    @property
    def language(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.language

    @language.setter
    def language(self, language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.language = language

    @property
    def usage(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.usage

    @usage.setter
    def usage(self, usage: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.usage = usage

    @property
    def additional_attributes(self) -> Optional[dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.additional_attributes
        )

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.additional_attributes = additional_attributes

    @property
    def glossary_type(self) -> Optional[AtlasGlossaryType]:
        return None if self.attributes is None else self.attributes.glossary_type

    @glossary_type.setter
    def glossary_type(self, glossary_type: Optional[AtlasGlossaryType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.glossary_type = glossary_type

    @property
    def terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.terms

    @terms.setter
    def terms(self, terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.terms = terms

    @property
    def categories(self) -> Optional[list[AtlasGlossaryCategory]]:
        return None if self.attributes is None else self.attributes.categories

    @categories.setter
    def categories(self, categories: Optional[list[AtlasGlossaryCategory]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.categories = categories

    class Attributes(Asset.Attributes):
        short_description: Optional[str] = Field(default=None, description="")
        long_description: Optional[str] = Field(default=None, description="")
        language: Optional[str] = Field(default=None, description="")
        usage: Optional[str] = Field(default=None, description="")
        additional_attributes: Optional[dict[str, str]] = Field(
            default=None, description=""
        )
        glossary_type: Optional[AtlasGlossaryType] = Field(default=None, description="")
        terms: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        categories: Optional[list[AtlasGlossaryCategory]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, *, name: StrictStr, icon: Optional[AtlanIcon] = None
        ) -> AtlasGlossary.Attributes:
            validate_required_fields(["name"], [name])
            icon_str = icon.value if icon is not None else None
            return AtlasGlossary.Attributes(
                name=name, qualified_name=next_id(), asset_icon=icon_str
            )

    attributes: "AtlasGlossary.Attributes" = Field(
        default_factory=lambda: AtlasGlossary.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AtlasGlossaryTerm(Asset, type_name="AtlasGlossaryTerm"):
    """Description"""

    @root_validator()
    def _set_qualified_name_fallback(cls, values):
        if (
            "attributes" in values
            and values["attributes"]
            and not values["attributes"].qualified_name
        ):
            values["attributes"].qualified_name = values["guid"]
        return values

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(
        cls,
        *,
        name: StrictStr,
        anchor: Optional[AtlasGlossary] = None,
        glossary_qualified_name: Optional[StrictStr] = None,
        glossary_guid: Optional[StrictStr] = None,
        categories: Optional[list[AtlasGlossaryCategory]] = None,
    ) -> AtlasGlossaryTerm:
        validate_required_fields(["name"], [name])
        return cls(
            attributes=AtlasGlossaryTerm.Attributes.create(
                name=name,
                anchor=anchor,
                glossary_qualified_name=glossary_qualified_name,
                glossary_guid=glossary_guid,
                categories=categories,
            )
        )

    def trim_to_required(self) -> AtlasGlossaryTerm:
        if self.anchor is None or not self.anchor.guid:
            raise ValueError("anchor.guid must be available")
        return self.create_for_modification(
            qualified_name=self.qualified_name or "",
            name=self.name or "",
            glossary_guid=self.anchor.guid,
        )

    @classmethod
    def create_for_modification(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = "",
        glossary_guid: str = "",
    ) -> SelfAsset:
        validate_required_fields(
            ["name", "qualified_name", "glossary_guid"],
            [name, qualified_name, glossary_guid],
        )
        glossary = AtlasGlossary()
        glossary.guid = glossary_guid
        return cls(
            attributes=cls.Attributes(
                qualified_name=qualified_name, name=name, anchor=glossary
            )
        )

    ANCHOR: ClassVar[KeywordField] = KeywordField("anchor", "__glossary")
    """Glossary in which the term is contained, searchable by the qualifiedName of the glossary."""

    CATEGORIES: ClassVar[KeywordField] = KeywordField("categories", "__categories")
    """Categories in which the term is organized, searchable by the qualifiedName of the category."""

    type_name: str = Field(default="AtlasGlossaryTerm", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlasGlossaryTerm":
            raise ValueError("must be AtlasGlossaryTerm")
        return v

    def __setattr__(self, name, value):
        if name in AtlasGlossaryTerm._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SHORT_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "shortDescription", "shortDescription"
    )
    """
    Unused. Brief summary of the term. See 'description' and 'userDescription' instead.
    """
    LONG_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "longDescription", "longDescription"
    )
    """
    Unused. Detailed definition of the term. See 'readme' instead.
    """
    EXAMPLES: ClassVar[KeywordField] = KeywordField("examples", "examples")
    """
    Unused. Exmaples of the term.
    """
    ABBREVIATION: ClassVar[KeywordField] = KeywordField("abbreviation", "abbreviation")
    """
    Unused. Abbreviation of the term.
    """
    USAGE: ClassVar[KeywordField] = KeywordField("usage", "usage")
    """
    Unused. Intended usage for the term.
    """
    ADDITIONAL_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "additionalAttributes", "additionalAttributes"
    )
    """
    Unused. Arbitrary set of additional attributes for the terrm.
    """
    TERM_TYPE: ClassVar[KeywordField] = KeywordField("termType", "termType")
    """
    TBC
    """

    VALID_VALUES_FOR: ClassVar[RelationField] = RelationField("validValuesFor")
    """
    TBC
    """
    VALID_VALUES: ClassVar[RelationField] = RelationField("validValues")
    """
    TBC
    """
    SEE_ALSO: ClassVar[RelationField] = RelationField("seeAlso")
    """
    TBC
    """
    IS_A: ClassVar[RelationField] = RelationField("isA")
    """
    TBC
    """
    ANTONYMS: ClassVar[RelationField] = RelationField("antonyms")
    """
    TBC
    """
    ASSIGNED_ENTITIES: ClassVar[RelationField] = RelationField("assignedEntities")
    """
    TBC
    """
    CLASSIFIES: ClassVar[RelationField] = RelationField("classifies")
    """
    TBC
    """
    PREFERRED_TO_TERMS: ClassVar[RelationField] = RelationField("preferredToTerms")
    """
    TBC
    """
    PREFERRED_TERMS: ClassVar[RelationField] = RelationField("preferredTerms")
    """
    TBC
    """
    TRANSLATION_TERMS: ClassVar[RelationField] = RelationField("translationTerms")
    """
    TBC
    """
    SYNONYMS: ClassVar[RelationField] = RelationField("synonyms")
    """
    TBC
    """
    REPLACED_BY: ClassVar[RelationField] = RelationField("replacedBy")
    """
    TBC
    """
    REPLACEMENT_TERMS: ClassVar[RelationField] = RelationField("replacementTerms")
    """
    TBC
    """
    TRANSLATED_TERMS: ClassVar[RelationField] = RelationField("translatedTerms")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "short_description",
        "long_description",
        "examples",
        "abbreviation",
        "usage",
        "additional_attributes",
        "term_type",
        "valid_values_for",
        "valid_values",
        "see_also",
        "is_a",
        "antonyms",
        "assigned_entities",
        "classifies",
        "categories",
        "preferred_to_terms",
        "preferred_terms",
        "translation_terms",
        "synonyms",
        "replaced_by",
        "replacement_terms",
        "translated_terms",
        "anchor",
    ]

    @property
    def short_description(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.short_description

    @short_description.setter
    def short_description(self, short_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.short_description = short_description

    @property
    def long_description(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.long_description

    @long_description.setter
    def long_description(self, long_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.long_description = long_description

    @property
    def examples(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.examples

    @examples.setter
    def examples(self, examples: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.examples = examples

    @property
    def abbreviation(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.abbreviation

    @abbreviation.setter
    def abbreviation(self, abbreviation: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.abbreviation = abbreviation

    @property
    def usage(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.usage

    @usage.setter
    def usage(self, usage: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.usage = usage

    @property
    def additional_attributes(self) -> Optional[dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.additional_attributes
        )

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.additional_attributes = additional_attributes

    @property
    def term_type(self) -> Optional[AtlasGlossaryTermType]:
        return None if self.attributes is None else self.attributes.term_type

    @term_type.setter
    def term_type(self, term_type: Optional[AtlasGlossaryTermType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.term_type = term_type

    @property
    def valid_values_for(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.valid_values_for

    @valid_values_for.setter
    def valid_values_for(self, valid_values_for: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.valid_values_for = valid_values_for

    @property
    def valid_values(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.valid_values

    @valid_values.setter
    def valid_values(self, valid_values: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.valid_values = valid_values

    @property
    def see_also(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.see_also

    @see_also.setter
    def see_also(self, see_also: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.see_also = see_also

    @property
    def is_a(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.is_a

    @is_a.setter
    def is_a(self, is_a: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_a = is_a

    @property
    def antonyms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.antonyms

    @antonyms.setter
    def antonyms(self, antonyms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.antonyms = antonyms

    @property
    def assigned_entities(self) -> Optional[list[Referenceable]]:
        return None if self.attributes is None else self.attributes.assigned_entities

    @assigned_entities.setter
    def assigned_entities(self, assigned_entities: Optional[list[Referenceable]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.assigned_entities = assigned_entities

    @property
    def classifies(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.classifies

    @classifies.setter
    def classifies(self, classifies: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.classifies = classifies

    @property
    def categories(self) -> Optional[list[AtlasGlossaryCategory]]:
        return None if self.attributes is None else self.attributes.categories

    @categories.setter
    def categories(self, categories: Optional[list[AtlasGlossaryCategory]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.categories = categories

    @property
    def preferred_to_terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.preferred_to_terms

    @preferred_to_terms.setter
    def preferred_to_terms(self, preferred_to_terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preferred_to_terms = preferred_to_terms

    @property
    def preferred_terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.preferred_terms

    @preferred_terms.setter
    def preferred_terms(self, preferred_terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preferred_terms = preferred_terms

    @property
    def translation_terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.translation_terms

    @translation_terms.setter
    def translation_terms(self, translation_terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.translation_terms = translation_terms

    @property
    def synonyms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.synonyms

    @synonyms.setter
    def synonyms(self, synonyms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.synonyms = synonyms

    @property
    def replaced_by(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.replaced_by

    @replaced_by.setter
    def replaced_by(self, replaced_by: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.replaced_by = replaced_by

    @property
    def replacement_terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.replacement_terms

    @replacement_terms.setter
    def replacement_terms(self, replacement_terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.replacement_terms = replacement_terms

    @property
    def translated_terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.translated_terms

    @translated_terms.setter
    def translated_terms(self, translated_terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.translated_terms = translated_terms

    @property
    def anchor(self) -> Optional[AtlasGlossary]:
        return None if self.attributes is None else self.attributes.anchor

    @anchor.setter
    def anchor(self, anchor: Optional[AtlasGlossary]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anchor = anchor

    class Attributes(Asset.Attributes):
        short_description: Optional[str] = Field(default=None, description="")
        long_description: Optional[str] = Field(default=None, description="")
        examples: Optional[set[str]] = Field(default=None, description="")
        abbreviation: Optional[str] = Field(default=None, description="")
        usage: Optional[str] = Field(default=None, description="")
        additional_attributes: Optional[dict[str, str]] = Field(
            default=None, description=""
        )
        term_type: Optional[AtlasGlossaryTermType] = Field(default=None, description="")
        valid_values_for: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        valid_values: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        see_also: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        is_a: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        antonyms: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        assigned_entities: Optional[list[Referenceable]] = Field(
            default=None, description=""
        )  # relationship
        classifies: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        categories: Optional[list[AtlasGlossaryCategory]] = Field(
            default=None, description=""
        )  # relationship
        preferred_to_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        preferred_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        translation_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        synonyms: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        replaced_by: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        replacement_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        translated_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        anchor: Optional[AtlasGlossary] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls,
            *,
            name: StrictStr,
            anchor: Optional[AtlasGlossary] = None,
            glossary_qualified_name: Optional[StrictStr] = None,
            glossary_guid: Optional[StrictStr] = None,
            categories: Optional[list[AtlasGlossaryCategory]] = None,
        ) -> AtlasGlossaryTerm.Attributes:
            validate_required_fields(["name"], [name])
            validate_single_required_field(
                ["anchor", "glossary_qualified_name", "glossary_guid"],
                [anchor, glossary_qualified_name, glossary_guid],
            )
            if glossary_qualified_name:
                anchor = AtlasGlossary()
                anchor.unique_attributes = {"qualifiedName": glossary_qualified_name}
            if glossary_guid:
                anchor = AtlasGlossary()
                anchor.guid = glossary_guid
            return AtlasGlossaryTerm.Attributes(
                name=name,
                anchor=anchor,
                categories=categories,
                qualified_name=next_id(),
            )

    attributes: "AtlasGlossaryTerm.Attributes" = Field(
        default_factory=lambda: AtlasGlossaryTerm.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Process(Asset, type_name="Process"):
    """Description"""

    @classmethod
    @init_guid
    def create(
        cls,
        name: str,
        connection_qualified_name: str,
        inputs: list["Catalog"],
        outputs: list["Catalog"],
        process_id: Optional[str] = None,
        parent: Optional[Process] = None,
    ) -> Process:
        return Process(
            attributes=Process.Attributes.create(
                name=name,
                connection_qualified_name=connection_qualified_name,
                process_id=process_id,
                inputs=inputs,
                outputs=outputs,
                parent=parent,
            )
        )

    type_name: str = Field(default="Process", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Process":
            raise ValueError("must be Process")
        return v

    def __setattr__(self, name, value):
        if name in Process._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CODE: ClassVar[KeywordField] = KeywordField("code", "code")
    """
    Code that ran within the process.
    """
    SQL: ClassVar[KeywordField] = KeywordField("sql", "sql")
    """
    SQL query that ran to produce the outputs.
    """
    AST: ClassVar[KeywordField] = KeywordField("ast", "ast")
    """
    Parsed AST of the code or SQL statements that describe the logic of this process.
    """

    MATILLION_COMPONENT: ClassVar[RelationField] = RelationField("matillionComponent")
    """
    TBC
    """
    AIRFLOW_TASKS: ClassVar[RelationField] = RelationField("airflowTasks")
    """
    TBC
    """
    COLUMN_PROCESSES: ClassVar[RelationField] = RelationField("columnProcesses")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "inputs",
        "outputs",
        "code",
        "sql",
        "ast",
        "matillion_component",
        "airflow_tasks",
        "column_processes",
    ]

    @property
    def inputs(self) -> Optional[list[Catalog]]:
        return None if self.attributes is None else self.attributes.inputs

    @inputs.setter
    def inputs(self, inputs: Optional[list[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inputs = inputs

    @property
    def outputs(self) -> Optional[list[Catalog]]:
        return None if self.attributes is None else self.attributes.outputs

    @outputs.setter
    def outputs(self, outputs: Optional[list[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.outputs = outputs

    @property
    def code(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.code

    @code.setter
    def code(self, code: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.code = code

    @property
    def sql(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sql

    @sql.setter
    def sql(self, sql: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql = sql

    @property
    def ast(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ast

    @ast.setter
    def ast(self, ast: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ast = ast

    @property
    def matillion_component(self) -> Optional[MatillionComponent]:
        return None if self.attributes is None else self.attributes.matillion_component

    @matillion_component.setter
    def matillion_component(self, matillion_component: Optional[MatillionComponent]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component = matillion_component

    @property
    def airflow_tasks(self) -> Optional[list[AirflowTask]]:
        return None if self.attributes is None else self.attributes.airflow_tasks

    @airflow_tasks.setter
    def airflow_tasks(self, airflow_tasks: Optional[list[AirflowTask]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_tasks = airflow_tasks

    @property
    def column_processes(self) -> Optional[list[ColumnProcess]]:
        return None if self.attributes is None else self.attributes.column_processes

    @column_processes.setter
    def column_processes(self, column_processes: Optional[list[ColumnProcess]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_processes = column_processes

    class Attributes(Asset.Attributes):
        inputs: Optional[list[Catalog]] = Field(default=None, description="")
        outputs: Optional[list[Catalog]] = Field(default=None, description="")
        code: Optional[str] = Field(default=None, description="")
        sql: Optional[str] = Field(default=None, description="")
        ast: Optional[str] = Field(default=None, description="")
        matillion_component: Optional[MatillionComponent] = Field(
            default=None, description=""
        )  # relationship
        airflow_tasks: Optional[list[AirflowTask]] = Field(
            default=None, description=""
        )  # relationship
        column_processes: Optional[list[ColumnProcess]] = Field(
            default=None, description=""
        )  # relationship

        @staticmethod
        def generate_qualified_name(
            name: str,
            connection_qualified_name: str,
            inputs: list["Catalog"],
            outputs: list["Catalog"],
            parent: Optional["Process"] = None,
            process_id: Optional[str] = None,
        ) -> str:
            def append_relationship(output: StringIO, relationship: Asset):
                if relationship.guid:
                    output.write(relationship.guid)

            def append_relationships(output: StringIO, relationships: list["Catalog"]):
                for catalog in relationships:
                    append_relationship(output, catalog)

            validate_required_fields(
                ["name", "connection_qualified_name", "inputs", "outputs"],
                [name, connection_qualified_name, inputs, outputs],
            )
            if process_id and process_id.strip():
                return f"{connection_qualified_name}/{process_id}"
            buffer = StringIO()
            buffer.write(name)
            buffer.write(connection_qualified_name)
            if parent:
                append_relationship(buffer, parent)
            append_relationships(buffer, inputs)
            append_relationships(buffer, outputs)
            ret_value = hashlib.md5(
                buffer.getvalue().encode(), usedforsecurity=False
            ).hexdigest()
            buffer.close()
            return ret_value

        @classmethod
        @init_guid
        def create(
            cls,
            name: str,
            connection_qualified_name: str,
            inputs: list["Catalog"],
            outputs: list["Catalog"],
            process_id: Optional[str] = None,
            parent: Optional[Process] = None,
        ) -> Process.Attributes:
            qualified_name = Process.Attributes.generate_qualified_name(
                name=name,
                connection_qualified_name=connection_qualified_name,
                process_id=process_id,
                inputs=inputs,
                outputs=outputs,
                parent=parent,
            )
            connector_name = connection_qualified_name.split("/")[1]
            return Process.Attributes(
                name=name,
                qualified_name=qualified_name,
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name,
                inputs=inputs,
                outputs=outputs,
            )

    attributes: "Process.Attributes" = Field(
        default_factory=lambda: Process.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Namespace(Asset, type_name="Namespace"):
    """Description"""

    type_name: str = Field(default="Namespace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Namespace":
            raise ValueError("must be Namespace")
        return v

    def __setattr__(self, name, value):
        if name in Namespace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CHILDREN_QUERIES: ClassVar[RelationField] = RelationField("childrenQueries")
    """
    TBC
    """
    CHILDREN_FOLDERS: ClassVar[RelationField] = RelationField("childrenFolders")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "children_queries",
        "children_folders",
    ]

    @property
    def children_queries(self) -> Optional[list[Query]]:
        return None if self.attributes is None else self.attributes.children_queries

    @children_queries.setter
    def children_queries(self, children_queries: Optional[list[Query]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.children_queries = children_queries

    @property
    def children_folders(self) -> Optional[list[Folder]]:
        return None if self.attributes is None else self.attributes.children_folders

    @children_folders.setter
    def children_folders(self, children_folders: Optional[list[Folder]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.children_folders = children_folders

    class Attributes(Asset.Attributes):
        children_queries: Optional[list[Query]] = Field(
            default=None, description=""
        )  # relationship
        children_folders: Optional[list[Folder]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "Namespace.Attributes" = Field(
        default_factory=lambda: Namespace.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Folder(Namespace):
    """Description"""

    type_name: str = Field(default="Folder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Folder":
            raise ValueError("must be Folder")
        return v

    def __setattr__(self, name, value):
        if name in Folder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PARENT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "parentQualifiedName", "parentQualifiedName", "parentQualifiedName.text"
    )
    """
    Unique name of the parent folder or collection in which this folder exists.
    """
    COLLECTION_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "collectionQualifiedName",
        "collectionQualifiedName",
        "collectionQualifiedName.text",
    )
    """
    Unique name of the collection in which this folder exists.
    """

    PARENT: ClassVar[RelationField] = RelationField("parent")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "parent_qualified_name",
        "collection_qualified_name",
        "parent",
    ]

    @property
    def parent_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.parent_qualified_name
        )

    @parent_qualified_name.setter
    def parent_qualified_name(self, parent_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_qualified_name = parent_qualified_name

    @property
    def collection_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.collection_qualified_name
        )

    @collection_qualified_name.setter
    def collection_qualified_name(self, collection_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.collection_qualified_name = collection_qualified_name

    @property
    def parent(self) -> Optional[Namespace]:
        return None if self.attributes is None else self.attributes.parent

    @parent.setter
    def parent(self, parent: Optional[Namespace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent = parent

    class Attributes(Namespace.Attributes):
        parent_qualified_name: Optional[str] = Field(default=None, description="")
        collection_qualified_name: Optional[str] = Field(default=None, description="")
        parent: Optional[Namespace] = Field(
            default=None, description=""
        )  # relationship

    attributes: "Folder.Attributes" = Field(
        default_factory=lambda: Folder.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Catalog(Asset, type_name="Catalog"):
    """Description"""

    type_name: str = Field(default="Catalog", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Catalog":
            raise ValueError("must be Catalog")
        return v

    def __setattr__(self, name, value):
        if name in Catalog._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    INPUT_TO_PROCESSES: ClassVar[RelationField] = RelationField("inputToProcesses")
    """
    TBC
    """
    OUTPUT_FROM_AIRFLOW_TASKS: ClassVar[RelationField] = RelationField(
        "outputFromAirflowTasks"
    )
    """
    TBC
    """
    INPUT_TO_AIRFLOW_TASKS: ClassVar[RelationField] = RelationField(
        "inputToAirflowTasks"
    )
    """
    TBC
    """
    OUTPUT_FROM_PROCESSES: ClassVar[RelationField] = RelationField(
        "outputFromProcesses"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "input_to_processes",
        "output_from_airflow_tasks",
        "input_to_airflow_tasks",
        "output_from_processes",
    ]

    @property
    def input_to_processes(self) -> Optional[list[Process]]:
        return None if self.attributes is None else self.attributes.input_to_processes

    @input_to_processes.setter
    def input_to_processes(self, input_to_processes: Optional[list[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_processes = input_to_processes

    @property
    def output_from_airflow_tasks(self) -> Optional[list[AirflowTask]]:
        return (
            None
            if self.attributes is None
            else self.attributes.output_from_airflow_tasks
        )

    @output_from_airflow_tasks.setter
    def output_from_airflow_tasks(
        self, output_from_airflow_tasks: Optional[list[AirflowTask]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_from_airflow_tasks = output_from_airflow_tasks

    @property
    def input_to_airflow_tasks(self) -> Optional[list[AirflowTask]]:
        return (
            None if self.attributes is None else self.attributes.input_to_airflow_tasks
        )

    @input_to_airflow_tasks.setter
    def input_to_airflow_tasks(
        self, input_to_airflow_tasks: Optional[list[AirflowTask]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_airflow_tasks = input_to_airflow_tasks

    @property
    def output_from_processes(self) -> Optional[list[Process]]:
        return (
            None if self.attributes is None else self.attributes.output_from_processes
        )

    @output_from_processes.setter
    def output_from_processes(self, output_from_processes: Optional[list[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_from_processes = output_from_processes

    class Attributes(Asset.Attributes):
        input_to_processes: Optional[list[Process]] = Field(
            default=None, description=""
        )  # relationship
        output_from_airflow_tasks: Optional[list[AirflowTask]] = Field(
            default=None, description=""
        )  # relationship
        input_to_airflow_tasks: Optional[list[AirflowTask]] = Field(
            default=None, description=""
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "Catalog.Attributes" = Field(
        default_factory=lambda: Catalog.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Tag(Catalog):
    """Description"""

    type_name: str = Field(default="Tag", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Tag":
            raise ValueError("must be Tag")
        return v

    def __setattr__(self, name, value):
        if name in Tag._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    TAG_ID: ClassVar[KeywordField] = KeywordField("tagId", "tagId")
    """
    Unique identifier of the tag in the source system.
    """
    TAG_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "tagAttributes", "tagAttributes"
    )
    """
    Attributes associated with the tag in the source system.
    """
    TAG_ALLOWED_VALUES: ClassVar[KeywordTextField] = KeywordTextField(
        "tagAllowedValues", "tagAllowedValues", "tagAllowedValues.text"
    )
    """
    Allowed values for the tag in the source system. These are denormalized from tagAttributes for ease of querying.
    """
    MAPPED_CLASSIFICATION_NAME: ClassVar[KeywordField] = KeywordField(
        "mappedClassificationName", "mappedClassificationName"
    )
    """
    Name of the classification in Atlan that is mapped to this tag.
    """

    _convenience_properties: ClassVar[list[str]] = [
        "tag_id",
        "tag_attributes",
        "tag_allowed_values",
        "mapped_atlan_tag_name",
    ]

    @property
    def tag_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.tag_id

    @tag_id.setter
    def tag_id(self, tag_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tag_id = tag_id

    @property
    def tag_attributes(self) -> Optional[list[SourceTagAttribute]]:
        return None if self.attributes is None else self.attributes.tag_attributes

    @tag_attributes.setter
    def tag_attributes(self, tag_attributes: Optional[list[SourceTagAttribute]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tag_attributes = tag_attributes

    @property
    def tag_allowed_values(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.tag_allowed_values

    @tag_allowed_values.setter
    def tag_allowed_values(self, tag_allowed_values: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tag_allowed_values = tag_allowed_values

    @property
    def mapped_atlan_tag_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.mapped_atlan_tag_name
        )

    @mapped_atlan_tag_name.setter
    def mapped_atlan_tag_name(self, mapped_atlan_tag_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mapped_atlan_tag_name = mapped_atlan_tag_name

    class Attributes(Catalog.Attributes):
        tag_id: Optional[str] = Field(default=None, description="")
        tag_attributes: Optional[list[SourceTagAttribute]] = Field(
            default=None, description=""
        )
        tag_allowed_values: Optional[set[str]] = Field(default=None, description="")
        mapped_atlan_tag_name: Optional[str] = Field(default=None, description="")

    attributes: "Tag.Attributes" = Field(
        default_factory=lambda: Tag.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ColumnProcess(Process):
    """Description"""

    @classmethod
    @init_guid
    def create(
        cls,
        name: str,
        connection_qualified_name: str,
        inputs: list["Catalog"],
        outputs: list["Catalog"],
        parent: Process,
        process_id: Optional[str] = None,
    ) -> ColumnProcess:
        return ColumnProcess(
            attributes=ColumnProcess.Attributes.create(
                name=name,
                connection_qualified_name=connection_qualified_name,
                process_id=process_id,
                inputs=inputs,
                outputs=outputs,
                parent=parent,
            )
        )

    type_name: str = Field(default="ColumnProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ColumnProcess":
            raise ValueError("must be ColumnProcess")
        return v

    def __setattr__(self, name, value):
        if name in ColumnProcess._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    OUTPUTS: ClassVar[RelationField] = RelationField("outputs")
    """
    Assets that are outputs from this process.
    """
    PROCESS: ClassVar[RelationField] = RelationField("process")
    """
    TBC
    """
    INPUTS: ClassVar[RelationField] = RelationField("inputs")
    """
    Assets that are inputs to this process.
    """

    _convenience_properties: ClassVar[list[str]] = [
        "outputs",
        "process",
        "inputs",
    ]

    @property
    def outputs(self) -> Optional[list[Catalog]]:
        return None if self.attributes is None else self.attributes.outputs

    @outputs.setter
    def outputs(self, outputs: Optional[list[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.outputs = outputs

    @property
    def process(self) -> Optional[Process]:
        return None if self.attributes is None else self.attributes.process

    @process.setter
    def process(self, process: Optional[Process]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.process = process

    @property
    def inputs(self) -> Optional[list[Catalog]]:
        return None if self.attributes is None else self.attributes.inputs

    @inputs.setter
    def inputs(self, inputs: Optional[list[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inputs = inputs

    class Attributes(Process.Attributes):
        outputs: Optional[list[Catalog]] = Field(
            default=None, description=""
        )  # relationship
        process: Optional[Process] = Field(default=None, description="")  # relationship
        inputs: Optional[list[Catalog]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            name: str,
            connection_qualified_name: str,
            inputs: list["Catalog"],
            outputs: list["Catalog"],
            parent: Process,
            process_id: Optional[str] = None,
        ) -> ColumnProcess.Attributes:
            validate_required_fields(["parent"], [parent])
            qualified_name = Process.Attributes.generate_qualified_name(
                name=name,
                connection_qualified_name=connection_qualified_name,
                process_id=process_id,
                inputs=inputs,
                outputs=outputs,
                parent=parent,
            )
            connector_name = connection_qualified_name.split("/")[1]
            return ColumnProcess.Attributes(
                name=name,
                qualified_name=qualified_name,
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name,
                inputs=inputs,
                outputs=outputs,
                process=parent,
            )

    attributes: "ColumnProcess.Attributes" = Field(
        default_factory=lambda: ColumnProcess.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Airflow(Catalog):
    """Description"""

    type_name: str = Field(default="Airflow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Airflow":
            raise ValueError("must be Airflow")
        return v

    def __setattr__(self, name, value):
        if name in Airflow._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AIRFLOW_TAGS: ClassVar[KeywordField] = KeywordField("airflowTags", "airflowTags")
    """
    Tags assigned to the asset in Airflow.
    """
    AIRFLOW_RUN_VERSION: ClassVar[KeywordField] = KeywordField(
        "airflowRunVersion", "airflowRunVersion"
    )
    """
    Version of the run in Airflow.
    """
    AIRFLOW_RUN_OPEN_LINEAGE_VERSION: ClassVar[KeywordField] = KeywordField(
        "airflowRunOpenLineageVersion", "airflowRunOpenLineageVersion"
    )
    """
    Version of the run in OpenLineage.
    """
    AIRFLOW_RUN_NAME: ClassVar[KeywordField] = KeywordField(
        "airflowRunName", "airflowRunName"
    )
    """
    Name of the run.
    """
    AIRFLOW_RUN_TYPE: ClassVar[KeywordField] = KeywordField(
        "airflowRunType", "airflowRunType"
    )
    """
    Type of the run.
    """
    AIRFLOW_RUN_START_TIME: ClassVar[NumericField] = NumericField(
        "airflowRunStartTime", "airflowRunStartTime"
    )
    """
    Start time of the run.
    """
    AIRFLOW_RUN_END_TIME: ClassVar[NumericField] = NumericField(
        "airflowRunEndTime", "airflowRunEndTime"
    )
    """
    End time of the run.
    """
    AIRFLOW_RUN_OPEN_LINEAGE_STATE: ClassVar[KeywordField] = KeywordField(
        "airflowRunOpenLineageState", "airflowRunOpenLineageState"
    )
    """
    State of the run in OpenLineage.
    """

    _convenience_properties: ClassVar[list[str]] = [
        "airflow_tags",
        "airflow_run_version",
        "airflow_run_open_lineage_version",
        "airflow_run_name",
        "airflow_run_type",
        "airflow_run_start_time",
        "airflow_run_end_time",
        "airflow_run_open_lineage_state",
    ]

    @property
    def airflow_tags(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.airflow_tags

    @airflow_tags.setter
    def airflow_tags(self, airflow_tags: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_tags = airflow_tags

    @property
    def airflow_run_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.airflow_run_version

    @airflow_run_version.setter
    def airflow_run_version(self, airflow_run_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_run_version = airflow_run_version

    @property
    def airflow_run_open_lineage_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_run_open_lineage_version
        )

    @airflow_run_open_lineage_version.setter
    def airflow_run_open_lineage_version(
        self, airflow_run_open_lineage_version: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_run_open_lineage_version = (
            airflow_run_open_lineage_version
        )

    @property
    def airflow_run_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.airflow_run_name

    @airflow_run_name.setter
    def airflow_run_name(self, airflow_run_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_run_name = airflow_run_name

    @property
    def airflow_run_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.airflow_run_type

    @airflow_run_type.setter
    def airflow_run_type(self, airflow_run_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_run_type = airflow_run_type

    @property
    def airflow_run_start_time(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.airflow_run_start_time
        )

    @airflow_run_start_time.setter
    def airflow_run_start_time(self, airflow_run_start_time: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_run_start_time = airflow_run_start_time

    @property
    def airflow_run_end_time(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.airflow_run_end_time

    @airflow_run_end_time.setter
    def airflow_run_end_time(self, airflow_run_end_time: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_run_end_time = airflow_run_end_time

    @property
    def airflow_run_open_lineage_state(self) -> Optional[OpenLineageRunState]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_run_open_lineage_state
        )

    @airflow_run_open_lineage_state.setter
    def airflow_run_open_lineage_state(
        self, airflow_run_open_lineage_state: Optional[OpenLineageRunState]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_run_open_lineage_state = airflow_run_open_lineage_state

    class Attributes(Catalog.Attributes):
        airflow_tags: Optional[set[str]] = Field(default=None, description="")
        airflow_run_version: Optional[str] = Field(default=None, description="")
        airflow_run_open_lineage_version: Optional[str] = Field(
            default=None, description=""
        )
        airflow_run_name: Optional[str] = Field(default=None, description="")
        airflow_run_type: Optional[str] = Field(default=None, description="")
        airflow_run_start_time: Optional[datetime] = Field(default=None, description="")
        airflow_run_end_time: Optional[datetime] = Field(default=None, description="")
        airflow_run_open_lineage_state: Optional[OpenLineageRunState] = Field(
            default=None, description=""
        )

    attributes: "Airflow.Attributes" = Field(
        default_factory=lambda: Airflow.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AirflowDag(Airflow):
    """Description"""

    type_name: str = Field(default="AirflowDag", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AirflowDag":
            raise ValueError("must be AirflowDag")
        return v

    def __setattr__(self, name, value):
        if name in AirflowDag._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AIRFLOW_DAG_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "airflowDagSchedule", "airflowDagSchedule"
    )
    """
    Schedule for the DAG.
    """
    AIRFLOW_DAG_SCHEDULE_DELTA: ClassVar[NumericField] = NumericField(
        "airflowDagScheduleDelta", "airflowDagScheduleDelta"
    )
    """
    Duration between scheduled runs, in seconds.
    """

    AIRFLOW_TASKS: ClassVar[RelationField] = RelationField("airflowTasks")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "airflow_dag_schedule",
        "airflow_dag_schedule_delta",
        "airflow_tasks",
    ]

    @property
    def airflow_dag_schedule(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.airflow_dag_schedule

    @airflow_dag_schedule.setter
    def airflow_dag_schedule(self, airflow_dag_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_dag_schedule = airflow_dag_schedule

    @property
    def airflow_dag_schedule_delta(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_dag_schedule_delta
        )

    @airflow_dag_schedule_delta.setter
    def airflow_dag_schedule_delta(self, airflow_dag_schedule_delta: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_dag_schedule_delta = airflow_dag_schedule_delta

    @property
    def airflow_tasks(self) -> Optional[list[AirflowTask]]:
        return None if self.attributes is None else self.attributes.airflow_tasks

    @airflow_tasks.setter
    def airflow_tasks(self, airflow_tasks: Optional[list[AirflowTask]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_tasks = airflow_tasks

    class Attributes(Airflow.Attributes):
        airflow_dag_schedule: Optional[str] = Field(default=None, description="")
        airflow_dag_schedule_delta: Optional[int] = Field(default=None, description="")
        airflow_tasks: Optional[list[AirflowTask]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "AirflowDag.Attributes" = Field(
        default_factory=lambda: AirflowDag.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AirflowTask(Airflow):
    """Description"""

    type_name: str = Field(default="AirflowTask", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AirflowTask":
            raise ValueError("must be AirflowTask")
        return v

    def __setattr__(self, name, value):
        if name in AirflowTask._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AIRFLOW_TASK_OPERATOR_CLASS: ClassVar[KeywordTextField] = KeywordTextField(
        "airflowTaskOperatorClass",
        "airflowTaskOperatorClass.keyword",
        "airflowTaskOperatorClass",
    )
    """
    Class name for the operator this task uses.
    """
    AIRFLOW_DAG_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "airflowDagName", "airflowDagName.keyword", "airflowDagName"
    )
    """
    Simple name of the DAG this task is contained within.
    """
    AIRFLOW_DAG_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "airflowDagQualifiedName", "airflowDagQualifiedName"
    )
    """
    Unique name of the DAG this task is contained within.
    """
    AIRFLOW_TASK_CONNECTION_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "airflowTaskConnectionId",
        "airflowTaskConnectionId.keyword",
        "airflowTaskConnectionId",
    )
    """
    Identifier for the connection this task accesses.
    """
    AIRFLOW_TASK_SQL: ClassVar[KeywordField] = KeywordField(
        "airflowTaskSql", "airflowTaskSql"
    )
    """
    SQL code that executes through this task.
    """
    AIRFLOW_TASK_RETRY_NUMBER: ClassVar[NumericField] = NumericField(
        "airflowTaskRetryNumber", "airflowTaskRetryNumber"
    )
    """
    Retry count for this task running.
    """
    AIRFLOW_TASK_POOL: ClassVar[KeywordField] = KeywordField(
        "airflowTaskPool", "airflowTaskPool"
    )
    """
    Pool on which this run happened.
    """
    AIRFLOW_TASK_POOL_SLOTS: ClassVar[NumericField] = NumericField(
        "airflowTaskPoolSlots", "airflowTaskPoolSlots"
    )
    """
    Pool slots used for the run.
    """
    AIRFLOW_TASK_QUEUE: ClassVar[KeywordField] = KeywordField(
        "airflowTaskQueue", "airflowTaskQueue"
    )
    """
    Queue on which this run happened.
    """
    AIRFLOW_TASK_PRIORITY_WEIGHT: ClassVar[NumericField] = NumericField(
        "airflowTaskPriorityWeight", "airflowTaskPriorityWeight"
    )
    """
    Priority of the run.
    """
    AIRFLOW_TASK_TRIGGER_RULE: ClassVar[KeywordField] = KeywordField(
        "airflowTaskTriggerRule", "airflowTaskTriggerRule"
    )
    """
    Trigger for the run.
    """

    OUTPUTS: ClassVar[RelationField] = RelationField("outputs")
    """
    TBC
    """
    PROCESS: ClassVar[RelationField] = RelationField("process")
    """
    TBC
    """
    INPUTS: ClassVar[RelationField] = RelationField("inputs")
    """
    TBC
    """
    AIRFLOW_DAG: ClassVar[RelationField] = RelationField("airflowDag")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "airflow_task_operator_class",
        "airflow_dag_name",
        "airflow_dag_qualified_name",
        "airflow_task_connection_id",
        "airflow_task_sql",
        "airflow_task_retry_number",
        "airflow_task_pool",
        "airflow_task_pool_slots",
        "airflow_task_queue",
        "airflow_task_priority_weight",
        "airflow_task_trigger_rule",
        "outputs",
        "process",
        "inputs",
        "airflow_dag",
    ]

    @property
    def airflow_task_operator_class(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_task_operator_class
        )

    @airflow_task_operator_class.setter
    def airflow_task_operator_class(self, airflow_task_operator_class: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_operator_class = airflow_task_operator_class

    @property
    def airflow_dag_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.airflow_dag_name

    @airflow_dag_name.setter
    def airflow_dag_name(self, airflow_dag_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_dag_name = airflow_dag_name

    @property
    def airflow_dag_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_dag_qualified_name
        )

    @airflow_dag_qualified_name.setter
    def airflow_dag_qualified_name(self, airflow_dag_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_dag_qualified_name = airflow_dag_qualified_name

    @property
    def airflow_task_connection_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_task_connection_id
        )

    @airflow_task_connection_id.setter
    def airflow_task_connection_id(self, airflow_task_connection_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_connection_id = airflow_task_connection_id

    @property
    def airflow_task_sql(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.airflow_task_sql

    @airflow_task_sql.setter
    def airflow_task_sql(self, airflow_task_sql: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_sql = airflow_task_sql

    @property
    def airflow_task_retry_number(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_task_retry_number
        )

    @airflow_task_retry_number.setter
    def airflow_task_retry_number(self, airflow_task_retry_number: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_retry_number = airflow_task_retry_number

    @property
    def airflow_task_pool(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.airflow_task_pool

    @airflow_task_pool.setter
    def airflow_task_pool(self, airflow_task_pool: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_pool = airflow_task_pool

    @property
    def airflow_task_pool_slots(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.airflow_task_pool_slots
        )

    @airflow_task_pool_slots.setter
    def airflow_task_pool_slots(self, airflow_task_pool_slots: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_pool_slots = airflow_task_pool_slots

    @property
    def airflow_task_queue(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.airflow_task_queue

    @airflow_task_queue.setter
    def airflow_task_queue(self, airflow_task_queue: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_queue = airflow_task_queue

    @property
    def airflow_task_priority_weight(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_task_priority_weight
        )

    @airflow_task_priority_weight.setter
    def airflow_task_priority_weight(self, airflow_task_priority_weight: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_priority_weight = airflow_task_priority_weight

    @property
    def airflow_task_trigger_rule(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_task_trigger_rule
        )

    @airflow_task_trigger_rule.setter
    def airflow_task_trigger_rule(self, airflow_task_trigger_rule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_trigger_rule = airflow_task_trigger_rule

    @property
    def outputs(self) -> Optional[list[Catalog]]:
        return None if self.attributes is None else self.attributes.outputs

    @outputs.setter
    def outputs(self, outputs: Optional[list[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.outputs = outputs

    @property
    def process(self) -> Optional[Process]:
        return None if self.attributes is None else self.attributes.process

    @process.setter
    def process(self, process: Optional[Process]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.process = process

    @property
    def inputs(self) -> Optional[list[Catalog]]:
        return None if self.attributes is None else self.attributes.inputs

    @inputs.setter
    def inputs(self, inputs: Optional[list[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inputs = inputs

    @property
    def airflow_dag(self) -> Optional[AirflowDag]:
        return None if self.attributes is None else self.attributes.airflow_dag

    @airflow_dag.setter
    def airflow_dag(self, airflow_dag: Optional[AirflowDag]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_dag = airflow_dag

    class Attributes(Airflow.Attributes):
        airflow_task_operator_class: Optional[str] = Field(default=None, description="")
        airflow_dag_name: Optional[str] = Field(default=None, description="")
        airflow_dag_qualified_name: Optional[str] = Field(default=None, description="")
        airflow_task_connection_id: Optional[str] = Field(default=None, description="")
        airflow_task_sql: Optional[str] = Field(default=None, description="")
        airflow_task_retry_number: Optional[int] = Field(default=None, description="")
        airflow_task_pool: Optional[str] = Field(default=None, description="")
        airflow_task_pool_slots: Optional[int] = Field(default=None, description="")
        airflow_task_queue: Optional[str] = Field(default=None, description="")
        airflow_task_priority_weight: Optional[int] = Field(
            default=None, description=""
        )
        airflow_task_trigger_rule: Optional[str] = Field(default=None, description="")
        outputs: Optional[list[Catalog]] = Field(
            default=None, description=""
        )  # relationship
        process: Optional[Process] = Field(default=None, description="")  # relationship
        inputs: Optional[list[Catalog]] = Field(
            default=None, description=""
        )  # relationship
        airflow_dag: Optional[AirflowDag] = Field(
            default=None, description=""
        )  # relationship

    attributes: "AirflowTask.Attributes" = Field(
        default_factory=lambda: AirflowTask.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DataQuality(Catalog):
    """Description"""

    type_name: str = Field(default="DataQuality", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataQuality":
            raise ValueError("must be DataQuality")
        return v

    def __setattr__(self, name, value):
        if name in DataQuality._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[list[str]] = []


class Metric(DataQuality):
    """Description"""

    type_name: str = Field(default="Metric", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Metric":
            raise ValueError("must be Metric")
        return v

    def __setattr__(self, name, value):
        if name in Metric._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    METRIC_TYPE: ClassVar[KeywordField] = KeywordField("metricType", "metricType")
    """
    Type of the metric.
    """
    METRIC_SQL: ClassVar[KeywordField] = KeywordField("metricSQL", "metricSQL")
    """
    SQL query used to compute the metric.
    """
    METRIC_FILTERS: ClassVar[TextField] = TextField("metricFilters", "metricFilters")
    """
    Filters to be applied to the metric query.
    """
    METRIC_TIME_GRAINS: ClassVar[TextField] = TextField(
        "metricTimeGrains", "metricTimeGrains"
    )
    """
    List of time grains to be applied to the metric query.
    """

    METRIC_TIMESTAMP_COLUMN: ClassVar[RelationField] = RelationField(
        "metricTimestampColumn"
    )
    """
    TBC
    """
    ASSETS: ClassVar[RelationField] = RelationField("assets")
    """
    TBC
    """
    METRIC_DIMENSION_COLUMNS: ClassVar[RelationField] = RelationField(
        "metricDimensionColumns"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "metric_type",
        "metric_s_q_l",
        "metric_filters",
        "metric_time_grains",
        "metric_timestamp_column",
        "assets",
        "metric_dimension_columns",
    ]

    @property
    def metric_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metric_type

    @metric_type.setter
    def metric_type(self, metric_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_type = metric_type

    @property
    def metric_s_q_l(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metric_s_q_l

    @metric_s_q_l.setter
    def metric_s_q_l(self, metric_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_s_q_l = metric_s_q_l

    @property
    def metric_filters(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metric_filters

    @metric_filters.setter
    def metric_filters(self, metric_filters: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_filters = metric_filters

    @property
    def metric_time_grains(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.metric_time_grains

    @metric_time_grains.setter
    def metric_time_grains(self, metric_time_grains: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_time_grains = metric_time_grains

    @property
    def metric_timestamp_column(self) -> Optional[Column]:
        return (
            None if self.attributes is None else self.attributes.metric_timestamp_column
        )

    @metric_timestamp_column.setter
    def metric_timestamp_column(self, metric_timestamp_column: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_timestamp_column = metric_timestamp_column

    @property
    def assets(self) -> Optional[list[Asset]]:
        return None if self.attributes is None else self.attributes.assets

    @assets.setter
    def assets(self, assets: Optional[list[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.assets = assets

    @property
    def metric_dimension_columns(self) -> Optional[list[Column]]:
        return (
            None
            if self.attributes is None
            else self.attributes.metric_dimension_columns
        )

    @metric_dimension_columns.setter
    def metric_dimension_columns(
        self, metric_dimension_columns: Optional[list[Column]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_dimension_columns = metric_dimension_columns

    class Attributes(DataQuality.Attributes):
        metric_type: Optional[str] = Field(default=None, description="")
        metric_s_q_l: Optional[str] = Field(default=None, description="")
        metric_filters: Optional[str] = Field(default=None, description="")
        metric_time_grains: Optional[set[str]] = Field(default=None, description="")
        metric_timestamp_column: Optional[Column] = Field(
            default=None, description=""
        )  # relationship
        assets: Optional[list[Asset]] = Field(
            default=None, description=""
        )  # relationship
        metric_dimension_columns: Optional[list[Column]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "Metric.Attributes" = Field(
        default_factory=lambda: Metric.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Resource(Catalog):
    """Description"""

    type_name: str = Field(default="Resource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Resource":
            raise ValueError("must be Resource")
        return v

    def __setattr__(self, name, value):
        if name in Resource._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    LINK: ClassVar[KeywordField] = KeywordField("link", "link")
    """
    URL to the resource.
    """
    IS_GLOBAL: ClassVar[BooleanField] = BooleanField("isGlobal", "isGlobal")
    """
    Whether the resource is global (true) or not (false).
    """
    REFERENCE: ClassVar[KeywordField] = KeywordField("reference", "reference")
    """
    Reference to the resource.
    """
    RESOURCE_METADATA: ClassVar[KeywordField] = KeywordField(
        "resourceMetadata", "resourceMetadata"
    )
    """
    Metadata of the resource.
    """

    _convenience_properties: ClassVar[list[str]] = [
        "link",
        "is_global",
        "reference",
        "resource_metadata",
    ]

    @property
    def link(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.link

    @link.setter
    def link(self, link: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.link = link

    @property
    def is_global(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_global

    @is_global.setter
    def is_global(self, is_global: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_global = is_global

    @property
    def reference(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.reference

    @reference.setter
    def reference(self, reference: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reference = reference

    @property
    def resource_metadata(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.resource_metadata

    @resource_metadata.setter
    def resource_metadata(self, resource_metadata: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.resource_metadata = resource_metadata

    class Attributes(Catalog.Attributes):
        link: Optional[str] = Field(default=None, description="")
        is_global: Optional[bool] = Field(default=None, description="")
        reference: Optional[str] = Field(default=None, description="")
        resource_metadata: Optional[dict[str, str]] = Field(
            default=None, description=""
        )

    attributes: "Resource.Attributes" = Field(
        default_factory=lambda: Resource.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Readme(Resource):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(
        cls, *, asset: Asset, content: str, asset_name: Optional[str] = None
    ) -> Readme:
        return Readme(
            attributes=Readme.Attributes.create(
                asset=asset, content=content, asset_name=asset_name
            )
        )

    @property
    def description(self) -> Optional[str]:
        ret_value = self.attributes.description
        return unquote(ret_value) if ret_value is not None else ret_value

    @description.setter
    def description(self, description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.description = (
            quote(description) if description is not None else description
        )

    type_name: str = Field(default="Readme", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Readme":
            raise ValueError("must be Readme")
        return v

    def __setattr__(self, name, value):
        if name in Readme._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SEE_ALSO: ClassVar[RelationField] = RelationField("seeAlso")
    """
    TBC
    """
    ASSET: ClassVar[RelationField] = RelationField("asset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "see_also",
        "asset",
    ]

    @property
    def see_also(self) -> Optional[list[Readme]]:
        return None if self.attributes is None else self.attributes.see_also

    @see_also.setter
    def see_also(self, see_also: Optional[list[Readme]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.see_also = see_also

    @property
    def asset(self) -> Optional[Asset]:
        return None if self.attributes is None else self.attributes.asset

    @asset.setter
    def asset(self, asset: Optional[Asset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset = asset

    class Attributes(Resource.Attributes):
        see_also: Optional[list[Readme]] = Field(
            default=None, description=""
        )  # relationship
        asset: Optional[Asset] = Field(default=None, description="")  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, *, asset: Asset, content: str, asset_name: Optional[str] = None
        ) -> Readme.Attributes:
            validate_required_fields(["asset", "content"], [asset, content])
            if not asset.name or len(asset.name) < 1:
                if not asset_name:
                    raise ValueError(
                        "asset_name is required when name is not available from asset"
                    )
            elif asset_name:
                raise ValueError(
                    "asset_name can not be given when name is available from asset"
                )
            else:
                asset_name = asset.name
            return Readme.Attributes(
                qualified_name=f"{asset.guid}/readme",
                name=f"{asset_name} Readme",
                asset=asset,
                description=quote(content),
            )

    attributes: "Readme.Attributes" = Field(
        default_factory=lambda: Readme.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class File(Resource):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(
        cls, *, name: str, connection_qualified_name: str, file_type: FileType
    ) -> File:
        return File(
            attributes=File.Attributes.create(
                name=name,
                connection_qualified_name=connection_qualified_name,
                file_type=file_type,
            )
        )

    type_name: str = Field(default="File", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "File":
            raise ValueError("must be File")
        return v

    def __setattr__(self, name, value):
        if name in File._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FILE_TYPE: ClassVar[KeywordField] = KeywordField("fileType", "fileType")
    """
    Type (extension) of the file.
    """
    FILE_PATH: ClassVar[KeywordField] = KeywordField("filePath", "filePath")
    """
    URL giving the online location where the file can be accessed.
    """

    FILE_ASSETS: ClassVar[RelationField] = RelationField("fileAssets")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "file_type",
        "file_path",
        "file_assets",
    ]

    @property
    def file_type(self) -> Optional[FileType]:
        return None if self.attributes is None else self.attributes.file_type

    @file_type.setter
    def file_type(self, file_type: Optional[FileType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.file_type = file_type

    @property
    def file_path(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.file_path

    @file_path.setter
    def file_path(self, file_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.file_path = file_path

    @property
    def file_assets(self) -> Optional[Asset]:
        return None if self.attributes is None else self.attributes.file_assets

    @file_assets.setter
    def file_assets(self, file_assets: Optional[Asset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.file_assets = file_assets

    class Attributes(Resource.Attributes):
        file_type: Optional[FileType] = Field(default=None, description="")
        file_path: Optional[str] = Field(default=None, description="")
        file_assets: Optional[Asset] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, *, name: str, connection_qualified_name: str, file_type: FileType
        ) -> File.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name", "file_type"],
                [name, connection_qualified_name, file_type],
            )
            return File.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                file_type=file_type,
            )

    attributes: "File.Attributes" = Field(
        default_factory=lambda: File.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Link(Resource):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(
        cls, *, asset: Asset, name: str, link: str, idempotent: bool = False
    ) -> Link:
        return Link(
            attributes=Link.Attributes.create(
                asset=asset, name=name, link=link, idempotent=idempotent
            )
        )

    type_name: str = Field(default="Link", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Link":
            raise ValueError("must be Link")
        return v

    def __setattr__(self, name, value):
        if name in Link._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ICON: ClassVar[KeywordField] = KeywordField("icon", "icon")
    """
    Icon for the link.
    """
    ICON_TYPE: ClassVar[KeywordField] = KeywordField("iconType", "iconType")
    """
    Type of icon for the link, for example: image or emoji.
    """

    ASSET: ClassVar[RelationField] = RelationField("asset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "icon",
        "icon_type",
        "asset",
    ]

    @property
    def icon(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.icon

    @icon.setter
    def icon(self, icon: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon = icon

    @property
    def icon_type(self) -> Optional[IconType]:
        return None if self.attributes is None else self.attributes.icon_type

    @icon_type.setter
    def icon_type(self, icon_type: Optional[IconType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon_type = icon_type

    @property
    def asset(self) -> Optional[Asset]:
        return None if self.attributes is None else self.attributes.asset

    @asset.setter
    def asset(self, asset: Optional[Asset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset = asset

    class Attributes(Resource.Attributes):
        icon: Optional[str] = Field(default=None, description="")
        icon_type: Optional[IconType] = Field(default=None, description="")
        asset: Optional[Asset] = Field(default=None, description="")  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, *, asset: Asset, name: str, link: str, idempotent: bool
        ) -> Link.Attributes:
            validate_required_fields(["asset", "name", "link"], [asset, name, link])
            qn = f"{asset.qualified_name}/{name}" if idempotent else str(uuid.uuid4())
            return Link.Attributes(
                qualified_name=qn,
                name=name,
                link=link,
                asset=asset.trim_to_reference(),
            )

    attributes: "Link.Attributes" = Field(
        default_factory=lambda: Link.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DataMesh(Catalog):
    """Description"""

    type_name: str = Field(default="DataMesh", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataMesh":
            raise ValueError("must be DataMesh")
        return v

    def __setattr__(self, name, value):
        if name in DataMesh._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PARENT_DOMAIN_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "parentDomainQualifiedName",
        "parentDomainQualifiedName",
        "parentDomainQualifiedName.text",
    )
    """
    Unique name of the parent domain in which this asset exists.
    """
    SUPER_DOMAIN_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "superDomainQualifiedName",
        "superDomainQualifiedName",
        "superDomainQualifiedName.text",
    )
    """
    Unique name of the top-level domain in which this asset exists.
    """

    _convenience_properties: ClassVar[list[str]] = [
        "parent_domain_qualified_name",
        "super_domain_qualified_name",
    ]

    @property
    def parent_domain_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.parent_domain_qualified_name
        )

    @parent_domain_qualified_name.setter
    def parent_domain_qualified_name(self, parent_domain_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_domain_qualified_name = parent_domain_qualified_name

    @property
    def super_domain_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.super_domain_qualified_name
        )

    @super_domain_qualified_name.setter
    def super_domain_qualified_name(self, super_domain_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.super_domain_qualified_name = super_domain_qualified_name

    class Attributes(Catalog.Attributes):
        parent_domain_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        super_domain_qualified_name: Optional[str] = Field(default=None, description="")

    attributes: "DataMesh.Attributes" = Field(
        default_factory=lambda: DataMesh.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DataDomain(DataMesh):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(
        cls,
        *,
        name: StrictStr,
        icon: Optional[AtlanIcon] = None,
        parent_domain: Optional[DataDomain] = None,
        parent_domain_qualified_name: Optional[StrictStr] = None,
    ) -> DataDomain:
        validate_required_fields(["name"], [name])
        attributes = DataDomain.Attributes.create(
            name=name,
            icon=icon,
            parent_domain=parent_domain,
            parent_domain_qualified_name=parent_domain_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    def create_for_modification(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = "",
    ) -> SelfAsset:
        validate_required_fields(["name", "qualified_name"], [name, qualified_name])
        # Split the data domain qualified_name to extract data mesh info
        fields = qualified_name.split("/")
        # for domain and subdomain
        if len(fields) not in (3, 5):
            raise ValueError(f"Invalid data domain qualified_name: {qualified_name}")
        return cls(
            attributes=cls.Attributes(
                qualified_name=qualified_name,
                name=name,
            )
        )

    type_name: str = Field(default="DataDomain", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataDomain":
            raise ValueError("must be DataDomain")
        return v

    def __setattr__(self, name, value):
        if name in DataDomain._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_PRODUCTS: ClassVar[RelationField] = RelationField("dataProducts")
    """
    TBC
    """
    PARENT_DOMAIN: ClassVar[RelationField] = RelationField("parentDomain")
    """
    TBC
    """
    SUB_DOMAINS: ClassVar[RelationField] = RelationField("subDomains")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "data_products",
        "parent_domain",
        "sub_domains",
    ]

    @property
    def data_products(self) -> Optional[list[DataProduct]]:
        return None if self.attributes is None else self.attributes.data_products

    @data_products.setter
    def data_products(self, data_products: Optional[list[DataProduct]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_products = data_products

    @property
    def parent_domain(self) -> Optional[DataDomain]:
        return None if self.attributes is None else self.attributes.parent_domain

    @parent_domain.setter
    def parent_domain(self, parent_domain: Optional[DataDomain]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_domain = parent_domain

    @property
    def sub_domains(self) -> Optional[list[DataDomain]]:
        return None if self.attributes is None else self.attributes.sub_domains

    @sub_domains.setter
    def sub_domains(self, sub_domains: Optional[list[DataDomain]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sub_domains = sub_domains

    class Attributes(DataMesh.Attributes):
        data_products: Optional[list[DataProduct]] = Field(
            default=None, description=""
        )  # relationship
        parent_domain: Optional[DataDomain] = Field(
            default=None, description=""
        )  # relationship
        sub_domains: Optional[list[DataDomain]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: StrictStr,
            icon: Optional[AtlanIcon] = None,
            parent_domain: Optional[DataDomain] = None,
            parent_domain_qualified_name: Optional[StrictStr] = None,
        ) -> DataDomain.Attributes:
            validate_required_fields(["name"], [name])
            mesh_name = to_camel_case(name)
            qualified_name = f"default/domain/{mesh_name}"
            # If "qualified name" of the parent domain is specified
            if parent_domain_qualified_name:
                parent_domain = DataDomain()
                parent_domain.unique_attributes = {
                    "qualifiedName": parent_domain_qualified_name
                }
                qualified_name = f"{parent_domain_qualified_name}/domain/{mesh_name}"
            icon_str = icon.value if icon is not None else None
            return DataDomain.Attributes(
                name=name,
                parent_domain=parent_domain,
                qualified_name=qualified_name,
                asset_icon=icon_str,
            )

    attributes: "DataDomain.Attributes" = Field(
        default_factory=lambda: DataDomain.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DataProduct(DataMesh):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(
        cls,
        *,
        name: StrictStr,
        assets: IndexSearchRequest,
        icon: Optional[AtlanIcon] = None,
        domain: Optional[DataDomain] = None,
        domain_qualified_name: Optional[StrictStr] = None,
    ) -> DataProduct:
        validate_required_fields(["name", "assets"], [name, assets])
        assets_dsl = assets.get_dsl_str()
        attributes = DataProduct.Attributes.create(
            name=name,
            assets_dsl=assets_dsl,
            icon=icon,
            domain=domain,
            domain_qualified_name=domain_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    def create_for_modification(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = "",
    ) -> SelfAsset:
        validate_required_fields(
            ["name", "qualified_name"],
            [name, qualified_name],
        )
        # Split the data product qualified_name to extract data mesh info
        fields = qualified_name.split("/")
        if len(fields) != 3:
            raise ValueError(f"Invalid data product qualified_name: {qualified_name}")
        return cls(
            attributes=cls.Attributes(
                qualified_name=qualified_name,
                name=name,
            )
        )

    type_name: str = Field(default="DataProduct", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataProduct":
            raise ValueError("must be DataProduct")
        return v

    def __setattr__(self, name, value):
        if name in DataProduct._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_PRODUCT_STATUS: ClassVar[KeywordField] = KeywordField(
        "dataProductStatus", "dataProductStatus"
    )
    """
    Status of this data product.
    """
    DATA_PRODUCT_CRITICALITY: ClassVar[KeywordField] = KeywordField(
        "dataProductCriticality", "dataProductCriticality"
    )
    """
    Criticality of this data product.
    """
    DATA_PRODUCT_SENSITIVITY: ClassVar[KeywordField] = KeywordField(
        "dataProductSensitivity", "dataProductSensitivity"
    )
    """
    Information sensitivity of this data product.
    """
    DATA_PRODUCT_ASSETS_DSL: ClassVar[KeywordField] = KeywordField(
        "dataProductAssetsDSL", "dataProductAssetsDSL"
    )
    """
    Search DSL used to define which assets are part of this data product.
    """
    DATA_PRODUCT_ASSETS_PLAYBOOK_FILTER: ClassVar[KeywordField] = KeywordField(
        "dataProductAssetsPlaybookFilter", "dataProductAssetsPlaybookFilter"
    )
    """
    Playbook filter to define which assets are part of this data product.
    """

    DATA_DOMAIN: ClassVar[RelationField] = RelationField("dataDomain")
    """
    TBC
    """
    OUTPUT_PORTS: ClassVar[RelationField] = RelationField("outputPorts")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "data_product_status",
        "data_product_criticality",
        "data_product_sensitivity",
        "data_product_assets_d_s_l",
        "data_product_assets_playbook_filter",
        "data_domain",
        "output_ports",
    ]

    @property
    def data_product_status(self) -> Optional[DataProductStatus]:
        return None if self.attributes is None else self.attributes.data_product_status

    @data_product_status.setter
    def data_product_status(self, data_product_status: Optional[DataProductStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_product_status = data_product_status

    @property
    def data_product_criticality(self) -> Optional[DataProductCriticality]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_product_criticality
        )

    @data_product_criticality.setter
    def data_product_criticality(
        self, data_product_criticality: Optional[DataProductCriticality]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_product_criticality = data_product_criticality

    @property
    def data_product_sensitivity(self) -> Optional[DataProductSensitivity]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_product_sensitivity
        )

    @data_product_sensitivity.setter
    def data_product_sensitivity(
        self, data_product_sensitivity: Optional[DataProductSensitivity]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_product_sensitivity = data_product_sensitivity

    @property
    def data_product_assets_d_s_l(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_product_assets_d_s_l
        )

    @data_product_assets_d_s_l.setter
    def data_product_assets_d_s_l(self, data_product_assets_d_s_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_product_assets_d_s_l = data_product_assets_d_s_l

    @property
    def data_product_assets_playbook_filter(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_product_assets_playbook_filter
        )

    @data_product_assets_playbook_filter.setter
    def data_product_assets_playbook_filter(
        self, data_product_assets_playbook_filter: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_product_assets_playbook_filter = (
            data_product_assets_playbook_filter
        )

    @property
    def data_domain(self) -> Optional[DataDomain]:
        return None if self.attributes is None else self.attributes.data_domain

    @data_domain.setter
    def data_domain(self, data_domain: Optional[DataDomain]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_domain = data_domain

    @property
    def output_ports(self) -> Optional[list[Asset]]:
        return None if self.attributes is None else self.attributes.output_ports

    @output_ports.setter
    def output_ports(self, output_ports: Optional[list[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_ports = output_ports

    class Attributes(DataMesh.Attributes):
        data_product_status: Optional[DataProductStatus] = Field(
            default=None, description=""
        )
        data_product_criticality: Optional[DataProductCriticality] = Field(
            default=None, description=""
        )
        data_product_sensitivity: Optional[DataProductSensitivity] = Field(
            default=None, description=""
        )
        data_product_assets_d_s_l: Optional[str] = Field(default=None, description="")
        data_product_assets_playbook_filter: Optional[str] = Field(
            default=None, description=""
        )
        data_domain: Optional[DataDomain] = Field(
            default=None, description=""
        )  # relationship
        output_ports: Optional[list[Asset]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: StrictStr,
            assets_dsl: StrictStr,
            icon: Optional[AtlanIcon] = None,
            domain: Optional[DataDomain] = None,
            domain_qualified_name: Optional[StrictStr] = None,
        ) -> DataProduct.Attributes:
            validate_required_fields(["name"], [name])
            validate_single_required_field(
                ["domain", "domain_qualified_name"],
                [domain, domain_qualified_name],
            )
            if domain_qualified_name:
                domain = DataDomain()
                domain.unique_attributes = {"qualifiedName": domain_qualified_name}
            icon_str = icon.value if icon is not None else None
            camel_case_name = to_camel_case(name)
            return DataProduct.Attributes(
                name=name,
                data_product_assets_d_s_l=assets_dsl,
                data_domain=domain,
                qualified_name=f"default/product/{camel_case_name}",
                asset_icon=icon_str,
            )

    attributes: "DataProduct.Attributes" = Field(
        default_factory=lambda: DataProduct.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SQL(Catalog):
    """Description"""

    type_name: str = Field(default="SQL", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SQL":
            raise ValueError("must be SQL")
        return v

    def __setattr__(self, name, value):
        if name in SQL._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUERY_COUNT: ClassVar[NumericField] = NumericField("queryCount", "queryCount")
    """
    Number of times this asset has been queried.
    """
    QUERY_USER_COUNT: ClassVar[NumericField] = NumericField(
        "queryUserCount", "queryUserCount"
    )
    """
    Number of unique users who have queried this asset.
    """
    QUERY_USER_MAP: ClassVar[KeywordField] = KeywordField(
        "queryUserMap", "queryUserMap"
    )
    """
    Map of unique users who have queried this asset to the number of times they have queried it.
    """
    QUERY_COUNT_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "queryCountUpdatedAt", "queryCountUpdatedAt"
    )
    """
    Time (epoch) at which the query count was last updated, in milliseconds.
    """
    DATABASE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "databaseName", "databaseName.keyword", "databaseName"
    )
    """
    Simple name of the database in which this SQL asset exists, or empty if it does not exist within a database.
    """
    DATABASE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "databaseQualifiedName", "databaseQualifiedName"
    )
    """
    Unique name of the database in which this SQL asset exists, or empty if it does not exist within a database.
    """
    SCHEMA_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "schemaName", "schemaName.keyword", "schemaName"
    )
    """
    Simple name of the schema in which this SQL asset exists, or empty if it does not exist within a schema.
    """
    SCHEMA_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "schemaQualifiedName", "schemaQualifiedName"
    )
    """
    Unique name of the schema in which this SQL asset exists, or empty if it does not exist within a schema.
    """
    TABLE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "tableName", "tableName.keyword", "tableName"
    )
    """
    Simple name of the table in which this SQL asset exists, or empty if it does not exist within a table.
    """
    TABLE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "tableQualifiedName", "tableQualifiedName"
    )
    """
    Unique name of the table in which this SQL asset exists, or empty if it does not exist within a table.
    """
    VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "viewName", "viewName.keyword", "viewName"
    )
    """
    Simple name of the view in which this SQL asset exists, or empty if it does not exist within a view.
    """
    VIEW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "viewQualifiedName", "viewQualifiedName"
    )
    """
    Unique name of the view in which this SQL asset exists, or empty if it does not exist within a view.
    """
    IS_PROFILED: ClassVar[BooleanField] = BooleanField("isProfiled", "isProfiled")
    """
    Whether this asset has been profiled (true) or not (false).
    """
    LAST_PROFILED_AT: ClassVar[NumericField] = NumericField(
        "lastProfiledAt", "lastProfiledAt"
    )
    """
    Time (epoch) at which this asset was last profiled, in milliseconds.
    """

    DBT_SOURCES: ClassVar[RelationField] = RelationField("dbtSources")
    """
    TBC
    """
    SQL_DBT_MODELS: ClassVar[RelationField] = RelationField("sqlDbtModels")
    """
    TBC
    """
    SQL_DBT_SOURCES: ClassVar[RelationField] = RelationField("sqlDBTSources")
    """
    TBC
    """
    DBT_MODELS: ClassVar[RelationField] = RelationField("dbtModels")
    """
    TBC
    """
    DBT_TESTS: ClassVar[RelationField] = RelationField("dbtTests")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "query_count",
        "query_user_count",
        "query_user_map",
        "query_count_updated_at",
        "database_name",
        "database_qualified_name",
        "schema_name",
        "schema_qualified_name",
        "table_name",
        "table_qualified_name",
        "view_name",
        "view_qualified_name",
        "is_profiled",
        "last_profiled_at",
        "dbt_sources",
        "sql_dbt_models",
        "sql_dbt_sources",
        "dbt_models",
        "dbt_tests",
    ]

    @property
    def query_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_count

    @query_count.setter
    def query_count(self, query_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_count = query_count

    @property
    def query_user_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_user_count

    @query_user_count.setter
    def query_user_count(self, query_user_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_user_count = query_user_count

    @property
    def query_user_map(self) -> Optional[dict[str, int]]:
        return None if self.attributes is None else self.attributes.query_user_map

    @query_user_map.setter
    def query_user_map(self, query_user_map: Optional[dict[str, int]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_user_map = query_user_map

    @property
    def query_count_updated_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.query_count_updated_at
        )

    @query_count_updated_at.setter
    def query_count_updated_at(self, query_count_updated_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_count_updated_at = query_count_updated_at

    @property
    def database_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.database_name

    @database_name.setter
    def database_name(self, database_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database_name = database_name

    @property
    def database_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.database_qualified_name
        )

    @database_qualified_name.setter
    def database_qualified_name(self, database_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database_qualified_name = database_qualified_name

    @property
    def schema_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.schema_name

    @schema_name.setter
    def schema_name(self, schema_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_name = schema_name

    @property
    def schema_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.schema_qualified_name
        )

    @schema_qualified_name.setter
    def schema_qualified_name(self, schema_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_qualified_name = schema_qualified_name

    @property
    def table_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.table_name

    @table_name.setter
    def table_name(self, table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_name = table_name

    @property
    def table_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.table_qualified_name

    @table_qualified_name.setter
    def table_qualified_name(self, table_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_qualified_name = table_qualified_name

    @property
    def view_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.view_name

    @view_name.setter
    def view_name(self, view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_name = view_name

    @property
    def view_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.view_qualified_name

    @view_qualified_name.setter
    def view_qualified_name(self, view_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_qualified_name = view_qualified_name

    @property
    def is_profiled(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_profiled

    @is_profiled.setter
    def is_profiled(self, is_profiled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_profiled = is_profiled

    @property
    def last_profiled_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.last_profiled_at

    @last_profiled_at.setter
    def last_profiled_at(self, last_profiled_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_profiled_at = last_profiled_at

    @property
    def dbt_sources(self) -> Optional[list[DbtSource]]:
        return None if self.attributes is None else self.attributes.dbt_sources

    @dbt_sources.setter
    def dbt_sources(self, dbt_sources: Optional[list[DbtSource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_sources = dbt_sources

    @property
    def sql_dbt_models(self) -> Optional[list[DbtModel]]:
        return None if self.attributes is None else self.attributes.sql_dbt_models

    @sql_dbt_models.setter
    def sql_dbt_models(self, sql_dbt_models: Optional[list[DbtModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_dbt_models = sql_dbt_models

    @property
    def sql_dbt_sources(self) -> Optional[list[DbtSource]]:
        return None if self.attributes is None else self.attributes.sql_dbt_sources

    @sql_dbt_sources.setter
    def sql_dbt_sources(self, sql_dbt_sources: Optional[list[DbtSource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_dbt_sources = sql_dbt_sources

    @property
    def dbt_models(self) -> Optional[list[DbtModel]]:
        return None if self.attributes is None else self.attributes.dbt_models

    @dbt_models.setter
    def dbt_models(self, dbt_models: Optional[list[DbtModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_models = dbt_models

    @property
    def dbt_tests(self) -> Optional[list[DbtTest]]:
        return None if self.attributes is None else self.attributes.dbt_tests

    @dbt_tests.setter
    def dbt_tests(self, dbt_tests: Optional[list[DbtTest]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tests = dbt_tests

    class Attributes(Catalog.Attributes):
        query_count: Optional[int] = Field(default=None, description="")
        query_user_count: Optional[int] = Field(default=None, description="")
        query_user_map: Optional[dict[str, int]] = Field(default=None, description="")
        query_count_updated_at: Optional[datetime] = Field(default=None, description="")
        database_name: Optional[str] = Field(default=None, description="")
        database_qualified_name: Optional[str] = Field(default=None, description="")
        schema_name: Optional[str] = Field(default=None, description="")
        schema_qualified_name: Optional[str] = Field(default=None, description="")
        table_name: Optional[str] = Field(default=None, description="")
        table_qualified_name: Optional[str] = Field(default=None, description="")
        view_name: Optional[str] = Field(default=None, description="")
        view_qualified_name: Optional[str] = Field(default=None, description="")
        is_profiled: Optional[bool] = Field(default=None, description="")
        last_profiled_at: Optional[datetime] = Field(default=None, description="")
        dbt_sources: Optional[list[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        dbt_tests: Optional[list[DbtTest]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "SQL.Attributes" = Field(
        default_factory=lambda: SQL.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Query(SQL):
    """Description"""

    type_name: str = Field(default="Query", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Query":
            raise ValueError("must be Query")
        return v

    def __setattr__(self, name, value):
        if name in Query._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    RAW_QUERY: ClassVar[KeywordField] = KeywordField("rawQuery", "rawQuery")
    """
    Deprecated. See 'longRawQuery' instead.
    """
    LONG_RAW_QUERY: ClassVar[KeywordField] = KeywordField(
        "longRawQuery", "longRawQuery"
    )
    """
    Raw SQL query string.
    """
    RAW_QUERY_TEXT: ClassVar[RelationField] = RelationField("rawQueryText")
    """

    """
    DEFAULT_SCHEMA_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "defaultSchemaQualifiedName",
        "defaultSchemaQualifiedName",
        "defaultSchemaQualifiedName.text",
    )
    """
    Unique name of the default schema to use for this query.
    """
    DEFAULT_DATABASE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "defaultDatabaseQualifiedName",
        "defaultDatabaseQualifiedName",
        "defaultDatabaseQualifiedName.text",
    )
    """
    Unique name of the default database to use for this query.
    """
    VARIABLES_SCHEMA_BASE64: ClassVar[KeywordField] = KeywordField(
        "variablesSchemaBase64", "variablesSchemaBase64"
    )
    """
    Base64-encoded string of the variables to use in this query.
    """
    IS_PRIVATE: ClassVar[BooleanField] = BooleanField("isPrivate", "isPrivate")
    """
    Whether this query is private (true) or shared (false).
    """
    IS_SQL_SNIPPET: ClassVar[BooleanField] = BooleanField(
        "isSqlSnippet", "isSqlSnippet"
    )
    """
    Whether this query is a SQL snippet (true) or not (false).
    """
    PARENT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "parentQualifiedName", "parentQualifiedName", "parentQualifiedName.text"
    )
    """
    Unique name of the parent collection or folder in which this query exists.
    """
    COLLECTION_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "collectionQualifiedName",
        "collectionQualifiedName",
        "collectionQualifiedName.text",
    )
    """
    Unique name of the collection in which this query exists.
    """
    IS_VISUAL_QUERY: ClassVar[BooleanField] = BooleanField(
        "isVisualQuery", "isVisualQuery"
    )
    """
    Whether this query is a visual query (true) or not (false).
    """
    VISUAL_BUILDER_SCHEMA_BASE64: ClassVar[KeywordField] = KeywordField(
        "visualBuilderSchemaBase64", "visualBuilderSchemaBase64"
    )
    """
    Base64-encoded string for the visual query builder.
    """

    PARENT: ClassVar[RelationField] = RelationField("parent")
    """
    TBC
    """
    COLUMNS: ClassVar[RelationField] = RelationField("columns")
    """
    TBC
    """
    TABLES: ClassVar[RelationField] = RelationField("tables")
    """
    TBC
    """
    VIEWS: ClassVar[RelationField] = RelationField("views")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "raw_query",
        "long_raw_query",
        "raw_query_text",
        "default_schema_qualified_name",
        "default_database_qualified_name",
        "variables_schema_base64",
        "is_private",
        "is_sql_snippet",
        "parent_qualified_name",
        "collection_qualified_name",
        "is_visual_query",
        "visual_builder_schema_base64",
        "parent",
        "columns",
        "tables",
        "views",
    ]

    @property
    def raw_query(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.raw_query

    @raw_query.setter
    def raw_query(self, raw_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.raw_query = raw_query

    @property
    def long_raw_query(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.long_raw_query

    @long_raw_query.setter
    def long_raw_query(self, long_raw_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.long_raw_query = long_raw_query

    @property
    def raw_query_text(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.raw_query_text

    @raw_query_text.setter
    def raw_query_text(self, raw_query_text: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.raw_query_text = raw_query_text

    @property
    def default_schema_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.default_schema_qualified_name
        )

    @default_schema_qualified_name.setter
    def default_schema_qualified_name(
        self, default_schema_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.default_schema_qualified_name = default_schema_qualified_name

    @property
    def default_database_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.default_database_qualified_name
        )

    @default_database_qualified_name.setter
    def default_database_qualified_name(
        self, default_database_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.default_database_qualified_name = (
            default_database_qualified_name
        )

    @property
    def variables_schema_base64(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.variables_schema_base64
        )

    @variables_schema_base64.setter
    def variables_schema_base64(self, variables_schema_base64: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.variables_schema_base64 = variables_schema_base64

    @property
    def is_private(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_private

    @is_private.setter
    def is_private(self, is_private: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_private = is_private

    @property
    def is_sql_snippet(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_sql_snippet

    @is_sql_snippet.setter
    def is_sql_snippet(self, is_sql_snippet: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_sql_snippet = is_sql_snippet

    @property
    def parent_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.parent_qualified_name
        )

    @parent_qualified_name.setter
    def parent_qualified_name(self, parent_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_qualified_name = parent_qualified_name

    @property
    def collection_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.collection_qualified_name
        )

    @collection_qualified_name.setter
    def collection_qualified_name(self, collection_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.collection_qualified_name = collection_qualified_name

    @property
    def is_visual_query(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_visual_query

    @is_visual_query.setter
    def is_visual_query(self, is_visual_query: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_visual_query = is_visual_query

    @property
    def visual_builder_schema_base64(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.visual_builder_schema_base64
        )

    @visual_builder_schema_base64.setter
    def visual_builder_schema_base64(self, visual_builder_schema_base64: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.visual_builder_schema_base64 = visual_builder_schema_base64

    @property
    def parent(self) -> Optional[Namespace]:
        return None if self.attributes is None else self.attributes.parent

    @parent.setter
    def parent(self, parent: Optional[Namespace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent = parent

    @property
    def columns(self) -> Optional[list[Column]]:
        return None if self.attributes is None else self.attributes.columns

    @columns.setter
    def columns(self, columns: Optional[list[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.columns = columns

    @property
    def tables(self) -> Optional[list[Table]]:
        return None if self.attributes is None else self.attributes.tables

    @tables.setter
    def tables(self, tables: Optional[list[Table]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tables = tables

    @property
    def views(self) -> Optional[list[View]]:
        return None if self.attributes is None else self.attributes.views

    @views.setter
    def views(self, views: Optional[list[View]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.views = views

    class Attributes(SQL.Attributes):
        raw_query: Optional[str] = Field(default=None, description="")
        long_raw_query: Optional[str] = Field(default=None, description="")
        raw_query_text: Optional[str] = Field(default=None, description="")
        default_schema_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        default_database_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        variables_schema_base64: Optional[str] = Field(default=None, description="")
        is_private: Optional[bool] = Field(default=None, description="")
        is_sql_snippet: Optional[bool] = Field(default=None, description="")
        parent_qualified_name: Optional[str] = Field(default=None, description="")
        collection_qualified_name: Optional[str] = Field(default=None, description="")
        is_visual_query: Optional[bool] = Field(default=None, description="")
        visual_builder_schema_base64: Optional[str] = Field(
            default=None, description=""
        )
        parent: Optional[Namespace] = Field(
            default=None, description=""
        )  # relationship
        columns: Optional[list[Column]] = Field(
            default=None, description=""
        )  # relationship
        tables: Optional[list[Table]] = Field(
            default=None, description=""
        )  # relationship
        views: Optional[list[View]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "Query.Attributes" = Field(
        default_factory=lambda: Query.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Schema(SQL):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(cls, *, name: str, database_qualified_name: str) -> Schema:
        validate_required_fields(
            ["name", "database_qualified_name"], [name, database_qualified_name]
        )
        attributes = Schema.Attributes.create(
            name=name, database_qualified_name=database_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="Schema", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Schema":
            raise ValueError("must be Schema")
        return v

    def __setattr__(self, name, value):
        if name in Schema._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    TABLE_COUNT: ClassVar[NumericField] = NumericField("tableCount", "tableCount")
    """
    Number of tables in this schema.
    """
    VIEWS_COUNT: ClassVar[NumericField] = NumericField("viewsCount", "viewsCount")
    """
    Number of views in this schema.
    """

    SNOWFLAKE_TAGS: ClassVar[RelationField] = RelationField("snowflakeTags")
    """
    TBC
    """
    FUNCTIONS: ClassVar[RelationField] = RelationField("functions")
    """
    TBC
    """
    TABLES: ClassVar[RelationField] = RelationField("tables")
    """
    TBC
    """
    DATABASE: ClassVar[RelationField] = RelationField("database")
    """
    TBC
    """
    PROCEDURES: ClassVar[RelationField] = RelationField("procedures")
    """
    TBC
    """
    VIEWS: ClassVar[RelationField] = RelationField("views")
    """
    TBC
    """
    MATERIALISED_VIEWS: ClassVar[RelationField] = RelationField("materialisedViews")
    """
    TBC
    """
    SNOWFLAKE_DYNAMIC_TABLES: ClassVar[RelationField] = RelationField(
        "snowflakeDynamicTables"
    )
    """
    TBC
    """
    SNOWFLAKE_PIPES: ClassVar[RelationField] = RelationField("snowflakePipes")
    """
    TBC
    """
    SNOWFLAKE_STREAMS: ClassVar[RelationField] = RelationField("snowflakeStreams")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "table_count",
        "views_count",
        "snowflake_tags",
        "functions",
        "tables",
        "database",
        "procedures",
        "views",
        "materialised_views",
        "snowflake_dynamic_tables",
        "snowflake_pipes",
        "snowflake_streams",
    ]

    @property
    def table_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.table_count

    @table_count.setter
    def table_count(self, table_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_count = table_count

    @property
    def views_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.views_count

    @views_count.setter
    def views_count(self, views_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.views_count = views_count

    @property
    def snowflake_tags(self) -> Optional[list[SnowflakeTag]]:
        return None if self.attributes is None else self.attributes.snowflake_tags

    @snowflake_tags.setter
    def snowflake_tags(self, snowflake_tags: Optional[list[SnowflakeTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_tags = snowflake_tags

    @property
    def functions(self) -> Optional[list[Function]]:
        return None if self.attributes is None else self.attributes.functions

    @functions.setter
    def functions(self, functions: Optional[list[Function]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.functions = functions

    @property
    def tables(self) -> Optional[list[Table]]:
        return None if self.attributes is None else self.attributes.tables

    @tables.setter
    def tables(self, tables: Optional[list[Table]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tables = tables

    @property
    def database(self) -> Optional[Database]:
        return None if self.attributes is None else self.attributes.database

    @database.setter
    def database(self, database: Optional[Database]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database = database

    @property
    def procedures(self) -> Optional[list[Procedure]]:
        return None if self.attributes is None else self.attributes.procedures

    @procedures.setter
    def procedures(self, procedures: Optional[list[Procedure]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.procedures = procedures

    @property
    def views(self) -> Optional[list[View]]:
        return None if self.attributes is None else self.attributes.views

    @views.setter
    def views(self, views: Optional[list[View]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.views = views

    @property
    def materialised_views(self) -> Optional[list[MaterialisedView]]:
        return None if self.attributes is None else self.attributes.materialised_views

    @materialised_views.setter
    def materialised_views(self, materialised_views: Optional[list[MaterialisedView]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.materialised_views = materialised_views

    @property
    def snowflake_dynamic_tables(self) -> Optional[list[SnowflakeDynamicTable]]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_dynamic_tables
        )

    @snowflake_dynamic_tables.setter
    def snowflake_dynamic_tables(
        self, snowflake_dynamic_tables: Optional[list[SnowflakeDynamicTable]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_dynamic_tables = snowflake_dynamic_tables

    @property
    def snowflake_pipes(self) -> Optional[list[SnowflakePipe]]:
        return None if self.attributes is None else self.attributes.snowflake_pipes

    @snowflake_pipes.setter
    def snowflake_pipes(self, snowflake_pipes: Optional[list[SnowflakePipe]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_pipes = snowflake_pipes

    @property
    def snowflake_streams(self) -> Optional[list[SnowflakeStream]]:
        return None if self.attributes is None else self.attributes.snowflake_streams

    @snowflake_streams.setter
    def snowflake_streams(self, snowflake_streams: Optional[list[SnowflakeStream]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_streams = snowflake_streams

    class Attributes(SQL.Attributes):
        table_count: Optional[int] = Field(default=None, description="")
        views_count: Optional[int] = Field(default=None, description="")
        snowflake_tags: Optional[list[SnowflakeTag]] = Field(
            default=None, description=""
        )  # relationship
        functions: Optional[list[Function]] = Field(
            default=None, description=""
        )  # relationship
        tables: Optional[list[Table]] = Field(
            default=None, description=""
        )  # relationship
        database: Optional[Database] = Field(
            default=None, description=""
        )  # relationship
        procedures: Optional[list[Procedure]] = Field(
            default=None, description=""
        )  # relationship
        views: Optional[list[View]] = Field(
            default=None, description=""
        )  # relationship
        materialised_views: Optional[list[MaterialisedView]] = Field(
            default=None, description=""
        )  # relationship
        snowflake_dynamic_tables: Optional[list[SnowflakeDynamicTable]] = Field(
            default=None, description=""
        )  # relationship
        snowflake_pipes: Optional[list[SnowflakePipe]] = Field(
            default=None, description=""
        )  # relationship
        snowflake_streams: Optional[list[SnowflakeStream]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, *, name: str, database_qualified_name: str
        ) -> Schema.Attributes:
            if not name:
                raise ValueError("name cannot be blank")
            validate_required_fields(
                ["database_qualified_name"], [database_qualified_name]
            )
            fields = database_qualified_name.split("/")
            if len(fields) != 4:
                raise ValueError("Invalid database_qualified_name")
            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid database_qualified_name") from e
            return Schema.Attributes(
                name=name,
                database_name=fields[3],
                connection_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}",
                database_qualified_name=database_qualified_name,
                qualified_name=f"{database_qualified_name}/{name}",
                connector_name=connector_type.value,
                database=Database.ref_by_qualified_name(database_qualified_name),
            )

    attributes: "Schema.Attributes" = Field(
        default_factory=lambda: Schema.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SnowflakePipe(SQL):
    """Description"""

    type_name: str = Field(default="SnowflakePipe", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakePipe":
            raise ValueError("must be SnowflakePipe")
        return v

    def __setattr__(self, name, value):
        if name in SnowflakePipe._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DEFINITION: ClassVar[KeywordField] = KeywordField("definition", "definition")
    """
    SQL definition of this pipe.
    """
    SNOWFLAKE_PIPE_IS_AUTO_INGEST_ENABLED: ClassVar[BooleanField] = BooleanField(
        "snowflakePipeIsAutoIngestEnabled", "snowflakePipeIsAutoIngestEnabled"
    )
    """
    Whether auto-ingest is enabled for this pipe (true) or not (false).
    """
    SNOWFLAKE_PIPE_NOTIFICATION_CHANNEL_NAME: ClassVar[
        KeywordTextField
    ] = KeywordTextField(
        "snowflakePipeNotificationChannelName",
        "snowflakePipeNotificationChannelName",
        "snowflakePipeNotificationChannelName.text",
    )
    """
    Name of the notification channel for this pipe.
    """

    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "definition",
        "snowflake_pipe_is_auto_ingest_enabled",
        "snowflake_pipe_notification_channel_name",
        "atlan_schema",
    ]

    @property
    def definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.definition

    @definition.setter
    def definition(self, definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.definition = definition

    @property
    def snowflake_pipe_is_auto_ingest_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_pipe_is_auto_ingest_enabled
        )

    @snowflake_pipe_is_auto_ingest_enabled.setter
    def snowflake_pipe_is_auto_ingest_enabled(
        self, snowflake_pipe_is_auto_ingest_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_pipe_is_auto_ingest_enabled = (
            snowflake_pipe_is_auto_ingest_enabled
        )

    @property
    def snowflake_pipe_notification_channel_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_pipe_notification_channel_name
        )

    @snowflake_pipe_notification_channel_name.setter
    def snowflake_pipe_notification_channel_name(
        self, snowflake_pipe_notification_channel_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_pipe_notification_channel_name = (
            snowflake_pipe_notification_channel_name
        )

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    class Attributes(SQL.Attributes):
        definition: Optional[str] = Field(default=None, description="")
        snowflake_pipe_is_auto_ingest_enabled: Optional[bool] = Field(
            default=None, description=""
        )
        snowflake_pipe_notification_channel_name: Optional[str] = Field(
            default=None, description=""
        )
        atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship

    attributes: "SnowflakePipe.Attributes" = Field(
        default_factory=lambda: SnowflakePipe.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class View(SQL):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(cls, *, name: str, schema_qualified_name: str) -> View:
        validate_required_fields(
            ["name", "schema_qualified_name"], [name, schema_qualified_name]
        )
        attributes = View.Attributes.create(
            name=name, schema_qualified_name=schema_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="View", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "View":
            raise ValueError("must be View")
        return v

    def __setattr__(self, name, value):
        if name in View._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COLUMN_COUNT: ClassVar[NumericField] = NumericField("columnCount", "columnCount")
    """
    Number of columns in this view.
    """
    ROW_COUNT: ClassVar[NumericField] = NumericField("rowCount", "rowCount")
    """
    Number of rows in this view.
    """
    SIZE_BYTES: ClassVar[NumericField] = NumericField("sizeBytes", "sizeBytes")
    """
    Size of this view, in bytes.
    """
    IS_QUERY_PREVIEW: ClassVar[BooleanField] = BooleanField(
        "isQueryPreview", "isQueryPreview"
    )
    """
    Whether preview queries are allowed on this view (true) or not (false).
    """
    QUERY_PREVIEW_CONFIG: ClassVar[KeywordField] = KeywordField(
        "queryPreviewConfig", "queryPreviewConfig"
    )
    """
    Configuration for preview queries on this view.
    """
    ALIAS: ClassVar[KeywordField] = KeywordField("alias", "alias")
    """
    Alias for this view.
    """
    IS_TEMPORARY: ClassVar[BooleanField] = BooleanField("isTemporary", "isTemporary")
    """
    Whether this view is temporary (true) or not (false).
    """
    DEFINITION: ClassVar[KeywordField] = KeywordField("definition", "definition")
    """
    SQL definition of this view.
    """

    COLUMNS: ClassVar[RelationField] = RelationField("columns")
    """
    TBC
    """
    QUERIES: ClassVar[RelationField] = RelationField("queries")
    """
    TBC
    """
    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "column_count",
        "row_count",
        "size_bytes",
        "is_query_preview",
        "query_preview_config",
        "alias",
        "is_temporary",
        "definition",
        "columns",
        "queries",
        "atlan_schema",
    ]

    @property
    def column_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.column_count

    @column_count.setter
    def column_count(self, column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_count = column_count

    @property
    def row_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.row_count

    @row_count.setter
    def row_count(self, row_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.row_count = row_count

    @property
    def size_bytes(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.size_bytes

    @size_bytes.setter
    def size_bytes(self, size_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.size_bytes = size_bytes

    @property
    def is_query_preview(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_query_preview

    @is_query_preview.setter
    def is_query_preview(self, is_query_preview: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_query_preview = is_query_preview

    @property
    def query_preview_config(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.query_preview_config

    @query_preview_config.setter
    def query_preview_config(self, query_preview_config: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_preview_config = query_preview_config

    @property
    def alias(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.alias

    @alias.setter
    def alias(self, alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alias = alias

    @property
    def is_temporary(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_temporary

    @is_temporary.setter
    def is_temporary(self, is_temporary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_temporary = is_temporary

    @property
    def definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.definition

    @definition.setter
    def definition(self, definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.definition = definition

    @property
    def columns(self) -> Optional[list[Column]]:
        return None if self.attributes is None else self.attributes.columns

    @columns.setter
    def columns(self, columns: Optional[list[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.columns = columns

    @property
    def queries(self) -> Optional[list[Query]]:
        return None if self.attributes is None else self.attributes.queries

    @queries.setter
    def queries(self, queries: Optional[list[Query]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.queries = queries

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    class Attributes(SQL.Attributes):
        column_count: Optional[int] = Field(default=None, description="")
        row_count: Optional[int] = Field(default=None, description="")
        size_bytes: Optional[int] = Field(default=None, description="")
        is_query_preview: Optional[bool] = Field(default=None, description="")
        query_preview_config: Optional[dict[str, str]] = Field(
            default=None, description=""
        )
        alias: Optional[str] = Field(default=None, description="")
        is_temporary: Optional[bool] = Field(default=None, description="")
        definition: Optional[str] = Field(default=None, description="")
        columns: Optional[list[Column]] = Field(
            default=None, description=""
        )  # relationship
        queries: Optional[list[Query]] = Field(
            default=None, description=""
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(cls, *, name: str, schema_qualified_name: str) -> View.Attributes:
            if not name:
                raise ValueError("name cannot be blank")
            validate_required_fields(["schema_qualified_name"], [schema_qualified_name])
            fields = schema_qualified_name.split("/")
            if len(fields) != 5:
                raise ValueError("Invalid schema_qualified_name")
            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid schema_qualified_name") from e
            return View.Attributes(
                name=name,
                database_name=fields[3],
                connection_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}",
                database_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}/{fields[3]}",
                qualified_name=f"{schema_qualified_name}/{name}",
                schema_qualified_name=schema_qualified_name,
                schema_name=fields[4],
                connector_name=connector_type.value,
                atlan_schema=Schema.ref_by_qualified_name(schema_qualified_name),
            )

    attributes: "View.Attributes" = Field(
        default_factory=lambda: View.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MaterialisedView(SQL):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(cls, *, name: str, schema_qualified_name: str) -> MaterialisedView:
        validate_required_fields(
            ["name", "schema_qualified_name"], [name, schema_qualified_name]
        )
        attributes = MaterialisedView.Attributes.create(
            name=name, schema_qualified_name=schema_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="MaterialisedView", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MaterialisedView":
            raise ValueError("must be MaterialisedView")
        return v

    def __setattr__(self, name, value):
        if name in MaterialisedView._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    REFRESH_MODE: ClassVar[KeywordField] = KeywordField("refreshMode", "refreshMode")
    """
    Refresh mode for this materialized view.
    """
    REFRESH_METHOD: ClassVar[KeywordField] = KeywordField(
        "refreshMethod", "refreshMethod"
    )
    """
    Refresh method for this materialized view.
    """
    STALENESS: ClassVar[KeywordField] = KeywordField("staleness", "staleness")
    """
    Staleness of this materialized view.
    """
    STALE_SINCE_DATE: ClassVar[NumericField] = NumericField(
        "staleSinceDate", "staleSinceDate"
    )
    """
    Time (epoch) from which this materialized view is stale, in milliseconds.
    """
    COLUMN_COUNT: ClassVar[NumericField] = NumericField("columnCount", "columnCount")
    """
    Number of columns in this materialized view.
    """
    ROW_COUNT: ClassVar[NumericField] = NumericField("rowCount", "rowCount")
    """
    Number of rows in this materialized view.
    """
    SIZE_BYTES: ClassVar[NumericField] = NumericField("sizeBytes", "sizeBytes")
    """
    Size of this materialized view, in bytes.
    """
    IS_QUERY_PREVIEW: ClassVar[BooleanField] = BooleanField(
        "isQueryPreview", "isQueryPreview"
    )
    """
    Whether it's possible to run a preview query on this materialized view (true) or not (false).
    """
    QUERY_PREVIEW_CONFIG: ClassVar[KeywordField] = KeywordField(
        "queryPreviewConfig", "queryPreviewConfig"
    )
    """
    Configuration for the query preview of this materialized view.
    """
    ALIAS: ClassVar[KeywordField] = KeywordField("alias", "alias")
    """
    Alias for this materialized view.
    """
    IS_TEMPORARY: ClassVar[BooleanField] = BooleanField("isTemporary", "isTemporary")
    """
    Whether this materialized view is temporary (true) or not (false).
    """
    DEFINITION: ClassVar[KeywordField] = KeywordField("definition", "definition")
    """
    SQL definition of this materialized view.
    """

    COLUMNS: ClassVar[RelationField] = RelationField("columns")
    """
    TBC
    """
    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "refresh_mode",
        "refresh_method",
        "staleness",
        "stale_since_date",
        "column_count",
        "row_count",
        "size_bytes",
        "is_query_preview",
        "query_preview_config",
        "alias",
        "is_temporary",
        "definition",
        "columns",
        "atlan_schema",
    ]

    @property
    def refresh_mode(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.refresh_mode

    @refresh_mode.setter
    def refresh_mode(self, refresh_mode: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.refresh_mode = refresh_mode

    @property
    def refresh_method(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.refresh_method

    @refresh_method.setter
    def refresh_method(self, refresh_method: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.refresh_method = refresh_method

    @property
    def staleness(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.staleness

    @staleness.setter
    def staleness(self, staleness: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.staleness = staleness

    @property
    def stale_since_date(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.stale_since_date

    @stale_since_date.setter
    def stale_since_date(self, stale_since_date: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.stale_since_date = stale_since_date

    @property
    def column_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.column_count

    @column_count.setter
    def column_count(self, column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_count = column_count

    @property
    def row_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.row_count

    @row_count.setter
    def row_count(self, row_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.row_count = row_count

    @property
    def size_bytes(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.size_bytes

    @size_bytes.setter
    def size_bytes(self, size_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.size_bytes = size_bytes

    @property
    def is_query_preview(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_query_preview

    @is_query_preview.setter
    def is_query_preview(self, is_query_preview: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_query_preview = is_query_preview

    @property
    def query_preview_config(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.query_preview_config

    @query_preview_config.setter
    def query_preview_config(self, query_preview_config: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_preview_config = query_preview_config

    @property
    def alias(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.alias

    @alias.setter
    def alias(self, alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alias = alias

    @property
    def is_temporary(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_temporary

    @is_temporary.setter
    def is_temporary(self, is_temporary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_temporary = is_temporary

    @property
    def definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.definition

    @definition.setter
    def definition(self, definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.definition = definition

    @property
    def columns(self) -> Optional[list[Column]]:
        return None if self.attributes is None else self.attributes.columns

    @columns.setter
    def columns(self, columns: Optional[list[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.columns = columns

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    class Attributes(SQL.Attributes):
        refresh_mode: Optional[str] = Field(default=None, description="")
        refresh_method: Optional[str] = Field(default=None, description="")
        staleness: Optional[str] = Field(default=None, description="")
        stale_since_date: Optional[datetime] = Field(default=None, description="")
        column_count: Optional[int] = Field(default=None, description="")
        row_count: Optional[int] = Field(default=None, description="")
        size_bytes: Optional[int] = Field(default=None, description="")
        is_query_preview: Optional[bool] = Field(default=None, description="")
        query_preview_config: Optional[dict[str, str]] = Field(
            default=None, description=""
        )
        alias: Optional[str] = Field(default=None, description="")
        is_temporary: Optional[bool] = Field(default=None, description="")
        definition: Optional[str] = Field(default=None, description="")
        columns: Optional[list[Column]] = Field(
            default=None, description=""
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, *, name: str, schema_qualified_name: str
        ) -> MaterialisedView.Attributes:
            if not name:
                raise ValueError("name cannot be blank")
            validate_required_fields(["schema_qualified_name"], [schema_qualified_name])
            fields = schema_qualified_name.split("/")
            if len(fields) != 5:
                raise ValueError("Invalid schema_qualified_name")
            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid schema_qualified_name") from e
            return MaterialisedView.Attributes(
                name=name,
                database_name=fields[3],
                connection_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}",
                database_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}/{fields[3]}",
                qualified_name=f"{schema_qualified_name}/{name}",
                schema_qualified_name=schema_qualified_name,
                schema_name=fields[4],
                connector_name=connector_type.value,
                atlan_schema=Schema.ref_by_qualified_name(schema_qualified_name),
            )

    attributes: "MaterialisedView.Attributes" = Field(
        default_factory=lambda: MaterialisedView.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Function(SQL):
    """Description"""

    type_name: str = Field(default="Function", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Function":
            raise ValueError("must be Function")
        return v

    def __setattr__(self, name, value):
        if name in Function._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FUNCTION_DEFINITION: ClassVar[KeywordField] = KeywordField(
        "functionDefinition", "functionDefinition"
    )
    """
    Code or set of statements that determine the output of the function.
    """
    FUNCTION_RETURN_TYPE: ClassVar[KeywordField] = KeywordField(
        "functionReturnType", "functionReturnType"
    )
    """
    Data type of the value returned by the function.
    """
    FUNCTION_ARGUMENTS: ClassVar[KeywordField] = KeywordField(
        "functionArguments", "functionArguments"
    )
    """
    Arguments that are passed in to the function.
    """
    FUNCTION_LANGUAGE: ClassVar[KeywordField] = KeywordField(
        "functionLanguage", "functionLanguage"
    )
    """
    Programming language in which the function is written.
    """
    FUNCTION_TYPE: ClassVar[KeywordField] = KeywordField("functionType", "functionType")
    """
    Type of function.
    """
    FUNCTION_IS_EXTERNAL: ClassVar[BooleanField] = BooleanField(
        "functionIsExternal", "functionIsExternal"
    )
    """
    Whether the function is stored or executed externally (true) or internally (false).
    """
    FUNCTION_IS_SECURE: ClassVar[BooleanField] = BooleanField(
        "functionIsSecure", "functionIsSecure"
    )
    """
    Whether sensitive information of the function is omitted for unauthorized users (true) or not (false).
    """
    FUNCTION_IS_MEMOIZABLE: ClassVar[BooleanField] = BooleanField(
        "functionIsMemoizable", "functionIsMemoizable"
    )
    """
    Whether the function must re-compute if there are no underlying changes in the values (false) or not (true).
    """

    FUNCTION_SCHEMA: ClassVar[RelationField] = RelationField("functionSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "function_definition",
        "function_return_type",
        "function_arguments",
        "function_language",
        "function_type",
        "function_is_external",
        "function_is_secure",
        "function_is_memoizable",
        "function_schema",
    ]

    @property
    def function_definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.function_definition

    @function_definition.setter
    def function_definition(self, function_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_definition = function_definition

    @property
    def function_return_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.function_return_type

    @function_return_type.setter
    def function_return_type(self, function_return_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_return_type = function_return_type

    @property
    def function_arguments(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.function_arguments

    @function_arguments.setter
    def function_arguments(self, function_arguments: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_arguments = function_arguments

    @property
    def function_language(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.function_language

    @function_language.setter
    def function_language(self, function_language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_language = function_language

    @property
    def function_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.function_type

    @function_type.setter
    def function_type(self, function_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_type = function_type

    @property
    def function_is_external(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.function_is_external

    @function_is_external.setter
    def function_is_external(self, function_is_external: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_is_external = function_is_external

    @property
    def function_is_secure(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.function_is_secure

    @function_is_secure.setter
    def function_is_secure(self, function_is_secure: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_is_secure = function_is_secure

    @property
    def function_is_memoizable(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.function_is_memoizable
        )

    @function_is_memoizable.setter
    def function_is_memoizable(self, function_is_memoizable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_is_memoizable = function_is_memoizable

    @property
    def function_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.function_schema

    @function_schema.setter
    def function_schema(self, function_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_schema = function_schema

    class Attributes(SQL.Attributes):
        function_definition: Optional[str] = Field(default=None, description="")
        function_return_type: Optional[str] = Field(default=None, description="")
        function_arguments: Optional[set[str]] = Field(default=None, description="")
        function_language: Optional[str] = Field(default=None, description="")
        function_type: Optional[str] = Field(default=None, description="")
        function_is_external: Optional[bool] = Field(default=None, description="")
        function_is_secure: Optional[bool] = Field(default=None, description="")
        function_is_memoizable: Optional[bool] = Field(default=None, description="")
        function_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship

    attributes: "Function.Attributes" = Field(
        default_factory=lambda: Function.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TablePartition(SQL):
    """Description"""

    type_name: str = Field(default="TablePartition", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TablePartition":
            raise ValueError("must be TablePartition")
        return v

    def __setattr__(self, name, value):
        if name in TablePartition._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CONSTRAINT: ClassVar[KeywordField] = KeywordField("constraint", "constraint")
    """
    Constraint that defines this table partition.
    """
    COLUMN_COUNT: ClassVar[NumericField] = NumericField("columnCount", "columnCount")
    """
    Number of columns in this partition.
    """
    ROW_COUNT: ClassVar[NumericField] = NumericField("rowCount", "rowCount")
    """
    Number of rows in this partition.
    """
    SIZE_BYTES: ClassVar[NumericField] = NumericField("sizeBytes", "sizeBytes")
    """
    Size of this partition, in bytes.
    """
    ALIAS: ClassVar[KeywordField] = KeywordField("alias", "alias")
    """
    Alias for this partition.
    """
    IS_TEMPORARY: ClassVar[BooleanField] = BooleanField("isTemporary", "isTemporary")
    """
    Whether this partition is temporary (true) or not (false).
    """
    IS_QUERY_PREVIEW: ClassVar[BooleanField] = BooleanField(
        "isQueryPreview", "isQueryPreview"
    )
    """
    Whether preview queries for this partition are allowed (true) or not (false).
    """
    QUERY_PREVIEW_CONFIG: ClassVar[KeywordField] = KeywordField(
        "queryPreviewConfig", "queryPreviewConfig"
    )
    """
    Configuration for the preview queries.
    """
    EXTERNAL_LOCATION: ClassVar[KeywordField] = KeywordField(
        "externalLocation", "externalLocation"
    )
    """
    External location of this partition, for example: an S3 object location.
    """
    EXTERNAL_LOCATION_REGION: ClassVar[KeywordField] = KeywordField(
        "externalLocationRegion", "externalLocationRegion"
    )
    """
    Region of the external location of this partition, for example: S3 region.
    """
    EXTERNAL_LOCATION_FORMAT: ClassVar[KeywordField] = KeywordField(
        "externalLocationFormat", "externalLocationFormat"
    )
    """
    Format of the external location of this partition, for example: JSON, CSV, PARQUET, etc.
    """
    IS_PARTITIONED: ClassVar[BooleanField] = BooleanField(
        "isPartitioned", "isPartitioned"
    )
    """
    Whether this partition is further partitioned (true) or not (false).
    """
    PARTITION_STRATEGY: ClassVar[KeywordField] = KeywordField(
        "partitionStrategy", "partitionStrategy"
    )
    """
    Partition strategy of this partition.
    """
    PARTITION_COUNT: ClassVar[NumericField] = NumericField(
        "partitionCount", "partitionCount"
    )
    """
    Number of sub-partitions of this partition.
    """
    PARTITION_LIST: ClassVar[KeywordField] = KeywordField(
        "partitionList", "partitionList"
    )
    """
    List of sub-partitions in this partition.
    """

    CHILD_TABLE_PARTITIONS: ClassVar[RelationField] = RelationField(
        "childTablePartitions"
    )
    """
    TBC
    """
    COLUMNS: ClassVar[RelationField] = RelationField("columns")
    """
    TBC
    """
    PARENT_TABLE_PARTITION: ClassVar[RelationField] = RelationField(
        "parentTablePartition"
    )
    """
    TBC
    """
    PARENT_TABLE: ClassVar[RelationField] = RelationField("parentTable")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "constraint",
        "column_count",
        "row_count",
        "size_bytes",
        "alias",
        "is_temporary",
        "is_query_preview",
        "query_preview_config",
        "external_location",
        "external_location_region",
        "external_location_format",
        "is_partitioned",
        "partition_strategy",
        "partition_count",
        "partition_list",
        "child_table_partitions",
        "columns",
        "parent_table_partition",
        "parent_table",
    ]

    @property
    def constraint(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.constraint

    @constraint.setter
    def constraint(self, constraint: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.constraint = constraint

    @property
    def column_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.column_count

    @column_count.setter
    def column_count(self, column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_count = column_count

    @property
    def row_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.row_count

    @row_count.setter
    def row_count(self, row_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.row_count = row_count

    @property
    def size_bytes(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.size_bytes

    @size_bytes.setter
    def size_bytes(self, size_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.size_bytes = size_bytes

    @property
    def alias(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.alias

    @alias.setter
    def alias(self, alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alias = alias

    @property
    def is_temporary(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_temporary

    @is_temporary.setter
    def is_temporary(self, is_temporary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_temporary = is_temporary

    @property
    def is_query_preview(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_query_preview

    @is_query_preview.setter
    def is_query_preview(self, is_query_preview: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_query_preview = is_query_preview

    @property
    def query_preview_config(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.query_preview_config

    @query_preview_config.setter
    def query_preview_config(self, query_preview_config: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_preview_config = query_preview_config

    @property
    def external_location(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.external_location

    @external_location.setter
    def external_location(self, external_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location = external_location

    @property
    def external_location_region(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.external_location_region
        )

    @external_location_region.setter
    def external_location_region(self, external_location_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location_region = external_location_region

    @property
    def external_location_format(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.external_location_format
        )

    @external_location_format.setter
    def external_location_format(self, external_location_format: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location_format = external_location_format

    @property
    def is_partitioned(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_partitioned

    @is_partitioned.setter
    def is_partitioned(self, is_partitioned: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_partitioned = is_partitioned

    @property
    def partition_strategy(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.partition_strategy

    @partition_strategy.setter
    def partition_strategy(self, partition_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_strategy = partition_strategy

    @property
    def partition_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.partition_count

    @partition_count.setter
    def partition_count(self, partition_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_count = partition_count

    @property
    def partition_list(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.partition_list

    @partition_list.setter
    def partition_list(self, partition_list: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_list = partition_list

    @property
    def child_table_partitions(self) -> Optional[list[TablePartition]]:
        return (
            None if self.attributes is None else self.attributes.child_table_partitions
        )

    @child_table_partitions.setter
    def child_table_partitions(
        self, child_table_partitions: Optional[list[TablePartition]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.child_table_partitions = child_table_partitions

    @property
    def columns(self) -> Optional[list[Column]]:
        return None if self.attributes is None else self.attributes.columns

    @columns.setter
    def columns(self, columns: Optional[list[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.columns = columns

    @property
    def parent_table_partition(self) -> Optional[TablePartition]:
        return (
            None if self.attributes is None else self.attributes.parent_table_partition
        )

    @parent_table_partition.setter
    def parent_table_partition(self, parent_table_partition: Optional[TablePartition]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_table_partition = parent_table_partition

    @property
    def parent_table(self) -> Optional[Table]:
        return None if self.attributes is None else self.attributes.parent_table

    @parent_table.setter
    def parent_table(self, parent_table: Optional[Table]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_table = parent_table

    class Attributes(SQL.Attributes):
        constraint: Optional[str] = Field(default=None, description="")
        column_count: Optional[int] = Field(default=None, description="")
        row_count: Optional[int] = Field(default=None, description="")
        size_bytes: Optional[int] = Field(default=None, description="")
        alias: Optional[str] = Field(default=None, description="")
        is_temporary: Optional[bool] = Field(default=None, description="")
        is_query_preview: Optional[bool] = Field(default=None, description="")
        query_preview_config: Optional[dict[str, str]] = Field(
            default=None, description=""
        )
        external_location: Optional[str] = Field(default=None, description="")
        external_location_region: Optional[str] = Field(default=None, description="")
        external_location_format: Optional[str] = Field(default=None, description="")
        is_partitioned: Optional[bool] = Field(default=None, description="")
        partition_strategy: Optional[str] = Field(default=None, description="")
        partition_count: Optional[int] = Field(default=None, description="")
        partition_list: Optional[str] = Field(default=None, description="")
        child_table_partitions: Optional[list[TablePartition]] = Field(
            default=None, description=""
        )  # relationship
        columns: Optional[list[Column]] = Field(
            default=None, description=""
        )  # relationship
        parent_table_partition: Optional[TablePartition] = Field(
            default=None, description=""
        )  # relationship
        parent_table: Optional[Table] = Field(
            default=None, description=""
        )  # relationship

    attributes: "TablePartition.Attributes" = Field(
        default_factory=lambda: TablePartition.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Column(SQL):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(
        cls, *, name: str, parent_qualified_name: str, parent_type: type, order: int
    ) -> Column:
        return Column(
            attributes=Column.Attributes.create(
                name=name,
                parent_qualified_name=parent_qualified_name,
                parent_type=parent_type,
                order=order,
            )
        )

    type_name: str = Field(default="Column", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Column":
            raise ValueError("must be Column")
        return v

    def __setattr__(self, name, value):
        if name in Column._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "dataType", "dataType", "dataType.text"
    )
    """
    Data type of values in this column.
    """
    SUB_DATA_TYPE: ClassVar[KeywordField] = KeywordField("subDataType", "subDataType")
    """
    Sub-data type of this column.
    """
    RAW_DATA_TYPE_DEFINITION: ClassVar[KeywordField] = KeywordField(
        "rawDataTypeDefinition", "rawDataTypeDefinition"
    )
    """

    """
    ORDER: ClassVar[NumericField] = NumericField("order", "order")
    """
    Order (position) in which this column appears in the table (starting at 1).
    """
    NESTED_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "nestedColumnCount", "nestedColumnCount"
    )
    """
    Number of columns nested within this (STRUCT or NESTED) column.
    """
    IS_PARTITION: ClassVar[BooleanField] = BooleanField("isPartition", "isPartition")
    """
    Whether this column is a partition column (true) or not (false).
    """
    PARTITION_ORDER: ClassVar[NumericField] = NumericField(
        "partitionOrder", "partitionOrder"
    )
    """
    Order (position) of this partition column in the table.
    """
    IS_CLUSTERED: ClassVar[BooleanField] = BooleanField("isClustered", "isClustered")
    """
    Whether this column is a clustered column (true) or not (false).
    """
    IS_PRIMARY: ClassVar[BooleanField] = BooleanField("isPrimary", "isPrimary")
    """
    When true, this column is the primary key for the table.
    """
    IS_FOREIGN: ClassVar[BooleanField] = BooleanField("isForeign", "isForeign")
    """
    When true, this column is a foreign key to another table. NOTE: this must be true when using the foreignKeyTo relationship to specify columns that refer to this column as a foreign key.
    """  # noqa: E501
    IS_INDEXED: ClassVar[BooleanField] = BooleanField("isIndexed", "isIndexed")
    """
    When true, this column is indexed in the database.
    """
    IS_SORT: ClassVar[BooleanField] = BooleanField("isSort", "isSort")
    """
    Whether this column is a sort column (true) or not (false).
    """
    IS_DIST: ClassVar[BooleanField] = BooleanField("isDist", "isDist")
    """
    Whether this column is a distribution column (true) or not (false).
    """
    IS_PINNED: ClassVar[BooleanField] = BooleanField("isPinned", "isPinned")
    """
    Whether this column is pinned (true) or not (false).
    """
    PINNED_BY: ClassVar[KeywordField] = KeywordField("pinnedBy", "pinnedBy")
    """
    User who pinned this column.
    """
    PINNED_AT: ClassVar[NumericField] = NumericField("pinnedAt", "pinnedAt")
    """
    Time (epoch) at which this column was pinned, in milliseconds.
    """
    PRECISION: ClassVar[NumericField] = NumericField("precision", "precision")
    """
    Total number of digits allowed, when the dataType is numeric.
    """
    DEFAULT_VALUE: ClassVar[KeywordField] = KeywordField("defaultValue", "defaultValue")
    """
    Default value for this column.
    """
    IS_NULLABLE: ClassVar[BooleanField] = BooleanField("isNullable", "isNullable")
    """
    When true, the values in this column can be null.
    """
    NUMERIC_SCALE: ClassVar[NumericField] = NumericField("numericScale", "numericScale")
    """
    Number of digits allowed to the right of the decimal point.
    """
    MAX_LENGTH: ClassVar[NumericField] = NumericField("maxLength", "maxLength")
    """
    Maximum length of a value in this column.
    """
    VALIDATIONS: ClassVar[KeywordField] = KeywordField("validations", "validations")
    """
    Validations for this column.
    """
    PARENT_COLUMN_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "parentColumnQualifiedName",
        "parentColumnQualifiedName",
        "parentColumnQualifiedName.text",
    )
    """
    Unique name of the column this column is nested within, for STRUCT and NESTED columns.
    """
    PARENT_COLUMN_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "parentColumnName", "parentColumnName.keyword", "parentColumnName"
    )
    """
    Simple name of the column this column is nested within, for STRUCT and NESTED columns.
    """
    COLUMN_DISTINCT_VALUES_COUNT: ClassVar[NumericField] = NumericField(
        "columnDistinctValuesCount", "columnDistinctValuesCount"
    )
    """
    Number of rows that contain distinct values.
    """
    COLUMN_DISTINCT_VALUES_COUNT_LONG: ClassVar[NumericField] = NumericField(
        "columnDistinctValuesCountLong", "columnDistinctValuesCountLong"
    )
    """
    Number of rows that contain distinct values.
    """
    COLUMN_HISTOGRAM: ClassVar[KeywordField] = KeywordField(
        "columnHistogram", "columnHistogram"
    )
    """
    List of values in a histogram that represents the contents of this column.
    """
    COLUMN_MAX: ClassVar[NumericField] = NumericField("columnMax", "columnMax")
    """
    Greatest value in a numeric column.
    """
    COLUMN_MIN: ClassVar[NumericField] = NumericField("columnMin", "columnMin")
    """
    Least value in a numeric column.
    """
    COLUMN_MEAN: ClassVar[NumericField] = NumericField("columnMean", "columnMean")
    """
    Arithmetic mean of the values in a numeric column.
    """
    COLUMN_SUM: ClassVar[NumericField] = NumericField("columnSum", "columnSum")
    """
    Calculated sum of the values in a numeric column.
    """
    COLUMN_MEDIAN: ClassVar[NumericField] = NumericField("columnMedian", "columnMedian")
    """
    Calculated median of the values in a numeric column.
    """
    COLUMN_STANDARD_DEVIATION: ClassVar[NumericField] = NumericField(
        "columnStandardDeviation", "columnStandardDeviation"
    )
    """
    Calculated standard deviation of the values in a numeric column.
    """
    COLUMN_UNIQUE_VALUES_COUNT: ClassVar[NumericField] = NumericField(
        "columnUniqueValuesCount", "columnUniqueValuesCount"
    )
    """
    Number of rows in which a value in this column appears only once.
    """
    COLUMN_UNIQUE_VALUES_COUNT_LONG: ClassVar[NumericField] = NumericField(
        "columnUniqueValuesCountLong", "columnUniqueValuesCountLong"
    )
    """
    Number of rows in which a value in this column appears only once.
    """
    COLUMN_AVERAGE: ClassVar[NumericField] = NumericField(
        "columnAverage", "columnAverage"
    )
    """
    Average value in this column.
    """
    COLUMN_AVERAGE_LENGTH: ClassVar[NumericField] = NumericField(
        "columnAverageLength", "columnAverageLength"
    )
    """
    Average length of values in a string column.
    """
    COLUMN_DUPLICATE_VALUES_COUNT: ClassVar[NumericField] = NumericField(
        "columnDuplicateValuesCount", "columnDuplicateValuesCount"
    )
    """
    Number of rows that contain duplicate values.
    """
    COLUMN_DUPLICATE_VALUES_COUNT_LONG: ClassVar[NumericField] = NumericField(
        "columnDuplicateValuesCountLong", "columnDuplicateValuesCountLong"
    )
    """
    Number of rows that contain duplicate values.
    """
    COLUMN_MAXIMUM_STRING_LENGTH: ClassVar[NumericField] = NumericField(
        "columnMaximumStringLength", "columnMaximumStringLength"
    )
    """
    Length of the longest value in a string column.
    """
    COLUMN_MAXS: ClassVar[KeywordField] = KeywordField("columnMaxs", "columnMaxs")
    """
    List of the greatest values in a column.
    """
    COLUMN_MINIMUM_STRING_LENGTH: ClassVar[NumericField] = NumericField(
        "columnMinimumStringLength", "columnMinimumStringLength"
    )
    """
    Length of the shortest value in a string column.
    """
    COLUMN_MINS: ClassVar[KeywordField] = KeywordField("columnMins", "columnMins")
    """
    List of the least values in a column.
    """
    COLUMN_MISSING_VALUES_COUNT: ClassVar[NumericField] = NumericField(
        "columnMissingValuesCount", "columnMissingValuesCount"
    )
    """
    Number of rows in a column that do not contain content.
    """
    COLUMN_MISSING_VALUES_COUNT_LONG: ClassVar[NumericField] = NumericField(
        "columnMissingValuesCountLong", "columnMissingValuesCountLong"
    )
    """
    Number of rows in a column that do not contain content.
    """
    COLUMN_MISSING_VALUES_PERCENTAGE: ClassVar[NumericField] = NumericField(
        "columnMissingValuesPercentage", "columnMissingValuesPercentage"
    )
    """
    Percentage of rows in a column that do not contain content.
    """
    COLUMN_UNIQUENESS_PERCENTAGE: ClassVar[NumericField] = NumericField(
        "columnUniquenessPercentage", "columnUniquenessPercentage"
    )
    """
    Ratio indicating how unique data in this column is: 0 indicates that all values are the same, 100 indicates that all values in this column are unique.
    """  # noqa: E501
    COLUMN_VARIANCE: ClassVar[NumericField] = NumericField(
        "columnVariance", "columnVariance"
    )
    """
    Calculated variance of the values in a numeric column.
    """
    COLUMN_TOP_VALUES: ClassVar[KeywordField] = KeywordField(
        "columnTopValues", "columnTopValues"
    )
    """
    List of top values in this column.
    """
    COLUMN_DEPTH_LEVEL: ClassVar[NumericField] = NumericField(
        "columnDepthLevel", "columnDepthLevel"
    )
    """
    Level of nesting of this column, used for STRUCT and NESTED columns.
    """

    SNOWFLAKE_DYNAMIC_TABLE: ClassVar[RelationField] = RelationField(
        "snowflakeDynamicTable"
    )
    """
    TBC
    """
    VIEW: ClassVar[RelationField] = RelationField("view")
    """
    TBC
    """
    NESTED_COLUMNS: ClassVar[RelationField] = RelationField("nestedColumns")
    """
    TBC
    """
    DATA_QUALITY_METRIC_DIMENSIONS: ClassVar[RelationField] = RelationField(
        "dataQualityMetricDimensions"
    )
    """
    TBC
    """
    DBT_MODEL_COLUMNS: ClassVar[RelationField] = RelationField("dbtModelColumns")
    """
    TBC
    """
    TABLE: ClassVar[RelationField] = RelationField("table")
    """
    TBC
    """
    COLUMN_DBT_MODEL_COLUMNS: ClassVar[RelationField] = RelationField(
        "columnDbtModelColumns"
    )
    """
    TBC
    """
    MATERIALISED_VIEW: ClassVar[RelationField] = RelationField("materialisedView")
    """
    TBC
    """
    PARENT_COLUMN: ClassVar[RelationField] = RelationField("parentColumn")
    """
    TBC
    """
    QUERIES: ClassVar[RelationField] = RelationField("queries")
    """
    TBC
    """
    METRIC_TIMESTAMPS: ClassVar[RelationField] = RelationField("metricTimestamps")
    """
    TBC
    """
    FOREIGN_KEY_TO: ClassVar[RelationField] = RelationField("foreignKeyTo")
    """
    TBC
    """
    FOREIGN_KEY_FROM: ClassVar[RelationField] = RelationField("foreignKeyFrom")
    """
    TBC
    """
    DBT_METRICS: ClassVar[RelationField] = RelationField("dbtMetrics")
    """
    TBC
    """
    TABLE_PARTITION: ClassVar[RelationField] = RelationField("tablePartition")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "data_type",
        "sub_data_type",
        "raw_data_type_definition",
        "order",
        "nested_column_count",
        "is_partition",
        "partition_order",
        "is_clustered",
        "is_primary",
        "is_foreign",
        "is_indexed",
        "is_sort",
        "is_dist",
        "is_pinned",
        "pinned_by",
        "pinned_at",
        "precision",
        "default_value",
        "is_nullable",
        "numeric_scale",
        "max_length",
        "validations",
        "parent_column_qualified_name",
        "parent_column_name",
        "column_distinct_values_count",
        "column_distinct_values_count_long",
        "column_histogram",
        "column_max",
        "column_min",
        "column_mean",
        "column_sum",
        "column_median",
        "column_standard_deviation",
        "column_unique_values_count",
        "column_unique_values_count_long",
        "column_average",
        "column_average_length",
        "column_duplicate_values_count",
        "column_duplicate_values_count_long",
        "column_maximum_string_length",
        "column_maxs",
        "column_minimum_string_length",
        "column_mins",
        "column_missing_values_count",
        "column_missing_values_count_long",
        "column_missing_values_percentage",
        "column_uniqueness_percentage",
        "column_variance",
        "column_top_values",
        "column_depth_level",
        "snowflake_dynamic_table",
        "view",
        "nested_columns",
        "data_quality_metric_dimensions",
        "dbt_model_columns",
        "table",
        "column_dbt_model_columns",
        "materialised_view",
        "parent_column",
        "queries",
        "metric_timestamps",
        "foreign_key_to",
        "foreign_key_from",
        "dbt_metrics",
        "table_partition",
    ]

    @property
    def data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_type

    @data_type.setter
    def data_type(self, data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_type = data_type

    @property
    def sub_data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sub_data_type

    @sub_data_type.setter
    def sub_data_type(self, sub_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sub_data_type = sub_data_type

    @property
    def raw_data_type_definition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.raw_data_type_definition
        )

    @raw_data_type_definition.setter
    def raw_data_type_definition(self, raw_data_type_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.raw_data_type_definition = raw_data_type_definition

    @property
    def order(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.order

    @order.setter
    def order(self, order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.order = order

    @property
    def nested_column_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.nested_column_count

    @nested_column_count.setter
    def nested_column_count(self, nested_column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.nested_column_count = nested_column_count

    @property
    def is_partition(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_partition

    @is_partition.setter
    def is_partition(self, is_partition: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_partition = is_partition

    @property
    def partition_order(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.partition_order

    @partition_order.setter
    def partition_order(self, partition_order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_order = partition_order

    @property
    def is_clustered(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_clustered

    @is_clustered.setter
    def is_clustered(self, is_clustered: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_clustered = is_clustered

    @property
    def is_primary(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_primary

    @is_primary.setter
    def is_primary(self, is_primary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_primary = is_primary

    @property
    def is_foreign(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_foreign

    @is_foreign.setter
    def is_foreign(self, is_foreign: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_foreign = is_foreign

    @property
    def is_indexed(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_indexed

    @is_indexed.setter
    def is_indexed(self, is_indexed: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_indexed = is_indexed

    @property
    def is_sort(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_sort

    @is_sort.setter
    def is_sort(self, is_sort: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_sort = is_sort

    @property
    def is_dist(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_dist

    @is_dist.setter
    def is_dist(self, is_dist: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_dist = is_dist

    @property
    def is_pinned(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_pinned

    @is_pinned.setter
    def is_pinned(self, is_pinned: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_pinned = is_pinned

    @property
    def pinned_by(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.pinned_by

    @pinned_by.setter
    def pinned_by(self, pinned_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.pinned_by = pinned_by

    @property
    def pinned_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.pinned_at

    @pinned_at.setter
    def pinned_at(self, pinned_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.pinned_at = pinned_at

    @property
    def precision(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.precision

    @precision.setter
    def precision(self, precision: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.precision = precision

    @property
    def default_value(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.default_value

    @default_value.setter
    def default_value(self, default_value: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.default_value = default_value

    @property
    def is_nullable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_nullable

    @is_nullable.setter
    def is_nullable(self, is_nullable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_nullable = is_nullable

    @property
    def numeric_scale(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.numeric_scale

    @numeric_scale.setter
    def numeric_scale(self, numeric_scale: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.numeric_scale = numeric_scale

    @property
    def max_length(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.max_length

    @max_length.setter
    def max_length(self, max_length: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.max_length = max_length

    @property
    def validations(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.validations

    @validations.setter
    def validations(self, validations: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.validations = validations

    @property
    def parent_column_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.parent_column_qualified_name
        )

    @parent_column_qualified_name.setter
    def parent_column_qualified_name(self, parent_column_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_column_qualified_name = parent_column_qualified_name

    @property
    def parent_column_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.parent_column_name

    @parent_column_name.setter
    def parent_column_name(self, parent_column_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_column_name = parent_column_name

    @property
    def column_distinct_values_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_distinct_values_count
        )

    @column_distinct_values_count.setter
    def column_distinct_values_count(self, column_distinct_values_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_distinct_values_count = column_distinct_values_count

    @property
    def column_distinct_values_count_long(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_distinct_values_count_long
        )

    @column_distinct_values_count_long.setter
    def column_distinct_values_count_long(
        self, column_distinct_values_count_long: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_distinct_values_count_long = (
            column_distinct_values_count_long
        )

    @property
    def column_histogram(self) -> Optional[Histogram]:
        return None if self.attributes is None else self.attributes.column_histogram

    @column_histogram.setter
    def column_histogram(self, column_histogram: Optional[Histogram]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_histogram = column_histogram

    @property
    def column_max(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_max

    @column_max.setter
    def column_max(self, column_max: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_max = column_max

    @property
    def column_min(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_min

    @column_min.setter
    def column_min(self, column_min: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_min = column_min

    @property
    def column_mean(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_mean

    @column_mean.setter
    def column_mean(self, column_mean: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_mean = column_mean

    @property
    def column_sum(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_sum

    @column_sum.setter
    def column_sum(self, column_sum: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_sum = column_sum

    @property
    def column_median(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_median

    @column_median.setter
    def column_median(self, column_median: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_median = column_median

    @property
    def column_standard_deviation(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_standard_deviation
        )

    @column_standard_deviation.setter
    def column_standard_deviation(self, column_standard_deviation: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_standard_deviation = column_standard_deviation

    @property
    def column_unique_values_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_unique_values_count
        )

    @column_unique_values_count.setter
    def column_unique_values_count(self, column_unique_values_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_unique_values_count = column_unique_values_count

    @property
    def column_unique_values_count_long(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_unique_values_count_long
        )

    @column_unique_values_count_long.setter
    def column_unique_values_count_long(
        self, column_unique_values_count_long: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_unique_values_count_long = (
            column_unique_values_count_long
        )

    @property
    def column_average(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_average

    @column_average.setter
    def column_average(self, column_average: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_average = column_average

    @property
    def column_average_length(self) -> Optional[float]:
        return (
            None if self.attributes is None else self.attributes.column_average_length
        )

    @column_average_length.setter
    def column_average_length(self, column_average_length: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_average_length = column_average_length

    @property
    def column_duplicate_values_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_duplicate_values_count
        )

    @column_duplicate_values_count.setter
    def column_duplicate_values_count(
        self, column_duplicate_values_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_duplicate_values_count = column_duplicate_values_count

    @property
    def column_duplicate_values_count_long(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_duplicate_values_count_long
        )

    @column_duplicate_values_count_long.setter
    def column_duplicate_values_count_long(
        self, column_duplicate_values_count_long: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_duplicate_values_count_long = (
            column_duplicate_values_count_long
        )

    @property
    def column_maximum_string_length(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_maximum_string_length
        )

    @column_maximum_string_length.setter
    def column_maximum_string_length(self, column_maximum_string_length: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_maximum_string_length = column_maximum_string_length

    @property
    def column_maxs(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.column_maxs

    @column_maxs.setter
    def column_maxs(self, column_maxs: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_maxs = column_maxs

    @property
    def column_minimum_string_length(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_minimum_string_length
        )

    @column_minimum_string_length.setter
    def column_minimum_string_length(self, column_minimum_string_length: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_minimum_string_length = column_minimum_string_length

    @property
    def column_mins(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.column_mins

    @column_mins.setter
    def column_mins(self, column_mins: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_mins = column_mins

    @property
    def column_missing_values_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_missing_values_count
        )

    @column_missing_values_count.setter
    def column_missing_values_count(self, column_missing_values_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_missing_values_count = column_missing_values_count

    @property
    def column_missing_values_count_long(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_missing_values_count_long
        )

    @column_missing_values_count_long.setter
    def column_missing_values_count_long(
        self, column_missing_values_count_long: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_missing_values_count_long = (
            column_missing_values_count_long
        )

    @property
    def column_missing_values_percentage(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_missing_values_percentage
        )

    @column_missing_values_percentage.setter
    def column_missing_values_percentage(
        self, column_missing_values_percentage: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_missing_values_percentage = (
            column_missing_values_percentage
        )

    @property
    def column_uniqueness_percentage(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_uniqueness_percentage
        )

    @column_uniqueness_percentage.setter
    def column_uniqueness_percentage(
        self, column_uniqueness_percentage: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_uniqueness_percentage = column_uniqueness_percentage

    @property
    def column_variance(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_variance

    @column_variance.setter
    def column_variance(self, column_variance: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_variance = column_variance

    @property
    def column_top_values(self) -> Optional[list[ColumnValueFrequencyMap]]:
        return None if self.attributes is None else self.attributes.column_top_values

    @column_top_values.setter
    def column_top_values(
        self, column_top_values: Optional[list[ColumnValueFrequencyMap]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_top_values = column_top_values

    @property
    def column_depth_level(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.column_depth_level

    @column_depth_level.setter
    def column_depth_level(self, column_depth_level: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_depth_level = column_depth_level

    @property
    def snowflake_dynamic_table(self) -> Optional[SnowflakeDynamicTable]:
        return (
            None if self.attributes is None else self.attributes.snowflake_dynamic_table
        )

    @snowflake_dynamic_table.setter
    def snowflake_dynamic_table(
        self, snowflake_dynamic_table: Optional[SnowflakeDynamicTable]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_dynamic_table = snowflake_dynamic_table

    @property
    def view(self) -> Optional[View]:
        return None if self.attributes is None else self.attributes.view

    @view.setter
    def view(self, view: Optional[View]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view = view

    @property
    def nested_columns(self) -> Optional[list[Column]]:
        return None if self.attributes is None else self.attributes.nested_columns

    @nested_columns.setter
    def nested_columns(self, nested_columns: Optional[list[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.nested_columns = nested_columns

    @property
    def data_quality_metric_dimensions(self) -> Optional[list[Metric]]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_quality_metric_dimensions
        )

    @data_quality_metric_dimensions.setter
    def data_quality_metric_dimensions(
        self, data_quality_metric_dimensions: Optional[list[Metric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_quality_metric_dimensions = data_quality_metric_dimensions

    @property
    def dbt_model_columns(self) -> Optional[list[DbtModelColumn]]:
        return None if self.attributes is None else self.attributes.dbt_model_columns

    @dbt_model_columns.setter
    def dbt_model_columns(self, dbt_model_columns: Optional[list[DbtModelColumn]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_columns = dbt_model_columns

    @property
    def table(self) -> Optional[Table]:
        return None if self.attributes is None else self.attributes.table

    @table.setter
    def table(self, table: Optional[Table]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table = table

    @property
    def column_dbt_model_columns(self) -> Optional[list[DbtModelColumn]]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_dbt_model_columns
        )

    @column_dbt_model_columns.setter
    def column_dbt_model_columns(
        self, column_dbt_model_columns: Optional[list[DbtModelColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_dbt_model_columns = column_dbt_model_columns

    @property
    def materialised_view(self) -> Optional[MaterialisedView]:
        return None if self.attributes is None else self.attributes.materialised_view

    @materialised_view.setter
    def materialised_view(self, materialised_view: Optional[MaterialisedView]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.materialised_view = materialised_view

    @property
    def parent_column(self) -> Optional[Column]:
        return None if self.attributes is None else self.attributes.parent_column

    @parent_column.setter
    def parent_column(self, parent_column: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_column = parent_column

    @property
    def queries(self) -> Optional[list[Query]]:
        return None if self.attributes is None else self.attributes.queries

    @queries.setter
    def queries(self, queries: Optional[list[Query]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.queries = queries

    @property
    def metric_timestamps(self) -> Optional[list[Metric]]:
        return None if self.attributes is None else self.attributes.metric_timestamps

    @metric_timestamps.setter
    def metric_timestamps(self, metric_timestamps: Optional[list[Metric]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_timestamps = metric_timestamps

    @property
    def foreign_key_to(self) -> Optional[list[Column]]:
        return None if self.attributes is None else self.attributes.foreign_key_to

    @foreign_key_to.setter
    def foreign_key_to(self, foreign_key_to: Optional[list[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.foreign_key_to = foreign_key_to

    @property
    def foreign_key_from(self) -> Optional[Column]:
        return None if self.attributes is None else self.attributes.foreign_key_from

    @foreign_key_from.setter
    def foreign_key_from(self, foreign_key_from: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.foreign_key_from = foreign_key_from

    @property
    def dbt_metrics(self) -> Optional[list[DbtMetric]]:
        return None if self.attributes is None else self.attributes.dbt_metrics

    @dbt_metrics.setter
    def dbt_metrics(self, dbt_metrics: Optional[list[DbtMetric]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_metrics = dbt_metrics

    @property
    def table_partition(self) -> Optional[TablePartition]:
        return None if self.attributes is None else self.attributes.table_partition

    @table_partition.setter
    def table_partition(self, table_partition: Optional[TablePartition]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_partition = table_partition

    class Attributes(SQL.Attributes):
        data_type: Optional[str] = Field(default=None, description="")
        sub_data_type: Optional[str] = Field(default=None, description="")
        raw_data_type_definition: Optional[str] = Field(default=None, description="")
        order: Optional[int] = Field(default=None, description="")
        nested_column_count: Optional[int] = Field(default=None, description="")
        is_partition: Optional[bool] = Field(default=None, description="")
        partition_order: Optional[int] = Field(default=None, description="")
        is_clustered: Optional[bool] = Field(default=None, description="")
        is_primary: Optional[bool] = Field(default=None, description="")
        is_foreign: Optional[bool] = Field(default=None, description="")
        is_indexed: Optional[bool] = Field(default=None, description="")
        is_sort: Optional[bool] = Field(default=None, description="")
        is_dist: Optional[bool] = Field(default=None, description="")
        is_pinned: Optional[bool] = Field(default=None, description="")
        pinned_by: Optional[str] = Field(default=None, description="")
        pinned_at: Optional[datetime] = Field(default=None, description="")
        precision: Optional[int] = Field(default=None, description="")
        default_value: Optional[str] = Field(default=None, description="")
        is_nullable: Optional[bool] = Field(default=None, description="")
        numeric_scale: Optional[float] = Field(default=None, description="")
        max_length: Optional[int] = Field(default=None, description="")
        validations: Optional[dict[str, str]] = Field(default=None, description="")
        parent_column_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        parent_column_name: Optional[str] = Field(default=None, description="")
        column_distinct_values_count: Optional[int] = Field(
            default=None, description=""
        )
        column_distinct_values_count_long: Optional[int] = Field(
            default=None, description=""
        )
        column_histogram: Optional[Histogram] = Field(default=None, description="")
        column_max: Optional[float] = Field(default=None, description="")
        column_min: Optional[float] = Field(default=None, description="")
        column_mean: Optional[float] = Field(default=None, description="")
        column_sum: Optional[float] = Field(default=None, description="")
        column_median: Optional[float] = Field(default=None, description="")
        column_standard_deviation: Optional[float] = Field(default=None, description="")
        column_unique_values_count: Optional[int] = Field(default=None, description="")
        column_unique_values_count_long: Optional[int] = Field(
            default=None, description=""
        )
        column_average: Optional[float] = Field(default=None, description="")
        column_average_length: Optional[float] = Field(default=None, description="")
        column_duplicate_values_count: Optional[int] = Field(
            default=None, description=""
        )
        column_duplicate_values_count_long: Optional[int] = Field(
            default=None, description=""
        )
        column_maximum_string_length: Optional[int] = Field(
            default=None, description=""
        )
        column_maxs: Optional[set[str]] = Field(default=None, description="")
        column_minimum_string_length: Optional[int] = Field(
            default=None, description=""
        )
        column_mins: Optional[set[str]] = Field(default=None, description="")
        column_missing_values_count: Optional[int] = Field(default=None, description="")
        column_missing_values_count_long: Optional[int] = Field(
            default=None, description=""
        )
        column_missing_values_percentage: Optional[float] = Field(
            default=None, description=""
        )
        column_uniqueness_percentage: Optional[float] = Field(
            default=None, description=""
        )
        column_variance: Optional[float] = Field(default=None, description="")
        column_top_values: Optional[list[ColumnValueFrequencyMap]] = Field(
            default=None, description=""
        )
        column_depth_level: Optional[int] = Field(default=None, description="")
        snowflake_dynamic_table: Optional[SnowflakeDynamicTable] = Field(
            default=None, description=""
        )  # relationship
        view: Optional[View] = Field(default=None, description="")  # relationship
        nested_columns: Optional[list[Column]] = Field(
            default=None, description=""
        )  # relationship
        data_quality_metric_dimensions: Optional[list[Metric]] = Field(
            default=None, description=""
        )  # relationship
        dbt_model_columns: Optional[list[DbtModelColumn]] = Field(
            default=None, description=""
        )  # relationship
        table: Optional[Table] = Field(default=None, description="")  # relationship
        column_dbt_model_columns: Optional[list[DbtModelColumn]] = Field(
            default=None, description=""
        )  # relationship
        materialised_view: Optional[MaterialisedView] = Field(
            default=None, description=""
        )  # relationship
        parent_column: Optional[Column] = Field(
            default=None, description=""
        )  # relationship
        queries: Optional[list[Query]] = Field(
            default=None, description=""
        )  # relationship
        metric_timestamps: Optional[list[Metric]] = Field(
            default=None, description=""
        )  # relationship
        foreign_key_to: Optional[list[Column]] = Field(
            default=None, description=""
        )  # relationship
        foreign_key_from: Optional[Column] = Field(
            default=None, description=""
        )  # relationship
        dbt_metrics: Optional[list[DbtMetric]] = Field(
            default=None, description=""
        )  # relationship
        table_partition: Optional[TablePartition] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, *, name: str, parent_qualified_name: str, parent_type: type, order: int
        ) -> Column.Attributes:
            validate_required_fields(
                ["name", "parent_qualified_name", "parent_type", "order"],
                [name, parent_qualified_name, parent_type, order],
            )
            fields = parent_qualified_name.split("/")
            if len(fields) != 6:
                raise ValueError("Invalid parent_qualified_name")
            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid parent_qualified_name") from e
            if order < 0:
                raise ValueError("Order must be be a positive integer")
            ret_value = Column.Attributes(
                name=name,
                qualified_name=f"{parent_qualified_name}/{name}",
                connector_name=connector_type.value,
                schema_name=fields[4],
                schema_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}/{fields[3]}/{fields[4]}",
                database_name=fields[3],
                database_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}/{fields[3]}",
                connection_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}",
                order=order,
            )
            if parent_type == Table:
                ret_value.table_qualified_name = parent_qualified_name
                ret_value.table = Table.ref_by_qualified_name(parent_qualified_name)
                ret_value.table_name = fields[5]
            elif parent_type == View:
                ret_value.view_qualified_name = parent_qualified_name
                ret_value.view = View.ref_by_qualified_name(parent_qualified_name)
                ret_value.view_name = fields[5]
            elif parent_type == MaterialisedView:
                ret_value.view_qualified_name = parent_qualified_name
                ret_value.materialised_view = MaterialisedView.ref_by_qualified_name(
                    parent_qualified_name
                )
                ret_value.view_name = fields[5]
            else:
                raise ValueError(
                    "parent_type must be either Table, View or MaterializeView"
                )
            return ret_value

    attributes: "Column.Attributes" = Field(
        default_factory=lambda: Column.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SnowflakeStream(SQL):
    """Description"""

    type_name: str = Field(default="SnowflakeStream", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakeStream":
            raise ValueError("must be SnowflakeStream")
        return v

    def __setattr__(self, name, value):
        if name in SnowflakeStream._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SNOWFLAKE_STREAM_TYPE: ClassVar[KeywordField] = KeywordField(
        "snowflakeStreamType", "snowflakeStreamType"
    )
    """
    Type of this stream, for example: standard, append-only, insert-only, etc.
    """
    SNOWFLAKE_STREAM_SOURCE_TYPE: ClassVar[KeywordField] = KeywordField(
        "snowflakeStreamSourceType", "snowflakeStreamSourceType"
    )
    """
    Type of the source of this stream.
    """
    SNOWFLAKE_STREAM_MODE: ClassVar[KeywordField] = KeywordField(
        "snowflakeStreamMode", "snowflakeStreamMode"
    )
    """
    Mode of this stream.
    """
    SNOWFLAKE_STREAM_IS_STALE: ClassVar[BooleanField] = BooleanField(
        "snowflakeStreamIsStale", "snowflakeStreamIsStale"
    )
    """
    Whether this stream is stale (true) or not (false).
    """
    SNOWFLAKE_STREAM_STALE_AFTER: ClassVar[NumericField] = NumericField(
        "snowflakeStreamStaleAfter", "snowflakeStreamStaleAfter"
    )
    """
    Time (epoch) after which this stream will be stale, in milliseconds.
    """

    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "snowflake_stream_type",
        "snowflake_stream_source_type",
        "snowflake_stream_mode",
        "snowflake_stream_is_stale",
        "snowflake_stream_stale_after",
        "atlan_schema",
    ]

    @property
    def snowflake_stream_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.snowflake_stream_type
        )

    @snowflake_stream_type.setter
    def snowflake_stream_type(self, snowflake_stream_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_type = snowflake_stream_type

    @property
    def snowflake_stream_source_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_stream_source_type
        )

    @snowflake_stream_source_type.setter
    def snowflake_stream_source_type(self, snowflake_stream_source_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_source_type = snowflake_stream_source_type

    @property
    def snowflake_stream_mode(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.snowflake_stream_mode
        )

    @snowflake_stream_mode.setter
    def snowflake_stream_mode(self, snowflake_stream_mode: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_mode = snowflake_stream_mode

    @property
    def snowflake_stream_is_stale(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_stream_is_stale
        )

    @snowflake_stream_is_stale.setter
    def snowflake_stream_is_stale(self, snowflake_stream_is_stale: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_is_stale = snowflake_stream_is_stale

    @property
    def snowflake_stream_stale_after(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_stream_stale_after
        )

    @snowflake_stream_stale_after.setter
    def snowflake_stream_stale_after(
        self, snowflake_stream_stale_after: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_stale_after = snowflake_stream_stale_after

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    class Attributes(SQL.Attributes):
        snowflake_stream_type: Optional[str] = Field(default=None, description="")
        snowflake_stream_source_type: Optional[str] = Field(
            default=None, description=""
        )
        snowflake_stream_mode: Optional[str] = Field(default=None, description="")
        snowflake_stream_is_stale: Optional[bool] = Field(default=None, description="")
        snowflake_stream_stale_after: Optional[datetime] = Field(
            default=None, description=""
        )
        atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship

    attributes: "SnowflakeStream.Attributes" = Field(
        default_factory=lambda: SnowflakeStream.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Procedure(SQL):
    """Description"""

    type_name: str = Field(default="Procedure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Procedure":
            raise ValueError("must be Procedure")
        return v

    def __setattr__(self, name, value):
        if name in Procedure._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DEFINITION: ClassVar[KeywordField] = KeywordField("definition", "definition")
    """
    SQL definition of the procedure.
    """

    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "definition",
        "atlan_schema",
    ]

    @property
    def definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.definition

    @definition.setter
    def definition(self, definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.definition = definition

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    class Attributes(SQL.Attributes):
        definition: Optional[str] = Field(default=None, description="")
        atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship

    attributes: "Procedure.Attributes" = Field(
        default_factory=lambda: Procedure.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SnowflakeTag(Tag):
    """Description"""

    type_name: str = Field(default="SnowflakeTag", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakeTag":
            raise ValueError("must be SnowflakeTag")
        return v

    def __setattr__(self, name, value):
        if name in SnowflakeTag._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    TAG_ID: ClassVar[KeywordField] = KeywordField("tagId", "tagId")
    """
    Unique identifier of the tag in the source system.
    """
    TAG_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "tagAttributes", "tagAttributes"
    )
    """
    Attributes associated with the tag in the source system.
    """
    TAG_ALLOWED_VALUES: ClassVar[KeywordTextField] = KeywordTextField(
        "tagAllowedValues", "tagAllowedValues", "tagAllowedValues.text"
    )
    """
    Allowed values for the tag in the source system. These are denormalized from tagAttributes for ease of querying.
    """
    MAPPED_CLASSIFICATION_NAME: ClassVar[KeywordField] = KeywordField(
        "mappedClassificationName", "mappedClassificationName"
    )
    """
    Name of the classification in Atlan that is mapped to this tag.
    """
    QUERY_COUNT: ClassVar[NumericField] = NumericField("queryCount", "queryCount")
    """
    Number of times this asset has been queried.
    """
    QUERY_USER_COUNT: ClassVar[NumericField] = NumericField(
        "queryUserCount", "queryUserCount"
    )
    """
    Number of unique users who have queried this asset.
    """
    QUERY_USER_MAP: ClassVar[KeywordField] = KeywordField(
        "queryUserMap", "queryUserMap"
    )
    """
    Map of unique users who have queried this asset to the number of times they have queried it.
    """
    QUERY_COUNT_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "queryCountUpdatedAt", "queryCountUpdatedAt"
    )
    """
    Time (epoch) at which the query count was last updated, in milliseconds.
    """
    DATABASE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "databaseName", "databaseName.keyword", "databaseName"
    )
    """
    Simple name of the database in which this SQL asset exists, or empty if it does not exist within a database.
    """
    DATABASE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "databaseQualifiedName", "databaseQualifiedName"
    )
    """
    Unique name of the database in which this SQL asset exists, or empty if it does not exist within a database.
    """
    SCHEMA_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "schemaName", "schemaName.keyword", "schemaName"
    )
    """
    Simple name of the schema in which this SQL asset exists, or empty if it does not exist within a schema.
    """
    SCHEMA_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "schemaQualifiedName", "schemaQualifiedName"
    )
    """
    Unique name of the schema in which this SQL asset exists, or empty if it does not exist within a schema.
    """
    TABLE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "tableName", "tableName.keyword", "tableName"
    )
    """
    Simple name of the table in which this SQL asset exists, or empty if it does not exist within a table.
    """
    TABLE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "tableQualifiedName", "tableQualifiedName"
    )
    """
    Unique name of the table in which this SQL asset exists, or empty if it does not exist within a table.
    """
    VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "viewName", "viewName.keyword", "viewName"
    )
    """
    Simple name of the view in which this SQL asset exists, or empty if it does not exist within a view.
    """
    VIEW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "viewQualifiedName", "viewQualifiedName"
    )
    """
    Unique name of the view in which this SQL asset exists, or empty if it does not exist within a view.
    """
    IS_PROFILED: ClassVar[BooleanField] = BooleanField("isProfiled", "isProfiled")
    """
    Whether this asset has been profiled (true) or not (false).
    """
    LAST_PROFILED_AT: ClassVar[NumericField] = NumericField(
        "lastProfiledAt", "lastProfiledAt"
    )
    """
    Time (epoch) at which this asset was last profiled, in milliseconds.
    """

    DBT_SOURCES: ClassVar[RelationField] = RelationField("dbtSources")
    """
    TBC
    """
    SQL_DBT_MODELS: ClassVar[RelationField] = RelationField("sqlDbtModels")
    """
    TBC
    """
    SQL_DBT_SOURCES: ClassVar[RelationField] = RelationField("sqlDBTSources")
    """
    TBC
    """
    DBT_MODELS: ClassVar[RelationField] = RelationField("dbtModels")
    """
    TBC
    """
    DBT_TESTS: ClassVar[RelationField] = RelationField("dbtTests")
    """
    TBC
    """
    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "tag_id",
        "tag_attributes",
        "tag_allowed_values",
        "mapped_atlan_tag_name",
        "query_count",
        "query_user_count",
        "query_user_map",
        "query_count_updated_at",
        "database_name",
        "database_qualified_name",
        "schema_name",
        "schema_qualified_name",
        "table_name",
        "table_qualified_name",
        "view_name",
        "view_qualified_name",
        "is_profiled",
        "last_profiled_at",
        "dbt_sources",
        "sql_dbt_models",
        "sql_dbt_sources",
        "dbt_models",
        "dbt_tests",
        "atlan_schema",
    ]

    @property
    def tag_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.tag_id

    @tag_id.setter
    def tag_id(self, tag_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tag_id = tag_id

    @property
    def tag_attributes(self) -> Optional[list[SourceTagAttribute]]:
        return None if self.attributes is None else self.attributes.tag_attributes

    @tag_attributes.setter
    def tag_attributes(self, tag_attributes: Optional[list[SourceTagAttribute]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tag_attributes = tag_attributes

    @property
    def tag_allowed_values(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.tag_allowed_values

    @tag_allowed_values.setter
    def tag_allowed_values(self, tag_allowed_values: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tag_allowed_values = tag_allowed_values

    @property
    def mapped_atlan_tag_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.mapped_atlan_tag_name
        )

    @mapped_atlan_tag_name.setter
    def mapped_atlan_tag_name(self, mapped_atlan_tag_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mapped_atlan_tag_name = mapped_atlan_tag_name

    @property
    def query_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_count

    @query_count.setter
    def query_count(self, query_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_count = query_count

    @property
    def query_user_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_user_count

    @query_user_count.setter
    def query_user_count(self, query_user_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_user_count = query_user_count

    @property
    def query_user_map(self) -> Optional[dict[str, int]]:
        return None if self.attributes is None else self.attributes.query_user_map

    @query_user_map.setter
    def query_user_map(self, query_user_map: Optional[dict[str, int]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_user_map = query_user_map

    @property
    def query_count_updated_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.query_count_updated_at
        )

    @query_count_updated_at.setter
    def query_count_updated_at(self, query_count_updated_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_count_updated_at = query_count_updated_at

    @property
    def database_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.database_name

    @database_name.setter
    def database_name(self, database_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database_name = database_name

    @property
    def database_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.database_qualified_name
        )

    @database_qualified_name.setter
    def database_qualified_name(self, database_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database_qualified_name = database_qualified_name

    @property
    def schema_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.schema_name

    @schema_name.setter
    def schema_name(self, schema_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_name = schema_name

    @property
    def schema_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.schema_qualified_name
        )

    @schema_qualified_name.setter
    def schema_qualified_name(self, schema_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_qualified_name = schema_qualified_name

    @property
    def table_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.table_name

    @table_name.setter
    def table_name(self, table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_name = table_name

    @property
    def table_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.table_qualified_name

    @table_qualified_name.setter
    def table_qualified_name(self, table_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_qualified_name = table_qualified_name

    @property
    def view_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.view_name

    @view_name.setter
    def view_name(self, view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_name = view_name

    @property
    def view_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.view_qualified_name

    @view_qualified_name.setter
    def view_qualified_name(self, view_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_qualified_name = view_qualified_name

    @property
    def is_profiled(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_profiled

    @is_profiled.setter
    def is_profiled(self, is_profiled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_profiled = is_profiled

    @property
    def last_profiled_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.last_profiled_at

    @last_profiled_at.setter
    def last_profiled_at(self, last_profiled_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_profiled_at = last_profiled_at

    @property
    def dbt_sources(self) -> Optional[list[DbtSource]]:
        return None if self.attributes is None else self.attributes.dbt_sources

    @dbt_sources.setter
    def dbt_sources(self, dbt_sources: Optional[list[DbtSource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_sources = dbt_sources

    @property
    def sql_dbt_models(self) -> Optional[list[DbtModel]]:
        return None if self.attributes is None else self.attributes.sql_dbt_models

    @sql_dbt_models.setter
    def sql_dbt_models(self, sql_dbt_models: Optional[list[DbtModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_dbt_models = sql_dbt_models

    @property
    def sql_dbt_sources(self) -> Optional[list[DbtSource]]:
        return None if self.attributes is None else self.attributes.sql_dbt_sources

    @sql_dbt_sources.setter
    def sql_dbt_sources(self, sql_dbt_sources: Optional[list[DbtSource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_dbt_sources = sql_dbt_sources

    @property
    def dbt_models(self) -> Optional[list[DbtModel]]:
        return None if self.attributes is None else self.attributes.dbt_models

    @dbt_models.setter
    def dbt_models(self, dbt_models: Optional[list[DbtModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_models = dbt_models

    @property
    def dbt_tests(self) -> Optional[list[DbtTest]]:
        return None if self.attributes is None else self.attributes.dbt_tests

    @dbt_tests.setter
    def dbt_tests(self, dbt_tests: Optional[list[DbtTest]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tests = dbt_tests

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    class Attributes(Tag.Attributes):
        tag_id: Optional[str] = Field(default=None, description="")
        tag_attributes: Optional[list[SourceTagAttribute]] = Field(
            default=None, description=""
        )
        tag_allowed_values: Optional[set[str]] = Field(default=None, description="")
        mapped_atlan_tag_name: Optional[str] = Field(default=None, description="")
        query_count: Optional[int] = Field(default=None, description="")
        query_user_count: Optional[int] = Field(default=None, description="")
        query_user_map: Optional[dict[str, int]] = Field(default=None, description="")
        query_count_updated_at: Optional[datetime] = Field(default=None, description="")
        database_name: Optional[str] = Field(default=None, description="")
        database_qualified_name: Optional[str] = Field(default=None, description="")
        schema_name: Optional[str] = Field(default=None, description="")
        schema_qualified_name: Optional[str] = Field(default=None, description="")
        table_name: Optional[str] = Field(default=None, description="")
        table_qualified_name: Optional[str] = Field(default=None, description="")
        view_name: Optional[str] = Field(default=None, description="")
        view_qualified_name: Optional[str] = Field(default=None, description="")
        is_profiled: Optional[bool] = Field(default=None, description="")
        last_profiled_at: Optional[datetime] = Field(default=None, description="")
        dbt_sources: Optional[list[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        dbt_tests: Optional[list[DbtTest]] = Field(
            default=None, description=""
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship

    attributes: "SnowflakeTag.Attributes" = Field(
        default_factory=lambda: SnowflakeTag.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Matillion(Catalog):
    """Description"""

    type_name: str = Field(default="Matillion", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Matillion":
            raise ValueError("must be Matillion")
        return v

    def __setattr__(self, name, value):
        if name in Matillion._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MATILLION_VERSION: ClassVar[KeywordField] = KeywordField(
        "matillionVersion", "matillionVersion"
    )
    """
    Current point in time state of a project.
    """

    _convenience_properties: ClassVar[list[str]] = [
        "matillion_version",
    ]

    @property
    def matillion_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.matillion_version

    @matillion_version.setter
    def matillion_version(self, matillion_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_version = matillion_version

    class Attributes(Catalog.Attributes):
        matillion_version: Optional[str] = Field(default=None, description="")

    attributes: "Matillion.Attributes" = Field(
        default_factory=lambda: Matillion.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MatillionGroup(Matillion):
    """Description"""

    type_name: str = Field(default="MatillionGroup", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MatillionGroup":
            raise ValueError("must be MatillionGroup")
        return v

    def __setattr__(self, name, value):
        if name in MatillionGroup._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MATILLION_PROJECT_COUNT: ClassVar[NumericField] = NumericField(
        "matillionProjectCount", "matillionProjectCount"
    )
    """
    Number of projects within the group.
    """

    MATILLION_PROJECTS: ClassVar[RelationField] = RelationField("matillionProjects")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "matillion_project_count",
        "matillion_projects",
    ]

    @property
    def matillion_project_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.matillion_project_count
        )

    @matillion_project_count.setter
    def matillion_project_count(self, matillion_project_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_project_count = matillion_project_count

    @property
    def matillion_projects(self) -> Optional[list[MatillionProject]]:
        return None if self.attributes is None else self.attributes.matillion_projects

    @matillion_projects.setter
    def matillion_projects(self, matillion_projects: Optional[list[MatillionProject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_projects = matillion_projects

    class Attributes(Matillion.Attributes):
        matillion_project_count: Optional[int] = Field(default=None, description="")
        matillion_projects: Optional[list[MatillionProject]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "MatillionGroup.Attributes" = Field(
        default_factory=lambda: MatillionGroup.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MatillionJob(Matillion):
    """Description"""

    type_name: str = Field(default="MatillionJob", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MatillionJob":
            raise ValueError("must be MatillionJob")
        return v

    def __setattr__(self, name, value):
        if name in MatillionJob._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MATILLION_JOB_TYPE: ClassVar[KeywordField] = KeywordField(
        "matillionJobType", "matillionJobType"
    )
    """
    Type of the job, for example: orchestration or transformation.
    """
    MATILLION_JOB_PATH: ClassVar[KeywordTextField] = KeywordTextField(
        "matillionJobPath", "matillionJobPath", "matillionJobPath.text"
    )
    """
    Path of the job within the project. Jobs can be managed at multiple folder levels within a project.
    """
    MATILLION_JOB_COMPONENT_COUNT: ClassVar[NumericField] = NumericField(
        "matillionJobComponentCount", "matillionJobComponentCount"
    )
    """
    Number of components within the job.
    """
    MATILLION_JOB_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "matillionJobSchedule", "matillionJobSchedule"
    )
    """
    How the job is scheduled, for example: weekly or monthly.
    """
    MATILLION_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "matillionProjectName", "matillionProjectName.keyword", "matillionProjectName"
    )
    """
    Simple name of the project to which the job belongs.
    """
    MATILLION_PROJECT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "matillionProjectQualifiedName",
        "matillionProjectQualifiedName",
        "matillionProjectQualifiedName.text",
    )
    """
    Unique name of the project to which the job belongs.
    """

    MATILLION_PROJECT: ClassVar[RelationField] = RelationField("matillionProject")
    """
    TBC
    """
    MATILLION_COMPONENTS: ClassVar[RelationField] = RelationField("matillionComponents")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "matillion_job_type",
        "matillion_job_path",
        "matillion_job_component_count",
        "matillion_job_schedule",
        "matillion_project_name",
        "matillion_project_qualified_name",
        "matillion_project",
        "matillion_components",
    ]

    @property
    def matillion_job_type(self) -> Optional[MatillionJobType]:
        return None if self.attributes is None else self.attributes.matillion_job_type

    @matillion_job_type.setter
    def matillion_job_type(self, matillion_job_type: Optional[MatillionJobType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job_type = matillion_job_type

    @property
    def matillion_job_path(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.matillion_job_path

    @matillion_job_path.setter
    def matillion_job_path(self, matillion_job_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job_path = matillion_job_path

    @property
    def matillion_job_component_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_job_component_count
        )

    @matillion_job_component_count.setter
    def matillion_job_component_count(
        self, matillion_job_component_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job_component_count = matillion_job_component_count

    @property
    def matillion_job_schedule(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.matillion_job_schedule
        )

    @matillion_job_schedule.setter
    def matillion_job_schedule(self, matillion_job_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job_schedule = matillion_job_schedule

    @property
    def matillion_project_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.matillion_project_name
        )

    @matillion_project_name.setter
    def matillion_project_name(self, matillion_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_project_name = matillion_project_name

    @property
    def matillion_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_project_qualified_name
        )

    @matillion_project_qualified_name.setter
    def matillion_project_qualified_name(
        self, matillion_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_project_qualified_name = (
            matillion_project_qualified_name
        )

    @property
    def matillion_project(self) -> Optional[MatillionProject]:
        return None if self.attributes is None else self.attributes.matillion_project

    @matillion_project.setter
    def matillion_project(self, matillion_project: Optional[MatillionProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_project = matillion_project

    @property
    def matillion_components(self) -> Optional[list[MatillionComponent]]:
        return None if self.attributes is None else self.attributes.matillion_components

    @matillion_components.setter
    def matillion_components(
        self, matillion_components: Optional[list[MatillionComponent]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_components = matillion_components

    class Attributes(Matillion.Attributes):
        matillion_job_type: Optional[MatillionJobType] = Field(
            default=None, description=""
        )
        matillion_job_path: Optional[str] = Field(default=None, description="")
        matillion_job_component_count: Optional[int] = Field(
            default=None, description=""
        )
        matillion_job_schedule: Optional[str] = Field(default=None, description="")
        matillion_project_name: Optional[str] = Field(default=None, description="")
        matillion_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        matillion_project: Optional[MatillionProject] = Field(
            default=None, description=""
        )  # relationship
        matillion_components: Optional[list[MatillionComponent]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "MatillionJob.Attributes" = Field(
        default_factory=lambda: MatillionJob.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MatillionProject(Matillion):
    """Description"""

    type_name: str = Field(default="MatillionProject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MatillionProject":
            raise ValueError("must be MatillionProject")
        return v

    def __setattr__(self, name, value):
        if name in MatillionProject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MATILLION_VERSIONS: ClassVar[KeywordField] = KeywordField(
        "matillionVersions", "matillionVersions"
    )
    """
    List of versions in the project.
    """
    MATILLION_ENVIRONMENTS: ClassVar[KeywordField] = KeywordField(
        "matillionEnvironments", "matillionEnvironments"
    )
    """
    List of environments in the project.
    """
    MATILLION_PROJECT_JOB_COUNT: ClassVar[NumericField] = NumericField(
        "matillionProjectJobCount", "matillionProjectJobCount"
    )
    """
    Number of jobs in the project.
    """
    MATILLION_GROUP_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "matillionGroupName", "matillionGroupName.keyword", "matillionGroupName"
    )
    """
    Simple name of the Matillion group to which the project belongs.
    """
    MATILLION_GROUP_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "matillionGroupQualifiedName",
        "matillionGroupQualifiedName",
        "matillionGroupQualifiedName.text",
    )
    """
    Unique name of the Matillion group to which the project belongs.
    """

    MATILLION_JOBS: ClassVar[RelationField] = RelationField("matillionJobs")
    """
    TBC
    """
    MATILLION_GROUP: ClassVar[RelationField] = RelationField("matillionGroup")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "matillion_versions",
        "matillion_environments",
        "matillion_project_job_count",
        "matillion_group_name",
        "matillion_group_qualified_name",
        "matillion_jobs",
        "matillion_group",
    ]

    @property
    def matillion_versions(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.matillion_versions

    @matillion_versions.setter
    def matillion_versions(self, matillion_versions: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_versions = matillion_versions

    @property
    def matillion_environments(self) -> Optional[set[str]]:
        return (
            None if self.attributes is None else self.attributes.matillion_environments
        )

    @matillion_environments.setter
    def matillion_environments(self, matillion_environments: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_environments = matillion_environments

    @property
    def matillion_project_job_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_project_job_count
        )

    @matillion_project_job_count.setter
    def matillion_project_job_count(self, matillion_project_job_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_project_job_count = matillion_project_job_count

    @property
    def matillion_group_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.matillion_group_name

    @matillion_group_name.setter
    def matillion_group_name(self, matillion_group_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_group_name = matillion_group_name

    @property
    def matillion_group_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_group_qualified_name
        )

    @matillion_group_qualified_name.setter
    def matillion_group_qualified_name(
        self, matillion_group_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_group_qualified_name = matillion_group_qualified_name

    @property
    def matillion_jobs(self) -> Optional[list[MatillionJob]]:
        return None if self.attributes is None else self.attributes.matillion_jobs

    @matillion_jobs.setter
    def matillion_jobs(self, matillion_jobs: Optional[list[MatillionJob]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_jobs = matillion_jobs

    @property
    def matillion_group(self) -> Optional[MatillionGroup]:
        return None if self.attributes is None else self.attributes.matillion_group

    @matillion_group.setter
    def matillion_group(self, matillion_group: Optional[MatillionGroup]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_group = matillion_group

    class Attributes(Matillion.Attributes):
        matillion_versions: Optional[set[str]] = Field(default=None, description="")
        matillion_environments: Optional[set[str]] = Field(default=None, description="")
        matillion_project_job_count: Optional[int] = Field(default=None, description="")
        matillion_group_name: Optional[str] = Field(default=None, description="")
        matillion_group_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        matillion_jobs: Optional[list[MatillionJob]] = Field(
            default=None, description=""
        )  # relationship
        matillion_group: Optional[MatillionGroup] = Field(
            default=None, description=""
        )  # relationship

    attributes: "MatillionProject.Attributes" = Field(
        default_factory=lambda: MatillionProject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MatillionComponent(Matillion):
    """Description"""

    type_name: str = Field(default="MatillionComponent", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MatillionComponent":
            raise ValueError("must be MatillionComponent")
        return v

    def __setattr__(self, name, value):
        if name in MatillionComponent._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MATILLION_COMPONENT_ID: ClassVar[KeywordField] = KeywordField(
        "matillionComponentId", "matillionComponentId"
    )
    """
    Unique identifier of the component in Matillion.
    """
    MATILLION_COMPONENT_IMPLEMENTATION_ID: ClassVar[KeywordField] = KeywordField(
        "matillionComponentImplementationId", "matillionComponentImplementationId"
    )
    """
    Unique identifier for the type of the component in Matillion.
    """
    MATILLION_COMPONENT_LINKED_JOB: ClassVar[KeywordField] = KeywordField(
        "matillionComponentLinkedJob", "matillionComponentLinkedJob"
    )
    """
    Job details of the job to which the component internally links.
    """
    MATILLION_COMPONENT_LAST_RUN_STATUS: ClassVar[KeywordField] = KeywordField(
        "matillionComponentLastRunStatus", "matillionComponentLastRunStatus"
    )
    """
    Latest run status of the component within a job.
    """
    MATILLION_COMPONENT_LAST_FIVE_RUN_STATUS: ClassVar[KeywordField] = KeywordField(
        "matillionComponentLastFiveRunStatus", "matillionComponentLastFiveRunStatus"
    )
    """
    Last five run statuses of the component within a job.
    """
    MATILLION_COMPONENT_SQLS: ClassVar[KeywordField] = KeywordField(
        "matillionComponentSqls", "matillionComponentSqls"
    )
    """
    SQL queries used by the component.
    """
    MATILLION_JOB_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "matillionJobName", "matillionJobName.keyword", "matillionJobName"
    )
    """
    Simple name of the job to which the component belongs.
    """
    MATILLION_JOB_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "matillionJobQualifiedName",
        "matillionJobQualifiedName",
        "matillionJobQualifiedName.text",
    )
    """
    Unique name of the job to which the component belongs.
    """

    MATILLION_PROCESS: ClassVar[RelationField] = RelationField("matillionProcess")
    """
    TBC
    """
    MATILLION_JOB: ClassVar[RelationField] = RelationField("matillionJob")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "matillion_component_id",
        "matillion_component_implementation_id",
        "matillion_component_linked_job",
        "matillion_component_last_run_status",
        "matillion_component_last_five_run_status",
        "matillion_component_sqls",
        "matillion_job_name",
        "matillion_job_qualified_name",
        "matillion_process",
        "matillion_job",
    ]

    @property
    def matillion_component_id(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.matillion_component_id
        )

    @matillion_component_id.setter
    def matillion_component_id(self, matillion_component_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component_id = matillion_component_id

    @property
    def matillion_component_implementation_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_component_implementation_id
        )

    @matillion_component_implementation_id.setter
    def matillion_component_implementation_id(
        self, matillion_component_implementation_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component_implementation_id = (
            matillion_component_implementation_id
        )

    @property
    def matillion_component_linked_job(self) -> Optional[dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_component_linked_job
        )

    @matillion_component_linked_job.setter
    def matillion_component_linked_job(
        self, matillion_component_linked_job: Optional[dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component_linked_job = matillion_component_linked_job

    @property
    def matillion_component_last_run_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_component_last_run_status
        )

    @matillion_component_last_run_status.setter
    def matillion_component_last_run_status(
        self, matillion_component_last_run_status: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component_last_run_status = (
            matillion_component_last_run_status
        )

    @property
    def matillion_component_last_five_run_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_component_last_five_run_status
        )

    @matillion_component_last_five_run_status.setter
    def matillion_component_last_five_run_status(
        self, matillion_component_last_five_run_status: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component_last_five_run_status = (
            matillion_component_last_five_run_status
        )

    @property
    def matillion_component_sqls(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_component_sqls
        )

    @matillion_component_sqls.setter
    def matillion_component_sqls(self, matillion_component_sqls: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component_sqls = matillion_component_sqls

    @property
    def matillion_job_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.matillion_job_name

    @matillion_job_name.setter
    def matillion_job_name(self, matillion_job_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job_name = matillion_job_name

    @property
    def matillion_job_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_job_qualified_name
        )

    @matillion_job_qualified_name.setter
    def matillion_job_qualified_name(self, matillion_job_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job_qualified_name = matillion_job_qualified_name

    @property
    def matillion_process(self) -> Optional[Process]:
        return None if self.attributes is None else self.attributes.matillion_process

    @matillion_process.setter
    def matillion_process(self, matillion_process: Optional[Process]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_process = matillion_process

    @property
    def matillion_job(self) -> Optional[MatillionJob]:
        return None if self.attributes is None else self.attributes.matillion_job

    @matillion_job.setter
    def matillion_job(self, matillion_job: Optional[MatillionJob]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job = matillion_job

    class Attributes(Matillion.Attributes):
        matillion_component_id: Optional[str] = Field(default=None, description="")
        matillion_component_implementation_id: Optional[str] = Field(
            default=None, description=""
        )
        matillion_component_linked_job: Optional[dict[str, str]] = Field(
            default=None, description=""
        )
        matillion_component_last_run_status: Optional[str] = Field(
            default=None, description=""
        )
        matillion_component_last_five_run_status: Optional[str] = Field(
            default=None, description=""
        )
        matillion_component_sqls: Optional[set[str]] = Field(
            default=None, description=""
        )
        matillion_job_name: Optional[str] = Field(default=None, description="")
        matillion_job_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        matillion_process: Optional[Process] = Field(
            default=None, description=""
        )  # relationship
        matillion_job: Optional[MatillionJob] = Field(
            default=None, description=""
        )  # relationship

    attributes: "MatillionComponent.Attributes" = Field(
        default_factory=lambda: MatillionComponent.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Dbt(Catalog):
    """Description"""

    type_name: str = Field(default="Dbt", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Dbt":
            raise ValueError("must be Dbt")
        return v

    def __setattr__(self, name, value):
        if name in Dbt._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DBT_ALIAS: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtAlias", "dbtAlias.keyword", "dbtAlias"
    )
    """

    """
    DBT_META: ClassVar[KeywordField] = KeywordField("dbtMeta", "dbtMeta")
    """

    """
    DBT_UNIQUE_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtUniqueId", "dbtUniqueId.keyword", "dbtUniqueId"
    )
    """

    """
    DBT_ACCOUNT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtAccountName", "dbtAccountName.keyword", "dbtAccountName"
    )
    """

    """
    DBT_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtProjectName", "dbtProjectName.keyword", "dbtProjectName"
    )
    """

    """
    DBT_PACKAGE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtPackageName", "dbtPackageName.keyword", "dbtPackageName"
    )
    """

    """
    DBT_JOB_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobName", "dbtJobName.keyword", "dbtJobName"
    )
    """

    """
    DBT_JOB_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "dbtJobSchedule", "dbtJobSchedule"
    )
    """

    """
    DBT_JOB_STATUS: ClassVar[KeywordField] = KeywordField(
        "dbtJobStatus", "dbtJobStatus"
    )
    """

    """
    DBT_JOB_SCHEDULE_CRON_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobScheduleCronHumanized",
        "dbtJobScheduleCronHumanized.keyword",
        "dbtJobScheduleCronHumanized",
    )
    """

    """
    DBT_JOB_LAST_RUN: ClassVar[NumericField] = NumericField(
        "dbtJobLastRun", "dbtJobLastRun"
    )
    """

    """
    DBT_JOB_NEXT_RUN: ClassVar[NumericField] = NumericField(
        "dbtJobNextRun", "dbtJobNextRun"
    )
    """

    """
    DBT_JOB_NEXT_RUN_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobNextRunHumanized",
        "dbtJobNextRunHumanized.keyword",
        "dbtJobNextRunHumanized",
    )
    """

    """
    DBT_ENVIRONMENT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtEnvironmentName", "dbtEnvironmentName.keyword", "dbtEnvironmentName"
    )
    """

    """
    DBT_ENVIRONMENT_DBT_VERSION: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtEnvironmentDbtVersion",
        "dbtEnvironmentDbtVersion.keyword",
        "dbtEnvironmentDbtVersion",
    )
    """

    """
    DBT_TAGS: ClassVar[KeywordField] = KeywordField("dbtTags", "dbtTags")
    """

    """
    DBT_CONNECTION_CONTEXT: ClassVar[KeywordField] = KeywordField(
        "dbtConnectionContext", "dbtConnectionContext"
    )
    """

    """
    DBT_SEMANTIC_LAYER_PROXY_URL: ClassVar[KeywordField] = KeywordField(
        "dbtSemanticLayerProxyUrl", "dbtSemanticLayerProxyUrl"
    )
    """

    """

    _convenience_properties: ClassVar[list[str]] = [
        "dbt_alias",
        "dbt_meta",
        "dbt_unique_id",
        "dbt_account_name",
        "dbt_project_name",
        "dbt_package_name",
        "dbt_job_name",
        "dbt_job_schedule",
        "dbt_job_status",
        "dbt_job_schedule_cron_humanized",
        "dbt_job_last_run",
        "dbt_job_next_run",
        "dbt_job_next_run_humanized",
        "dbt_environment_name",
        "dbt_environment_dbt_version",
        "dbt_tags",
        "dbt_connection_context",
        "dbt_semantic_layer_proxy_url",
    ]

    @property
    def dbt_alias(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_alias

    @dbt_alias.setter
    def dbt_alias(self, dbt_alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_alias = dbt_alias

    @property
    def dbt_meta(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_meta

    @dbt_meta.setter
    def dbt_meta(self, dbt_meta: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_meta = dbt_meta

    @property
    def dbt_unique_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_unique_id

    @dbt_unique_id.setter
    def dbt_unique_id(self, dbt_unique_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_unique_id = dbt_unique_id

    @property
    def dbt_account_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_account_name

    @dbt_account_name.setter
    def dbt_account_name(self, dbt_account_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_account_name = dbt_account_name

    @property
    def dbt_project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_project_name

    @dbt_project_name.setter
    def dbt_project_name(self, dbt_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_project_name = dbt_project_name

    @property
    def dbt_package_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_package_name

    @dbt_package_name.setter
    def dbt_package_name(self, dbt_package_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_package_name = dbt_package_name

    @property
    def dbt_job_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_job_name

    @dbt_job_name.setter
    def dbt_job_name(self, dbt_job_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_name = dbt_job_name

    @property
    def dbt_job_schedule(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_job_schedule

    @dbt_job_schedule.setter
    def dbt_job_schedule(self, dbt_job_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_schedule = dbt_job_schedule

    @property
    def dbt_job_status(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_job_status

    @dbt_job_status.setter
    def dbt_job_status(self, dbt_job_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_status = dbt_job_status

    @property
    def dbt_job_schedule_cron_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_job_schedule_cron_humanized
        )

    @dbt_job_schedule_cron_humanized.setter
    def dbt_job_schedule_cron_humanized(
        self, dbt_job_schedule_cron_humanized: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_schedule_cron_humanized = (
            dbt_job_schedule_cron_humanized
        )

    @property
    def dbt_job_last_run(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.dbt_job_last_run

    @dbt_job_last_run.setter
    def dbt_job_last_run(self, dbt_job_last_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_last_run = dbt_job_last_run

    @property
    def dbt_job_next_run(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.dbt_job_next_run

    @dbt_job_next_run.setter
    def dbt_job_next_run(self, dbt_job_next_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run = dbt_job_next_run

    @property
    def dbt_job_next_run_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_job_next_run_humanized
        )

    @dbt_job_next_run_humanized.setter
    def dbt_job_next_run_humanized(self, dbt_job_next_run_humanized: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run_humanized = dbt_job_next_run_humanized

    @property
    def dbt_environment_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_environment_name

    @dbt_environment_name.setter
    def dbt_environment_name(self, dbt_environment_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_name = dbt_environment_name

    @property
    def dbt_environment_dbt_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_environment_dbt_version
        )

    @dbt_environment_dbt_version.setter
    def dbt_environment_dbt_version(self, dbt_environment_dbt_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_dbt_version = dbt_environment_dbt_version

    @property
    def dbt_tags(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.dbt_tags

    @dbt_tags.setter
    def dbt_tags(self, dbt_tags: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tags = dbt_tags

    @property
    def dbt_connection_context(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dbt_connection_context
        )

    @dbt_connection_context.setter
    def dbt_connection_context(self, dbt_connection_context: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_connection_context = dbt_connection_context

    @property
    def dbt_semantic_layer_proxy_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_semantic_layer_proxy_url
        )

    @dbt_semantic_layer_proxy_url.setter
    def dbt_semantic_layer_proxy_url(self, dbt_semantic_layer_proxy_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_semantic_layer_proxy_url = dbt_semantic_layer_proxy_url

    class Attributes(Catalog.Attributes):
        dbt_alias: Optional[str] = Field(default=None, description="")
        dbt_meta: Optional[str] = Field(default=None, description="")
        dbt_unique_id: Optional[str] = Field(default=None, description="")
        dbt_account_name: Optional[str] = Field(default=None, description="")
        dbt_project_name: Optional[str] = Field(default=None, description="")
        dbt_package_name: Optional[str] = Field(default=None, description="")
        dbt_job_name: Optional[str] = Field(default=None, description="")
        dbt_job_schedule: Optional[str] = Field(default=None, description="")
        dbt_job_status: Optional[str] = Field(default=None, description="")
        dbt_job_schedule_cron_humanized: Optional[str] = Field(
            default=None, description=""
        )
        dbt_job_last_run: Optional[datetime] = Field(default=None, description="")
        dbt_job_next_run: Optional[datetime] = Field(default=None, description="")
        dbt_job_next_run_humanized: Optional[str] = Field(default=None, description="")
        dbt_environment_name: Optional[str] = Field(default=None, description="")
        dbt_environment_dbt_version: Optional[str] = Field(default=None, description="")
        dbt_tags: Optional[set[str]] = Field(default=None, description="")
        dbt_connection_context: Optional[str] = Field(default=None, description="")
        dbt_semantic_layer_proxy_url: Optional[str] = Field(
            default=None, description=""
        )

    attributes: "Dbt.Attributes" = Field(
        default_factory=lambda: Dbt.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtModelColumn(Dbt):
    """Description"""

    type_name: str = Field(default="DbtModelColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtModelColumn":
            raise ValueError("must be DbtModelColumn")
        return v

    def __setattr__(self, name, value):
        if name in DbtModelColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DBT_MODEL_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtModelQualifiedName", "dbtModelQualifiedName", "dbtModelQualifiedName.text"
    )
    """

    """
    DBT_MODEL_COLUMN_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "dbtModelColumnDataType", "dbtModelColumnDataType"
    )
    """

    """
    DBT_MODEL_COLUMN_ORDER: ClassVar[NumericField] = NumericField(
        "dbtModelColumnOrder", "dbtModelColumnOrder"
    )
    """

    """

    SQL_COLUMN: ClassVar[RelationField] = RelationField("sqlColumn")
    """
    TBC
    """
    DBT_MODEL: ClassVar[RelationField] = RelationField("dbtModel")
    """
    TBC
    """
    DBT_MODEL_COLUMN_SQL_COLUMNS: ClassVar[RelationField] = RelationField(
        "dbtModelColumnSqlColumns"
    )
    """
    TBC
    """
    DBT_TESTS: ClassVar[RelationField] = RelationField("dbtTests")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "dbt_model_qualified_name",
        "dbt_model_column_data_type",
        "dbt_model_column_order",
        "sql_column",
        "dbt_model",
        "dbt_model_column_sql_columns",
        "dbt_tests",
    ]

    @property
    def dbt_model_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_qualified_name
        )

    @dbt_model_qualified_name.setter
    def dbt_model_qualified_name(self, dbt_model_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_qualified_name = dbt_model_qualified_name

    @property
    def dbt_model_column_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_column_data_type
        )

    @dbt_model_column_data_type.setter
    def dbt_model_column_data_type(self, dbt_model_column_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_column_data_type = dbt_model_column_data_type

    @property
    def dbt_model_column_order(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.dbt_model_column_order
        )

    @dbt_model_column_order.setter
    def dbt_model_column_order(self, dbt_model_column_order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_column_order = dbt_model_column_order

    @property
    def sql_column(self) -> Optional[Column]:
        return None if self.attributes is None else self.attributes.sql_column

    @sql_column.setter
    def sql_column(self, sql_column: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_column = sql_column

    @property
    def dbt_model(self) -> Optional[DbtModel]:
        return None if self.attributes is None else self.attributes.dbt_model

    @dbt_model.setter
    def dbt_model(self, dbt_model: Optional[DbtModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model = dbt_model

    @property
    def dbt_model_column_sql_columns(self) -> Optional[list[Column]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_column_sql_columns
        )

    @dbt_model_column_sql_columns.setter
    def dbt_model_column_sql_columns(
        self, dbt_model_column_sql_columns: Optional[list[Column]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_column_sql_columns = dbt_model_column_sql_columns

    @property
    def dbt_tests(self) -> Optional[list[DbtTest]]:
        return None if self.attributes is None else self.attributes.dbt_tests

    @dbt_tests.setter
    def dbt_tests(self, dbt_tests: Optional[list[DbtTest]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tests = dbt_tests

    class Attributes(Dbt.Attributes):
        dbt_model_qualified_name: Optional[str] = Field(default=None, description="")
        dbt_model_column_data_type: Optional[str] = Field(default=None, description="")
        dbt_model_column_order: Optional[int] = Field(default=None, description="")
        sql_column: Optional[Column] = Field(
            default=None, description=""
        )  # relationship
        dbt_model: Optional[DbtModel] = Field(
            default=None, description=""
        )  # relationship
        dbt_model_column_sql_columns: Optional[list[Column]] = Field(
            default=None, description=""
        )  # relationship
        dbt_tests: Optional[list[DbtTest]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "DbtModelColumn.Attributes" = Field(
        default_factory=lambda: DbtModelColumn.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtTest(Dbt):
    """Description"""

    type_name: str = Field(default="DbtTest", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtTest":
            raise ValueError("must be DbtTest")
        return v

    def __setattr__(self, name, value):
        if name in DbtTest._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DBT_TEST_STATUS: ClassVar[KeywordField] = KeywordField(
        "dbtTestStatus", "dbtTestStatus"
    )
    """
    Details of the results of the test. For errors, it reads "ERROR".
    """
    DBT_TEST_STATE: ClassVar[KeywordField] = KeywordField(
        "dbtTestState", "dbtTestState"
    )
    """
    Test results. Can be one of, in order of severity, "error", "fail", "warn", "pass".
    """
    DBT_TEST_ERROR: ClassVar[KeywordField] = KeywordField(
        "dbtTestError", "dbtTestError"
    )
    """
    Error message in the case of state being "error".
    """
    DBT_TEST_RAW_SQL: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtTestRawSQL", "dbtTestRawSQL", "dbtTestRawSQL.text"
    )
    """
    Raw SQL of the test.
    """
    DBT_TEST_COMPILED_SQL: ClassVar[KeywordField] = KeywordField(
        "dbtTestCompiledSQL", "dbtTestCompiledSQL"
    )
    """
    Compiled SQL of the test.
    """
    DBT_TEST_RAW_CODE: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtTestRawCode", "dbtTestRawCode", "dbtTestRawCode.text"
    )
    """
    Raw code of the test (when the test is defined using Python).
    """
    DBT_TEST_COMPILED_CODE: ClassVar[KeywordField] = KeywordField(
        "dbtTestCompiledCode", "dbtTestCompiledCode"
    )
    """
    Compiled code of the test (when the test is defined using Python).
    """
    DBT_TEST_LANGUAGE: ClassVar[KeywordField] = KeywordField(
        "dbtTestLanguage", "dbtTestLanguage"
    )
    """
    Language in which the test is written, for example: SQL or Python.
    """

    DBT_SOURCES: ClassVar[RelationField] = RelationField("dbtSources")
    """
    TBC
    """
    SQL_ASSETS: ClassVar[RelationField] = RelationField("sqlAssets")
    """
    TBC
    """
    DBT_MODELS: ClassVar[RelationField] = RelationField("dbtModels")
    """
    TBC
    """
    DBT_MODEL_COLUMNS: ClassVar[RelationField] = RelationField("dbtModelColumns")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "dbt_test_status",
        "dbt_test_state",
        "dbt_test_error",
        "dbt_test_raw_s_q_l",
        "dbt_test_compiled_s_q_l",
        "dbt_test_raw_code",
        "dbt_test_compiled_code",
        "dbt_test_language",
        "dbt_sources",
        "sql_assets",
        "dbt_models",
        "dbt_model_columns",
    ]

    @property
    def dbt_test_status(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_test_status

    @dbt_test_status.setter
    def dbt_test_status(self, dbt_test_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_test_status = dbt_test_status

    @property
    def dbt_test_state(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_test_state

    @dbt_test_state.setter
    def dbt_test_state(self, dbt_test_state: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_test_state = dbt_test_state

    @property
    def dbt_test_error(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_test_error

    @dbt_test_error.setter
    def dbt_test_error(self, dbt_test_error: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_test_error = dbt_test_error

    @property
    def dbt_test_raw_s_q_l(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_test_raw_s_q_l

    @dbt_test_raw_s_q_l.setter
    def dbt_test_raw_s_q_l(self, dbt_test_raw_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_test_raw_s_q_l = dbt_test_raw_s_q_l

    @property
    def dbt_test_compiled_s_q_l(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dbt_test_compiled_s_q_l
        )

    @dbt_test_compiled_s_q_l.setter
    def dbt_test_compiled_s_q_l(self, dbt_test_compiled_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_test_compiled_s_q_l = dbt_test_compiled_s_q_l

    @property
    def dbt_test_raw_code(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_test_raw_code

    @dbt_test_raw_code.setter
    def dbt_test_raw_code(self, dbt_test_raw_code: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_test_raw_code = dbt_test_raw_code

    @property
    def dbt_test_compiled_code(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dbt_test_compiled_code
        )

    @dbt_test_compiled_code.setter
    def dbt_test_compiled_code(self, dbt_test_compiled_code: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_test_compiled_code = dbt_test_compiled_code

    @property
    def dbt_test_language(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_test_language

    @dbt_test_language.setter
    def dbt_test_language(self, dbt_test_language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_test_language = dbt_test_language

    @property
    def dbt_sources(self) -> Optional[list[DbtSource]]:
        return None if self.attributes is None else self.attributes.dbt_sources

    @dbt_sources.setter
    def dbt_sources(self, dbt_sources: Optional[list[DbtSource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_sources = dbt_sources

    @property
    def sql_assets(self) -> Optional[list[SQL]]:
        return None if self.attributes is None else self.attributes.sql_assets

    @sql_assets.setter
    def sql_assets(self, sql_assets: Optional[list[SQL]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_assets = sql_assets

    @property
    def dbt_models(self) -> Optional[list[DbtModel]]:
        return None if self.attributes is None else self.attributes.dbt_models

    @dbt_models.setter
    def dbt_models(self, dbt_models: Optional[list[DbtModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_models = dbt_models

    @property
    def dbt_model_columns(self) -> Optional[list[DbtModelColumn]]:
        return None if self.attributes is None else self.attributes.dbt_model_columns

    @dbt_model_columns.setter
    def dbt_model_columns(self, dbt_model_columns: Optional[list[DbtModelColumn]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_columns = dbt_model_columns

    class Attributes(Dbt.Attributes):
        dbt_test_status: Optional[str] = Field(default=None, description="")
        dbt_test_state: Optional[str] = Field(default=None, description="")
        dbt_test_error: Optional[str] = Field(default=None, description="")
        dbt_test_raw_s_q_l: Optional[str] = Field(default=None, description="")
        dbt_test_compiled_s_q_l: Optional[str] = Field(default=None, description="")
        dbt_test_raw_code: Optional[str] = Field(default=None, description="")
        dbt_test_compiled_code: Optional[str] = Field(default=None, description="")
        dbt_test_language: Optional[str] = Field(default=None, description="")
        dbt_sources: Optional[list[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        sql_assets: Optional[list[SQL]] = Field(
            default=None, description=""
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        dbt_model_columns: Optional[list[DbtModelColumn]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "DbtTest.Attributes" = Field(
        default_factory=lambda: DbtTest.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtModel(Dbt):
    """Description"""

    type_name: str = Field(default="DbtModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtModel":
            raise ValueError("must be DbtModel")
        return v

    def __setattr__(self, name, value):
        if name in DbtModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DBT_STATUS: ClassVar[KeywordField] = KeywordField("dbtStatus", "dbtStatus")
    """

    """
    DBT_ERROR: ClassVar[KeywordField] = KeywordField("dbtError", "dbtError")
    """

    """
    DBT_RAW_SQL: ClassVar[KeywordField] = KeywordField("dbtRawSQL", "dbtRawSQL")
    """

    """
    DBT_COMPILED_SQL: ClassVar[KeywordField] = KeywordField(
        "dbtCompiledSQL", "dbtCompiledSQL"
    )
    """

    """
    DBT_STATS: ClassVar[KeywordField] = KeywordField("dbtStats", "dbtStats")
    """

    """
    DBT_MATERIALIZATION_TYPE: ClassVar[KeywordField] = KeywordField(
        "dbtMaterializationType", "dbtMaterializationType"
    )
    """

    """
    DBT_MODEL_COMPILE_STARTED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelCompileStartedAt", "dbtModelCompileStartedAt"
    )
    """

    """
    DBT_MODEL_COMPILE_COMPLETED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelCompileCompletedAt", "dbtModelCompileCompletedAt"
    )
    """

    """
    DBT_MODEL_EXECUTE_STARTED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelExecuteStartedAt", "dbtModelExecuteStartedAt"
    )
    """

    """
    DBT_MODEL_EXECUTE_COMPLETED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelExecuteCompletedAt", "dbtModelExecuteCompletedAt"
    )
    """

    """
    DBT_MODEL_EXECUTION_TIME: ClassVar[NumericField] = NumericField(
        "dbtModelExecutionTime", "dbtModelExecutionTime"
    )
    """

    """
    DBT_MODEL_RUN_GENERATED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelRunGeneratedAt", "dbtModelRunGeneratedAt"
    )
    """

    """
    DBT_MODEL_RUN_ELAPSED_TIME: ClassVar[NumericField] = NumericField(
        "dbtModelRunElapsedTime", "dbtModelRunElapsedTime"
    )
    """

    """

    DBT_METRICS: ClassVar[RelationField] = RelationField("dbtMetrics")
    """
    TBC
    """
    DBT_TESTS: ClassVar[RelationField] = RelationField("dbtTests")
    """
    TBC
    """
    DBT_MODEL_SQL_ASSETS: ClassVar[RelationField] = RelationField("dbtModelSqlAssets")
    """
    TBC
    """
    DBT_MODEL_COLUMNS: ClassVar[RelationField] = RelationField("dbtModelColumns")
    """
    TBC
    """
    SQL_ASSET: ClassVar[RelationField] = RelationField("sqlAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "dbt_status",
        "dbt_error",
        "dbt_raw_s_q_l",
        "dbt_compiled_s_q_l",
        "dbt_stats",
        "dbt_materialization_type",
        "dbt_model_compile_started_at",
        "dbt_model_compile_completed_at",
        "dbt_model_execute_started_at",
        "dbt_model_execute_completed_at",
        "dbt_model_execution_time",
        "dbt_model_run_generated_at",
        "dbt_model_run_elapsed_time",
        "dbt_metrics",
        "dbt_tests",
        "dbt_model_sql_assets",
        "dbt_model_columns",
        "sql_asset",
    ]

    @property
    def dbt_status(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_status

    @dbt_status.setter
    def dbt_status(self, dbt_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_status = dbt_status

    @property
    def dbt_error(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_error

    @dbt_error.setter
    def dbt_error(self, dbt_error: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_error = dbt_error

    @property
    def dbt_raw_s_q_l(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_raw_s_q_l

    @dbt_raw_s_q_l.setter
    def dbt_raw_s_q_l(self, dbt_raw_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_raw_s_q_l = dbt_raw_s_q_l

    @property
    def dbt_compiled_s_q_l(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_compiled_s_q_l

    @dbt_compiled_s_q_l.setter
    def dbt_compiled_s_q_l(self, dbt_compiled_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_compiled_s_q_l = dbt_compiled_s_q_l

    @property
    def dbt_stats(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_stats

    @dbt_stats.setter
    def dbt_stats(self, dbt_stats: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_stats = dbt_stats

    @property
    def dbt_materialization_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_materialization_type
        )

    @dbt_materialization_type.setter
    def dbt_materialization_type(self, dbt_materialization_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_materialization_type = dbt_materialization_type

    @property
    def dbt_model_compile_started_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_compile_started_at
        )

    @dbt_model_compile_started_at.setter
    def dbt_model_compile_started_at(
        self, dbt_model_compile_started_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_compile_started_at = dbt_model_compile_started_at

    @property
    def dbt_model_compile_completed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_compile_completed_at
        )

    @dbt_model_compile_completed_at.setter
    def dbt_model_compile_completed_at(
        self, dbt_model_compile_completed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_compile_completed_at = dbt_model_compile_completed_at

    @property
    def dbt_model_execute_started_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_execute_started_at
        )

    @dbt_model_execute_started_at.setter
    def dbt_model_execute_started_at(
        self, dbt_model_execute_started_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_execute_started_at = dbt_model_execute_started_at

    @property
    def dbt_model_execute_completed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_execute_completed_at
        )

    @dbt_model_execute_completed_at.setter
    def dbt_model_execute_completed_at(
        self, dbt_model_execute_completed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_execute_completed_at = dbt_model_execute_completed_at

    @property
    def dbt_model_execution_time(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_execution_time
        )

    @dbt_model_execution_time.setter
    def dbt_model_execution_time(self, dbt_model_execution_time: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_execution_time = dbt_model_execution_time

    @property
    def dbt_model_run_generated_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_run_generated_at
        )

    @dbt_model_run_generated_at.setter
    def dbt_model_run_generated_at(
        self, dbt_model_run_generated_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_run_generated_at = dbt_model_run_generated_at

    @property
    def dbt_model_run_elapsed_time(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_run_elapsed_time
        )

    @dbt_model_run_elapsed_time.setter
    def dbt_model_run_elapsed_time(self, dbt_model_run_elapsed_time: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_run_elapsed_time = dbt_model_run_elapsed_time

    @property
    def dbt_metrics(self) -> Optional[list[DbtMetric]]:
        return None if self.attributes is None else self.attributes.dbt_metrics

    @dbt_metrics.setter
    def dbt_metrics(self, dbt_metrics: Optional[list[DbtMetric]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_metrics = dbt_metrics

    @property
    def dbt_tests(self) -> Optional[list[DbtTest]]:
        return None if self.attributes is None else self.attributes.dbt_tests

    @dbt_tests.setter
    def dbt_tests(self, dbt_tests: Optional[list[DbtTest]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tests = dbt_tests

    @property
    def dbt_model_sql_assets(self) -> Optional[list[SQL]]:
        return None if self.attributes is None else self.attributes.dbt_model_sql_assets

    @dbt_model_sql_assets.setter
    def dbt_model_sql_assets(self, dbt_model_sql_assets: Optional[list[SQL]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_sql_assets = dbt_model_sql_assets

    @property
    def dbt_model_columns(self) -> Optional[list[DbtModelColumn]]:
        return None if self.attributes is None else self.attributes.dbt_model_columns

    @dbt_model_columns.setter
    def dbt_model_columns(self, dbt_model_columns: Optional[list[DbtModelColumn]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_columns = dbt_model_columns

    @property
    def sql_asset(self) -> Optional[SQL]:
        return None if self.attributes is None else self.attributes.sql_asset

    @sql_asset.setter
    def sql_asset(self, sql_asset: Optional[SQL]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_asset = sql_asset

    class Attributes(Dbt.Attributes):
        dbt_status: Optional[str] = Field(default=None, description="")
        dbt_error: Optional[str] = Field(default=None, description="")
        dbt_raw_s_q_l: Optional[str] = Field(default=None, description="")
        dbt_compiled_s_q_l: Optional[str] = Field(default=None, description="")
        dbt_stats: Optional[str] = Field(default=None, description="")
        dbt_materialization_type: Optional[str] = Field(default=None, description="")
        dbt_model_compile_started_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dbt_model_compile_completed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dbt_model_execute_started_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dbt_model_execute_completed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dbt_model_execution_time: Optional[float] = Field(default=None, description="")
        dbt_model_run_generated_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dbt_model_run_elapsed_time: Optional[float] = Field(
            default=None, description=""
        )
        dbt_metrics: Optional[list[DbtMetric]] = Field(
            default=None, description=""
        )  # relationship
        dbt_tests: Optional[list[DbtTest]] = Field(
            default=None, description=""
        )  # relationship
        dbt_model_sql_assets: Optional[list[SQL]] = Field(
            default=None, description=""
        )  # relationship
        dbt_model_columns: Optional[list[DbtModelColumn]] = Field(
            default=None, description=""
        )  # relationship
        sql_asset: Optional[SQL] = Field(default=None, description="")  # relationship

    attributes: "DbtModel.Attributes" = Field(
        default_factory=lambda: DbtModel.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtMetric(Dbt):
    """Description"""

    type_name: str = Field(default="DbtMetric", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtMetric":
            raise ValueError("must be DbtMetric")
        return v

    def __setattr__(self, name, value):
        if name in DbtMetric._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DBT_METRIC_FILTERS: ClassVar[KeywordField] = KeywordField(
        "dbtMetricFilters", "dbtMetricFilters"
    )
    """

    """
    DBT_ALIAS: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtAlias", "dbtAlias.keyword", "dbtAlias"
    )
    """

    """
    DBT_META: ClassVar[KeywordField] = KeywordField("dbtMeta", "dbtMeta")
    """

    """
    DBT_UNIQUE_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtUniqueId", "dbtUniqueId.keyword", "dbtUniqueId"
    )
    """

    """
    DBT_ACCOUNT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtAccountName", "dbtAccountName.keyword", "dbtAccountName"
    )
    """

    """
    DBT_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtProjectName", "dbtProjectName.keyword", "dbtProjectName"
    )
    """

    """
    DBT_PACKAGE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtPackageName", "dbtPackageName.keyword", "dbtPackageName"
    )
    """

    """
    DBT_JOB_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobName", "dbtJobName.keyword", "dbtJobName"
    )
    """

    """
    DBT_JOB_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "dbtJobSchedule", "dbtJobSchedule"
    )
    """

    """
    DBT_JOB_STATUS: ClassVar[KeywordField] = KeywordField(
        "dbtJobStatus", "dbtJobStatus"
    )
    """

    """
    DBT_JOB_SCHEDULE_CRON_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobScheduleCronHumanized",
        "dbtJobScheduleCronHumanized.keyword",
        "dbtJobScheduleCronHumanized",
    )
    """

    """
    DBT_JOB_LAST_RUN: ClassVar[NumericField] = NumericField(
        "dbtJobLastRun", "dbtJobLastRun"
    )
    """

    """
    DBT_JOB_NEXT_RUN: ClassVar[NumericField] = NumericField(
        "dbtJobNextRun", "dbtJobNextRun"
    )
    """

    """
    DBT_JOB_NEXT_RUN_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobNextRunHumanized",
        "dbtJobNextRunHumanized.keyword",
        "dbtJobNextRunHumanized",
    )
    """

    """
    DBT_ENVIRONMENT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtEnvironmentName", "dbtEnvironmentName.keyword", "dbtEnvironmentName"
    )
    """

    """
    DBT_ENVIRONMENT_DBT_VERSION: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtEnvironmentDbtVersion",
        "dbtEnvironmentDbtVersion.keyword",
        "dbtEnvironmentDbtVersion",
    )
    """

    """
    DBT_TAGS: ClassVar[KeywordField] = KeywordField("dbtTags", "dbtTags")
    """

    """
    DBT_CONNECTION_CONTEXT: ClassVar[KeywordField] = KeywordField(
        "dbtConnectionContext", "dbtConnectionContext"
    )
    """

    """
    DBT_SEMANTIC_LAYER_PROXY_URL: ClassVar[KeywordField] = KeywordField(
        "dbtSemanticLayerProxyUrl", "dbtSemanticLayerProxyUrl"
    )
    """

    """
    METRIC_TYPE: ClassVar[KeywordField] = KeywordField("metricType", "metricType")
    """
    Type of the metric.
    """
    METRIC_SQL: ClassVar[KeywordField] = KeywordField("metricSQL", "metricSQL")
    """
    SQL query used to compute the metric.
    """
    METRIC_FILTERS: ClassVar[TextField] = TextField("metricFilters", "metricFilters")
    """
    Filters to be applied to the metric query.
    """
    METRIC_TIME_GRAINS: ClassVar[TextField] = TextField(
        "metricTimeGrains", "metricTimeGrains"
    )
    """
    List of time grains to be applied to the metric query.
    """

    METRIC_TIMESTAMP_COLUMN: ClassVar[RelationField] = RelationField(
        "metricTimestampColumn"
    )
    """
    TBC
    """
    DBT_MODEL: ClassVar[RelationField] = RelationField("dbtModel")
    """
    TBC
    """
    ASSETS: ClassVar[RelationField] = RelationField("assets")
    """
    TBC
    """
    METRIC_DIMENSION_COLUMNS: ClassVar[RelationField] = RelationField(
        "metricDimensionColumns"
    )
    """
    TBC
    """
    DBT_METRIC_FILTER_COLUMNS: ClassVar[RelationField] = RelationField(
        "dbtMetricFilterColumns"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "dbt_metric_filters",
        "dbt_alias",
        "dbt_meta",
        "dbt_unique_id",
        "dbt_account_name",
        "dbt_project_name",
        "dbt_package_name",
        "dbt_job_name",
        "dbt_job_schedule",
        "dbt_job_status",
        "dbt_job_schedule_cron_humanized",
        "dbt_job_last_run",
        "dbt_job_next_run",
        "dbt_job_next_run_humanized",
        "dbt_environment_name",
        "dbt_environment_dbt_version",
        "dbt_tags",
        "dbt_connection_context",
        "dbt_semantic_layer_proxy_url",
        "metric_type",
        "metric_s_q_l",
        "metric_filters",
        "metric_time_grains",
        "metric_timestamp_column",
        "dbt_model",
        "assets",
        "metric_dimension_columns",
        "dbt_metric_filter_columns",
    ]

    @property
    def dbt_metric_filters(self) -> Optional[list[DbtMetricFilter]]:
        return None if self.attributes is None else self.attributes.dbt_metric_filters

    @dbt_metric_filters.setter
    def dbt_metric_filters(self, dbt_metric_filters: Optional[list[DbtMetricFilter]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_metric_filters = dbt_metric_filters

    @property
    def dbt_alias(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_alias

    @dbt_alias.setter
    def dbt_alias(self, dbt_alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_alias = dbt_alias

    @property
    def dbt_meta(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_meta

    @dbt_meta.setter
    def dbt_meta(self, dbt_meta: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_meta = dbt_meta

    @property
    def dbt_unique_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_unique_id

    @dbt_unique_id.setter
    def dbt_unique_id(self, dbt_unique_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_unique_id = dbt_unique_id

    @property
    def dbt_account_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_account_name

    @dbt_account_name.setter
    def dbt_account_name(self, dbt_account_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_account_name = dbt_account_name

    @property
    def dbt_project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_project_name

    @dbt_project_name.setter
    def dbt_project_name(self, dbt_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_project_name = dbt_project_name

    @property
    def dbt_package_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_package_name

    @dbt_package_name.setter
    def dbt_package_name(self, dbt_package_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_package_name = dbt_package_name

    @property
    def dbt_job_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_job_name

    @dbt_job_name.setter
    def dbt_job_name(self, dbt_job_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_name = dbt_job_name

    @property
    def dbt_job_schedule(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_job_schedule

    @dbt_job_schedule.setter
    def dbt_job_schedule(self, dbt_job_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_schedule = dbt_job_schedule

    @property
    def dbt_job_status(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_job_status

    @dbt_job_status.setter
    def dbt_job_status(self, dbt_job_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_status = dbt_job_status

    @property
    def dbt_job_schedule_cron_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_job_schedule_cron_humanized
        )

    @dbt_job_schedule_cron_humanized.setter
    def dbt_job_schedule_cron_humanized(
        self, dbt_job_schedule_cron_humanized: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_schedule_cron_humanized = (
            dbt_job_schedule_cron_humanized
        )

    @property
    def dbt_job_last_run(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.dbt_job_last_run

    @dbt_job_last_run.setter
    def dbt_job_last_run(self, dbt_job_last_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_last_run = dbt_job_last_run

    @property
    def dbt_job_next_run(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.dbt_job_next_run

    @dbt_job_next_run.setter
    def dbt_job_next_run(self, dbt_job_next_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run = dbt_job_next_run

    @property
    def dbt_job_next_run_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_job_next_run_humanized
        )

    @dbt_job_next_run_humanized.setter
    def dbt_job_next_run_humanized(self, dbt_job_next_run_humanized: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run_humanized = dbt_job_next_run_humanized

    @property
    def dbt_environment_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_environment_name

    @dbt_environment_name.setter
    def dbt_environment_name(self, dbt_environment_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_name = dbt_environment_name

    @property
    def dbt_environment_dbt_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_environment_dbt_version
        )

    @dbt_environment_dbt_version.setter
    def dbt_environment_dbt_version(self, dbt_environment_dbt_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_dbt_version = dbt_environment_dbt_version

    @property
    def dbt_tags(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.dbt_tags

    @dbt_tags.setter
    def dbt_tags(self, dbt_tags: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tags = dbt_tags

    @property
    def dbt_connection_context(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dbt_connection_context
        )

    @dbt_connection_context.setter
    def dbt_connection_context(self, dbt_connection_context: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_connection_context = dbt_connection_context

    @property
    def dbt_semantic_layer_proxy_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_semantic_layer_proxy_url
        )

    @dbt_semantic_layer_proxy_url.setter
    def dbt_semantic_layer_proxy_url(self, dbt_semantic_layer_proxy_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_semantic_layer_proxy_url = dbt_semantic_layer_proxy_url

    @property
    def metric_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metric_type

    @metric_type.setter
    def metric_type(self, metric_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_type = metric_type

    @property
    def metric_s_q_l(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metric_s_q_l

    @metric_s_q_l.setter
    def metric_s_q_l(self, metric_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_s_q_l = metric_s_q_l

    @property
    def metric_filters(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metric_filters

    @metric_filters.setter
    def metric_filters(self, metric_filters: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_filters = metric_filters

    @property
    def metric_time_grains(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.metric_time_grains

    @metric_time_grains.setter
    def metric_time_grains(self, metric_time_grains: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_time_grains = metric_time_grains

    @property
    def metric_timestamp_column(self) -> Optional[Column]:
        return (
            None if self.attributes is None else self.attributes.metric_timestamp_column
        )

    @metric_timestamp_column.setter
    def metric_timestamp_column(self, metric_timestamp_column: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_timestamp_column = metric_timestamp_column

    @property
    def dbt_model(self) -> Optional[DbtModel]:
        return None if self.attributes is None else self.attributes.dbt_model

    @dbt_model.setter
    def dbt_model(self, dbt_model: Optional[DbtModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model = dbt_model

    @property
    def assets(self) -> Optional[list[Asset]]:
        return None if self.attributes is None else self.attributes.assets

    @assets.setter
    def assets(self, assets: Optional[list[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.assets = assets

    @property
    def metric_dimension_columns(self) -> Optional[list[Column]]:
        return (
            None
            if self.attributes is None
            else self.attributes.metric_dimension_columns
        )

    @metric_dimension_columns.setter
    def metric_dimension_columns(
        self, metric_dimension_columns: Optional[list[Column]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_dimension_columns = metric_dimension_columns

    @property
    def dbt_metric_filter_columns(self) -> Optional[list[Column]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_metric_filter_columns
        )

    @dbt_metric_filter_columns.setter
    def dbt_metric_filter_columns(
        self, dbt_metric_filter_columns: Optional[list[Column]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_metric_filter_columns = dbt_metric_filter_columns

    class Attributes(Dbt.Attributes):
        dbt_metric_filters: Optional[list[DbtMetricFilter]] = Field(
            default=None, description=""
        )
        dbt_alias: Optional[str] = Field(default=None, description="")
        dbt_meta: Optional[str] = Field(default=None, description="")
        dbt_unique_id: Optional[str] = Field(default=None, description="")
        dbt_account_name: Optional[str] = Field(default=None, description="")
        dbt_project_name: Optional[str] = Field(default=None, description="")
        dbt_package_name: Optional[str] = Field(default=None, description="")
        dbt_job_name: Optional[str] = Field(default=None, description="")
        dbt_job_schedule: Optional[str] = Field(default=None, description="")
        dbt_job_status: Optional[str] = Field(default=None, description="")
        dbt_job_schedule_cron_humanized: Optional[str] = Field(
            default=None, description=""
        )
        dbt_job_last_run: Optional[datetime] = Field(default=None, description="")
        dbt_job_next_run: Optional[datetime] = Field(default=None, description="")
        dbt_job_next_run_humanized: Optional[str] = Field(default=None, description="")
        dbt_environment_name: Optional[str] = Field(default=None, description="")
        dbt_environment_dbt_version: Optional[str] = Field(default=None, description="")
        dbt_tags: Optional[set[str]] = Field(default=None, description="")
        dbt_connection_context: Optional[str] = Field(default=None, description="")
        dbt_semantic_layer_proxy_url: Optional[str] = Field(
            default=None, description=""
        )
        metric_type: Optional[str] = Field(default=None, description="")
        metric_s_q_l: Optional[str] = Field(default=None, description="")
        metric_filters: Optional[str] = Field(default=None, description="")
        metric_time_grains: Optional[set[str]] = Field(default=None, description="")
        metric_timestamp_column: Optional[Column] = Field(
            default=None, description=""
        )  # relationship
        dbt_model: Optional[DbtModel] = Field(
            default=None, description=""
        )  # relationship
        assets: Optional[list[Asset]] = Field(
            default=None, description=""
        )  # relationship
        metric_dimension_columns: Optional[list[Column]] = Field(
            default=None, description=""
        )  # relationship
        dbt_metric_filter_columns: Optional[list[Column]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "DbtMetric.Attributes" = Field(
        default_factory=lambda: DbtMetric.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtSource(Dbt):
    """Description"""

    type_name: str = Field(default="DbtSource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtSource":
            raise ValueError("must be DbtSource")
        return v

    def __setattr__(self, name, value):
        if name in DbtSource._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DBT_STATE: ClassVar[KeywordField] = KeywordField("dbtState", "dbtState")
    """

    """
    DBT_FRESHNESS_CRITERIA: ClassVar[KeywordField] = KeywordField(
        "dbtFreshnessCriteria", "dbtFreshnessCriteria"
    )
    """

    """

    SQL_ASSETS: ClassVar[RelationField] = RelationField("sqlAssets")
    """
    TBC
    """
    DBT_TESTS: ClassVar[RelationField] = RelationField("dbtTests")
    """
    TBC
    """
    SQL_ASSET: ClassVar[RelationField] = RelationField("sqlAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "dbt_state",
        "dbt_freshness_criteria",
        "sql_assets",
        "dbt_tests",
        "sql_asset",
    ]

    @property
    def dbt_state(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_state

    @dbt_state.setter
    def dbt_state(self, dbt_state: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_state = dbt_state

    @property
    def dbt_freshness_criteria(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dbt_freshness_criteria
        )

    @dbt_freshness_criteria.setter
    def dbt_freshness_criteria(self, dbt_freshness_criteria: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_freshness_criteria = dbt_freshness_criteria

    @property
    def sql_assets(self) -> Optional[list[SQL]]:
        return None if self.attributes is None else self.attributes.sql_assets

    @sql_assets.setter
    def sql_assets(self, sql_assets: Optional[list[SQL]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_assets = sql_assets

    @property
    def dbt_tests(self) -> Optional[list[DbtTest]]:
        return None if self.attributes is None else self.attributes.dbt_tests

    @dbt_tests.setter
    def dbt_tests(self, dbt_tests: Optional[list[DbtTest]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tests = dbt_tests

    @property
    def sql_asset(self) -> Optional[SQL]:
        return None if self.attributes is None else self.attributes.sql_asset

    @sql_asset.setter
    def sql_asset(self, sql_asset: Optional[SQL]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_asset = sql_asset

    class Attributes(Dbt.Attributes):
        dbt_state: Optional[str] = Field(default=None, description="")
        dbt_freshness_criteria: Optional[str] = Field(default=None, description="")
        sql_assets: Optional[list[SQL]] = Field(
            default=None, description=""
        )  # relationship
        dbt_tests: Optional[list[DbtTest]] = Field(
            default=None, description=""
        )  # relationship
        sql_asset: Optional[SQL] = Field(default=None, description="")  # relationship

    attributes: "DbtSource.Attributes" = Field(
        default_factory=lambda: DbtSource.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SchemaRegistry(Catalog):
    """Description"""

    type_name: str = Field(default="SchemaRegistry", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SchemaRegistry":
            raise ValueError("must be SchemaRegistry")
        return v

    def __setattr__(self, name, value):
        if name in SchemaRegistry._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SCHEMA_REGISTRY_SCHEMA_TYPE: ClassVar[KeywordField] = KeywordField(
        "schemaRegistrySchemaType", "schemaRegistrySchemaType"
    )
    """
    Type of language or specification used to define the schema, for example: JSON, Protobuf, etc.
    """
    SCHEMA_REGISTRY_SCHEMA_ID: ClassVar[KeywordField] = KeywordField(
        "schemaRegistrySchemaId", "schemaRegistrySchemaId"
    )
    """
    Unique identifier for schema definition set by the schema registry.
    """

    _convenience_properties: ClassVar[list[str]] = [
        "schema_registry_schema_type",
        "schema_registry_schema_id",
    ]

    @property
    def schema_registry_schema_type(self) -> Optional[SchemaRegistrySchemaType]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_schema_type
        )

    @schema_registry_schema_type.setter
    def schema_registry_schema_type(
        self, schema_registry_schema_type: Optional[SchemaRegistrySchemaType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_schema_type = schema_registry_schema_type

    @property
    def schema_registry_schema_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_schema_id
        )

    @schema_registry_schema_id.setter
    def schema_registry_schema_id(self, schema_registry_schema_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_schema_id = schema_registry_schema_id

    class Attributes(Catalog.Attributes):
        schema_registry_schema_type: Optional[SchemaRegistrySchemaType] = Field(
            default=None, description=""
        )
        schema_registry_schema_id: Optional[str] = Field(default=None, description="")

    attributes: "SchemaRegistry.Attributes" = Field(
        default_factory=lambda: SchemaRegistry.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SchemaRegistrySubject(SchemaRegistry):
    """Description"""

    type_name: str = Field(default="SchemaRegistrySubject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SchemaRegistrySubject":
            raise ValueError("must be SchemaRegistrySubject")
        return v

    def __setattr__(self, name, value):
        if name in SchemaRegistrySubject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SCHEMA_REGISTRY_SUBJECT_BASE_NAME: ClassVar[KeywordField] = KeywordField(
        "schemaRegistrySubjectBaseName", "schemaRegistrySubjectBaseName"
    )
    """
    Base name of the subject, without -key, -value prefixes.
    """
    SCHEMA_REGISTRY_SUBJECT_IS_KEY_SCHEMA: ClassVar[BooleanField] = BooleanField(
        "schemaRegistrySubjectIsKeySchema", "schemaRegistrySubjectIsKeySchema"
    )
    """
    Whether the subject is a schema for the keys of the messages (true) or not (false).
    """
    SCHEMA_REGISTRY_SUBJECT_SCHEMA_COMPATIBILITY: ClassVar[KeywordField] = KeywordField(
        "schemaRegistrySubjectSchemaCompatibility",
        "schemaRegistrySubjectSchemaCompatibility",
    )
    """
    Compatibility of the schema across versions.
    """
    SCHEMA_REGISTRY_SUBJECT_LATEST_SCHEMA_VERSION: ClassVar[
        KeywordField
    ] = KeywordField(
        "schemaRegistrySubjectLatestSchemaVersion",
        "schemaRegistrySubjectLatestSchemaVersion",
    )
    """
    Latest schema version of the subject.
    """
    SCHEMA_REGISTRY_SUBJECT_LATEST_SCHEMA_DEFINITION: ClassVar[TextField] = TextField(
        "schemaRegistrySubjectLatestSchemaDefinition",
        "schemaRegistrySubjectLatestSchemaDefinition",
    )
    """
    Definition of the latest schema in the subject.
    """
    SCHEMA_REGISTRY_SUBJECT_GOVERNING_ASSET_QUALIFIED_NAMES: ClassVar[
        KeywordField
    ] = KeywordField(
        "schemaRegistrySubjectGoverningAssetQualifiedNames",
        "schemaRegistrySubjectGoverningAssetQualifiedNames",
    )
    """
    List of asset qualified names that this subject is governing/validating.
    """

    ASSETS: ClassVar[RelationField] = RelationField("assets")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "schema_registry_subject_base_name",
        "schema_registry_subject_is_key_schema",
        "schema_registry_subject_schema_compatibility",
        "schema_registry_subject_latest_schema_version",
        "schema_registry_subject_latest_schema_definition",
        "schema_registry_subject_governing_asset_qualified_names",
        "assets",
    ]

    @property
    def schema_registry_subject_base_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subject_base_name
        )

    @schema_registry_subject_base_name.setter
    def schema_registry_subject_base_name(
        self, schema_registry_subject_base_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject_base_name = (
            schema_registry_subject_base_name
        )

    @property
    def schema_registry_subject_is_key_schema(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subject_is_key_schema
        )

    @schema_registry_subject_is_key_schema.setter
    def schema_registry_subject_is_key_schema(
        self, schema_registry_subject_is_key_schema: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject_is_key_schema = (
            schema_registry_subject_is_key_schema
        )

    @property
    def schema_registry_subject_schema_compatibility(
        self,
    ) -> Optional[SchemaRegistrySchemaCompatibility]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subject_schema_compatibility
        )

    @schema_registry_subject_schema_compatibility.setter
    def schema_registry_subject_schema_compatibility(
        self,
        schema_registry_subject_schema_compatibility: Optional[
            SchemaRegistrySchemaCompatibility
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject_schema_compatibility = (
            schema_registry_subject_schema_compatibility
        )

    @property
    def schema_registry_subject_latest_schema_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subject_latest_schema_version
        )

    @schema_registry_subject_latest_schema_version.setter
    def schema_registry_subject_latest_schema_version(
        self, schema_registry_subject_latest_schema_version: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject_latest_schema_version = (
            schema_registry_subject_latest_schema_version
        )

    @property
    def schema_registry_subject_latest_schema_definition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subject_latest_schema_definition
        )

    @schema_registry_subject_latest_schema_definition.setter
    def schema_registry_subject_latest_schema_definition(
        self, schema_registry_subject_latest_schema_definition: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject_latest_schema_definition = (
            schema_registry_subject_latest_schema_definition
        )

    @property
    def schema_registry_subject_governing_asset_qualified_names(
        self,
    ) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subject_governing_asset_qualified_names
        )

    @schema_registry_subject_governing_asset_qualified_names.setter
    def schema_registry_subject_governing_asset_qualified_names(
        self,
        schema_registry_subject_governing_asset_qualified_names: Optional[set[str]],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject_governing_asset_qualified_names = (
            schema_registry_subject_governing_asset_qualified_names
        )

    @property
    def assets(self) -> Optional[list[Asset]]:
        return None if self.attributes is None else self.attributes.assets

    @assets.setter
    def assets(self, assets: Optional[list[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.assets = assets

    class Attributes(SchemaRegistry.Attributes):
        schema_registry_subject_base_name: Optional[str] = Field(
            default=None, description=""
        )
        schema_registry_subject_is_key_schema: Optional[bool] = Field(
            default=None, description=""
        )
        schema_registry_subject_schema_compatibility: Optional[
            SchemaRegistrySchemaCompatibility
        ] = Field(default=None, description="")
        schema_registry_subject_latest_schema_version: Optional[str] = Field(
            default=None, description=""
        )
        schema_registry_subject_latest_schema_definition: Optional[str] = Field(
            default=None, description=""
        )
        schema_registry_subject_governing_asset_qualified_names: Optional[
            set[str]
        ] = Field(default=None, description="")
        assets: Optional[list[Asset]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "SchemaRegistrySubject.Attributes" = Field(
        default_factory=lambda: SchemaRegistrySubject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MonteCarlo(DataQuality):
    """Description"""

    type_name: str = Field(default="MonteCarlo", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MonteCarlo":
            raise ValueError("must be MonteCarlo")
        return v

    def __setattr__(self, name, value):
        if name in MonteCarlo._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MC_LABELS: ClassVar[KeywordField] = KeywordField("mcLabels", "mcLabels")
    """
    List of labels for this Monte Carlo asset.
    """
    MC_ASSET_QUALIFIED_NAMES: ClassVar[KeywordField] = KeywordField(
        "mcAssetQualifiedNames", "mcAssetQualifiedNames"
    )
    """
    List of unique names of assets that are part of this Monte Carlo asset.
    """

    _convenience_properties: ClassVar[list[str]] = [
        "mc_labels",
        "mc_asset_qualified_names",
    ]

    @property
    def mc_labels(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.mc_labels

    @mc_labels.setter
    def mc_labels(self, mc_labels: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_labels = mc_labels

    @property
    def mc_asset_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_asset_qualified_names
        )

    @mc_asset_qualified_names.setter
    def mc_asset_qualified_names(self, mc_asset_qualified_names: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_asset_qualified_names = mc_asset_qualified_names

    class Attributes(DataQuality.Attributes):
        mc_labels: Optional[set[str]] = Field(default=None, description="")
        mc_asset_qualified_names: Optional[set[str]] = Field(
            default=None, description=""
        )

    attributes: "MonteCarlo.Attributes" = Field(
        default_factory=lambda: MonteCarlo.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MCIncident(MonteCarlo):
    """Description"""

    type_name: str = Field(default="MCIncident", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MCIncident":
            raise ValueError("must be MCIncident")
        return v

    def __setattr__(self, name, value):
        if name in MCIncident._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MC_INCIDENT_ID: ClassVar[KeywordField] = KeywordField(
        "mcIncidentId", "mcIncidentId"
    )
    """
    Identifier of this incident, from Monte Carlo.
    """
    MC_INCIDENT_TYPE: ClassVar[KeywordField] = KeywordField(
        "mcIncidentType", "mcIncidentType"
    )
    """
    Type of this incident.
    """
    MC_INCIDENT_SUB_TYPES: ClassVar[KeywordField] = KeywordField(
        "mcIncidentSubTypes", "mcIncidentSubTypes"
    )
    """
    Subtypes of this incident.
    """
    MC_INCIDENT_SEVERITY: ClassVar[KeywordField] = KeywordField(
        "mcIncidentSeverity", "mcIncidentSeverity"
    )
    """
    Severity of this incident.
    """
    MC_INCIDENT_STATE: ClassVar[KeywordField] = KeywordField(
        "mcIncidentState", "mcIncidentState"
    )
    """
    State of this incident.
    """
    MC_INCIDENT_WAREHOUSE: ClassVar[KeywordField] = KeywordField(
        "mcIncidentWarehouse", "mcIncidentWarehouse"
    )
    """
    Name of this incident's warehouse.
    """

    MC_MONITOR: ClassVar[RelationField] = RelationField("mcMonitor")
    """
    TBC
    """
    MC_INCIDENT_ASSETS: ClassVar[RelationField] = RelationField("mcIncidentAssets")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "mc_incident_id",
        "mc_incident_type",
        "mc_incident_sub_types",
        "mc_incident_severity",
        "mc_incident_state",
        "mc_incident_warehouse",
        "mc_monitor",
        "mc_incident_assets",
    ]

    @property
    def mc_incident_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_incident_id

    @mc_incident_id.setter
    def mc_incident_id(self, mc_incident_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_id = mc_incident_id

    @property
    def mc_incident_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_incident_type

    @mc_incident_type.setter
    def mc_incident_type(self, mc_incident_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_type = mc_incident_type

    @property
    def mc_incident_sub_types(self) -> Optional[set[str]]:
        return (
            None if self.attributes is None else self.attributes.mc_incident_sub_types
        )

    @mc_incident_sub_types.setter
    def mc_incident_sub_types(self, mc_incident_sub_types: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_sub_types = mc_incident_sub_types

    @property
    def mc_incident_severity(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_incident_severity

    @mc_incident_severity.setter
    def mc_incident_severity(self, mc_incident_severity: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_severity = mc_incident_severity

    @property
    def mc_incident_state(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_incident_state

    @mc_incident_state.setter
    def mc_incident_state(self, mc_incident_state: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_state = mc_incident_state

    @property
    def mc_incident_warehouse(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.mc_incident_warehouse
        )

    @mc_incident_warehouse.setter
    def mc_incident_warehouse(self, mc_incident_warehouse: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_warehouse = mc_incident_warehouse

    @property
    def mc_monitor(self) -> Optional[MCMonitor]:
        return None if self.attributes is None else self.attributes.mc_monitor

    @mc_monitor.setter
    def mc_monitor(self, mc_monitor: Optional[MCMonitor]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor = mc_monitor

    @property
    def mc_incident_assets(self) -> Optional[list[Asset]]:
        return None if self.attributes is None else self.attributes.mc_incident_assets

    @mc_incident_assets.setter
    def mc_incident_assets(self, mc_incident_assets: Optional[list[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_assets = mc_incident_assets

    class Attributes(MonteCarlo.Attributes):
        mc_incident_id: Optional[str] = Field(default=None, description="")
        mc_incident_type: Optional[str] = Field(default=None, description="")
        mc_incident_sub_types: Optional[set[str]] = Field(default=None, description="")
        mc_incident_severity: Optional[str] = Field(default=None, description="")
        mc_incident_state: Optional[str] = Field(default=None, description="")
        mc_incident_warehouse: Optional[str] = Field(default=None, description="")
        mc_monitor: Optional[MCMonitor] = Field(
            default=None, description=""
        )  # relationship
        mc_incident_assets: Optional[list[Asset]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "MCIncident.Attributes" = Field(
        default_factory=lambda: MCIncident.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MCMonitor(MonteCarlo):
    """Description"""

    type_name: str = Field(default="MCMonitor", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MCMonitor":
            raise ValueError("must be MCMonitor")
        return v

    def __setattr__(self, name, value):
        if name in MCMonitor._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MC_MONITOR_ID: ClassVar[KeywordField] = KeywordField("mcMonitorId", "mcMonitorId")
    """
    Unique identifier for this monitor, from Monte Carlo.
    """
    MC_MONITOR_STATUS: ClassVar[KeywordField] = KeywordField(
        "mcMonitorStatus", "mcMonitorStatus"
    )
    """
    Status of this monitor.
    """
    MC_MONITOR_TYPE: ClassVar[KeywordField] = KeywordField(
        "mcMonitorType", "mcMonitorType"
    )
    """
    Type of this monitor, for example: field health (stats) or dimension tracking (categories).
    """
    MC_MONITOR_WAREHOUSE: ClassVar[KeywordField] = KeywordField(
        "mcMonitorWarehouse", "mcMonitorWarehouse"
    )
    """
    Name of the warehouse for this monitor.
    """
    MC_MONITOR_SCHEDULE_TYPE: ClassVar[KeywordField] = KeywordField(
        "mcMonitorScheduleType", "mcMonitorScheduleType"
    )
    """
    Type of schedule for this monitor, for example: fixed or dynamic.
    """
    MC_MONITOR_NAMESPACE: ClassVar[KeywordTextField] = KeywordTextField(
        "mcMonitorNamespace", "mcMonitorNamespace.keyword", "mcMonitorNamespace"
    )
    """
    Namespace of this monitor.
    """
    MC_MONITOR_RULE_TYPE: ClassVar[KeywordField] = KeywordField(
        "mcMonitorRuleType", "mcMonitorRuleType"
    )
    """
    Type of rule for this monitor.
    """
    MC_MONITOR_RULE_CUSTOM_SQL: ClassVar[KeywordField] = KeywordField(
        "mcMonitorRuleCustomSql", "mcMonitorRuleCustomSql"
    )
    """
    SQL code for custom SQL rules.
    """
    MC_MONITOR_RULE_SCHEDULE_CONFIG: ClassVar[KeywordField] = KeywordField(
        "mcMonitorRuleScheduleConfig", "mcMonitorRuleScheduleConfig"
    )
    """
    Schedule details for the rule.
    """
    MC_MONITOR_RULE_SCHEDULE_CONFIG_HUMANIZED: ClassVar[TextField] = TextField(
        "mcMonitorRuleScheduleConfigHumanized", "mcMonitorRuleScheduleConfigHumanized"
    )
    """
    Readable description of the schedule for the rule.
    """
    MC_MONITOR_ALERT_CONDITION: ClassVar[TextField] = TextField(
        "mcMonitorAlertCondition", "mcMonitorAlertCondition"
    )
    """
    Condition on which the monitor produces an alert.
    """
    MC_MONITOR_RULE_NEXT_EXECUTION_TIME: ClassVar[NumericField] = NumericField(
        "mcMonitorRuleNextExecutionTime", "mcMonitorRuleNextExecutionTime"
    )
    """
    Time at which the next execution of the rule should occur.
    """
    MC_MONITOR_RULE_PREVIOUS_EXECUTION_TIME: ClassVar[NumericField] = NumericField(
        "mcMonitorRulePreviousExecutionTime", "mcMonitorRulePreviousExecutionTime"
    )
    """
    Time at which the previous execution of the rule occurred.
    """
    MC_MONITOR_RULE_COMPARISONS: ClassVar[KeywordField] = KeywordField(
        "mcMonitorRuleComparisons", "mcMonitorRuleComparisons"
    )
    """
    Comparison logic used for the rule.
    """
    MC_MONITOR_RULE_IS_SNOOZED: ClassVar[BooleanField] = BooleanField(
        "mcMonitorRuleIsSnoozed", "mcMonitorRuleIsSnoozed"
    )
    """
    Whether the rule is currently snoozed (true) or not (false).
    """
    MC_MONITOR_BREACH_RATE: ClassVar[NumericField] = NumericField(
        "mcMonitorBreachRate", "mcMonitorBreachRate"
    )
    """
    Rate at which this monitor is breached.
    """
    MC_MONITOR_INCIDENT_COUNT: ClassVar[NumericField] = NumericField(
        "mcMonitorIncidentCount", "mcMonitorIncidentCount"
    )
    """
    Number of incidents associated with this monitor.
    """

    MC_MONITOR_ASSETS: ClassVar[RelationField] = RelationField("mcMonitorAssets")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "mc_monitor_id",
        "mc_monitor_status",
        "mc_monitor_type",
        "mc_monitor_warehouse",
        "mc_monitor_schedule_type",
        "mc_monitor_namespace",
        "mc_monitor_rule_type",
        "mc_monitor_rule_custom_sql",
        "mc_monitor_rule_schedule_config",
        "mc_monitor_rule_schedule_config_humanized",
        "mc_monitor_alert_condition",
        "mc_monitor_rule_next_execution_time",
        "mc_monitor_rule_previous_execution_time",
        "mc_monitor_rule_comparisons",
        "mc_monitor_rule_is_snoozed",
        "mc_monitor_breach_rate",
        "mc_monitor_incident_count",
        "mc_monitor_assets",
    ]

    @property
    def mc_monitor_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_monitor_id

    @mc_monitor_id.setter
    def mc_monitor_id(self, mc_monitor_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_id = mc_monitor_id

    @property
    def mc_monitor_status(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_monitor_status

    @mc_monitor_status.setter
    def mc_monitor_status(self, mc_monitor_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_status = mc_monitor_status

    @property
    def mc_monitor_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_monitor_type

    @mc_monitor_type.setter
    def mc_monitor_type(self, mc_monitor_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_type = mc_monitor_type

    @property
    def mc_monitor_warehouse(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_monitor_warehouse

    @mc_monitor_warehouse.setter
    def mc_monitor_warehouse(self, mc_monitor_warehouse: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_warehouse = mc_monitor_warehouse

    @property
    def mc_monitor_schedule_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_schedule_type
        )

    @mc_monitor_schedule_type.setter
    def mc_monitor_schedule_type(self, mc_monitor_schedule_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_schedule_type = mc_monitor_schedule_type

    @property
    def mc_monitor_namespace(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_monitor_namespace

    @mc_monitor_namespace.setter
    def mc_monitor_namespace(self, mc_monitor_namespace: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_namespace = mc_monitor_namespace

    @property
    def mc_monitor_rule_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_monitor_rule_type

    @mc_monitor_rule_type.setter
    def mc_monitor_rule_type(self, mc_monitor_rule_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_type = mc_monitor_rule_type

    @property
    def mc_monitor_rule_custom_sql(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_custom_sql
        )

    @mc_monitor_rule_custom_sql.setter
    def mc_monitor_rule_custom_sql(self, mc_monitor_rule_custom_sql: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_custom_sql = mc_monitor_rule_custom_sql

    @property
    def mc_monitor_rule_schedule_config(self) -> Optional[MCRuleSchedule]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_schedule_config
        )

    @mc_monitor_rule_schedule_config.setter
    def mc_monitor_rule_schedule_config(
        self, mc_monitor_rule_schedule_config: Optional[MCRuleSchedule]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_schedule_config = (
            mc_monitor_rule_schedule_config
        )

    @property
    def mc_monitor_rule_schedule_config_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_schedule_config_humanized
        )

    @mc_monitor_rule_schedule_config_humanized.setter
    def mc_monitor_rule_schedule_config_humanized(
        self, mc_monitor_rule_schedule_config_humanized: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_schedule_config_humanized = (
            mc_monitor_rule_schedule_config_humanized
        )

    @property
    def mc_monitor_alert_condition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_alert_condition
        )

    @mc_monitor_alert_condition.setter
    def mc_monitor_alert_condition(self, mc_monitor_alert_condition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_alert_condition = mc_monitor_alert_condition

    @property
    def mc_monitor_rule_next_execution_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_next_execution_time
        )

    @mc_monitor_rule_next_execution_time.setter
    def mc_monitor_rule_next_execution_time(
        self, mc_monitor_rule_next_execution_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_next_execution_time = (
            mc_monitor_rule_next_execution_time
        )

    @property
    def mc_monitor_rule_previous_execution_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_previous_execution_time
        )

    @mc_monitor_rule_previous_execution_time.setter
    def mc_monitor_rule_previous_execution_time(
        self, mc_monitor_rule_previous_execution_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_previous_execution_time = (
            mc_monitor_rule_previous_execution_time
        )

    @property
    def mc_monitor_rule_comparisons(self) -> Optional[list[MCRuleComparison]]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_comparisons
        )

    @mc_monitor_rule_comparisons.setter
    def mc_monitor_rule_comparisons(
        self, mc_monitor_rule_comparisons: Optional[list[MCRuleComparison]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_comparisons = mc_monitor_rule_comparisons

    @property
    def mc_monitor_rule_is_snoozed(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_is_snoozed
        )

    @mc_monitor_rule_is_snoozed.setter
    def mc_monitor_rule_is_snoozed(self, mc_monitor_rule_is_snoozed: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_is_snoozed = mc_monitor_rule_is_snoozed

    @property
    def mc_monitor_breach_rate(self) -> Optional[float]:
        return (
            None if self.attributes is None else self.attributes.mc_monitor_breach_rate
        )

    @mc_monitor_breach_rate.setter
    def mc_monitor_breach_rate(self, mc_monitor_breach_rate: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_breach_rate = mc_monitor_breach_rate

    @property
    def mc_monitor_incident_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_incident_count
        )

    @mc_monitor_incident_count.setter
    def mc_monitor_incident_count(self, mc_monitor_incident_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_incident_count = mc_monitor_incident_count

    @property
    def mc_monitor_assets(self) -> Optional[list[Asset]]:
        return None if self.attributes is None else self.attributes.mc_monitor_assets

    @mc_monitor_assets.setter
    def mc_monitor_assets(self, mc_monitor_assets: Optional[list[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_assets = mc_monitor_assets

    class Attributes(MonteCarlo.Attributes):
        mc_monitor_id: Optional[str] = Field(default=None, description="")
        mc_monitor_status: Optional[str] = Field(default=None, description="")
        mc_monitor_type: Optional[str] = Field(default=None, description="")
        mc_monitor_warehouse: Optional[str] = Field(default=None, description="")
        mc_monitor_schedule_type: Optional[str] = Field(default=None, description="")
        mc_monitor_namespace: Optional[str] = Field(default=None, description="")
        mc_monitor_rule_type: Optional[str] = Field(default=None, description="")
        mc_monitor_rule_custom_sql: Optional[str] = Field(default=None, description="")
        mc_monitor_rule_schedule_config: Optional[MCRuleSchedule] = Field(
            default=None, description=""
        )
        mc_monitor_rule_schedule_config_humanized: Optional[str] = Field(
            default=None, description=""
        )
        mc_monitor_alert_condition: Optional[str] = Field(default=None, description="")
        mc_monitor_rule_next_execution_time: Optional[datetime] = Field(
            default=None, description=""
        )
        mc_monitor_rule_previous_execution_time: Optional[datetime] = Field(
            default=None, description=""
        )
        mc_monitor_rule_comparisons: Optional[list[MCRuleComparison]] = Field(
            default=None, description=""
        )
        mc_monitor_rule_is_snoozed: Optional[bool] = Field(default=None, description="")
        mc_monitor_breach_rate: Optional[float] = Field(default=None, description="")
        mc_monitor_incident_count: Optional[int] = Field(default=None, description="")
        mc_monitor_assets: Optional[list[Asset]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "MCMonitor.Attributes" = Field(
        default_factory=lambda: MCMonitor.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Soda(DataQuality):
    """Description"""

    type_name: str = Field(default="Soda", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Soda":
            raise ValueError("must be Soda")
        return v

    def __setattr__(self, name, value):
        if name in Soda._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[list[str]] = []


class SodaCheck(Soda):
    """Description"""

    type_name: str = Field(default="SodaCheck", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SodaCheck":
            raise ValueError("must be SodaCheck")
        return v

    def __setattr__(self, name, value):
        if name in SodaCheck._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SODA_CHECK_ID: ClassVar[KeywordField] = KeywordField("sodaCheckId", "sodaCheckId")
    """
    Identifier of the check in Soda.
    """
    SODA_CHECK_EVALUATION_STATUS: ClassVar[KeywordField] = KeywordField(
        "sodaCheckEvaluationStatus", "sodaCheckEvaluationStatus"
    )
    """
    Status of the check in Soda.
    """
    SODA_CHECK_DEFINITION: ClassVar[KeywordField] = KeywordField(
        "sodaCheckDefinition", "sodaCheckDefinition"
    )
    """
    Definition of the check in Soda.
    """
    SODA_CHECK_LAST_SCAN_AT: ClassVar[NumericField] = NumericField(
        "sodaCheckLastScanAt", "sodaCheckLastScanAt"
    )
    """

    """
    SODA_CHECK_INCIDENT_COUNT: ClassVar[NumericField] = NumericField(
        "sodaCheckIncidentCount", "sodaCheckIncidentCount"
    )
    """

    """

    SODA_CHECK_COLUMNS: ClassVar[RelationField] = RelationField("sodaCheckColumns")
    """
    TBC
    """
    SODA_CHECK_ASSETS: ClassVar[RelationField] = RelationField("sodaCheckAssets")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "soda_check_id",
        "soda_check_evaluation_status",
        "soda_check_definition",
        "soda_check_last_scan_at",
        "soda_check_incident_count",
        "soda_check_columns",
        "soda_check_assets",
    ]

    @property
    def soda_check_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.soda_check_id

    @soda_check_id.setter
    def soda_check_id(self, soda_check_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.soda_check_id = soda_check_id

    @property
    def soda_check_evaluation_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.soda_check_evaluation_status
        )

    @soda_check_evaluation_status.setter
    def soda_check_evaluation_status(self, soda_check_evaluation_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.soda_check_evaluation_status = soda_check_evaluation_status

    @property
    def soda_check_definition(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.soda_check_definition
        )

    @soda_check_definition.setter
    def soda_check_definition(self, soda_check_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.soda_check_definition = soda_check_definition

    @property
    def soda_check_last_scan_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.soda_check_last_scan_at
        )

    @soda_check_last_scan_at.setter
    def soda_check_last_scan_at(self, soda_check_last_scan_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.soda_check_last_scan_at = soda_check_last_scan_at

    @property
    def soda_check_incident_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.soda_check_incident_count
        )

    @soda_check_incident_count.setter
    def soda_check_incident_count(self, soda_check_incident_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.soda_check_incident_count = soda_check_incident_count

    @property
    def soda_check_columns(self) -> Optional[list[Column]]:
        return None if self.attributes is None else self.attributes.soda_check_columns

    @soda_check_columns.setter
    def soda_check_columns(self, soda_check_columns: Optional[list[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.soda_check_columns = soda_check_columns

    @property
    def soda_check_assets(self) -> Optional[list[Asset]]:
        return None if self.attributes is None else self.attributes.soda_check_assets

    @soda_check_assets.setter
    def soda_check_assets(self, soda_check_assets: Optional[list[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.soda_check_assets = soda_check_assets

    class Attributes(Soda.Attributes):
        soda_check_id: Optional[str] = Field(default=None, description="")
        soda_check_evaluation_status: Optional[str] = Field(
            default=None, description=""
        )
        soda_check_definition: Optional[str] = Field(default=None, description="")
        soda_check_last_scan_at: Optional[datetime] = Field(
            default=None, description=""
        )
        soda_check_incident_count: Optional[int] = Field(default=None, description="")
        soda_check_columns: Optional[list[Column]] = Field(
            default=None, description=""
        )  # relationship
        soda_check_assets: Optional[list[Asset]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "SodaCheck.Attributes" = Field(
        default_factory=lambda: SodaCheck.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Table(SQL):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(cls, *, name: str, schema_qualified_name: str) -> Table:
        validate_required_fields(
            ["name", "schema_qualified_name"], [name, schema_qualified_name]
        )
        attributes = Table.Attributes.create(
            name=name, schema_qualified_name=schema_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="Table", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Table":
            raise ValueError("must be Table")
        return v

    def __setattr__(self, name, value):
        if name in Table._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COLUMN_COUNT: ClassVar[NumericField] = NumericField("columnCount", "columnCount")
    """
    Number of columns in this table.
    """
    ROW_COUNT: ClassVar[NumericField] = NumericField("rowCount", "rowCount")
    """
    Number of rows in this table.
    """
    SIZE_BYTES: ClassVar[NumericField] = NumericField("sizeBytes", "sizeBytes")
    """
    Size of this table, in bytes.
    """
    ALIAS: ClassVar[KeywordField] = KeywordField("alias", "alias")
    """
    Alias for this table.
    """
    IS_TEMPORARY: ClassVar[BooleanField] = BooleanField("isTemporary", "isTemporary")
    """
    Whether this table is temporary (true) or not (false).
    """
    IS_QUERY_PREVIEW: ClassVar[BooleanField] = BooleanField(
        "isQueryPreview", "isQueryPreview"
    )
    """
    Whether preview queries are allowed for this table (true) or not (false).
    """
    QUERY_PREVIEW_CONFIG: ClassVar[KeywordField] = KeywordField(
        "queryPreviewConfig", "queryPreviewConfig"
    )
    """
    Configuration for preview queries.
    """
    EXTERNAL_LOCATION: ClassVar[KeywordField] = KeywordField(
        "externalLocation", "externalLocation"
    )
    """
    External location of this table, for example: an S3 object location.
    """
    EXTERNAL_LOCATION_REGION: ClassVar[KeywordField] = KeywordField(
        "externalLocationRegion", "externalLocationRegion"
    )
    """
    Region of the external location of this table, for example: S3 region.
    """
    EXTERNAL_LOCATION_FORMAT: ClassVar[KeywordField] = KeywordField(
        "externalLocationFormat", "externalLocationFormat"
    )
    """
    Format of the external location of this table, for example: JSON, CSV, PARQUET, etc.
    """
    IS_PARTITIONED: ClassVar[BooleanField] = BooleanField(
        "isPartitioned", "isPartitioned"
    )
    """
    Whether this table is partitioned (true) or not (false).
    """
    PARTITION_STRATEGY: ClassVar[KeywordField] = KeywordField(
        "partitionStrategy", "partitionStrategy"
    )
    """
    Partition strategy for this table.
    """
    PARTITION_COUNT: ClassVar[NumericField] = NumericField(
        "partitionCount", "partitionCount"
    )
    """
    Number of partitions in this table.
    """
    PARTITION_LIST: ClassVar[KeywordField] = KeywordField(
        "partitionList", "partitionList"
    )
    """
    List of partitions in this table.
    """

    COLUMNS: ClassVar[RelationField] = RelationField("columns")
    """
    TBC
    """
    FACTS: ClassVar[RelationField] = RelationField("facts")
    """
    TBC
    """
    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """
    PARTITIONS: ClassVar[RelationField] = RelationField("partitions")
    """
    TBC
    """
    QUERIES: ClassVar[RelationField] = RelationField("queries")
    """
    TBC
    """
    DIMENSIONS: ClassVar[RelationField] = RelationField("dimensions")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "column_count",
        "row_count",
        "size_bytes",
        "alias",
        "is_temporary",
        "is_query_preview",
        "query_preview_config",
        "external_location",
        "external_location_region",
        "external_location_format",
        "is_partitioned",
        "partition_strategy",
        "partition_count",
        "partition_list",
        "columns",
        "facts",
        "atlan_schema",
        "partitions",
        "queries",
        "dimensions",
    ]

    @property
    def column_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.column_count

    @column_count.setter
    def column_count(self, column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_count = column_count

    @property
    def row_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.row_count

    @row_count.setter
    def row_count(self, row_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.row_count = row_count

    @property
    def size_bytes(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.size_bytes

    @size_bytes.setter
    def size_bytes(self, size_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.size_bytes = size_bytes

    @property
    def alias(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.alias

    @alias.setter
    def alias(self, alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alias = alias

    @property
    def is_temporary(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_temporary

    @is_temporary.setter
    def is_temporary(self, is_temporary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_temporary = is_temporary

    @property
    def is_query_preview(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_query_preview

    @is_query_preview.setter
    def is_query_preview(self, is_query_preview: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_query_preview = is_query_preview

    @property
    def query_preview_config(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.query_preview_config

    @query_preview_config.setter
    def query_preview_config(self, query_preview_config: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_preview_config = query_preview_config

    @property
    def external_location(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.external_location

    @external_location.setter
    def external_location(self, external_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location = external_location

    @property
    def external_location_region(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.external_location_region
        )

    @external_location_region.setter
    def external_location_region(self, external_location_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location_region = external_location_region

    @property
    def external_location_format(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.external_location_format
        )

    @external_location_format.setter
    def external_location_format(self, external_location_format: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location_format = external_location_format

    @property
    def is_partitioned(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_partitioned

    @is_partitioned.setter
    def is_partitioned(self, is_partitioned: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_partitioned = is_partitioned

    @property
    def partition_strategy(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.partition_strategy

    @partition_strategy.setter
    def partition_strategy(self, partition_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_strategy = partition_strategy

    @property
    def partition_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.partition_count

    @partition_count.setter
    def partition_count(self, partition_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_count = partition_count

    @property
    def partition_list(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.partition_list

    @partition_list.setter
    def partition_list(self, partition_list: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_list = partition_list

    @property
    def columns(self) -> Optional[list[Column]]:
        return None if self.attributes is None else self.attributes.columns

    @columns.setter
    def columns(self, columns: Optional[list[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.columns = columns

    @property
    def facts(self) -> Optional[list[Table]]:
        return None if self.attributes is None else self.attributes.facts

    @facts.setter
    def facts(self, facts: Optional[list[Table]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.facts = facts

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    @property
    def partitions(self) -> Optional[list[TablePartition]]:
        return None if self.attributes is None else self.attributes.partitions

    @partitions.setter
    def partitions(self, partitions: Optional[list[TablePartition]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partitions = partitions

    @property
    def queries(self) -> Optional[list[Query]]:
        return None if self.attributes is None else self.attributes.queries

    @queries.setter
    def queries(self, queries: Optional[list[Query]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.queries = queries

    @property
    def dimensions(self) -> Optional[list[Table]]:
        return None if self.attributes is None else self.attributes.dimensions

    @dimensions.setter
    def dimensions(self, dimensions: Optional[list[Table]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dimensions = dimensions

    class Attributes(SQL.Attributes):
        column_count: Optional[int] = Field(default=None, description="")
        row_count: Optional[int] = Field(default=None, description="")
        size_bytes: Optional[int] = Field(default=None, description="")
        alias: Optional[str] = Field(default=None, description="")
        is_temporary: Optional[bool] = Field(default=None, description="")
        is_query_preview: Optional[bool] = Field(default=None, description="")
        query_preview_config: Optional[dict[str, str]] = Field(
            default=None, description=""
        )
        external_location: Optional[str] = Field(default=None, description="")
        external_location_region: Optional[str] = Field(default=None, description="")
        external_location_format: Optional[str] = Field(default=None, description="")
        is_partitioned: Optional[bool] = Field(default=None, description="")
        partition_strategy: Optional[str] = Field(default=None, description="")
        partition_count: Optional[int] = Field(default=None, description="")
        partition_list: Optional[str] = Field(default=None, description="")
        columns: Optional[list[Column]] = Field(
            default=None, description=""
        )  # relationship
        facts: Optional[list[Table]] = Field(
            default=None, description=""
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship
        partitions: Optional[list[TablePartition]] = Field(
            default=None, description=""
        )  # relationship
        queries: Optional[list[Query]] = Field(
            default=None, description=""
        )  # relationship
        dimensions: Optional[list[Table]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(cls, *, name: str, schema_qualified_name: str) -> Table.Attributes:
            if not name:
                raise ValueError("name cannot be blank")
            validate_required_fields(["schema_qualified_name"], [schema_qualified_name])
            fields = schema_qualified_name.split("/")
            if len(fields) != 5:
                raise ValueError("Invalid schema_qualified_name")
            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid schema_qualified_name") from e
            return Table.Attributes(
                name=name,
                database_name=fields[3],
                connection_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}",
                database_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}/{fields[3]}",
                qualified_name=f"{schema_qualified_name}/{name}",
                schema_qualified_name=schema_qualified_name,
                schema_name=fields[4],
                connector_name=connector_type.value,
                atlan_schema=Schema.ref_by_qualified_name(schema_qualified_name),
            )

    attributes: "Table.Attributes" = Field(
        default_factory=lambda: Table.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SnowflakeDynamicTable(Table):
    """Description"""

    type_name: str = Field(default="SnowflakeDynamicTable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakeDynamicTable":
            raise ValueError("must be SnowflakeDynamicTable")
        return v

    def __setattr__(self, name, value):
        if name in SnowflakeDynamicTable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DEFINITION: ClassVar[KeywordField] = KeywordField("definition", "definition")
    """
    SQL statements used to define the dynamic table.
    """

    _convenience_properties: ClassVar[list[str]] = [
        "definition",
    ]

    @property
    def definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.definition

    @definition.setter
    def definition(self, definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.definition = definition

    class Attributes(Table.Attributes):
        definition: Optional[str] = Field(default=None, description="")

    attributes: "SnowflakeDynamicTable.Attributes" = Field(
        default_factory=lambda: SnowflakeDynamicTable.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Database(SQL):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(cls, *, name: str, connection_qualified_name: str) -> Database:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        fields = connection_qualified_name.split("/")
        if len(fields) != 3:
            raise ValueError("Invalid connection_qualified_name")
        try:
            connector_type = AtlanConnectorType(fields[1])  # type:ignore
        except ValueError as e:
            raise ValueError("Invalid connection_qualified_name") from e
        attributes = Database.Attributes(
            name=name,
            connection_qualified_name=connection_qualified_name,
            qualified_name=f"{connection_qualified_name}/{name}",
            connector_name=connector_type.value,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="Database", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Database":
            raise ValueError("must be Database")
        return v

    def __setattr__(self, name, value):
        if name in Database._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SCHEMA_COUNT: ClassVar[NumericField] = NumericField("schemaCount", "schemaCount")
    """
    Number of schemas in this database.
    """

    SCHEMAS: ClassVar[RelationField] = RelationField("schemas")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "schema_count",
        "schemas",
    ]

    @property
    def schema_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.schema_count

    @schema_count.setter
    def schema_count(self, schema_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_count = schema_count

    @property
    def schemas(self) -> Optional[list[Schema]]:
        return None if self.attributes is None else self.attributes.schemas

    @schemas.setter
    def schemas(self, schemas: Optional[list[Schema]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schemas = schemas

    class Attributes(SQL.Attributes):
        schema_count: Optional[int] = Field(default=None, description="")
        schemas: Optional[list[Schema]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, name: str, connection_qualified_name: str
        ) -> Database.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            fields = connection_qualified_name.split("/")
            if len(fields) != 3:
                raise ValueError("Invalid connection_qualified_name")
            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid connection_qualified_name") from e
            return Database.Attributes(
                name=name,
                connection_qualified_name=connection_qualified_name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connector_name=connector_type.value,
            )

    attributes: "Database.Attributes" = Field(
        default_factory=lambda: Database.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


Referenceable.Attributes.update_forward_refs()


Asset.Attributes.update_forward_refs()


AtlasGlossaryCategory.Attributes.update_forward_refs()


AtlasGlossary.Attributes.update_forward_refs()


AtlasGlossaryTerm.Attributes.update_forward_refs()


Process.Attributes.update_forward_refs()


Namespace.Attributes.update_forward_refs()


Folder.Attributes.update_forward_refs()


Catalog.Attributes.update_forward_refs()


Tag.Attributes.update_forward_refs()


ColumnProcess.Attributes.update_forward_refs()


Airflow.Attributes.update_forward_refs()


AirflowDag.Attributes.update_forward_refs()


AirflowTask.Attributes.update_forward_refs()


DataQuality.Attributes.update_forward_refs()


Metric.Attributes.update_forward_refs()


Resource.Attributes.update_forward_refs()


Readme.Attributes.update_forward_refs()


File.Attributes.update_forward_refs()


Link.Attributes.update_forward_refs()


DataMesh.Attributes.update_forward_refs()


DataDomain.Attributes.update_forward_refs()


DataProduct.Attributes.update_forward_refs()


SQL.Attributes.update_forward_refs()


Query.Attributes.update_forward_refs()


Schema.Attributes.update_forward_refs()


SnowflakePipe.Attributes.update_forward_refs()


View.Attributes.update_forward_refs()


MaterialisedView.Attributes.update_forward_refs()


Function.Attributes.update_forward_refs()


TablePartition.Attributes.update_forward_refs()


Column.Attributes.update_forward_refs()


SnowflakeStream.Attributes.update_forward_refs()


Procedure.Attributes.update_forward_refs()


SnowflakeTag.Attributes.update_forward_refs()


Matillion.Attributes.update_forward_refs()


MatillionGroup.Attributes.update_forward_refs()


MatillionJob.Attributes.update_forward_refs()


MatillionProject.Attributes.update_forward_refs()


MatillionComponent.Attributes.update_forward_refs()


Dbt.Attributes.update_forward_refs()


DbtModelColumn.Attributes.update_forward_refs()


DbtTest.Attributes.update_forward_refs()


DbtModel.Attributes.update_forward_refs()


DbtMetric.Attributes.update_forward_refs()


DbtSource.Attributes.update_forward_refs()


SchemaRegistry.Attributes.update_forward_refs()


SchemaRegistrySubject.Attributes.update_forward_refs()


MonteCarlo.Attributes.update_forward_refs()


MCIncident.Attributes.update_forward_refs()


MCMonitor.Attributes.update_forward_refs()


Soda.Attributes.update_forward_refs()


SodaCheck.Attributes.update_forward_refs()


Table.Attributes.update_forward_refs()


SnowflakeDynamicTable.Attributes.update_forward_refs()


Database.Attributes.update_forward_refs()
