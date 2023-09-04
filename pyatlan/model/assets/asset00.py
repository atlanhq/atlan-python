# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

import hashlib
import sys
from datetime import datetime
from io import StringIO
from typing import Any, ClassVar, Dict, List, Optional, Type, TypeVar
from urllib.parse import quote, unquote

from pydantic import Field, PrivateAttr, StrictStr, root_validator, validator

from pyatlan.model.core import Announcement, AtlanObject, AtlanTag, Meaning
from pyatlan.model.custom_metadata import CustomMetadataDict, CustomMetadataProxy
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    EntityStatus,
    FileType,
    IconType,
    OpenLineageRunState,
    SchemaRegistrySchemaCompatibility,
    SchemaRegistrySchemaType,
    SourceCostUnitType,
)
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    KeywordTextStemmedField,
    NumericField,
    NumericRankField,
    RelationField,
    TextField,
)
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
from pyatlan.utils import next_id, validate_required_fields


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
        qualified_name: Optional[str] = Field("", description="", alias="qualifiedName")
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship

        def validate_required(self):
            pass

    TYPE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "typeName", "__typeName.keyword", "__typeName"
    )
    """Type of the asset. For example Table, Column, and so on."""

    GUID: ClassVar[KeywordField] = KeywordField("guid", "__guid")
    """Globally unique identifier (GUID) of any object in Atlan."""

    CREATED_BY: ClassVar[KeywordField] = KeywordField("createdBy", "__createdBy")
    """Atlan user who created this asset."""

    UPDATED_BY: ClassVar[KeywordField] = KeywordField("updatedBy", "__modifiedBy")
    """Atlan user who last updated the asset."""

    STATUS: ClassVar[KeywordField] = KeywordField("status", "__state")
    """Asset status in Atlan (active vs deleted)."""

    ATLAN_TAGS: ClassVar[KeywordTextField] = KeywordTextField(
        "classificationNames", "__traitNames", "__classificationsText"
    )
    """
    All directly-assigned Atlan tags that exist on an asset, searchable by internal hashed-string ID of the Atlan tag.
    """

    PROPAGATED_ATLAN_TAGS: ClassVar[KeywordTextField] = KeywordTextField(
        "classificationNames", "__propagatedTraitNames", "__classificationsText"
    )
    """All propagated Atlan tags that exist on an asset, searchable by internal hashed-string ID of the Atlan tag."""

    ASSIGNED_TERMS: ClassVar[KeywordTextField] = KeywordTextField(
        "meanings", "__meanings", "__meaningsText"
    )
    """All terms attached to an asset, searchable by the term's qualifiedName."""

    SUPER_TYPE_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "typeName", "__superTypeNames.keyword", "__superTypeNames"
    )
    """All super types of an asset."""

    CREATE_TIME: ClassVar[NumericField] = NumericField("createTime", "__timestamp")
    """Time (in milliseconds) when the asset was created."""

    UPDATE_TIME: ClassVar[NumericField] = NumericField(
        "updateTime", "__modificationTimestamp"
    )
    """Time (in milliseconds) when the asset was last updated."""

    QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "qualifiedName", "qualifiedName", "qualifiedName.text"
    )
    """Unique fully-qualified name of the asset in Atlan."""

    type_name: str = Field(
        "Referenceable",
        description="Name of the type definition that defines this instance.\n",
    )
    _metadata_proxy: CustomMetadataProxy = PrivateAttr()
    attributes: Referenceable.Attributes = Field(
        default_factory=lambda: Referenceable.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary "
        "by type, so are described in the sub-types of this schema.\n",
    )
    business_attributes: Optional[Dict[str, Any]] = Field(
        None,
        description="Map of custom metadata attributes and values defined on the entity.\n",
        alias="businessAttributes",
    )
    created_by: Optional[str] = Field(
        None,
        description="Username of the user who created the object.\n",
        example="jsmith",
    )
    create_time: Optional[int] = Field(
        None,
        description="Time (epoch) at which this object was created, in milliseconds.\n",
        example=1648852296555,
    )
    delete_handler: Optional[str] = Field(
        None,
        description="Details on the handler used for deletion of the asset.",
        example="Hard",
    )
    guid: str = Field(
        "",
        description="Unique identifier of the entity instance.\n",
        example="917ffec9-fa84-4c59-8e6c-c7b114d04be3",
    )
    is_incomplete: Optional[bool] = Field(True, description="", example=True)
    labels: Optional[List[str]] = Field(None, description="Internal use only.")
    relationship_attributes: Optional[Dict[str, Any]] = Field(
        None,
        description="Map of relationships for the entity. The specific keys of this map will vary by type, "
        "so are described in the sub-types of this schema.\n",
    )
    status: Optional[EntityStatus] = Field(
        None, description="Status of the entity", example=EntityStatus.ACTIVE
    )
    updated_by: Optional[str] = Field(
        None,
        description="Username of the user who last assets_updated the object.\n",
        example="jsmith",
    )
    update_time: Optional[int] = Field(
        None,
        description="Time (epoch) at which this object was last assets_updated, in milliseconds.\n",
        example=1649172284333,
    )
    version: Optional[int] = Field(
        None, description="Version of this object.\n", example=2
    )
    atlan_tags: Optional[list[AtlanTag]] = Field(
        None, description="Atlan tags", alias="classifications"
    )
    classification_names: Optional[list[str]] = Field(
        None, description="The names of the classifications that exist on the asset."
    )
    display_text: Optional[str] = Field(
        None,
        description="Human-readable name of the entity..\n",
    )
    entity_status: Optional[str] = Field(
        None,
        description="Status of the entity (if this is a related entity).\n",
    )
    relationship_guid: Optional[str] = Field(
        None,
        description="Unique identifier of the relationship (when this is a related entity).\n",
    )
    relationship_status: Optional[str] = Field(
        None,
        description="Status of the relationship (when this is a related entity).\n",
    )
    relationship_type: Optional[str] = Field(
        None,
        description="Status of the relationship (when this is a related entity).\n",
    )
    meaning_names: Optional[list[str]] = Field(
        None, description="Names of assigned_terms that have been linked to this asset."
    )
    meanings: Optional[list[Meaning]] = Field(None, description="", alias="meanings")
    custom_attributes: Optional[dict[str, Any]] = Field(
        None, description="", alias="customAttributes"
    )
    scrubbed: Optional[bool] = Field(
        None, description="", alias="fields removed from results"
    )
    pending_tasks: Optional[list[str]] = Field(None)

    unique_attributes: Optional[dict[str, Any]] = Field(None)


