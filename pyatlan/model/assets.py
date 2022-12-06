from __future__ import annotations
from typing import Optional, Dict, Any, List, Literal
from pydantic import Field
from datetime import date, datetime
from pyatlan.model.core import AtlanObject, Classification, Announcement
from pyatlan.model.enums import (
    CertificateStatus,
    EntityStatus,
    google_datastudio_asset_type,
    powerbi_endorsement,
    icon_type,
    AnnouncementType,
)


class Internal(AtlanObject):
    """For internal usage"""


class AtlasServer(AtlanObject):
    """For internal usage"""


class AwsTag(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        aws_tag_key: str = Field(None, description="", alias="awsTagKey")
        aws_tag_value: str = Field(None, description="", alias="awsTagValue")


class AwsCloudWatchMetric(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        aws_cloud_watch_metric_name: str = Field(
            None, description="", alias="awsCloudWatchMetricName"
        )
        aws_cloud_watch_metric_scope: str = Field(
            None, description="", alias="awsCloudWatchMetricScope"
        )


class Histogram(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        boundaries: list[float] = Field(None, description="", alias="boundaries")
        frequencies: list[float] = Field(None, description="", alias="frequencies")


class DbtMetricFilter(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        dbt_metric_filter_column_qualified_name: Optional[str] = Field(
            None, description="", alias="dbtMetricFilterColumnQualifiedName"
        )
        dbt_metric_filter_field: Optional[str] = Field(
            None, description="", alias="dbtMetricFilterField"
        )
        dbt_metric_filter_operator: Optional[str] = Field(
            None, description="", alias="dbtMetricFilterOperator"
        )
        dbt_metric_filter_value: Optional[str] = Field(
            None, description="", alias="dbtMetricFilterValue"
        )


class GoogleTag(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        google_tag_key: str = Field(None, description="", alias="googleTagKey")
        google_tag_value: str = Field(None, description="", alias="googleTagValue")


class ColumnValueFrequencyMap(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        column_value: Optional[str] = Field(None, description="", alias="columnValue")
        column_value_frequency: Optional[int] = Field(
            None, description="", alias="columnValueFrequency"
        )


class BadgeCondition(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        badge_condition_operator: Optional[str] = Field(
            None, description="", alias="badgeConditionOperator"
        )
        badge_condition_value: Optional[str] = Field(
            None, description="", alias="badgeConditionValue"
        )
        badge_condition_colorhex: Optional[str] = Field(
            None, description="", alias="badgeConditionColorhex"
        )


class GoogleLabel(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        google_label_key: str = Field(None, description="", alias="googleLabelKey")
        google_label_value: str = Field(None, description="", alias="googleLabelValue")


class PopularityInsights(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        record_user: Optional[str] = Field(None, description="", alias="recordUser")
        record_query_count: Optional[int] = Field(
            None, description="", alias="recordQueryCount"
        )
        record_last_timestamp: Optional[date] = Field(
            None, description="", alias="recordLastTimestamp"
        )


class Referenceable(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        qualified_name: str = Field(None, description="", alias="qualifiedName")
        replicated_from: Optional[list[AtlasServer]] = Field(
            None, description="", alias="replicatedFrom"
        )
        replicated_to: Optional[list[AtlasServer]] = Field(
            None, description="", alias="replicatedTo"
        )
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship

    attributes: "Referenceable.Attributes" = Field(
        None,
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
    guid: Optional[str] = Field(
        None,
        description="Unique identifier of the entity instance.\n",
        example="917ffec9-fa84-4c59-8e6c-c7b114d04be3",
    )
    is_incomplete: Optional[bool] = Field(False, description="", example=False)
    labels: Optional[List[str]] = Field(None, description="Internal use only.")
    relationship_attributes: Optional[Dict[str, Any]] = Field(
        None,
        description="Map of relationships for the entity. The specific keys of this map will vary by type, "
        "so are described in the sub-types of this schema.\n",
    )
    status: Optional[EntityStatus] = Field(
        None, description="Status of the entity", example=EntityStatus.ACTIVE
    )
    type_name: str = Field(
        None, description="Name of the type definition that defines this instance.\n"
    )
    updated_by: Optional[str] = Field(
        None,
        description="Username of the user who last updated the object.\n",
        example="jsmith",
    )
    update_time: Optional[int] = Field(
        None,
        description="Time (epoch) at which this object was last updated, in milliseconds.\n",
        example=1649172284333,
    )
    version: Optional[int] = Field(
        None, description="Version of this object.\n", example=2
    )
    classifications: Optional[list[Classification]] = Field(
        None, description="classifications"
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
        None, description="Names of terms that have been linked to this asset."
    )
    meanings: Optional[list[AtlasGlossaryTerm]] = Field(
        None, description="", alias="meanings"
    )


class Asset(Referenceable):
    """Description"""

    class Attributes(Referenceable.Attributes):
        name: str = Field(None, description="", alias="name")
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
        owner_users: Optional[list[str]] = Field(
            None, description="", alias="ownerUsers"
        )
        owner_groups: Optional[list[str]] = Field(
            None, description="", alias="ownerGroups"
        )
        admin_users: Optional[list[str]] = Field(
            None, description="", alias="adminUsers"
        )
        admin_groups: Optional[list[str]] = Field(
            None, description="", alias="adminGroups"
        )
        viewer_users: Optional[list[str]] = Field(
            None, description="", alias="viewerUsers"
        )
        viewer_groups: Optional[list[str]] = Field(
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
        admin_roles: Optional[list[str]] = Field(
            None, description="", alias="adminRoles"
        )
        source_read_count: Optional[int] = Field(
            None, description="", alias="sourceReadCount"
        )
        source_read_user_count: Optional[int] = Field(
            None, description="", alias="sourceReadUserCount"
        )
        source_last_read_at: Optional[date] = Field(
            None, description="", alias="sourceLastReadAt"
        )
        last_row_changed_at: Optional[date] = Field(
            None, description="", alias="lastRowChangedAt"
        )
        source_read_recent_user_list: Optional[list[str]] = Field(
            None, description="", alias="sourceReadRecentUserList"
        )
        source_read_recent_user_record_list: Optional[list[PopularityInsights]] = Field(
            None, description="", alias="sourceReadRecentUserRecordList"
        )
        source_read_top_user_list: Optional[list[str]] = Field(
            None, description="", alias="sourceReadTopUserList"
        )
        source_read_top_user_record_list: Optional[list[PopularityInsights]] = Field(
            None, description="", alias="sourceReadTopUserRecordList"
        )
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
        asset_dbt_job_schedule_cron_humanized: Optional[str] = Field(
            None, description="", alias="assetDbtJobScheduleCronHumanized"
        )
        asset_dbt_job_last_run: Optional[date] = Field(
            None, description="", alias="assetDbtJobLastRun"
        )
        asset_dbt_job_last_run_url: Optional[str] = Field(
            None, description="", alias="assetDbtJobLastRunUrl"
        )
        asset_dbt_job_last_run_created_at: Optional[date] = Field(
            None, description="", alias="assetDbtJobLastRunCreatedAt"
        )
        asset_dbt_job_last_run_updated_at: Optional[date] = Field(
            None, description="", alias="assetDbtJobLastRunUpdatedAt"
        )
        asset_dbt_job_last_run_dequed_at: Optional[date] = Field(
            None, description="", alias="assetDbtJobLastRunDequedAt"
        )
        asset_dbt_job_last_run_started_at: Optional[date] = Field(
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
        asset_dbt_job_next_run: Optional[date] = Field(
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
        asset_dbt_tags: Optional[list[str]] = Field(
            None, description="", alias="assetDbtTags"
        )
        asset_dbt_semantic_layer_proxy_url: Optional[str] = Field(
            None, description="", alias="assetDbtSemanticLayerProxyUrl"
        )
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship

    attributes: "Asset.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )

    def has_announcement(self) -> bool:
        if self.attributes and (
            self.attributes.announcement_title or self.attributes.announcement_type
        ):
            return True
        else:
            return False

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

    def clear_announcment(self):
        self.attributes.announcement_message = None
        self.attributes.announcement_title = None
        self.attributes.announcement_type = None


class AtlasGlossary(Asset):
    """Description"""

    type_name: Literal["AtlasGlossary"]

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
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        categories: Optional[list[AtlasGlossaryCategory]] = Field(
            None, description="", alias="categories"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship

    attributes: "AtlasGlossary.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DataSet(Asset):
    """Description"""


class ProcessExecution(Asset):
    """Description"""


class AtlasGlossaryTerm(Asset):
    """Description"""

    type_name: Literal["AtlasGlossaryTerm"]

    class Attributes(Asset.Attributes):
        short_description: Optional[str] = Field(
            None, description="", alias="shortDescription"
        )
        long_description: Optional[str] = Field(
            None, description="", alias="longDescription"
        )
        examples: Optional[list[str]] = Field(None, description="", alias="examples")
        abbreviation: Optional[str] = Field(None, description="", alias="abbreviation")
        usage: Optional[str] = Field(None, description="", alias="usage")
        additional_attributes: Optional[dict[str, str]] = Field(
            None, description="", alias="additionalAttributes"
        )
        translation_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="translationTerms"
        )  # relationship
        valid_values_for: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="validValuesFor"
        )  # relationship
        synonyms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="synonyms"
        )  # relationship
        replaced_by: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="replacedBy"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        valid_values: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="validValues"
        )  # relationship
        replacement_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="replacementTerms"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        see_also: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="seeAlso"
        )  # relationship
        translated_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="translatedTerms"
        )  # relationship
        is_a: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="isA"
        )  # relationship
        anchor: AtlasGlossary = Field(
            None, description="", alias="anchor"
        )  # relationship
        antonyms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="antonyms"
        )  # relationship
        assigned_entities: Optional[list[Referenceable]] = Field(
            None, description="", alias="assignedEntities"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        categories: Optional[list[AtlasGlossaryCategory]] = Field(
            None, description="", alias="categories"
        )  # relationship
        classifies: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="classifies"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        preferred_to_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="preferredToTerms"
        )  # relationship
        preferred_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="preferredTerms"
        )  # relationship

    attributes: "AtlasGlossaryTerm.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Cloud(Asset):
    """Description"""


class Infrastructure(Asset):
    """Description"""


class Connection(Asset):
    """Description"""

    type_name: Literal["Connection"]

    class Attributes(Asset.Attributes):
        category: Optional[str] = Field(None, description="", alias="category")
        sub_category: Optional[str] = Field(None, description="", alias="subCategory")
        host: Optional[str] = Field(None, description="", alias="host")
        port: Optional[int] = Field(None, description="", alias="port")
        allow_query: Optional[bool] = Field(None, description="", alias="allowQuery")
        allow_query_preview: Optional[bool] = Field(
            None, description="", alias="allowQueryPreview"
        )
        query_preview_config: Optional[dict[str, str]] = Field(
            None, description="", alias="queryPreviewConfig"
        )
        query_config: Optional[str] = Field(None, description="", alias="queryConfig")
        credential_strategy: Optional[str] = Field(
            None, description="", alias="credentialStrategy"
        )
        preview_credential_strategy: Optional[str] = Field(
            None, description="", alias="previewCredentialStrategy"
        )
        row_limit: Optional[int] = Field(None, description="", alias="rowLimit")
        default_credential_guid: Optional[str] = Field(
            None, description="", alias="defaultCredentialGuid"
        )
        connector_icon: Optional[str] = Field(
            None, description="", alias="connectorIcon"
        )
        connector_image: Optional[str] = Field(
            None, description="", alias="connectorImage"
        )
        source_logo: Optional[str] = Field(None, description="", alias="sourceLogo")
        popularity_insights_timeframe: Optional[int] = Field(
            None, description="", alias="popularityInsightsTimeframe"
        )
        has_popularity_insights: Optional[bool] = Field(
            None, description="", alias="hasPopularityInsights"
        )
        connection_dbt_environments: Optional[list[str]] = Field(
            None, description="", alias="connectionDbtEnvironments"
        )
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship

    attributes: "Connection.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Process(Asset):
    """Description"""

    class Attributes(Asset.Attributes):
        inputs: Optional[list[Catalog]] = Field(None, description="", alias="inputs")
        outputs: Optional[list[Catalog]] = Field(None, description="", alias="outputs")
        code: Optional[str] = Field(None, description="", alias="code")
        sql: Optional[str] = Field(None, description="", alias="sql")
        ast: Optional[str] = Field(None, description="", alias="ast")
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        column_processes: Optional[list[ColumnProcess]] = Field(
            None, description="", alias="columnProcesses"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship

    attributes: "Process.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AtlasGlossaryCategory(Asset):
    """Description"""

    type_name: Literal["AtlasGlossaryCategory"]

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
        anchor: AtlasGlossary = Field(
            None, description="", alias="anchor"
        )  # relationship
        parent_category: Optional[AtlasGlossaryCategory] = Field(
            None, description="", alias="parentCategory"
        )  # relationship
        children_categories: Optional[list[AtlasGlossaryCategory]] = Field(
            None, description="", alias="childrenCategories"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship

    attributes: "AtlasGlossaryCategory.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Badge(Asset):
    """Description"""

    type_name: Literal["Badge"]

    class Attributes(Asset.Attributes):
        badge_conditions: Optional[list[BadgeCondition]] = Field(
            None, description="", alias="badgeConditions"
        )
        badge_metadata_attribute: Optional[str] = Field(
            None, description="", alias="badgeMetadataAttribute"
        )
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship

    attributes: "Badge.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Namespace(Asset):
    """Description"""


class Catalog(Asset):
    """Description"""


class Google(Cloud):
    """Description"""

    class Attributes(Cloud.Attributes):
        google_service: Optional[str] = Field(
            None, description="", alias="googleService"
        )
        google_project_name: Optional[str] = Field(
            None, description="", alias="googleProjectName"
        )
        google_project_id: Optional[str] = Field(
            None, description="", alias="googleProjectId"
        )
        google_project_number: Optional[int] = Field(
            None, description="", alias="googleProjectNumber"
        )
        google_location: Optional[str] = Field(
            None, description="", alias="googleLocation"
        )
        google_location_type: Optional[str] = Field(
            None, description="", alias="googleLocationType"
        )
        google_labels: Optional[list[GoogleLabel]] = Field(
            None, description="", alias="googleLabels"
        )
        google_tags: Optional[list[GoogleTag]] = Field(
            None, description="", alias="googleTags"
        )
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship

    attributes: "Google.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AWS(Cloud):
    """Description"""

    class Attributes(Cloud.Attributes):
        aws_arn: Optional[str] = Field(None, description="", alias="awsArn")
        aws_partition: Optional[str] = Field(None, description="", alias="awsPartition")
        aws_service: Optional[str] = Field(None, description="", alias="awsService")
        aws_region: Optional[str] = Field(None, description="", alias="awsRegion")
        aws_account_id: Optional[str] = Field(
            None, description="", alias="awsAccountId"
        )
        aws_resource_id: Optional[str] = Field(
            None, description="", alias="awsResourceId"
        )
        aws_owner_name: Optional[str] = Field(
            None, description="", alias="awsOwnerName"
        )
        aws_owner_id: Optional[str] = Field(None, description="", alias="awsOwnerId")
        aws_tags: Optional[list[AwsTag]] = Field(None, description="", alias="awsTags")
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship

    attributes: "AWS.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class BIProcess(Process):
    """Description"""


class ColumnProcess(Process):
    """Description"""


class Collection(Namespace):
    """Description"""

    type_name: Literal["Collection"]

    class Attributes(Namespace.Attributes):
        icon: Optional[str] = Field(None, description="", alias="icon")
        icon_type: Optional[icon_type] = Field(None, description="", alias="iconType")
        children_queries: Optional[list[Query]] = Field(
            None, description="", alias="childrenQueries"
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
        children_folders: Optional[list[Folder]] = Field(
            None, description="", alias="childrenFolders"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship

    attributes: "Collection.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Folder(Namespace):
    """Description"""

    type_name: Literal["Folder"]

    class Attributes(Namespace.Attributes):
        parent_qualified_name: str = Field(
            None, description="", alias="parentQualifiedName"
        )
        collection_qualified_name: str = Field(
            None, description="", alias="collectionQualifiedName"
        )
        parent: Namespace = Field(None, description="", alias="parent")  # relationship
        children_queries: Optional[list[Query]] = Field(
            None, description="", alias="childrenQueries"
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
        children_folders: Optional[list[Folder]] = Field(
            None, description="", alias="childrenFolders"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship

    attributes: "Folder.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ObjectStore(Catalog):
    """Description"""


class DataQuality(Catalog):
    """Description"""


class BI(Catalog):
    """Description"""


class SaaS(Catalog):
    """Description"""


class Dbt(Catalog):
    """Description"""

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
        dbt_job_last_run: Optional[date] = Field(
            None, description="", alias="dbtJobLastRun"
        )
        dbt_job_next_run: Optional[date] = Field(
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
        dbt_tags: Optional[list[str]] = Field(None, description="", alias="dbtTags")
        dbt_connection_context: Optional[str] = Field(
            None, description="", alias="dbtConnectionContext"
        )
        dbt_semantic_layer_proxy_url: Optional[str] = Field(
            None, description="", alias="dbtSemanticLayerProxyUrl"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Dbt.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Resource(Catalog):
    """Description"""

    class Attributes(Catalog.Attributes):
        link: Optional[str] = Field(None, description="", alias="link")
        is_global: Optional[bool] = Field(None, description="", alias="isGlobal")
        reference: Optional[str] = Field(None, description="", alias="reference")
        resource_metadata: Optional[dict[str, str]] = Field(
            None, description="", alias="resourceMetadata"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Resource.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Insight(Catalog):
    """Description"""


class API(Catalog):
    """Description"""

    class Attributes(Catalog.Attributes):
        api_spec_type: Optional[str] = Field(None, description="", alias="apiSpecType")
        api_spec_version: Optional[str] = Field(
            None, description="", alias="apiSpecVersion"
        )
        api_spec_name: Optional[str] = Field(None, description="", alias="apiSpecName")
        api_spec_qualified_name: Optional[str] = Field(
            None, description="", alias="apiSpecQualifiedName"
        )
        api_external_docs: Optional[dict[str, str]] = Field(
            None, description="", alias="apiExternalDocs"
        )
        api_is_auth_optional: Optional[bool] = Field(
            None, description="", alias="apiIsAuthOptional"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "API.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SQL(Catalog):
    """Description"""

    class Attributes(Catalog.Attributes):
        query_count: Optional[int] = Field(None, description="", alias="queryCount")
        query_user_count: Optional[int] = Field(
            None, description="", alias="queryUserCount"
        )
        query_user_map: Optional[dict[str, int]] = Field(
            None, description="", alias="queryUserMap"
        )
        query_count_updated_at: Optional[date] = Field(
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
        last_profiled_at: Optional[date] = Field(
            None, description="", alias="lastProfiledAt"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "SQL.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DataStudio(Google):
    """Description"""


class GCS(Google):
    """Description"""

    class Attributes(Google.Attributes):
        gcs_storage_class: Optional[str] = Field(
            None, description="", alias="gcsStorageClass"
        )
        gcs_encryption_type: Optional[str] = Field(
            None, description="", alias="gcsEncryptionType"
        )
        gcs_e_tag: Optional[str] = Field(None, description="", alias="gcsETag")
        gcs_requester_pays: Optional[bool] = Field(
            None, description="", alias="gcsRequesterPays"
        )
        gcs_access_control: Optional[str] = Field(
            None, description="", alias="gcsAccessControl"
        )
        gcs_meta_generation_id: Optional[int] = Field(
            None, description="", alias="gcsMetaGenerationId"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "GCS.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DataStudioAsset(DataStudio):
    """Description"""

    type_name: Literal["DataStudioAsset"]

    class Attributes(DataStudio.Attributes):
        data_studio_asset_type: Optional[google_datastudio_asset_type] = Field(
            None, description="", alias="dataStudioAssetType"
        )
        data_studio_asset_title: Optional[str] = Field(
            None, description="", alias="dataStudioAssetTitle"
        )
        data_studio_asset_owner: Optional[str] = Field(
            None, description="", alias="dataStudioAssetOwner"
        )
        is_trashed_data_studio_asset: Optional[bool] = Field(
            None, description="", alias="isTrashedDataStudioAsset"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "DataStudioAsset.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class S3(ObjectStore):
    """Description"""

    class Attributes(ObjectStore.Attributes):
        s3_e_tag: Optional[str] = Field(None, description="", alias="s3ETag")
        s3_encryption: Optional[str] = Field(None, description="", alias="s3Encryption")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "S3.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtColumnProcess(Dbt):
    """Description"""

    type_name: Literal["DbtColumnProcess"]

    class Attributes(Dbt.Attributes):
        dbt_column_process_job_status: Optional[str] = Field(
            None, description="", alias="dbtColumnProcessJobStatus"
        )
        outputs: Optional[list[Catalog]] = Field(
            None, description="", alias="outputs"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        process: Optional[Process] = Field(
            None, description="", alias="process"
        )  # relationship
        inputs: Optional[list[Catalog]] = Field(
            None, description="", alias="inputs"
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
        column_processes: Optional[list[ColumnProcess]] = Field(
            None, description="", alias="columnProcesses"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "DbtColumnProcess.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Metric(DataQuality):
    """Description"""

    class Attributes(DataQuality.Attributes):
        metric_type: Optional[str] = Field(None, description="", alias="metricType")
        metric_s_q_l: Optional[str] = Field(None, description="", alias="metricSQL")
        metric_filters: Optional[str] = Field(
            None, description="", alias="metricFilters"
        )
        metric_time_grains: Optional[list[str]] = Field(
            None, description="", alias="metricTimeGrains"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        assets: Optional[list[Asset]] = Field(
            None, description="", alias="assets"
        )  # relationship
        metric_dimension_columns: Optional[list[Column]] = Field(
            None, description="", alias="metricDimensionColumns"
        )  # relationship
        metric_timestamp_column: Optional[Column] = Field(
            None, description="", alias="metricTimestampColumn"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Metric.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Metabase(BI):
    """Description"""

    class Attributes(BI.Attributes):
        metabase_collection_name: Optional[str] = Field(
            None, description="", alias="metabaseCollectionName"
        )
        metabase_collection_qualified_name: Optional[str] = Field(
            None, description="", alias="metabaseCollectionQualifiedName"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Metabase.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBI(BI):
    """Description"""

    class Attributes(BI.Attributes):
        power_b_i_is_hidden: Optional[bool] = Field(
            None, description="", alias="powerBIIsHidden"
        )
        power_b_i_table_qualified_name: Optional[str] = Field(
            None, description="", alias="powerBITableQualifiedName"
        )
        power_b_i_format_string: Optional[str] = Field(
            None, description="", alias="powerBIFormatString"
        )
        power_b_i_endorsement: Optional[powerbi_endorsement] = Field(
            None, description="", alias="powerBIEndorsement"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PowerBI.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Preset(BI):
    """Description"""

    class Attributes(BI.Attributes):
        preset_workspace_id: Optional[int] = Field(
            None, description="", alias="presetWorkspaceId"
        )
        preset_workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="presetWorkspaceQualifiedName"
        )
        preset_dashboard_id: Optional[int] = Field(
            None, description="", alias="presetDashboardId"
        )
        preset_dashboard_qualified_name: Optional[str] = Field(
            None, description="", alias="presetDashboardQualifiedName"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Preset.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Mode(BI):
    """Description"""

    class Attributes(BI.Attributes):
        mode_id: Optional[str] = Field(None, description="", alias="modeId")
        mode_token: Optional[str] = Field(None, description="", alias="modeToken")
        mode_workspace_name: Optional[str] = Field(
            None, description="", alias="modeWorkspaceName"
        )
        mode_workspace_username: Optional[str] = Field(
            None, description="", alias="modeWorkspaceUsername"
        )
        mode_workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="modeWorkspaceQualifiedName"
        )
        mode_report_name: Optional[str] = Field(
            None, description="", alias="modeReportName"
        )
        mode_report_qualified_name: Optional[str] = Field(
            None, description="", alias="modeReportQualifiedName"
        )
        mode_query_name: Optional[str] = Field(
            None, description="", alias="modeQueryName"
        )
        mode_query_qualified_name: Optional[str] = Field(
            None, description="", alias="modeQueryQualifiedName"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Mode.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Tableau(BI):
    """Description"""


class Looker(BI):
    """Description"""


class Salesforce(SaaS):
    """Description"""

    class Attributes(SaaS.Attributes):
        organization_qualified_name: Optional[str] = Field(
            None, description="", alias="organizationQualifiedName"
        )
        api_name: Optional[str] = Field(None, description="", alias="apiName")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Salesforce.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtModelColumn(Dbt):
    """Description"""

    type_name: Literal["DbtModelColumn"]

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
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        sql_column: Optional[Column] = Field(
            None, description="", alias="sqlColumn"
        )  # relationship
        dbt_model: Optional[DbtModel] = Field(
            None, description="", alias="dbtModel"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "DbtModelColumn.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtModel(Dbt):
    """Description"""

    type_name: Literal["DbtModel"]

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
        dbt_model_compile_started_at: Optional[date] = Field(
            None, description="", alias="dbtModelCompileStartedAt"
        )
        dbt_model_compile_completed_at: Optional[date] = Field(
            None, description="", alias="dbtModelCompileCompletedAt"
        )
        dbt_model_execute_started_at: Optional[date] = Field(
            None, description="", alias="dbtModelExecuteStartedAt"
        )
        dbt_model_execute_completed_at: Optional[date] = Field(
            None, description="", alias="dbtModelExecuteCompletedAt"
        )
        dbt_model_execution_time: Optional[float] = Field(
            None, description="", alias="dbtModelExecutionTime"
        )
        dbt_model_run_generated_at: Optional[date] = Field(
            None, description="", alias="dbtModelRunGeneratedAt"
        )
        dbt_model_run_elapsed_time: Optional[float] = Field(
            None, description="", alias="dbtModelRunElapsedTime"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        dbt_metrics: Optional[list[DbtMetric]] = Field(
            None, description="", alias="dbtMetrics"
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
        dbt_model_columns: Optional[list[DbtModelColumn]] = Field(
            None, description="", alias="dbtModelColumns"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        sql_asset: Optional[SQL] = Field(
            None, description="", alias="sqlAsset"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "DbtModel.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtMetric(Dbt):
    """Description"""

    type_name: Literal["DbtMetric"]

    class Attributes(Dbt.Attributes):
        dbt_metric_filters: Optional[list[DbtMetricFilter]] = Field(
            None, description="", alias="dbtMetricFilters"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        assets: Optional[list[Asset]] = Field(
            None, description="", alias="assets"
        )  # relationship
        metric_dimension_columns: Optional[list[Column]] = Field(
            None, description="", alias="metricDimensionColumns"
        )  # relationship
        metric_timestamp_column: Optional[Column] = Field(
            None, description="", alias="metricTimestampColumn"
        )  # relationship
        dbt_metric_filter_columns: Optional[list[Column]] = Field(
            None, description="", alias="dbtMetricFilterColumns"
        )  # relationship
        dbt_model: Optional[DbtModel] = Field(
            None, description="", alias="dbtModel"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "DbtMetric.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtSource(Dbt):
    """Description"""

    type_name: Literal["DbtSource"]

    class Attributes(Dbt.Attributes):
        dbt_state: Optional[str] = Field(None, description="", alias="dbtState")
        dbt_freshness_criteria: Optional[str] = Field(
            None, description="", alias="dbtFreshnessCriteria"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        sql_asset: Optional[SQL] = Field(
            None, description="", alias="sqlAsset"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "DbtSource.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtProcess(Dbt):
    """Description"""

    type_name: Literal["DbtProcess"]

    class Attributes(Dbt.Attributes):
        dbt_process_job_status: Optional[str] = Field(
            None, description="", alias="dbtProcessJobStatus"
        )
        outputs: Optional[list[Catalog]] = Field(
            None, description="", alias="outputs"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        inputs: Optional[list[Catalog]] = Field(
            None, description="", alias="inputs"
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
        column_processes: Optional[list[ColumnProcess]] = Field(
            None, description="", alias="columnProcesses"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "DbtProcess.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ReadmeTemplate(Resource):
    """Description"""

    type_name: Literal["ReadmeTemplate"]

    class Attributes(Resource.Attributes):
        icon: Optional[str] = Field(None, description="", alias="icon")
        icon_type: Optional[icon_type] = Field(None, description="", alias="iconType")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "ReadmeTemplate.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Readme(Resource):
    """Description"""


class Link(Resource):
    """Description"""

    type_name: Literal["Link"]

    class Attributes(Resource.Attributes):
        icon: Optional[str] = Field(None, description="", alias="icon")
        icon_type: Optional[icon_type] = Field(None, description="", alias="iconType")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        internal: Optional[Internal] = Field(
            None, description="", alias="internal"
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
        asset: Optional[Asset] = Field(
            None, description="", alias="asset"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Link.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class APISpec(API):
    """Description"""

    type_name: Literal["APISpec"]

    class Attributes(API.Attributes):
        api_spec_terms_of_service_url: Optional[str] = Field(
            None, description="", alias="apiSpecTermsOfServiceURL"
        )
        api_spec_contact_email: Optional[str] = Field(
            None, description="", alias="apiSpecContactEmail"
        )
        api_spec_contact_name: Optional[str] = Field(
            None, description="", alias="apiSpecContactName"
        )
        api_spec_contact_url: Optional[str] = Field(
            None, description="", alias="apiSpecContactURL"
        )
        api_spec_license_name: Optional[str] = Field(
            None, description="", alias="apiSpecLicenseName"
        )
        api_spec_license_url: Optional[str] = Field(
            None, description="", alias="apiSpecLicenseURL"
        )
        api_spec_contract_version: Optional[str] = Field(
            None, description="", alias="apiSpecContractVersion"
        )
        api_spec_service_alias: Optional[str] = Field(
            None, description="", alias="apiSpecServiceAlias"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        api_paths: Optional[list[APIPath]] = Field(
            None, description="", alias="apiPaths"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "APISpec.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class APIPath(API):
    """Description"""

    type_name: Literal["APIPath"]

    class Attributes(API.Attributes):
        api_path_summary: Optional[str] = Field(
            None, description="", alias="apiPathSummary"
        )
        api_path_raw_u_r_i: Optional[str] = Field(
            None, description="", alias="apiPathRawURI"
        )
        api_path_is_templated: Optional[bool] = Field(
            None, description="", alias="apiPathIsTemplated"
        )
        api_path_available_operations: Optional[list[str]] = Field(
            None, description="", alias="apiPathAvailableOperations"
        )
        api_path_available_response_codes: Optional[dict[str, str]] = Field(
            None, description="", alias="apiPathAvailableResponseCodes"
        )
        api_path_is_ingress_exposed: Optional[bool] = Field(
            None, description="", alias="apiPathIsIngressExposed"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship
        api_spec: Optional[APISpec] = Field(
            None, description="", alias="apiSpec"
        )  # relationship

    attributes: "APIPath.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TablePartition(SQL):
    """Description"""

    type_name: Literal["TablePartition"]

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
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        parent_table: Optional[Table] = Field(
            None, description="", alias="parentTable"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "TablePartition.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Table(SQL):
    """Description"""

    type_name: Literal["Table"]

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
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
        )  # relationship
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
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
        queries: Optional[list[Query]] = Field(
            None, description="", alias="queries"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Table.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Query(SQL):
    """Description"""

    type_name: Literal["Query"]

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
        parent_qualified_name: str = Field(
            None, description="", alias="parentQualifiedName"
        )
        collection_qualified_name: str = Field(
            None, description="", alias="collectionQualifiedName"
        )
        is_visual_query: Optional[bool] = Field(
            None, description="", alias="isVisualQuery"
        )
        visual_builder_schema_base64: Optional[str] = Field(
            None, description="", alias="visualBuilderSchemaBase64"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        parent: Namespace = Field(None, description="", alias="parent")  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        tables: Optional[list[Table]] = Field(
            None, description="", alias="tables"
        )  # relationship
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        views: Optional[list[View]] = Field(
            None, description="", alias="views"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Query.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Column(SQL):
    """Description"""

    type_name: Literal["Column"]

    class Attributes(SQL.Attributes):
        data_type: Optional[str] = Field(None, description="", alias="dataType")
        sub_data_type: Optional[str] = Field(None, description="", alias="subDataType")
        order: Optional[int] = Field(None, description="", alias="order")
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
        pinned_at: Optional[date] = Field(None, description="", alias="pinnedAt")
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
        column_distinct_values_count: Optional[int] = Field(
            None, description="", alias="columnDistinctValuesCount"
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
        column_average: Optional[float] = Field(
            None, description="", alias="columnAverage"
        )
        column_average_length: Optional[float] = Field(
            None, description="", alias="columnAverageLength"
        )
        column_duplicate_values_count: Optional[int] = Field(
            None, description="", alias="columnDuplicateValuesCount"
        )
        column_maximum_string_length: Optional[int] = Field(
            None, description="", alias="columnMaximumStringLength"
        )
        column_maxs: Optional[list[str]] = Field(
            None, description="", alias="columnMaxs"
        )
        column_minimum_string_length: Optional[int] = Field(
            None, description="", alias="columnMinimumStringLength"
        )
        column_mins: Optional[list[str]] = Field(
            None, description="", alias="columnMins"
        )
        column_missing_values_count: Optional[int] = Field(
            None, description="", alias="columnMissingValuesCount"
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
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        materialised_view: Optional[MaterialisedView] = Field(
            None, description="", alias="materialisedView"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        queries: Optional[list[Query]] = Field(
            None, description="", alias="queries"
        )  # relationship
        metric_timestamps: Optional[list[Metric]] = Field(
            None, description="", alias="metricTimestamps"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        dbt_metrics: Optional[list[DbtMetric]] = Field(
            None, description="", alias="dbtMetrics"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        view: Optional[View] = Field(None, description="", alias="view")  # relationship
        table_partition: Optional[TablePartition] = Field(
            None, description="", alias="tablePartition"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        data_quality_metric_dimensions: Optional[list[Metric]] = Field(
            None, description="", alias="dataQualityMetricDimensions"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        dbt_model_columns: Optional[list[DbtModelColumn]] = Field(
            None, description="", alias="dbtModelColumns"
        )  # relationship
        table: Optional[Table] = Field(
            None, description="", alias="table"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Column.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Schema(SQL):
    """Description"""

    type_name: Literal["Schema"]

    class Attributes(SQL.Attributes):
        table_count: Optional[int] = Field(None, description="", alias="tableCount")
        views_count: Optional[int] = Field(None, description="", alias="viewsCount")
        materialised_views: Optional[list[MaterialisedView]] = Field(
            None, description="", alias="materialisedViews"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        tables: Optional[list[Table]] = Field(
            None, description="", alias="tables"
        )  # relationship
        database: Optional[Database] = Field(
            None, description="", alias="database"
        )  # relationship
        snowflake_pipes: Optional[list[SnowflakePipe]] = Field(
            None, description="", alias="snowflakePipes"
        )  # relationship
        snowflake_streams: Optional[list[SnowflakeStream]] = Field(
            None, description="", alias="snowflakeStreams"
        )  # relationship
        procedures: Optional[list[Procedure]] = Field(
            None, description="", alias="procedures"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        views: Optional[list[View]] = Field(
            None, description="", alias="views"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Schema.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Database(SQL):
    """Description"""

    type_name: Literal["Database"]

    class Attributes(SQL.Attributes):
        schema_count: Optional[int] = Field(None, description="", alias="schemaCount")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        schemas: Optional[list[Schema]] = Field(
            None, description="", alias="schemas"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Database.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SnowflakeStream(SQL):
    """Description"""

    type_name: Literal["SnowflakeStream"]

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
        snowflake_stream_stale_after: Optional[date] = Field(
            None, description="", alias="snowflakeStreamStaleAfter"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "SnowflakeStream.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SnowflakePipe(SQL):
    """Description"""

    type_name: Literal["SnowflakePipe"]

    class Attributes(SQL.Attributes):
        definition: Optional[str] = Field(None, description="", alias="definition")
        snowflake_pipe_is_auto_ingest_enabled: Optional[bool] = Field(
            None, description="", alias="snowflakePipeIsAutoIngestEnabled"
        )
        snowflake_pipe_notification_channel_name: Optional[str] = Field(
            None, description="", alias="snowflakePipeNotificationChannelName"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "SnowflakePipe.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Procedure(SQL):
    """Description"""

    type_name: Literal["Procedure"]

    class Attributes(SQL.Attributes):
        definition: str = Field(None, description="", alias="definition")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Procedure.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class View(SQL):
    """Description"""

    type_name: Literal["View"]

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
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
        )  # relationship
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
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
        queries: Optional[list[Query]] = Field(
            None, description="", alias="queries"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "View.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MaterialisedView(SQL):
    """Description"""

    type_name: Literal["MaterialisedView"]

    class Attributes(SQL.Attributes):
        refresh_mode: Optional[str] = Field(None, description="", alias="refreshMode")
        refresh_method: Optional[str] = Field(
            None, description="", alias="refreshMethod"
        )
        staleness: Optional[str] = Field(None, description="", alias="staleness")
        stale_since_date: Optional[date] = Field(
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
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
        )  # relationship
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
        )  # relationship
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "MaterialisedView.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class GCSObject(GCS):
    """Description"""

    type_name: Literal["GCSObject"]

    class Attributes(GCS.Attributes):
        gcs_bucket_name: Optional[str] = Field(
            None, description="", alias="gcsBucketName"
        )
        gcs_bucket_qualified_name: Optional[str] = Field(
            None, description="", alias="gcsBucketQualifiedName"
        )
        gcs_object_size: Optional[int] = Field(
            None, description="", alias="gcsObjectSize"
        )
        gcs_object_key: Optional[str] = Field(
            None, description="", alias="gcsObjectKey"
        )
        gcs_object_media_link: Optional[str] = Field(
            None, description="", alias="gcsObjectMediaLink"
        )
        gcs_object_hold_type: Optional[str] = Field(
            None, description="", alias="gcsObjectHoldType"
        )
        gcs_object_generation_id: Optional[int] = Field(
            None, description="", alias="gcsObjectGenerationId"
        )
        gcs_object_c_r_c32_c_hash: Optional[str] = Field(
            None, description="", alias="gcsObjectCRC32CHash"
        )
        gcs_object_m_d5_hash: Optional[str] = Field(
            None, description="", alias="gcsObjectMD5Hash"
        )
        gcs_object_data_last_modified_time: Optional[date] = Field(
            None, description="", alias="gcsObjectDataLastModifiedTime"
        )
        gcs_object_content_type: Optional[str] = Field(
            None, description="", alias="gcsObjectContentType"
        )
        gcs_object_content_encoding: Optional[str] = Field(
            None, description="", alias="gcsObjectContentEncoding"
        )
        gcs_object_content_disposition: Optional[str] = Field(
            None, description="", alias="gcsObjectContentDisposition"
        )
        gcs_object_content_language: Optional[str] = Field(
            None, description="", alias="gcsObjectContentLanguage"
        )
        gcs_object_retention_expiration_date: Optional[date] = Field(
            None, description="", alias="gcsObjectRetentionExpirationDate"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        gcs_bucket: Optional[GCSBucket] = Field(
            None, description="", alias="gcsBucket"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "GCSObject.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class GCSBucket(GCS):
    """Description"""

    type_name: Literal["GCSBucket"]

    class Attributes(GCS.Attributes):
        gcs_object_count: Optional[int] = Field(
            None, description="", alias="gcsObjectCount"
        )
        gcs_bucket_versioning_enabled: Optional[bool] = Field(
            None, description="", alias="gcsBucketVersioningEnabled"
        )
        gcs_bucket_retention_locked: Optional[bool] = Field(
            None, description="", alias="gcsBucketRetentionLocked"
        )
        gcs_bucket_retention_period: Optional[int] = Field(
            None, description="", alias="gcsBucketRetentionPeriod"
        )
        gcs_bucket_retention_effective_time: Optional[date] = Field(
            None, description="", alias="gcsBucketRetentionEffectiveTime"
        )
        gcs_bucket_lifecycle_rules: Optional[str] = Field(
            None, description="", alias="gcsBucketLifecycleRules"
        )
        gcs_bucket_retention_policy: Optional[str] = Field(
            None, description="", alias="gcsBucketRetentionPolicy"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        gcs_objects: Optional[list[GCSObject]] = Field(
            None, description="", alias="gcsObjects"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "GCSBucket.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class S3Bucket(S3):
    """Description"""

    type_name: Literal["S3Bucket"]

    class Attributes(S3.Attributes):
        s3_object_count: Optional[int] = Field(
            None, description="", alias="s3ObjectCount"
        )
        s3_bucket_versioning_enabled: Optional[bool] = Field(
            None, description="", alias="s3BucketVersioningEnabled"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        objects: Optional[list[S3Object]] = Field(
            None, description="", alias="objects"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "S3Bucket.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class S3Object(S3):
    """Description"""

    type_name: Literal["S3Object"]

    class Attributes(S3.Attributes):
        s3_object_last_modified_time: Optional[date] = Field(
            None, description="", alias="s3ObjectLastModifiedTime"
        )
        s3_bucket_name: Optional[str] = Field(
            None, description="", alias="s3BucketName"
        )
        s3_bucket_qualified_name: Optional[str] = Field(
            None, description="", alias="s3BucketQualifiedName"
        )
        s3_object_size: Optional[int] = Field(
            None, description="", alias="s3ObjectSize"
        )
        s3_object_storage_class: Optional[str] = Field(
            None, description="", alias="s3ObjectStorageClass"
        )
        s3_object_key: Optional[str] = Field(None, description="", alias="s3ObjectKey")
        s3_object_content_type: Optional[str] = Field(
            None, description="", alias="s3ObjectContentType"
        )
        s3_object_content_disposition: Optional[str] = Field(
            None, description="", alias="s3ObjectContentDisposition"
        )
        s3_object_version_id: Optional[str] = Field(
            None, description="", alias="s3ObjectVersionId"
        )
        bucket: Optional[S3Bucket] = Field(
            None, description="", alias="bucket"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "S3Object.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MetabaseQuestion(Metabase):
    """Description"""

    type_name: Literal["MetabaseQuestion"]

    class Attributes(Metabase.Attributes):
        metabase_dashboard_count: Optional[int] = Field(
            None, description="", alias="metabaseDashboardCount"
        )
        metabase_query_type: Optional[str] = Field(
            None, description="", alias="metabaseQueryType"
        )
        metabase_query: Optional[str] = Field(
            None, description="", alias="metabaseQuery"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        metabase_dashboards: Optional[list[MetabaseDashboard]] = Field(
            None, description="", alias="metabaseDashboards"
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
        metabase_collection: Optional[MetabaseCollection] = Field(
            None, description="", alias="metabaseCollection"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "MetabaseQuestion.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MetabaseCollection(Metabase):
    """Description"""

    type_name: Literal["MetabaseCollection"]

    class Attributes(Metabase.Attributes):
        metabase_slug: Optional[str] = Field(None, description="", alias="metabaseSlug")
        metabase_color: Optional[str] = Field(
            None, description="", alias="metabaseColor"
        )
        metabase_namespace: Optional[str] = Field(
            None, description="", alias="metabaseNamespace"
        )
        metabase_is_personal_collection: Optional[bool] = Field(
            None, description="", alias="metabaseIsPersonalCollection"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        metabase_dashboards: Optional[list[MetabaseDashboard]] = Field(
            None, description="", alias="metabaseDashboards"
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
        metabase_questions: Optional[list[MetabaseQuestion]] = Field(
            None, description="", alias="metabaseQuestions"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "MetabaseCollection.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MetabaseDashboard(Metabase):
    """Description"""

    type_name: Literal["MetabaseDashboard"]

    class Attributes(Metabase.Attributes):
        metabase_question_count: Optional[int] = Field(
            None, description="", alias="metabaseQuestionCount"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        metabase_questions: Optional[list[MetabaseQuestion]] = Field(
            None, description="", alias="metabaseQuestions"
        )  # relationship
        metabase_collection: Optional[MetabaseCollection] = Field(
            None, description="", alias="metabaseCollection"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "MetabaseDashboard.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIReport(PowerBI):
    """Description"""

    type_name: Literal["PowerBIReport"]

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="datasetQualifiedName"
        )
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        page_count: Optional[int] = Field(None, description="", alias="pageCount")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        tiles: Optional[list[PowerBITile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        workspace: Optional[PowerBIWorkspace] = Field(
            None, description="", alias="workspace"
        )  # relationship
        pages: Optional[list[PowerBIPage]] = Field(
            None, description="", alias="pages"
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
        dataset: Optional[PowerBIDataset] = Field(
            None, description="", alias="dataset"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PowerBIReport.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIMeasure(PowerBI):
    """Description"""

    type_name: Literal["PowerBIMeasure"]

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="datasetQualifiedName"
        )
        power_b_i_measure_expression: Optional[str] = Field(
            None, description="", alias="powerBIMeasureExpression"
        )
        power_b_i_is_external_measure: Optional[bool] = Field(
            None, description="", alias="powerBIIsExternalMeasure"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        table: Optional[PowerBITable] = Field(
            None, description="", alias="table"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PowerBIMeasure.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIColumn(PowerBI):
    """Description"""

    type_name: Literal["PowerBIColumn"]

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="datasetQualifiedName"
        )
        power_b_i_column_data_category: Optional[str] = Field(
            None, description="", alias="powerBIColumnDataCategory"
        )
        power_b_i_column_data_type: Optional[str] = Field(
            None, description="", alias="powerBIColumnDataType"
        )
        power_b_i_sort_by_column: Optional[str] = Field(
            None, description="", alias="powerBISortByColumn"
        )
        power_b_i_column_summarize_by: Optional[str] = Field(
            None, description="", alias="powerBIColumnSummarizeBy"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        table: Optional[PowerBITable] = Field(
            None, description="", alias="table"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PowerBIColumn.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBITile(PowerBI):
    """Description"""

    type_name: Literal["PowerBITile"]

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        dashboard_qualified_name: Optional[str] = Field(
            None, description="", alias="dashboardQualifiedName"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        report: Optional[PowerBIReport] = Field(
            None, description="", alias="report"
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
        dataset: Optional[PowerBIDataset] = Field(
            None, description="", alias="dataset"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        dashboard: Optional[PowerBIDashboard] = Field(
            None, description="", alias="dashboard"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PowerBITile.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBITable(PowerBI):
    """Description"""

    type_name: Literal["PowerBITable"]

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="datasetQualifiedName"
        )
        power_b_i_table_source_expressions: Optional[list[str]] = Field(
            None, description="", alias="powerBITableSourceExpressions"
        )
        power_b_i_table_column_count: Optional[int] = Field(
            None, description="", alias="powerBITableColumnCount"
        )
        power_b_i_table_measure_count: Optional[int] = Field(
            None, description="", alias="powerBITableMeasureCount"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        measures: Optional[list[PowerBIMeasure]] = Field(
            None, description="", alias="measures"
        )  # relationship
        columns: Optional[list[PowerBIColumn]] = Field(
            None, description="", alias="columns"
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
        dataset: Optional[PowerBIDataset] = Field(
            None, description="", alias="dataset"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PowerBITable.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIDatasource(PowerBI):
    """Description"""

    type_name: Literal["PowerBIDatasource"]

    class Attributes(PowerBI.Attributes):
        connection_details: Optional[dict[str, str]] = Field(
            None, description="", alias="connectionDetails"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        datasets: Optional[list[PowerBIDataset]] = Field(
            None, description="", alias="datasets"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PowerBIDatasource.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIWorkspace(PowerBI):
    """Description"""

    type_name: Literal["PowerBIWorkspace"]

    class Attributes(PowerBI.Attributes):
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        report_count: Optional[int] = Field(None, description="", alias="reportCount")
        dashboard_count: Optional[int] = Field(
            None, description="", alias="dashboardCount"
        )
        dataset_count: Optional[int] = Field(None, description="", alias="datasetCount")
        dataflow_count: Optional[int] = Field(
            None, description="", alias="dataflowCount"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        reports: Optional[list[PowerBIReport]] = Field(
            None, description="", alias="reports"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        datasets: Optional[list[PowerBIDataset]] = Field(
            None, description="", alias="datasets"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        dashboards: Optional[list[PowerBIDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship
        dataflows: Optional[list[PowerBIDataflow]] = Field(
            None, description="", alias="dataflows"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PowerBIWorkspace.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIDataset(PowerBI):
    """Description"""

    type_name: Literal["PowerBIDataset"]

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        reports: Optional[list[PowerBIReport]] = Field(
            None, description="", alias="reports"
        )  # relationship
        tiles: Optional[list[PowerBITile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        workspace: Optional[PowerBIWorkspace] = Field(
            None, description="", alias="workspace"
        )  # relationship
        tables: Optional[list[PowerBITable]] = Field(
            None, description="", alias="tables"
        )  # relationship
        datasources: Optional[list[PowerBIDatasource]] = Field(
            None, description="", alias="datasources"
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
        dataflows: Optional[list[PowerBIDataflow]] = Field(
            None, description="", alias="dataflows"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PowerBIDataset.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIDashboard(PowerBI):
    """Description"""

    type_name: Literal["PowerBIDashboard"]

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        tile_count: Optional[int] = Field(None, description="", alias="tileCount")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        tiles: Optional[list[PowerBITile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        workspace: Optional[PowerBIWorkspace] = Field(
            None, description="", alias="workspace"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PowerBIDashboard.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIPage(PowerBI):
    """Description"""

    type_name: Literal["PowerBIPage"]

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        report_qualified_name: Optional[str] = Field(
            None, description="", alias="reportQualifiedName"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        report: Optional[PowerBIReport] = Field(
            None, description="", alias="report"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PowerBIPage.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIDataflow(PowerBI):
    """Description"""

    type_name: Literal["PowerBIDataflow"]

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        workspace: Optional[PowerBIWorkspace] = Field(
            None, description="", alias="workspace"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        datasets: Optional[list[PowerBIDataset]] = Field(
            None, description="", alias="datasets"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PowerBIDataflow.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PresetChart(Preset):
    """Description"""

    type_name: Literal["PresetChart"]

    class Attributes(Preset.Attributes):
        preset_chart_description_markdown: Optional[str] = Field(
            None, description="", alias="presetChartDescriptionMarkdown"
        )
        preset_chart_form_data: Optional[dict[str, str]] = Field(
            None, description="", alias="presetChartFormData"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        preset_dashboard: Optional[PresetDashboard] = Field(
            None, description="", alias="presetDashboard"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PresetChart.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PresetDataset(Preset):
    """Description"""

    type_name: Literal["PresetDataset"]

    class Attributes(Preset.Attributes):
        preset_dataset_datasource_name: Optional[str] = Field(
            None, description="", alias="presetDatasetDatasourceName"
        )
        preset_dataset_id: Optional[int] = Field(
            None, description="", alias="presetDatasetId"
        )
        preset_dataset_type: Optional[str] = Field(
            None, description="", alias="presetDatasetType"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        preset_dashboard: Optional[PresetDashboard] = Field(
            None, description="", alias="presetDashboard"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PresetDataset.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PresetDashboard(Preset):
    """Description"""

    type_name: Literal["PresetDashboard"]

    class Attributes(Preset.Attributes):
        preset_dashboard_changed_by_name: Optional[str] = Field(
            None, description="", alias="presetDashboardChangedByName"
        )
        preset_dashboard_changed_by_url: Optional[str] = Field(
            None, description="", alias="presetDashboardChangedByURL"
        )
        preset_dashboard_is_managed_externally: Optional[bool] = Field(
            None, description="", alias="presetDashboardIsManagedExternally"
        )
        preset_dashboard_is_published: Optional[bool] = Field(
            None, description="", alias="presetDashboardIsPublished"
        )
        preset_dashboard_thumbnail_url: Optional[str] = Field(
            None, description="", alias="presetDashboardThumbnailURL"
        )
        preset_dashboard_chart_count: Optional[int] = Field(
            None, description="", alias="presetDashboardChartCount"
        )
        preset_datasets: Optional[list[PresetDataset]] = Field(
            None, description="", alias="presetDatasets"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        preset_charts: Optional[list[PresetChart]] = Field(
            None, description="", alias="presetCharts"
        )  # relationship
        preset_workspace: Optional[PresetWorkspace] = Field(
            None, description="", alias="presetWorkspace"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PresetDashboard.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PresetWorkspace(Preset):
    """Description"""

    type_name: Literal["PresetWorkspace"]

    class Attributes(Preset.Attributes):
        preset_workspace_public_dashboards_allowed: Optional[bool] = Field(
            None, description="", alias="presetWorkspacePublicDashboardsAllowed"
        )
        preset_workspace_cluster_id: Optional[int] = Field(
            None, description="", alias="presetWorkspaceClusterId"
        )
        preset_workspace_hostname: Optional[str] = Field(
            None, description="", alias="presetWorkspaceHostname"
        )
        preset_workspace_is_in_maintenance_mode: Optional[bool] = Field(
            None, description="", alias="presetWorkspaceIsInMaintenanceMode"
        )
        preset_workspace_region: Optional[str] = Field(
            None, description="", alias="presetWorkspaceRegion"
        )
        preset_workspace_status: Optional[str] = Field(
            None, description="", alias="presetWorkspaceStatus"
        )
        preset_workspace_deployment_id: Optional[int] = Field(
            None, description="", alias="presetWorkspaceDeploymentId"
        )
        preset_workspace_dashboard_count: Optional[int] = Field(
            None, description="", alias="presetWorkspaceDashboardCount"
        )
        preset_workspace_dataset_count: Optional[int] = Field(
            None, description="", alias="presetWorkspaceDatasetCount"
        )
        preset_dashboards: Optional[list[PresetDashboard]] = Field(
            None, description="", alias="presetDashboards"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "PresetWorkspace.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeReport(Mode):
    """Description"""

    type_name: Literal["ModeReport"]

    class Attributes(Mode.Attributes):
        mode_collection_token: Optional[str] = Field(
            None, description="", alias="modeCollectionToken"
        )
        mode_report_published_at: Optional[date] = Field(
            None, description="", alias="modeReportPublishedAt"
        )
        mode_query_count: Optional[int] = Field(
            None, description="", alias="modeQueryCount"
        )
        mode_chart_count: Optional[int] = Field(
            None, description="", alias="modeChartCount"
        )
        mode_query_preview: Optional[str] = Field(
            None, description="", alias="modeQueryPreview"
        )
        mode_is_public: Optional[bool] = Field(
            None, description="", alias="modeIsPublic"
        )
        mode_is_shared: Optional[bool] = Field(
            None, description="", alias="modeIsShared"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        mode_collections: Optional[list[ModeCollection]] = Field(
            None, description="", alias="modeCollections"
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
        mode_queries: Optional[list[ModeQuery]] = Field(
            None, description="", alias="modeQueries"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "ModeReport.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeQuery(Mode):
    """Description"""

    type_name: Literal["ModeQuery"]

    class Attributes(Mode.Attributes):
        mode_raw_query: Optional[str] = Field(
            None, description="", alias="modeRawQuery"
        )
        mode_report_import_count: Optional[int] = Field(
            None, description="", alias="modeReportImportCount"
        )
        mode_charts: Optional[list[ModeChart]] = Field(
            None, description="", alias="modeCharts"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        mode_report: Optional[ModeReport] = Field(
            None, description="", alias="modeReport"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "ModeQuery.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeChart(Mode):
    """Description"""

    type_name: Literal["ModeChart"]

    class Attributes(Mode.Attributes):
        mode_chart_type: Optional[str] = Field(
            None, description="", alias="modeChartType"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship
        mode_query: Optional[ModeQuery] = Field(
            None, description="", alias="modeQuery"
        )  # relationship

    attributes: "ModeChart.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeWorkspace(Mode):
    """Description"""

    type_name: Literal["ModeWorkspace"]

    class Attributes(Mode.Attributes):
        mode_collection_count: Optional[int] = Field(
            None, description="", alias="modeCollectionCount"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        mode_collections: Optional[list[ModeCollection]] = Field(
            None, description="", alias="modeCollections"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "ModeWorkspace.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeCollection(Mode):
    """Description"""

    type_name: Literal["ModeCollection"]

    class Attributes(Mode.Attributes):
        mode_collection_type: Optional[str] = Field(
            None, description="", alias="modeCollectionType"
        )
        mode_collection_state: Optional[str] = Field(
            None, description="", alias="modeCollectionState"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        mode_workspace: Optional[ModeWorkspace] = Field(
            None, description="", alias="modeWorkspace"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        mode_reports: Optional[list[ModeReport]] = Field(
            None, description="", alias="modeReports"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "ModeCollection.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauWorkbook(Tableau):
    """Description"""

    type_name: Literal["TableauWorkbook"]

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        top_level_project_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        worksheets: Optional[list[TableauWorksheet]] = Field(
            None, description="", alias="worksheets"
        )  # relationship
        datasources: Optional[list[TableauDatasource]] = Field(
            None, description="", alias="datasources"
        )  # relationship
        project: Optional[TableauProject] = Field(
            None, description="", alias="project"
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
        dashboards: Optional[list[TableauDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "TableauWorkbook.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauDatasourceField(Tableau):
    """Description"""

    type_name: Literal["TableauDatasourceField"]

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        workbook_qualified_name: Optional[str] = Field(
            None, description="", alias="workbookQualifiedName"
        )
        datasource_qualified_name: Optional[str] = Field(
            None, description="", alias="datasourceQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        fully_qualified_name: Optional[str] = Field(
            None, description="", alias="fullyQualifiedName"
        )
        tableau_datasource_field_data_category: Optional[str] = Field(
            None, description="", alias="tableauDatasourceFieldDataCategory"
        )
        tableau_datasource_field_role: Optional[str] = Field(
            None, description="", alias="tableauDatasourceFieldRole"
        )
        tableau_datasource_field_data_type: Optional[str] = Field(
            None, description="", alias="tableauDatasourceFieldDataType"
        )
        upstream_tables: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="upstreamTables"
        )
        tableau_datasource_field_formula: Optional[str] = Field(
            None, description="", alias="tableauDatasourceFieldFormula"
        )
        tableau_datasource_field_bin_size: Optional[str] = Field(
            None, description="", alias="tableauDatasourceFieldBinSize"
        )
        upstream_columns: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="upstreamColumns"
        )
        upstream_fields: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="upstreamFields"
        )
        datasource_field_type: Optional[str] = Field(
            None, description="", alias="datasourceFieldType"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        worksheets: Optional[list[TableauWorksheet]] = Field(
            None, description="", alias="worksheets"
        )  # relationship
        datasource: Optional[TableauDatasource] = Field(
            None, description="", alias="datasource"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "TableauDatasourceField.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauCalculatedField(Tableau):
    """Description"""

    type_name: Literal["TableauCalculatedField"]

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        workbook_qualified_name: Optional[str] = Field(
            None, description="", alias="workbookQualifiedName"
        )
        datasource_qualified_name: Optional[str] = Field(
            None, description="", alias="datasourceQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        data_category: Optional[str] = Field(None, description="", alias="dataCategory")
        role: Optional[str] = Field(None, description="", alias="role")
        tableau_data_type: Optional[str] = Field(
            None, description="", alias="tableauDataType"
        )
        formula: Optional[str] = Field(None, description="", alias="formula")
        upstream_fields: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="upstreamFields"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        worksheets: Optional[list[TableauWorksheet]] = Field(
            None, description="", alias="worksheets"
        )  # relationship
        datasource: Optional[TableauDatasource] = Field(
            None, description="", alias="datasource"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "TableauCalculatedField.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauProject(Tableau):
    """Description"""

    type_name: Literal["TableauProject"]

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        is_top_level_project: Optional[bool] = Field(
            None, description="", alias="isTopLevelProject"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        workbooks: Optional[list[TableauWorkbook]] = Field(
            None, description="", alias="workbooks"
        )  # relationship
        site: Optional[TableauSite] = Field(
            None, description="", alias="site"
        )  # relationship
        parent_project: Optional[TableauProject] = Field(
            None, description="", alias="parentProject"
        )  # relationship
        datasources: Optional[list[TableauDatasource]] = Field(
            None, description="", alias="datasources"
        )  # relationship
        flows: Optional[list[TableauFlow]] = Field(
            None, description="", alias="flows"
        )  # relationship
        child_projects: Optional[list[TableauProject]] = Field(
            None, description="", alias="childProjects"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        metrics: Optional[list[TableauMetric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        metrics: Optional[list[Metric]] = Field(
            None, description="", alias="metrics"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "TableauProject.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauMetric(Tableau):
    """Description"""

    type_name: Literal["TableauMetric"]

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        project: Optional[TableauProject] = Field(
            None, description="", alias="project"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "TableauMetric.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauDatasource(Tableau):
    """Description"""

    type_name: Literal["TableauDatasource"]

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        workbook_qualified_name: Optional[str] = Field(
            None, description="", alias="workbookQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        is_published: Optional[bool] = Field(None, description="", alias="isPublished")
        has_extracts: Optional[bool] = Field(None, description="", alias="hasExtracts")
        is_certified: Optional[bool] = Field(None, description="", alias="isCertified")
        certifier: Optional[dict[str, str]] = Field(
            None, description="", alias="certifier"
        )
        certification_note: Optional[str] = Field(
            None, description="", alias="certificationNote"
        )
        certifier_display_name: Optional[str] = Field(
            None, description="", alias="certifierDisplayName"
        )
        upstream_tables: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="upstreamTables"
        )
        upstream_datasources: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="upstreamDatasources"
        )
        workbook: Optional[TableauWorkbook] = Field(
            None, description="", alias="workbook"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        project: Optional[TableauProject] = Field(
            None, description="", alias="project"
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
        fields: Optional[list[TableauCalculatedField]] = Field(
            None, description="", alias="fields"
        )  # relationship
        fields: Optional[list[TableauDatasourceField]] = Field(
            None, description="", alias="fields"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "TableauDatasource.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauSite(Tableau):
    """Description"""


class TableauDashboard(Tableau):
    """Description"""

    type_name: Literal["TableauDashboard"]

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        workbook_qualified_name: Optional[str] = Field(
            None, description="", alias="workbookQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        workbook: Optional[TableauWorkbook] = Field(
            None, description="", alias="workbook"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        worksheets: Optional[list[TableauWorksheet]] = Field(
            None, description="", alias="worksheets"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "TableauDashboard.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauFlow(Tableau):
    """Description"""

    type_name: Literal["TableauFlow"]

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        input_fields: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="inputFields"
        )
        output_fields: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="outputFields"
        )
        output_steps: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="outputSteps"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        project: Optional[TableauProject] = Field(
            None, description="", alias="project"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "TableauFlow.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauWorksheet(Tableau):
    """Description"""

    type_name: Literal["TableauWorksheet"]

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        workbook_qualified_name: Optional[str] = Field(
            None, description="", alias="workbookQualifiedName"
        )
        workbook: Optional[TableauWorkbook] = Field(
            None, description="", alias="workbook"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        datasource_fields: Optional[list[TableauDatasourceField]] = Field(
            None, description="", alias="datasourceFields"
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
        calculated_fields: Optional[list[TableauCalculatedField]] = Field(
            None, description="", alias="calculatedFields"
        )  # relationship
        dashboards: Optional[list[TableauDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "TableauWorksheet.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerLook(Looker):
    """Description"""

    type_name: Literal["LookerLook"]

    class Attributes(Looker.Attributes):
        folder_name: Optional[str] = Field(None, description="", alias="folderName")
        source_user_id: Optional[int] = Field(
            None, description="", alias="sourceUserId"
        )
        source_view_count: Optional[int] = Field(
            None, description="", alias="sourceViewCount"
        )
        sourcelast_updater_id: Optional[int] = Field(
            None, description="", alias="sourcelastUpdaterId"
        )
        source_last_accessed_at: Optional[date] = Field(
            None, description="", alias="sourceLastAccessedAt"
        )
        source_last_viewed_at: Optional[date] = Field(
            None, description="", alias="sourceLastViewedAt"
        )
        source_content_metadata_id: Optional[int] = Field(
            None, description="", alias="sourceContentMetadataId"
        )
        source_query_id: Optional[int] = Field(
            None, description="", alias="sourceQueryId"
        )
        model_name: Optional[str] = Field(None, description="", alias="modelName")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        folder: Optional[LookerFolder] = Field(
            None, description="", alias="folder"
        )  # relationship
        query: Optional[LookerQuery] = Field(
            None, description="", alias="query"
        )  # relationship
        tile: Optional[LookerTile] = Field(
            None, description="", alias="tile"
        )  # relationship
        model: Optional[LookerModel] = Field(
            None, description="", alias="model"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        dashboard: Optional[LookerDashboard] = Field(
            None, description="", alias="dashboard"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "LookerLook.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerDashboard(Looker):
    """Description"""

    type_name: Literal["LookerDashboard"]

    class Attributes(Looker.Attributes):
        folder_name: Optional[str] = Field(None, description="", alias="folderName")
        source_user_id: Optional[int] = Field(
            None, description="", alias="sourceUserId"
        )
        source_view_count: Optional[int] = Field(
            None, description="", alias="sourceViewCount"
        )
        source_metadata_id: Optional[int] = Field(
            None, description="", alias="sourceMetadataId"
        )
        sourcelast_updater_id: Optional[int] = Field(
            None, description="", alias="sourcelastUpdaterId"
        )
        source_last_accessed_at: Optional[date] = Field(
            None, description="", alias="sourceLastAccessedAt"
        )
        source_last_viewed_at: Optional[date] = Field(
            None, description="", alias="sourceLastViewedAt"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        tiles: Optional[list[LookerTile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        looks: Optional[list[LookerLook]] = Field(
            None, description="", alias="looks"
        )  # relationship
        folder: Optional[LookerFolder] = Field(
            None, description="", alias="folder"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "LookerDashboard.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerFolder(Looker):
    """Description"""

    type_name: Literal["LookerFolder"]

    class Attributes(Looker.Attributes):
        source_content_metadata_id: Optional[int] = Field(
            None, description="", alias="sourceContentMetadataId"
        )
        source_creator_id: Optional[int] = Field(
            None, description="", alias="sourceCreatorId"
        )
        source_child_count: Optional[int] = Field(
            None, description="", alias="sourceChildCount"
        )
        source_parent_i_d: Optional[int] = Field(
            None, description="", alias="sourceParentID"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        looks: Optional[list[LookerLook]] = Field(
            None, description="", alias="looks"
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
        dashboards: Optional[list[LookerDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "LookerFolder.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerTile(Looker):
    """Description"""

    type_name: Literal["LookerTile"]

    class Attributes(Looker.Attributes):
        lookml_link_id: Optional[str] = Field(
            None, description="", alias="lookmlLinkId"
        )
        merge_result_id: Optional[str] = Field(
            None, description="", alias="mergeResultId"
        )
        note_text: Optional[str] = Field(None, description="", alias="noteText")
        query_i_d: Optional[int] = Field(None, description="", alias="queryID")
        result_maker_i_d: Optional[int] = Field(
            None, description="", alias="resultMakerID"
        )
        subtitle_text: Optional[str] = Field(None, description="", alias="subtitleText")
        look_id: Optional[int] = Field(None, description="", alias="lookId")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        query: Optional[LookerQuery] = Field(
            None, description="", alias="query"
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
        look: Optional[LookerLook] = Field(
            None, description="", alias="look"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        dashboard: Optional[LookerDashboard] = Field(
            None, description="", alias="dashboard"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "LookerTile.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerModel(Looker):
    """Description"""

    type_name: Literal["LookerModel"]

    class Attributes(Looker.Attributes):
        project_name: Optional[str] = Field(None, description="", alias="projectName")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        explores: Optional[list[LookerExplore]] = Field(
            None, description="", alias="explores"
        )  # relationship
        project: Optional[LookerProject] = Field(
            None, description="", alias="project"
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
        fields: Optional[list[LookerField]] = Field(
            None, description="", alias="fields"
        )  # relationship
        look: Optional[LookerLook] = Field(
            None, description="", alias="look"
        )  # relationship
        queries: Optional[list[LookerQuery]] = Field(
            None, description="", alias="queries"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "LookerModel.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerExplore(Looker):
    """Description"""

    type_name: Literal["LookerExplore"]

    class Attributes(Looker.Attributes):
        project_name: Optional[str] = Field(None, description="", alias="projectName")
        model_name: Optional[str] = Field(None, description="", alias="modelName")
        source_connection_name: Optional[str] = Field(
            None, description="", alias="sourceConnectionName"
        )
        view_name: Optional[str] = Field(None, description="", alias="viewName")
        sql_table_name: Optional[str] = Field(
            None, description="", alias="sqlTableName"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        project: Optional[LookerProject] = Field(
            None, description="", alias="project"
        )  # relationship
        model: Optional[LookerModel] = Field(
            None, description="", alias="model"
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
        fields: Optional[list[LookerField]] = Field(
            None, description="", alias="fields"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "LookerExplore.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerProject(Looker):
    """Description"""


class LookerQuery(Looker):
    """Description"""

    type_name: Literal["LookerQuery"]

    class Attributes(Looker.Attributes):
        source_definition: Optional[str] = Field(
            None, description="", alias="sourceDefinition"
        )
        source_definition_database: Optional[str] = Field(
            None, description="", alias="sourceDefinitionDatabase"
        )
        source_definition_schema: Optional[str] = Field(
            None, description="", alias="sourceDefinitionSchema"
        )
        fields: Optional[list[str]] = Field(None, description="", alias="fields")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        tiles: Optional[list[LookerTile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        looks: Optional[list[LookerLook]] = Field(
            None, description="", alias="looks"
        )  # relationship
        model: Optional[LookerModel] = Field(
            None, description="", alias="model"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "LookerQuery.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerField(Looker):
    """Description"""

    type_name: Literal["LookerField"]

    class Attributes(Looker.Attributes):
        project_name: Optional[str] = Field(None, description="", alias="projectName")
        looker_explore_qualified_name: Optional[str] = Field(
            None, description="", alias="lookerExploreQualifiedName"
        )
        looker_view_qualified_name: Optional[str] = Field(
            None, description="", alias="lookerViewQualifiedName"
        )
        model_name: Optional[str] = Field(None, description="", alias="modelName")
        source_definition: Optional[str] = Field(
            None, description="", alias="sourceDefinition"
        )
        looker_field_data_type: Optional[str] = Field(
            None, description="", alias="lookerFieldDataType"
        )
        looker_times_used: Optional[int] = Field(
            None, description="", alias="lookerTimesUsed"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        view: Optional[LookerView] = Field(
            None, description="", alias="view"
        )  # relationship
        explore: Optional[LookerExplore] = Field(
            None, description="", alias="explore"
        )  # relationship
        project: Optional[LookerProject] = Field(
            None, description="", alias="project"
        )  # relationship
        model: Optional[LookerModel] = Field(
            None, description="", alias="model"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "LookerField.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerView(Looker):
    """Description"""

    type_name: Literal["LookerView"]

    class Attributes(Looker.Attributes):
        project_name: Optional[str] = Field(None, description="", alias="projectName")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        project: Optional[LookerProject] = Field(
            None, description="", alias="project"
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
        fields: Optional[list[LookerField]] = Field(
            None, description="", alias="fields"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "LookerView.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceObject(Salesforce):
    """Description"""

    type_name: Literal["SalesforceObject"]

    class Attributes(Salesforce.Attributes):
        is_custom: Optional[bool] = Field(None, description="", alias="isCustom")
        is_mergable: Optional[bool] = Field(None, description="", alias="isMergable")
        is_queryable: Optional[bool] = Field(None, description="", alias="isQueryable")
        field_count: Optional[int] = Field(None, description="", alias="fieldCount")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        organization: Optional[SalesforceOrganization] = Field(
            None, description="", alias="organization"
        )  # relationship
        lookup_fields: Optional[list[SalesforceField]] = Field(
            None, description="", alias="lookupFields"
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
        fields: Optional[list[SalesforceField]] = Field(
            None, description="", alias="fields"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "SalesforceObject.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceField(Salesforce):
    """Description"""

    type_name: Literal["SalesforceField"]

    class Attributes(Salesforce.Attributes):
        data_type: Optional[str] = Field(None, description="", alias="dataType")
        object_qualified_name: Optional[str] = Field(
            None, description="", alias="objectQualifiedName"
        )
        order: Optional[int] = Field(None, description="", alias="order")
        inline_help_text: Optional[str] = Field(
            None, description="", alias="inlineHelpText"
        )
        is_calculated: Optional[bool] = Field(
            None, description="", alias="isCalculated"
        )
        formula: Optional[str] = Field(None, description="", alias="formula")
        is_case_sensitive: Optional[bool] = Field(
            None, description="", alias="isCaseSensitive"
        )
        is_encrypted: Optional[bool] = Field(None, description="", alias="isEncrypted")
        max_length: Optional[int] = Field(None, description="", alias="maxLength")
        is_nullable: Optional[bool] = Field(None, description="", alias="isNullable")
        precision: Optional[int] = Field(None, description="", alias="precision")
        numeric_scale: Optional[float] = Field(
            None, description="", alias="numericScale"
        )
        is_unique: Optional[bool] = Field(None, description="", alias="isUnique")
        picklist_values: Optional[list[str]] = Field(
            None, description="", alias="picklistValues"
        )
        is_polymorphic_foreign_key: Optional[bool] = Field(
            None, description="", alias="isPolymorphicForeignKey"
        )
        default_value_formula: Optional[str] = Field(
            None, description="", alias="defaultValueFormula"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        lookup_objects: Optional[list[SalesforceObject]] = Field(
            None, description="", alias="lookupObjects"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship
        object: Optional[SalesforceObject] = Field(
            None, description="", alias="object"
        )  # relationship

    attributes: "SalesforceField.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceOrganization(Salesforce):
    """Description"""

    type_name: Literal["SalesforceOrganization"]

    class Attributes(Salesforce.Attributes):
        source_id: Optional[str] = Field(None, description="", alias="sourceId")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        reports: Optional[list[SalesforceReport]] = Field(
            None, description="", alias="reports"
        )  # relationship
        objects: Optional[list[SalesforceObject]] = Field(
            None, description="", alias="objects"
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
        dashboards: Optional[list[SalesforceDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "SalesforceOrganization.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceDashboard(Salesforce):
    """Description"""

    type_name: Literal["SalesforceDashboard"]

    class Attributes(Salesforce.Attributes):
        source_id: Optional[str] = Field(None, description="", alias="sourceId")
        dashboard_type: Optional[str] = Field(
            None, description="", alias="dashboardType"
        )
        report_count: Optional[int] = Field(None, description="", alias="reportCount")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        reports: Optional[list[SalesforceReport]] = Field(
            None, description="", alias="reports"
        )  # relationship
        organization: Optional[SalesforceOrganization] = Field(
            None, description="", alias="organization"
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
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "SalesforceDashboard.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceReport(Salesforce):
    """Description"""

    type_name: Literal["SalesforceReport"]

    class Attributes(Salesforce.Attributes):
        source_id: Optional[str] = Field(None, description="", alias="sourceId")
        report_type: Optional[dict[str, str]] = Field(
            None, description="", alias="reportType"
        )
        detail_columns: Optional[list[str]] = Field(
            None, description="", alias="detailColumns"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        organization: Optional[SalesforceOrganization] = Field(
            None, description="", alias="organization"
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
        dashboards: Optional[list[SalesforceDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "SalesforceReport.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


Referenceable.update_forward_refs()
AtlasGlossary.update_forward_refs()

Referenceable.Attributes.update_forward_refs()

Asset.Attributes.update_forward_refs()

AtlasGlossary.Attributes.update_forward_refs()

DataSet.Attributes.update_forward_refs()

ProcessExecution.Attributes.update_forward_refs()

AtlasGlossaryTerm.Attributes.update_forward_refs()

Cloud.Attributes.update_forward_refs()

Infrastructure.Attributes.update_forward_refs()

Connection.Attributes.update_forward_refs()

Process.Attributes.update_forward_refs()

AtlasGlossaryCategory.Attributes.update_forward_refs()

Badge.Attributes.update_forward_refs()

Namespace.Attributes.update_forward_refs()

Catalog.Attributes.update_forward_refs()

Google.Attributes.update_forward_refs()

AWS.Attributes.update_forward_refs()

BIProcess.Attributes.update_forward_refs()

ColumnProcess.Attributes.update_forward_refs()

Collection.Attributes.update_forward_refs()

Folder.Attributes.update_forward_refs()

ObjectStore.Attributes.update_forward_refs()

DataQuality.Attributes.update_forward_refs()

BI.Attributes.update_forward_refs()

SaaS.Attributes.update_forward_refs()

Dbt.Attributes.update_forward_refs()

Resource.Attributes.update_forward_refs()

Insight.Attributes.update_forward_refs()

API.Attributes.update_forward_refs()

SQL.Attributes.update_forward_refs()

DataStudio.Attributes.update_forward_refs()

GCS.Attributes.update_forward_refs()

DataStudioAsset.Attributes.update_forward_refs()

S3.Attributes.update_forward_refs()

DbtColumnProcess.Attributes.update_forward_refs()

Metric.Attributes.update_forward_refs()

Metabase.Attributes.update_forward_refs()

PowerBI.Attributes.update_forward_refs()

Preset.Attributes.update_forward_refs()

Mode.Attributes.update_forward_refs()

Tableau.Attributes.update_forward_refs()

Looker.Attributes.update_forward_refs()

Salesforce.Attributes.update_forward_refs()

DbtModelColumn.Attributes.update_forward_refs()

DbtModel.Attributes.update_forward_refs()

DbtMetric.Attributes.update_forward_refs()

DbtSource.Attributes.update_forward_refs()

DbtProcess.Attributes.update_forward_refs()

ReadmeTemplate.Attributes.update_forward_refs()

Readme.Attributes.update_forward_refs()

Link.Attributes.update_forward_refs()

APISpec.Attributes.update_forward_refs()

APIPath.Attributes.update_forward_refs()

TablePartition.Attributes.update_forward_refs()

Table.Attributes.update_forward_refs()

Query.Attributes.update_forward_refs()

Column.Attributes.update_forward_refs()

Schema.Attributes.update_forward_refs()

Database.Attributes.update_forward_refs()

SnowflakeStream.Attributes.update_forward_refs()

SnowflakePipe.Attributes.update_forward_refs()

Procedure.Attributes.update_forward_refs()

View.Attributes.update_forward_refs()

MaterialisedView.Attributes.update_forward_refs()

GCSObject.Attributes.update_forward_refs()

GCSBucket.Attributes.update_forward_refs()

S3Bucket.Attributes.update_forward_refs()

S3Object.Attributes.update_forward_refs()

MetabaseQuestion.Attributes.update_forward_refs()

MetabaseCollection.Attributes.update_forward_refs()

MetabaseDashboard.Attributes.update_forward_refs()

PowerBIReport.Attributes.update_forward_refs()

PowerBIMeasure.Attributes.update_forward_refs()

PowerBIColumn.Attributes.update_forward_refs()

PowerBITile.Attributes.update_forward_refs()

PowerBITable.Attributes.update_forward_refs()

PowerBIDatasource.Attributes.update_forward_refs()

PowerBIWorkspace.Attributes.update_forward_refs()

PowerBIDataset.Attributes.update_forward_refs()

PowerBIDashboard.Attributes.update_forward_refs()

PowerBIPage.Attributes.update_forward_refs()

PowerBIDataflow.Attributes.update_forward_refs()

PresetChart.Attributes.update_forward_refs()

PresetDataset.Attributes.update_forward_refs()

PresetDashboard.Attributes.update_forward_refs()

PresetWorkspace.Attributes.update_forward_refs()

ModeReport.Attributes.update_forward_refs()

ModeQuery.Attributes.update_forward_refs()

ModeChart.Attributes.update_forward_refs()

ModeWorkspace.Attributes.update_forward_refs()

ModeCollection.Attributes.update_forward_refs()

TableauWorkbook.Attributes.update_forward_refs()

TableauDatasourceField.Attributes.update_forward_refs()

TableauCalculatedField.Attributes.update_forward_refs()

TableauProject.Attributes.update_forward_refs()

TableauMetric.Attributes.update_forward_refs()

TableauDatasource.Attributes.update_forward_refs()

TableauSite.Attributes.update_forward_refs()

TableauDashboard.Attributes.update_forward_refs()

TableauFlow.Attributes.update_forward_refs()

TableauWorksheet.Attributes.update_forward_refs()

LookerLook.Attributes.update_forward_refs()

LookerDashboard.Attributes.update_forward_refs()

LookerFolder.Attributes.update_forward_refs()

LookerTile.Attributes.update_forward_refs()

LookerModel.Attributes.update_forward_refs()

LookerExplore.Attributes.update_forward_refs()

LookerProject.Attributes.update_forward_refs()

LookerQuery.Attributes.update_forward_refs()

LookerField.Attributes.update_forward_refs()

LookerView.Attributes.update_forward_refs()

SalesforceObject.Attributes.update_forward_refs()

SalesforceField.Attributes.update_forward_refs()

SalesforceOrganization.Attributes.update_forward_refs()

SalesforceDashboard.Attributes.update_forward_refs()

SalesforceReport.Attributes.update_forward_refs()
