# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

import sys
from datetime import datetime
from typing import TYPE_CHECKING, ClassVar, Dict, List, Optional, Set, Type, TypeVar
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.errors import ErrorCode
from pyatlan.model.core import Announcement
from pyatlan.model.enums import (
    AnnouncementType,
    CertificateStatus,
    SaveSemantic,
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
from pyatlan.model.structs import PopularityInsights, StarredDetails
from pyatlan.utils import init_guid, validate_required_fields

from .referenceable import Referenceable

SelfAsset = TypeVar("SelfAsset", bound="Asset")


class Asset(Referenceable):
    """Description"""

    _subtypes_: Dict[str, type] = dict()

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
    def creator(cls: Type[SelfAsset], *args, **kwargs) -> SelfAsset:
        raise NotImplementedError(
            "Creator has not been implemented for this class. "
            "Please submit an enhancement request if you need it implemented."
        )

    @classmethod
    @init_guid
    def create(cls: Type[SelfAsset], *args, **kwargs) -> SelfAsset:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(*args, **kwargs)

    @classmethod
    def updater(
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
    def create_for_modification(
        cls: type[SelfAsset], qualified_name: str = "", name: str = ""
    ) -> SelfAsset:
        warn(
            (
                "This method is deprecated, please use 'updater' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.updater(qualified_name=qualified_name, name=name)

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
    ASSET_DBT_WORKFLOW_LAST_UPDATED: ClassVar[KeywordField] = KeywordField(
        "assetDbtWorkflowLastUpdated", "assetDbtWorkflowLastUpdated"
    )
    """
    Name of the DBT workflow in Atlan that last updated the asset.
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
    ASSET_DBT_JOB_LAST_RUN_TOTAL_DURATION_HUMANIZED: ClassVar[KeywordField] = (
        KeywordField(
            "assetDbtJobLastRunTotalDurationHumanized",
            "assetDbtJobLastRunTotalDurationHumanized",
        )
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
    ASSET_DBT_JOB_LAST_RUN_QUEUED_DURATION_HUMANIZED: ClassVar[KeywordField] = (
        KeywordField(
            "assetDbtJobLastRunQueuedDurationHumanized",
            "assetDbtJobLastRunQueuedDurationHumanized",
        )
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
    ASSET_DBT_JOB_LAST_RUN_RUN_DURATION_HUMANIZED: ClassVar[KeywordField] = (
        KeywordField(
            "assetDbtJobLastRunRunDurationHumanized",
            "assetDbtJobLastRunRunDurationHumanized",
        )
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
    ASSET_DBT_JOB_LAST_RUN_STATUS_MESSAGE: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "assetDbtJobLastRunStatusMessage",
            "assetDbtJobLastRunStatusMessage.keyword",
            "assetDbtJobLastRunStatusMessage",
        )
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
    HAS_CONTRACT: ClassVar[BooleanField] = BooleanField("hasContract", "hasContract")
    """
    Whether this asset has contract (true) or not (false).
    """

    SCHEMA_REGISTRY_SUBJECTS: ClassVar[RelationField] = RelationField(
        "schemaRegistrySubjects"
    )
    """
    TBC
    """
    DATA_CONTRACT_LATEST_CERTIFIED: ClassVar[RelationField] = RelationField(
        "dataContractLatestCertified"
    )
    """
    TBC
    """
    OUTPUT_PORT_DATA_PRODUCTS: ClassVar[RelationField] = RelationField(
        "outputPortDataProducts"
    )
    """
    TBC
    """
    README: ClassVar[RelationField] = RelationField("readme")
    """
    TBC
    """
    DATA_CONTRACT_LATEST: ClassVar[RelationField] = RelationField("dataContractLatest")
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
    INPUT_PORT_DATA_PRODUCTS: ClassVar[RelationField] = RelationField(
        "inputPortDataProducts"
    )
    """
    TBC
    """
    SODA_CHECKS: ClassVar[RelationField] = RelationField("sodaChecks")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
        "asset_dbt_workflow_last_updated",
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
        "has_contract",
        "schema_registry_subjects",
        "data_contract_latest_certified",
        "output_port_data_products",
        "readme",
        "data_contract_latest",
        "assigned_terms",
        "mc_monitors",
        "files",
        "mc_incidents",
        "links",
        "metrics",
        "input_port_data_products",
        "soda_checks",
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
    def owner_users(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.owner_users

    @owner_users.setter
    def owner_users(self, owner_users: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.owner_users = owner_users

    @property
    def owner_groups(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.owner_groups

    @owner_groups.setter
    def owner_groups(self, owner_groups: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.owner_groups = owner_groups

    @property
    def admin_users(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.admin_users

    @admin_users.setter
    def admin_users(self, admin_users: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.admin_users = admin_users

    @property
    def admin_groups(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.admin_groups

    @admin_groups.setter
    def admin_groups(self, admin_groups: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.admin_groups = admin_groups

    @property
    def viewer_users(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.viewer_users

    @viewer_users.setter
    def viewer_users(self, viewer_users: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.viewer_users = viewer_users

    @property
    def viewer_groups(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.viewer_groups

    @viewer_groups.setter
    def viewer_groups(self, viewer_groups: Optional[Set[str]]):
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
    def admin_roles(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.admin_roles

    @admin_roles.setter
    def admin_roles(self, admin_roles: Optional[Set[str]]):
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
    def source_read_recent_user_list(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_recent_user_list
        )

    @source_read_recent_user_list.setter
    def source_read_recent_user_list(
        self, source_read_recent_user_list: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_recent_user_list = source_read_recent_user_list

    @property
    def source_read_recent_user_record_list(self) -> Optional[List[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_recent_user_record_list
        )

    @source_read_recent_user_record_list.setter
    def source_read_recent_user_record_list(
        self, source_read_recent_user_record_list: Optional[List[PopularityInsights]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_recent_user_record_list = (
            source_read_recent_user_record_list
        )

    @property
    def source_read_top_user_list(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_top_user_list
        )

    @source_read_top_user_list.setter
    def source_read_top_user_list(self, source_read_top_user_list: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_top_user_list = source_read_top_user_list

    @property
    def source_read_top_user_record_list(self) -> Optional[List[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_top_user_record_list
        )

    @source_read_top_user_record_list.setter
    def source_read_top_user_record_list(
        self, source_read_top_user_record_list: Optional[List[PopularityInsights]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_top_user_record_list = (
            source_read_top_user_record_list
        )

    @property
    def source_read_popular_query_record_list(
        self,
    ) -> Optional[List[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_popular_query_record_list
        )

    @source_read_popular_query_record_list.setter
    def source_read_popular_query_record_list(
        self, source_read_popular_query_record_list: Optional[List[PopularityInsights]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_popular_query_record_list = (
            source_read_popular_query_record_list
        )

    @property
    def source_read_expensive_query_record_list(
        self,
    ) -> Optional[List[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_expensive_query_record_list
        )

    @source_read_expensive_query_record_list.setter
    def source_read_expensive_query_record_list(
        self,
        source_read_expensive_query_record_list: Optional[List[PopularityInsights]],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_expensive_query_record_list = (
            source_read_expensive_query_record_list
        )

    @property
    def source_read_slow_query_record_list(self) -> Optional[List[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_read_slow_query_record_list
        )

    @source_read_slow_query_record_list.setter
    def source_read_slow_query_record_list(
        self, source_read_slow_query_record_list: Optional[List[PopularityInsights]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_slow_query_record_list = (
            source_read_slow_query_record_list
        )

    @property
    def source_query_compute_cost_list(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_query_compute_cost_list
        )

    @source_query_compute_cost_list.setter
    def source_query_compute_cost_list(
        self, source_query_compute_cost_list: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_query_compute_cost_list = source_query_compute_cost_list

    @property
    def source_query_compute_cost_record_list(
        self,
    ) -> Optional[List[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_query_compute_cost_record_list
        )

    @source_query_compute_cost_record_list.setter
    def source_query_compute_cost_record_list(
        self, source_query_compute_cost_record_list: Optional[List[PopularityInsights]]
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
    def asset_dbt_workflow_last_updated(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_dbt_workflow_last_updated
        )

    @asset_dbt_workflow_last_updated.setter
    def asset_dbt_workflow_last_updated(
        self, asset_dbt_workflow_last_updated: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_workflow_last_updated = (
            asset_dbt_workflow_last_updated
        )

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
    def asset_dbt_tags(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.asset_dbt_tags

    @asset_dbt_tags.setter
    def asset_dbt_tags(self, asset_dbt_tags: Optional[Set[str]]):
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
    def asset_tags(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.asset_tags

    @asset_tags.setter
    def asset_tags(self, asset_tags: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_tags = asset_tags

    @property
    def asset_mc_incident_names(self) -> Optional[Set[str]]:
        return (
            None if self.attributes is None else self.attributes.asset_mc_incident_names
        )

    @asset_mc_incident_names.setter
    def asset_mc_incident_names(self, asset_mc_incident_names: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_incident_names = asset_mc_incident_names

    @property
    def asset_mc_incident_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_incident_qualified_names
        )

    @asset_mc_incident_qualified_names.setter
    def asset_mc_incident_qualified_names(
        self, asset_mc_incident_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_incident_qualified_names = (
            asset_mc_incident_qualified_names
        )

    @property
    def asset_mc_monitor_names(self) -> Optional[Set[str]]:
        return (
            None if self.attributes is None else self.attributes.asset_mc_monitor_names
        )

    @asset_mc_monitor_names.setter
    def asset_mc_monitor_names(self, asset_mc_monitor_names: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_monitor_names = asset_mc_monitor_names

    @property
    def asset_mc_monitor_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_monitor_qualified_names
        )

    @asset_mc_monitor_qualified_names.setter
    def asset_mc_monitor_qualified_names(
        self, asset_mc_monitor_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_monitor_qualified_names = (
            asset_mc_monitor_qualified_names
        )

    @property
    def asset_mc_monitor_statuses(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_monitor_statuses
        )

    @asset_mc_monitor_statuses.setter
    def asset_mc_monitor_statuses(self, asset_mc_monitor_statuses: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_monitor_statuses = asset_mc_monitor_statuses

    @property
    def asset_mc_monitor_types(self) -> Optional[Set[str]]:
        return (
            None if self.attributes is None else self.attributes.asset_mc_monitor_types
        )

    @asset_mc_monitor_types.setter
    def asset_mc_monitor_types(self, asset_mc_monitor_types: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_monitor_types = asset_mc_monitor_types

    @property
    def asset_mc_monitor_schedule_types(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_monitor_schedule_types
        )

    @asset_mc_monitor_schedule_types.setter
    def asset_mc_monitor_schedule_types(
        self, asset_mc_monitor_schedule_types: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_monitor_schedule_types = (
            asset_mc_monitor_schedule_types
        )

    @property
    def asset_mc_incident_types(self) -> Optional[Set[str]]:
        return (
            None if self.attributes is None else self.attributes.asset_mc_incident_types
        )

    @asset_mc_incident_types.setter
    def asset_mc_incident_types(self, asset_mc_incident_types: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_incident_types = asset_mc_incident_types

    @property
    def asset_mc_incident_sub_types(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_incident_sub_types
        )

    @asset_mc_incident_sub_types.setter
    def asset_mc_incident_sub_types(
        self, asset_mc_incident_sub_types: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_incident_sub_types = asset_mc_incident_sub_types

    @property
    def asset_mc_incident_severities(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_incident_severities
        )

    @asset_mc_incident_severities.setter
    def asset_mc_incident_severities(
        self, asset_mc_incident_severities: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_mc_incident_severities = asset_mc_incident_severities

    @property
    def asset_mc_incident_states(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_mc_incident_states
        )

    @asset_mc_incident_states.setter
    def asset_mc_incident_states(self, asset_mc_incident_states: Optional[Set[str]]):
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
    def starred_by(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.starred_by

    @starred_by.setter
    def starred_by(self, starred_by: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.starred_by = starred_by

    @property
    def starred_details_list(self) -> Optional[List[StarredDetails]]:
        return None if self.attributes is None else self.attributes.starred_details_list

    @starred_details_list.setter
    def starred_details_list(
        self, starred_details_list: Optional[List[StarredDetails]]
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
    def has_contract(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.has_contract

    @has_contract.setter
    def has_contract(self, has_contract: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.has_contract = has_contract

    @property
    def schema_registry_subjects(self) -> Optional[List[SchemaRegistrySubject]]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subjects
        )

    @schema_registry_subjects.setter
    def schema_registry_subjects(
        self, schema_registry_subjects: Optional[List[SchemaRegistrySubject]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subjects = schema_registry_subjects

    @property
    def data_contract_latest_certified(self) -> Optional[DataContract]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_contract_latest_certified
        )

    @data_contract_latest_certified.setter
    def data_contract_latest_certified(
        self, data_contract_latest_certified: Optional[DataContract]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_contract_latest_certified = data_contract_latest_certified

    @property
    def output_port_data_products(self) -> Optional[List[DataProduct]]:
        return (
            None
            if self.attributes is None
            else self.attributes.output_port_data_products
        )

    @output_port_data_products.setter
    def output_port_data_products(
        self, output_port_data_products: Optional[List[DataProduct]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_port_data_products = output_port_data_products

    @property
    def readme(self) -> Optional[Readme]:
        return None if self.attributes is None else self.attributes.readme

    @readme.setter
    def readme(self, readme: Optional[Readme]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.readme = readme

    @property
    def data_contract_latest(self) -> Optional[DataContract]:
        return None if self.attributes is None else self.attributes.data_contract_latest

    @data_contract_latest.setter
    def data_contract_latest(self, data_contract_latest: Optional[DataContract]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_contract_latest = data_contract_latest

    @property
    def assigned_terms(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.meanings

    @assigned_terms.setter
    def assigned_terms(self, assigned_terms: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = assigned_terms

    @property
    def mc_monitors(self) -> Optional[List[MCMonitor]]:
        return None if self.attributes is None else self.attributes.mc_monitors

    @mc_monitors.setter
    def mc_monitors(self, mc_monitors: Optional[List[MCMonitor]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitors = mc_monitors

    @property
    def files(self) -> Optional[List[File]]:
        return None if self.attributes is None else self.attributes.files

    @files.setter
    def files(self, files: Optional[List[File]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.files = files

    @property
    def mc_incidents(self) -> Optional[List[MCIncident]]:
        return None if self.attributes is None else self.attributes.mc_incidents

    @mc_incidents.setter
    def mc_incidents(self, mc_incidents: Optional[List[MCIncident]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incidents = mc_incidents

    @property
    def links(self) -> Optional[List[Link]]:
        return None if self.attributes is None else self.attributes.links

    @links.setter
    def links(self, links: Optional[List[Link]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.links = links

    @property
    def metrics(self) -> Optional[List[Metric]]:
        return None if self.attributes is None else self.attributes.metrics

    @metrics.setter
    def metrics(self, metrics: Optional[List[Metric]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metrics = metrics

    @property
    def input_port_data_products(self) -> Optional[List[DataProduct]]:
        return (
            None
            if self.attributes is None
            else self.attributes.input_port_data_products
        )

    @input_port_data_products.setter
    def input_port_data_products(
        self, input_port_data_products: Optional[List[DataProduct]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_port_data_products = input_port_data_products

    @property
    def soda_checks(self) -> Optional[List[SodaCheck]]:
        return None if self.attributes is None else self.attributes.soda_checks

    @soda_checks.setter
    def soda_checks(self, soda_checks: Optional[List[SodaCheck]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.soda_checks = soda_checks

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
        owner_users: Optional[Set[str]] = Field(default=None, description="")
        owner_groups: Optional[Set[str]] = Field(default=None, description="")
        admin_users: Optional[Set[str]] = Field(default=None, description="")
        admin_groups: Optional[Set[str]] = Field(default=None, description="")
        viewer_users: Optional[Set[str]] = Field(default=None, description="")
        viewer_groups: Optional[Set[str]] = Field(default=None, description="")
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
        admin_roles: Optional[Set[str]] = Field(default=None, description="")
        source_read_count: Optional[int] = Field(default=None, description="")
        source_read_user_count: Optional[int] = Field(default=None, description="")
        source_last_read_at: Optional[datetime] = Field(default=None, description="")
        last_row_changed_at: Optional[datetime] = Field(default=None, description="")
        source_total_cost: Optional[float] = Field(default=None, description="")
        source_cost_unit: Optional[SourceCostUnitType] = Field(
            default=None, description=""
        )
        source_read_query_cost: Optional[float] = Field(default=None, description="")
        source_read_recent_user_list: Optional[Set[str]] = Field(
            default=None, description=""
        )
        source_read_recent_user_record_list: Optional[List[PopularityInsights]] = Field(
            default=None, description=""
        )
        source_read_top_user_list: Optional[Set[str]] = Field(
            default=None, description=""
        )
        source_read_top_user_record_list: Optional[List[PopularityInsights]] = Field(
            default=None, description=""
        )
        source_read_popular_query_record_list: Optional[List[PopularityInsights]] = (
            Field(default=None, description="")
        )
        source_read_expensive_query_record_list: Optional[List[PopularityInsights]] = (
            Field(default=None, description="")
        )
        source_read_slow_query_record_list: Optional[List[PopularityInsights]] = Field(
            default=None, description=""
        )
        source_query_compute_cost_list: Optional[Set[str]] = Field(
            default=None, description=""
        )
        source_query_compute_cost_record_list: Optional[List[PopularityInsights]] = (
            Field(default=None, description="")
        )
        dbt_qualified_name: Optional[str] = Field(default=None, description="")
        asset_dbt_workflow_last_updated: Optional[str] = Field(
            default=None, description=""
        )
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
        asset_dbt_tags: Optional[Set[str]] = Field(default=None, description="")
        asset_dbt_semantic_layer_proxy_url: Optional[str] = Field(
            default=None, description=""
        )
        asset_dbt_source_freshness_criteria: Optional[str] = Field(
            default=None, description=""
        )
        sample_data_url: Optional[str] = Field(default=None, description="")
        asset_tags: Optional[Set[str]] = Field(default=None, description="")
        asset_mc_incident_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        asset_mc_incident_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        asset_mc_monitor_names: Optional[Set[str]] = Field(default=None, description="")
        asset_mc_monitor_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        asset_mc_monitor_statuses: Optional[Set[str]] = Field(
            default=None, description=""
        )
        asset_mc_monitor_types: Optional[Set[str]] = Field(default=None, description="")
        asset_mc_monitor_schedule_types: Optional[Set[str]] = Field(
            default=None, description=""
        )
        asset_mc_incident_types: Optional[Set[str]] = Field(
            default=None, description=""
        )
        asset_mc_incident_sub_types: Optional[Set[str]] = Field(
            default=None, description=""
        )
        asset_mc_incident_severities: Optional[Set[str]] = Field(
            default=None, description=""
        )
        asset_mc_incident_states: Optional[Set[str]] = Field(
            default=None, description=""
        )
        asset_mc_last_sync_run_at: Optional[datetime] = Field(
            default=None, description=""
        )
        starred_by: Optional[Set[str]] = Field(default=None, description="")
        starred_details_list: Optional[List[StarredDetails]] = Field(
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
        has_contract: Optional[bool] = Field(default=None, description="")
        schema_registry_subjects: Optional[List[SchemaRegistrySubject]] = Field(
            default=None, description=""
        )  # relationship
        data_contract_latest_certified: Optional[DataContract] = Field(
            default=None, description=""
        )  # relationship
        output_port_data_products: Optional[List[DataProduct]] = Field(
            default=None, description=""
        )  # relationship
        readme: Optional[Readme] = Field(default=None, description="")  # relationship
        data_contract_latest: Optional[DataContract] = Field(
            default=None, description=""
        )  # relationship
        meanings: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        mc_monitors: Optional[List[MCMonitor]] = Field(
            default=None, description=""
        )  # relationship
        files: Optional[List[File]] = Field(
            default=None, description=""
        )  # relationship
        mc_incidents: Optional[List[MCIncident]] = Field(
            default=None, description=""
        )  # relationship
        links: Optional[List[Link]] = Field(
            default=None, description=""
        )  # relationship
        metrics: Optional[List[Metric]] = Field(
            default=None, description=""
        )  # relationship
        input_port_data_products: Optional[List[DataProduct]] = Field(
            default=None, description=""
        )  # relationship
        soda_checks: Optional[List[SodaCheck]] = Field(
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

    attributes: Asset.Attributes = Field(
        default_factory=lambda: Asset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .atlas_glossary_term import AtlasGlossaryTerm  # noqa
from .data_contract import DataContract  # noqa
from .data_product import DataProduct  # noqa
from .file import File  # noqa
from .link import Link  # noqa
from .m_c_incident import MCIncident  # noqa
from .m_c_monitor import MCMonitor  # noqa
from .metric import Metric  # noqa
from .readme import Readme  # noqa
from .schema_registry_subject import SchemaRegistrySubject  # noqa
from .soda_check import SodaCheck  # noqa