class Asset(Referenceable):
    """Description"""

    _subtypes_: dict[str, type] = dict()

    def __init_subclass__(cls, type_name=None):
        cls._subtypes_[type_name or cls.__name__.lower()] = cls

    def trim_to_required(self: SelfAsset) -> SelfAsset:
        return self.create_for_modification(
            qualified_name=self.qualified_name or "", name=self.name or ""
        )

    @classmethod
    def create(cls: Type[SelfAsset], *args, **kwargs) -> SelfAsset:
        raise NotImplementedError(
            "Create has not been implemented for this class. Please submit an enhancement"
            "request if you need it implemented."
        )

    @classmethod
    def create_for_modification(
        cls: type[SelfAsset], qualified_name: str = "", name: str = ""
    ) -> SelfAsset:
        validate_required_fields(
            ["name", "qualified_name"],
            [name, qualified_name],
        )
        return cls(attributes=cls.Attributes(qualified_name=qualified_name, name=name))

    @classmethod
    def ref_by_guid(cls: type[SelfAsset], guid: str) -> SelfAsset:
        retval: SelfAsset = cls(attributes=cls.Attributes())
        retval.guid = guid
        return retval

    @classmethod
    def ref_by_qualified_name(cls: type[SelfAsset], qualified_name: str) -> SelfAsset:
        ret_value: SelfAsset = cls(
            attributes=cls.Attributes(name="", qualified_name=qualified_name)
        )
        ret_value.unique_attributes = {"qualifiedName": qualified_name}
        return ret_value

    @classmethod
    def __get_validators__(cls):
        yield cls._convert_to_real_type_

    @classmethod
    def _convert_to_real_type_(cls, data):
        if isinstance(data, Asset):
            return data

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

        return sub(**data)

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

    type_name: str = Field("Asset", allow_mutation=False)

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
    TBC
    """
    DISPLAY_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "displayName", "displayName.keyword", "displayName"
    )
    """
    TBC
    """
    DESCRIPTION: ClassVar[KeywordTextField] = KeywordTextField(
        "description", "description.keyword", "description"
    )
    """
    TBC
    """
    USER_DESCRIPTION: ClassVar[KeywordTextField] = KeywordTextField(
        "userDescription", "userDescription.keyword", "userDescription"
    )
    """
    TBC
    """
    TENANT_ID: ClassVar[KeywordField] = KeywordField("tenantId", "tenantId")
    """
    TBC
    """
    CERTIFICATE_STATUS: ClassVar[KeywordTextField] = KeywordTextField(
        "certificateStatus", "certificateStatus", "certificateStatus.text"
    )
    """
    TBC
    """
    CERTIFICATE_STATUS_MESSAGE: ClassVar[KeywordField] = KeywordField(
        "certificateStatusMessage", "certificateStatusMessage"
    )
    """
    TBC
    """
    CERTIFICATE_UPDATED_BY: ClassVar[KeywordField] = KeywordField(
        "certificateUpdatedBy", "certificateUpdatedBy"
    )
    """
    TBC
    """
    CERTIFICATE_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "certificateUpdatedAt", "certificateUpdatedAt"
    )
    """
    TBC
    """
    ANNOUNCEMENT_TITLE: ClassVar[KeywordField] = KeywordField(
        "announcementTitle", "announcementTitle"
    )
    """
    TBC
    """
    ANNOUNCEMENT_MESSAGE: ClassVar[KeywordField] = KeywordField(
        "announcementMessage", "announcementMessage"
    )
    """
    TBC
    """
    ANNOUNCEMENT_TYPE: ClassVar[KeywordField] = KeywordField(
        "announcementType", "announcementType"
    )
    """
    TBC
    """
    ANNOUNCEMENT_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "announcementUpdatedAt", "announcementUpdatedAt"
    )
    """
    TBC
    """
    ANNOUNCEMENT_UPDATED_BY: ClassVar[KeywordField] = KeywordField(
        "announcementUpdatedBy", "announcementUpdatedBy"
    )
    """
    TBC
    """
    OWNER_USERS: ClassVar[KeywordField] = KeywordField("ownerUsers", "ownerUsers")
    """
    TBC
    """
    OWNER_GROUPS: ClassVar[KeywordField] = KeywordField("ownerGroups", "ownerGroups")
    """
    TBC
    """
    ADMIN_USERS: ClassVar[KeywordField] = KeywordField("adminUsers", "adminUsers")
    """
    TBC
    """
    ADMIN_GROUPS: ClassVar[KeywordField] = KeywordField("adminGroups", "adminGroups")
    """
    TBC
    """
    VIEWER_USERS: ClassVar[KeywordField] = KeywordField("viewerUsers", "viewerUsers")
    """
    TBC
    """
    VIEWER_GROUPS: ClassVar[KeywordField] = KeywordField("viewerGroups", "viewerGroups")
    """
    TBC
    """
    CONNECTOR_NAME: ClassVar[KeywordField] = KeywordField(
        "connectorName", "connectorName"
    )
    """
    TBC
    """
    CONNECTION_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "connectionName", "connectionName", "connectionName.text"
    )
    """
    TBC
    """
    CONNECTION_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "connectionQualifiedName",
        "connectionQualifiedName",
        "connectionQualifiedName.text",
    )
    """
    TBC
    """
    HAS_LINEAGE: ClassVar[BooleanField] = BooleanField("__hasLineage", "__hasLineage")
    """
    TBC
    """
    IS_DISCOVERABLE: ClassVar[BooleanField] = BooleanField(
        "isDiscoverable", "isDiscoverable"
    )
    """
    TBC
    """
    IS_EDITABLE: ClassVar[BooleanField] = BooleanField("isEditable", "isEditable")
    """
    TBC
    """
    SUB_TYPE: ClassVar[KeywordField] = KeywordField("subType", "subType")
    """
    TBC
    """
    VIEW_SCORE: ClassVar[NumericRankField] = NumericRankField(
        "viewScore", "viewScore", "viewScore.rank_feature"
    )
    """
    TBC
    """
    POPULARITY_SCORE: ClassVar[NumericRankField] = NumericRankField(
        "popularityScore", "popularityScore", "popularityScore.rank_feature"
    )
    """
    TBC
    """
    SOURCE_OWNERS: ClassVar[KeywordField] = KeywordField("sourceOwners", "sourceOwners")
    """
    TBC
    """
    SOURCE_CREATED_BY: ClassVar[KeywordField] = KeywordField(
        "sourceCreatedBy", "sourceCreatedBy"
    )
    """
    TBC
    """
    SOURCE_CREATED_AT: ClassVar[NumericField] = NumericField(
        "sourceCreatedAt", "sourceCreatedAt"
    )
    """
    TBC
    """
    SOURCE_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "sourceUpdatedAt", "sourceUpdatedAt"
    )
    """
    TBC
    """
    SOURCE_UPDATED_BY: ClassVar[KeywordField] = KeywordField(
        "sourceUpdatedBy", "sourceUpdatedBy"
    )
    """
    TBC
    """
    SOURCE_URL: ClassVar[KeywordField] = KeywordField("sourceURL", "sourceURL")
    """
    TBC
    """
    SOURCE_EMBED_URL: ClassVar[KeywordField] = KeywordField(
        "sourceEmbedURL", "sourceEmbedURL"
    )
    """
    TBC
    """
    LAST_SYNC_WORKFLOW_NAME: ClassVar[KeywordField] = KeywordField(
        "lastSyncWorkflowName", "lastSyncWorkflowName"
    )
    """
    TBC
    """
    LAST_SYNC_RUN_AT: ClassVar[NumericField] = NumericField(
        "lastSyncRunAt", "lastSyncRunAt"
    )
    """
    TBC
    """
    LAST_SYNC_RUN: ClassVar[KeywordField] = KeywordField("lastSyncRun", "lastSyncRun")
    """
    TBC
    """
    ADMIN_ROLES: ClassVar[KeywordField] = KeywordField("adminRoles", "adminRoles")
    """
    TBC
    """
    SOURCE_READ_COUNT: ClassVar[NumericField] = NumericField(
        "sourceReadCount", "sourceReadCount"
    )
    """
    Total count of all read operations at source
    """
    SOURCE_READ_USER_COUNT: ClassVar[NumericField] = NumericField(
        "sourceReadUserCount", "sourceReadUserCount"
    )
    """
    Total number of unique users that read data from asset
    """
    SOURCE_LAST_READ_AT: ClassVar[NumericField] = NumericField(
        "sourceLastReadAt", "sourceLastReadAt"
    )
    """
    Timestamp of most recent read operation
    """
    LAST_ROW_CHANGED_AT: ClassVar[NumericField] = NumericField(
        "lastRowChangedAt", "lastRowChangedAt"
    )
    """
    Timestamp of last operation that inserted/updated/deleted rows. Google Sheets, Mysql table etc
    """
    SOURCE_TOTAL_COST: ClassVar[NumericField] = NumericField(
        "sourceTotalCost", "sourceTotalCost"
    )
    """
    Total cost of all operations at source
    """
    SOURCE_COST_UNIT: ClassVar[KeywordField] = KeywordField(
        "sourceCostUnit", "sourceCostUnit"
    )
    """
    The unit of measure for sourceTotalCost
    """
    SOURCE_READ_QUERY_COST: ClassVar[NumericField] = NumericField(
        "sourceReadQueryCost", "sourceReadQueryCost"
    )
    """
    Total cost of read queries at source
    """
    SOURCE_READ_RECENT_USER_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadRecentUserList", "sourceReadRecentUserList"
    )
    """
    List of usernames of the most recent users who read the asset
    """
    SOURCE_READ_RECENT_USER_RECORD_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadRecentUserRecordList", "sourceReadRecentUserRecordList"
    )
    """
    List of usernames with extra insights for the most recent users who read the asset
    """
    SOURCE_READ_TOP_USER_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadTopUserList", "sourceReadTopUserList"
    )
    """
    List of usernames of the top users who read the asset the most
    """
    SOURCE_READ_TOP_USER_RECORD_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadTopUserRecordList", "sourceReadTopUserRecordList"
    )
    """
    List of usernames with extra insights for the top users who read the asset the most
    """
    SOURCE_READ_POPULAR_QUERY_RECORD_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadPopularQueryRecordList", "sourceReadPopularQueryRecordList"
    )
    """
    List of the most popular queries that accessed this asset
    """
    SOURCE_READ_EXPENSIVE_QUERY_RECORD_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadExpensiveQueryRecordList", "sourceReadExpensiveQueryRecordList"
    )
    """
    List of the most expensive queries that accessed this asset
    """
    SOURCE_READ_SLOW_QUERY_RECORD_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceReadSlowQueryRecordList", "sourceReadSlowQueryRecordList"
    )
    """
    List of the slowest queries that accessed this asset
    """
    SOURCE_QUERY_COMPUTE_COST_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceQueryComputeCostList", "sourceQueryComputeCostList"
    )
    """
    List of most expensive warehouse names
    """
    SOURCE_QUERY_COMPUTE_COST_RECORD_LIST: ClassVar[KeywordField] = KeywordField(
        "sourceQueryComputeCostRecordList", "sourceQueryComputeCostRecordList"
    )
    """
    List of most expensive warehouses with extra insights
    """
    DBT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtQualifiedName", "dbtQualifiedName", "dbtQualifiedName.text"
    )
    """
    TBC
    """
    ASSET_DBT_ALIAS: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtAlias", "assetDbtAlias.keyword", "assetDbtAlias"
    )
    """
    TBC
    """
    ASSET_DBT_META: ClassVar[KeywordField] = KeywordField(
        "assetDbtMeta", "assetDbtMeta"
    )
    """
    TBC
    """
    ASSET_DBT_UNIQUE_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtUniqueId", "assetDbtUniqueId.keyword", "assetDbtUniqueId"
    )
    """
    TBC
    """
    ASSET_DBT_ACCOUNT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtAccountName", "assetDbtAccountName.keyword", "assetDbtAccountName"
    )
    """
    TBC
    """
    ASSET_DBT_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtProjectName", "assetDbtProjectName.keyword", "assetDbtProjectName"
    )
    """
    TBC
    """
    ASSET_DBT_PACKAGE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtPackageName", "assetDbtPackageName.keyword", "assetDbtPackageName"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtJobName", "assetDbtJobName.keyword", "assetDbtJobName"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobSchedule", "assetDbtJobSchedule"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_STATUS: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobStatus", "assetDbtJobStatus"
    )
    """
    TBC
    """
    ASSET_DBT_TEST_STATUS: ClassVar[KeywordField] = KeywordField(
        "assetDbtTestStatus", "assetDbtTestStatus"
    )
    """
    All associated dbt test statuses
    """
    ASSET_DBT_JOB_SCHEDULE_CRON_HUMANIZED: ClassVar[TextField] = TextField(
        "assetDbtJobScheduleCronHumanized", "assetDbtJobScheduleCronHumanized"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN: ClassVar[NumericField] = NumericField(
        "assetDbtJobLastRun", "assetDbtJobLastRun"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_URL: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunUrl", "assetDbtJobLastRunUrl"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_CREATED_AT: ClassVar[NumericField] = NumericField(
        "assetDbtJobLastRunCreatedAt", "assetDbtJobLastRunCreatedAt"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "assetDbtJobLastRunUpdatedAt", "assetDbtJobLastRunUpdatedAt"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_DEQUED_AT: ClassVar[NumericField] = NumericField(
        "assetDbtJobLastRunDequedAt", "assetDbtJobLastRunDequedAt"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_STARTED_AT: ClassVar[NumericField] = NumericField(
        "assetDbtJobLastRunStartedAt", "assetDbtJobLastRunStartedAt"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_TOTAL_DURATION: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunTotalDuration", "assetDbtJobLastRunTotalDuration"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_TOTAL_DURATION_HUMANIZED: ClassVar[
        KeywordField
    ] = KeywordField(
        "assetDbtJobLastRunTotalDurationHumanized",
        "assetDbtJobLastRunTotalDurationHumanized",
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_QUEUED_DURATION: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunQueuedDuration", "assetDbtJobLastRunQueuedDuration"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_QUEUED_DURATION_HUMANIZED: ClassVar[
        KeywordField
    ] = KeywordField(
        "assetDbtJobLastRunQueuedDurationHumanized",
        "assetDbtJobLastRunQueuedDurationHumanized",
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_RUN_DURATION: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunRunDuration", "assetDbtJobLastRunRunDuration"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_RUN_DURATION_HUMANIZED: ClassVar[
        KeywordField
    ] = KeywordField(
        "assetDbtJobLastRunRunDurationHumanized",
        "assetDbtJobLastRunRunDurationHumanized",
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_GIT_BRANCH: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtJobLastRunGitBranch",
        "assetDbtJobLastRunGitBranch",
        "assetDbtJobLastRunGitBranch.text",
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_GIT_SHA: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunGitSha", "assetDbtJobLastRunGitSha"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_STATUS_MESSAGE: ClassVar[
        KeywordTextField
    ] = KeywordTextField(
        "assetDbtJobLastRunStatusMessage",
        "assetDbtJobLastRunStatusMessage.keyword",
        "assetDbtJobLastRunStatusMessage",
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_OWNER_THREAD_ID: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunOwnerThreadId", "assetDbtJobLastRunOwnerThreadId"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_EXECUTED_BY_THREAD_ID: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunExecutedByThreadId", "assetDbtJobLastRunExecutedByThreadId"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_ARTIFACTS_SAVED: ClassVar[BooleanField] = BooleanField(
        "assetDbtJobLastRunArtifactsSaved", "assetDbtJobLastRunArtifactsSaved"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_ARTIFACT_S3PATH: ClassVar[KeywordField] = KeywordField(
        "assetDbtJobLastRunArtifactS3Path", "assetDbtJobLastRunArtifactS3Path"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_HAS_DOCS_GENERATED: ClassVar[BooleanField] = BooleanField(
        "assetDbtJobLastRunHasDocsGenerated", "assetDbtJobLastRunHasDocsGenerated"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_HAS_SOURCES_GENERATED: ClassVar[BooleanField] = BooleanField(
        "assetDbtJobLastRunHasSourcesGenerated", "assetDbtJobLastRunHasSourcesGenerated"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_LAST_RUN_NOTIFICATIONS_SENT: ClassVar[BooleanField] = BooleanField(
        "assetDbtJobLastRunNotificationsSent", "assetDbtJobLastRunNotificationsSent"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_NEXT_RUN: ClassVar[NumericField] = NumericField(
        "assetDbtJobNextRun", "assetDbtJobNextRun"
    )
    """
    TBC
    """
    ASSET_DBT_JOB_NEXT_RUN_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtJobNextRunHumanized",
        "assetDbtJobNextRunHumanized.keyword",
        "assetDbtJobNextRunHumanized",
    )
    """
    TBC
    """
    ASSET_DBT_ENVIRONMENT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtEnvironmentName",
        "assetDbtEnvironmentName.keyword",
        "assetDbtEnvironmentName",
    )
    """
    TBC
    """
    ASSET_DBT_ENVIRONMENT_DBT_VERSION: ClassVar[KeywordField] = KeywordField(
        "assetDbtEnvironmentDbtVersion", "assetDbtEnvironmentDbtVersion"
    )
    """
    TBC
    """
    ASSET_DBT_TAGS: ClassVar[KeywordTextField] = KeywordTextField(
        "assetDbtTags", "assetDbtTags", "assetDbtTags.text"
    )
    """
    TBC
    """
    ASSET_DBT_SEMANTIC_LAYER_PROXY_URL: ClassVar[KeywordField] = KeywordField(
        "assetDbtSemanticLayerProxyUrl", "assetDbtSemanticLayerProxyUrl"
    )
    """
    TBC
    """
    ASSET_DBT_SOURCE_FRESHNESS_CRITERIA: ClassVar[KeywordField] = KeywordField(
        "assetDbtSourceFreshnessCriteria", "assetDbtSourceFreshnessCriteria"
    )
    """
    TBC
    """
    SAMPLE_DATA_URL: ClassVar[KeywordTextField] = KeywordTextField(
        "sampleDataUrl", "sampleDataUrl", "sampleDataUrl.text"
    )
    """
    TBC
    """
    ASSET_TAGS: ClassVar[KeywordTextField] = KeywordTextField(
        "assetTags", "assetTags", "assetTags.text"
    )
    """
    TBC
    """
    ASSET_MC_INCIDENT_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "assetMcIncidentNames", "assetMcIncidentNames.keyword", "assetMcIncidentNames"
    )
    """
    TBC
    """
    ASSET_MC_INCIDENT_QUALIFIED_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "assetMcIncidentQualifiedNames",
        "assetMcIncidentQualifiedNames",
        "assetMcIncidentQualifiedNames.text",
    )
    """
    TBC
    """
    ASSET_MC_MONITOR_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "assetMcMonitorNames", "assetMcMonitorNames.keyword", "assetMcMonitorNames"
    )
    """
    TBC
    """
    ASSET_MC_MONITOR_QUALIFIED_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "assetMcMonitorQualifiedNames",
        "assetMcMonitorQualifiedNames",
        "assetMcMonitorQualifiedNames.text",
    )
    """
    TBC
    """
    ASSET_MC_MONITOR_STATUSES: ClassVar[KeywordField] = KeywordField(
        "assetMcMonitorStatuses", "assetMcMonitorStatuses"
    )
    """
    All associated monitors statuses
    """
    ASSET_MC_MONITOR_TYPES: ClassVar[KeywordField] = KeywordField(
        "assetMcMonitorTypes", "assetMcMonitorTypes"
    )
    """
    All associated monitor types
    """
    ASSET_MC_MONITOR_SCHEDULE_TYPES: ClassVar[KeywordField] = KeywordField(
        "assetMcMonitorScheduleTypes", "assetMcMonitorScheduleTypes"
    )
    """
    MonteCarlo Monitor schedule type
    """
    ASSET_MC_INCIDENT_TYPES: ClassVar[KeywordField] = KeywordField(
        "assetMcIncidentTypes", "assetMcIncidentTypes"
    )
    """
    TBC
    """
    ASSET_MC_INCIDENT_SUB_TYPES: ClassVar[KeywordField] = KeywordField(
        "assetMcIncidentSubTypes", "assetMcIncidentSubTypes"
    )
    """
    TBC
    """
    ASSET_MC_INCIDENT_SEVERITIES: ClassVar[KeywordField] = KeywordField(
        "assetMcIncidentSeverities", "assetMcIncidentSeverities"
    )
    """
    TBC
    """
    ASSET_MC_INCIDENT_STATES: ClassVar[KeywordField] = KeywordField(
        "assetMcIncidentStates", "assetMcIncidentStates"
    )
    """
    TBC
    """
    ASSET_MC_LAST_SYNC_RUN_AT: ClassVar[NumericField] = NumericField(
        "assetMcLastSyncRunAt", "assetMcLastSyncRunAt"
    )
    """
    TBC
    """
    STARRED_BY: ClassVar[KeywordField] = KeywordField("starredBy", "starredBy")
    """
    TBC
    """
    STARRED_DETAILS_LIST: ClassVar[KeywordField] = KeywordField(
        "starredDetailsList", "starredDetailsList"
    )
    """
    List of usernames with extra information of the users who have starred an asset
    """
    STARRED_COUNT: ClassVar[NumericField] = NumericField("starredCount", "starredCount")
    """
    TBC
    """
    ASSET_SODA_DQ_STATUS: ClassVar[KeywordField] = KeywordField(
        "assetSodaDQStatus", "assetSodaDQStatus"
    )
    """
    Soda DQ Status
    """
    ASSET_SODA_CHECK_COUNT: ClassVar[NumericField] = NumericField(
        "assetSodaCheckCount", "assetSodaCheckCount"
    )
    """
    Soda check count
    """
    ASSET_SODA_LAST_SYNC_RUN_AT: ClassVar[NumericField] = NumericField(
        "assetSodaLastSyncRunAt", "assetSodaLastSyncRunAt"
    )
    """
    TBC
    """
    ASSET_SODA_LAST_SCAN_AT: ClassVar[NumericField] = NumericField(
        "assetSodaLastScanAt", "assetSodaLastScanAt"
    )
    """
    TBC
    """
    ASSET_SODA_CHECK_STATUSES: ClassVar[KeywordField] = KeywordField(
        "assetSodaCheckStatuses", "assetSodaCheckStatuses"
    )
    """
    All associated soda check statuses
    """
    ASSET_SODA_SOURCE_URL: ClassVar[KeywordField] = KeywordField(
        "assetSodaSourceURL", "assetSodaSourceURL"
    )
    """
    TBC
    """
    ASSET_ICON: ClassVar[KeywordField] = KeywordField("assetIcon", "assetIcon")
    """
    TBC
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
        "schema_registry_subjects",
        "mc_monitors",
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
        name: Optional[str] = Field(None, description="", alias="name")
        display_name: Optional[str] = Field(None, description="", alias="displayName")
        description: Optional[str] = Field(None, description="", alias="description")
        user_description: Optional[str] = Field(
            None, description="", alias="userDescription"
        )
        tenant_id: Optional[str] = Field(None, description="", alias="tenantId")
        certificate_status: Optional[CertificateStatus] = Field(
            None, description="", alias="certificateStatus"
        )
        certificate_status_message: Optional[str] = Field(
            None, description="", alias="certificateStatusMessage"
        )
        certificate_updated_by: Optional[str] = Field(
            None, description="", alias="certificateUpdatedBy"
        )
        certificate_updated_at: Optional[datetime] = Field(
            None, description="", alias="certificateUpdatedAt"
        )
        announcement_title: Optional[str] = Field(
            None, description="", alias="announcementTitle"
        )
        announcement_message: Optional[str] = Field(
            None, description="", alias="announcementMessage"
        )
        announcement_type: Optional[str] = Field(
            None, description="", alias="announcementType"
        )
        announcement_updated_at: Optional[datetime] = Field(
            None, description="", alias="announcementUpdatedAt"
        )
        announcement_updated_by: Optional[str] = Field(
            None, description="", alias="announcementUpdatedBy"
        )
        owner_users: Optional[set[str]] = Field(
            None, description="", alias="ownerUsers"
        )
        owner_groups: Optional[set[str]] = Field(
            None, description="", alias="ownerGroups"
        )
        admin_users: Optional[set[str]] = Field(
            None, description="", alias="adminUsers"
        )
        admin_groups: Optional[set[str]] = Field(
            None, description="", alias="adminGroups"
        )
        viewer_users: Optional[set[str]] = Field(
            None, description="", alias="viewerUsers"
        )
        viewer_groups: Optional[set[str]] = Field(
            None, description="", alias="viewerGroups"
        )
        connector_name: Optional[str] = Field(
            None, description="", alias="connectorName"
        )
        connection_name: Optional[str] = Field(
            None, description="", alias="connectionName"
        )
        connection_qualified_name: Optional[str] = Field(
            None, description="", alias="connectionQualifiedName"
        )
        has_lineage: Optional[bool] = Field(None, description="", alias="__hasLineage")
        is_discoverable: Optional[bool] = Field(
            None, description="", alias="isDiscoverable"
        )
        is_editable: Optional[bool] = Field(None, description="", alias="isEditable")
        sub_type: Optional[str] = Field(None, description="", alias="subType")
        view_score: Optional[float] = Field(None, description="", alias="viewScore")
        popularity_score: Optional[float] = Field(
            None, description="", alias="popularityScore"
        )
        source_owners: Optional[str] = Field(None, description="", alias="sourceOwners")
        source_created_by: Optional[str] = Field(
            None, description="", alias="sourceCreatedBy"
        )
        source_created_at: Optional[datetime] = Field(
            None, description="", alias="sourceCreatedAt"
        )
        source_updated_at: Optional[datetime] = Field(
            None, description="", alias="sourceUpdatedAt"
        )
        source_updated_by: Optional[str] = Field(
            None, description="", alias="sourceUpdatedBy"
        )
        source_url: Optional[str] = Field(None, description="", alias="sourceURL")
        source_embed_url: Optional[str] = Field(
            None, description="", alias="sourceEmbedURL"
        )
        last_sync_workflow_name: Optional[str] = Field(
            None, description="", alias="lastSyncWorkflowName"
        )
        last_sync_run_at: Optional[datetime] = Field(
            None, description="", alias="lastSyncRunAt"
        )
        last_sync_run: Optional[str] = Field(None, description="", alias="lastSyncRun")
        admin_roles: Optional[set[str]] = Field(
            None, description="", alias="adminRoles"
        )
        source_read_count: Optional[int] = Field(
            None, description="", alias="sourceReadCount"
        )
        source_read_user_count: Optional[int] = Field(
            None, description="", alias="sourceReadUserCount"
        )
        source_last_read_at: Optional[datetime] = Field(
            None, description="", alias="sourceLastReadAt"
        )
        last_row_changed_at: Optional[datetime] = Field(
            None, description="", alias="lastRowChangedAt"
        )
        source_total_cost: Optional[float] = Field(
            None, description="", alias="sourceTotalCost"
        )
        source_cost_unit: Optional[SourceCostUnitType] = Field(
            None, description="", alias="sourceCostUnit"
        )
        source_read_query_cost: Optional[float] = Field(
            None, description="", alias="sourceReadQueryCost"
        )
        source_read_recent_user_list: Optional[set[str]] = Field(
            None, description="", alias="sourceReadRecentUserList"
        )
        source_read_recent_user_record_list: Optional[list[PopularityInsights]] = Field(
            None, description="", alias="sourceReadRecentUserRecordList"
        )
        source_read_top_user_list: Optional[set[str]] = Field(
            None, description="", alias="sourceReadTopUserList"
        )
        source_read_top_user_record_list: Optional[list[PopularityInsights]] = Field(
            None, description="", alias="sourceReadTopUserRecordList"
        )
        source_read_popular_query_record_list: Optional[
            list[PopularityInsights]
        ] = Field(None, description="", alias="sourceReadPopularQueryRecordList")
        source_read_expensive_query_record_list: Optional[
            list[PopularityInsights]
        ] = Field(None, description="", alias="sourceReadExpensiveQueryRecordList")
        source_read_slow_query_record_list: Optional[list[PopularityInsights]] = Field(
            None, description="", alias="sourceReadSlowQueryRecordList"
        )
        source_query_compute_cost_list: Optional[set[str]] = Field(
            None, description="", alias="sourceQueryComputeCostList"
        )
        source_query_compute_cost_record_list: Optional[
            list[PopularityInsights]
        ] = Field(None, description="", alias="sourceQueryComputeCostRecordList")
        dbt_qualified_name: Optional[str] = Field(
            None, description="", alias="dbtQualifiedName"
        )
        asset_dbt_alias: Optional[str] = Field(
            None, description="", alias="assetDbtAlias"
        )
        asset_dbt_meta: Optional[str] = Field(
            None, description="", alias="assetDbtMeta"
        )
        asset_dbt_unique_id: Optional[str] = Field(
            None, description="", alias="assetDbtUniqueId"
        )
        asset_dbt_account_name: Optional[str] = Field(
            None, description="", alias="assetDbtAccountName"
        )
        asset_dbt_project_name: Optional[str] = Field(
            None, description="", alias="assetDbtProjectName"
        )
        asset_dbt_package_name: Optional[str] = Field(
            None, description="", alias="assetDbtPackageName"
        )
        asset_dbt_job_name: Optional[str] = Field(
            None, description="", alias="assetDbtJobName"
        )
        asset_dbt_job_schedule: Optional[str] = Field(
            None, description="", alias="assetDbtJobSchedule"
        )
        asset_dbt_job_status: Optional[str] = Field(
            None, description="", alias="assetDbtJobStatus"
        )
        asset_dbt_test_status: Optional[str] = Field(
            None, description="", alias="assetDbtTestStatus"
        )
        asset_dbt_job_schedule_cron_humanized: Optional[str] = Field(
            None, description="", alias="assetDbtJobScheduleCronHumanized"
        )
        asset_dbt_job_last_run: Optional[datetime] = Field(
            None, description="", alias="assetDbtJobLastRun"
        )
        asset_dbt_job_last_run_url: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunUrl"
        )
        asset_dbt_job_last_run_created_at: Optional[datetime] = Field(
            None, description="", alias="assetDbtJobLastRunCreatedAt"
        )
        asset_dbt_job_last_run_updated_at: Optional[datetime] = Field(
            None, description="", alias="assetDbtJobLastRunUpdatedAt"
        )
        asset_dbt_job_last_run_dequed_at: Optional[datetime] = Field(
            None, description="", alias="assetDbtJobLastRunDequedAt"
        )
        asset_dbt_job_last_run_started_at: Optional[datetime] = Field(
            None, description="", alias="assetDbtJobLastRunStartedAt"
        )
        asset_dbt_job_last_run_total_duration: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunTotalDuration"
        )
        asset_dbt_job_last_run_total_duration_humanized: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunTotalDurationHumanized"
        )
        asset_dbt_job_last_run_queued_duration: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunQueuedDuration"
        )
        asset_dbt_job_last_run_queued_duration_humanized: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunQueuedDurationHumanized"
        )
        asset_dbt_job_last_run_run_duration: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunRunDuration"
        )
        asset_dbt_job_last_run_run_duration_humanized: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunRunDurationHumanized"
        )
        asset_dbt_job_last_run_git_branch: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunGitBranch"
        )
        asset_dbt_job_last_run_git_sha: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunGitSha"
        )
        asset_dbt_job_last_run_status_message: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunStatusMessage"
        )
        asset_dbt_job_last_run_owner_thread_id: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunOwnerThreadId"
        )
        asset_dbt_job_last_run_executed_by_thread_id: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunExecutedByThreadId"
        )
        asset_dbt_job_last_run_artifacts_saved: Optional[bool] = Field(
            None, description="", alias="assetDbtJobLastRunArtifactsSaved"
        )
        asset_dbt_job_last_run_artifact_s3_path: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunArtifactS3Path"
        )
        asset_dbt_job_last_run_has_docs_generated: Optional[bool] = Field(
            None, description="", alias="assetDbtJobLastRunHasDocsGenerated"
        )
        asset_dbt_job_last_run_has_sources_generated: Optional[bool] = Field(
            None, description="", alias="assetDbtJobLastRunHasSourcesGenerated"
        )
        asset_dbt_job_last_run_notifications_sent: Optional[bool] = Field(
            None, description="", alias="assetDbtJobLastRunNotificationsSent"
        )
        asset_dbt_job_next_run: Optional[datetime] = Field(
            None, description="", alias="assetDbtJobNextRun"
        )
        asset_dbt_job_next_run_humanized: Optional[str] = Field(
            None, description="", alias="assetDbtJobNextRunHumanized"
        )
        asset_dbt_environment_name: Optional[str] = Field(
            None, description="", alias="assetDbtEnvironmentName"
        )
        asset_dbt_environment_dbt_version: Optional[str] = Field(
            None, description="", alias="assetDbtEnvironmentDbtVersion"
        )
        asset_dbt_tags: Optional[set[str]] = Field(
            None, description="", alias="assetDbtTags"
        )
        asset_dbt_semantic_layer_proxy_url: Optional[str] = Field(
            None, description="", alias="assetDbtSemanticLayerProxyUrl"
        )
        asset_dbt_source_freshness_criteria: Optional[str] = Field(
            None, description="", alias="assetDbtSourceFreshnessCriteria"
        )
        sample_data_url: Optional[str] = Field(
            None, description="", alias="sampleDataUrl"
        )
        asset_tags: Optional[set[str]] = Field(None, description="", alias="assetTags")
        asset_mc_incident_names: Optional[set[str]] = Field(
            None, description="", alias="assetMcIncidentNames"
        )
        asset_mc_incident_qualified_names: Optional[set[str]] = Field(
            None, description="", alias="assetMcIncidentQualifiedNames"
        )
        asset_mc_monitor_names: Optional[set[str]] = Field(
            None, description="", alias="assetMcMonitorNames"
        )
        asset_mc_monitor_qualified_names: Optional[set[str]] = Field(
            None, description="", alias="assetMcMonitorQualifiedNames"
        )
        asset_mc_monitor_statuses: Optional[set[str]] = Field(
            None, description="", alias="assetMcMonitorStatuses"
        )
        asset_mc_monitor_types: Optional[set[str]] = Field(
            None, description="", alias="assetMcMonitorTypes"
        )
        asset_mc_monitor_schedule_types: Optional[set[str]] = Field(
            None, description="", alias="assetMcMonitorScheduleTypes"
        )
        asset_mc_incident_types: Optional[set[str]] = Field(
            None, description="", alias="assetMcIncidentTypes"
        )
        asset_mc_incident_sub_types: Optional[set[str]] = Field(
            None, description="", alias="assetMcIncidentSubTypes"
        )
        asset_mc_incident_severities: Optional[set[str]] = Field(
            None, description="", alias="assetMcIncidentSeverities"
        )
        asset_mc_incident_states: Optional[set[str]] = Field(
            None, description="", alias="assetMcIncidentStates"
        )
        asset_mc_last_sync_run_at: Optional[datetime] = Field(
            None, description="", alias="assetMcLastSyncRunAt"
        )
        starred_by: Optional[set[str]] = Field(None, description="", alias="starredBy")
        starred_details_list: Optional[list[StarredDetails]] = Field(
            None, description="", alias="starredDetailsList"
        )
        starred_count: Optional[int] = Field(None, description="", alias="starredCount")
        asset_soda_d_q_status: Optional[str] = Field(
            None, description="", alias="assetSodaDQStatus"
        )
        asset_soda_check_count: Optional[int] = Field(
            None, description="", alias="assetSodaCheckCount"
        )
        asset_soda_last_sync_run_at: Optional[datetime] = Field(
            None, description="", alias="assetSodaLastSyncRunAt"
        )
        asset_soda_last_scan_at: Optional[datetime] = Field(
            None, description="", alias="assetSodaLastScanAt"
        )
        asset_soda_check_statuses: Optional[str] = Field(
            None, description="", alias="assetSodaCheckStatuses"
        )
        asset_soda_source_url: Optional[str] = Field(
            None, description="", alias="assetSodaSourceURL"
        )
        asset_icon: Optional[str] = Field(None, description="", alias="assetIcon")
        schema_registry_subjects: Optional[list[SchemaRegistrySubject]] = Field(
            None, description="", alias="schemaRegistrySubjects"
        )  # relationship
        mc_monitors: Optional[list[MCMonitor]] = Field(
            None, description="", alias="mcMonitors"
        )  # relationship
        files: Optional[list[File]] = Field(
            None, description="", alias="files"
        )  # relationship
        mc_incidents: Optional[list[MCIncident]] = Field(
            None, description="", alias="mcIncidents"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        soda_checks: Optional[list[SodaCheck]] = Field(
            None, description="", alias="sodaChecks"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
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
        "categories", "__parentCategory"
    )
    """Parent category in which a subcategory is contained, searchable by the qualifiedName of the category."""

    type_name: str = Field("AtlasGlossaryCategory", allow_mutation=False)

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
    TBC
    """
    LONG_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "longDescription", "longDescription"
    )
    """
    TBC
    """
    ADDITIONAL_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "additionalAttributes", "additionalAttributes"
    )
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
        short_description: Optional[str] = Field(
            None, description="", alias="shortDescription"
        )
        long_description: Optional[str] = Field(
            None, description="", alias="longDescription"
        )
        additional_attributes: Optional[dict[str, str]] = Field(
            None, description="", alias="additionalAttributes"
        )
        terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="terms"
        )  # relationship
        anchor: Optional[AtlasGlossary] = Field(
            None, description="", alias="anchor"
        )  # relationship
        parent_category: Optional[AtlasGlossaryCategory] = Field(
            None, description="", alias="parentCategory"
        )  # relationship
        children_categories: Optional[list[AtlasGlossaryCategory]] = Field(
            None, description="", alias="childrenCategories"
        )  # relationship

        @classmethod
        # @validate_arguments()
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
    def create(cls, *, name: StrictStr) -> AtlasGlossary:
        validate_required_fields(["name"], [name])
        return AtlasGlossary(attributes=AtlasGlossary.Attributes.create(name=name))

    type_name: str = Field("AtlasGlossary", allow_mutation=False)

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
    TBC
    """
    LONG_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "longDescription", "longDescription"
    )
    """
    TBC
    """
    LANGUAGE: ClassVar[KeywordField] = KeywordField("language", "language")
    """
    TBC
    """
    USAGE: ClassVar[KeywordField] = KeywordField("usage", "usage")
    """
    TBC
    """
    ADDITIONAL_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "additionalAttributes", "additionalAttributes"
    )
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
        short_description: Optional[str] = Field(
            None, description="", alias="shortDescription"
        )
        long_description: Optional[str] = Field(
            None, description="", alias="longDescription"
        )
        language: Optional[str] = Field(None, description="", alias="language")
        usage: Optional[str] = Field(None, description="", alias="usage")
        additional_attributes: Optional[dict[str, str]] = Field(
            None, description="", alias="additionalAttributes"
        )
        terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="terms"
        )  # relationship
        categories: Optional[list[AtlasGlossaryCategory]] = Field(
            None, description="", alias="categories"
        )  # relationship

        @classmethod
        # @validate_arguments()
        def create(cls, *, name: StrictStr) -> AtlasGlossary.Attributes:
            validate_required_fields(["name"], [name])
            return AtlasGlossary.Attributes(name=name, qualified_name=next_id())

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

    type_name: str = Field("AtlasGlossaryTerm", allow_mutation=False)

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
    TBC
    """
    LONG_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "longDescription", "longDescription"
    )
    """
    TBC
    """
    EXAMPLES: ClassVar[KeywordField] = KeywordField("examples", "examples")
    """
    TBC
    """
    ABBREVIATION: ClassVar[KeywordField] = KeywordField("abbreviation", "abbreviation")
    """
    TBC
    """
    USAGE: ClassVar[KeywordField] = KeywordField("usage", "usage")
    """
    TBC
    """
    ADDITIONAL_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "additionalAttributes", "additionalAttributes"
    )
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
        short_description: Optional[str] = Field(
            None, description="", alias="shortDescription"
        )
        long_description: Optional[str] = Field(
            None, description="", alias="longDescription"
        )
        examples: Optional[set[str]] = Field(None, description="", alias="examples")
        abbreviation: Optional[str] = Field(None, description="", alias="abbreviation")
        usage: Optional[str] = Field(None, description="", alias="usage")
        additional_attributes: Optional[dict[str, str]] = Field(
            None, description="", alias="additionalAttributes"
        )
        valid_values_for: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="validValuesFor"
        )  # relationship
        valid_values: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="validValues"
        )  # relationship
        see_also: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="seeAlso"
        )  # relationship
        is_a: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="isA"
        )  # relationship
        antonyms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="antonyms"
        )  # relationship
        assigned_entities: Optional[list[Referenceable]] = Field(
            None, description="", alias="assignedEntities"
        )  # relationship
        classifies: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="classifies"
        )  # relationship
        categories: Optional[list[AtlasGlossaryCategory]] = Field(
            None, description="", alias="categories"
        )  # relationship
        preferred_to_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="preferredToTerms"
        )  # relationship
        preferred_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="preferredTerms"
        )  # relationship
        translation_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="translationTerms"
        )  # relationship
        synonyms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="synonyms"
        )  # relationship
        replaced_by: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="replacedBy"
        )  # relationship
        replacement_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="replacementTerms"
        )  # relationship
        translated_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="translatedTerms"
        )  # relationship
        anchor: Optional[AtlasGlossary] = Field(
            None, description="", alias="anchor"
        )  # relationship

        @classmethod
        # @validate_arguments()
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

    type_name: str = Field("Process", allow_mutation=False)

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
    TBC
    """
    SQL: ClassVar[KeywordField] = KeywordField("sql", "sql")
    """
    TBC
    """
    AST: ClassVar[KeywordField] = KeywordField("ast", "ast")
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
        inputs: Optional[list[Catalog]] = Field(None, description="", alias="inputs")
        outputs: Optional[list[Catalog]] = Field(None, description="", alias="outputs")
        code: Optional[str] = Field(None, description="", alias="code")
        sql: Optional[str] = Field(None, description="", alias="sql")
        ast: Optional[str] = Field(None, description="", alias="ast")
        airflow_tasks: Optional[list[AirflowTask]] = Field(
            None, description="", alias="airflowTasks"
        )  # relationship
        column_processes: Optional[list[ColumnProcess]] = Field(
            None, description="", alias="columnProcesses"
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

    type_name: str = Field("Namespace", allow_mutation=False)

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
            None, description="", alias="childrenQueries"
        )  # relationship
        children_folders: Optional[list[Folder]] = Field(
            None, description="", alias="childrenFolders"
        )  # relationship

    attributes: "Namespace.Attributes" = Field(
        default_factory=lambda: Namespace.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Folder(Namespace):
    """Description"""

    type_name: str = Field("Folder", allow_mutation=False)

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
    TBC
    """
    COLLECTION_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "collectionQualifiedName",
        "collectionQualifiedName",
        "collectionQualifiedName.text",
    )
    """
    TBC
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
        parent_qualified_name: Optional[str] = Field(
            None, description="", alias="parentQualifiedName"
        )
        collection_qualified_name: Optional[str] = Field(
            None, description="", alias="collectionQualifiedName"
        )
        parent: Optional[Namespace] = Field(
            None, description="", alias="parent"
        )  # relationship

    attributes: "Folder.Attributes" = Field(
        default_factory=lambda: Folder.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Catalog(Asset, type_name="Catalog"):
    """Description"""

    type_name: str = Field("Catalog", allow_mutation=False)

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
            None, description="", alias="inputToProcesses"
        )  # relationship
        output_from_airflow_tasks: Optional[list[AirflowTask]] = Field(
            None, description="", alias="outputFromAirflowTasks"
        )  # relationship
        input_to_airflow_tasks: Optional[list[AirflowTask]] = Field(
            None, description="", alias="inputToAirflowTasks"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Catalog.Attributes" = Field(
        default_factory=lambda: Catalog.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Tag(Catalog):
    """Description"""

    type_name: str = Field("Tag", allow_mutation=False)

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
    Unique source tag identifier
    """
    TAG_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "tagAttributes", "tagAttributes"
    )
    """
    Source tag attributes
    """
    TAG_ALLOWED_VALUES: ClassVar[KeywordTextField] = KeywordTextField(
        "tagAllowedValues", "tagAllowedValues", "tagAllowedValues.text"
    )
    """
    Allowed values for the tag at source. De-normalised from sourceTagAttributed for ease of querying
    """
    MAPPED_CLASSIFICATION_NAME: ClassVar[KeywordField] = KeywordField(
        "mappedClassificationName", "mappedClassificationName"
    )
    """
    Mapped atlan classification name
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
        tag_id: Optional[str] = Field(None, description="", alias="tagId")
        tag_attributes: Optional[list[SourceTagAttribute]] = Field(
            None, description="", alias="tagAttributes"
        )
        tag_allowed_values: Optional[set[str]] = Field(
            None, description="", alias="tagAllowedValues"
        )
        mapped_atlan_tag_name: Optional[str] = Field(
            None, description="", alias="mappedClassificationName"
        )

    attributes: "Tag.Attributes" = Field(
        default_factory=lambda: Tag.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ColumnProcess(Process):
    """Description"""

    type_name: str = Field("ColumnProcess", allow_mutation=False)

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
            None, description="", alias="outputs"
        )  # relationship
        process: Optional[Process] = Field(
            None, description="", alias="process"
        )  # relationship
        inputs: Optional[list[Catalog]] = Field(
            None, description="", alias="inputs"
        )  # relationship

    attributes: "ColumnProcess.Attributes" = Field(
        default_factory=lambda: ColumnProcess.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Airflow(Catalog):
    """Description"""

    type_name: str = Field("Airflow", allow_mutation=False)

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
    TBC
    """
    AIRFLOW_RUN_VERSION: ClassVar[KeywordField] = KeywordField(
        "airflowRunVersion", "airflowRunVersion"
    )
    """
    Airflow Version of the run
    """
    AIRFLOW_RUN_OPEN_LINEAGE_VERSION: ClassVar[KeywordField] = KeywordField(
        "airflowRunOpenLineageVersion", "airflowRunOpenLineageVersion"
    )
    """
    OpenLineage Version of the run
    """
    AIRFLOW_RUN_NAME: ClassVar[KeywordField] = KeywordField(
        "airflowRunName", "airflowRunName"
    )
    """
    Name of the run
    """
    AIRFLOW_RUN_TYPE: ClassVar[KeywordField] = KeywordField(
        "airflowRunType", "airflowRunType"
    )
    """
    Type of the run
    """
    AIRFLOW_RUN_START_TIME: ClassVar[NumericField] = NumericField(
        "airflowRunStartTime", "airflowRunStartTime"
    )
    """
    Start time of the run
    """
    AIRFLOW_RUN_END_TIME: ClassVar[NumericField] = NumericField(
        "airflowRunEndTime", "airflowRunEndTime"
    )
    """
    End time of the run
    """
    AIRFLOW_RUN_OPEN_LINEAGE_STATE: ClassVar[KeywordField] = KeywordField(
        "airflowRunOpenLineageState", "airflowRunOpenLineageState"
    )
    """
    OpenLineage state of the run
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
        airflow_tags: Optional[set[str]] = Field(
            None, description="", alias="airflowTags"
        )
        airflow_run_version: Optional[str] = Field(
            None, description="", alias="airflowRunVersion"
        )
        airflow_run_open_lineage_version: Optional[str] = Field(
            None, description="", alias="airflowRunOpenLineageVersion"
        )
        airflow_run_name: Optional[str] = Field(
            None, description="", alias="airflowRunName"
        )
        airflow_run_type: Optional[str] = Field(
            None, description="", alias="airflowRunType"
        )
        airflow_run_start_time: Optional[datetime] = Field(
            None, description="", alias="airflowRunStartTime"
        )
        airflow_run_end_time: Optional[datetime] = Field(
            None, description="", alias="airflowRunEndTime"
        )
        airflow_run_open_lineage_state: Optional[OpenLineageRunState] = Field(
            None, description="", alias="airflowRunOpenLineageState"
        )

    attributes: "Airflow.Attributes" = Field(
        default_factory=lambda: Airflow.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AirflowDag(Airflow):
    """Description"""

    type_name: str = Field("AirflowDag", allow_mutation=False)

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
    TBC
    """
    AIRFLOW_DAG_SCHEDULE_DELTA: ClassVar[NumericField] = NumericField(
        "airflowDagScheduleDelta", "airflowDagScheduleDelta"
    )
    """
    Duration between scheduled runs in seconds
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
        airflow_dag_schedule: Optional[str] = Field(
            None, description="", alias="airflowDagSchedule"
        )
        airflow_dag_schedule_delta: Optional[int] = Field(
            None, description="", alias="airflowDagScheduleDelta"
        )
        airflow_tasks: Optional[list[AirflowTask]] = Field(
            None, description="", alias="airflowTasks"
        )  # relationship

    attributes: "AirflowDag.Attributes" = Field(
        default_factory=lambda: AirflowDag.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AirflowTask(Airflow):
    """Description"""

    type_name: str = Field("AirflowTask", allow_mutation=False)

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
    TBC
    """
    AIRFLOW_DAG_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "airflowDagName", "airflowDagName.keyword", "airflowDagName"
    )
    """
    TBC
    """
    AIRFLOW_DAG_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "airflowDagQualifiedName", "airflowDagQualifiedName"
    )
    """
    TBC
    """
    AIRFLOW_TASK_CONNECTION_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "airflowTaskConnectionId",
        "airflowTaskConnectionId.keyword",
        "airflowTaskConnectionId",
    )
    """
    TBC
    """
    AIRFLOW_TASK_SQL: ClassVar[KeywordField] = KeywordField(
        "airflowTaskSql", "airflowTaskSql"
    )
    """
    TBC
    """
    AIRFLOW_TASK_RETRY_NUMBER: ClassVar[NumericField] = NumericField(
        "airflowTaskRetryNumber", "airflowTaskRetryNumber"
    )
    """
    Retry required for the run
    """
    AIRFLOW_TASK_POOL: ClassVar[KeywordField] = KeywordField(
        "airflowTaskPool", "airflowTaskPool"
    )
    """
    Pool on which this run happened
    """
    AIRFLOW_TASK_POOL_SLOTS: ClassVar[NumericField] = NumericField(
        "airflowTaskPoolSlots", "airflowTaskPoolSlots"
    )
    """
    Pool slots used for the run
    """
    AIRFLOW_TASK_QUEUE: ClassVar[KeywordField] = KeywordField(
        "airflowTaskQueue", "airflowTaskQueue"
    )
    """
    Queue on which this run happened
    """
    AIRFLOW_TASK_PRIORITY_WEIGHT: ClassVar[NumericField] = NumericField(
        "airflowTaskPriorityWeight", "airflowTaskPriorityWeight"
    )
    """
    Priority weight of the run
    """
    AIRFLOW_TASK_TRIGGER_RULE: ClassVar[KeywordField] = KeywordField(
        "airflowTaskTriggerRule", "airflowTaskTriggerRule"
    )
    """
    Trigger rule of the run
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
        airflow_task_operator_class: Optional[str] = Field(
            None, description="", alias="airflowTaskOperatorClass"
        )
        airflow_dag_name: Optional[str] = Field(
            None, description="", alias="airflowDagName"
        )
        airflow_dag_qualified_name: Optional[str] = Field(
            None, description="", alias="airflowDagQualifiedName"
        )
        airflow_task_connection_id: Optional[str] = Field(
            None, description="", alias="airflowTaskConnectionId"
        )
        airflow_task_sql: Optional[str] = Field(
            None, description="", alias="airflowTaskSql"
        )
        airflow_task_retry_number: Optional[int] = Field(
            None, description="", alias="airflowTaskRetryNumber"
        )
        airflow_task_pool: Optional[str] = Field(
            None, description="", alias="airflowTaskPool"
        )
        airflow_task_pool_slots: Optional[int] = Field(
            None, description="", alias="airflowTaskPoolSlots"
        )
        airflow_task_queue: Optional[str] = Field(
            None, description="", alias="airflowTaskQueue"
        )
        airflow_task_priority_weight: Optional[int] = Field(
            None, description="", alias="airflowTaskPriorityWeight"
        )
        airflow_task_trigger_rule: Optional[str] = Field(
            None, description="", alias="airflowTaskTriggerRule"
        )
        outputs: Optional[list[Catalog]] = Field(
            None, description="", alias="outputs"
        )  # relationship
        process: Optional[Process] = Field(
            None, description="", alias="process"
        )  # relationship
        inputs: Optional[list[Catalog]] = Field(
            None, description="", alias="inputs"
        )  # relationship
        airflow_dag: Optional[AirflowDag] = Field(
            None, description="", alias="airflowDag"
        )  # relationship

    attributes: "AirflowTask.Attributes" = Field(
        default_factory=lambda: AirflowTask.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DataQuality(Catalog):
    """Description"""

    type_name: str = Field("DataQuality", allow_mutation=False)

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

    type_name: str = Field("Metric", allow_mutation=False)

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
    TBC
    """
    METRIC_SQL: ClassVar[KeywordField] = KeywordField("metricSQL", "metricSQL")
    """
    TBC
    """
    METRIC_FILTERS: ClassVar[TextField] = TextField("metricFilters", "metricFilters")
    """
    TBC
    """
    METRIC_TIME_GRAINS: ClassVar[TextField] = TextField(
        "metricTimeGrains", "metricTimeGrains"
    )
    """
    TBC
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
        metric_type: Optional[str] = Field(None, description="", alias="metricType")
        metric_s_q_l: Optional[str] = Field(None, description="", alias="metricSQL")
        metric_filters: Optional[str] = Field(
            None, description="", alias="metricFilters"
        )
        metric_time_grains: Optional[set[str]] = Field(
            None, description="", alias="metricTimeGrains"
        )
        metric_timestamp_column: Optional[Column] = Field(
            None, description="", alias="metricTimestampColumn"
        )  # relationship
        assets: Optional[list[Asset]] = Field(
            None, description="", alias="assets"
        )  # relationship
        metric_dimension_columns: Optional[list[Column]] = Field(
            None, description="", alias="metricDimensionColumns"
        )  # relationship

    attributes: "Metric.Attributes" = Field(
        default_factory=lambda: Metric.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Resource(Catalog):
    """Description"""

    type_name: str = Field("Resource", allow_mutation=False)

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
    TBC
    """
    IS_GLOBAL: ClassVar[BooleanField] = BooleanField("isGlobal", "isGlobal")
    """
    TBC
    """
    REFERENCE: ClassVar[KeywordField] = KeywordField("reference", "reference")
    """
    TBC
    """
    RESOURCE_METADATA: ClassVar[KeywordField] = KeywordField(
        "resourceMetadata", "resourceMetadata"
    )
    """
    TBC
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
        link: Optional[str] = Field(None, description="", alias="link")
        is_global: Optional[bool] = Field(None, description="", alias="isGlobal")
        reference: Optional[str] = Field(None, description="", alias="reference")
        resource_metadata: Optional[dict[str, str]] = Field(
            None, description="", alias="resourceMetadata"
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

    type_name: str = Field("Readme", allow_mutation=False)

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
            None, description="", alias="seeAlso"
        )  # relationship
        asset: Optional[Asset] = Field(
            None, description="", alias="asset"
        )  # relationship

        @classmethod
        # @validate_arguments()
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

    type_name: str = Field("File", allow_mutation=False)

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
    TBC
    """
    FILE_PATH: ClassVar[KeywordField] = KeywordField("filePath", "filePath")
    """
    TBC
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
        file_type: Optional[FileType] = Field(None, description="", alias="fileType")
        file_path: Optional[str] = Field(None, description="", alias="filePath")
        file_assets: Optional[Asset] = Field(
            None, description="", alias="fileAssets"
        )  # relationship

        @classmethod
        # @validate_arguments()
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

    type_name: str = Field("Link", allow_mutation=False)

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
    TBC
    """
    ICON_TYPE: ClassVar[KeywordField] = KeywordField("iconType", "iconType")
    """
    TBC
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
        icon: Optional[str] = Field(None, description="", alias="icon")
        icon_type: Optional[IconType] = Field(None, description="", alias="iconType")
        asset: Optional[Asset] = Field(
            None, description="", alias="asset"
        )  # relationship

    attributes: "Link.Attributes" = Field(
        default_factory=lambda: Link.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SQL(Catalog):
    """Description"""

    type_name: str = Field("SQL", allow_mutation=False)

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
    TBC
    """
    QUERY_USER_COUNT: ClassVar[NumericField] = NumericField(
        "queryUserCount", "queryUserCount"
    )
    """
    TBC
    """
    QUERY_USER_MAP: ClassVar[KeywordField] = KeywordField(
        "queryUserMap", "queryUserMap"
    )
    """
    TBC
    """
    QUERY_COUNT_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "queryCountUpdatedAt", "queryCountUpdatedAt"
    )
    """
    TBC
    """
    DATABASE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "databaseName", "databaseName.keyword", "databaseName"
    )
    """
    TBC
    """
    DATABASE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "databaseQualifiedName", "databaseQualifiedName"
    )
    """
    TBC
    """
    SCHEMA_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "schemaName", "schemaName.keyword", "schemaName"
    )
    """
    TBC
    """
    SCHEMA_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "schemaQualifiedName", "schemaQualifiedName"
    )
    """
    TBC
    """
    TABLE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "tableName", "tableName.keyword", "tableName"
    )
    """
    TBC
    """
    TABLE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "tableQualifiedName", "tableQualifiedName"
    )
    """
    TBC
    """
    VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "viewName", "viewName.keyword", "viewName"
    )
    """
    TBC
    """
    VIEW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "viewQualifiedName", "viewQualifiedName"
    )
    """
    TBC
    """
    IS_PROFILED: ClassVar[BooleanField] = BooleanField("isProfiled", "isProfiled")
    """
    TBC
    """
    LAST_PROFILED_AT: ClassVar[NumericField] = NumericField(
        "lastProfiledAt", "lastProfiledAt"
    )
    """
    TBC
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
        query_count: Optional[int] = Field(None, description="", alias="queryCount")
        query_user_count: Optional[int] = Field(
            None, description="", alias="queryUserCount"
        )
        query_user_map: Optional[dict[str, int]] = Field(
            None, description="", alias="queryUserMap"
        )
        query_count_updated_at: Optional[datetime] = Field(
            None, description="", alias="queryCountUpdatedAt"
        )
        database_name: Optional[str] = Field(None, description="", alias="databaseName")
        database_qualified_name: Optional[str] = Field(
            None, description="", alias="databaseQualifiedName"
        )
        schema_name: Optional[str] = Field(None, description="", alias="schemaName")
        schema_qualified_name: Optional[str] = Field(
            None, description="", alias="schemaQualifiedName"
        )
        table_name: Optional[str] = Field(None, description="", alias="tableName")
        table_qualified_name: Optional[str] = Field(
            None, description="", alias="tableQualifiedName"
        )
        view_name: Optional[str] = Field(None, description="", alias="viewName")
        view_qualified_name: Optional[str] = Field(
            None, description="", alias="viewQualifiedName"
        )
        is_profiled: Optional[bool] = Field(None, description="", alias="isProfiled")
        last_profiled_at: Optional[datetime] = Field(
            None, description="", alias="lastProfiledAt"
        )
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="sqlDbtModels"
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="sqlDBTSources"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        dbt_tests: Optional[list[DbtTest]] = Field(
            None, description="", alias="dbtTests"
        )  # relationship

    attributes: "SQL.Attributes" = Field(
        default_factory=lambda: SQL.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Query(SQL):
    """Description"""

    type_name: str = Field("Query", allow_mutation=False)

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
    TBC
    """
    DEFAULT_SCHEMA_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "defaultSchemaQualifiedName",
        "defaultSchemaQualifiedName",
        "defaultSchemaQualifiedName.text",
    )
    """
    TBC
    """
    DEFAULT_DATABASE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "defaultDatabaseQualifiedName",
        "defaultDatabaseQualifiedName",
        "defaultDatabaseQualifiedName.text",
    )
    """
    TBC
    """
    VARIABLES_SCHEMA_BASE64: ClassVar[KeywordField] = KeywordField(
        "variablesSchemaBase64", "variablesSchemaBase64"
    )
    """
    TBC
    """
    IS_PRIVATE: ClassVar[BooleanField] = BooleanField("isPrivate", "isPrivate")
    """
    TBC
    """
    IS_SQL_SNIPPET: ClassVar[BooleanField] = BooleanField(
        "isSqlSnippet", "isSqlSnippet"
    )
    """
    TBC
    """
    PARENT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "parentQualifiedName", "parentQualifiedName", "parentQualifiedName.text"
    )
    """
    TBC
    """
    COLLECTION_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "collectionQualifiedName",
        "collectionQualifiedName",
        "collectionQualifiedName.text",
    )
    """
    TBC
    """
    IS_VISUAL_QUERY: ClassVar[BooleanField] = BooleanField(
        "isVisualQuery", "isVisualQuery"
    )
    """
    TBC
    """
    VISUAL_BUILDER_SCHEMA_BASE64: ClassVar[KeywordField] = KeywordField(
        "visualBuilderSchemaBase64", "visualBuilderSchemaBase64"
    )
    """
    TBC
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
        raw_query: Optional[str] = Field(None, description="", alias="rawQuery")
        default_schema_qualified_name: Optional[str] = Field(
            None, description="", alias="defaultSchemaQualifiedName"
        )
        default_database_qualified_name: Optional[str] = Field(
            None, description="", alias="defaultDatabaseQualifiedName"
        )
        variables_schema_base64: Optional[str] = Field(
            None, description="", alias="variablesSchemaBase64"
        )
        is_private: Optional[bool] = Field(None, description="", alias="isPrivate")
        is_sql_snippet: Optional[bool] = Field(
            None, description="", alias="isSqlSnippet"
        )
        parent_qualified_name: Optional[str] = Field(
            None, description="", alias="parentQualifiedName"
        )
        collection_qualified_name: Optional[str] = Field(
            None, description="", alias="collectionQualifiedName"
        )
        is_visual_query: Optional[bool] = Field(
            None, description="", alias="isVisualQuery"
        )
        visual_builder_schema_base64: Optional[str] = Field(
            None, description="", alias="visualBuilderSchemaBase64"
        )
        parent: Optional[Namespace] = Field(
            None, description="", alias="parent"
        )  # relationship
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
        )  # relationship
        tables: Optional[list[Table]] = Field(
            None, description="", alias="tables"
        )  # relationship
        views: Optional[list[View]] = Field(
            None, description="", alias="views"
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
    def create(cls, *, name: str, database_qualified_name: str) -> Schema:
        validate_required_fields(
            ["name", "database_qualified_name"], [name, database_qualified_name]
        )
        attributes = Schema.Attributes.create(
            name=name, database_qualified_name=database_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field("Schema", allow_mutation=False)

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
    TBC
    """
    VIEWS_COUNT: ClassVar[NumericField] = NumericField("viewsCount", "viewsCount")
    """
    TBC
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
        table_count: Optional[int] = Field(None, description="", alias="tableCount")
        views_count: Optional[int] = Field(None, description="", alias="viewsCount")
        snowflake_tags: Optional[list[SnowflakeTag]] = Field(
            None, description="", alias="snowflakeTags"
        )  # relationship
        functions: Optional[list[Function]] = Field(
            None, description="", alias="functions"
        )  # relationship
        tables: Optional[list[Table]] = Field(
            None, description="", alias="tables"
        )  # relationship
        database: Optional[Database] = Field(
            None, description="", alias="database"
        )  # relationship
        procedures: Optional[list[Procedure]] = Field(
            None, description="", alias="procedures"
        )  # relationship
        views: Optional[list[View]] = Field(
            None, description="", alias="views"
        )  # relationship
        materialised_views: Optional[list[MaterialisedView]] = Field(
            None, description="", alias="materialisedViews"
        )  # relationship
        snowflake_dynamic_tables: Optional[list[SnowflakeDynamicTable]] = Field(
            None, description="", alias="snowflakeDynamicTables"
        )  # relationship
        snowflake_pipes: Optional[list[SnowflakePipe]] = Field(
            None, description="", alias="snowflakePipes"
        )  # relationship
        snowflake_streams: Optional[list[SnowflakeStream]] = Field(
            None, description="", alias="snowflakeStreams"
        )  # relationship

        @classmethod
        # @validate_arguments()
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

    type_name: str = Field("SnowflakePipe", allow_mutation=False)

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
    TBC
    """
    SNOWFLAKE_PIPE_IS_AUTO_INGEST_ENABLED: ClassVar[BooleanField] = BooleanField(
        "snowflakePipeIsAutoIngestEnabled", "snowflakePipeIsAutoIngestEnabled"
    )
    """
    TBC
    """
    SNOWFLAKE_PIPE_NOTIFICATION_CHANNEL_NAME: ClassVar[
        KeywordTextField
    ] = KeywordTextField(
        "snowflakePipeNotificationChannelName",
        "snowflakePipeNotificationChannelName",
        "snowflakePipeNotificationChannelName.text",
    )
    """
    TBC
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
        definition: Optional[str] = Field(None, description="", alias="definition")
        snowflake_pipe_is_auto_ingest_enabled: Optional[bool] = Field(
            None, description="", alias="snowflakePipeIsAutoIngestEnabled"
        )
        snowflake_pipe_notification_channel_name: Optional[str] = Field(
            None, description="", alias="snowflakePipeNotificationChannelName"
        )
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
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
    def create(cls, *, name: str, schema_qualified_name: str) -> View:
        validate_required_fields(
            ["name", "schema_qualified_name"], [name, schema_qualified_name]
        )
        attributes = View.Attributes.create(
            name=name, schema_qualified_name=schema_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field("View", allow_mutation=False)

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
    TBC
    """
    ROW_COUNT: ClassVar[NumericField] = NumericField("rowCount", "rowCount")
    """
    TBC
    """
    SIZE_BYTES: ClassVar[NumericField] = NumericField("sizeBytes", "sizeBytes")
    """
    TBC
    """
    IS_QUERY_PREVIEW: ClassVar[BooleanField] = BooleanField(
        "isQueryPreview", "isQueryPreview"
    )
    """
    TBC
    """
    QUERY_PREVIEW_CONFIG: ClassVar[KeywordField] = KeywordField(
        "queryPreviewConfig", "queryPreviewConfig"
    )
    """
    TBC
    """
    ALIAS: ClassVar[KeywordField] = KeywordField("alias", "alias")
    """
    TBC
    """
    IS_TEMPORARY: ClassVar[BooleanField] = BooleanField("isTemporary", "isTemporary")
    """
    TBC
    """
    DEFINITION: ClassVar[KeywordField] = KeywordField("definition", "definition")
    """
    TBC
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
        column_count: Optional[int] = Field(None, description="", alias="columnCount")
        row_count: Optional[int] = Field(None, description="", alias="rowCount")
        size_bytes: Optional[int] = Field(None, description="", alias="sizeBytes")
        is_query_preview: Optional[bool] = Field(
            None, description="", alias="isQueryPreview"
        )
        query_preview_config: Optional[dict[str, str]] = Field(
            None, description="", alias="queryPreviewConfig"
        )
        alias: Optional[str] = Field(None, description="", alias="alias")
        is_temporary: Optional[bool] = Field(None, description="", alias="isTemporary")
        definition: Optional[str] = Field(None, description="", alias="definition")
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
        )  # relationship
        queries: Optional[list[Query]] = Field(
            None, description="", alias="queries"
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
        )  # relationship

        @classmethod
        # @validate_arguments()
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
    def create(cls, *, name: str, schema_qualified_name: str) -> MaterialisedView:
        validate_required_fields(
            ["name", "schema_qualified_name"], [name, schema_qualified_name]
        )
        attributes = MaterialisedView.Attributes.create(
            name=name, schema_qualified_name=schema_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field("MaterialisedView", allow_mutation=False)

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
    TBC
    """
    REFRESH_METHOD: ClassVar[KeywordField] = KeywordField(
        "refreshMethod", "refreshMethod"
    )
    """
    TBC
    """
    STALENESS: ClassVar[KeywordField] = KeywordField("staleness", "staleness")
    """
    TBC
    """
    STALE_SINCE_DATE: ClassVar[NumericField] = NumericField(
        "staleSinceDate", "staleSinceDate"
    )
    """
    TBC
    """
    COLUMN_COUNT: ClassVar[NumericField] = NumericField("columnCount", "columnCount")
    """
    TBC
    """
    ROW_COUNT: ClassVar[NumericField] = NumericField("rowCount", "rowCount")
    """
    TBC
    """
    SIZE_BYTES: ClassVar[NumericField] = NumericField("sizeBytes", "sizeBytes")
    """
    TBC
    """
    IS_QUERY_PREVIEW: ClassVar[BooleanField] = BooleanField(
        "isQueryPreview", "isQueryPreview"
    )
    """
    TBC
    """
    QUERY_PREVIEW_CONFIG: ClassVar[KeywordField] = KeywordField(
        "queryPreviewConfig", "queryPreviewConfig"
    )
    """
    TBC
    """
    ALIAS: ClassVar[KeywordField] = KeywordField("alias", "alias")
    """
    TBC
    """
    IS_TEMPORARY: ClassVar[BooleanField] = BooleanField("isTemporary", "isTemporary")
    """
    TBC
    """
    DEFINITION: ClassVar[KeywordField] = KeywordField("definition", "definition")
    """
    TBC
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
        refresh_mode: Optional[str] = Field(None, description="", alias="refreshMode")
        refresh_method: Optional[str] = Field(
            None, description="", alias="refreshMethod"
        )
        staleness: Optional[str] = Field(None, description="", alias="staleness")
        stale_since_date: Optional[datetime] = Field(
            None, description="", alias="staleSinceDate"
        )
        column_count: Optional[int] = Field(None, description="", alias="columnCount")
        row_count: Optional[int] = Field(None, description="", alias="rowCount")
        size_bytes: Optional[int] = Field(None, description="", alias="sizeBytes")
        is_query_preview: Optional[bool] = Field(
            None, description="", alias="isQueryPreview"
        )
        query_preview_config: Optional[dict[str, str]] = Field(
            None, description="", alias="queryPreviewConfig"
        )
        alias: Optional[str] = Field(None, description="", alias="alias")
        is_temporary: Optional[bool] = Field(None, description="", alias="isTemporary")
        definition: Optional[str] = Field(None, description="", alias="definition")
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
        )  # relationship

        @classmethod
        # @validate_arguments()
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

    type_name: str = Field("Function", allow_mutation=False)

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
    The programming language in which the function is written.
    """
    FUNCTION_TYPE: ClassVar[KeywordField] = KeywordField("functionType", "functionType")
    """
    The type of function.
    """
    FUNCTION_IS_EXTERNAL: ClassVar[BooleanField] = BooleanField(
        "functionIsExternal", "functionIsExternal"
    )
    """
    Determines whether the functions is stored or executed externally.
    """
    FUNCTION_IS_SECURE: ClassVar[BooleanField] = BooleanField(
        "functionIsSecure", "functionIsSecure"
    )
    """
    Determines whether sensitive information of the function is omitted for unauthorized users.
    """
    FUNCTION_IS_MEMOIZABLE: ClassVar[BooleanField] = BooleanField(
        "functionIsMemoizable", "functionIsMemoizable"
    )
    """
    Determines whether the function must re-compute or not if there are no underlying changes in the values.
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
        function_definition: Optional[str] = Field(
            None, description="", alias="functionDefinition"
        )
        function_return_type: Optional[str] = Field(
            None, description="", alias="functionReturnType"
        )
        function_arguments: Optional[set[str]] = Field(
            None, description="", alias="functionArguments"
        )
        function_language: Optional[str] = Field(
            None, description="", alias="functionLanguage"
        )
        function_type: Optional[str] = Field(None, description="", alias="functionType")
        function_is_external: Optional[bool] = Field(
            None, description="", alias="functionIsExternal"
        )
        function_is_secure: Optional[bool] = Field(
            None, description="", alias="functionIsSecure"
        )
        function_is_memoizable: Optional[bool] = Field(
            None, description="", alias="functionIsMemoizable"
        )
        function_schema: Optional[Schema] = Field(
            None, description="", alias="functionSchema"
        )  # relationship

    attributes: "Function.Attributes" = Field(
        default_factory=lambda: Function.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TablePartition(SQL):
    """Description"""

    type_name: str = Field("TablePartition", allow_mutation=False)

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
    TBC
    """
    COLUMN_COUNT: ClassVar[NumericField] = NumericField("columnCount", "columnCount")
    """
    TBC
    """
    ROW_COUNT: ClassVar[NumericField] = NumericField("rowCount", "rowCount")
    """
    TBC
    """
    SIZE_BYTES: ClassVar[NumericField] = NumericField("sizeBytes", "sizeBytes")
    """
    TBC
    """
    ALIAS: ClassVar[KeywordField] = KeywordField("alias", "alias")
    """
    TBC
    """
    IS_TEMPORARY: ClassVar[BooleanField] = BooleanField("isTemporary", "isTemporary")
    """
    TBC
    """
    IS_QUERY_PREVIEW: ClassVar[BooleanField] = BooleanField(
        "isQueryPreview", "isQueryPreview"
    )
    """
    TBC
    """
    QUERY_PREVIEW_CONFIG: ClassVar[KeywordField] = KeywordField(
        "queryPreviewConfig", "queryPreviewConfig"
    )
    """
    TBC
    """
    EXTERNAL_LOCATION: ClassVar[KeywordField] = KeywordField(
        "externalLocation", "externalLocation"
    )
    """
    TBC
    """
    EXTERNAL_LOCATION_REGION: ClassVar[KeywordField] = KeywordField(
        "externalLocationRegion", "externalLocationRegion"
    )
    """
    TBC
    """
    EXTERNAL_LOCATION_FORMAT: ClassVar[KeywordField] = KeywordField(
        "externalLocationFormat", "externalLocationFormat"
    )
    """
    TBC
    """
    IS_PARTITIONED: ClassVar[BooleanField] = BooleanField(
        "isPartitioned", "isPartitioned"
    )
    """
    TBC
    """
    PARTITION_STRATEGY: ClassVar[KeywordField] = KeywordField(
        "partitionStrategy", "partitionStrategy"
    )
    """
    TBC
    """
    PARTITION_COUNT: ClassVar[NumericField] = NumericField(
        "partitionCount", "partitionCount"
    )
    """
    TBC
    """
    PARTITION_LIST: ClassVar[KeywordField] = KeywordField(
        "partitionList", "partitionList"
    )
    """
    TBC
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
        constraint: Optional[str] = Field(None, description="", alias="constraint")
        column_count: Optional[int] = Field(None, description="", alias="columnCount")
        row_count: Optional[int] = Field(None, description="", alias="rowCount")
        size_bytes: Optional[int] = Field(None, description="", alias="sizeBytes")
        alias: Optional[str] = Field(None, description="", alias="alias")
        is_temporary: Optional[bool] = Field(None, description="", alias="isTemporary")
        is_query_preview: Optional[bool] = Field(
            None, description="", alias="isQueryPreview"
        )
        query_preview_config: Optional[dict[str, str]] = Field(
            None, description="", alias="queryPreviewConfig"
        )
        external_location: Optional[str] = Field(
            None, description="", alias="externalLocation"
        )
        external_location_region: Optional[str] = Field(
            None, description="", alias="externalLocationRegion"
        )
        external_location_format: Optional[str] = Field(
            None, description="", alias="externalLocationFormat"
        )
        is_partitioned: Optional[bool] = Field(
            None, description="", alias="isPartitioned"
        )
        partition_strategy: Optional[str] = Field(
            None, description="", alias="partitionStrategy"
        )
        partition_count: Optional[int] = Field(
            None, description="", alias="partitionCount"
        )
        partition_list: Optional[str] = Field(
            None, description="", alias="partitionList"
        )
        child_table_partitions: Optional[list[TablePartition]] = Field(
            None, description="", alias="childTablePartitions"
        )  # relationship
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
        )  # relationship
        parent_table_partition: Optional[TablePartition] = Field(
            None, description="", alias="parentTablePartition"
        )  # relationship
        parent_table: Optional[Table] = Field(
            None, description="", alias="parentTable"
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

    type_name: str = Field("Column", allow_mutation=False)

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
    TBC
    """
    SUB_DATA_TYPE: ClassVar[KeywordField] = KeywordField("subDataType", "subDataType")
    """
    TBC
    """
    RAW_DATA_TYPE_DEFINITION: ClassVar[KeywordField] = KeywordField(
        "rawDataTypeDefinition", "rawDataTypeDefinition"
    )
    """
    TBC
    """
    ORDER: ClassVar[NumericField] = NumericField("order", "order")
    """
    TBC
    """
    NESTED_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "nestedColumnCount", "nestedColumnCount"
    )
    """
    TBC
    """
    IS_PARTITION: ClassVar[BooleanField] = BooleanField("isPartition", "isPartition")
    """
    TBC
    """
    PARTITION_ORDER: ClassVar[NumericField] = NumericField(
        "partitionOrder", "partitionOrder"
    )
    """
    TBC
    """
    IS_CLUSTERED: ClassVar[BooleanField] = BooleanField("isClustered", "isClustered")
    """
    TBC
    """
    IS_PRIMARY: ClassVar[BooleanField] = BooleanField("isPrimary", "isPrimary")
    """
    TBC
    """
    IS_FOREIGN: ClassVar[BooleanField] = BooleanField("isForeign", "isForeign")
    """
    TBC
    """
    IS_INDEXED: ClassVar[BooleanField] = BooleanField("isIndexed", "isIndexed")
    """
    TBC
    """
    IS_SORT: ClassVar[BooleanField] = BooleanField("isSort", "isSort")
    """
    TBC
    """
    IS_DIST: ClassVar[BooleanField] = BooleanField("isDist", "isDist")
    """
    TBC
    """
    IS_PINNED: ClassVar[BooleanField] = BooleanField("isPinned", "isPinned")
    """
    TBC
    """
    PINNED_BY: ClassVar[KeywordField] = KeywordField("pinnedBy", "pinnedBy")
    """
    TBC
    """
    PINNED_AT: ClassVar[NumericField] = NumericField("pinnedAt", "pinnedAt")
    """
    TBC
    """
    PRECISION: ClassVar[NumericField] = NumericField("precision", "precision")
    """
    Total number of digits allowed
    """
    DEFAULT_VALUE: ClassVar[KeywordField] = KeywordField("defaultValue", "defaultValue")
    """
    TBC
    """
    IS_NULLABLE: ClassVar[BooleanField] = BooleanField("isNullable", "isNullable")
    """
    TBC
    """
    NUMERIC_SCALE: ClassVar[NumericField] = NumericField("numericScale", "numericScale")
    """
    TBC
    """
    MAX_LENGTH: ClassVar[NumericField] = NumericField("maxLength", "maxLength")
    """
    TBC
    """
    VALIDATIONS: ClassVar[KeywordField] = KeywordField("validations", "validations")
    """
    TBC
    """
    PARENT_COLUMN_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "parentColumnQualifiedName",
        "parentColumnQualifiedName",
        "parentColumnQualifiedName.text",
    )
    """
    TBC
    """
    PARENT_COLUMN_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "parentColumnName", "parentColumnName.keyword", "parentColumnName"
    )
    """
    TBC
    """
    COLUMN_DISTINCT_VALUES_COUNT: ClassVar[NumericField] = NumericField(
        "columnDistinctValuesCount", "columnDistinctValuesCount"
    )
    """
    TBC
    """
    COLUMN_DISTINCT_VALUES_COUNT_LONG: ClassVar[NumericField] = NumericField(
        "columnDistinctValuesCountLong", "columnDistinctValuesCountLong"
    )
    """
    TBC
    """
    COLUMN_HISTOGRAM: ClassVar[KeywordField] = KeywordField(
        "columnHistogram", "columnHistogram"
    )
    """
    TBC
    """
    COLUMN_MAX: ClassVar[NumericField] = NumericField("columnMax", "columnMax")
    """
    TBC
    """
    COLUMN_MIN: ClassVar[NumericField] = NumericField("columnMin", "columnMin")
    """
    TBC
    """
    COLUMN_MEAN: ClassVar[NumericField] = NumericField("columnMean", "columnMean")
    """
    TBC
    """
    COLUMN_SUM: ClassVar[NumericField] = NumericField("columnSum", "columnSum")
    """
    TBC
    """
    COLUMN_MEDIAN: ClassVar[NumericField] = NumericField("columnMedian", "columnMedian")
    """
    TBC
    """
    COLUMN_STANDARD_DEVIATION: ClassVar[NumericField] = NumericField(
        "columnStandardDeviation", "columnStandardDeviation"
    )
    """
    TBC
    """
    COLUMN_UNIQUE_VALUES_COUNT: ClassVar[NumericField] = NumericField(
        "columnUniqueValuesCount", "columnUniqueValuesCount"
    )
    """
    TBC
    """
    COLUMN_UNIQUE_VALUES_COUNT_LONG: ClassVar[NumericField] = NumericField(
        "columnUniqueValuesCountLong", "columnUniqueValuesCountLong"
    )
    """
    TBC
    """
    COLUMN_AVERAGE: ClassVar[NumericField] = NumericField(
        "columnAverage", "columnAverage"
    )
    """
    TBC
    """
    COLUMN_AVERAGE_LENGTH: ClassVar[NumericField] = NumericField(
        "columnAverageLength", "columnAverageLength"
    )
    """
    TBC
    """
    COLUMN_DUPLICATE_VALUES_COUNT: ClassVar[NumericField] = NumericField(
        "columnDuplicateValuesCount", "columnDuplicateValuesCount"
    )
    """
    TBC
    """
    COLUMN_DUPLICATE_VALUES_COUNT_LONG: ClassVar[NumericField] = NumericField(
        "columnDuplicateValuesCountLong", "columnDuplicateValuesCountLong"
    )
    """
    TBC
    """
    COLUMN_MAXIMUM_STRING_LENGTH: ClassVar[NumericField] = NumericField(
        "columnMaximumStringLength", "columnMaximumStringLength"
    )
    """
    TBC
    """
    COLUMN_MAXS: ClassVar[KeywordField] = KeywordField("columnMaxs", "columnMaxs")
    """
    TBC
    """
    COLUMN_MINIMUM_STRING_LENGTH: ClassVar[NumericField] = NumericField(
        "columnMinimumStringLength", "columnMinimumStringLength"
    )
    """
    TBC
    """
    COLUMN_MINS: ClassVar[KeywordField] = KeywordField("columnMins", "columnMins")
    """
    TBC
    """
    COLUMN_MISSING_VALUES_COUNT: ClassVar[NumericField] = NumericField(
        "columnMissingValuesCount", "columnMissingValuesCount"
    )
    """
    TBC
    """
    COLUMN_MISSING_VALUES_COUNT_LONG: ClassVar[NumericField] = NumericField(
        "columnMissingValuesCountLong", "columnMissingValuesCountLong"
    )
    """
    TBC
    """
    COLUMN_MISSING_VALUES_PERCENTAGE: ClassVar[NumericField] = NumericField(
        "columnMissingValuesPercentage", "columnMissingValuesPercentage"
    )
    """
    TBC
    """
    COLUMN_UNIQUENESS_PERCENTAGE: ClassVar[NumericField] = NumericField(
        "columnUniquenessPercentage", "columnUniquenessPercentage"
    )
    """
    TBC
    """
    COLUMN_VARIANCE: ClassVar[NumericField] = NumericField(
        "columnVariance", "columnVariance"
    )
    """
    TBC
    """
    COLUMN_TOP_VALUES: ClassVar[KeywordField] = KeywordField(
        "columnTopValues", "columnTopValues"
    )
    """
    TBC
    """
    COLUMN_DEPTH_LEVEL: ClassVar[NumericField] = NumericField(
        "columnDepthLevel", "columnDepthLevel"
    )
    """
    Level of nesting, used for STRUCT/NESTED columns
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
        data_type: Optional[str] = Field(None, description="", alias="dataType")
        sub_data_type: Optional[str] = Field(None, description="", alias="subDataType")
        raw_data_type_definition: Optional[str] = Field(
            None, description="", alias="rawDataTypeDefinition"
        )
        order: Optional[int] = Field(None, description="", alias="order")
        nested_column_count: Optional[int] = Field(
            None, description="", alias="nestedColumnCount"
        )
        is_partition: Optional[bool] = Field(None, description="", alias="isPartition")
        partition_order: Optional[int] = Field(
            None, description="", alias="partitionOrder"
        )
        is_clustered: Optional[bool] = Field(None, description="", alias="isClustered")
        is_primary: Optional[bool] = Field(None, description="", alias="isPrimary")
        is_foreign: Optional[bool] = Field(None, description="", alias="isForeign")
        is_indexed: Optional[bool] = Field(None, description="", alias="isIndexed")
        is_sort: Optional[bool] = Field(None, description="", alias="isSort")
        is_dist: Optional[bool] = Field(None, description="", alias="isDist")
        is_pinned: Optional[bool] = Field(None, description="", alias="isPinned")
        pinned_by: Optional[str] = Field(None, description="", alias="pinnedBy")
        pinned_at: Optional[datetime] = Field(None, description="", alias="pinnedAt")
        precision: Optional[int] = Field(None, description="", alias="precision")
        default_value: Optional[str] = Field(None, description="", alias="defaultValue")
        is_nullable: Optional[bool] = Field(None, description="", alias="isNullable")
        numeric_scale: Optional[float] = Field(
            None, description="", alias="numericScale"
        )
        max_length: Optional[int] = Field(None, description="", alias="maxLength")
        validations: Optional[dict[str, str]] = Field(
            None, description="", alias="validations"
        )
        parent_column_qualified_name: Optional[str] = Field(
            None, description="", alias="parentColumnQualifiedName"
        )
        parent_column_name: Optional[str] = Field(
            None, description="", alias="parentColumnName"
        )
        column_distinct_values_count: Optional[int] = Field(
            None, description="", alias="columnDistinctValuesCount"
        )
        column_distinct_values_count_long: Optional[int] = Field(
            None, description="", alias="columnDistinctValuesCountLong"
        )
        column_histogram: Optional[Histogram] = Field(
            None, description="", alias="columnHistogram"
        )
        column_max: Optional[float] = Field(None, description="", alias="columnMax")
        column_min: Optional[float] = Field(None, description="", alias="columnMin")
        column_mean: Optional[float] = Field(None, description="", alias="columnMean")
        column_sum: Optional[float] = Field(None, description="", alias="columnSum")
        column_median: Optional[float] = Field(
            None, description="", alias="columnMedian"
        )
        column_standard_deviation: Optional[float] = Field(
            None, description="", alias="columnStandardDeviation"
        )
        column_unique_values_count: Optional[int] = Field(
            None, description="", alias="columnUniqueValuesCount"
        )
        column_unique_values_count_long: Optional[int] = Field(
            None, description="", alias="columnUniqueValuesCountLong"
        )
        column_average: Optional[float] = Field(
            None, description="", alias="columnAverage"
        )
        column_average_length: Optional[float] = Field(
            None, description="", alias="columnAverageLength"
        )
        column_duplicate_values_count: Optional[int] = Field(
            None, description="", alias="columnDuplicateValuesCount"
        )
        column_duplicate_values_count_long: Optional[int] = Field(
            None, description="", alias="columnDuplicateValuesCountLong"
        )
        column_maximum_string_length: Optional[int] = Field(
            None, description="", alias="columnMaximumStringLength"
        )
        column_maxs: Optional[set[str]] = Field(
            None, description="", alias="columnMaxs"
        )
        column_minimum_string_length: Optional[int] = Field(
            None, description="", alias="columnMinimumStringLength"
        )
        column_mins: Optional[set[str]] = Field(
            None, description="", alias="columnMins"
        )
        column_missing_values_count: Optional[int] = Field(
            None, description="", alias="columnMissingValuesCount"
        )
        column_missing_values_count_long: Optional[int] = Field(
            None, description="", alias="columnMissingValuesCountLong"
        )
        column_missing_values_percentage: Optional[float] = Field(
            None, description="", alias="columnMissingValuesPercentage"
        )
        column_uniqueness_percentage: Optional[float] = Field(
            None, description="", alias="columnUniquenessPercentage"
        )
        column_variance: Optional[float] = Field(
            None, description="", alias="columnVariance"
        )
        column_top_values: Optional[list[ColumnValueFrequencyMap]] = Field(
            None, description="", alias="columnTopValues"
        )
        column_depth_level: Optional[int] = Field(
            None, description="", alias="columnDepthLevel"
        )
        snowflake_dynamic_table: Optional[SnowflakeDynamicTable] = Field(
            None, description="", alias="snowflakeDynamicTable"
        )  # relationship
        view: Optional[View] = Field(None, description="", alias="view")  # relationship
        nested_columns: Optional[list[Column]] = Field(
            None, description="", alias="nestedColumns"
        )  # relationship
        data_quality_metric_dimensions: Optional[list[Metric]] = Field(
            None, description="", alias="dataQualityMetricDimensions"
        )  # relationship
        dbt_model_columns: Optional[list[DbtModelColumn]] = Field(
            None, description="", alias="dbtModelColumns"
        )  # relationship
        table: Optional[Table] = Field(
            None, description="", alias="table"
        )  # relationship
        column_dbt_model_columns: Optional[list[DbtModelColumn]] = Field(
            None, description="", alias="columnDbtModelColumns"
        )  # relationship
        materialised_view: Optional[MaterialisedView] = Field(
            None, description="", alias="materialisedView"
        )  # relationship
        parent_column: Optional[Column] = Field(
            None, description="", alias="parentColumn"
        )  # relationship
        queries: Optional[list[Query]] = Field(
            None, description="", alias="queries"
        )  # relationship
        metric_timestamps: Optional[list[Metric]] = Field(
            None, description="", alias="metricTimestamps"
        )  # relationship
        foreign_key_to: Optional[list[Column]] = Field(
            None, description="", alias="foreignKeyTo"
        )  # relationship
        foreign_key_from: Optional[Column] = Field(
            None, description="", alias="foreignKeyFrom"
        )  # relationship
        dbt_metrics: Optional[list[DbtMetric]] = Field(
            None, description="", alias="dbtMetrics"
        )  # relationship
        table_partition: Optional[TablePartition] = Field(
            None, description="", alias="tablePartition"
        )  # relationship

        @classmethod
        # @validate_arguments()
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

    type_name: str = Field("SnowflakeStream", allow_mutation=False)

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
    TBC
    """
    SNOWFLAKE_STREAM_SOURCE_TYPE: ClassVar[KeywordField] = KeywordField(
        "snowflakeStreamSourceType", "snowflakeStreamSourceType"
    )
    """
    TBC
    """
    SNOWFLAKE_STREAM_MODE: ClassVar[KeywordField] = KeywordField(
        "snowflakeStreamMode", "snowflakeStreamMode"
    )
    """
    TBC
    """
    SNOWFLAKE_STREAM_IS_STALE: ClassVar[BooleanField] = BooleanField(
        "snowflakeStreamIsStale", "snowflakeStreamIsStale"
    )
    """
    TBC
    """
    SNOWFLAKE_STREAM_STALE_AFTER: ClassVar[NumericField] = NumericField(
        "snowflakeStreamStaleAfter", "snowflakeStreamStaleAfter"
    )
    """
    TBC
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
        snowflake_stream_type: Optional[str] = Field(
            None, description="", alias="snowflakeStreamType"
        )
        snowflake_stream_source_type: Optional[str] = Field(
            None, description="", alias="snowflakeStreamSourceType"
        )
        snowflake_stream_mode: Optional[str] = Field(
            None, description="", alias="snowflakeStreamMode"
        )
        snowflake_stream_is_stale: Optional[bool] = Field(
            None, description="", alias="snowflakeStreamIsStale"
        )
        snowflake_stream_stale_after: Optional[datetime] = Field(
            None, description="", alias="snowflakeStreamStaleAfter"
        )
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
        )  # relationship

    attributes: "SnowflakeStream.Attributes" = Field(
        default_factory=lambda: SnowflakeStream.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Database(SQL):
    """Description"""

    @classmethod
    # @validate_arguments()
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

    type_name: str = Field("Database", allow_mutation=False)

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
    TBC
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
        schema_count: Optional[int] = Field(None, description="", alias="schemaCount")
        schemas: Optional[list[Schema]] = Field(
            None, description="", alias="schemas"
        )  # relationship

        @classmethod
        # @validate_arguments()
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


class Procedure(SQL):
    """Description"""

    type_name: str = Field("Procedure", allow_mutation=False)

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
    TBC
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
        definition: Optional[str] = Field(None, description="", alias="definition")
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
        )  # relationship

    attributes: "Procedure.Attributes" = Field(
        default_factory=lambda: Procedure.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SnowflakeTag(Tag):
    """Description"""

    type_name: str = Field("SnowflakeTag", allow_mutation=False)

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
    Unique source tag identifier
    """
    TAG_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "tagAttributes", "tagAttributes"
    )
    """
    Source tag attributes
    """
    TAG_ALLOWED_VALUES: ClassVar[KeywordTextField] = KeywordTextField(
        "tagAllowedValues", "tagAllowedValues", "tagAllowedValues.text"
    )
    """
    Allowed values for the tag at source. De-normalised from sourceTagAttributed for ease of querying
    """
    MAPPED_CLASSIFICATION_NAME: ClassVar[KeywordField] = KeywordField(
        "mappedClassificationName", "mappedClassificationName"
    )
    """
    Mapped atlan classification name
    """
    QUERY_COUNT: ClassVar[NumericField] = NumericField("queryCount", "queryCount")
    """
    TBC
    """
    QUERY_USER_COUNT: ClassVar[NumericField] = NumericField(
        "queryUserCount", "queryUserCount"
    )
    """
    TBC
    """
    QUERY_USER_MAP: ClassVar[KeywordField] = KeywordField(
        "queryUserMap", "queryUserMap"
    )
    """
    TBC
    """
    QUERY_COUNT_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "queryCountUpdatedAt", "queryCountUpdatedAt"
    )
    """
    TBC
    """
    DATABASE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "databaseName", "databaseName.keyword", "databaseName"
    )
    """
    TBC
    """
    DATABASE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "databaseQualifiedName", "databaseQualifiedName"
    )
    """
    TBC
    """
    SCHEMA_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "schemaName", "schemaName.keyword", "schemaName"
    )
    """
    TBC
    """
    SCHEMA_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "schemaQualifiedName", "schemaQualifiedName"
    )
    """
    TBC
    """
    TABLE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "tableName", "tableName.keyword", "tableName"
    )
    """
    TBC
    """
    TABLE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "tableQualifiedName", "tableQualifiedName"
    )
    """
    TBC
    """
    VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "viewName", "viewName.keyword", "viewName"
    )
    """
    TBC
    """
    VIEW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "viewQualifiedName", "viewQualifiedName"
    )
    """
    TBC
    """
    IS_PROFILED: ClassVar[BooleanField] = BooleanField("isProfiled", "isProfiled")
    """
    TBC
    """
    LAST_PROFILED_AT: ClassVar[NumericField] = NumericField(
        "lastProfiledAt", "lastProfiledAt"
    )
    """
    TBC
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
        tag_id: Optional[str] = Field(None, description="", alias="tagId")
        tag_attributes: Optional[list[SourceTagAttribute]] = Field(
            None, description="", alias="tagAttributes"
        )
        tag_allowed_values: Optional[set[str]] = Field(
            None, description="", alias="tagAllowedValues"
        )
        mapped_atlan_tag_name: Optional[str] = Field(
            None, description="", alias="mappedClassificationName"
        )
        query_count: Optional[int] = Field(None, description="", alias="queryCount")
        query_user_count: Optional[int] = Field(
            None, description="", alias="queryUserCount"
        )
        query_user_map: Optional[dict[str, int]] = Field(
            None, description="", alias="queryUserMap"
        )
        query_count_updated_at: Optional[datetime] = Field(
            None, description="", alias="queryCountUpdatedAt"
        )
        database_name: Optional[str] = Field(None, description="", alias="databaseName")
        database_qualified_name: Optional[str] = Field(
            None, description="", alias="databaseQualifiedName"
        )
        schema_name: Optional[str] = Field(None, description="", alias="schemaName")
        schema_qualified_name: Optional[str] = Field(
            None, description="", alias="schemaQualifiedName"
        )
        table_name: Optional[str] = Field(None, description="", alias="tableName")
        table_qualified_name: Optional[str] = Field(
            None, description="", alias="tableQualifiedName"
        )
        view_name: Optional[str] = Field(None, description="", alias="viewName")
        view_qualified_name: Optional[str] = Field(
            None, description="", alias="viewQualifiedName"
        )
        is_profiled: Optional[bool] = Field(None, description="", alias="isProfiled")
        last_profiled_at: Optional[datetime] = Field(
            None, description="", alias="lastProfiledAt"
        )
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="sqlDbtModels"
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="sqlDBTSources"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        dbt_tests: Optional[list[DbtTest]] = Field(
            None, description="", alias="dbtTests"
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
        )  # relationship

    attributes: "SnowflakeTag.Attributes" = Field(
        default_factory=lambda: SnowflakeTag.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Dbt(Catalog):
    """Description"""

    type_name: str = Field("Dbt", allow_mutation=False)

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
    TBC
    """
    DBT_META: ClassVar[KeywordField] = KeywordField("dbtMeta", "dbtMeta")
    """
    TBC
    """
    DBT_UNIQUE_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtUniqueId", "dbtUniqueId.keyword", "dbtUniqueId"
    )
    """
    TBC
    """
    DBT_ACCOUNT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtAccountName", "dbtAccountName.keyword", "dbtAccountName"
    )
    """
    TBC
    """
    DBT_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtProjectName", "dbtProjectName.keyword", "dbtProjectName"
    )
    """
    TBC
    """
    DBT_PACKAGE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtPackageName", "dbtPackageName.keyword", "dbtPackageName"
    )
    """
    TBC
    """
    DBT_JOB_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobName", "dbtJobName.keyword", "dbtJobName"
    )
    """
    TBC
    """
    DBT_JOB_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "dbtJobSchedule", "dbtJobSchedule"
    )
    """
    TBC
    """
    DBT_JOB_STATUS: ClassVar[KeywordField] = KeywordField(
        "dbtJobStatus", "dbtJobStatus"
    )
    """
    TBC
    """
    DBT_JOB_SCHEDULE_CRON_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobScheduleCronHumanized",
        "dbtJobScheduleCronHumanized.keyword",
        "dbtJobScheduleCronHumanized",
    )
    """
    TBC
    """
    DBT_JOB_LAST_RUN: ClassVar[NumericField] = NumericField(
        "dbtJobLastRun", "dbtJobLastRun"
    )
    """
    TBC
    """
    DBT_JOB_NEXT_RUN: ClassVar[NumericField] = NumericField(
        "dbtJobNextRun", "dbtJobNextRun"
    )
    """
    TBC
    """
    DBT_JOB_NEXT_RUN_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobNextRunHumanized",
        "dbtJobNextRunHumanized.keyword",
        "dbtJobNextRunHumanized",
    )
    """
    TBC
    """
    DBT_ENVIRONMENT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtEnvironmentName", "dbtEnvironmentName.keyword", "dbtEnvironmentName"
    )
    """
    TBC
    """
    DBT_ENVIRONMENT_DBT_VERSION: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtEnvironmentDbtVersion",
        "dbtEnvironmentDbtVersion.keyword",
        "dbtEnvironmentDbtVersion",
    )
    """
    TBC
    """
    DBT_TAGS: ClassVar[KeywordField] = KeywordField("dbtTags", "dbtTags")
    """
    TBC
    """
    DBT_CONNECTION_CONTEXT: ClassVar[KeywordField] = KeywordField(
        "dbtConnectionContext", "dbtConnectionContext"
    )
    """
    TBC
    """
    DBT_SEMANTIC_LAYER_PROXY_URL: ClassVar[KeywordField] = KeywordField(
        "dbtSemanticLayerProxyUrl", "dbtSemanticLayerProxyUrl"
    )
    """
    TBC
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
        dbt_alias: Optional[str] = Field(None, description="", alias="dbtAlias")
        dbt_meta: Optional[str] = Field(None, description="", alias="dbtMeta")
        dbt_unique_id: Optional[str] = Field(None, description="", alias="dbtUniqueId")
        dbt_account_name: Optional[str] = Field(
            None, description="", alias="dbtAccountName"
        )
        dbt_project_name: Optional[str] = Field(
            None, description="", alias="dbtProjectName"
        )
        dbt_package_name: Optional[str] = Field(
            None, description="", alias="dbtPackageName"
        )
        dbt_job_name: Optional[str] = Field(None, description="", alias="dbtJobName")
        dbt_job_schedule: Optional[str] = Field(
            None, description="", alias="dbtJobSchedule"
        )
        dbt_job_status: Optional[str] = Field(
            None, description="", alias="dbtJobStatus"
        )
        dbt_job_schedule_cron_humanized: Optional[str] = Field(
            None, description="", alias="dbtJobScheduleCronHumanized"
        )
        dbt_job_last_run: Optional[datetime] = Field(
            None, description="", alias="dbtJobLastRun"
        )
        dbt_job_next_run: Optional[datetime] = Field(
            None, description="", alias="dbtJobNextRun"
        )
        dbt_job_next_run_humanized: Optional[str] = Field(
            None, description="", alias="dbtJobNextRunHumanized"
        )
        dbt_environment_name: Optional[str] = Field(
            None, description="", alias="dbtEnvironmentName"
        )
        dbt_environment_dbt_version: Optional[str] = Field(
            None, description="", alias="dbtEnvironmentDbtVersion"
        )
        dbt_tags: Optional[set[str]] = Field(None, description="", alias="dbtTags")
        dbt_connection_context: Optional[str] = Field(
            None, description="", alias="dbtConnectionContext"
        )
        dbt_semantic_layer_proxy_url: Optional[str] = Field(
            None, description="", alias="dbtSemanticLayerProxyUrl"
        )

    attributes: "Dbt.Attributes" = Field(
        default_factory=lambda: Dbt.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtModelColumn(Dbt):
    """Description"""

    type_name: str = Field("DbtModelColumn", allow_mutation=False)

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
    TBC
    """
    DBT_MODEL_COLUMN_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "dbtModelColumnDataType", "dbtModelColumnDataType"
    )
    """
    TBC
    """
    DBT_MODEL_COLUMN_ORDER: ClassVar[NumericField] = NumericField(
        "dbtModelColumnOrder", "dbtModelColumnOrder"
    )
    """
    TBC
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
        dbt_model_qualified_name: Optional[str] = Field(
            None, description="", alias="dbtModelQualifiedName"
        )
        dbt_model_column_data_type: Optional[str] = Field(
            None, description="", alias="dbtModelColumnDataType"
        )
        dbt_model_column_order: Optional[int] = Field(
            None, description="", alias="dbtModelColumnOrder"
        )
        sql_column: Optional[Column] = Field(
            None, description="", alias="sqlColumn"
        )  # relationship
        dbt_model: Optional[DbtModel] = Field(
            None, description="", alias="dbtModel"
        )  # relationship
        dbt_model_column_sql_columns: Optional[list[Column]] = Field(
            None, description="", alias="dbtModelColumnSqlColumns"
        )  # relationship
        dbt_tests: Optional[list[DbtTest]] = Field(
            None, description="", alias="dbtTests"
        )  # relationship

    attributes: "DbtModelColumn.Attributes" = Field(
        default_factory=lambda: DbtModelColumn.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtTest(Dbt):
    """Description"""

    type_name: str = Field("DbtTest", allow_mutation=False)

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
    Status provides the details of the results of a test. For errors, it reads "ERROR".
    """
    DBT_TEST_STATE: ClassVar[KeywordField] = KeywordField(
        "dbtTestState", "dbtTestState"
    )
    """
    The test results. Can be one of, in order of severity, "error", "fail", "warn", "pass"
    """
    DBT_TEST_ERROR: ClassVar[KeywordField] = KeywordField(
        "dbtTestError", "dbtTestError"
    )
    """
    The error message in the case of state being "error"
    """
    DBT_TEST_RAW_SQL: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtTestRawSQL", "dbtTestRawSQL", "dbtTestRawSQL.text"
    )
    """
    The raw sql of a test
    """
    DBT_TEST_COMPILED_SQL: ClassVar[KeywordField] = KeywordField(
        "dbtTestCompiledSQL", "dbtTestCompiledSQL"
    )
    """
    The compiled sql of a test
    """
    DBT_TEST_RAW_CODE: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtTestRawCode", "dbtTestRawCode", "dbtTestRawCode.text"
    )
    """
    The raw code of a test ( tests in dbt can be defined using python )
    """
    DBT_TEST_COMPILED_CODE: ClassVar[KeywordField] = KeywordField(
        "dbtTestCompiledCode", "dbtTestCompiledCode"
    )
    """
    The compiled code of a test ( tests in dbt can be defined using python )
    """
    DBT_TEST_LANGUAGE: ClassVar[KeywordField] = KeywordField(
        "dbtTestLanguage", "dbtTestLanguage"
    )
    """
    The language in which a dbt test is written. Example: sql,python
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
        dbt_test_status: Optional[str] = Field(
            None, description="", alias="dbtTestStatus"
        )
        dbt_test_state: Optional[str] = Field(
            None, description="", alias="dbtTestState"
        )
        dbt_test_error: Optional[str] = Field(
            None, description="", alias="dbtTestError"
        )
        dbt_test_raw_s_q_l: Optional[str] = Field(
            None, description="", alias="dbtTestRawSQL"
        )
        dbt_test_compiled_s_q_l: Optional[str] = Field(
            None, description="", alias="dbtTestCompiledSQL"
        )
        dbt_test_raw_code: Optional[str] = Field(
            None, description="", alias="dbtTestRawCode"
        )
        dbt_test_compiled_code: Optional[str] = Field(
            None, description="", alias="dbtTestCompiledCode"
        )
        dbt_test_language: Optional[str] = Field(
            None, description="", alias="dbtTestLanguage"
        )
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        sql_assets: Optional[list[SQL]] = Field(
            None, description="", alias="sqlAssets"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        dbt_model_columns: Optional[list[DbtModelColumn]] = Field(
            None, description="", alias="dbtModelColumns"
        )  # relationship

    attributes: "DbtTest.Attributes" = Field(
        default_factory=lambda: DbtTest.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtModel(Dbt):
    """Description"""

    type_name: str = Field("DbtModel", allow_mutation=False)

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
    TBC
    """
    DBT_ERROR: ClassVar[KeywordField] = KeywordField("dbtError", "dbtError")
    """
    TBC
    """
    DBT_RAW_SQL: ClassVar[KeywordField] = KeywordField("dbtRawSQL", "dbtRawSQL")
    """
    TBC
    """
    DBT_COMPILED_SQL: ClassVar[KeywordField] = KeywordField(
        "dbtCompiledSQL", "dbtCompiledSQL"
    )
    """
    TBC
    """
    DBT_STATS: ClassVar[KeywordField] = KeywordField("dbtStats", "dbtStats")
    """
    TBC
    """
    DBT_MATERIALIZATION_TYPE: ClassVar[KeywordField] = KeywordField(
        "dbtMaterializationType", "dbtMaterializationType"
    )
    """
    TBC
    """
    DBT_MODEL_COMPILE_STARTED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelCompileStartedAt", "dbtModelCompileStartedAt"
    )
    """
    TBC
    """
    DBT_MODEL_COMPILE_COMPLETED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelCompileCompletedAt", "dbtModelCompileCompletedAt"
    )
    """
    TBC
    """
    DBT_MODEL_EXECUTE_STARTED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelExecuteStartedAt", "dbtModelExecuteStartedAt"
    )
    """
    TBC
    """
    DBT_MODEL_EXECUTE_COMPLETED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelExecuteCompletedAt", "dbtModelExecuteCompletedAt"
    )
    """
    TBC
    """
    DBT_MODEL_EXECUTION_TIME: ClassVar[NumericField] = NumericField(
        "dbtModelExecutionTime", "dbtModelExecutionTime"
    )
    """
    TBC
    """
    DBT_MODEL_RUN_GENERATED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelRunGeneratedAt", "dbtModelRunGeneratedAt"
    )
    """
    TBC
    """
    DBT_MODEL_RUN_ELAPSED_TIME: ClassVar[NumericField] = NumericField(
        "dbtModelRunElapsedTime", "dbtModelRunElapsedTime"
    )
    """
    TBC
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
        dbt_status: Optional[str] = Field(None, description="", alias="dbtStatus")
        dbt_error: Optional[str] = Field(None, description="", alias="dbtError")
        dbt_raw_s_q_l: Optional[str] = Field(None, description="", alias="dbtRawSQL")
        dbt_compiled_s_q_l: Optional[str] = Field(
            None, description="", alias="dbtCompiledSQL"
        )
        dbt_stats: Optional[str] = Field(None, description="", alias="dbtStats")
        dbt_materialization_type: Optional[str] = Field(
            None, description="", alias="dbtMaterializationType"
        )
        dbt_model_compile_started_at: Optional[datetime] = Field(
            None, description="", alias="dbtModelCompileStartedAt"
        )
        dbt_model_compile_completed_at: Optional[datetime] = Field(
            None, description="", alias="dbtModelCompileCompletedAt"
        )
        dbt_model_execute_started_at: Optional[datetime] = Field(
            None, description="", alias="dbtModelExecuteStartedAt"
        )
        dbt_model_execute_completed_at: Optional[datetime] = Field(
            None, description="", alias="dbtModelExecuteCompletedAt"
        )
        dbt_model_execution_time: Optional[float] = Field(
            None, description="", alias="dbtModelExecutionTime"
        )
        dbt_model_run_generated_at: Optional[datetime] = Field(
            None, description="", alias="dbtModelRunGeneratedAt"
        )
        dbt_model_run_elapsed_time: Optional[float] = Field(
            None, description="", alias="dbtModelRunElapsedTime"
        )
        dbt_metrics: Optional[list[DbtMetric]] = Field(
            None, description="", alias="dbtMetrics"
        )  # relationship
        dbt_tests: Optional[list[DbtTest]] = Field(
            None, description="", alias="dbtTests"
        )  # relationship
        dbt_model_sql_assets: Optional[list[SQL]] = Field(
            None, description="", alias="dbtModelSqlAssets"
        )  # relationship
        dbt_model_columns: Optional[list[DbtModelColumn]] = Field(
            None, description="", alias="dbtModelColumns"
        )  # relationship
        sql_asset: Optional[SQL] = Field(
            None, description="", alias="sqlAsset"
        )  # relationship

    attributes: "DbtModel.Attributes" = Field(
        default_factory=lambda: DbtModel.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtMetric(Dbt):
    """Description"""

    type_name: str = Field("DbtMetric", allow_mutation=False)

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
    TBC
    """
    DBT_ALIAS: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtAlias", "dbtAlias.keyword", "dbtAlias"
    )
    """
    TBC
    """
    DBT_META: ClassVar[KeywordField] = KeywordField("dbtMeta", "dbtMeta")
    """
    TBC
    """
    DBT_UNIQUE_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtUniqueId", "dbtUniqueId.keyword", "dbtUniqueId"
    )
    """
    TBC
    """
    DBT_ACCOUNT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtAccountName", "dbtAccountName.keyword", "dbtAccountName"
    )
    """
    TBC
    """
    DBT_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtProjectName", "dbtProjectName.keyword", "dbtProjectName"
    )
    """
    TBC
    """
    DBT_PACKAGE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtPackageName", "dbtPackageName.keyword", "dbtPackageName"
    )
    """
    TBC
    """
    DBT_JOB_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobName", "dbtJobName.keyword", "dbtJobName"
    )
    """
    TBC
    """
    DBT_JOB_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "dbtJobSchedule", "dbtJobSchedule"
    )
    """
    TBC
    """
    DBT_JOB_STATUS: ClassVar[KeywordField] = KeywordField(
        "dbtJobStatus", "dbtJobStatus"
    )
    """
    TBC
    """
    DBT_JOB_SCHEDULE_CRON_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobScheduleCronHumanized",
        "dbtJobScheduleCronHumanized.keyword",
        "dbtJobScheduleCronHumanized",
    )
    """
    TBC
    """
    DBT_JOB_LAST_RUN: ClassVar[NumericField] = NumericField(
        "dbtJobLastRun", "dbtJobLastRun"
    )
    """
    TBC
    """
    DBT_JOB_NEXT_RUN: ClassVar[NumericField] = NumericField(
        "dbtJobNextRun", "dbtJobNextRun"
    )
    """
    TBC
    """
    DBT_JOB_NEXT_RUN_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobNextRunHumanized",
        "dbtJobNextRunHumanized.keyword",
        "dbtJobNextRunHumanized",
    )
    """
    TBC
    """
    DBT_ENVIRONMENT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtEnvironmentName", "dbtEnvironmentName.keyword", "dbtEnvironmentName"
    )
    """
    TBC
    """
    DBT_ENVIRONMENT_DBT_VERSION: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtEnvironmentDbtVersion",
        "dbtEnvironmentDbtVersion.keyword",
        "dbtEnvironmentDbtVersion",
    )
    """
    TBC
    """
    DBT_TAGS: ClassVar[KeywordField] = KeywordField("dbtTags", "dbtTags")
    """
    TBC
    """
    DBT_CONNECTION_CONTEXT: ClassVar[KeywordField] = KeywordField(
        "dbtConnectionContext", "dbtConnectionContext"
    )
    """
    TBC
    """
    DBT_SEMANTIC_LAYER_PROXY_URL: ClassVar[KeywordField] = KeywordField(
        "dbtSemanticLayerProxyUrl", "dbtSemanticLayerProxyUrl"
    )
    """
    TBC
    """
    METRIC_TYPE: ClassVar[KeywordField] = KeywordField("metricType", "metricType")
    """
    TBC
    """
    METRIC_SQL: ClassVar[KeywordField] = KeywordField("metricSQL", "metricSQL")
    """
    TBC
    """
    METRIC_FILTERS: ClassVar[TextField] = TextField("metricFilters", "metricFilters")
    """
    TBC
    """
    METRIC_TIME_GRAINS: ClassVar[TextField] = TextField(
        "metricTimeGrains", "metricTimeGrains"
    )
    """
    TBC
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
            None, description="", alias="dbtMetricFilters"
        )
        dbt_alias: Optional[str] = Field(None, description="", alias="dbtAlias")
        dbt_meta: Optional[str] = Field(None, description="", alias="dbtMeta")
        dbt_unique_id: Optional[str] = Field(None, description="", alias="dbtUniqueId")
        dbt_account_name: Optional[str] = Field(
            None, description="", alias="dbtAccountName"
        )
        dbt_project_name: Optional[str] = Field(
            None, description="", alias="dbtProjectName"
        )
        dbt_package_name: Optional[str] = Field(
            None, description="", alias="dbtPackageName"
        )
        dbt_job_name: Optional[str] = Field(None, description="", alias="dbtJobName")
        dbt_job_schedule: Optional[str] = Field(
            None, description="", alias="dbtJobSchedule"
        )
        dbt_job_status: Optional[str] = Field(
            None, description="", alias="dbtJobStatus"
        )
        dbt_job_schedule_cron_humanized: Optional[str] = Field(
            None, description="", alias="dbtJobScheduleCronHumanized"
        )
        dbt_job_last_run: Optional[datetime] = Field(
            None, description="", alias="dbtJobLastRun"
        )
        dbt_job_next_run: Optional[datetime] = Field(
            None, description="", alias="dbtJobNextRun"
        )
        dbt_job_next_run_humanized: Optional[str] = Field(
            None, description="", alias="dbtJobNextRunHumanized"
        )
        dbt_environment_name: Optional[str] = Field(
            None, description="", alias="dbtEnvironmentName"
        )
        dbt_environment_dbt_version: Optional[str] = Field(
            None, description="", alias="dbtEnvironmentDbtVersion"
        )
        dbt_tags: Optional[set[str]] = Field(None, description="", alias="dbtTags")
        dbt_connection_context: Optional[str] = Field(
            None, description="", alias="dbtConnectionContext"
        )
        dbt_semantic_layer_proxy_url: Optional[str] = Field(
            None, description="", alias="dbtSemanticLayerProxyUrl"
        )
        metric_type: Optional[str] = Field(None, description="", alias="metricType")
        metric_s_q_l: Optional[str] = Field(None, description="", alias="metricSQL")
        metric_filters: Optional[str] = Field(
            None, description="", alias="metricFilters"
        )
        metric_time_grains: Optional[set[str]] = Field(
            None, description="", alias="metricTimeGrains"
        )
        metric_timestamp_column: Optional[Column] = Field(
            None, description="", alias="metricTimestampColumn"
        )  # relationship
        dbt_model: Optional[DbtModel] = Field(
            None, description="", alias="dbtModel"
        )  # relationship
        assets: Optional[list[Asset]] = Field(
            None, description="", alias="assets"
        )  # relationship
        metric_dimension_columns: Optional[list[Column]] = Field(
            None, description="", alias="metricDimensionColumns"
        )  # relationship
        dbt_metric_filter_columns: Optional[list[Column]] = Field(
            None, description="", alias="dbtMetricFilterColumns"
        )  # relationship

    attributes: "DbtMetric.Attributes" = Field(
        default_factory=lambda: DbtMetric.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtSource(Dbt):
    """Description"""

    type_name: str = Field("DbtSource", allow_mutation=False)

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
    TBC
    """
    DBT_FRESHNESS_CRITERIA: ClassVar[KeywordField] = KeywordField(
        "dbtFreshnessCriteria", "dbtFreshnessCriteria"
    )
    """
    TBC
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
        dbt_state: Optional[str] = Field(None, description="", alias="dbtState")
        dbt_freshness_criteria: Optional[str] = Field(
            None, description="", alias="dbtFreshnessCriteria"
        )
        sql_assets: Optional[list[SQL]] = Field(
            None, description="", alias="sqlAssets"
        )  # relationship
        dbt_tests: Optional[list[DbtTest]] = Field(
            None, description="", alias="dbtTests"
        )  # relationship
        sql_asset: Optional[SQL] = Field(
            None, description="", alias="sqlAsset"
        )  # relationship

    attributes: "DbtSource.Attributes" = Field(
        default_factory=lambda: DbtSource.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SchemaRegistry(Catalog):
    """Description"""

    type_name: str = Field("SchemaRegistry", allow_mutation=False)

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
    Type of language/specification used to define the schema like JSON, Protobuf etc.
    """
    SCHEMA_REGISTRY_SCHEMA_ID: ClassVar[KeywordField] = KeywordField(
        "schemaRegistrySchemaId", "schemaRegistrySchemaId"
    )
    """
    Unique identifier for schema definition set by the schema registry
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
            None, description="", alias="schemaRegistrySchemaType"
        )
        schema_registry_schema_id: Optional[str] = Field(
            None, description="", alias="schemaRegistrySchemaId"
        )

    attributes: "SchemaRegistry.Attributes" = Field(
        default_factory=lambda: SchemaRegistry.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SchemaRegistrySubject(SchemaRegistry):
    """Description"""

    type_name: str = Field("SchemaRegistrySubject", allow_mutation=False)

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
    Base name of the subject (i.e. without -key, -value prefixes)
    """
    SCHEMA_REGISTRY_SUBJECT_IS_KEY_SCHEMA: ClassVar[BooleanField] = BooleanField(
        "schemaRegistrySubjectIsKeySchema", "schemaRegistrySubjectIsKeySchema"
    )
    """
    If the subject is a schema for the keys of the messages.
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
            None, description="", alias="schemaRegistrySubjectBaseName"
        )
        schema_registry_subject_is_key_schema: Optional[bool] = Field(
            None, description="", alias="schemaRegistrySubjectIsKeySchema"
        )
        schema_registry_subject_schema_compatibility: Optional[
            SchemaRegistrySchemaCompatibility
        ] = Field(
            None, description="", alias="schemaRegistrySubjectSchemaCompatibility"
        )
        schema_registry_subject_latest_schema_version: Optional[str] = Field(
            None, description="", alias="schemaRegistrySubjectLatestSchemaVersion"
        )
        schema_registry_subject_latest_schema_definition: Optional[str] = Field(
            None, description="", alias="schemaRegistrySubjectLatestSchemaDefinition"
        )
        schema_registry_subject_governing_asset_qualified_names: Optional[
            set[str]
        ] = Field(
            None,
            description="",
            alias="schemaRegistrySubjectGoverningAssetQualifiedNames",
        )
        assets: Optional[list[Asset]] = Field(
            None, description="", alias="assets"
        )  # relationship

    attributes: "SchemaRegistrySubject.Attributes" = Field(
        default_factory=lambda: SchemaRegistrySubject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MonteCarlo(DataQuality):
    """Description"""

    type_name: str = Field("MonteCarlo", allow_mutation=False)

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
    TBC
    """
    MC_ASSET_QUALIFIED_NAMES: ClassVar[KeywordField] = KeywordField(
        "mcAssetQualifiedNames", "mcAssetQualifiedNames"
    )
    """
    TBC
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
        mc_labels: Optional[set[str]] = Field(None, description="", alias="mcLabels")
        mc_asset_qualified_names: Optional[set[str]] = Field(
            None, description="", alias="mcAssetQualifiedNames"
        )

    attributes: "MonteCarlo.Attributes" = Field(
        default_factory=lambda: MonteCarlo.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MCIncident(MonteCarlo):
    """Description"""

    type_name: str = Field("MCIncident", allow_mutation=False)

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
    TBC
    """
    MC_INCIDENT_TYPE: ClassVar[KeywordField] = KeywordField(
        "mcIncidentType", "mcIncidentType"
    )
    """
    TBC
    """
    MC_INCIDENT_SUB_TYPES: ClassVar[KeywordField] = KeywordField(
        "mcIncidentSubTypes", "mcIncidentSubTypes"
    )
    """
    TBC
    """
    MC_INCIDENT_SEVERITY: ClassVar[KeywordField] = KeywordField(
        "mcIncidentSeverity", "mcIncidentSeverity"
    )
    """
    TBC
    """
    MC_INCIDENT_STATE: ClassVar[KeywordField] = KeywordField(
        "mcIncidentState", "mcIncidentState"
    )
    """
    TBC
    """
    MC_INCIDENT_WAREHOUSE: ClassVar[KeywordField] = KeywordField(
        "mcIncidentWarehouse", "mcIncidentWarehouse"
    )
    """
    Incident warehouse name
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
        mc_incident_id: Optional[str] = Field(
            None, description="", alias="mcIncidentId"
        )
        mc_incident_type: Optional[str] = Field(
            None, description="", alias="mcIncidentType"
        )
        mc_incident_sub_types: Optional[set[str]] = Field(
            None, description="", alias="mcIncidentSubTypes"
        )
        mc_incident_severity: Optional[str] = Field(
            None, description="", alias="mcIncidentSeverity"
        )
        mc_incident_state: Optional[str] = Field(
            None, description="", alias="mcIncidentState"
        )
        mc_incident_warehouse: Optional[str] = Field(
            None, description="", alias="mcIncidentWarehouse"
        )
        mc_monitor: Optional[MCMonitor] = Field(
            None, description="", alias="mcMonitor"
        )  # relationship
        mc_incident_assets: Optional[list[Asset]] = Field(
            None, description="", alias="mcIncidentAssets"
        )  # relationship

    attributes: "MCIncident.Attributes" = Field(
        default_factory=lambda: MCIncident.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MCMonitor(MonteCarlo):
    """Description"""

    type_name: str = Field("MCMonitor", allow_mutation=False)

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
    Monitor Id
    """
    MC_MONITOR_STATUS: ClassVar[KeywordField] = KeywordField(
        "mcMonitorStatus", "mcMonitorStatus"
    )
    """
    Monitor status
    """
    MC_MONITOR_TYPE: ClassVar[KeywordField] = KeywordField(
        "mcMonitorType", "mcMonitorType"
    )
    """
    Monitor type
    """
    MC_MONITOR_WAREHOUSE: ClassVar[KeywordField] = KeywordField(
        "mcMonitorWarehouse", "mcMonitorWarehouse"
    )
    """
    Monitor warehouse name
    """
    MC_MONITOR_SCHEDULE_TYPE: ClassVar[KeywordField] = KeywordField(
        "mcMonitorScheduleType", "mcMonitorScheduleType"
    )
    """
    Monitor schedule type
    """
    MC_MONITOR_NAMESPACE: ClassVar[KeywordTextField] = KeywordTextField(
        "mcMonitorNamespace", "mcMonitorNamespace.keyword", "mcMonitorNamespace"
    )
    """
    Monitor namespace
    """
    MC_MONITOR_RULE_TYPE: ClassVar[KeywordField] = KeywordField(
        "mcMonitorRuleType", "mcMonitorRuleType"
    )
    """
    TBC
    """
    MC_MONITOR_RULE_CUSTOM_SQL: ClassVar[KeywordField] = KeywordField(
        "mcMonitorRuleCustomSql", "mcMonitorRuleCustomSql"
    )
    """
    custom sql query
    """
    MC_MONITOR_RULE_SCHEDULE_CONFIG: ClassVar[KeywordField] = KeywordField(
        "mcMonitorRuleScheduleConfig", "mcMonitorRuleScheduleConfig"
    )
    """
    TBC
    """
    MC_MONITOR_RULE_SCHEDULE_CONFIG_HUMANIZED: ClassVar[TextField] = TextField(
        "mcMonitorRuleScheduleConfigHumanized", "mcMonitorRuleScheduleConfigHumanized"
    )
    """
    TBC
    """
    MC_MONITOR_ALERT_CONDITION: ClassVar[TextField] = TextField(
        "mcMonitorAlertCondition", "mcMonitorAlertCondition"
    )
    """
    TBC
    """
    MC_MONITOR_RULE_NEXT_EXECUTION_TIME: ClassVar[NumericField] = NumericField(
        "mcMonitorRuleNextExecutionTime", "mcMonitorRuleNextExecutionTime"
    )
    """
    TBC
    """
    MC_MONITOR_RULE_PREVIOUS_EXECUTION_TIME: ClassVar[NumericField] = NumericField(
        "mcMonitorRulePreviousExecutionTime", "mcMonitorRulePreviousExecutionTime"
    )
    """
    TBC
    """
    MC_MONITOR_RULE_COMPARISONS: ClassVar[KeywordField] = KeywordField(
        "mcMonitorRuleComparisons", "mcMonitorRuleComparisons"
    )
    """
    TBC
    """
    MC_MONITOR_RULE_IS_SNOOZED: ClassVar[BooleanField] = BooleanField(
        "mcMonitorRuleIsSnoozed", "mcMonitorRuleIsSnoozed"
    )
    """
    TBC
    """
    MC_MONITOR_BREACH_RATE: ClassVar[NumericField] = NumericField(
        "mcMonitorBreachRate", "mcMonitorBreachRate"
    )
    """
    TBC
    """
    MC_MONITOR_INCIDENT_COUNT: ClassVar[NumericField] = NumericField(
        "mcMonitorIncidentCount", "mcMonitorIncidentCount"
    )
    """
    TBC
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
        mc_monitor_id: Optional[str] = Field(None, description="", alias="mcMonitorId")
        mc_monitor_status: Optional[str] = Field(
            None, description="", alias="mcMonitorStatus"
        )
        mc_monitor_type: Optional[str] = Field(
            None, description="", alias="mcMonitorType"
        )
        mc_monitor_warehouse: Optional[str] = Field(
            None, description="", alias="mcMonitorWarehouse"
        )
        mc_monitor_schedule_type: Optional[str] = Field(
            None, description="", alias="mcMonitorScheduleType"
        )
        mc_monitor_namespace: Optional[str] = Field(
            None, description="", alias="mcMonitorNamespace"
        )
        mc_monitor_rule_type: Optional[str] = Field(
            None, description="", alias="mcMonitorRuleType"
        )
        mc_monitor_rule_custom_sql: Optional[str] = Field(
            None, description="", alias="mcMonitorRuleCustomSql"
        )
        mc_monitor_rule_schedule_config: Optional[MCRuleSchedule] = Field(
            None, description="", alias="mcMonitorRuleScheduleConfig"
        )
        mc_monitor_rule_schedule_config_humanized: Optional[str] = Field(
            None, description="", alias="mcMonitorRuleScheduleConfigHumanized"
        )
        mc_monitor_alert_condition: Optional[str] = Field(
            None, description="", alias="mcMonitorAlertCondition"
        )
        mc_monitor_rule_next_execution_time: Optional[datetime] = Field(
            None, description="", alias="mcMonitorRuleNextExecutionTime"
        )
        mc_monitor_rule_previous_execution_time: Optional[datetime] = Field(
            None, description="", alias="mcMonitorRulePreviousExecutionTime"
        )
        mc_monitor_rule_comparisons: Optional[list[MCRuleComparison]] = Field(
            None, description="", alias="mcMonitorRuleComparisons"
        )
        mc_monitor_rule_is_snoozed: Optional[bool] = Field(
            None, description="", alias="mcMonitorRuleIsSnoozed"
        )
        mc_monitor_breach_rate: Optional[float] = Field(
            None, description="", alias="mcMonitorBreachRate"
        )
        mc_monitor_incident_count: Optional[int] = Field(
            None, description="", alias="mcMonitorIncidentCount"
        )
        mc_monitor_assets: Optional[list[Asset]] = Field(
            None, description="", alias="mcMonitorAssets"
        )  # relationship

    attributes: "MCMonitor.Attributes" = Field(
        default_factory=lambda: MCMonitor.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Soda(DataQuality):
    """Description"""

    type_name: str = Field("Soda", allow_mutation=False)

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

    type_name: str = Field("SodaCheck", allow_mutation=False)

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
    Check Id
    """
    SODA_CHECK_EVALUATION_STATUS: ClassVar[KeywordField] = KeywordField(
        "sodaCheckEvaluationStatus", "sodaCheckEvaluationStatus"
    )
    """
    Check status
    """
    SODA_CHECK_DEFINITION: ClassVar[KeywordField] = KeywordField(
        "sodaCheckDefinition", "sodaCheckDefinition"
    )
    """
    Check definition
    """
    SODA_CHECK_LAST_SCAN_AT: ClassVar[NumericField] = NumericField(
        "sodaCheckLastScanAt", "sodaCheckLastScanAt"
    )
    """
    TBC
    """
    SODA_CHECK_INCIDENT_COUNT: ClassVar[NumericField] = NumericField(
        "sodaCheckIncidentCount", "sodaCheckIncidentCount"
    )
    """
    TBC
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
        soda_check_id: Optional[str] = Field(None, description="", alias="sodaCheckId")
        soda_check_evaluation_status: Optional[str] = Field(
            None, description="", alias="sodaCheckEvaluationStatus"
        )
        soda_check_definition: Optional[str] = Field(
            None, description="", alias="sodaCheckDefinition"
        )
        soda_check_last_scan_at: Optional[datetime] = Field(
            None, description="", alias="sodaCheckLastScanAt"
        )
        soda_check_incident_count: Optional[int] = Field(
            None, description="", alias="sodaCheckIncidentCount"
        )
        soda_check_columns: Optional[list[Column]] = Field(
            None, description="", alias="sodaCheckColumns"
        )  # relationship
        soda_check_assets: Optional[list[Asset]] = Field(
            None, description="", alias="sodaCheckAssets"
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
    def create(cls, *, name: str, schema_qualified_name: str) -> Table:
        validate_required_fields(
            ["name", "schema_qualified_name"], [name, schema_qualified_name]
        )
        attributes = Table.Attributes.create(
            name=name, schema_qualified_name=schema_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field("Table", allow_mutation=False)

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
    TBC
    """
    ROW_COUNT: ClassVar[NumericField] = NumericField("rowCount", "rowCount")
    """
    TBC
    """
    SIZE_BYTES: ClassVar[NumericField] = NumericField("sizeBytes", "sizeBytes")
    """
    TBC
    """
    ALIAS: ClassVar[KeywordField] = KeywordField("alias", "alias")
    """
    TBC
    """
    IS_TEMPORARY: ClassVar[BooleanField] = BooleanField("isTemporary", "isTemporary")
    """
    TBC
    """
    IS_QUERY_PREVIEW: ClassVar[BooleanField] = BooleanField(
        "isQueryPreview", "isQueryPreview"
    )
    """
    TBC
    """
    QUERY_PREVIEW_CONFIG: ClassVar[KeywordField] = KeywordField(
        "queryPreviewConfig", "queryPreviewConfig"
    )
    """
    TBC
    """
    EXTERNAL_LOCATION: ClassVar[KeywordField] = KeywordField(
        "externalLocation", "externalLocation"
    )
    """
    TBC
    """
    EXTERNAL_LOCATION_REGION: ClassVar[KeywordField] = KeywordField(
        "externalLocationRegion", "externalLocationRegion"
    )
    """
    TBC
    """
    EXTERNAL_LOCATION_FORMAT: ClassVar[KeywordField] = KeywordField(
        "externalLocationFormat", "externalLocationFormat"
    )
    """
    TBC
    """
    IS_PARTITIONED: ClassVar[BooleanField] = BooleanField(
        "isPartitioned", "isPartitioned"
    )
    """
    TBC
    """
    PARTITION_STRATEGY: ClassVar[KeywordField] = KeywordField(
        "partitionStrategy", "partitionStrategy"
    )
    """
    TBC
    """
    PARTITION_COUNT: ClassVar[NumericField] = NumericField(
        "partitionCount", "partitionCount"
    )
    """
    TBC
    """
    PARTITION_LIST: ClassVar[KeywordField] = KeywordField(
        "partitionList", "partitionList"
    )
    """
    TBC
    """

    PARTITIONS: ClassVar[RelationField] = RelationField("partitions")
    """
    TBC
    """
    COLUMNS: ClassVar[RelationField] = RelationField("columns")
    """
    TBC
    """
    QUERIES: ClassVar[RelationField] = RelationField("queries")
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
        "partitions",
        "columns",
        "queries",
        "facts",
        "atlan_schema",
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
    def partitions(self) -> Optional[list[TablePartition]]:
        return None if self.attributes is None else self.attributes.partitions

    @partitions.setter
    def partitions(self, partitions: Optional[list[TablePartition]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partitions = partitions

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
    def dimensions(self) -> Optional[list[Table]]:
        return None if self.attributes is None else self.attributes.dimensions

    @dimensions.setter
    def dimensions(self, dimensions: Optional[list[Table]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dimensions = dimensions

    class Attributes(SQL.Attributes):
        column_count: Optional[int] = Field(None, description="", alias="columnCount")
        row_count: Optional[int] = Field(None, description="", alias="rowCount")
        size_bytes: Optional[int] = Field(None, description="", alias="sizeBytes")
        alias: Optional[str] = Field(None, description="", alias="alias")
        is_temporary: Optional[bool] = Field(None, description="", alias="isTemporary")
        is_query_preview: Optional[bool] = Field(
            None, description="", alias="isQueryPreview"
        )
        query_preview_config: Optional[dict[str, str]] = Field(
            None, description="", alias="queryPreviewConfig"
        )
        external_location: Optional[str] = Field(
            None, description="", alias="externalLocation"
        )
        external_location_region: Optional[str] = Field(
            None, description="", alias="externalLocationRegion"
        )
        external_location_format: Optional[str] = Field(
            None, description="", alias="externalLocationFormat"
        )
        is_partitioned: Optional[bool] = Field(
            None, description="", alias="isPartitioned"
        )
        partition_strategy: Optional[str] = Field(
            None, description="", alias="partitionStrategy"
        )
        partition_count: Optional[int] = Field(
            None, description="", alias="partitionCount"
        )
        partition_list: Optional[str] = Field(
            None, description="", alias="partitionList"
        )
        partitions: Optional[list[TablePartition]] = Field(
            None, description="", alias="partitions"
        )  # relationship
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
        )  # relationship
        queries: Optional[list[Query]] = Field(
            None, description="", alias="queries"
        )  # relationship
        facts: Optional[list[Table]] = Field(
            None, description="", alias="facts"
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
        )  # relationship
        dimensions: Optional[list[Table]] = Field(
            None, description="", alias="dimensions"
        )  # relationship

        @classmethod
        # @validate_arguments()
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

    type_name: str = Field("SnowflakeDynamicTable", allow_mutation=False)

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
    SQL statements used to define a Snowflake Dynamic Table
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
        definition: Optional[str] = Field(None, description="", alias="definition")

    attributes: "SnowflakeDynamicTable.Attributes" = Field(
        default_factory=lambda: SnowflakeDynamicTable.Attributes(),
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


Database.Attributes.update_forward_refs()


Procedure.Attributes.update_forward_refs()


SnowflakeTag.Attributes.update_forward_refs()


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
