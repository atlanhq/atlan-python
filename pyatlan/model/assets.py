# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, TypeVar
from urllib.parse import quote, unquote

from pydantic import Field, StrictStr, root_validator, validator

from pyatlan.model.core import (
    Announcement,
    AtlanObject,
    Classification,
    CustomMetadata,
    Meaning,
)
from pyatlan.model.enums import (
    ADLSAccessTier,
    ADLSAccountStatus,
    ADLSEncryptionTypes,
    ADLSLeaseState,
    ADLSLeaseStatus,
    ADLSObjectArchiveStatus,
    ADLSObjectType,
    ADLSPerformance,
    ADLSProvisionState,
    ADLSReplicationType,
    ADLSStorageKind,
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    EntityStatus,
    GoogleDatastudioAssetType,
    IconType,
    KafkaTopicCompressionType,
    PowerbiEndorsement,
    QueryUsernameStrategy,
    QuickSightAnalysisStatus,
    QuickSightDatasetFieldType,
    QuickSightDatasetImportMode,
    QuickSightFolderType,
    SourceCostUnitType,
)
from pyatlan.model.internal import AtlasServer, Internal
from pyatlan.model.structs import (
    AwsTag,
    AzureTag,
    BadgeCondition,
    ColumnValueFrequencyMap,
    DbtMetricFilter,
    GoogleLabel,
    GoogleTag,
    Histogram,
    KafkaTopicConsumption,
    PopularityInsights,
)
from pyatlan.utils import next_id


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


def validate_required_fields(field_names: list[str], values: list[Any]):
    for field_name, value in zip(field_names, values):
        if value is None:
            raise ValueError(f"{field_name} is required")
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{field_name} cannot be blank")


SelfAsset = TypeVar("SelfAsset", bound="Asset")


class Referenceable(AtlanObject):
    """Description"""

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__.__fields_set__.add("type_name")

    def __setattr__(self, name, value):
        if name in Referenceable._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "qualified_name",
        "replicated_from",
        "replicated_to",
        "terms",
    ]

    @property
    def qualified_name(self) -> str:
        return self.attributes.qualified_name

    @qualified_name.setter
    def qualified_name(self, qualified_name: str):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qualified_name = qualified_name

    @property
    def replicated_from(self) -> Optional[list[AtlasServer]]:
        return self.attributes.replicated_from

    @replicated_from.setter
    def replicated_from(self, replicated_from: Optional[list[AtlasServer]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.replicated_from = replicated_from

    @property
    def replicated_to(self) -> Optional[list[AtlasServer]]:
        return self.attributes.replicated_to

    @replicated_to.setter
    def replicated_to(self, replicated_to: Optional[list[AtlasServer]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.replicated_to = replicated_to

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    class Attributes(AtlanObject):
        qualified_name: str = Field("", description="", alias="qualifiedName")
        replicated_from: Optional[list[AtlasServer]] = Field(
            None, description="", alias="replicatedFrom"
        )
        replicated_to: Optional[list[AtlasServer]] = Field(
            None, description="", alias="replicatedTo"
        )
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship

        def validate_required(self):
            pass

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
    type_name: str = Field(
        None, description="Name of the type definition that defines this instance.\n"
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
    meanings: Optional[list[Meaning]] = Field(None, description="", alias="meanings")
    custom_attributes: Optional[dict[str, Any]] = Field(
        None, description="", alias="customAttributes"
    )
    scrubbed: Optional[bool] = Field(
        None, description="", alias="fields removed from results"
    )
    pending_tasks: Optional[list[str]] = Field(None)

    unique_attributes: Optional[dict[str, Any]] = Field(None)

    def validate_required(self):
        if not self.create_time or self.created_by:
            self.attributes.validate_required()

    def get_custom_metadata(self, name: str) -> CustomMetadata:
        from pyatlan.cache.custom_metadata_cache import CustomMetadataCache

        ba_id = CustomMetadataCache.get_id_for_name(name)
        if ba_id is None:
            raise ValueError(f"No custom metadata with the name: {name} exist")
        for a_type in CustomMetadataCache.types_by_asset[self.type_name]:
            if (
                hasattr(a_type, "_meta_data_type_name")
                and a_type._meta_data_type_name == name
            ):
                break
        else:
            raise ValueError(
                f"Custom metadata attributes {name} are not applicable to {self.type_name}"
            )
        if ba_type := CustomMetadataCache.get_type_for_id(ba_id):
            return (
                ba_type(self.business_attributes[ba_id])
                if self.business_attributes and ba_id in self.business_attributes
                else ba_type()
            )
        else:
            raise ValueError(
                f"Custom metadata attributes {name} are not applicable to {self.type_name}"
            )

    def set_custom_metadata(self, custom_metadata: CustomMetadata) -> None:
        from pyatlan.cache.custom_metadata_cache import CustomMetadataCache

        if not isinstance(custom_metadata, CustomMetadata):
            raise ValueError(
                "business_attributes must be an instance of CustomMetadata"
            )
        if (
            type(custom_metadata)
            not in CustomMetadataCache.types_by_asset[self.type_name]
        ):
            raise ValueError(
                f"Business attributes {custom_metadata._meta_data_type_name} are not applicable to {self.type_name}"
            )
        ba_dict = dict(custom_metadata)
        if not self.business_attributes:
            self.business_attributes = {}
        self.business_attributes[custom_metadata._meta_data_type_id] = ba_dict


class Asset(Referenceable):
    """Description"""

    def __setattr__(self, name, value):
        if name in Asset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
        "terms",
    ]

    @property
    def name(self) -> str:
        return self.attributes.name

    @name.setter
    def name(self, name: str):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.name = name

    @property
    def display_name(self) -> Optional[str]:
        return self.attributes.display_name

    @display_name.setter
    def display_name(self, display_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.display_name = display_name

    @property
    def description(self) -> Optional[str]:
        return self.attributes.description

    @description.setter
    def description(self, description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.description = description

    @property
    def user_description(self) -> Optional[str]:
        return self.attributes.user_description

    @user_description.setter
    def user_description(self, user_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.user_description = user_description

    @property
    def tenant_id(self) -> Optional[str]:
        return self.attributes.tenant_id

    @tenant_id.setter
    def tenant_id(self, tenant_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tenant_id = tenant_id

    @property
    def certificate_status(self) -> Optional[CertificateStatus]:
        return self.attributes.certificate_status

    @certificate_status.setter
    def certificate_status(self, certificate_status: Optional[CertificateStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certificate_status = certificate_status

    @property
    def certificate_status_message(self) -> Optional[str]:
        return self.attributes.certificate_status_message

    @certificate_status_message.setter
    def certificate_status_message(self, certificate_status_message: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certificate_status_message = certificate_status_message

    @property
    def certificate_updated_by(self) -> Optional[str]:
        return self.attributes.certificate_updated_by

    @certificate_updated_by.setter
    def certificate_updated_by(self, certificate_updated_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certificate_updated_by = certificate_updated_by

    @property
    def certificate_updated_at(self) -> Optional[datetime]:
        return self.attributes.certificate_updated_at

    @certificate_updated_at.setter
    def certificate_updated_at(self, certificate_updated_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certificate_updated_at = certificate_updated_at

    @property
    def announcement_title(self) -> Optional[str]:
        return self.attributes.announcement_title

    @announcement_title.setter
    def announcement_title(self, announcement_title: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.announcement_title = announcement_title

    @property
    def announcement_message(self) -> Optional[str]:
        return self.attributes.announcement_message

    @announcement_message.setter
    def announcement_message(self, announcement_message: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.announcement_message = announcement_message

    @property
    def announcement_type(self) -> Optional[str]:
        return self.attributes.announcement_type

    @announcement_type.setter
    def announcement_type(self, announcement_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.announcement_type = announcement_type

    @property
    def announcement_updated_at(self) -> Optional[datetime]:
        return self.attributes.announcement_updated_at

    @announcement_updated_at.setter
    def announcement_updated_at(self, announcement_updated_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.announcement_updated_at = announcement_updated_at

    @property
    def announcement_updated_by(self) -> Optional[str]:
        return self.attributes.announcement_updated_by

    @announcement_updated_by.setter
    def announcement_updated_by(self, announcement_updated_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.announcement_updated_by = announcement_updated_by

    @property
    def owner_users(self) -> Optional[set[str]]:
        return self.attributes.owner_users

    @owner_users.setter
    def owner_users(self, owner_users: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.owner_users = owner_users

    @property
    def owner_groups(self) -> Optional[set[str]]:
        return self.attributes.owner_groups

    @owner_groups.setter
    def owner_groups(self, owner_groups: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.owner_groups = owner_groups

    @property
    def admin_users(self) -> Optional[set[str]]:
        return self.attributes.admin_users

    @admin_users.setter
    def admin_users(self, admin_users: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.admin_users = admin_users

    @property
    def admin_groups(self) -> Optional[set[str]]:
        return self.attributes.admin_groups

    @admin_groups.setter
    def admin_groups(self, admin_groups: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.admin_groups = admin_groups

    @property
    def viewer_users(self) -> Optional[set[str]]:
        return self.attributes.viewer_users

    @viewer_users.setter
    def viewer_users(self, viewer_users: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.viewer_users = viewer_users

    @property
    def viewer_groups(self) -> Optional[set[str]]:
        return self.attributes.viewer_groups

    @viewer_groups.setter
    def viewer_groups(self, viewer_groups: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.viewer_groups = viewer_groups

    @property
    def connector_name(self) -> Optional[str]:
        return self.attributes.connector_name

    @connector_name.setter
    def connector_name(self, connector_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connector_name = connector_name

    @property
    def connection_name(self) -> Optional[str]:
        return self.attributes.connection_name

    @connection_name.setter
    def connection_name(self, connection_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connection_name = connection_name

    @property
    def connection_qualified_name(self) -> Optional[str]:
        return self.attributes.connection_qualified_name

    @connection_qualified_name.setter
    def connection_qualified_name(self, connection_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connection_qualified_name = connection_qualified_name

    @property
    def has_lineage(self) -> Optional[bool]:
        return self.attributes.has_lineage

    @has_lineage.setter
    def has_lineage(self, has_lineage: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.has_lineage = has_lineage

    @property
    def is_discoverable(self) -> Optional[bool]:
        return self.attributes.is_discoverable

    @is_discoverable.setter
    def is_discoverable(self, is_discoverable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_discoverable = is_discoverable

    @property
    def is_editable(self) -> Optional[bool]:
        return self.attributes.is_editable

    @is_editable.setter
    def is_editable(self, is_editable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_editable = is_editable

    @property
    def sub_type(self) -> Optional[str]:
        return self.attributes.sub_type

    @sub_type.setter
    def sub_type(self, sub_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sub_type = sub_type

    @property
    def view_score(self) -> Optional[float]:
        return self.attributes.view_score

    @view_score.setter
    def view_score(self, view_score: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_score = view_score

    @property
    def popularity_score(self) -> Optional[float]:
        return self.attributes.popularity_score

    @popularity_score.setter
    def popularity_score(self, popularity_score: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.popularity_score = popularity_score

    @property
    def source_owners(self) -> Optional[str]:
        return self.attributes.source_owners

    @source_owners.setter
    def source_owners(self, source_owners: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_owners = source_owners

    @property
    def source_created_by(self) -> Optional[str]:
        return self.attributes.source_created_by

    @source_created_by.setter
    def source_created_by(self, source_created_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_created_by = source_created_by

    @property
    def source_created_at(self) -> Optional[datetime]:
        return self.attributes.source_created_at

    @source_created_at.setter
    def source_created_at(self, source_created_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_created_at = source_created_at

    @property
    def source_updated_at(self) -> Optional[datetime]:
        return self.attributes.source_updated_at

    @source_updated_at.setter
    def source_updated_at(self, source_updated_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_updated_at = source_updated_at

    @property
    def source_updated_by(self) -> Optional[str]:
        return self.attributes.source_updated_by

    @source_updated_by.setter
    def source_updated_by(self, source_updated_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_updated_by = source_updated_by

    @property
    def source_url(self) -> Optional[str]:
        return self.attributes.source_url

    @source_url.setter
    def source_url(self, source_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_url = source_url

    @property
    def source_embed_url(self) -> Optional[str]:
        return self.attributes.source_embed_url

    @source_embed_url.setter
    def source_embed_url(self, source_embed_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_embed_url = source_embed_url

    @property
    def last_sync_workflow_name(self) -> Optional[str]:
        return self.attributes.last_sync_workflow_name

    @last_sync_workflow_name.setter
    def last_sync_workflow_name(self, last_sync_workflow_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_sync_workflow_name = last_sync_workflow_name

    @property
    def last_sync_run_at(self) -> Optional[datetime]:
        return self.attributes.last_sync_run_at

    @last_sync_run_at.setter
    def last_sync_run_at(self, last_sync_run_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_sync_run_at = last_sync_run_at

    @property
    def last_sync_run(self) -> Optional[str]:
        return self.attributes.last_sync_run

    @last_sync_run.setter
    def last_sync_run(self, last_sync_run: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_sync_run = last_sync_run

    @property
    def admin_roles(self) -> Optional[set[str]]:
        return self.attributes.admin_roles

    @admin_roles.setter
    def admin_roles(self, admin_roles: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.admin_roles = admin_roles

    @property
    def source_read_count(self) -> Optional[int]:
        return self.attributes.source_read_count

    @source_read_count.setter
    def source_read_count(self, source_read_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_count = source_read_count

    @property
    def source_read_user_count(self) -> Optional[int]:
        return self.attributes.source_read_user_count

    @source_read_user_count.setter
    def source_read_user_count(self, source_read_user_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_user_count = source_read_user_count

    @property
    def source_last_read_at(self) -> Optional[datetime]:
        return self.attributes.source_last_read_at

    @source_last_read_at.setter
    def source_last_read_at(self, source_last_read_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_last_read_at = source_last_read_at

    @property
    def last_row_changed_at(self) -> Optional[datetime]:
        return self.attributes.last_row_changed_at

    @last_row_changed_at.setter
    def last_row_changed_at(self, last_row_changed_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_row_changed_at = last_row_changed_at

    @property
    def source_total_cost(self) -> Optional[float]:
        return self.attributes.source_total_cost

    @source_total_cost.setter
    def source_total_cost(self, source_total_cost: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_total_cost = source_total_cost

    @property
    def source_cost_unit(self) -> Optional[SourceCostUnitType]:
        return self.attributes.source_cost_unit

    @source_cost_unit.setter
    def source_cost_unit(self, source_cost_unit: Optional[SourceCostUnitType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_cost_unit = source_cost_unit

    @property
    def source_read_recent_user_list(self) -> Optional[set[str]]:
        return self.attributes.source_read_recent_user_list

    @source_read_recent_user_list.setter
    def source_read_recent_user_list(
        self, source_read_recent_user_list: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_recent_user_list = source_read_recent_user_list

    @property
    def source_read_recent_user_record_list(self) -> Optional[list[PopularityInsights]]:
        return self.attributes.source_read_recent_user_record_list

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
        return self.attributes.source_read_top_user_list

    @source_read_top_user_list.setter
    def source_read_top_user_list(self, source_read_top_user_list: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_read_top_user_list = source_read_top_user_list

    @property
    def source_read_top_user_record_list(self) -> Optional[list[PopularityInsights]]:
        return self.attributes.source_read_top_user_record_list

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
        return self.attributes.source_read_popular_query_record_list

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
        return self.attributes.source_read_expensive_query_record_list

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
        return self.attributes.source_read_slow_query_record_list

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
        return self.attributes.source_query_compute_cost_list

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
        return self.attributes.source_query_compute_cost_record_list

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
        return self.attributes.dbt_qualified_name

    @dbt_qualified_name.setter
    def dbt_qualified_name(self, dbt_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_qualified_name = dbt_qualified_name

    @property
    def asset_dbt_alias(self) -> Optional[str]:
        return self.attributes.asset_dbt_alias

    @asset_dbt_alias.setter
    def asset_dbt_alias(self, asset_dbt_alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_alias = asset_dbt_alias

    @property
    def asset_dbt_meta(self) -> Optional[str]:
        return self.attributes.asset_dbt_meta

    @asset_dbt_meta.setter
    def asset_dbt_meta(self, asset_dbt_meta: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_meta = asset_dbt_meta

    @property
    def asset_dbt_unique_id(self) -> Optional[str]:
        return self.attributes.asset_dbt_unique_id

    @asset_dbt_unique_id.setter
    def asset_dbt_unique_id(self, asset_dbt_unique_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_unique_id = asset_dbt_unique_id

    @property
    def asset_dbt_account_name(self) -> Optional[str]:
        return self.attributes.asset_dbt_account_name

    @asset_dbt_account_name.setter
    def asset_dbt_account_name(self, asset_dbt_account_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_account_name = asset_dbt_account_name

    @property
    def asset_dbt_project_name(self) -> Optional[str]:
        return self.attributes.asset_dbt_project_name

    @asset_dbt_project_name.setter
    def asset_dbt_project_name(self, asset_dbt_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_project_name = asset_dbt_project_name

    @property
    def asset_dbt_package_name(self) -> Optional[str]:
        return self.attributes.asset_dbt_package_name

    @asset_dbt_package_name.setter
    def asset_dbt_package_name(self, asset_dbt_package_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_package_name = asset_dbt_package_name

    @property
    def asset_dbt_job_name(self) -> Optional[str]:
        return self.attributes.asset_dbt_job_name

    @asset_dbt_job_name.setter
    def asset_dbt_job_name(self, asset_dbt_job_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_name = asset_dbt_job_name

    @property
    def asset_dbt_job_schedule(self) -> Optional[str]:
        return self.attributes.asset_dbt_job_schedule

    @asset_dbt_job_schedule.setter
    def asset_dbt_job_schedule(self, asset_dbt_job_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_schedule = asset_dbt_job_schedule

    @property
    def asset_dbt_job_status(self) -> Optional[str]:
        return self.attributes.asset_dbt_job_status

    @asset_dbt_job_status.setter
    def asset_dbt_job_status(self, asset_dbt_job_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_status = asset_dbt_job_status

    @property
    def asset_dbt_job_schedule_cron_humanized(self) -> Optional[str]:
        return self.attributes.asset_dbt_job_schedule_cron_humanized

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
        return self.attributes.asset_dbt_job_last_run

    @asset_dbt_job_last_run.setter
    def asset_dbt_job_last_run(self, asset_dbt_job_last_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run = asset_dbt_job_last_run

    @property
    def asset_dbt_job_last_run_url(self) -> Optional[str]:
        return self.attributes.asset_dbt_job_last_run_url

    @asset_dbt_job_last_run_url.setter
    def asset_dbt_job_last_run_url(self, asset_dbt_job_last_run_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_url = asset_dbt_job_last_run_url

    @property
    def asset_dbt_job_last_run_created_at(self) -> Optional[datetime]:
        return self.attributes.asset_dbt_job_last_run_created_at

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
        return self.attributes.asset_dbt_job_last_run_updated_at

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
        return self.attributes.asset_dbt_job_last_run_dequed_at

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
        return self.attributes.asset_dbt_job_last_run_started_at

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
        return self.attributes.asset_dbt_job_last_run_total_duration

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
        return self.attributes.asset_dbt_job_last_run_total_duration_humanized

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
        return self.attributes.asset_dbt_job_last_run_queued_duration

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
        return self.attributes.asset_dbt_job_last_run_queued_duration_humanized

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
        return self.attributes.asset_dbt_job_last_run_run_duration

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
        return self.attributes.asset_dbt_job_last_run_run_duration_humanized

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
        return self.attributes.asset_dbt_job_last_run_git_branch

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
        return self.attributes.asset_dbt_job_last_run_git_sha

    @asset_dbt_job_last_run_git_sha.setter
    def asset_dbt_job_last_run_git_sha(
        self, asset_dbt_job_last_run_git_sha: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_last_run_git_sha = asset_dbt_job_last_run_git_sha

    @property
    def asset_dbt_job_last_run_status_message(self) -> Optional[str]:
        return self.attributes.asset_dbt_job_last_run_status_message

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
        return self.attributes.asset_dbt_job_last_run_owner_thread_id

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
        return self.attributes.asset_dbt_job_last_run_executed_by_thread_id

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
        return self.attributes.asset_dbt_job_last_run_artifacts_saved

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
        return self.attributes.asset_dbt_job_last_run_artifact_s3_path

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
        return self.attributes.asset_dbt_job_last_run_has_docs_generated

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
        return self.attributes.asset_dbt_job_last_run_has_sources_generated

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
        return self.attributes.asset_dbt_job_last_run_notifications_sent

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
        return self.attributes.asset_dbt_job_next_run

    @asset_dbt_job_next_run.setter
    def asset_dbt_job_next_run(self, asset_dbt_job_next_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_job_next_run = asset_dbt_job_next_run

    @property
    def asset_dbt_job_next_run_humanized(self) -> Optional[str]:
        return self.attributes.asset_dbt_job_next_run_humanized

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
        return self.attributes.asset_dbt_environment_name

    @asset_dbt_environment_name.setter
    def asset_dbt_environment_name(self, asset_dbt_environment_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_environment_name = asset_dbt_environment_name

    @property
    def asset_dbt_environment_dbt_version(self) -> Optional[str]:
        return self.attributes.asset_dbt_environment_dbt_version

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
        return self.attributes.asset_dbt_tags

    @asset_dbt_tags.setter
    def asset_dbt_tags(self, asset_dbt_tags: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_dbt_tags = asset_dbt_tags

    @property
    def asset_dbt_semantic_layer_proxy_url(self) -> Optional[str]:
        return self.attributes.asset_dbt_semantic_layer_proxy_url

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
        return self.attributes.asset_dbt_source_freshness_criteria

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
        return self.attributes.sample_data_url

    @sample_data_url.setter
    def sample_data_url(self, sample_data_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sample_data_url = sample_data_url

    @property
    def asset_tags(self) -> Optional[set[str]]:
        return self.attributes.asset_tags

    @asset_tags.setter
    def asset_tags(self, asset_tags: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_tags = asset_tags

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    _subtypes_: dict[str, type] = dict()

    def __init_subclass__(cls, type_name=None):
        cls._subtypes_[type_name or cls.__name__.lower()] = cls

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
            attributes=cls.Attributes(qualified_name=qualified_name)
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
            sub = getattr(sys.modules[__name__], data_type)

        if sub is None:
            raise TypeError(f"Unsupport sub-type: {data_type}")

        return sub(**data)

    type_name: str = Field("Asset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Asset":
            raise ValueError("must be Asset")
        return v

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
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )

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


class AtlasGlossary(Asset, type_name="AtlasGlossary"):
    """Description"""

    def __setattr__(self, name, value):
        if name in AtlasGlossary._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "short_description",
        "long_description",
        "language",
        "usage",
        "additional_attributes",
        "terms",
    ]

    @property
    def short_description(self) -> Optional[str]:
        return self.attributes.short_description

    @short_description.setter
    def short_description(self, short_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.short_description = short_description

    @property
    def long_description(self) -> Optional[str]:
        return self.attributes.long_description

    @long_description.setter
    def long_description(self, long_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.long_description = long_description

    @property
    def language(self) -> Optional[str]:
        return self.attributes.language

    @language.setter
    def language(self, language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.language = language

    @property
    def usage(self) -> Optional[str]:
        return self.attributes.usage

    @usage.setter
    def usage(self, usage: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.usage = usage

    @property
    def additional_attributes(self) -> Optional[dict[str, str]]:
        return self.attributes.additional_attributes

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.additional_attributes = additional_attributes

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("AtlasGlossary", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlasGlossary":
            raise ValueError("must be AtlasGlossary")
        return v

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

        @classmethod
        # @validate_arguments()
        def create(cls, *, name: StrictStr) -> AtlasGlossary.Attributes:
            validate_required_fields(["name"], [name])
            return AtlasGlossary.Attributes(name=name, qualified_name=next_id())

    attributes: "AtlasGlossary.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )

    @root_validator()
    def update_qualified_name(cls, values):
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


class DataSet(Asset, type_name="DataSet"):
    """Description"""

    def __setattr__(self, name, value):
        if name in DataSet._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("DataSet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataSet":
            raise ValueError("must be DataSet")
        return v

    class Attributes(Asset.Attributes):
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

    attributes: "DataSet.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ProcessExecution(Asset, type_name="ProcessExecution"):
    """Description"""

    def __setattr__(self, name, value):
        if name in ProcessExecution._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ProcessExecution", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ProcessExecution":
            raise ValueError("must be ProcessExecution")
        return v

    class Attributes(Asset.Attributes):
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

    attributes: "ProcessExecution.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AtlasGlossaryTerm(Asset, type_name="AtlasGlossaryTerm"):
    """Description"""

    def __setattr__(self, name, value):
        if name in AtlasGlossaryTerm._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "short_description",
        "long_description",
        "examples",
        "abbreviation",
        "usage",
        "additional_attributes",
        "terms",
    ]

    @property
    def short_description(self) -> Optional[str]:
        return self.attributes.short_description

    @short_description.setter
    def short_description(self, short_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.short_description = short_description

    @property
    def long_description(self) -> Optional[str]:
        return self.attributes.long_description

    @long_description.setter
    def long_description(self, long_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.long_description = long_description

    @property
    def examples(self) -> Optional[set[str]]:
        return self.attributes.examples

    @examples.setter
    def examples(self, examples: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.examples = examples

    @property
    def abbreviation(self) -> Optional[str]:
        return self.attributes.abbreviation

    @abbreviation.setter
    def abbreviation(self, abbreviation: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.abbreviation = abbreviation

    @property
    def usage(self) -> Optional[str]:
        return self.attributes.usage

    @usage.setter
    def usage(self, usage: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.usage = usage

    @property
    def additional_attributes(self) -> Optional[dict[str, str]]:
        return self.attributes.additional_attributes

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.additional_attributes = additional_attributes

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("AtlasGlossaryTerm", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlasGlossaryTerm":
            raise ValueError("must be AtlasGlossaryTerm")
        return v

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
        classifies: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="classifies"
        )  # relationship
        categories: Optional[list[AtlasGlossaryCategory]] = Field(
            None, description="", alias="categories"
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
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )

    @root_validator()
    def update_qualified_name(cls, values):
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


class Cloud(Asset, type_name="Cloud"):
    """Description"""

    def __setattr__(self, name, value):
        if name in Cloud._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Cloud", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Cloud":
            raise ValueError("must be Cloud")
        return v

    class Attributes(Asset.Attributes):
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

    attributes: "Cloud.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Infrastructure(Asset, type_name="Infrastructure"):
    """Description"""

    def __setattr__(self, name, value):
        if name in Infrastructure._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Infrastructure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Infrastructure":
            raise ValueError("must be Infrastructure")
        return v

    class Attributes(Asset.Attributes):
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

    attributes: "Infrastructure.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Connection(Asset, type_name="Connection"):
    """Description"""

    def __setattr__(self, name, value):
        if name in Connection._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "category",
        "sub_category",
        "host",
        "port",
        "allow_query",
        "allow_query_preview",
        "query_preview_config",
        "query_config",
        "credential_strategy",
        "preview_credential_strategy",
        "policy_strategy",
        "query_username_strategy",
        "row_limit",
        "default_credential_guid",
        "connector_icon",
        "connector_image",
        "source_logo",
        "is_sample_data_preview_enabled",
        "popularity_insights_timeframe",
        "has_popularity_insights",
        "connection_dbt_environments",
        "terms",
    ]

    @property
    def category(self) -> Optional[str]:
        return self.attributes.category

    @category.setter
    def category(self, category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.category = category

    @property
    def sub_category(self) -> Optional[str]:
        return self.attributes.sub_category

    @sub_category.setter
    def sub_category(self, sub_category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sub_category = sub_category

    @property
    def host(self) -> Optional[str]:
        return self.attributes.host

    @host.setter
    def host(self, host: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.host = host

    @property
    def port(self) -> Optional[int]:
        return self.attributes.port

    @port.setter
    def port(self, port: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.port = port

    @property
    def allow_query(self) -> Optional[bool]:
        return self.attributes.allow_query

    @allow_query.setter
    def allow_query(self, allow_query: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.allow_query = allow_query

    @property
    def allow_query_preview(self) -> Optional[bool]:
        return self.attributes.allow_query_preview

    @allow_query_preview.setter
    def allow_query_preview(self, allow_query_preview: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.allow_query_preview = allow_query_preview

    @property
    def query_preview_config(self) -> Optional[dict[str, str]]:
        return self.attributes.query_preview_config

    @query_preview_config.setter
    def query_preview_config(self, query_preview_config: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_preview_config = query_preview_config

    @property
    def query_config(self) -> Optional[str]:
        return self.attributes.query_config

    @query_config.setter
    def query_config(self, query_config: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_config = query_config

    @property
    def credential_strategy(self) -> Optional[str]:
        return self.attributes.credential_strategy

    @credential_strategy.setter
    def credential_strategy(self, credential_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.credential_strategy = credential_strategy

    @property
    def preview_credential_strategy(self) -> Optional[str]:
        return self.attributes.preview_credential_strategy

    @preview_credential_strategy.setter
    def preview_credential_strategy(self, preview_credential_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preview_credential_strategy = preview_credential_strategy

    @property
    def policy_strategy(self) -> Optional[str]:
        return self.attributes.policy_strategy

    @policy_strategy.setter
    def policy_strategy(self, policy_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_strategy = policy_strategy

    @property
    def query_username_strategy(self) -> Optional[QueryUsernameStrategy]:
        return self.attributes.query_username_strategy

    @query_username_strategy.setter
    def query_username_strategy(
        self, query_username_strategy: Optional[QueryUsernameStrategy]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_username_strategy = query_username_strategy

    @property
    def row_limit(self) -> Optional[int]:
        return self.attributes.row_limit

    @row_limit.setter
    def row_limit(self, row_limit: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.row_limit = row_limit

    @property
    def default_credential_guid(self) -> Optional[str]:
        return self.attributes.default_credential_guid

    @default_credential_guid.setter
    def default_credential_guid(self, default_credential_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.default_credential_guid = default_credential_guid

    @property
    def connector_icon(self) -> Optional[str]:
        return self.attributes.connector_icon

    @connector_icon.setter
    def connector_icon(self, connector_icon: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connector_icon = connector_icon

    @property
    def connector_image(self) -> Optional[str]:
        return self.attributes.connector_image

    @connector_image.setter
    def connector_image(self, connector_image: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connector_image = connector_image

    @property
    def source_logo(self) -> Optional[str]:
        return self.attributes.source_logo

    @source_logo.setter
    def source_logo(self, source_logo: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_logo = source_logo

    @property
    def is_sample_data_preview_enabled(self) -> Optional[bool]:
        return self.attributes.is_sample_data_preview_enabled

    @is_sample_data_preview_enabled.setter
    def is_sample_data_preview_enabled(
        self, is_sample_data_preview_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_sample_data_preview_enabled = is_sample_data_preview_enabled

    @property
    def popularity_insights_timeframe(self) -> Optional[int]:
        return self.attributes.popularity_insights_timeframe

    @popularity_insights_timeframe.setter
    def popularity_insights_timeframe(
        self, popularity_insights_timeframe: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.popularity_insights_timeframe = popularity_insights_timeframe

    @property
    def has_popularity_insights(self) -> Optional[bool]:
        return self.attributes.has_popularity_insights

    @has_popularity_insights.setter
    def has_popularity_insights(self, has_popularity_insights: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.has_popularity_insights = has_popularity_insights

    @property
    def connection_dbt_environments(self) -> Optional[set[str]]:
        return self.attributes.connection_dbt_environments

    @connection_dbt_environments.setter
    def connection_dbt_environments(
        self, connection_dbt_environments: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connection_dbt_environments = connection_dbt_environments

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Connection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Connection":
            raise ValueError("must be Connection")
        return v

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
        policy_strategy: Optional[str] = Field(
            None, description="", alias="policyStrategy"
        )
        query_username_strategy: Optional[QueryUsernameStrategy] = Field(
            None, description="", alias="queryUsernameStrategy"
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
        is_sample_data_preview_enabled: Optional[bool] = Field(
            None, description="", alias="isSampleDataPreviewEnabled"
        )
        popularity_insights_timeframe: Optional[int] = Field(
            None, description="", alias="popularityInsightsTimeframe"
        )
        has_popularity_insights: Optional[bool] = Field(
            None, description="", alias="hasPopularityInsights"
        )
        connection_dbt_environments: Optional[set[str]] = Field(
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

        def validate_required(self):
            if not self.name:
                raise ValueError("name is required")
            if not self.admin_roles and not self.admin_groups and not self.admin_users:
                raise ValueError(
                    "One of admin_user, admin_groups or admin_roles is required"
                )
            if not self.qualified_name:
                raise ValueError("qualified_name is required")
            if not self.category:
                raise ValueError("category is required")
            if not self.connector_name:
                raise ValueError("connector_name is required")

        @classmethod
        # @validate_arguments()
        def create(
            cls,
            *,
            name: str,
            connector_type: AtlanConnectorType,
            admin_users: Optional[list[str]] = None,
            admin_groups: Optional[list[str]] = None,
            admin_roles: Optional[list[str]] = None,
        ) -> Connection.Attributes:
            if not name:
                raise ValueError("name cannot be blank")
            validate_required_fields(["connector_type"], [connector_type])
            if admin_users or admin_groups or admin_roles:
                return cls(
                    name=name,
                    qualified_name=connector_type.to_qualified_name(),
                    connector_name=connector_type.value,
                    category=connector_type.category.value,
                    admin_users=admin_users,
                    admin_groups=admin_groups,
                    admin_roles=admin_roles,
                )
            else:
                raise ValueError(
                    "One of admin_user, admin_groups or admin_roles is required"
                )

    attributes: "Connection.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )

    @classmethod
    # @validate_arguments()
    def create(
        cls,
        *,
        name: str,
        connector_type: AtlanConnectorType,
        admin_users: Optional[list[str]] = None,
        admin_groups: Optional[list[str]] = None,
        admin_roles: Optional[list[str]] = None,
    ) -> Connection:
        if not name:
            raise ValueError("name cannot be blank")
        validate_required_fields(["connector_type"], [connector_type])
        if admin_users or admin_groups or admin_roles:
            attr = cls.Attributes(
                name=name,
                qualified_name=connector_type.to_qualified_name(),
                connector_name=connector_type.value,
                category=connector_type.category.value,
                admin_users=admin_users,
                admin_groups=admin_groups,
                admin_roles=admin_roles,
            )
            return cls(attributes=attr)
        else:
            raise ValueError(
                "One of admin_user, admin_groups or admin_roles is required"
            )


class Process(Asset, type_name="Process"):
    """Description"""

    def __setattr__(self, name, value):
        if name in Process._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "inputs",
        "outputs",
        "code",
        "sql",
        "ast",
        "terms",
    ]

    @property
    def inputs(self) -> Optional[list[Catalog]]:
        return self.attributes.inputs

    @inputs.setter
    def inputs(self, inputs: Optional[list[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inputs = inputs

    @property
    def outputs(self) -> Optional[list[Catalog]]:
        return self.attributes.outputs

    @outputs.setter
    def outputs(self, outputs: Optional[list[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.outputs = outputs

    @property
    def code(self) -> Optional[str]:
        return self.attributes.code

    @code.setter
    def code(self, code: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.code = code

    @property
    def sql(self) -> Optional[str]:
        return self.attributes.sql

    @sql.setter
    def sql(self, sql: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql = sql

    @property
    def ast(self) -> Optional[str]:
        return self.attributes.ast

    @ast.setter
    def ast(self, ast: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ast = ast

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Process", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Process":
            raise ValueError("must be Process")
        return v

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


class AtlasGlossaryCategory(Asset, type_name="AtlasGlossaryCategory"):
    """Description"""

    def __setattr__(self, name, value):
        if name in AtlasGlossaryCategory._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "short_description",
        "long_description",
        "additional_attributes",
        "terms",
    ]

    @property
    def short_description(self) -> Optional[str]:
        return self.attributes.short_description

    @short_description.setter
    def short_description(self, short_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.short_description = short_description

    @property
    def long_description(self) -> Optional[str]:
        return self.attributes.long_description

    @long_description.setter
    def long_description(self, long_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.long_description = long_description

    @property
    def additional_attributes(self) -> Optional[dict[str, str]]:
        return self.attributes.additional_attributes

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.additional_attributes = additional_attributes

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("AtlasGlossaryCategory", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlasGlossaryCategory":
            raise ValueError("must be AtlasGlossaryCategory")
        return v

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
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )

    @root_validator()
    def update_qualified_name(cls, values):
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


class Badge(Asset, type_name="Badge"):
    """Description"""

    def __setattr__(self, name, value):
        if name in Badge._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "badge_conditions",
        "badge_metadata_attribute",
        "terms",
    ]

    @property
    def badge_conditions(self) -> Optional[list[BadgeCondition]]:
        return self.attributes.badge_conditions

    @badge_conditions.setter
    def badge_conditions(self, badge_conditions: Optional[list[BadgeCondition]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.badge_conditions = badge_conditions

    @property
    def badge_metadata_attribute(self) -> Optional[str]:
        return self.attributes.badge_metadata_attribute

    @badge_metadata_attribute.setter
    def badge_metadata_attribute(self, badge_metadata_attribute: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.badge_metadata_attribute = badge_metadata_attribute

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Badge", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Badge":
            raise ValueError("must be Badge")
        return v

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


class Namespace(Asset, type_name="Namespace"):
    """Description"""

    def __setattr__(self, name, value):
        if name in Namespace._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Namespace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Namespace":
            raise ValueError("must be Namespace")
        return v

    class Attributes(Asset.Attributes):
        children_queries: Optional[list[Query]] = Field(
            None, description="", alias="childrenQueries"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        children_folders: Optional[list[Folder]] = Field(
            None, description="", alias="childrenFolders"
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

    attributes: "Namespace.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Catalog(Asset, type_name="Catalog"):
    """Description"""

    def __setattr__(self, name, value):
        if name in Catalog._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Catalog", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Catalog":
            raise ValueError("must be Catalog")
        return v

    class Attributes(Asset.Attributes):
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

    attributes: "Catalog.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Google(Cloud):
    """Description"""

    def __setattr__(self, name, value):
        if name in Google._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "google_service",
        "google_project_name",
        "google_project_id",
        "google_project_number",
        "google_location",
        "google_location_type",
        "google_labels",
        "google_tags",
        "terms",
    ]

    @property
    def google_service(self) -> Optional[str]:
        return self.attributes.google_service

    @google_service.setter
    def google_service(self, google_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_service = google_service

    @property
    def google_project_name(self) -> Optional[str]:
        return self.attributes.google_project_name

    @google_project_name.setter
    def google_project_name(self, google_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_name = google_project_name

    @property
    def google_project_id(self) -> Optional[str]:
        return self.attributes.google_project_id

    @google_project_id.setter
    def google_project_id(self, google_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_id = google_project_id

    @property
    def google_project_number(self) -> Optional[int]:
        return self.attributes.google_project_number

    @google_project_number.setter
    def google_project_number(self, google_project_number: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_number = google_project_number

    @property
    def google_location(self) -> Optional[str]:
        return self.attributes.google_location

    @google_location.setter
    def google_location(self, google_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location = google_location

    @property
    def google_location_type(self) -> Optional[str]:
        return self.attributes.google_location_type

    @google_location_type.setter
    def google_location_type(self, google_location_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location_type = google_location_type

    @property
    def google_labels(self) -> Optional[list[GoogleLabel]]:
        return self.attributes.google_labels

    @google_labels.setter
    def google_labels(self, google_labels: Optional[list[GoogleLabel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_labels = google_labels

    @property
    def google_tags(self) -> Optional[list[GoogleTag]]:
        return self.attributes.google_tags

    @google_tags.setter
    def google_tags(self, google_tags: Optional[list[GoogleTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_tags = google_tags

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Google", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Google":
            raise ValueError("must be Google")
        return v

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


class Azure(Cloud):
    """Description"""

    def __setattr__(self, name, value):
        if name in Azure._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "azure_resource_id",
        "azure_location",
        "adls_account_secondary_location",
        "azure_tags",
        "terms",
    ]

    @property
    def azure_resource_id(self) -> Optional[str]:
        return self.attributes.azure_resource_id

    @azure_resource_id.setter
    def azure_resource_id(self, azure_resource_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_resource_id = azure_resource_id

    @property
    def azure_location(self) -> Optional[str]:
        return self.attributes.azure_location

    @azure_location.setter
    def azure_location(self, azure_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_location = azure_location

    @property
    def adls_account_secondary_location(self) -> Optional[str]:
        return self.attributes.adls_account_secondary_location

    @adls_account_secondary_location.setter
    def adls_account_secondary_location(
        self, adls_account_secondary_location: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_secondary_location = (
            adls_account_secondary_location
        )

    @property
    def azure_tags(self) -> Optional[list[AzureTag]]:
        return self.attributes.azure_tags

    @azure_tags.setter
    def azure_tags(self, azure_tags: Optional[list[AzureTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_tags = azure_tags

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Azure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Azure":
            raise ValueError("must be Azure")
        return v

    class Attributes(Cloud.Attributes):
        azure_resource_id: Optional[str] = Field(
            None, description="", alias="azureResourceId"
        )
        azure_location: Optional[str] = Field(
            None, description="", alias="azureLocation"
        )
        adls_account_secondary_location: Optional[str] = Field(
            None, description="", alias="adlsAccountSecondaryLocation"
        )
        azure_tags: Optional[list[AzureTag]] = Field(
            None, description="", alias="azureTags"
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

    attributes: "Azure.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AWS(Cloud):
    """Description"""

    def __setattr__(self, name, value):
        if name in AWS._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "aws_arn",
        "aws_partition",
        "aws_service",
        "aws_region",
        "aws_account_id",
        "aws_resource_id",
        "aws_owner_name",
        "aws_owner_id",
        "aws_tags",
        "terms",
    ]

    @property
    def aws_arn(self) -> Optional[str]:
        return self.attributes.aws_arn

    @aws_arn.setter
    def aws_arn(self, aws_arn: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_arn = aws_arn

    @property
    def aws_partition(self) -> Optional[str]:
        return self.attributes.aws_partition

    @aws_partition.setter
    def aws_partition(self, aws_partition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_partition = aws_partition

    @property
    def aws_service(self) -> Optional[str]:
        return self.attributes.aws_service

    @aws_service.setter
    def aws_service(self, aws_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_service = aws_service

    @property
    def aws_region(self) -> Optional[str]:
        return self.attributes.aws_region

    @aws_region.setter
    def aws_region(self, aws_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_region = aws_region

    @property
    def aws_account_id(self) -> Optional[str]:
        return self.attributes.aws_account_id

    @aws_account_id.setter
    def aws_account_id(self, aws_account_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_account_id = aws_account_id

    @property
    def aws_resource_id(self) -> Optional[str]:
        return self.attributes.aws_resource_id

    @aws_resource_id.setter
    def aws_resource_id(self, aws_resource_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_resource_id = aws_resource_id

    @property
    def aws_owner_name(self) -> Optional[str]:
        return self.attributes.aws_owner_name

    @aws_owner_name.setter
    def aws_owner_name(self, aws_owner_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_owner_name = aws_owner_name

    @property
    def aws_owner_id(self) -> Optional[str]:
        return self.attributes.aws_owner_id

    @aws_owner_id.setter
    def aws_owner_id(self, aws_owner_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_owner_id = aws_owner_id

    @property
    def aws_tags(self) -> Optional[list[AwsTag]]:
        return self.attributes.aws_tags

    @aws_tags.setter
    def aws_tags(self, aws_tags: Optional[list[AwsTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_tags = aws_tags

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("AWS", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AWS":
            raise ValueError("must be AWS")
        return v

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

    def __setattr__(self, name, value):
        if name in BIProcess._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("BIProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "BIProcess":
            raise ValueError("must be BIProcess")
        return v

    class Attributes(Process.Attributes):
        outputs: Optional[list[Catalog]] = Field(
            None, description="", alias="outputs"
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

    attributes: "BIProcess.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ColumnProcess(Process):
    """Description"""

    def __setattr__(self, name, value):
        if name in ColumnProcess._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ColumnProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ColumnProcess":
            raise ValueError("must be ColumnProcess")
        return v

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

    attributes: "ColumnProcess.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Collection(Namespace):
    """Description"""

    def __setattr__(self, name, value):
        if name in Collection._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "icon",
        "icon_type",
        "terms",
    ]

    @property
    def icon(self) -> Optional[str]:
        return self.attributes.icon

    @icon.setter
    def icon(self, icon: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon = icon

    @property
    def icon_type(self) -> Optional[IconType]:
        return self.attributes.icon_type

    @icon_type.setter
    def icon_type(self, icon_type: Optional[IconType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon_type = icon_type

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Collection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Collection":
            raise ValueError("must be Collection")
        return v

    class Attributes(Namespace.Attributes):
        icon: Optional[str] = Field(None, description="", alias="icon")
        icon_type: Optional[IconType] = Field(None, description="", alias="iconType")
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

    def __setattr__(self, name, value):
        if name in Folder._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "parent_qualified_name",
        "collection_qualified_name",
        "terms",
    ]

    @property
    def parent_qualified_name(self) -> str:
        return self.attributes.parent_qualified_name

    @parent_qualified_name.setter
    def parent_qualified_name(self, parent_qualified_name: str):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_qualified_name = parent_qualified_name

    @property
    def collection_qualified_name(self) -> str:
        return self.attributes.collection_qualified_name

    @collection_qualified_name.setter
    def collection_qualified_name(self, collection_qualified_name: str):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.collection_qualified_name = collection_qualified_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Folder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Folder":
            raise ValueError("must be Folder")
        return v

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


class EventStore(Catalog):
    """Description"""

    def __setattr__(self, name, value):
        if name in EventStore._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("EventStore", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "EventStore":
            raise ValueError("must be EventStore")
        return v

    class Attributes(Catalog.Attributes):
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

    attributes: "EventStore.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ObjectStore(Catalog):
    """Description"""

    def __setattr__(self, name, value):
        if name in ObjectStore._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ObjectStore", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ObjectStore":
            raise ValueError("must be ObjectStore")
        return v

    class Attributes(Catalog.Attributes):
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

    attributes: "ObjectStore.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DataQuality(Catalog):
    """Description"""

    def __setattr__(self, name, value):
        if name in DataQuality._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("DataQuality", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataQuality":
            raise ValueError("must be DataQuality")
        return v

    class Attributes(Catalog.Attributes):
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

    attributes: "DataQuality.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class BI(Catalog):
    """Description"""

    def __setattr__(self, name, value):
        if name in BI._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("BI", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "BI":
            raise ValueError("must be BI")
        return v

    class Attributes(Catalog.Attributes):
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

    attributes: "BI.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SaaS(Catalog):
    """Description"""

    def __setattr__(self, name, value):
        if name in SaaS._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SaaS", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SaaS":
            raise ValueError("must be SaaS")
        return v

    class Attributes(Catalog.Attributes):
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

    attributes: "SaaS.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Dbt(Catalog):
    """Description"""

    def __setattr__(self, name, value):
        if name in Dbt._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
        "terms",
    ]

    @property
    def dbt_alias(self) -> Optional[str]:
        return self.attributes.dbt_alias

    @dbt_alias.setter
    def dbt_alias(self, dbt_alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_alias = dbt_alias

    @property
    def dbt_meta(self) -> Optional[str]:
        return self.attributes.dbt_meta

    @dbt_meta.setter
    def dbt_meta(self, dbt_meta: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_meta = dbt_meta

    @property
    def dbt_unique_id(self) -> Optional[str]:
        return self.attributes.dbt_unique_id

    @dbt_unique_id.setter
    def dbt_unique_id(self, dbt_unique_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_unique_id = dbt_unique_id

    @property
    def dbt_account_name(self) -> Optional[str]:
        return self.attributes.dbt_account_name

    @dbt_account_name.setter
    def dbt_account_name(self, dbt_account_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_account_name = dbt_account_name

    @property
    def dbt_project_name(self) -> Optional[str]:
        return self.attributes.dbt_project_name

    @dbt_project_name.setter
    def dbt_project_name(self, dbt_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_project_name = dbt_project_name

    @property
    def dbt_package_name(self) -> Optional[str]:
        return self.attributes.dbt_package_name

    @dbt_package_name.setter
    def dbt_package_name(self, dbt_package_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_package_name = dbt_package_name

    @property
    def dbt_job_name(self) -> Optional[str]:
        return self.attributes.dbt_job_name

    @dbt_job_name.setter
    def dbt_job_name(self, dbt_job_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_name = dbt_job_name

    @property
    def dbt_job_schedule(self) -> Optional[str]:
        return self.attributes.dbt_job_schedule

    @dbt_job_schedule.setter
    def dbt_job_schedule(self, dbt_job_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_schedule = dbt_job_schedule

    @property
    def dbt_job_status(self) -> Optional[str]:
        return self.attributes.dbt_job_status

    @dbt_job_status.setter
    def dbt_job_status(self, dbt_job_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_status = dbt_job_status

    @property
    def dbt_job_schedule_cron_humanized(self) -> Optional[str]:
        return self.attributes.dbt_job_schedule_cron_humanized

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
        return self.attributes.dbt_job_last_run

    @dbt_job_last_run.setter
    def dbt_job_last_run(self, dbt_job_last_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_last_run = dbt_job_last_run

    @property
    def dbt_job_next_run(self) -> Optional[datetime]:
        return self.attributes.dbt_job_next_run

    @dbt_job_next_run.setter
    def dbt_job_next_run(self, dbt_job_next_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run = dbt_job_next_run

    @property
    def dbt_job_next_run_humanized(self) -> Optional[str]:
        return self.attributes.dbt_job_next_run_humanized

    @dbt_job_next_run_humanized.setter
    def dbt_job_next_run_humanized(self, dbt_job_next_run_humanized: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run_humanized = dbt_job_next_run_humanized

    @property
    def dbt_environment_name(self) -> Optional[str]:
        return self.attributes.dbt_environment_name

    @dbt_environment_name.setter
    def dbt_environment_name(self, dbt_environment_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_name = dbt_environment_name

    @property
    def dbt_environment_dbt_version(self) -> Optional[str]:
        return self.attributes.dbt_environment_dbt_version

    @dbt_environment_dbt_version.setter
    def dbt_environment_dbt_version(self, dbt_environment_dbt_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_dbt_version = dbt_environment_dbt_version

    @property
    def dbt_tags(self) -> Optional[set[str]]:
        return self.attributes.dbt_tags

    @dbt_tags.setter
    def dbt_tags(self, dbt_tags: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tags = dbt_tags

    @property
    def dbt_connection_context(self) -> Optional[str]:
        return self.attributes.dbt_connection_context

    @dbt_connection_context.setter
    def dbt_connection_context(self, dbt_connection_context: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_connection_context = dbt_connection_context

    @property
    def dbt_semantic_layer_proxy_url(self) -> Optional[str]:
        return self.attributes.dbt_semantic_layer_proxy_url

    @dbt_semantic_layer_proxy_url.setter
    def dbt_semantic_layer_proxy_url(self, dbt_semantic_layer_proxy_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_semantic_layer_proxy_url = dbt_semantic_layer_proxy_url

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Dbt", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Dbt":
            raise ValueError("must be Dbt")
        return v

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

    def __setattr__(self, name, value):
        if name in Resource._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "link",
        "is_global",
        "reference",
        "resource_metadata",
        "terms",
    ]

    @property
    def link(self) -> Optional[str]:
        return self.attributes.link

    @link.setter
    def link(self, link: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.link = link

    @property
    def is_global(self) -> Optional[bool]:
        return self.attributes.is_global

    @is_global.setter
    def is_global(self, is_global: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_global = is_global

    @property
    def reference(self) -> Optional[str]:
        return self.attributes.reference

    @reference.setter
    def reference(self, reference: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reference = reference

    @property
    def resource_metadata(self) -> Optional[dict[str, str]]:
        return self.attributes.resource_metadata

    @resource_metadata.setter
    def resource_metadata(self, resource_metadata: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.resource_metadata = resource_metadata

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Resource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Resource":
            raise ValueError("must be Resource")
        return v

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

    def __setattr__(self, name, value):
        if name in Insight._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Insight", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Insight":
            raise ValueError("must be Insight")
        return v

    class Attributes(Catalog.Attributes):
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

    attributes: "Insight.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class API(Catalog):
    """Description"""

    def __setattr__(self, name, value):
        if name in API._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "api_spec_type",
        "api_spec_version",
        "api_spec_name",
        "api_spec_qualified_name",
        "api_external_docs",
        "api_is_auth_optional",
        "terms",
    ]

    @property
    def api_spec_type(self) -> Optional[str]:
        return self.attributes.api_spec_type

    @api_spec_type.setter
    def api_spec_type(self, api_spec_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_type = api_spec_type

    @property
    def api_spec_version(self) -> Optional[str]:
        return self.attributes.api_spec_version

    @api_spec_version.setter
    def api_spec_version(self, api_spec_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_version = api_spec_version

    @property
    def api_spec_name(self) -> Optional[str]:
        return self.attributes.api_spec_name

    @api_spec_name.setter
    def api_spec_name(self, api_spec_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_name = api_spec_name

    @property
    def api_spec_qualified_name(self) -> Optional[str]:
        return self.attributes.api_spec_qualified_name

    @api_spec_qualified_name.setter
    def api_spec_qualified_name(self, api_spec_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_qualified_name = api_spec_qualified_name

    @property
    def api_external_docs(self) -> Optional[dict[str, str]]:
        return self.attributes.api_external_docs

    @api_external_docs.setter
    def api_external_docs(self, api_external_docs: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_external_docs = api_external_docs

    @property
    def api_is_auth_optional(self) -> Optional[bool]:
        return self.attributes.api_is_auth_optional

    @api_is_auth_optional.setter
    def api_is_auth_optional(self, api_is_auth_optional: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_is_auth_optional = api_is_auth_optional

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("API", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "API":
            raise ValueError("must be API")
        return v

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

    def __setattr__(self, name, value):
        if name in SQL._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
        "terms",
    ]

    @property
    def query_count(self) -> Optional[int]:
        return self.attributes.query_count

    @query_count.setter
    def query_count(self, query_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_count = query_count

    @property
    def query_user_count(self) -> Optional[int]:
        return self.attributes.query_user_count

    @query_user_count.setter
    def query_user_count(self, query_user_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_user_count = query_user_count

    @property
    def query_user_map(self) -> Optional[dict[str, int]]:
        return self.attributes.query_user_map

    @query_user_map.setter
    def query_user_map(self, query_user_map: Optional[dict[str, int]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_user_map = query_user_map

    @property
    def query_count_updated_at(self) -> Optional[datetime]:
        return self.attributes.query_count_updated_at

    @query_count_updated_at.setter
    def query_count_updated_at(self, query_count_updated_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_count_updated_at = query_count_updated_at

    @property
    def database_name(self) -> Optional[str]:
        return self.attributes.database_name

    @database_name.setter
    def database_name(self, database_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database_name = database_name

    @property
    def database_qualified_name(self) -> Optional[str]:
        return self.attributes.database_qualified_name

    @database_qualified_name.setter
    def database_qualified_name(self, database_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database_qualified_name = database_qualified_name

    @property
    def schema_name(self) -> Optional[str]:
        return self.attributes.schema_name

    @schema_name.setter
    def schema_name(self, schema_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_name = schema_name

    @property
    def schema_qualified_name(self) -> Optional[str]:
        return self.attributes.schema_qualified_name

    @schema_qualified_name.setter
    def schema_qualified_name(self, schema_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_qualified_name = schema_qualified_name

    @property
    def table_name(self) -> Optional[str]:
        return self.attributes.table_name

    @table_name.setter
    def table_name(self, table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_name = table_name

    @property
    def table_qualified_name(self) -> Optional[str]:
        return self.attributes.table_qualified_name

    @table_qualified_name.setter
    def table_qualified_name(self, table_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_qualified_name = table_qualified_name

    @property
    def view_name(self) -> Optional[str]:
        return self.attributes.view_name

    @view_name.setter
    def view_name(self, view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_name = view_name

    @property
    def view_qualified_name(self) -> Optional[str]:
        return self.attributes.view_qualified_name

    @view_qualified_name.setter
    def view_qualified_name(self, view_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_qualified_name = view_qualified_name

    @property
    def is_profiled(self) -> Optional[bool]:
        return self.attributes.is_profiled

    @is_profiled.setter
    def is_profiled(self, is_profiled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_profiled = is_profiled

    @property
    def last_profiled_at(self) -> Optional[datetime]:
        return self.attributes.last_profiled_at

    @last_profiled_at.setter
    def last_profiled_at(self, last_profiled_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_profiled_at = last_profiled_at

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SQL", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SQL":
            raise ValueError("must be SQL")
        return v

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
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="sqlDbtModels"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="sqlDBTSources"
        )  # relationship

    attributes: "SQL.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DataStudio(Google):
    """Description"""

    def __setattr__(self, name, value):
        if name in DataStudio._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "google_service",
        "google_project_name",
        "google_project_id",
        "google_project_number",
        "google_location",
        "google_location_type",
        "google_labels",
        "google_tags",
        "terms",
    ]

    @property
    def google_service(self) -> Optional[str]:
        return self.attributes.google_service

    @google_service.setter
    def google_service(self, google_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_service = google_service

    @property
    def google_project_name(self) -> Optional[str]:
        return self.attributes.google_project_name

    @google_project_name.setter
    def google_project_name(self, google_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_name = google_project_name

    @property
    def google_project_id(self) -> Optional[str]:
        return self.attributes.google_project_id

    @google_project_id.setter
    def google_project_id(self, google_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_id = google_project_id

    @property
    def google_project_number(self) -> Optional[int]:
        return self.attributes.google_project_number

    @google_project_number.setter
    def google_project_number(self, google_project_number: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_number = google_project_number

    @property
    def google_location(self) -> Optional[str]:
        return self.attributes.google_location

    @google_location.setter
    def google_location(self, google_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location = google_location

    @property
    def google_location_type(self) -> Optional[str]:
        return self.attributes.google_location_type

    @google_location_type.setter
    def google_location_type(self, google_location_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location_type = google_location_type

    @property
    def google_labels(self) -> Optional[list[GoogleLabel]]:
        return self.attributes.google_labels

    @google_labels.setter
    def google_labels(self, google_labels: Optional[list[GoogleLabel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_labels = google_labels

    @property
    def google_tags(self) -> Optional[list[GoogleTag]]:
        return self.attributes.google_tags

    @google_tags.setter
    def google_tags(self, google_tags: Optional[list[GoogleTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_tags = google_tags

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("DataStudio", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataStudio":
            raise ValueError("must be DataStudio")
        return v

    class Attributes(Google.Attributes):
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

    attributes: "DataStudio.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class GCS(Google):
    """Description"""

    def __setattr__(self, name, value):
        if name in GCS._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "gcs_storage_class",
        "gcs_encryption_type",
        "gcs_e_tag",
        "gcs_requester_pays",
        "gcs_access_control",
        "gcs_meta_generation_id",
        "google_service",
        "google_project_name",
        "google_project_id",
        "google_project_number",
        "google_location",
        "google_location_type",
        "google_labels",
        "google_tags",
        "terms",
    ]

    @property
    def gcs_storage_class(self) -> Optional[str]:
        return self.attributes.gcs_storage_class

    @gcs_storage_class.setter
    def gcs_storage_class(self, gcs_storage_class: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_storage_class = gcs_storage_class

    @property
    def gcs_encryption_type(self) -> Optional[str]:
        return self.attributes.gcs_encryption_type

    @gcs_encryption_type.setter
    def gcs_encryption_type(self, gcs_encryption_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_encryption_type = gcs_encryption_type

    @property
    def gcs_e_tag(self) -> Optional[str]:
        return self.attributes.gcs_e_tag

    @gcs_e_tag.setter
    def gcs_e_tag(self, gcs_e_tag: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_e_tag = gcs_e_tag

    @property
    def gcs_requester_pays(self) -> Optional[bool]:
        return self.attributes.gcs_requester_pays

    @gcs_requester_pays.setter
    def gcs_requester_pays(self, gcs_requester_pays: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_requester_pays = gcs_requester_pays

    @property
    def gcs_access_control(self) -> Optional[str]:
        return self.attributes.gcs_access_control

    @gcs_access_control.setter
    def gcs_access_control(self, gcs_access_control: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_access_control = gcs_access_control

    @property
    def gcs_meta_generation_id(self) -> Optional[int]:
        return self.attributes.gcs_meta_generation_id

    @gcs_meta_generation_id.setter
    def gcs_meta_generation_id(self, gcs_meta_generation_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_meta_generation_id = gcs_meta_generation_id

    @property
    def google_service(self) -> Optional[str]:
        return self.attributes.google_service

    @google_service.setter
    def google_service(self, google_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_service = google_service

    @property
    def google_project_name(self) -> Optional[str]:
        return self.attributes.google_project_name

    @google_project_name.setter
    def google_project_name(self, google_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_name = google_project_name

    @property
    def google_project_id(self) -> Optional[str]:
        return self.attributes.google_project_id

    @google_project_id.setter
    def google_project_id(self, google_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_id = google_project_id

    @property
    def google_project_number(self) -> Optional[int]:
        return self.attributes.google_project_number

    @google_project_number.setter
    def google_project_number(self, google_project_number: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_number = google_project_number

    @property
    def google_location(self) -> Optional[str]:
        return self.attributes.google_location

    @google_location.setter
    def google_location(self, google_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location = google_location

    @property
    def google_location_type(self) -> Optional[str]:
        return self.attributes.google_location_type

    @google_location_type.setter
    def google_location_type(self, google_location_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location_type = google_location_type

    @property
    def google_labels(self) -> Optional[list[GoogleLabel]]:
        return self.attributes.google_labels

    @google_labels.setter
    def google_labels(self, google_labels: Optional[list[GoogleLabel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_labels = google_labels

    @property
    def google_tags(self) -> Optional[list[GoogleTag]]:
        return self.attributes.google_tags

    @google_tags.setter
    def google_tags(self, google_tags: Optional[list[GoogleTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_tags = google_tags

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("GCS", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "GCS":
            raise ValueError("must be GCS")
        return v

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

    def __setattr__(self, name, value):
        if name in DataStudioAsset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "data_studio_asset_type",
        "data_studio_asset_title",
        "data_studio_asset_owner",
        "is_trashed_data_studio_asset",
        "google_service",
        "google_project_name",
        "google_project_id",
        "google_project_number",
        "google_location",
        "google_location_type",
        "google_labels",
        "google_tags",
        "terms",
    ]

    @property
    def data_studio_asset_type(self) -> Optional[GoogleDatastudioAssetType]:
        return self.attributes.data_studio_asset_type

    @data_studio_asset_type.setter
    def data_studio_asset_type(
        self, data_studio_asset_type: Optional[GoogleDatastudioAssetType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_studio_asset_type = data_studio_asset_type

    @property
    def data_studio_asset_title(self) -> Optional[str]:
        return self.attributes.data_studio_asset_title

    @data_studio_asset_title.setter
    def data_studio_asset_title(self, data_studio_asset_title: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_studio_asset_title = data_studio_asset_title

    @property
    def data_studio_asset_owner(self) -> Optional[str]:
        return self.attributes.data_studio_asset_owner

    @data_studio_asset_owner.setter
    def data_studio_asset_owner(self, data_studio_asset_owner: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_studio_asset_owner = data_studio_asset_owner

    @property
    def is_trashed_data_studio_asset(self) -> Optional[bool]:
        return self.attributes.is_trashed_data_studio_asset

    @is_trashed_data_studio_asset.setter
    def is_trashed_data_studio_asset(
        self, is_trashed_data_studio_asset: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_trashed_data_studio_asset = is_trashed_data_studio_asset

    @property
    def google_service(self) -> Optional[str]:
        return self.attributes.google_service

    @google_service.setter
    def google_service(self, google_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_service = google_service

    @property
    def google_project_name(self) -> Optional[str]:
        return self.attributes.google_project_name

    @google_project_name.setter
    def google_project_name(self, google_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_name = google_project_name

    @property
    def google_project_id(self) -> Optional[str]:
        return self.attributes.google_project_id

    @google_project_id.setter
    def google_project_id(self, google_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_id = google_project_id

    @property
    def google_project_number(self) -> Optional[int]:
        return self.attributes.google_project_number

    @google_project_number.setter
    def google_project_number(self, google_project_number: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_number = google_project_number

    @property
    def google_location(self) -> Optional[str]:
        return self.attributes.google_location

    @google_location.setter
    def google_location(self, google_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location = google_location

    @property
    def google_location_type(self) -> Optional[str]:
        return self.attributes.google_location_type

    @google_location_type.setter
    def google_location_type(self, google_location_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location_type = google_location_type

    @property
    def google_labels(self) -> Optional[list[GoogleLabel]]:
        return self.attributes.google_labels

    @google_labels.setter
    def google_labels(self, google_labels: Optional[list[GoogleLabel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_labels = google_labels

    @property
    def google_tags(self) -> Optional[list[GoogleTag]]:
        return self.attributes.google_tags

    @google_tags.setter
    def google_tags(self, google_tags: Optional[list[GoogleTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_tags = google_tags

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("DataStudioAsset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataStudioAsset":
            raise ValueError("must be DataStudioAsset")
        return v

    class Attributes(DataStudio.Attributes):
        data_studio_asset_type: Optional[GoogleDatastudioAssetType] = Field(
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


class ADLS(ObjectStore):
    """Description"""

    def __setattr__(self, name, value):
        if name in ADLS._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "adls_account_qualified_name",
        "azure_resource_id",
        "azure_location",
        "adls_account_secondary_location",
        "azure_tags",
        "terms",
    ]

    @property
    def adls_account_qualified_name(self) -> Optional[str]:
        return self.attributes.adls_account_qualified_name

    @adls_account_qualified_name.setter
    def adls_account_qualified_name(self, adls_account_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_qualified_name = adls_account_qualified_name

    @property
    def azure_resource_id(self) -> Optional[str]:
        return self.attributes.azure_resource_id

    @azure_resource_id.setter
    def azure_resource_id(self, azure_resource_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_resource_id = azure_resource_id

    @property
    def azure_location(self) -> Optional[str]:
        return self.attributes.azure_location

    @azure_location.setter
    def azure_location(self, azure_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_location = azure_location

    @property
    def adls_account_secondary_location(self) -> Optional[str]:
        return self.attributes.adls_account_secondary_location

    @adls_account_secondary_location.setter
    def adls_account_secondary_location(
        self, adls_account_secondary_location: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_secondary_location = (
            adls_account_secondary_location
        )

    @property
    def azure_tags(self) -> Optional[list[AzureTag]]:
        return self.attributes.azure_tags

    @azure_tags.setter
    def azure_tags(self, azure_tags: Optional[list[AzureTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_tags = azure_tags

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ADLS", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADLS":
            raise ValueError("must be ADLS")
        return v

    class Attributes(ObjectStore.Attributes):
        adls_account_qualified_name: Optional[str] = Field(
            None, description="", alias="adlsAccountQualifiedName"
        )
        azure_resource_id: Optional[str] = Field(
            None, description="", alias="azureResourceId"
        )
        azure_location: Optional[str] = Field(
            None, description="", alias="azureLocation"
        )
        adls_account_secondary_location: Optional[str] = Field(
            None, description="", alias="adlsAccountSecondaryLocation"
        )
        azure_tags: Optional[list[AzureTag]] = Field(
            None, description="", alias="azureTags"
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

    attributes: "ADLS.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class S3(ObjectStore):
    """Description"""

    def __setattr__(self, name, value):
        if name in S3._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "s3_e_tag",
        "s3_encryption",
        "aws_arn",
        "aws_partition",
        "aws_service",
        "aws_region",
        "aws_account_id",
        "aws_resource_id",
        "aws_owner_name",
        "aws_owner_id",
        "aws_tags",
        "terms",
    ]

    @property
    def s3_e_tag(self) -> Optional[str]:
        return self.attributes.s3_e_tag

    @s3_e_tag.setter
    def s3_e_tag(self, s3_e_tag: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_e_tag = s3_e_tag

    @property
    def s3_encryption(self) -> Optional[str]:
        return self.attributes.s3_encryption

    @s3_encryption.setter
    def s3_encryption(self, s3_encryption: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_encryption = s3_encryption

    @property
    def aws_arn(self) -> Optional[str]:
        return self.attributes.aws_arn

    @aws_arn.setter
    def aws_arn(self, aws_arn: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_arn = aws_arn

    @property
    def aws_partition(self) -> Optional[str]:
        return self.attributes.aws_partition

    @aws_partition.setter
    def aws_partition(self, aws_partition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_partition = aws_partition

    @property
    def aws_service(self) -> Optional[str]:
        return self.attributes.aws_service

    @aws_service.setter
    def aws_service(self, aws_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_service = aws_service

    @property
    def aws_region(self) -> Optional[str]:
        return self.attributes.aws_region

    @aws_region.setter
    def aws_region(self, aws_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_region = aws_region

    @property
    def aws_account_id(self) -> Optional[str]:
        return self.attributes.aws_account_id

    @aws_account_id.setter
    def aws_account_id(self, aws_account_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_account_id = aws_account_id

    @property
    def aws_resource_id(self) -> Optional[str]:
        return self.attributes.aws_resource_id

    @aws_resource_id.setter
    def aws_resource_id(self, aws_resource_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_resource_id = aws_resource_id

    @property
    def aws_owner_name(self) -> Optional[str]:
        return self.attributes.aws_owner_name

    @aws_owner_name.setter
    def aws_owner_name(self, aws_owner_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_owner_name = aws_owner_name

    @property
    def aws_owner_id(self) -> Optional[str]:
        return self.attributes.aws_owner_id

    @aws_owner_id.setter
    def aws_owner_id(self, aws_owner_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_owner_id = aws_owner_id

    @property
    def aws_tags(self) -> Optional[list[AwsTag]]:
        return self.attributes.aws_tags

    @aws_tags.setter
    def aws_tags(self, aws_tags: Optional[list[AwsTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_tags = aws_tags

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("S3", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "S3":
            raise ValueError("must be S3")
        return v

    class Attributes(ObjectStore.Attributes):
        s3_e_tag: Optional[str] = Field(None, description="", alias="s3ETag")
        s3_encryption: Optional[str] = Field(None, description="", alias="s3Encryption")
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

    def __setattr__(self, name, value):
        if name in DbtColumnProcess._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "dbt_column_process_job_status",
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
        "inputs",
        "outputs",
        "code",
        "sql",
        "ast",
        "terms",
    ]

    @property
    def dbt_column_process_job_status(self) -> Optional[str]:
        return self.attributes.dbt_column_process_job_status

    @dbt_column_process_job_status.setter
    def dbt_column_process_job_status(
        self, dbt_column_process_job_status: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_column_process_job_status = dbt_column_process_job_status

    @property
    def dbt_alias(self) -> Optional[str]:
        return self.attributes.dbt_alias

    @dbt_alias.setter
    def dbt_alias(self, dbt_alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_alias = dbt_alias

    @property
    def dbt_meta(self) -> Optional[str]:
        return self.attributes.dbt_meta

    @dbt_meta.setter
    def dbt_meta(self, dbt_meta: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_meta = dbt_meta

    @property
    def dbt_unique_id(self) -> Optional[str]:
        return self.attributes.dbt_unique_id

    @dbt_unique_id.setter
    def dbt_unique_id(self, dbt_unique_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_unique_id = dbt_unique_id

    @property
    def dbt_account_name(self) -> Optional[str]:
        return self.attributes.dbt_account_name

    @dbt_account_name.setter
    def dbt_account_name(self, dbt_account_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_account_name = dbt_account_name

    @property
    def dbt_project_name(self) -> Optional[str]:
        return self.attributes.dbt_project_name

    @dbt_project_name.setter
    def dbt_project_name(self, dbt_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_project_name = dbt_project_name

    @property
    def dbt_package_name(self) -> Optional[str]:
        return self.attributes.dbt_package_name

    @dbt_package_name.setter
    def dbt_package_name(self, dbt_package_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_package_name = dbt_package_name

    @property
    def dbt_job_name(self) -> Optional[str]:
        return self.attributes.dbt_job_name

    @dbt_job_name.setter
    def dbt_job_name(self, dbt_job_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_name = dbt_job_name

    @property
    def dbt_job_schedule(self) -> Optional[str]:
        return self.attributes.dbt_job_schedule

    @dbt_job_schedule.setter
    def dbt_job_schedule(self, dbt_job_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_schedule = dbt_job_schedule

    @property
    def dbt_job_status(self) -> Optional[str]:
        return self.attributes.dbt_job_status

    @dbt_job_status.setter
    def dbt_job_status(self, dbt_job_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_status = dbt_job_status

    @property
    def dbt_job_schedule_cron_humanized(self) -> Optional[str]:
        return self.attributes.dbt_job_schedule_cron_humanized

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
        return self.attributes.dbt_job_last_run

    @dbt_job_last_run.setter
    def dbt_job_last_run(self, dbt_job_last_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_last_run = dbt_job_last_run

    @property
    def dbt_job_next_run(self) -> Optional[datetime]:
        return self.attributes.dbt_job_next_run

    @dbt_job_next_run.setter
    def dbt_job_next_run(self, dbt_job_next_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run = dbt_job_next_run

    @property
    def dbt_job_next_run_humanized(self) -> Optional[str]:
        return self.attributes.dbt_job_next_run_humanized

    @dbt_job_next_run_humanized.setter
    def dbt_job_next_run_humanized(self, dbt_job_next_run_humanized: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run_humanized = dbt_job_next_run_humanized

    @property
    def dbt_environment_name(self) -> Optional[str]:
        return self.attributes.dbt_environment_name

    @dbt_environment_name.setter
    def dbt_environment_name(self, dbt_environment_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_name = dbt_environment_name

    @property
    def dbt_environment_dbt_version(self) -> Optional[str]:
        return self.attributes.dbt_environment_dbt_version

    @dbt_environment_dbt_version.setter
    def dbt_environment_dbt_version(self, dbt_environment_dbt_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_dbt_version = dbt_environment_dbt_version

    @property
    def dbt_tags(self) -> Optional[set[str]]:
        return self.attributes.dbt_tags

    @dbt_tags.setter
    def dbt_tags(self, dbt_tags: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tags = dbt_tags

    @property
    def dbt_connection_context(self) -> Optional[str]:
        return self.attributes.dbt_connection_context

    @dbt_connection_context.setter
    def dbt_connection_context(self, dbt_connection_context: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_connection_context = dbt_connection_context

    @property
    def dbt_semantic_layer_proxy_url(self) -> Optional[str]:
        return self.attributes.dbt_semantic_layer_proxy_url

    @dbt_semantic_layer_proxy_url.setter
    def dbt_semantic_layer_proxy_url(self, dbt_semantic_layer_proxy_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_semantic_layer_proxy_url = dbt_semantic_layer_proxy_url

    @property
    def inputs(self) -> Optional[list[Catalog]]:
        return self.attributes.inputs

    @inputs.setter
    def inputs(self, inputs: Optional[list[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inputs = inputs

    @property
    def outputs(self) -> Optional[list[Catalog]]:
        return self.attributes.outputs

    @outputs.setter
    def outputs(self, outputs: Optional[list[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.outputs = outputs

    @property
    def code(self) -> Optional[str]:
        return self.attributes.code

    @code.setter
    def code(self, code: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.code = code

    @property
    def sql(self) -> Optional[str]:
        return self.attributes.sql

    @sql.setter
    def sql(self, sql: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql = sql

    @property
    def ast(self) -> Optional[str]:
        return self.attributes.ast

    @ast.setter
    def ast(self, ast: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ast = ast

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("DbtColumnProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtColumnProcess":
            raise ValueError("must be DbtColumnProcess")
        return v

    class Attributes(Dbt.Attributes):
        dbt_column_process_job_status: Optional[str] = Field(
            None, description="", alias="dbtColumnProcessJobStatus"
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
        inputs: Optional[list[Catalog]] = Field(None, description="", alias="inputs")
        outputs: Optional[list[Catalog]] = Field(None, description="", alias="outputs")
        code: Optional[str] = Field(None, description="", alias="code")
        sql: Optional[str] = Field(None, description="", alias="sql")
        ast: Optional[str] = Field(None, description="", alias="ast")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        process: Optional[Process] = Field(
            None, description="", alias="process"
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


class Kafka(EventStore):
    """Description"""

    def __setattr__(self, name, value):
        if name in Kafka._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Kafka", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Kafka":
            raise ValueError("must be Kafka")
        return v

    class Attributes(EventStore.Attributes):
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

    attributes: "Kafka.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Metric(DataQuality):
    """Description"""

    def __setattr__(self, name, value):
        if name in Metric._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "metric_type",
        "metric_s_q_l",
        "metric_filters",
        "metric_time_grains",
        "terms",
    ]

    @property
    def metric_type(self) -> Optional[str]:
        return self.attributes.metric_type

    @metric_type.setter
    def metric_type(self, metric_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_type = metric_type

    @property
    def metric_s_q_l(self) -> Optional[str]:
        return self.attributes.metric_s_q_l

    @metric_s_q_l.setter
    def metric_s_q_l(self, metric_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_s_q_l = metric_s_q_l

    @property
    def metric_filters(self) -> Optional[str]:
        return self.attributes.metric_filters

    @metric_filters.setter
    def metric_filters(self, metric_filters: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_filters = metric_filters

    @property
    def metric_time_grains(self) -> Optional[set[str]]:
        return self.attributes.metric_time_grains

    @metric_time_grains.setter
    def metric_time_grains(self, metric_time_grains: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_time_grains = metric_time_grains

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Metric", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Metric":
            raise ValueError("must be Metric")
        return v

    class Attributes(DataQuality.Attributes):
        metric_type: Optional[str] = Field(None, description="", alias="metricType")
        metric_s_q_l: Optional[str] = Field(None, description="", alias="metricSQL")
        metric_filters: Optional[str] = Field(
            None, description="", alias="metricFilters"
        )
        metric_time_grains: Optional[set[str]] = Field(
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

    def __setattr__(self, name, value):
        if name in Metabase._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "metabase_collection_name",
        "metabase_collection_qualified_name",
        "terms",
    ]

    @property
    def metabase_collection_name(self) -> Optional[str]:
        return self.attributes.metabase_collection_name

    @metabase_collection_name.setter
    def metabase_collection_name(self, metabase_collection_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_collection_name = metabase_collection_name

    @property
    def metabase_collection_qualified_name(self) -> Optional[str]:
        return self.attributes.metabase_collection_qualified_name

    @metabase_collection_qualified_name.setter
    def metabase_collection_qualified_name(
        self, metabase_collection_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_collection_qualified_name = (
            metabase_collection_qualified_name
        )

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Metabase", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Metabase":
            raise ValueError("must be Metabase")
        return v

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


class QuickSight(BI):
    """Description"""

    def __setattr__(self, name, value):
        if name in QuickSight._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_id",
        "quick_sight_sheet_id",
        "quick_sight_sheet_name",
        "terms",
    ]

    @property
    def quick_sight_id(self) -> Optional[str]:
        return self.attributes.quick_sight_id

    @quick_sight_id.setter
    def quick_sight_id(self, quick_sight_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_id = quick_sight_id

    @property
    def quick_sight_sheet_id(self) -> Optional[str]:
        return self.attributes.quick_sight_sheet_id

    @quick_sight_sheet_id.setter
    def quick_sight_sheet_id(self, quick_sight_sheet_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_sheet_id = quick_sight_sheet_id

    @property
    def quick_sight_sheet_name(self) -> Optional[str]:
        return self.attributes.quick_sight_sheet_name

    @quick_sight_sheet_name.setter
    def quick_sight_sheet_name(self, quick_sight_sheet_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_sheet_name = quick_sight_sheet_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QuickSight", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSight":
            raise ValueError("must be QuickSight")
        return v

    class Attributes(BI.Attributes):
        quick_sight_id: Optional[str] = Field(
            None, description="", alias="quickSightId"
        )
        quick_sight_sheet_id: Optional[str] = Field(
            None, description="", alias="quickSightSheetId"
        )
        quick_sight_sheet_name: Optional[str] = Field(
            None, description="", alias="quickSightSheetName"
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

    attributes: "QuickSight.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Thoughtspot(BI):
    """Description"""

    def __setattr__(self, name, value):
        if name in Thoughtspot._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "thoughtspot_chart_type",
        "thoughtspot_question_text",
        "terms",
    ]

    @property
    def thoughtspot_chart_type(self) -> Optional[str]:
        return self.attributes.thoughtspot_chart_type

    @thoughtspot_chart_type.setter
    def thoughtspot_chart_type(self, thoughtspot_chart_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_chart_type = thoughtspot_chart_type

    @property
    def thoughtspot_question_text(self) -> Optional[str]:
        return self.attributes.thoughtspot_question_text

    @thoughtspot_question_text.setter
    def thoughtspot_question_text(self, thoughtspot_question_text: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_question_text = thoughtspot_question_text

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Thoughtspot", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Thoughtspot":
            raise ValueError("must be Thoughtspot")
        return v

    class Attributes(BI.Attributes):
        thoughtspot_chart_type: Optional[str] = Field(
            None, description="", alias="thoughtspotChartType"
        )
        thoughtspot_question_text: Optional[str] = Field(
            None, description="", alias="thoughtspotQuestionText"
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

    attributes: "Thoughtspot.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBI(BI):
    """Description"""

    def __setattr__(self, name, value):
        if name in PowerBI._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "power_b_i_is_hidden",
        "power_b_i_table_qualified_name",
        "power_b_i_format_string",
        "power_b_i_endorsement",
        "terms",
    ]

    @property
    def power_b_i_is_hidden(self) -> Optional[bool]:
        return self.attributes.power_b_i_is_hidden

    @power_b_i_is_hidden.setter
    def power_b_i_is_hidden(self, power_b_i_is_hidden: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_is_hidden = power_b_i_is_hidden

    @property
    def power_b_i_table_qualified_name(self) -> Optional[str]:
        return self.attributes.power_b_i_table_qualified_name

    @power_b_i_table_qualified_name.setter
    def power_b_i_table_qualified_name(
        self, power_b_i_table_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_table_qualified_name = power_b_i_table_qualified_name

    @property
    def power_b_i_format_string(self) -> Optional[str]:
        return self.attributes.power_b_i_format_string

    @power_b_i_format_string.setter
    def power_b_i_format_string(self, power_b_i_format_string: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_format_string = power_b_i_format_string

    @property
    def power_b_i_endorsement(self) -> Optional[PowerbiEndorsement]:
        return self.attributes.power_b_i_endorsement

    @power_b_i_endorsement.setter
    def power_b_i_endorsement(
        self, power_b_i_endorsement: Optional[PowerbiEndorsement]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_endorsement = power_b_i_endorsement

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PowerBI", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBI":
            raise ValueError("must be PowerBI")
        return v

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
        power_b_i_endorsement: Optional[PowerbiEndorsement] = Field(
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

    def __setattr__(self, name, value):
        if name in Preset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "preset_workspace_id",
        "preset_workspace_qualified_name",
        "preset_dashboard_id",
        "preset_dashboard_qualified_name",
        "terms",
    ]

    @property
    def preset_workspace_id(self) -> Optional[int]:
        return self.attributes.preset_workspace_id

    @preset_workspace_id.setter
    def preset_workspace_id(self, preset_workspace_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_id = preset_workspace_id

    @property
    def preset_workspace_qualified_name(self) -> Optional[str]:
        return self.attributes.preset_workspace_qualified_name

    @preset_workspace_qualified_name.setter
    def preset_workspace_qualified_name(
        self, preset_workspace_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_qualified_name = (
            preset_workspace_qualified_name
        )

    @property
    def preset_dashboard_id(self) -> Optional[int]:
        return self.attributes.preset_dashboard_id

    @preset_dashboard_id.setter
    def preset_dashboard_id(self, preset_dashboard_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_id = preset_dashboard_id

    @property
    def preset_dashboard_qualified_name(self) -> Optional[str]:
        return self.attributes.preset_dashboard_qualified_name

    @preset_dashboard_qualified_name.setter
    def preset_dashboard_qualified_name(
        self, preset_dashboard_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_qualified_name = (
            preset_dashboard_qualified_name
        )

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Preset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Preset":
            raise ValueError("must be Preset")
        return v

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

    def __setattr__(self, name, value):
        if name in Mode._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "mode_id",
        "mode_token",
        "mode_workspace_name",
        "mode_workspace_username",
        "mode_workspace_qualified_name",
        "mode_report_name",
        "mode_report_qualified_name",
        "mode_query_name",
        "mode_query_qualified_name",
        "terms",
    ]

    @property
    def mode_id(self) -> Optional[str]:
        return self.attributes.mode_id

    @mode_id.setter
    def mode_id(self, mode_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_id = mode_id

    @property
    def mode_token(self) -> Optional[str]:
        return self.attributes.mode_token

    @mode_token.setter
    def mode_token(self, mode_token: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_token = mode_token

    @property
    def mode_workspace_name(self) -> Optional[str]:
        return self.attributes.mode_workspace_name

    @mode_workspace_name.setter
    def mode_workspace_name(self, mode_workspace_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_workspace_name = mode_workspace_name

    @property
    def mode_workspace_username(self) -> Optional[str]:
        return self.attributes.mode_workspace_username

    @mode_workspace_username.setter
    def mode_workspace_username(self, mode_workspace_username: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_workspace_username = mode_workspace_username

    @property
    def mode_workspace_qualified_name(self) -> Optional[str]:
        return self.attributes.mode_workspace_qualified_name

    @mode_workspace_qualified_name.setter
    def mode_workspace_qualified_name(
        self, mode_workspace_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_workspace_qualified_name = mode_workspace_qualified_name

    @property
    def mode_report_name(self) -> Optional[str]:
        return self.attributes.mode_report_name

    @mode_report_name.setter
    def mode_report_name(self, mode_report_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report_name = mode_report_name

    @property
    def mode_report_qualified_name(self) -> Optional[str]:
        return self.attributes.mode_report_qualified_name

    @mode_report_qualified_name.setter
    def mode_report_qualified_name(self, mode_report_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report_qualified_name = mode_report_qualified_name

    @property
    def mode_query_name(self) -> Optional[str]:
        return self.attributes.mode_query_name

    @mode_query_name.setter
    def mode_query_name(self, mode_query_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_name = mode_query_name

    @property
    def mode_query_qualified_name(self) -> Optional[str]:
        return self.attributes.mode_query_qualified_name

    @mode_query_qualified_name.setter
    def mode_query_qualified_name(self, mode_query_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_qualified_name = mode_query_qualified_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Mode", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Mode":
            raise ValueError("must be Mode")
        return v

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


class Sigma(BI):
    """Description"""

    def __setattr__(self, name, value):
        if name in Sigma._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "sigma_workbook_qualified_name",
        "sigma_workbook_name",
        "sigma_page_qualified_name",
        "sigma_page_name",
        "sigma_data_element_qualified_name",
        "sigma_data_element_name",
        "terms",
    ]

    @property
    def sigma_workbook_qualified_name(self) -> Optional[str]:
        return self.attributes.sigma_workbook_qualified_name

    @sigma_workbook_qualified_name.setter
    def sigma_workbook_qualified_name(
        self, sigma_workbook_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_workbook_qualified_name = sigma_workbook_qualified_name

    @property
    def sigma_workbook_name(self) -> Optional[str]:
        return self.attributes.sigma_workbook_name

    @sigma_workbook_name.setter
    def sigma_workbook_name(self, sigma_workbook_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_workbook_name = sigma_workbook_name

    @property
    def sigma_page_qualified_name(self) -> Optional[str]:
        return self.attributes.sigma_page_qualified_name

    @sigma_page_qualified_name.setter
    def sigma_page_qualified_name(self, sigma_page_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_page_qualified_name = sigma_page_qualified_name

    @property
    def sigma_page_name(self) -> Optional[str]:
        return self.attributes.sigma_page_name

    @sigma_page_name.setter
    def sigma_page_name(self, sigma_page_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_page_name = sigma_page_name

    @property
    def sigma_data_element_qualified_name(self) -> Optional[str]:
        return self.attributes.sigma_data_element_qualified_name

    @sigma_data_element_qualified_name.setter
    def sigma_data_element_qualified_name(
        self, sigma_data_element_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_qualified_name = (
            sigma_data_element_qualified_name
        )

    @property
    def sigma_data_element_name(self) -> Optional[str]:
        return self.attributes.sigma_data_element_name

    @sigma_data_element_name.setter
    def sigma_data_element_name(self, sigma_data_element_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_name = sigma_data_element_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Sigma", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Sigma":
            raise ValueError("must be Sigma")
        return v

    class Attributes(BI.Attributes):
        sigma_workbook_qualified_name: Optional[str] = Field(
            None, description="", alias="sigmaWorkbookQualifiedName"
        )
        sigma_workbook_name: Optional[str] = Field(
            None, description="", alias="sigmaWorkbookName"
        )
        sigma_page_qualified_name: Optional[str] = Field(
            None, description="", alias="sigmaPageQualifiedName"
        )
        sigma_page_name: Optional[str] = Field(
            None, description="", alias="sigmaPageName"
        )
        sigma_data_element_qualified_name: Optional[str] = Field(
            None, description="", alias="sigmaDataElementQualifiedName"
        )
        sigma_data_element_name: Optional[str] = Field(
            None, description="", alias="sigmaDataElementName"
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

    attributes: "Sigma.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Qlik(BI):
    """Description"""

    def __setattr__(self, name, value):
        if name in Qlik._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "qlik_id",
        "qlik_q_r_i",
        "qlik_space_id",
        "qlik_space_qualified_name",
        "qlik_app_id",
        "qlik_app_qualified_name",
        "qlik_owner_id",
        "qlik_is_published",
        "terms",
    ]

    @property
    def qlik_id(self) -> Optional[str]:
        return self.attributes.qlik_id

    @qlik_id.setter
    def qlik_id(self, qlik_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_id = qlik_id

    @property
    def qlik_q_r_i(self) -> Optional[str]:
        return self.attributes.qlik_q_r_i

    @qlik_q_r_i.setter
    def qlik_q_r_i(self, qlik_q_r_i: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_q_r_i = qlik_q_r_i

    @property
    def qlik_space_id(self) -> Optional[str]:
        return self.attributes.qlik_space_id

    @qlik_space_id.setter
    def qlik_space_id(self, qlik_space_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space_id = qlik_space_id

    @property
    def qlik_space_qualified_name(self) -> Optional[str]:
        return self.attributes.qlik_space_qualified_name

    @qlik_space_qualified_name.setter
    def qlik_space_qualified_name(self, qlik_space_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space_qualified_name = qlik_space_qualified_name

    @property
    def qlik_app_id(self) -> Optional[str]:
        return self.attributes.qlik_app_id

    @qlik_app_id.setter
    def qlik_app_id(self, qlik_app_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_app_id = qlik_app_id

    @property
    def qlik_app_qualified_name(self) -> Optional[str]:
        return self.attributes.qlik_app_qualified_name

    @qlik_app_qualified_name.setter
    def qlik_app_qualified_name(self, qlik_app_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_app_qualified_name = qlik_app_qualified_name

    @property
    def qlik_owner_id(self) -> Optional[str]:
        return self.attributes.qlik_owner_id

    @qlik_owner_id.setter
    def qlik_owner_id(self, qlik_owner_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_owner_id = qlik_owner_id

    @property
    def qlik_is_published(self) -> Optional[bool]:
        return self.attributes.qlik_is_published

    @qlik_is_published.setter
    def qlik_is_published(self, qlik_is_published: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_is_published = qlik_is_published

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Qlik", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Qlik":
            raise ValueError("must be Qlik")
        return v

    class Attributes(BI.Attributes):
        qlik_id: Optional[str] = Field(None, description="", alias="qlikId")
        qlik_q_r_i: Optional[str] = Field(None, description="", alias="qlikQRI")
        qlik_space_id: Optional[str] = Field(None, description="", alias="qlikSpaceId")
        qlik_space_qualified_name: Optional[str] = Field(
            None, description="", alias="qlikSpaceQualifiedName"
        )
        qlik_app_id: Optional[str] = Field(None, description="", alias="qlikAppId")
        qlik_app_qualified_name: Optional[str] = Field(
            None, description="", alias="qlikAppQualifiedName"
        )
        qlik_owner_id: Optional[str] = Field(None, description="", alias="qlikOwnerId")
        qlik_is_published: Optional[bool] = Field(
            None, description="", alias="qlikIsPublished"
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

    attributes: "Qlik.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Tableau(BI):
    """Description"""

    def __setattr__(self, name, value):
        if name in Tableau._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Tableau", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Tableau":
            raise ValueError("must be Tableau")
        return v

    class Attributes(BI.Attributes):
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

    attributes: "Tableau.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Looker(BI):
    """Description"""

    def __setattr__(self, name, value):
        if name in Looker._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Looker", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Looker":
            raise ValueError("must be Looker")
        return v

    class Attributes(BI.Attributes):
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

    attributes: "Looker.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Redash(BI):
    """Description"""

    def __setattr__(self, name, value):
        if name in Redash._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "redash_is_published",
        "terms",
    ]

    @property
    def redash_is_published(self) -> Optional[bool]:
        return self.attributes.redash_is_published

    @redash_is_published.setter
    def redash_is_published(self, redash_is_published: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_is_published = redash_is_published

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Redash", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Redash":
            raise ValueError("must be Redash")
        return v

    class Attributes(BI.Attributes):
        redash_is_published: Optional[bool] = Field(
            None, description="", alias="redashIsPublished"
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

    attributes: "Redash.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Salesforce(SaaS):
    """Description"""

    def __setattr__(self, name, value):
        if name in Salesforce._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "organization_qualified_name",
        "api_name",
        "terms",
    ]

    @property
    def organization_qualified_name(self) -> Optional[str]:
        return self.attributes.organization_qualified_name

    @organization_qualified_name.setter
    def organization_qualified_name(self, organization_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.organization_qualified_name = organization_qualified_name

    @property
    def api_name(self) -> Optional[str]:
        return self.attributes.api_name

    @api_name.setter
    def api_name(self, api_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_name = api_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Salesforce", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Salesforce":
            raise ValueError("must be Salesforce")
        return v

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

    def __setattr__(self, name, value):
        if name in DbtModelColumn._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "dbt_model_qualified_name",
        "dbt_model_column_data_type",
        "dbt_model_column_order",
        "terms",
    ]

    @property
    def dbt_model_qualified_name(self) -> Optional[str]:
        return self.attributes.dbt_model_qualified_name

    @dbt_model_qualified_name.setter
    def dbt_model_qualified_name(self, dbt_model_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_qualified_name = dbt_model_qualified_name

    @property
    def dbt_model_column_data_type(self) -> Optional[str]:
        return self.attributes.dbt_model_column_data_type

    @dbt_model_column_data_type.setter
    def dbt_model_column_data_type(self, dbt_model_column_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_column_data_type = dbt_model_column_data_type

    @property
    def dbt_model_column_order(self) -> Optional[int]:
        return self.attributes.dbt_model_column_order

    @dbt_model_column_order.setter
    def dbt_model_column_order(self, dbt_model_column_order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_column_order = dbt_model_column_order

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("DbtModelColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtModelColumn":
            raise ValueError("must be DbtModelColumn")
        return v

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
        dbt_model_column_sql_columns: Optional[list[Column]] = Field(
            None, description="", alias="dbtModelColumnSqlColumns"
        )  # relationship
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

    def __setattr__(self, name, value):
        if name in DbtModel._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
        "terms",
    ]

    @property
    def dbt_status(self) -> Optional[str]:
        return self.attributes.dbt_status

    @dbt_status.setter
    def dbt_status(self, dbt_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_status = dbt_status

    @property
    def dbt_error(self) -> Optional[str]:
        return self.attributes.dbt_error

    @dbt_error.setter
    def dbt_error(self, dbt_error: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_error = dbt_error

    @property
    def dbt_raw_s_q_l(self) -> Optional[str]:
        return self.attributes.dbt_raw_s_q_l

    @dbt_raw_s_q_l.setter
    def dbt_raw_s_q_l(self, dbt_raw_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_raw_s_q_l = dbt_raw_s_q_l

    @property
    def dbt_compiled_s_q_l(self) -> Optional[str]:
        return self.attributes.dbt_compiled_s_q_l

    @dbt_compiled_s_q_l.setter
    def dbt_compiled_s_q_l(self, dbt_compiled_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_compiled_s_q_l = dbt_compiled_s_q_l

    @property
    def dbt_stats(self) -> Optional[str]:
        return self.attributes.dbt_stats

    @dbt_stats.setter
    def dbt_stats(self, dbt_stats: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_stats = dbt_stats

    @property
    def dbt_materialization_type(self) -> Optional[str]:
        return self.attributes.dbt_materialization_type

    @dbt_materialization_type.setter
    def dbt_materialization_type(self, dbt_materialization_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_materialization_type = dbt_materialization_type

    @property
    def dbt_model_compile_started_at(self) -> Optional[datetime]:
        return self.attributes.dbt_model_compile_started_at

    @dbt_model_compile_started_at.setter
    def dbt_model_compile_started_at(
        self, dbt_model_compile_started_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_compile_started_at = dbt_model_compile_started_at

    @property
    def dbt_model_compile_completed_at(self) -> Optional[datetime]:
        return self.attributes.dbt_model_compile_completed_at

    @dbt_model_compile_completed_at.setter
    def dbt_model_compile_completed_at(
        self, dbt_model_compile_completed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_compile_completed_at = dbt_model_compile_completed_at

    @property
    def dbt_model_execute_started_at(self) -> Optional[datetime]:
        return self.attributes.dbt_model_execute_started_at

    @dbt_model_execute_started_at.setter
    def dbt_model_execute_started_at(
        self, dbt_model_execute_started_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_execute_started_at = dbt_model_execute_started_at

    @property
    def dbt_model_execute_completed_at(self) -> Optional[datetime]:
        return self.attributes.dbt_model_execute_completed_at

    @dbt_model_execute_completed_at.setter
    def dbt_model_execute_completed_at(
        self, dbt_model_execute_completed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_execute_completed_at = dbt_model_execute_completed_at

    @property
    def dbt_model_execution_time(self) -> Optional[float]:
        return self.attributes.dbt_model_execution_time

    @dbt_model_execution_time.setter
    def dbt_model_execution_time(self, dbt_model_execution_time: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_execution_time = dbt_model_execution_time

    @property
    def dbt_model_run_generated_at(self) -> Optional[datetime]:
        return self.attributes.dbt_model_run_generated_at

    @dbt_model_run_generated_at.setter
    def dbt_model_run_generated_at(
        self, dbt_model_run_generated_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_run_generated_at = dbt_model_run_generated_at

    @property
    def dbt_model_run_elapsed_time(self) -> Optional[float]:
        return self.attributes.dbt_model_run_elapsed_time

    @dbt_model_run_elapsed_time.setter
    def dbt_model_run_elapsed_time(self, dbt_model_run_elapsed_time: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_run_elapsed_time = dbt_model_run_elapsed_time

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("DbtModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtModel":
            raise ValueError("must be DbtModel")
        return v

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
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        dbt_metrics: Optional[list[DbtMetric]] = Field(
            None, description="", alias="dbtMetrics"
        )  # relationship
        dbt_model_sql_assets: Optional[list[SQL]] = Field(
            None, description="", alias="dbtModelSqlAssets"
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

    def __setattr__(self, name, value):
        if name in DbtMetric._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
        "terms",
    ]

    @property
    def dbt_metric_filters(self) -> Optional[list[DbtMetricFilter]]:
        return self.attributes.dbt_metric_filters

    @dbt_metric_filters.setter
    def dbt_metric_filters(self, dbt_metric_filters: Optional[list[DbtMetricFilter]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_metric_filters = dbt_metric_filters

    @property
    def dbt_alias(self) -> Optional[str]:
        return self.attributes.dbt_alias

    @dbt_alias.setter
    def dbt_alias(self, dbt_alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_alias = dbt_alias

    @property
    def dbt_meta(self) -> Optional[str]:
        return self.attributes.dbt_meta

    @dbt_meta.setter
    def dbt_meta(self, dbt_meta: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_meta = dbt_meta

    @property
    def dbt_unique_id(self) -> Optional[str]:
        return self.attributes.dbt_unique_id

    @dbt_unique_id.setter
    def dbt_unique_id(self, dbt_unique_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_unique_id = dbt_unique_id

    @property
    def dbt_account_name(self) -> Optional[str]:
        return self.attributes.dbt_account_name

    @dbt_account_name.setter
    def dbt_account_name(self, dbt_account_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_account_name = dbt_account_name

    @property
    def dbt_project_name(self) -> Optional[str]:
        return self.attributes.dbt_project_name

    @dbt_project_name.setter
    def dbt_project_name(self, dbt_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_project_name = dbt_project_name

    @property
    def dbt_package_name(self) -> Optional[str]:
        return self.attributes.dbt_package_name

    @dbt_package_name.setter
    def dbt_package_name(self, dbt_package_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_package_name = dbt_package_name

    @property
    def dbt_job_name(self) -> Optional[str]:
        return self.attributes.dbt_job_name

    @dbt_job_name.setter
    def dbt_job_name(self, dbt_job_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_name = dbt_job_name

    @property
    def dbt_job_schedule(self) -> Optional[str]:
        return self.attributes.dbt_job_schedule

    @dbt_job_schedule.setter
    def dbt_job_schedule(self, dbt_job_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_schedule = dbt_job_schedule

    @property
    def dbt_job_status(self) -> Optional[str]:
        return self.attributes.dbt_job_status

    @dbt_job_status.setter
    def dbt_job_status(self, dbt_job_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_status = dbt_job_status

    @property
    def dbt_job_schedule_cron_humanized(self) -> Optional[str]:
        return self.attributes.dbt_job_schedule_cron_humanized

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
        return self.attributes.dbt_job_last_run

    @dbt_job_last_run.setter
    def dbt_job_last_run(self, dbt_job_last_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_last_run = dbt_job_last_run

    @property
    def dbt_job_next_run(self) -> Optional[datetime]:
        return self.attributes.dbt_job_next_run

    @dbt_job_next_run.setter
    def dbt_job_next_run(self, dbt_job_next_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run = dbt_job_next_run

    @property
    def dbt_job_next_run_humanized(self) -> Optional[str]:
        return self.attributes.dbt_job_next_run_humanized

    @dbt_job_next_run_humanized.setter
    def dbt_job_next_run_humanized(self, dbt_job_next_run_humanized: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run_humanized = dbt_job_next_run_humanized

    @property
    def dbt_environment_name(self) -> Optional[str]:
        return self.attributes.dbt_environment_name

    @dbt_environment_name.setter
    def dbt_environment_name(self, dbt_environment_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_name = dbt_environment_name

    @property
    def dbt_environment_dbt_version(self) -> Optional[str]:
        return self.attributes.dbt_environment_dbt_version

    @dbt_environment_dbt_version.setter
    def dbt_environment_dbt_version(self, dbt_environment_dbt_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_dbt_version = dbt_environment_dbt_version

    @property
    def dbt_tags(self) -> Optional[set[str]]:
        return self.attributes.dbt_tags

    @dbt_tags.setter
    def dbt_tags(self, dbt_tags: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tags = dbt_tags

    @property
    def dbt_connection_context(self) -> Optional[str]:
        return self.attributes.dbt_connection_context

    @dbt_connection_context.setter
    def dbt_connection_context(self, dbt_connection_context: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_connection_context = dbt_connection_context

    @property
    def dbt_semantic_layer_proxy_url(self) -> Optional[str]:
        return self.attributes.dbt_semantic_layer_proxy_url

    @dbt_semantic_layer_proxy_url.setter
    def dbt_semantic_layer_proxy_url(self, dbt_semantic_layer_proxy_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_semantic_layer_proxy_url = dbt_semantic_layer_proxy_url

    @property
    def metric_type(self) -> Optional[str]:
        return self.attributes.metric_type

    @metric_type.setter
    def metric_type(self, metric_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_type = metric_type

    @property
    def metric_s_q_l(self) -> Optional[str]:
        return self.attributes.metric_s_q_l

    @metric_s_q_l.setter
    def metric_s_q_l(self, metric_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_s_q_l = metric_s_q_l

    @property
    def metric_filters(self) -> Optional[str]:
        return self.attributes.metric_filters

    @metric_filters.setter
    def metric_filters(self, metric_filters: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_filters = metric_filters

    @property
    def metric_time_grains(self) -> Optional[set[str]]:
        return self.attributes.metric_time_grains

    @metric_time_grains.setter
    def metric_time_grains(self, metric_time_grains: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_time_grains = metric_time_grains

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("DbtMetric", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtMetric":
            raise ValueError("must be DbtMetric")
        return v

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

    def __setattr__(self, name, value):
        if name in DbtSource._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "dbt_state",
        "dbt_freshness_criteria",
        "terms",
    ]

    @property
    def dbt_state(self) -> Optional[str]:
        return self.attributes.dbt_state

    @dbt_state.setter
    def dbt_state(self, dbt_state: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_state = dbt_state

    @property
    def dbt_freshness_criteria(self) -> Optional[str]:
        return self.attributes.dbt_freshness_criteria

    @dbt_freshness_criteria.setter
    def dbt_freshness_criteria(self, dbt_freshness_criteria: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_freshness_criteria = dbt_freshness_criteria

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("DbtSource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtSource":
            raise ValueError("must be DbtSource")
        return v

    class Attributes(Dbt.Attributes):
        dbt_state: Optional[str] = Field(None, description="", alias="dbtState")
        dbt_freshness_criteria: Optional[str] = Field(
            None, description="", alias="dbtFreshnessCriteria"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        sql_assets: Optional[list[SQL]] = Field(
            None, description="", alias="sqlAssets"
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

    def __setattr__(self, name, value):
        if name in DbtProcess._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "dbt_process_job_status",
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
        "inputs",
        "outputs",
        "code",
        "sql",
        "ast",
        "terms",
    ]

    @property
    def dbt_process_job_status(self) -> Optional[str]:
        return self.attributes.dbt_process_job_status

    @dbt_process_job_status.setter
    def dbt_process_job_status(self, dbt_process_job_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_process_job_status = dbt_process_job_status

    @property
    def dbt_alias(self) -> Optional[str]:
        return self.attributes.dbt_alias

    @dbt_alias.setter
    def dbt_alias(self, dbt_alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_alias = dbt_alias

    @property
    def dbt_meta(self) -> Optional[str]:
        return self.attributes.dbt_meta

    @dbt_meta.setter
    def dbt_meta(self, dbt_meta: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_meta = dbt_meta

    @property
    def dbt_unique_id(self) -> Optional[str]:
        return self.attributes.dbt_unique_id

    @dbt_unique_id.setter
    def dbt_unique_id(self, dbt_unique_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_unique_id = dbt_unique_id

    @property
    def dbt_account_name(self) -> Optional[str]:
        return self.attributes.dbt_account_name

    @dbt_account_name.setter
    def dbt_account_name(self, dbt_account_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_account_name = dbt_account_name

    @property
    def dbt_project_name(self) -> Optional[str]:
        return self.attributes.dbt_project_name

    @dbt_project_name.setter
    def dbt_project_name(self, dbt_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_project_name = dbt_project_name

    @property
    def dbt_package_name(self) -> Optional[str]:
        return self.attributes.dbt_package_name

    @dbt_package_name.setter
    def dbt_package_name(self, dbt_package_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_package_name = dbt_package_name

    @property
    def dbt_job_name(self) -> Optional[str]:
        return self.attributes.dbt_job_name

    @dbt_job_name.setter
    def dbt_job_name(self, dbt_job_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_name = dbt_job_name

    @property
    def dbt_job_schedule(self) -> Optional[str]:
        return self.attributes.dbt_job_schedule

    @dbt_job_schedule.setter
    def dbt_job_schedule(self, dbt_job_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_schedule = dbt_job_schedule

    @property
    def dbt_job_status(self) -> Optional[str]:
        return self.attributes.dbt_job_status

    @dbt_job_status.setter
    def dbt_job_status(self, dbt_job_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_status = dbt_job_status

    @property
    def dbt_job_schedule_cron_humanized(self) -> Optional[str]:
        return self.attributes.dbt_job_schedule_cron_humanized

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
        return self.attributes.dbt_job_last_run

    @dbt_job_last_run.setter
    def dbt_job_last_run(self, dbt_job_last_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_last_run = dbt_job_last_run

    @property
    def dbt_job_next_run(self) -> Optional[datetime]:
        return self.attributes.dbt_job_next_run

    @dbt_job_next_run.setter
    def dbt_job_next_run(self, dbt_job_next_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run = dbt_job_next_run

    @property
    def dbt_job_next_run_humanized(self) -> Optional[str]:
        return self.attributes.dbt_job_next_run_humanized

    @dbt_job_next_run_humanized.setter
    def dbt_job_next_run_humanized(self, dbt_job_next_run_humanized: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run_humanized = dbt_job_next_run_humanized

    @property
    def dbt_environment_name(self) -> Optional[str]:
        return self.attributes.dbt_environment_name

    @dbt_environment_name.setter
    def dbt_environment_name(self, dbt_environment_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_name = dbt_environment_name

    @property
    def dbt_environment_dbt_version(self) -> Optional[str]:
        return self.attributes.dbt_environment_dbt_version

    @dbt_environment_dbt_version.setter
    def dbt_environment_dbt_version(self, dbt_environment_dbt_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_dbt_version = dbt_environment_dbt_version

    @property
    def dbt_tags(self) -> Optional[set[str]]:
        return self.attributes.dbt_tags

    @dbt_tags.setter
    def dbt_tags(self, dbt_tags: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tags = dbt_tags

    @property
    def dbt_connection_context(self) -> Optional[str]:
        return self.attributes.dbt_connection_context

    @dbt_connection_context.setter
    def dbt_connection_context(self, dbt_connection_context: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_connection_context = dbt_connection_context

    @property
    def dbt_semantic_layer_proxy_url(self) -> Optional[str]:
        return self.attributes.dbt_semantic_layer_proxy_url

    @dbt_semantic_layer_proxy_url.setter
    def dbt_semantic_layer_proxy_url(self, dbt_semantic_layer_proxy_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_semantic_layer_proxy_url = dbt_semantic_layer_proxy_url

    @property
    def inputs(self) -> Optional[list[Catalog]]:
        return self.attributes.inputs

    @inputs.setter
    def inputs(self, inputs: Optional[list[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inputs = inputs

    @property
    def outputs(self) -> Optional[list[Catalog]]:
        return self.attributes.outputs

    @outputs.setter
    def outputs(self, outputs: Optional[list[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.outputs = outputs

    @property
    def code(self) -> Optional[str]:
        return self.attributes.code

    @code.setter
    def code(self, code: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.code = code

    @property
    def sql(self) -> Optional[str]:
        return self.attributes.sql

    @sql.setter
    def sql(self, sql: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql = sql

    @property
    def ast(self) -> Optional[str]:
        return self.attributes.ast

    @ast.setter
    def ast(self, ast: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ast = ast

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("DbtProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtProcess":
            raise ValueError("must be DbtProcess")
        return v

    class Attributes(Dbt.Attributes):
        dbt_process_job_status: Optional[str] = Field(
            None, description="", alias="dbtProcessJobStatus"
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
        inputs: Optional[list[Catalog]] = Field(None, description="", alias="inputs")
        outputs: Optional[list[Catalog]] = Field(None, description="", alias="outputs")
        code: Optional[str] = Field(None, description="", alias="code")
        sql: Optional[str] = Field(None, description="", alias="sql")
        ast: Optional[str] = Field(None, description="", alias="ast")
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

    def __setattr__(self, name, value):
        if name in ReadmeTemplate._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "icon",
        "icon_type",
        "terms",
    ]

    @property
    def icon(self) -> Optional[str]:
        return self.attributes.icon

    @icon.setter
    def icon(self, icon: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon = icon

    @property
    def icon_type(self) -> Optional[IconType]:
        return self.attributes.icon_type

    @icon_type.setter
    def icon_type(self, icon_type: Optional[IconType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon_type = icon_type

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ReadmeTemplate", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ReadmeTemplate":
            raise ValueError("must be ReadmeTemplate")
        return v

    class Attributes(Resource.Attributes):
        icon: Optional[str] = Field(None, description="", alias="icon")
        icon_type: Optional[IconType] = Field(None, description="", alias="iconType")
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

    def __setattr__(self, name, value):
        if name in Readme._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Readme", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Readme":
            raise ValueError("must be Readme")
        return v

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

    class Attributes(Resource.Attributes):
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        internal: Optional[Internal] = Field(
            None, description="", alias="__internal"
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
        see_also: Optional[list[Readme]] = Field(
            None, description="", alias="seeAlso"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

        @classmethod
        # @validate_arguments()
        def create(
            cls, *, asset: Asset, content: str, asset_name: Optional[str] = None
        ) -> Readme.Attributes:
            validate_required_fields(["asset", "content"], [asset, content])
            if not asset.name:
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
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Link(Resource):
    """Description"""

    def __setattr__(self, name, value):
        if name in Link._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "icon",
        "icon_type",
        "terms",
    ]

    @property
    def icon(self) -> Optional[str]:
        return self.attributes.icon

    @icon.setter
    def icon(self, icon: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon = icon

    @property
    def icon_type(self) -> Optional[IconType]:
        return self.attributes.icon_type

    @icon_type.setter
    def icon_type(self, icon_type: Optional[IconType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon_type = icon_type

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Link", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Link":
            raise ValueError("must be Link")
        return v

    class Attributes(Resource.Attributes):
        icon: Optional[str] = Field(None, description="", alias="icon")
        icon_type: Optional[IconType] = Field(None, description="", alias="iconType")
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

    def __setattr__(self, name, value):
        if name in APISpec._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "api_spec_terms_of_service_url",
        "api_spec_contact_email",
        "api_spec_contact_name",
        "api_spec_contact_url",
        "api_spec_license_name",
        "api_spec_license_url",
        "api_spec_contract_version",
        "api_spec_service_alias",
        "terms",
    ]

    @property
    def api_spec_terms_of_service_url(self) -> Optional[str]:
        return self.attributes.api_spec_terms_of_service_url

    @api_spec_terms_of_service_url.setter
    def api_spec_terms_of_service_url(
        self, api_spec_terms_of_service_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_terms_of_service_url = api_spec_terms_of_service_url

    @property
    def api_spec_contact_email(self) -> Optional[str]:
        return self.attributes.api_spec_contact_email

    @api_spec_contact_email.setter
    def api_spec_contact_email(self, api_spec_contact_email: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_contact_email = api_spec_contact_email

    @property
    def api_spec_contact_name(self) -> Optional[str]:
        return self.attributes.api_spec_contact_name

    @api_spec_contact_name.setter
    def api_spec_contact_name(self, api_spec_contact_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_contact_name = api_spec_contact_name

    @property
    def api_spec_contact_url(self) -> Optional[str]:
        return self.attributes.api_spec_contact_url

    @api_spec_contact_url.setter
    def api_spec_contact_url(self, api_spec_contact_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_contact_url = api_spec_contact_url

    @property
    def api_spec_license_name(self) -> Optional[str]:
        return self.attributes.api_spec_license_name

    @api_spec_license_name.setter
    def api_spec_license_name(self, api_spec_license_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_license_name = api_spec_license_name

    @property
    def api_spec_license_url(self) -> Optional[str]:
        return self.attributes.api_spec_license_url

    @api_spec_license_url.setter
    def api_spec_license_url(self, api_spec_license_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_license_url = api_spec_license_url

    @property
    def api_spec_contract_version(self) -> Optional[str]:
        return self.attributes.api_spec_contract_version

    @api_spec_contract_version.setter
    def api_spec_contract_version(self, api_spec_contract_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_contract_version = api_spec_contract_version

    @property
    def api_spec_service_alias(self) -> Optional[str]:
        return self.attributes.api_spec_service_alias

    @api_spec_service_alias.setter
    def api_spec_service_alias(self, api_spec_service_alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_service_alias = api_spec_service_alias

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("APISpec", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "APISpec":
            raise ValueError("must be APISpec")
        return v

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

    def __setattr__(self, name, value):
        if name in APIPath._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "api_path_summary",
        "api_path_raw_u_r_i",
        "api_path_is_templated",
        "api_path_available_operations",
        "api_path_available_response_codes",
        "api_path_is_ingress_exposed",
        "terms",
    ]

    @property
    def api_path_summary(self) -> Optional[str]:
        return self.attributes.api_path_summary

    @api_path_summary.setter
    def api_path_summary(self, api_path_summary: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_summary = api_path_summary

    @property
    def api_path_raw_u_r_i(self) -> Optional[str]:
        return self.attributes.api_path_raw_u_r_i

    @api_path_raw_u_r_i.setter
    def api_path_raw_u_r_i(self, api_path_raw_u_r_i: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_raw_u_r_i = api_path_raw_u_r_i

    @property
    def api_path_is_templated(self) -> Optional[bool]:
        return self.attributes.api_path_is_templated

    @api_path_is_templated.setter
    def api_path_is_templated(self, api_path_is_templated: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_is_templated = api_path_is_templated

    @property
    def api_path_available_operations(self) -> Optional[set[str]]:
        return self.attributes.api_path_available_operations

    @api_path_available_operations.setter
    def api_path_available_operations(
        self, api_path_available_operations: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_available_operations = api_path_available_operations

    @property
    def api_path_available_response_codes(self) -> Optional[dict[str, str]]:
        return self.attributes.api_path_available_response_codes

    @api_path_available_response_codes.setter
    def api_path_available_response_codes(
        self, api_path_available_response_codes: Optional[dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_available_response_codes = (
            api_path_available_response_codes
        )

    @property
    def api_path_is_ingress_exposed(self) -> Optional[bool]:
        return self.attributes.api_path_is_ingress_exposed

    @api_path_is_ingress_exposed.setter
    def api_path_is_ingress_exposed(self, api_path_is_ingress_exposed: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_is_ingress_exposed = api_path_is_ingress_exposed

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("APIPath", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "APIPath":
            raise ValueError("must be APIPath")
        return v

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
        api_path_available_operations: Optional[set[str]] = Field(
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

    def __setattr__(self, name, value):
        if name in TablePartition._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
        "terms",
    ]

    @property
    def constraint(self) -> Optional[str]:
        return self.attributes.constraint

    @constraint.setter
    def constraint(self, constraint: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.constraint = constraint

    @property
    def column_count(self) -> Optional[int]:
        return self.attributes.column_count

    @column_count.setter
    def column_count(self, column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_count = column_count

    @property
    def row_count(self) -> Optional[int]:
        return self.attributes.row_count

    @row_count.setter
    def row_count(self, row_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.row_count = row_count

    @property
    def size_bytes(self) -> Optional[int]:
        return self.attributes.size_bytes

    @size_bytes.setter
    def size_bytes(self, size_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.size_bytes = size_bytes

    @property
    def alias(self) -> Optional[str]:
        return self.attributes.alias

    @alias.setter
    def alias(self, alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alias = alias

    @property
    def is_temporary(self) -> Optional[bool]:
        return self.attributes.is_temporary

    @is_temporary.setter
    def is_temporary(self, is_temporary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_temporary = is_temporary

    @property
    def is_query_preview(self) -> Optional[bool]:
        return self.attributes.is_query_preview

    @is_query_preview.setter
    def is_query_preview(self, is_query_preview: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_query_preview = is_query_preview

    @property
    def query_preview_config(self) -> Optional[dict[str, str]]:
        return self.attributes.query_preview_config

    @query_preview_config.setter
    def query_preview_config(self, query_preview_config: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_preview_config = query_preview_config

    @property
    def external_location(self) -> Optional[str]:
        return self.attributes.external_location

    @external_location.setter
    def external_location(self, external_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location = external_location

    @property
    def external_location_region(self) -> Optional[str]:
        return self.attributes.external_location_region

    @external_location_region.setter
    def external_location_region(self, external_location_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location_region = external_location_region

    @property
    def external_location_format(self) -> Optional[str]:
        return self.attributes.external_location_format

    @external_location_format.setter
    def external_location_format(self, external_location_format: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location_format = external_location_format

    @property
    def is_partitioned(self) -> Optional[bool]:
        return self.attributes.is_partitioned

    @is_partitioned.setter
    def is_partitioned(self, is_partitioned: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_partitioned = is_partitioned

    @property
    def partition_strategy(self) -> Optional[str]:
        return self.attributes.partition_strategy

    @partition_strategy.setter
    def partition_strategy(self, partition_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_strategy = partition_strategy

    @property
    def partition_count(self) -> Optional[int]:
        return self.attributes.partition_count

    @partition_count.setter
    def partition_count(self, partition_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_count = partition_count

    @property
    def partition_list(self) -> Optional[str]:
        return self.attributes.partition_list

    @partition_list.setter
    def partition_list(self, partition_list: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_list = partition_list

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("TablePartition", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TablePartition":
            raise ValueError("must be TablePartition")
        return v

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
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="sqlDbtModels"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="sqlDBTSources"
        )  # relationship

    attributes: "TablePartition.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Table(SQL):
    """Description"""

    def __setattr__(self, name, value):
        if name in Table._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
        "terms",
    ]

    @property
    def column_count(self) -> Optional[int]:
        return self.attributes.column_count

    @column_count.setter
    def column_count(self, column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_count = column_count

    @property
    def row_count(self) -> Optional[int]:
        return self.attributes.row_count

    @row_count.setter
    def row_count(self, row_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.row_count = row_count

    @property
    def size_bytes(self) -> Optional[int]:
        return self.attributes.size_bytes

    @size_bytes.setter
    def size_bytes(self, size_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.size_bytes = size_bytes

    @property
    def alias(self) -> Optional[str]:
        return self.attributes.alias

    @alias.setter
    def alias(self, alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alias = alias

    @property
    def is_temporary(self) -> Optional[bool]:
        return self.attributes.is_temporary

    @is_temporary.setter
    def is_temporary(self, is_temporary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_temporary = is_temporary

    @property
    def is_query_preview(self) -> Optional[bool]:
        return self.attributes.is_query_preview

    @is_query_preview.setter
    def is_query_preview(self, is_query_preview: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_query_preview = is_query_preview

    @property
    def query_preview_config(self) -> Optional[dict[str, str]]:
        return self.attributes.query_preview_config

    @query_preview_config.setter
    def query_preview_config(self, query_preview_config: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_preview_config = query_preview_config

    @property
    def external_location(self) -> Optional[str]:
        return self.attributes.external_location

    @external_location.setter
    def external_location(self, external_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location = external_location

    @property
    def external_location_region(self) -> Optional[str]:
        return self.attributes.external_location_region

    @external_location_region.setter
    def external_location_region(self, external_location_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location_region = external_location_region

    @property
    def external_location_format(self) -> Optional[str]:
        return self.attributes.external_location_format

    @external_location_format.setter
    def external_location_format(self, external_location_format: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location_format = external_location_format

    @property
    def is_partitioned(self) -> Optional[bool]:
        return self.attributes.is_partitioned

    @is_partitioned.setter
    def is_partitioned(self, is_partitioned: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_partitioned = is_partitioned

    @property
    def partition_strategy(self) -> Optional[str]:
        return self.attributes.partition_strategy

    @partition_strategy.setter
    def partition_strategy(self, partition_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_strategy = partition_strategy

    @property
    def partition_count(self) -> Optional[int]:
        return self.attributes.partition_count

    @partition_count.setter
    def partition_count(self, partition_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_count = partition_count

    @property
    def partition_list(self) -> Optional[str]:
        return self.attributes.partition_list

    @partition_list.setter
    def partition_list(self, partition_list: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_list = partition_list

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Table", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Table":
            raise ValueError("must be Table")
        return v

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
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
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
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="sqlDbtModels"
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="sqlDBTSources"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
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
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
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
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )

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


class Query(SQL):
    """Description"""

    def __setattr__(self, name, value):
        if name in Query._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
        "terms",
    ]

    @property
    def raw_query(self) -> Optional[str]:
        return self.attributes.raw_query

    @raw_query.setter
    def raw_query(self, raw_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.raw_query = raw_query

    @property
    def default_schema_qualified_name(self) -> Optional[str]:
        return self.attributes.default_schema_qualified_name

    @default_schema_qualified_name.setter
    def default_schema_qualified_name(
        self, default_schema_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.default_schema_qualified_name = default_schema_qualified_name

    @property
    def default_database_qualified_name(self) -> Optional[str]:
        return self.attributes.default_database_qualified_name

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
        return self.attributes.variables_schema_base64

    @variables_schema_base64.setter
    def variables_schema_base64(self, variables_schema_base64: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.variables_schema_base64 = variables_schema_base64

    @property
    def is_private(self) -> Optional[bool]:
        return self.attributes.is_private

    @is_private.setter
    def is_private(self, is_private: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_private = is_private

    @property
    def is_sql_snippet(self) -> Optional[bool]:
        return self.attributes.is_sql_snippet

    @is_sql_snippet.setter
    def is_sql_snippet(self, is_sql_snippet: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_sql_snippet = is_sql_snippet

    @property
    def parent_qualified_name(self) -> str:
        return self.attributes.parent_qualified_name

    @parent_qualified_name.setter
    def parent_qualified_name(self, parent_qualified_name: str):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_qualified_name = parent_qualified_name

    @property
    def collection_qualified_name(self) -> str:
        return self.attributes.collection_qualified_name

    @collection_qualified_name.setter
    def collection_qualified_name(self, collection_qualified_name: str):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.collection_qualified_name = collection_qualified_name

    @property
    def is_visual_query(self) -> Optional[bool]:
        return self.attributes.is_visual_query

    @is_visual_query.setter
    def is_visual_query(self, is_visual_query: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_visual_query = is_visual_query

    @property
    def visual_builder_schema_base64(self) -> Optional[str]:
        return self.attributes.visual_builder_schema_base64

    @visual_builder_schema_base64.setter
    def visual_builder_schema_base64(self, visual_builder_schema_base64: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.visual_builder_schema_base64 = visual_builder_schema_base64

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Query", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Query":
            raise ValueError("must be Query")
        return v

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
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
        )  # relationship
        readme: Optional[Readme] = Field(
            None, description="", alias="readme"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
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
        tables: Optional[list[Table]] = Field(
            None, description="", alias="tables"
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

    attributes: "Query.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Column(SQL):
    """Description"""

    def __setattr__(self, name, value):
        if name in Column._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "data_type",
        "sub_data_type",
        "order",
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
        "terms",
    ]

    @property
    def data_type(self) -> Optional[str]:
        return self.attributes.data_type

    @data_type.setter
    def data_type(self, data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_type = data_type

    @property
    def sub_data_type(self) -> Optional[str]:
        return self.attributes.sub_data_type

    @sub_data_type.setter
    def sub_data_type(self, sub_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sub_data_type = sub_data_type

    @property
    def order(self) -> Optional[int]:
        return self.attributes.order

    @order.setter
    def order(self, order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.order = order

    @property
    def is_partition(self) -> Optional[bool]:
        return self.attributes.is_partition

    @is_partition.setter
    def is_partition(self, is_partition: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_partition = is_partition

    @property
    def partition_order(self) -> Optional[int]:
        return self.attributes.partition_order

    @partition_order.setter
    def partition_order(self, partition_order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_order = partition_order

    @property
    def is_clustered(self) -> Optional[bool]:
        return self.attributes.is_clustered

    @is_clustered.setter
    def is_clustered(self, is_clustered: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_clustered = is_clustered

    @property
    def is_primary(self) -> Optional[bool]:
        return self.attributes.is_primary

    @is_primary.setter
    def is_primary(self, is_primary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_primary = is_primary

    @property
    def is_foreign(self) -> Optional[bool]:
        return self.attributes.is_foreign

    @is_foreign.setter
    def is_foreign(self, is_foreign: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_foreign = is_foreign

    @property
    def is_indexed(self) -> Optional[bool]:
        return self.attributes.is_indexed

    @is_indexed.setter
    def is_indexed(self, is_indexed: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_indexed = is_indexed

    @property
    def is_sort(self) -> Optional[bool]:
        return self.attributes.is_sort

    @is_sort.setter
    def is_sort(self, is_sort: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_sort = is_sort

    @property
    def is_dist(self) -> Optional[bool]:
        return self.attributes.is_dist

    @is_dist.setter
    def is_dist(self, is_dist: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_dist = is_dist

    @property
    def is_pinned(self) -> Optional[bool]:
        return self.attributes.is_pinned

    @is_pinned.setter
    def is_pinned(self, is_pinned: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_pinned = is_pinned

    @property
    def pinned_by(self) -> Optional[str]:
        return self.attributes.pinned_by

    @pinned_by.setter
    def pinned_by(self, pinned_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.pinned_by = pinned_by

    @property
    def pinned_at(self) -> Optional[datetime]:
        return self.attributes.pinned_at

    @pinned_at.setter
    def pinned_at(self, pinned_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.pinned_at = pinned_at

    @property
    def precision(self) -> Optional[int]:
        return self.attributes.precision

    @precision.setter
    def precision(self, precision: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.precision = precision

    @property
    def default_value(self) -> Optional[str]:
        return self.attributes.default_value

    @default_value.setter
    def default_value(self, default_value: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.default_value = default_value

    @property
    def is_nullable(self) -> Optional[bool]:
        return self.attributes.is_nullable

    @is_nullable.setter
    def is_nullable(self, is_nullable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_nullable = is_nullable

    @property
    def numeric_scale(self) -> Optional[float]:
        return self.attributes.numeric_scale

    @numeric_scale.setter
    def numeric_scale(self, numeric_scale: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.numeric_scale = numeric_scale

    @property
    def max_length(self) -> Optional[int]:
        return self.attributes.max_length

    @max_length.setter
    def max_length(self, max_length: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.max_length = max_length

    @property
    def validations(self) -> Optional[dict[str, str]]:
        return self.attributes.validations

    @validations.setter
    def validations(self, validations: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.validations = validations

    @property
    def column_distinct_values_count(self) -> Optional[int]:
        return self.attributes.column_distinct_values_count

    @column_distinct_values_count.setter
    def column_distinct_values_count(self, column_distinct_values_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_distinct_values_count = column_distinct_values_count

    @property
    def column_distinct_values_count_long(self) -> Optional[int]:
        return self.attributes.column_distinct_values_count_long

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
        return self.attributes.column_histogram

    @column_histogram.setter
    def column_histogram(self, column_histogram: Optional[Histogram]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_histogram = column_histogram

    @property
    def column_max(self) -> Optional[float]:
        return self.attributes.column_max

    @column_max.setter
    def column_max(self, column_max: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_max = column_max

    @property
    def column_min(self) -> Optional[float]:
        return self.attributes.column_min

    @column_min.setter
    def column_min(self, column_min: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_min = column_min

    @property
    def column_mean(self) -> Optional[float]:
        return self.attributes.column_mean

    @column_mean.setter
    def column_mean(self, column_mean: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_mean = column_mean

    @property
    def column_sum(self) -> Optional[float]:
        return self.attributes.column_sum

    @column_sum.setter
    def column_sum(self, column_sum: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_sum = column_sum

    @property
    def column_median(self) -> Optional[float]:
        return self.attributes.column_median

    @column_median.setter
    def column_median(self, column_median: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_median = column_median

    @property
    def column_standard_deviation(self) -> Optional[float]:
        return self.attributes.column_standard_deviation

    @column_standard_deviation.setter
    def column_standard_deviation(self, column_standard_deviation: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_standard_deviation = column_standard_deviation

    @property
    def column_unique_values_count(self) -> Optional[int]:
        return self.attributes.column_unique_values_count

    @column_unique_values_count.setter
    def column_unique_values_count(self, column_unique_values_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_unique_values_count = column_unique_values_count

    @property
    def column_unique_values_count_long(self) -> Optional[int]:
        return self.attributes.column_unique_values_count_long

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
        return self.attributes.column_average

    @column_average.setter
    def column_average(self, column_average: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_average = column_average

    @property
    def column_average_length(self) -> Optional[float]:
        return self.attributes.column_average_length

    @column_average_length.setter
    def column_average_length(self, column_average_length: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_average_length = column_average_length

    @property
    def column_duplicate_values_count(self) -> Optional[int]:
        return self.attributes.column_duplicate_values_count

    @column_duplicate_values_count.setter
    def column_duplicate_values_count(
        self, column_duplicate_values_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_duplicate_values_count = column_duplicate_values_count

    @property
    def column_duplicate_values_count_long(self) -> Optional[int]:
        return self.attributes.column_duplicate_values_count_long

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
        return self.attributes.column_maximum_string_length

    @column_maximum_string_length.setter
    def column_maximum_string_length(self, column_maximum_string_length: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_maximum_string_length = column_maximum_string_length

    @property
    def column_maxs(self) -> Optional[set[str]]:
        return self.attributes.column_maxs

    @column_maxs.setter
    def column_maxs(self, column_maxs: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_maxs = column_maxs

    @property
    def column_minimum_string_length(self) -> Optional[int]:
        return self.attributes.column_minimum_string_length

    @column_minimum_string_length.setter
    def column_minimum_string_length(self, column_minimum_string_length: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_minimum_string_length = column_minimum_string_length

    @property
    def column_mins(self) -> Optional[set[str]]:
        return self.attributes.column_mins

    @column_mins.setter
    def column_mins(self, column_mins: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_mins = column_mins

    @property
    def column_missing_values_count(self) -> Optional[int]:
        return self.attributes.column_missing_values_count

    @column_missing_values_count.setter
    def column_missing_values_count(self, column_missing_values_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_missing_values_count = column_missing_values_count

    @property
    def column_missing_values_count_long(self) -> Optional[int]:
        return self.attributes.column_missing_values_count_long

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
        return self.attributes.column_missing_values_percentage

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
        return self.attributes.column_uniqueness_percentage

    @column_uniqueness_percentage.setter
    def column_uniqueness_percentage(
        self, column_uniqueness_percentage: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_uniqueness_percentage = column_uniqueness_percentage

    @property
    def column_variance(self) -> Optional[float]:
        return self.attributes.column_variance

    @column_variance.setter
    def column_variance(self, column_variance: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_variance = column_variance

    @property
    def column_top_values(self) -> Optional[list[ColumnValueFrequencyMap]]:
        return self.attributes.column_top_values

    @column_top_values.setter
    def column_top_values(
        self, column_top_values: Optional[list[ColumnValueFrequencyMap]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_top_values = column_top_values

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Column", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Column":
            raise ValueError("must be Column")
        return v

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
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="sqlDbtModels"
        )  # relationship
        foreign_key_to: Optional[list[Column]] = Field(
            None, description="", alias="foreignKeyTo"
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="sqlDBTSources"
        )  # relationship
        foreign_key_from: Optional[Column] = Field(
            None, description="", alias="foreignKeyFrom"
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
        column_dbt_model_columns: Optional[list[DbtModelColumn]] = Field(
            None, description="", alias="columnDbtModelColumns"
        )  # relationship

        @classmethod
        # @validate_arguments()
        def create(
            cls, *, name: str, parent_qualified_name: str, parent_type: type, order: int
        ) -> Column.Attributes:
            if not name:
                raise ValueError("name cannot be blank")
            validate_required_fields(["parent_qualified_name"], [parent_qualified_name])
            fields = parent_qualified_name.split("/")
            if len(fields) != 6:
                raise ValueError("Invalid parent_qualified_name")
            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid parent_qualified_name") from e
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
            elif parent_type == View:
                ret_value.view_qualified_name = parent_qualified_name
                ret_value.view = View.ref_by_qualified_name(parent_qualified_name)
            elif parent_type == MaterialisedView:
                ret_value.view_qualified_name = parent_qualified_name
                ret_value.materialised_view = MaterialisedView.ref_by_qualified_name(
                    parent_qualified_name
                )
            else:
                raise ValueError(
                    "parent_type must be either Table, View or MaterializeView"
                )
            return ret_value

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

    attributes: "Column.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Schema(SQL):
    """Description"""

    def __setattr__(self, name, value):
        if name in Schema._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "table_count",
        "views_count",
        "terms",
    ]

    @property
    def table_count(self) -> Optional[int]:
        return self.attributes.table_count

    @table_count.setter
    def table_count(self, table_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_count = table_count

    @property
    def views_count(self) -> Optional[int]:
        return self.attributes.views_count

    @views_count.setter
    def views_count(self, views_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.views_count = views_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Schema", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Schema":
            raise ValueError("must be Schema")
        return v

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
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="sqlDbtModels"
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="sqlDBTSources"
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
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )

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


class SnowflakeStream(SQL):
    """Description"""

    def __setattr__(self, name, value):
        if name in SnowflakeStream._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "snowflake_stream_type",
        "snowflake_stream_source_type",
        "snowflake_stream_mode",
        "snowflake_stream_is_stale",
        "snowflake_stream_stale_after",
        "terms",
    ]

    @property
    def snowflake_stream_type(self) -> Optional[str]:
        return self.attributes.snowflake_stream_type

    @snowflake_stream_type.setter
    def snowflake_stream_type(self, snowflake_stream_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_type = snowflake_stream_type

    @property
    def snowflake_stream_source_type(self) -> Optional[str]:
        return self.attributes.snowflake_stream_source_type

    @snowflake_stream_source_type.setter
    def snowflake_stream_source_type(self, snowflake_stream_source_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_source_type = snowflake_stream_source_type

    @property
    def snowflake_stream_mode(self) -> Optional[str]:
        return self.attributes.snowflake_stream_mode

    @snowflake_stream_mode.setter
    def snowflake_stream_mode(self, snowflake_stream_mode: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_mode = snowflake_stream_mode

    @property
    def snowflake_stream_is_stale(self) -> Optional[bool]:
        return self.attributes.snowflake_stream_is_stale

    @snowflake_stream_is_stale.setter
    def snowflake_stream_is_stale(self, snowflake_stream_is_stale: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_is_stale = snowflake_stream_is_stale

    @property
    def snowflake_stream_stale_after(self) -> Optional[datetime]:
        return self.attributes.snowflake_stream_stale_after

    @snowflake_stream_stale_after.setter
    def snowflake_stream_stale_after(
        self, snowflake_stream_stale_after: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_stale_after = snowflake_stream_stale_after

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SnowflakeStream", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakeStream":
            raise ValueError("must be SnowflakeStream")
        return v

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
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="sqlDbtModels"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="sqlDBTSources"
        )  # relationship

    attributes: "SnowflakeStream.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SnowflakePipe(SQL):
    """Description"""

    def __setattr__(self, name, value):
        if name in SnowflakePipe._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "definition",
        "snowflake_pipe_is_auto_ingest_enabled",
        "snowflake_pipe_notification_channel_name",
        "terms",
    ]

    @property
    def definition(self) -> Optional[str]:
        return self.attributes.definition

    @definition.setter
    def definition(self, definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.definition = definition

    @property
    def snowflake_pipe_is_auto_ingest_enabled(self) -> Optional[bool]:
        return self.attributes.snowflake_pipe_is_auto_ingest_enabled

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
        return self.attributes.snowflake_pipe_notification_channel_name

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
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SnowflakePipe", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakePipe":
            raise ValueError("must be SnowflakePipe")
        return v

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
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="sqlDbtModels"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="sqlDBTSources"
        )  # relationship

    attributes: "SnowflakePipe.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Database(SQL):
    """Description"""

    def __setattr__(self, name, value):
        if name in Database._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "schema_count",
        "terms",
    ]

    @property
    def schema_count(self) -> Optional[int]:
        return self.attributes.schema_count

    @schema_count.setter
    def schema_count(self, schema_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_count = schema_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Database", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Database":
            raise ValueError("must be Database")
        return v

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
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="sqlDbtModels"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="sqlDBTSources"
        )  # relationship

        @classmethod
        # @validate_arguments()
        def create(
            cls, name: str, connection_qualified_name: str
        ) -> Database.Attributes:
            if not name:
                raise ValueError("name cannot be blank")
            validate_required_fields(
                ["connection_qualified_name"], [connection_qualified_name]
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
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )

    @classmethod
    # @validate_arguments()
    def create(cls, *, name: str, connection_qualified_name: str) -> Database:
        if not name:
            raise ValueError("name cannot be blank")
        validate_required_fields(
            ["connection_qualified_name"], [connection_qualified_name]
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


class Procedure(SQL):
    """Description"""

    def __setattr__(self, name, value):
        if name in Procedure._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "definition",
        "terms",
    ]

    @property
    def definition(self) -> str:
        return self.attributes.definition

    @definition.setter
    def definition(self, definition: str):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.definition = definition

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("Procedure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Procedure":
            raise ValueError("must be Procedure")
        return v

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
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="sqlDbtModels"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="sqlDBTSources"
        )  # relationship

    attributes: "Procedure.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class View(SQL):
    """Description"""

    def __setattr__(self, name, value):
        if name in View._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "column_count",
        "row_count",
        "size_bytes",
        "is_query_preview",
        "query_preview_config",
        "alias",
        "is_temporary",
        "definition",
        "terms",
    ]

    @property
    def column_count(self) -> Optional[int]:
        return self.attributes.column_count

    @column_count.setter
    def column_count(self, column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_count = column_count

    @property
    def row_count(self) -> Optional[int]:
        return self.attributes.row_count

    @row_count.setter
    def row_count(self, row_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.row_count = row_count

    @property
    def size_bytes(self) -> Optional[int]:
        return self.attributes.size_bytes

    @size_bytes.setter
    def size_bytes(self, size_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.size_bytes = size_bytes

    @property
    def is_query_preview(self) -> Optional[bool]:
        return self.attributes.is_query_preview

    @is_query_preview.setter
    def is_query_preview(self, is_query_preview: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_query_preview = is_query_preview

    @property
    def query_preview_config(self) -> Optional[dict[str, str]]:
        return self.attributes.query_preview_config

    @query_preview_config.setter
    def query_preview_config(self, query_preview_config: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_preview_config = query_preview_config

    @property
    def alias(self) -> Optional[str]:
        return self.attributes.alias

    @alias.setter
    def alias(self, alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alias = alias

    @property
    def is_temporary(self) -> Optional[bool]:
        return self.attributes.is_temporary

    @is_temporary.setter
    def is_temporary(self, is_temporary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_temporary = is_temporary

    @property
    def definition(self) -> Optional[str]:
        return self.attributes.definition

    @definition.setter
    def definition(self, definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.definition = definition

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("View", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "View":
            raise ValueError("must be View")
        return v

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
        dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="dbtSources"
        )  # relationship
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
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
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="sqlDbtModels"
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="sqlDBTSources"
        )  # relationship
        dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="dbtModels"
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
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
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
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )

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


class MaterialisedView(SQL):
    """Description"""

    def __setattr__(self, name, value):
        if name in MaterialisedView._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
        "terms",
    ]

    @property
    def refresh_mode(self) -> Optional[str]:
        return self.attributes.refresh_mode

    @refresh_mode.setter
    def refresh_mode(self, refresh_mode: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.refresh_mode = refresh_mode

    @property
    def refresh_method(self) -> Optional[str]:
        return self.attributes.refresh_method

    @refresh_method.setter
    def refresh_method(self, refresh_method: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.refresh_method = refresh_method

    @property
    def staleness(self) -> Optional[str]:
        return self.attributes.staleness

    @staleness.setter
    def staleness(self, staleness: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.staleness = staleness

    @property
    def stale_since_date(self) -> Optional[datetime]:
        return self.attributes.stale_since_date

    @stale_since_date.setter
    def stale_since_date(self, stale_since_date: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.stale_since_date = stale_since_date

    @property
    def column_count(self) -> Optional[int]:
        return self.attributes.column_count

    @column_count.setter
    def column_count(self, column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_count = column_count

    @property
    def row_count(self) -> Optional[int]:
        return self.attributes.row_count

    @row_count.setter
    def row_count(self, row_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.row_count = row_count

    @property
    def size_bytes(self) -> Optional[int]:
        return self.attributes.size_bytes

    @size_bytes.setter
    def size_bytes(self, size_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.size_bytes = size_bytes

    @property
    def is_query_preview(self) -> Optional[bool]:
        return self.attributes.is_query_preview

    @is_query_preview.setter
    def is_query_preview(self, is_query_preview: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_query_preview = is_query_preview

    @property
    def query_preview_config(self) -> Optional[dict[str, str]]:
        return self.attributes.query_preview_config

    @query_preview_config.setter
    def query_preview_config(self, query_preview_config: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_preview_config = query_preview_config

    @property
    def alias(self) -> Optional[str]:
        return self.attributes.alias

    @alias.setter
    def alias(self, alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alias = alias

    @property
    def is_temporary(self) -> Optional[bool]:
        return self.attributes.is_temporary

    @is_temporary.setter
    def is_temporary(self, is_temporary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_temporary = is_temporary

    @property
    def definition(self) -> Optional[str]:
        return self.attributes.definition

    @definition.setter
    def definition(self, definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.definition = definition

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("MaterialisedView", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MaterialisedView":
            raise ValueError("must be MaterialisedView")
        return v

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
        sql_dbt_models: Optional[list[DbtModel]] = Field(
            None, description="", alias="sqlDbtModels"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship
        sql_dbt_sources: Optional[list[DbtSource]] = Field(
            None, description="", alias="sqlDBTSources"
        )  # relationship

    attributes: "MaterialisedView.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class GCSObject(GCS):
    """Description"""

    def __setattr__(self, name, value):
        if name in GCSObject._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "gcs_bucket_name",
        "gcs_bucket_qualified_name",
        "gcs_object_size",
        "gcs_object_key",
        "gcs_object_media_link",
        "gcs_object_hold_type",
        "gcs_object_generation_id",
        "gcs_object_c_r_c32_c_hash",
        "gcs_object_m_d5_hash",
        "gcs_object_data_last_modified_time",
        "gcs_object_content_type",
        "gcs_object_content_encoding",
        "gcs_object_content_disposition",
        "gcs_object_content_language",
        "gcs_object_retention_expiration_date",
        "terms",
    ]

    @property
    def gcs_bucket_name(self) -> Optional[str]:
        return self.attributes.gcs_bucket_name

    @gcs_bucket_name.setter
    def gcs_bucket_name(self, gcs_bucket_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_name = gcs_bucket_name

    @property
    def gcs_bucket_qualified_name(self) -> Optional[str]:
        return self.attributes.gcs_bucket_qualified_name

    @gcs_bucket_qualified_name.setter
    def gcs_bucket_qualified_name(self, gcs_bucket_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_qualified_name = gcs_bucket_qualified_name

    @property
    def gcs_object_size(self) -> Optional[int]:
        return self.attributes.gcs_object_size

    @gcs_object_size.setter
    def gcs_object_size(self, gcs_object_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_size = gcs_object_size

    @property
    def gcs_object_key(self) -> Optional[str]:
        return self.attributes.gcs_object_key

    @gcs_object_key.setter
    def gcs_object_key(self, gcs_object_key: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_key = gcs_object_key

    @property
    def gcs_object_media_link(self) -> Optional[str]:
        return self.attributes.gcs_object_media_link

    @gcs_object_media_link.setter
    def gcs_object_media_link(self, gcs_object_media_link: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_media_link = gcs_object_media_link

    @property
    def gcs_object_hold_type(self) -> Optional[str]:
        return self.attributes.gcs_object_hold_type

    @gcs_object_hold_type.setter
    def gcs_object_hold_type(self, gcs_object_hold_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_hold_type = gcs_object_hold_type

    @property
    def gcs_object_generation_id(self) -> Optional[int]:
        return self.attributes.gcs_object_generation_id

    @gcs_object_generation_id.setter
    def gcs_object_generation_id(self, gcs_object_generation_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_generation_id = gcs_object_generation_id

    @property
    def gcs_object_c_r_c32_c_hash(self) -> Optional[str]:
        return self.attributes.gcs_object_c_r_c32_c_hash

    @gcs_object_c_r_c32_c_hash.setter
    def gcs_object_c_r_c32_c_hash(self, gcs_object_c_r_c32_c_hash: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_c_r_c32_c_hash = gcs_object_c_r_c32_c_hash

    @property
    def gcs_object_m_d5_hash(self) -> Optional[str]:
        return self.attributes.gcs_object_m_d5_hash

    @gcs_object_m_d5_hash.setter
    def gcs_object_m_d5_hash(self, gcs_object_m_d5_hash: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_m_d5_hash = gcs_object_m_d5_hash

    @property
    def gcs_object_data_last_modified_time(self) -> Optional[datetime]:
        return self.attributes.gcs_object_data_last_modified_time

    @gcs_object_data_last_modified_time.setter
    def gcs_object_data_last_modified_time(
        self, gcs_object_data_last_modified_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_data_last_modified_time = (
            gcs_object_data_last_modified_time
        )

    @property
    def gcs_object_content_type(self) -> Optional[str]:
        return self.attributes.gcs_object_content_type

    @gcs_object_content_type.setter
    def gcs_object_content_type(self, gcs_object_content_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_type = gcs_object_content_type

    @property
    def gcs_object_content_encoding(self) -> Optional[str]:
        return self.attributes.gcs_object_content_encoding

    @gcs_object_content_encoding.setter
    def gcs_object_content_encoding(self, gcs_object_content_encoding: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_encoding = gcs_object_content_encoding

    @property
    def gcs_object_content_disposition(self) -> Optional[str]:
        return self.attributes.gcs_object_content_disposition

    @gcs_object_content_disposition.setter
    def gcs_object_content_disposition(
        self, gcs_object_content_disposition: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_disposition = gcs_object_content_disposition

    @property
    def gcs_object_content_language(self) -> Optional[str]:
        return self.attributes.gcs_object_content_language

    @gcs_object_content_language.setter
    def gcs_object_content_language(self, gcs_object_content_language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_language = gcs_object_content_language

    @property
    def gcs_object_retention_expiration_date(self) -> Optional[datetime]:
        return self.attributes.gcs_object_retention_expiration_date

    @gcs_object_retention_expiration_date.setter
    def gcs_object_retention_expiration_date(
        self, gcs_object_retention_expiration_date: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_retention_expiration_date = (
            gcs_object_retention_expiration_date
        )

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("GCSObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "GCSObject":
            raise ValueError("must be GCSObject")
        return v

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
        gcs_object_data_last_modified_time: Optional[datetime] = Field(
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
        gcs_object_retention_expiration_date: Optional[datetime] = Field(
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

    def __setattr__(self, name, value):
        if name in GCSBucket._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "gcs_object_count",
        "gcs_bucket_versioning_enabled",
        "gcs_bucket_retention_locked",
        "gcs_bucket_retention_period",
        "gcs_bucket_retention_effective_time",
        "gcs_bucket_lifecycle_rules",
        "gcs_bucket_retention_policy",
        "terms",
    ]

    @property
    def gcs_object_count(self) -> Optional[int]:
        return self.attributes.gcs_object_count

    @gcs_object_count.setter
    def gcs_object_count(self, gcs_object_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_count = gcs_object_count

    @property
    def gcs_bucket_versioning_enabled(self) -> Optional[bool]:
        return self.attributes.gcs_bucket_versioning_enabled

    @gcs_bucket_versioning_enabled.setter
    def gcs_bucket_versioning_enabled(
        self, gcs_bucket_versioning_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_versioning_enabled = gcs_bucket_versioning_enabled

    @property
    def gcs_bucket_retention_locked(self) -> Optional[bool]:
        return self.attributes.gcs_bucket_retention_locked

    @gcs_bucket_retention_locked.setter
    def gcs_bucket_retention_locked(self, gcs_bucket_retention_locked: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_locked = gcs_bucket_retention_locked

    @property
    def gcs_bucket_retention_period(self) -> Optional[int]:
        return self.attributes.gcs_bucket_retention_period

    @gcs_bucket_retention_period.setter
    def gcs_bucket_retention_period(self, gcs_bucket_retention_period: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_period = gcs_bucket_retention_period

    @property
    def gcs_bucket_retention_effective_time(self) -> Optional[datetime]:
        return self.attributes.gcs_bucket_retention_effective_time

    @gcs_bucket_retention_effective_time.setter
    def gcs_bucket_retention_effective_time(
        self, gcs_bucket_retention_effective_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_effective_time = (
            gcs_bucket_retention_effective_time
        )

    @property
    def gcs_bucket_lifecycle_rules(self) -> Optional[str]:
        return self.attributes.gcs_bucket_lifecycle_rules

    @gcs_bucket_lifecycle_rules.setter
    def gcs_bucket_lifecycle_rules(self, gcs_bucket_lifecycle_rules: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_lifecycle_rules = gcs_bucket_lifecycle_rules

    @property
    def gcs_bucket_retention_policy(self) -> Optional[str]:
        return self.attributes.gcs_bucket_retention_policy

    @gcs_bucket_retention_policy.setter
    def gcs_bucket_retention_policy(self, gcs_bucket_retention_policy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_policy = gcs_bucket_retention_policy

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("GCSBucket", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "GCSBucket":
            raise ValueError("must be GCSBucket")
        return v

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
        gcs_bucket_retention_effective_time: Optional[datetime] = Field(
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


class ADLSAccount(ADLS):
    """Description"""

    def __setattr__(self, name, value):
        if name in ADLSAccount._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "adls_e_tag",
        "adls_encryption_type",
        "adls_account_resource_group",
        "adls_account_subscription",
        "adls_account_performance",
        "adls_account_replication",
        "adls_account_kind",
        "adls_primary_disk_state",
        "adls_account_provision_state",
        "adls_account_access_tier",
        "terms",
    ]

    @property
    def adls_e_tag(self) -> Optional[str]:
        return self.attributes.adls_e_tag

    @adls_e_tag.setter
    def adls_e_tag(self, adls_e_tag: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_e_tag = adls_e_tag

    @property
    def adls_encryption_type(self) -> Optional[ADLSEncryptionTypes]:
        return self.attributes.adls_encryption_type

    @adls_encryption_type.setter
    def adls_encryption_type(self, adls_encryption_type: Optional[ADLSEncryptionTypes]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_encryption_type = adls_encryption_type

    @property
    def adls_account_resource_group(self) -> Optional[str]:
        return self.attributes.adls_account_resource_group

    @adls_account_resource_group.setter
    def adls_account_resource_group(self, adls_account_resource_group: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_resource_group = adls_account_resource_group

    @property
    def adls_account_subscription(self) -> Optional[str]:
        return self.attributes.adls_account_subscription

    @adls_account_subscription.setter
    def adls_account_subscription(self, adls_account_subscription: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_subscription = adls_account_subscription

    @property
    def adls_account_performance(self) -> Optional[ADLSPerformance]:
        return self.attributes.adls_account_performance

    @adls_account_performance.setter
    def adls_account_performance(
        self, adls_account_performance: Optional[ADLSPerformance]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_performance = adls_account_performance

    @property
    def adls_account_replication(self) -> Optional[ADLSReplicationType]:
        return self.attributes.adls_account_replication

    @adls_account_replication.setter
    def adls_account_replication(
        self, adls_account_replication: Optional[ADLSReplicationType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_replication = adls_account_replication

    @property
    def adls_account_kind(self) -> Optional[ADLSStorageKind]:
        return self.attributes.adls_account_kind

    @adls_account_kind.setter
    def adls_account_kind(self, adls_account_kind: Optional[ADLSStorageKind]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_kind = adls_account_kind

    @property
    def adls_primary_disk_state(self) -> Optional[ADLSAccountStatus]:
        return self.attributes.adls_primary_disk_state

    @adls_primary_disk_state.setter
    def adls_primary_disk_state(
        self, adls_primary_disk_state: Optional[ADLSAccountStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_primary_disk_state = adls_primary_disk_state

    @property
    def adls_account_provision_state(self) -> Optional[ADLSProvisionState]:
        return self.attributes.adls_account_provision_state

    @adls_account_provision_state.setter
    def adls_account_provision_state(
        self, adls_account_provision_state: Optional[ADLSProvisionState]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_provision_state = adls_account_provision_state

    @property
    def adls_account_access_tier(self) -> Optional[ADLSAccessTier]:
        return self.attributes.adls_account_access_tier

    @adls_account_access_tier.setter
    def adls_account_access_tier(
        self, adls_account_access_tier: Optional[ADLSAccessTier]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_access_tier = adls_account_access_tier

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ADLSAccount", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADLSAccount":
            raise ValueError("must be ADLSAccount")
        return v

    class Attributes(ADLS.Attributes):
        adls_e_tag: Optional[str] = Field(None, description="", alias="adlsETag")
        adls_encryption_type: Optional[ADLSEncryptionTypes] = Field(
            None, description="", alias="adlsEncryptionType"
        )
        adls_account_resource_group: Optional[str] = Field(
            None, description="", alias="adlsAccountResourceGroup"
        )
        adls_account_subscription: Optional[str] = Field(
            None, description="", alias="adlsAccountSubscription"
        )
        adls_account_performance: Optional[ADLSPerformance] = Field(
            None, description="", alias="adlsAccountPerformance"
        )
        adls_account_replication: Optional[ADLSReplicationType] = Field(
            None, description="", alias="adlsAccountReplication"
        )
        adls_account_kind: Optional[ADLSStorageKind] = Field(
            None, description="", alias="adlsAccountKind"
        )
        adls_primary_disk_state: Optional[ADLSAccountStatus] = Field(
            None, description="", alias="adlsPrimaryDiskState"
        )
        adls_account_provision_state: Optional[ADLSProvisionState] = Field(
            None, description="", alias="adlsAccountProvisionState"
        )
        adls_account_access_tier: Optional[ADLSAccessTier] = Field(
            None, description="", alias="adlsAccountAccessTier"
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
        adls_containers: Optional[list[ADLSContainer]] = Field(
            None, description="", alias="adlsContainers"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "ADLSAccount.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ADLSContainer(ADLS):
    """Description"""

    def __setattr__(self, name, value):
        if name in ADLSContainer._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "adls_container_url",
        "adls_container_lease_state",
        "adls_container_lease_status",
        "adls_container_encryption_scope",
        "adls_container_version_level_immutability_support",
        "adls_object_count",
        "terms",
    ]

    @property
    def adls_container_url(self) -> Optional[str]:
        return self.attributes.adls_container_url

    @adls_container_url.setter
    def adls_container_url(self, adls_container_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_url = adls_container_url

    @property
    def adls_container_lease_state(self) -> Optional[ADLSLeaseState]:
        return self.attributes.adls_container_lease_state

    @adls_container_lease_state.setter
    def adls_container_lease_state(
        self, adls_container_lease_state: Optional[ADLSLeaseState]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_lease_state = adls_container_lease_state

    @property
    def adls_container_lease_status(self) -> Optional[ADLSLeaseStatus]:
        return self.attributes.adls_container_lease_status

    @adls_container_lease_status.setter
    def adls_container_lease_status(
        self, adls_container_lease_status: Optional[ADLSLeaseStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_lease_status = adls_container_lease_status

    @property
    def adls_container_encryption_scope(self) -> Optional[str]:
        return self.attributes.adls_container_encryption_scope

    @adls_container_encryption_scope.setter
    def adls_container_encryption_scope(
        self, adls_container_encryption_scope: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_encryption_scope = (
            adls_container_encryption_scope
        )

    @property
    def adls_container_version_level_immutability_support(self) -> Optional[bool]:
        return self.attributes.adls_container_version_level_immutability_support

    @adls_container_version_level_immutability_support.setter
    def adls_container_version_level_immutability_support(
        self, adls_container_version_level_immutability_support: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_version_level_immutability_support = (
            adls_container_version_level_immutability_support
        )

    @property
    def adls_object_count(self) -> Optional[int]:
        return self.attributes.adls_object_count

    @adls_object_count.setter
    def adls_object_count(self, adls_object_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_count = adls_object_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ADLSContainer", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADLSContainer":
            raise ValueError("must be ADLSContainer")
        return v

    class Attributes(ADLS.Attributes):
        adls_container_url: Optional[str] = Field(
            None, description="", alias="adlsContainerUrl"
        )
        adls_container_lease_state: Optional[ADLSLeaseState] = Field(
            None, description="", alias="adlsContainerLeaseState"
        )
        adls_container_lease_status: Optional[ADLSLeaseStatus] = Field(
            None, description="", alias="adlsContainerLeaseStatus"
        )
        adls_container_encryption_scope: Optional[str] = Field(
            None, description="", alias="adlsContainerEncryptionScope"
        )
        adls_container_version_level_immutability_support: Optional[bool] = Field(
            None, description="", alias="adlsContainerVersionLevelImmutabilitySupport"
        )
        adls_object_count: Optional[int] = Field(
            None, description="", alias="adlsObjectCount"
        )
        adls_objects: Optional[list[ADLSObject]] = Field(
            None, description="", alias="adlsObjects"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        adls_account: Optional[ADLSAccount] = Field(
            None, description="", alias="adlsAccount"
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

    attributes: "ADLSContainer.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ADLSObject(ADLS):
    """Description"""

    def __setattr__(self, name, value):
        if name in ADLSObject._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "adls_object_url",
        "adls_object_version_id",
        "adls_object_type",
        "adls_object_size",
        "adls_object_access_tier",
        "adls_object_access_tier_last_modified_time",
        "adls_object_archive_status",
        "adls_object_server_encrypted",
        "adls_object_version_level_immutability_support",
        "adls_object_cache_control",
        "adls_object_content_type",
        "adls_object_content_m_d5_hash",
        "adls_object_content_language",
        "adls_object_lease_status",
        "adls_object_lease_state",
        "adls_object_metadata",
        "adls_container_qualified_name",
        "terms",
    ]

    @property
    def adls_object_url(self) -> Optional[str]:
        return self.attributes.adls_object_url

    @adls_object_url.setter
    def adls_object_url(self, adls_object_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_url = adls_object_url

    @property
    def adls_object_version_id(self) -> Optional[str]:
        return self.attributes.adls_object_version_id

    @adls_object_version_id.setter
    def adls_object_version_id(self, adls_object_version_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_version_id = adls_object_version_id

    @property
    def adls_object_type(self) -> Optional[ADLSObjectType]:
        return self.attributes.adls_object_type

    @adls_object_type.setter
    def adls_object_type(self, adls_object_type: Optional[ADLSObjectType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_type = adls_object_type

    @property
    def adls_object_size(self) -> Optional[int]:
        return self.attributes.adls_object_size

    @adls_object_size.setter
    def adls_object_size(self, adls_object_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_size = adls_object_size

    @property
    def adls_object_access_tier(self) -> Optional[ADLSAccessTier]:
        return self.attributes.adls_object_access_tier

    @adls_object_access_tier.setter
    def adls_object_access_tier(
        self, adls_object_access_tier: Optional[ADLSAccessTier]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_access_tier = adls_object_access_tier

    @property
    def adls_object_access_tier_last_modified_time(self) -> Optional[datetime]:
        return self.attributes.adls_object_access_tier_last_modified_time

    @adls_object_access_tier_last_modified_time.setter
    def adls_object_access_tier_last_modified_time(
        self, adls_object_access_tier_last_modified_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_access_tier_last_modified_time = (
            adls_object_access_tier_last_modified_time
        )

    @property
    def adls_object_archive_status(self) -> Optional[ADLSObjectArchiveStatus]:
        return self.attributes.adls_object_archive_status

    @adls_object_archive_status.setter
    def adls_object_archive_status(
        self, adls_object_archive_status: Optional[ADLSObjectArchiveStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_archive_status = adls_object_archive_status

    @property
    def adls_object_server_encrypted(self) -> Optional[bool]:
        return self.attributes.adls_object_server_encrypted

    @adls_object_server_encrypted.setter
    def adls_object_server_encrypted(
        self, adls_object_server_encrypted: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_server_encrypted = adls_object_server_encrypted

    @property
    def adls_object_version_level_immutability_support(self) -> Optional[bool]:
        return self.attributes.adls_object_version_level_immutability_support

    @adls_object_version_level_immutability_support.setter
    def adls_object_version_level_immutability_support(
        self, adls_object_version_level_immutability_support: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_version_level_immutability_support = (
            adls_object_version_level_immutability_support
        )

    @property
    def adls_object_cache_control(self) -> Optional[str]:
        return self.attributes.adls_object_cache_control

    @adls_object_cache_control.setter
    def adls_object_cache_control(self, adls_object_cache_control: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_cache_control = adls_object_cache_control

    @property
    def adls_object_content_type(self) -> Optional[str]:
        return self.attributes.adls_object_content_type

    @adls_object_content_type.setter
    def adls_object_content_type(self, adls_object_content_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_content_type = adls_object_content_type

    @property
    def adls_object_content_m_d5_hash(self) -> Optional[str]:
        return self.attributes.adls_object_content_m_d5_hash

    @adls_object_content_m_d5_hash.setter
    def adls_object_content_m_d5_hash(
        self, adls_object_content_m_d5_hash: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_content_m_d5_hash = adls_object_content_m_d5_hash

    @property
    def adls_object_content_language(self) -> Optional[str]:
        return self.attributes.adls_object_content_language

    @adls_object_content_language.setter
    def adls_object_content_language(self, adls_object_content_language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_content_language = adls_object_content_language

    @property
    def adls_object_lease_status(self) -> Optional[ADLSLeaseStatus]:
        return self.attributes.adls_object_lease_status

    @adls_object_lease_status.setter
    def adls_object_lease_status(
        self, adls_object_lease_status: Optional[ADLSLeaseStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_lease_status = adls_object_lease_status

    @property
    def adls_object_lease_state(self) -> Optional[ADLSLeaseState]:
        return self.attributes.adls_object_lease_state

    @adls_object_lease_state.setter
    def adls_object_lease_state(
        self, adls_object_lease_state: Optional[ADLSLeaseState]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_lease_state = adls_object_lease_state

    @property
    def adls_object_metadata(self) -> Optional[dict[str, str]]:
        return self.attributes.adls_object_metadata

    @adls_object_metadata.setter
    def adls_object_metadata(self, adls_object_metadata: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_metadata = adls_object_metadata

    @property
    def adls_container_qualified_name(self) -> Optional[str]:
        return self.attributes.adls_container_qualified_name

    @adls_container_qualified_name.setter
    def adls_container_qualified_name(
        self, adls_container_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_qualified_name = adls_container_qualified_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ADLSObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADLSObject":
            raise ValueError("must be ADLSObject")
        return v

    class Attributes(ADLS.Attributes):
        adls_object_url: Optional[str] = Field(
            None, description="", alias="adlsObjectUrl"
        )
        adls_object_version_id: Optional[str] = Field(
            None, description="", alias="adlsObjectVersionId"
        )
        adls_object_type: Optional[ADLSObjectType] = Field(
            None, description="", alias="adlsObjectType"
        )
        adls_object_size: Optional[int] = Field(
            None, description="", alias="adlsObjectSize"
        )
        adls_object_access_tier: Optional[ADLSAccessTier] = Field(
            None, description="", alias="adlsObjectAccessTier"
        )
        adls_object_access_tier_last_modified_time: Optional[datetime] = Field(
            None, description="", alias="adlsObjectAccessTierLastModifiedTime"
        )
        adls_object_archive_status: Optional[ADLSObjectArchiveStatus] = Field(
            None, description="", alias="adlsObjectArchiveStatus"
        )
        adls_object_server_encrypted: Optional[bool] = Field(
            None, description="", alias="adlsObjectServerEncrypted"
        )
        adls_object_version_level_immutability_support: Optional[bool] = Field(
            None, description="", alias="adlsObjectVersionLevelImmutabilitySupport"
        )
        adls_object_cache_control: Optional[str] = Field(
            None, description="", alias="adlsObjectCacheControl"
        )
        adls_object_content_type: Optional[str] = Field(
            None, description="", alias="adlsObjectContentType"
        )
        adls_object_content_m_d5_hash: Optional[str] = Field(
            None, description="", alias="adlsObjectContentMD5Hash"
        )
        adls_object_content_language: Optional[str] = Field(
            None, description="", alias="adlsObjectContentLanguage"
        )
        adls_object_lease_status: Optional[ADLSLeaseStatus] = Field(
            None, description="", alias="adlsObjectLeaseStatus"
        )
        adls_object_lease_state: Optional[ADLSLeaseState] = Field(
            None, description="", alias="adlsObjectLeaseState"
        )
        adls_object_metadata: Optional[dict[str, str]] = Field(
            None, description="", alias="adlsObjectMetadata"
        )
        adls_container_qualified_name: Optional[str] = Field(
            None, description="", alias="adlsContainerQualifiedName"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        adls_container: Optional[ADLSContainer] = Field(
            None, description="", alias="adlsContainer"
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

    attributes: "ADLSObject.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class S3Bucket(S3):
    """Description"""

    def __setattr__(self, name, value):
        if name in S3Bucket._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "s3_object_count",
        "s3_bucket_versioning_enabled",
        "terms",
    ]

    @property
    def s3_object_count(self) -> Optional[int]:
        return self.attributes.s3_object_count

    @s3_object_count.setter
    def s3_object_count(self, s3_object_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_count = s3_object_count

    @property
    def s3_bucket_versioning_enabled(self) -> Optional[bool]:
        return self.attributes.s3_bucket_versioning_enabled

    @s3_bucket_versioning_enabled.setter
    def s3_bucket_versioning_enabled(
        self, s3_bucket_versioning_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_bucket_versioning_enabled = s3_bucket_versioning_enabled

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("S3Bucket", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "S3Bucket":
            raise ValueError("must be S3Bucket")
        return v

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

        @classmethod
        # @validate_arguments()
        def create(
            cls, *, name: str, connection_qualified_name: str, aws_arn: str
        ) -> S3Bucket.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name", "aws_arn"],
                [name, connection_qualified_name, aws_arn],
            )
            fields = connection_qualified_name.split("/")
            if len(fields) != 3:
                raise ValueError("Invalid connection_qualified_name")
            try:
                if fields[0].replace(" ", "") == "" or fields[2].replace(" ", "") == "":
                    raise ValueError("Invalid connection_qualified_name")
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
                if connector_type != AtlanConnectorType.S3:
                    raise ValueError("Connector type must be s3")
            except ValueError as e:
                raise ValueError("Invalid connection_qualified_name") from e
            return S3Bucket.Attributes(
                aws_arn=aws_arn,
                name=name,
                connection_qualified_name=connection_qualified_name,
                qualified_name=f"{connection_qualified_name}/{aws_arn}",
                connector_name=connector_type.value,
            )

    attributes: "S3Bucket.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )

    @classmethod
    # @validate_arguments()
    def create(
        cls, *, name: str, connection_qualified_name: str, aws_arn: str
    ) -> S3Bucket:
        validate_required_fields(
            ["name", "connection_qualified_name", "aws_arn"],
            [name, connection_qualified_name, aws_arn],
        )
        attributes = S3Bucket.Attributes.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
            aws_arn=aws_arn,
        )
        return cls(attributes=attributes)


class S3Object(S3):
    """Description"""

    def __setattr__(self, name, value):
        if name in S3Object._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "s3_object_last_modified_time",
        "s3_bucket_name",
        "s3_bucket_qualified_name",
        "s3_object_size",
        "s3_object_storage_class",
        "s3_object_key",
        "s3_object_content_type",
        "s3_object_content_disposition",
        "s3_object_version_id",
        "terms",
    ]

    @property
    def s3_object_last_modified_time(self) -> Optional[datetime]:
        return self.attributes.s3_object_last_modified_time

    @s3_object_last_modified_time.setter
    def s3_object_last_modified_time(
        self, s3_object_last_modified_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_last_modified_time = s3_object_last_modified_time

    @property
    def s3_bucket_name(self) -> Optional[str]:
        return self.attributes.s3_bucket_name

    @s3_bucket_name.setter
    def s3_bucket_name(self, s3_bucket_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_bucket_name = s3_bucket_name

    @property
    def s3_bucket_qualified_name(self) -> Optional[str]:
        return self.attributes.s3_bucket_qualified_name

    @s3_bucket_qualified_name.setter
    def s3_bucket_qualified_name(self, s3_bucket_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_bucket_qualified_name = s3_bucket_qualified_name

    @property
    def s3_object_size(self) -> Optional[int]:
        return self.attributes.s3_object_size

    @s3_object_size.setter
    def s3_object_size(self, s3_object_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_size = s3_object_size

    @property
    def s3_object_storage_class(self) -> Optional[str]:
        return self.attributes.s3_object_storage_class

    @s3_object_storage_class.setter
    def s3_object_storage_class(self, s3_object_storage_class: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_storage_class = s3_object_storage_class

    @property
    def s3_object_key(self) -> Optional[str]:
        return self.attributes.s3_object_key

    @s3_object_key.setter
    def s3_object_key(self, s3_object_key: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_key = s3_object_key

    @property
    def s3_object_content_type(self) -> Optional[str]:
        return self.attributes.s3_object_content_type

    @s3_object_content_type.setter
    def s3_object_content_type(self, s3_object_content_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_content_type = s3_object_content_type

    @property
    def s3_object_content_disposition(self) -> Optional[str]:
        return self.attributes.s3_object_content_disposition

    @s3_object_content_disposition.setter
    def s3_object_content_disposition(
        self, s3_object_content_disposition: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_content_disposition = s3_object_content_disposition

    @property
    def s3_object_version_id(self) -> Optional[str]:
        return self.attributes.s3_object_version_id

    @s3_object_version_id.setter
    def s3_object_version_id(self, s3_object_version_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_version_id = s3_object_version_id

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("S3Object", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "S3Object":
            raise ValueError("must be S3Object")
        return v

    class Attributes(S3.Attributes):
        s3_object_last_modified_time: Optional[datetime] = Field(
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

        @classmethod
        # @validate_arguments()
        def create(
            cls,
            *,
            name: str,
            connection_qualified_name: str,
            aws_arn: str,
            s3_bucket_qualified_name: Optional[str] = None,
        ) -> S3Object.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name", "aws_arn"],
                [name, connection_qualified_name, aws_arn],
            )
            fields = connection_qualified_name.split("/")
            if len(fields) != 3:
                raise ValueError("Invalid connection_qualified_name")
            try:
                if fields[0].replace(" ", "") == "" or fields[2].replace(" ", "") == "":
                    raise ValueError("Invalid connection_qualified_name")
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
                if connector_type != AtlanConnectorType.S3:
                    raise ValueError("Connector type must be s3")
            except ValueError as e:
                raise ValueError("Invalid connection_qualified_name") from e
            return S3Object.Attributes(
                aws_arn=aws_arn,
                name=name,
                connection_qualified_name=connection_qualified_name,
                qualified_name=f"{connection_qualified_name}/{aws_arn}",
                connector_name=connector_type.value,
                s3_bucket_qualified_name=s3_bucket_qualified_name,
            )

    attributes: "S3Object.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )

    @classmethod
    # @validate_arguments()
    def create(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        aws_arn: str,
        s3_bucket_qualified_name: Optional[str] = None,
    ) -> S3Object:
        validate_required_fields(
            ["name", "connection_qualified_name", "aws_arn"],
            [name, connection_qualified_name, aws_arn],
        )
        attributes = S3Object.Attributes.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
            aws_arn=aws_arn,
            s3_bucket_qualified_name=s3_bucket_qualified_name,
        )
        return cls(attributes=attributes)


class KafkaTopic(Kafka):
    """Description"""

    def __setattr__(self, name, value):
        if name in KafkaTopic._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "kafka_topic_is_internal",
        "kafka_topic_compression_type",
        "kafka_topic_replication_factor",
        "kafka_topic_segment_bytes",
        "kafka_topic_partitions_count",
        "kafka_topic_size_in_bytes",
        "kafka_topic_record_count",
        "kafka_topic_cleanup_policy",
        "terms",
    ]

    @property
    def kafka_topic_is_internal(self) -> Optional[bool]:
        return self.attributes.kafka_topic_is_internal

    @kafka_topic_is_internal.setter
    def kafka_topic_is_internal(self, kafka_topic_is_internal: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_is_internal = kafka_topic_is_internal

    @property
    def kafka_topic_compression_type(self) -> Optional[KafkaTopicCompressionType]:
        return self.attributes.kafka_topic_compression_type

    @kafka_topic_compression_type.setter
    def kafka_topic_compression_type(
        self, kafka_topic_compression_type: Optional[KafkaTopicCompressionType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_compression_type = kafka_topic_compression_type

    @property
    def kafka_topic_replication_factor(self) -> Optional[int]:
        return self.attributes.kafka_topic_replication_factor

    @kafka_topic_replication_factor.setter
    def kafka_topic_replication_factor(
        self, kafka_topic_replication_factor: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_replication_factor = kafka_topic_replication_factor

    @property
    def kafka_topic_segment_bytes(self) -> Optional[int]:
        return self.attributes.kafka_topic_segment_bytes

    @kafka_topic_segment_bytes.setter
    def kafka_topic_segment_bytes(self, kafka_topic_segment_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_segment_bytes = kafka_topic_segment_bytes

    @property
    def kafka_topic_partitions_count(self) -> Optional[int]:
        return self.attributes.kafka_topic_partitions_count

    @kafka_topic_partitions_count.setter
    def kafka_topic_partitions_count(self, kafka_topic_partitions_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_partitions_count = kafka_topic_partitions_count

    @property
    def kafka_topic_size_in_bytes(self) -> Optional[int]:
        return self.attributes.kafka_topic_size_in_bytes

    @kafka_topic_size_in_bytes.setter
    def kafka_topic_size_in_bytes(self, kafka_topic_size_in_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_size_in_bytes = kafka_topic_size_in_bytes

    @property
    def kafka_topic_record_count(self) -> Optional[int]:
        return self.attributes.kafka_topic_record_count

    @kafka_topic_record_count.setter
    def kafka_topic_record_count(self, kafka_topic_record_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_record_count = kafka_topic_record_count

    @property
    def kafka_topic_cleanup_policy(self) -> Optional[PowerbiEndorsement]:
        return self.attributes.kafka_topic_cleanup_policy

    @kafka_topic_cleanup_policy.setter
    def kafka_topic_cleanup_policy(
        self, kafka_topic_cleanup_policy: Optional[PowerbiEndorsement]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_cleanup_policy = kafka_topic_cleanup_policy

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("KafkaTopic", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "KafkaTopic":
            raise ValueError("must be KafkaTopic")
        return v

    class Attributes(Kafka.Attributes):
        kafka_topic_is_internal: Optional[bool] = Field(
            None, description="", alias="kafkaTopicIsInternal"
        )
        kafka_topic_compression_type: Optional[KafkaTopicCompressionType] = Field(
            None, description="", alias="kafkaTopicCompressionType"
        )
        kafka_topic_replication_factor: Optional[int] = Field(
            None, description="", alias="kafkaTopicReplicationFactor"
        )
        kafka_topic_segment_bytes: Optional[int] = Field(
            None, description="", alias="kafkaTopicSegmentBytes"
        )
        kafka_topic_partitions_count: Optional[int] = Field(
            None, description="", alias="kafkaTopicPartitionsCount"
        )
        kafka_topic_size_in_bytes: Optional[int] = Field(
            None, description="", alias="kafkaTopicSizeInBytes"
        )
        kafka_topic_record_count: Optional[int] = Field(
            None, description="", alias="kafkaTopicRecordCount"
        )
        kafka_topic_cleanup_policy: Optional[PowerbiEndorsement] = Field(
            None, description="", alias="kafkaTopicCleanupPolicy"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        kafka_consumer_groups: Optional[list[KafkaConsumerGroup]] = Field(
            None, description="", alias="kafkaConsumerGroups"
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

    attributes: "KafkaTopic.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class KafkaConsumerGroup(Kafka):
    """Description"""

    def __setattr__(self, name, value):
        if name in KafkaConsumerGroup._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "kafka_consumer_group_topic_consumption_properties",
        "kafka_consumer_group_member_count",
        "kafka_topic_names",
        "kafka_topic_qualified_names",
        "terms",
    ]

    @property
    def kafka_consumer_group_topic_consumption_properties(
        self,
    ) -> Optional[list[KafkaTopicConsumption]]:
        return self.attributes.kafka_consumer_group_topic_consumption_properties

    @kafka_consumer_group_topic_consumption_properties.setter
    def kafka_consumer_group_topic_consumption_properties(
        self,
        kafka_consumer_group_topic_consumption_properties: Optional[
            list[KafkaTopicConsumption]
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_consumer_group_topic_consumption_properties = (
            kafka_consumer_group_topic_consumption_properties
        )

    @property
    def kafka_consumer_group_member_count(self) -> Optional[int]:
        return self.attributes.kafka_consumer_group_member_count

    @kafka_consumer_group_member_count.setter
    def kafka_consumer_group_member_count(
        self, kafka_consumer_group_member_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_consumer_group_member_count = (
            kafka_consumer_group_member_count
        )

    @property
    def kafka_topic_names(self) -> Optional[set[str]]:
        return self.attributes.kafka_topic_names

    @kafka_topic_names.setter
    def kafka_topic_names(self, kafka_topic_names: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_names = kafka_topic_names

    @property
    def kafka_topic_qualified_names(self) -> Optional[set[str]]:
        return self.attributes.kafka_topic_qualified_names

    @kafka_topic_qualified_names.setter
    def kafka_topic_qualified_names(
        self, kafka_topic_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_qualified_names = kafka_topic_qualified_names

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("KafkaConsumerGroup", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "KafkaConsumerGroup":
            raise ValueError("must be KafkaConsumerGroup")
        return v

    class Attributes(Kafka.Attributes):
        kafka_consumer_group_topic_consumption_properties: Optional[
            list[KafkaTopicConsumption]
        ] = Field(
            None, description="", alias="kafkaConsumerGroupTopicConsumptionProperties"
        )
        kafka_consumer_group_member_count: Optional[int] = Field(
            None, description="", alias="kafkaConsumerGroupMemberCount"
        )
        kafka_topic_names: Optional[set[str]] = Field(
            None, description="", alias="kafkaTopicNames"
        )
        kafka_topic_qualified_names: Optional[set[str]] = Field(
            None, description="", alias="kafkaTopicQualifiedNames"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        kafka_topics: Optional[list[KafkaTopic]] = Field(
            None, description="", alias="kafkaTopics"
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

    attributes: "KafkaConsumerGroup.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MetabaseQuestion(Metabase):
    """Description"""

    def __setattr__(self, name, value):
        if name in MetabaseQuestion._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "metabase_dashboard_count",
        "metabase_query_type",
        "metabase_query",
        "terms",
    ]

    @property
    def metabase_dashboard_count(self) -> Optional[int]:
        return self.attributes.metabase_dashboard_count

    @metabase_dashboard_count.setter
    def metabase_dashboard_count(self, metabase_dashboard_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_dashboard_count = metabase_dashboard_count

    @property
    def metabase_query_type(self) -> Optional[str]:
        return self.attributes.metabase_query_type

    @metabase_query_type.setter
    def metabase_query_type(self, metabase_query_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_query_type = metabase_query_type

    @property
    def metabase_query(self) -> Optional[str]:
        return self.attributes.metabase_query

    @metabase_query.setter
    def metabase_query(self, metabase_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_query = metabase_query

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("MetabaseQuestion", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MetabaseQuestion":
            raise ValueError("must be MetabaseQuestion")
        return v

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

    def __setattr__(self, name, value):
        if name in MetabaseCollection._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "metabase_slug",
        "metabase_color",
        "metabase_namespace",
        "metabase_is_personal_collection",
        "terms",
    ]

    @property
    def metabase_slug(self) -> Optional[str]:
        return self.attributes.metabase_slug

    @metabase_slug.setter
    def metabase_slug(self, metabase_slug: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_slug = metabase_slug

    @property
    def metabase_color(self) -> Optional[str]:
        return self.attributes.metabase_color

    @metabase_color.setter
    def metabase_color(self, metabase_color: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_color = metabase_color

    @property
    def metabase_namespace(self) -> Optional[str]:
        return self.attributes.metabase_namespace

    @metabase_namespace.setter
    def metabase_namespace(self, metabase_namespace: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_namespace = metabase_namespace

    @property
    def metabase_is_personal_collection(self) -> Optional[bool]:
        return self.attributes.metabase_is_personal_collection

    @metabase_is_personal_collection.setter
    def metabase_is_personal_collection(
        self, metabase_is_personal_collection: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_is_personal_collection = (
            metabase_is_personal_collection
        )

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("MetabaseCollection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MetabaseCollection":
            raise ValueError("must be MetabaseCollection")
        return v

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

    def __setattr__(self, name, value):
        if name in MetabaseDashboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "metabase_question_count",
        "terms",
    ]

    @property
    def metabase_question_count(self) -> Optional[int]:
        return self.attributes.metabase_question_count

    @metabase_question_count.setter
    def metabase_question_count(self, metabase_question_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_question_count = metabase_question_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("MetabaseDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MetabaseDashboard":
            raise ValueError("must be MetabaseDashboard")
        return v

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


class QuickSightFolder(QuickSight):
    """Description"""

    def __setattr__(self, name, value):
        if name in QuickSightFolder._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_folder_type",
        "quick_sight_folder_hierarchy",
        "terms",
    ]

    @property
    def quick_sight_folder_type(self) -> Optional[QuickSightFolderType]:
        return self.attributes.quick_sight_folder_type

    @quick_sight_folder_type.setter
    def quick_sight_folder_type(
        self, quick_sight_folder_type: Optional[QuickSightFolderType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_folder_type = quick_sight_folder_type

    @property
    def quick_sight_folder_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.quick_sight_folder_hierarchy

    @quick_sight_folder_hierarchy.setter
    def quick_sight_folder_hierarchy(
        self, quick_sight_folder_hierarchy: Optional[list[dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_folder_hierarchy = quick_sight_folder_hierarchy

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QuickSightFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightFolder":
            raise ValueError("must be QuickSightFolder")
        return v

    class Attributes(QuickSight.Attributes):
        quick_sight_folder_type: Optional[QuickSightFolderType] = Field(
            None, description="", alias="quickSightFolderType"
        )
        quick_sight_folder_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="quickSightFolderHierarchy"
        )
        quick_sight_dashboards: Optional[list[QuickSightDashboard]] = Field(
            None, description="", alias="quickSightDashboards"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        quick_sight_analyses: Optional[list[QuickSightAnalysis]] = Field(
            None, description="", alias="quickSightAnalyses"
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
        quick_sight_datasets: Optional[list[QuickSightDataset]] = Field(
            None, description="", alias="quickSightDatasets"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "QuickSightFolder.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightDashboardVisual(QuickSight):
    """Description"""

    def __setattr__(self, name, value):
        if name in QuickSightDashboardVisual._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_dashboard_qualified_name",
        "terms",
    ]

    @property
    def quick_sight_dashboard_qualified_name(self) -> Optional[str]:
        return self.attributes.quick_sight_dashboard_qualified_name

    @quick_sight_dashboard_qualified_name.setter
    def quick_sight_dashboard_qualified_name(
        self, quick_sight_dashboard_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_qualified_name = (
            quick_sight_dashboard_qualified_name
        )

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QuickSightDashboardVisual", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDashboardVisual":
            raise ValueError("must be QuickSightDashboardVisual")
        return v

    class Attributes(QuickSight.Attributes):
        quick_sight_dashboard_qualified_name: Optional[str] = Field(
            None, description="", alias="quickSightDashboardQualifiedName"
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
        quick_sight_dashboard: Optional[QuickSightDashboard] = Field(
            None, description="", alias="quickSightDashboard"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "QuickSightDashboardVisual.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightAnalysisVisual(QuickSight):
    """Description"""

    def __setattr__(self, name, value):
        if name in QuickSightAnalysisVisual._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_analysis_qualified_name",
        "terms",
    ]

    @property
    def quick_sight_analysis_qualified_name(self) -> Optional[str]:
        return self.attributes.quick_sight_analysis_qualified_name

    @quick_sight_analysis_qualified_name.setter
    def quick_sight_analysis_qualified_name(
        self, quick_sight_analysis_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_qualified_name = (
            quick_sight_analysis_qualified_name
        )

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QuickSightAnalysisVisual", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightAnalysisVisual":
            raise ValueError("must be QuickSightAnalysisVisual")
        return v

    class Attributes(QuickSight.Attributes):
        quick_sight_analysis_qualified_name: Optional[str] = Field(
            None, description="", alias="quickSightAnalysisQualifiedName"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        quick_sight_analysis: Optional[QuickSightAnalysis] = Field(
            None, description="", alias="quickSightAnalysis"
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

    attributes: "QuickSightAnalysisVisual.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightDatasetField(QuickSight):
    """Description"""

    def __setattr__(self, name, value):
        if name in QuickSightDatasetField._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_dataset_field_type",
        "quick_sight_dataset_qualified_name",
        "terms",
    ]

    @property
    def quick_sight_dataset_field_type(self) -> Optional[QuickSightDatasetFieldType]:
        return self.attributes.quick_sight_dataset_field_type

    @quick_sight_dataset_field_type.setter
    def quick_sight_dataset_field_type(
        self, quick_sight_dataset_field_type: Optional[QuickSightDatasetFieldType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_field_type = quick_sight_dataset_field_type

    @property
    def quick_sight_dataset_qualified_name(self) -> Optional[str]:
        return self.attributes.quick_sight_dataset_qualified_name

    @quick_sight_dataset_qualified_name.setter
    def quick_sight_dataset_qualified_name(
        self, quick_sight_dataset_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_qualified_name = (
            quick_sight_dataset_qualified_name
        )

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QuickSightDatasetField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDatasetField":
            raise ValueError("must be QuickSightDatasetField")
        return v

    class Attributes(QuickSight.Attributes):
        quick_sight_dataset_field_type: Optional[QuickSightDatasetFieldType] = Field(
            None, description="", alias="quickSightDatasetFieldType"
        )
        quick_sight_dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="quickSightDatasetQualifiedName"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        quick_sight_dataset: Optional[QuickSightDataset] = Field(
            None, description="", alias="quickSightDataset"
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

    attributes: "QuickSightDatasetField.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightAnalysis(QuickSight):
    """Description"""

    def __setattr__(self, name, value):
        if name in QuickSightAnalysis._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_analysis_status",
        "quick_sight_analysis_calculated_fields",
        "quick_sight_analysis_parameter_declarations",
        "quick_sight_analysis_filter_groups",
        "terms",
    ]

    @property
    def quick_sight_analysis_status(self) -> Optional[QuickSightAnalysisStatus]:
        return self.attributes.quick_sight_analysis_status

    @quick_sight_analysis_status.setter
    def quick_sight_analysis_status(
        self, quick_sight_analysis_status: Optional[QuickSightAnalysisStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_status = quick_sight_analysis_status

    @property
    def quick_sight_analysis_calculated_fields(self) -> Optional[set[str]]:
        return self.attributes.quick_sight_analysis_calculated_fields

    @quick_sight_analysis_calculated_fields.setter
    def quick_sight_analysis_calculated_fields(
        self, quick_sight_analysis_calculated_fields: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_calculated_fields = (
            quick_sight_analysis_calculated_fields
        )

    @property
    def quick_sight_analysis_parameter_declarations(self) -> Optional[set[str]]:
        return self.attributes.quick_sight_analysis_parameter_declarations

    @quick_sight_analysis_parameter_declarations.setter
    def quick_sight_analysis_parameter_declarations(
        self, quick_sight_analysis_parameter_declarations: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_parameter_declarations = (
            quick_sight_analysis_parameter_declarations
        )

    @property
    def quick_sight_analysis_filter_groups(self) -> Optional[set[str]]:
        return self.attributes.quick_sight_analysis_filter_groups

    @quick_sight_analysis_filter_groups.setter
    def quick_sight_analysis_filter_groups(
        self, quick_sight_analysis_filter_groups: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_filter_groups = (
            quick_sight_analysis_filter_groups
        )

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QuickSightAnalysis", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightAnalysis":
            raise ValueError("must be QuickSightAnalysis")
        return v

    class Attributes(QuickSight.Attributes):
        quick_sight_analysis_status: Optional[QuickSightAnalysisStatus] = Field(
            None, description="", alias="quickSightAnalysisStatus"
        )
        quick_sight_analysis_calculated_fields: Optional[set[str]] = Field(
            None, description="", alias="quickSightAnalysisCalculatedFields"
        )
        quick_sight_analysis_parameter_declarations: Optional[set[str]] = Field(
            None, description="", alias="quickSightAnalysisParameterDeclarations"
        )
        quick_sight_analysis_filter_groups: Optional[set[str]] = Field(
            None, description="", alias="quickSightAnalysisFilterGroups"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        quick_sight_analysis_visuals: Optional[list[QuickSightAnalysisVisual]] = Field(
            None, description="", alias="quickSightAnalysisVisuals"
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
        quick_sight_analysis_folders: Optional[list[QuickSightFolder]] = Field(
            None, description="", alias="quickSightAnalysisFolders"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "QuickSightAnalysis.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightDashboard(QuickSight):
    """Description"""

    def __setattr__(self, name, value):
        if name in QuickSightDashboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_dashboard_published_version_number",
        "quick_sight_dashboard_last_published_time",
        "terms",
    ]

    @property
    def quick_sight_dashboard_published_version_number(self) -> Optional[int]:
        return self.attributes.quick_sight_dashboard_published_version_number

    @quick_sight_dashboard_published_version_number.setter
    def quick_sight_dashboard_published_version_number(
        self, quick_sight_dashboard_published_version_number: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_published_version_number = (
            quick_sight_dashboard_published_version_number
        )

    @property
    def quick_sight_dashboard_last_published_time(self) -> Optional[datetime]:
        return self.attributes.quick_sight_dashboard_last_published_time

    @quick_sight_dashboard_last_published_time.setter
    def quick_sight_dashboard_last_published_time(
        self, quick_sight_dashboard_last_published_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_last_published_time = (
            quick_sight_dashboard_last_published_time
        )

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QuickSightDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDashboard":
            raise ValueError("must be QuickSightDashboard")
        return v

    class Attributes(QuickSight.Attributes):
        quick_sight_dashboard_published_version_number: Optional[int] = Field(
            None, description="", alias="quickSightDashboardPublishedVersionNumber"
        )
        quick_sight_dashboard_last_published_time: Optional[datetime] = Field(
            None, description="", alias="quickSightDashboardLastPublishedTime"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        quick_sight_dashboard_folders: Optional[list[QuickSightFolder]] = Field(
            None, description="", alias="quickSightDashboardFolders"
        )  # relationship
        quick_sight_dashboard_visuals: Optional[
            list[QuickSightDashboardVisual]
        ] = Field(
            None, description="", alias="quickSightDashboardVisuals"
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

    attributes: "QuickSightDashboard.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightDataset(QuickSight):
    """Description"""

    def __setattr__(self, name, value):
        if name in QuickSightDataset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_dataset_import_mode",
        "quick_sight_dataset_column_count",
        "terms",
    ]

    @property
    def quick_sight_dataset_import_mode(self) -> Optional[QuickSightDatasetImportMode]:
        return self.attributes.quick_sight_dataset_import_mode

    @quick_sight_dataset_import_mode.setter
    def quick_sight_dataset_import_mode(
        self, quick_sight_dataset_import_mode: Optional[QuickSightDatasetImportMode]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_import_mode = (
            quick_sight_dataset_import_mode
        )

    @property
    def quick_sight_dataset_column_count(self) -> Optional[int]:
        return self.attributes.quick_sight_dataset_column_count

    @quick_sight_dataset_column_count.setter
    def quick_sight_dataset_column_count(
        self, quick_sight_dataset_column_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_column_count = (
            quick_sight_dataset_column_count
        )

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QuickSightDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDataset":
            raise ValueError("must be QuickSightDataset")
        return v

    class Attributes(QuickSight.Attributes):
        quick_sight_dataset_import_mode: Optional[QuickSightDatasetImportMode] = Field(
            None, description="", alias="quickSightDatasetImportMode"
        )
        quick_sight_dataset_column_count: Optional[int] = Field(
            None, description="", alias="quickSightDatasetColumnCount"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        quick_sight_dataset_folders: Optional[list[QuickSightFolder]] = Field(
            None, description="", alias="quickSightDatasetFolders"
        )  # relationship
        quick_sight_dataset_fields: Optional[list[QuickSightDatasetField]] = Field(
            None, description="", alias="quickSightDatasetFields"
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

    attributes: "QuickSightDataset.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ThoughtspotLiveboard(Thoughtspot):
    """Description"""

    def __setattr__(self, name, value):
        if name in ThoughtspotLiveboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ThoughtspotLiveboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotLiveboard":
            raise ValueError("must be ThoughtspotLiveboard")
        return v

    class Attributes(Thoughtspot.Attributes):
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        thoughtspot_dashlets: Optional[list[ThoughtspotDashlet]] = Field(
            None, description="", alias="thoughtspotDashlets"
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

    attributes: "ThoughtspotLiveboard.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ThoughtspotDashlet(Thoughtspot):
    """Description"""

    def __setattr__(self, name, value):
        if name in ThoughtspotDashlet._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "thoughtspot_liveboard_name",
        "thoughtspot_liveboard_qualified_name",
        "terms",
    ]

    @property
    def thoughtspot_liveboard_name(self) -> Optional[str]:
        return self.attributes.thoughtspot_liveboard_name

    @thoughtspot_liveboard_name.setter
    def thoughtspot_liveboard_name(self, thoughtspot_liveboard_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_liveboard_name = thoughtspot_liveboard_name

    @property
    def thoughtspot_liveboard_qualified_name(self) -> Optional[str]:
        return self.attributes.thoughtspot_liveboard_qualified_name

    @thoughtspot_liveboard_qualified_name.setter
    def thoughtspot_liveboard_qualified_name(
        self, thoughtspot_liveboard_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_liveboard_qualified_name = (
            thoughtspot_liveboard_qualified_name
        )

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ThoughtspotDashlet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotDashlet":
            raise ValueError("must be ThoughtspotDashlet")
        return v

    class Attributes(Thoughtspot.Attributes):
        thoughtspot_liveboard_name: Optional[str] = Field(
            None, description="", alias="thoughtspotLiveboardName"
        )
        thoughtspot_liveboard_qualified_name: Optional[str] = Field(
            None, description="", alias="thoughtspotLiveboardQualifiedName"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        thoughtspot_liveboard: Optional[ThoughtspotLiveboard] = Field(
            None, description="", alias="thoughtspotLiveboard"
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

    attributes: "ThoughtspotDashlet.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ThoughtspotAnswer(Thoughtspot):
    """Description"""

    def __setattr__(self, name, value):
        if name in ThoughtspotAnswer._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ThoughtspotAnswer", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotAnswer":
            raise ValueError("must be ThoughtspotAnswer")
        return v

    class Attributes(Thoughtspot.Attributes):
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

    attributes: "ThoughtspotAnswer.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIReport(PowerBI):
    """Description"""

    def __setattr__(self, name, value):
        if name in PowerBIReport._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "dataset_qualified_name",
        "web_url",
        "page_count",
        "terms",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return self.attributes.workspace_qualified_name

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def dataset_qualified_name(self) -> Optional[str]:
        return self.attributes.dataset_qualified_name

    @dataset_qualified_name.setter
    def dataset_qualified_name(self, dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_qualified_name = dataset_qualified_name

    @property
    def web_url(self) -> Optional[str]:
        return self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def page_count(self) -> Optional[int]:
        return self.attributes.page_count

    @page_count.setter
    def page_count(self, page_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.page_count = page_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PowerBIReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIReport":
            raise ValueError("must be PowerBIReport")
        return v

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

    def __setattr__(self, name, value):
        if name in PowerBIMeasure._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "dataset_qualified_name",
        "power_b_i_measure_expression",
        "power_b_i_is_external_measure",
        "terms",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return self.attributes.workspace_qualified_name

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def dataset_qualified_name(self) -> Optional[str]:
        return self.attributes.dataset_qualified_name

    @dataset_qualified_name.setter
    def dataset_qualified_name(self, dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_qualified_name = dataset_qualified_name

    @property
    def power_b_i_measure_expression(self) -> Optional[str]:
        return self.attributes.power_b_i_measure_expression

    @power_b_i_measure_expression.setter
    def power_b_i_measure_expression(self, power_b_i_measure_expression: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_measure_expression = power_b_i_measure_expression

    @property
    def power_b_i_is_external_measure(self) -> Optional[bool]:
        return self.attributes.power_b_i_is_external_measure

    @power_b_i_is_external_measure.setter
    def power_b_i_is_external_measure(
        self, power_b_i_is_external_measure: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_is_external_measure = power_b_i_is_external_measure

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PowerBIMeasure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIMeasure":
            raise ValueError("must be PowerBIMeasure")
        return v

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

    def __setattr__(self, name, value):
        if name in PowerBIColumn._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "dataset_qualified_name",
        "power_b_i_column_data_category",
        "power_b_i_column_data_type",
        "power_b_i_sort_by_column",
        "power_b_i_column_summarize_by",
        "terms",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return self.attributes.workspace_qualified_name

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def dataset_qualified_name(self) -> Optional[str]:
        return self.attributes.dataset_qualified_name

    @dataset_qualified_name.setter
    def dataset_qualified_name(self, dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_qualified_name = dataset_qualified_name

    @property
    def power_b_i_column_data_category(self) -> Optional[str]:
        return self.attributes.power_b_i_column_data_category

    @power_b_i_column_data_category.setter
    def power_b_i_column_data_category(
        self, power_b_i_column_data_category: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_column_data_category = power_b_i_column_data_category

    @property
    def power_b_i_column_data_type(self) -> Optional[str]:
        return self.attributes.power_b_i_column_data_type

    @power_b_i_column_data_type.setter
    def power_b_i_column_data_type(self, power_b_i_column_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_column_data_type = power_b_i_column_data_type

    @property
    def power_b_i_sort_by_column(self) -> Optional[str]:
        return self.attributes.power_b_i_sort_by_column

    @power_b_i_sort_by_column.setter
    def power_b_i_sort_by_column(self, power_b_i_sort_by_column: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_sort_by_column = power_b_i_sort_by_column

    @property
    def power_b_i_column_summarize_by(self) -> Optional[str]:
        return self.attributes.power_b_i_column_summarize_by

    @power_b_i_column_summarize_by.setter
    def power_b_i_column_summarize_by(
        self, power_b_i_column_summarize_by: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_column_summarize_by = power_b_i_column_summarize_by

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PowerBIColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIColumn":
            raise ValueError("must be PowerBIColumn")
        return v

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


class PowerBITable(PowerBI):
    """Description"""

    def __setattr__(self, name, value):
        if name in PowerBITable._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "dataset_qualified_name",
        "power_b_i_table_source_expressions",
        "power_b_i_table_column_count",
        "power_b_i_table_measure_count",
        "terms",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return self.attributes.workspace_qualified_name

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def dataset_qualified_name(self) -> Optional[str]:
        return self.attributes.dataset_qualified_name

    @dataset_qualified_name.setter
    def dataset_qualified_name(self, dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_qualified_name = dataset_qualified_name

    @property
    def power_b_i_table_source_expressions(self) -> Optional[set[str]]:
        return self.attributes.power_b_i_table_source_expressions

    @power_b_i_table_source_expressions.setter
    def power_b_i_table_source_expressions(
        self, power_b_i_table_source_expressions: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_table_source_expressions = (
            power_b_i_table_source_expressions
        )

    @property
    def power_b_i_table_column_count(self) -> Optional[int]:
        return self.attributes.power_b_i_table_column_count

    @power_b_i_table_column_count.setter
    def power_b_i_table_column_count(self, power_b_i_table_column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_table_column_count = power_b_i_table_column_count

    @property
    def power_b_i_table_measure_count(self) -> Optional[int]:
        return self.attributes.power_b_i_table_measure_count

    @power_b_i_table_measure_count.setter
    def power_b_i_table_measure_count(
        self, power_b_i_table_measure_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_table_measure_count = power_b_i_table_measure_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PowerBITable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBITable":
            raise ValueError("must be PowerBITable")
        return v

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="datasetQualifiedName"
        )
        power_b_i_table_source_expressions: Optional[set[str]] = Field(
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


class PowerBITile(PowerBI):
    """Description"""

    def __setattr__(self, name, value):
        if name in PowerBITile._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "dashboard_qualified_name",
        "terms",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return self.attributes.workspace_qualified_name

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def dashboard_qualified_name(self) -> Optional[str]:
        return self.attributes.dashboard_qualified_name

    @dashboard_qualified_name.setter
    def dashboard_qualified_name(self, dashboard_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard_qualified_name = dashboard_qualified_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PowerBITile", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBITile":
            raise ValueError("must be PowerBITile")
        return v

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


class PowerBIDatasource(PowerBI):
    """Description"""

    def __setattr__(self, name, value):
        if name in PowerBIDatasource._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "connection_details",
        "terms",
    ]

    @property
    def connection_details(self) -> Optional[dict[str, str]]:
        return self.attributes.connection_details

    @connection_details.setter
    def connection_details(self, connection_details: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connection_details = connection_details

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PowerBIDatasource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDatasource":
            raise ValueError("must be PowerBIDatasource")
        return v

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

    def __setattr__(self, name, value):
        if name in PowerBIWorkspace._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "web_url",
        "report_count",
        "dashboard_count",
        "dataset_count",
        "dataflow_count",
        "terms",
    ]

    @property
    def web_url(self) -> Optional[str]:
        return self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def report_count(self) -> Optional[int]:
        return self.attributes.report_count

    @report_count.setter
    def report_count(self, report_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_count = report_count

    @property
    def dashboard_count(self) -> Optional[int]:
        return self.attributes.dashboard_count

    @dashboard_count.setter
    def dashboard_count(self, dashboard_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard_count = dashboard_count

    @property
    def dataset_count(self) -> Optional[int]:
        return self.attributes.dataset_count

    @dataset_count.setter
    def dataset_count(self, dataset_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_count = dataset_count

    @property
    def dataflow_count(self) -> Optional[int]:
        return self.attributes.dataflow_count

    @dataflow_count.setter
    def dataflow_count(self, dataflow_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataflow_count = dataflow_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PowerBIWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIWorkspace":
            raise ValueError("must be PowerBIWorkspace")
        return v

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

    def __setattr__(self, name, value):
        if name in PowerBIDataset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "web_url",
        "terms",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return self.attributes.workspace_qualified_name

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def web_url(self) -> Optional[str]:
        return self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PowerBIDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDataset":
            raise ValueError("must be PowerBIDataset")
        return v

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        tiles: Optional[list[PowerBITile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        reports: Optional[list[PowerBIReport]] = Field(
            None, description="", alias="reports"
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

    def __setattr__(self, name, value):
        if name in PowerBIDashboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "web_url",
        "tile_count",
        "terms",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return self.attributes.workspace_qualified_name

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def web_url(self) -> Optional[str]:
        return self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def tile_count(self) -> Optional[int]:
        return self.attributes.tile_count

    @tile_count.setter
    def tile_count(self, tile_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tile_count = tile_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PowerBIDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDashboard":
            raise ValueError("must be PowerBIDashboard")
        return v

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


class PowerBIDataflow(PowerBI):
    """Description"""

    def __setattr__(self, name, value):
        if name in PowerBIDataflow._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "web_url",
        "terms",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return self.attributes.workspace_qualified_name

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def web_url(self) -> Optional[str]:
        return self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PowerBIDataflow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDataflow":
            raise ValueError("must be PowerBIDataflow")
        return v

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


class PowerBIPage(PowerBI):
    """Description"""

    def __setattr__(self, name, value):
        if name in PowerBIPage._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "report_qualified_name",
        "terms",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return self.attributes.workspace_qualified_name

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def report_qualified_name(self) -> Optional[str]:
        return self.attributes.report_qualified_name

    @report_qualified_name.setter
    def report_qualified_name(self, report_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_qualified_name = report_qualified_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PowerBIPage", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIPage":
            raise ValueError("must be PowerBIPage")
        return v

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


class PresetChart(Preset):
    """Description"""

    def __setattr__(self, name, value):
        if name in PresetChart._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "preset_chart_description_markdown",
        "preset_chart_form_data",
        "terms",
    ]

    @property
    def preset_chart_description_markdown(self) -> Optional[str]:
        return self.attributes.preset_chart_description_markdown

    @preset_chart_description_markdown.setter
    def preset_chart_description_markdown(
        self, preset_chart_description_markdown: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_chart_description_markdown = (
            preset_chart_description_markdown
        )

    @property
    def preset_chart_form_data(self) -> Optional[dict[str, str]]:
        return self.attributes.preset_chart_form_data

    @preset_chart_form_data.setter
    def preset_chart_form_data(self, preset_chart_form_data: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_chart_form_data = preset_chart_form_data

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PresetChart", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetChart":
            raise ValueError("must be PresetChart")
        return v

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

    def __setattr__(self, name, value):
        if name in PresetDataset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "preset_dataset_datasource_name",
        "preset_dataset_id",
        "preset_dataset_type",
        "terms",
    ]

    @property
    def preset_dataset_datasource_name(self) -> Optional[str]:
        return self.attributes.preset_dataset_datasource_name

    @preset_dataset_datasource_name.setter
    def preset_dataset_datasource_name(
        self, preset_dataset_datasource_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dataset_datasource_name = preset_dataset_datasource_name

    @property
    def preset_dataset_id(self) -> Optional[int]:
        return self.attributes.preset_dataset_id

    @preset_dataset_id.setter
    def preset_dataset_id(self, preset_dataset_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dataset_id = preset_dataset_id

    @property
    def preset_dataset_type(self) -> Optional[str]:
        return self.attributes.preset_dataset_type

    @preset_dataset_type.setter
    def preset_dataset_type(self, preset_dataset_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dataset_type = preset_dataset_type

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PresetDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetDataset":
            raise ValueError("must be PresetDataset")
        return v

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

    def __setattr__(self, name, value):
        if name in PresetDashboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "preset_dashboard_changed_by_name",
        "preset_dashboard_changed_by_url",
        "preset_dashboard_is_managed_externally",
        "preset_dashboard_is_published",
        "preset_dashboard_thumbnail_url",
        "preset_dashboard_chart_count",
        "terms",
    ]

    @property
    def preset_dashboard_changed_by_name(self) -> Optional[str]:
        return self.attributes.preset_dashboard_changed_by_name

    @preset_dashboard_changed_by_name.setter
    def preset_dashboard_changed_by_name(
        self, preset_dashboard_changed_by_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_changed_by_name = (
            preset_dashboard_changed_by_name
        )

    @property
    def preset_dashboard_changed_by_url(self) -> Optional[str]:
        return self.attributes.preset_dashboard_changed_by_url

    @preset_dashboard_changed_by_url.setter
    def preset_dashboard_changed_by_url(
        self, preset_dashboard_changed_by_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_changed_by_url = (
            preset_dashboard_changed_by_url
        )

    @property
    def preset_dashboard_is_managed_externally(self) -> Optional[bool]:
        return self.attributes.preset_dashboard_is_managed_externally

    @preset_dashboard_is_managed_externally.setter
    def preset_dashboard_is_managed_externally(
        self, preset_dashboard_is_managed_externally: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_is_managed_externally = (
            preset_dashboard_is_managed_externally
        )

    @property
    def preset_dashboard_is_published(self) -> Optional[bool]:
        return self.attributes.preset_dashboard_is_published

    @preset_dashboard_is_published.setter
    def preset_dashboard_is_published(
        self, preset_dashboard_is_published: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_is_published = preset_dashboard_is_published

    @property
    def preset_dashboard_thumbnail_url(self) -> Optional[str]:
        return self.attributes.preset_dashboard_thumbnail_url

    @preset_dashboard_thumbnail_url.setter
    def preset_dashboard_thumbnail_url(
        self, preset_dashboard_thumbnail_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_thumbnail_url = preset_dashboard_thumbnail_url

    @property
    def preset_dashboard_chart_count(self) -> Optional[int]:
        return self.attributes.preset_dashboard_chart_count

    @preset_dashboard_chart_count.setter
    def preset_dashboard_chart_count(self, preset_dashboard_chart_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_chart_count = preset_dashboard_chart_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PresetDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetDashboard":
            raise ValueError("must be PresetDashboard")
        return v

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

    def __setattr__(self, name, value):
        if name in PresetWorkspace._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "preset_workspace_public_dashboards_allowed",
        "preset_workspace_cluster_id",
        "preset_workspace_hostname",
        "preset_workspace_is_in_maintenance_mode",
        "preset_workspace_region",
        "preset_workspace_status",
        "preset_workspace_deployment_id",
        "preset_workspace_dashboard_count",
        "preset_workspace_dataset_count",
        "terms",
    ]

    @property
    def preset_workspace_public_dashboards_allowed(self) -> Optional[bool]:
        return self.attributes.preset_workspace_public_dashboards_allowed

    @preset_workspace_public_dashboards_allowed.setter
    def preset_workspace_public_dashboards_allowed(
        self, preset_workspace_public_dashboards_allowed: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_public_dashboards_allowed = (
            preset_workspace_public_dashboards_allowed
        )

    @property
    def preset_workspace_cluster_id(self) -> Optional[int]:
        return self.attributes.preset_workspace_cluster_id

    @preset_workspace_cluster_id.setter
    def preset_workspace_cluster_id(self, preset_workspace_cluster_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_cluster_id = preset_workspace_cluster_id

    @property
    def preset_workspace_hostname(self) -> Optional[str]:
        return self.attributes.preset_workspace_hostname

    @preset_workspace_hostname.setter
    def preset_workspace_hostname(self, preset_workspace_hostname: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_hostname = preset_workspace_hostname

    @property
    def preset_workspace_is_in_maintenance_mode(self) -> Optional[bool]:
        return self.attributes.preset_workspace_is_in_maintenance_mode

    @preset_workspace_is_in_maintenance_mode.setter
    def preset_workspace_is_in_maintenance_mode(
        self, preset_workspace_is_in_maintenance_mode: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_is_in_maintenance_mode = (
            preset_workspace_is_in_maintenance_mode
        )

    @property
    def preset_workspace_region(self) -> Optional[str]:
        return self.attributes.preset_workspace_region

    @preset_workspace_region.setter
    def preset_workspace_region(self, preset_workspace_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_region = preset_workspace_region

    @property
    def preset_workspace_status(self) -> Optional[str]:
        return self.attributes.preset_workspace_status

    @preset_workspace_status.setter
    def preset_workspace_status(self, preset_workspace_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_status = preset_workspace_status

    @property
    def preset_workspace_deployment_id(self) -> Optional[int]:
        return self.attributes.preset_workspace_deployment_id

    @preset_workspace_deployment_id.setter
    def preset_workspace_deployment_id(
        self, preset_workspace_deployment_id: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_deployment_id = preset_workspace_deployment_id

    @property
    def preset_workspace_dashboard_count(self) -> Optional[int]:
        return self.attributes.preset_workspace_dashboard_count

    @preset_workspace_dashboard_count.setter
    def preset_workspace_dashboard_count(
        self, preset_workspace_dashboard_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_dashboard_count = (
            preset_workspace_dashboard_count
        )

    @property
    def preset_workspace_dataset_count(self) -> Optional[int]:
        return self.attributes.preset_workspace_dataset_count

    @preset_workspace_dataset_count.setter
    def preset_workspace_dataset_count(
        self, preset_workspace_dataset_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_dataset_count = preset_workspace_dataset_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("PresetWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetWorkspace":
            raise ValueError("must be PresetWorkspace")
        return v

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

    def __setattr__(self, name, value):
        if name in ModeReport._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "mode_collection_token",
        "mode_report_published_at",
        "mode_query_count",
        "mode_chart_count",
        "mode_query_preview",
        "mode_is_public",
        "mode_is_shared",
        "terms",
    ]

    @property
    def mode_collection_token(self) -> Optional[str]:
        return self.attributes.mode_collection_token

    @mode_collection_token.setter
    def mode_collection_token(self, mode_collection_token: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_token = mode_collection_token

    @property
    def mode_report_published_at(self) -> Optional[datetime]:
        return self.attributes.mode_report_published_at

    @mode_report_published_at.setter
    def mode_report_published_at(self, mode_report_published_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report_published_at = mode_report_published_at

    @property
    def mode_query_count(self) -> Optional[int]:
        return self.attributes.mode_query_count

    @mode_query_count.setter
    def mode_query_count(self, mode_query_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_count = mode_query_count

    @property
    def mode_chart_count(self) -> Optional[int]:
        return self.attributes.mode_chart_count

    @mode_chart_count.setter
    def mode_chart_count(self, mode_chart_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_chart_count = mode_chart_count

    @property
    def mode_query_preview(self) -> Optional[str]:
        return self.attributes.mode_query_preview

    @mode_query_preview.setter
    def mode_query_preview(self, mode_query_preview: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_preview = mode_query_preview

    @property
    def mode_is_public(self) -> Optional[bool]:
        return self.attributes.mode_is_public

    @mode_is_public.setter
    def mode_is_public(self, mode_is_public: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_is_public = mode_is_public

    @property
    def mode_is_shared(self) -> Optional[bool]:
        return self.attributes.mode_is_shared

    @mode_is_shared.setter
    def mode_is_shared(self, mode_is_shared: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_is_shared = mode_is_shared

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ModeReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeReport":
            raise ValueError("must be ModeReport")
        return v

    class Attributes(Mode.Attributes):
        mode_collection_token: Optional[str] = Field(
            None, description="", alias="modeCollectionToken"
        )
        mode_report_published_at: Optional[datetime] = Field(
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

    def __setattr__(self, name, value):
        if name in ModeQuery._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "mode_raw_query",
        "mode_report_import_count",
        "terms",
    ]

    @property
    def mode_raw_query(self) -> Optional[str]:
        return self.attributes.mode_raw_query

    @mode_raw_query.setter
    def mode_raw_query(self, mode_raw_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_raw_query = mode_raw_query

    @property
    def mode_report_import_count(self) -> Optional[int]:
        return self.attributes.mode_report_import_count

    @mode_report_import_count.setter
    def mode_report_import_count(self, mode_report_import_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report_import_count = mode_report_import_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ModeQuery", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeQuery":
            raise ValueError("must be ModeQuery")
        return v

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

    def __setattr__(self, name, value):
        if name in ModeChart._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "mode_chart_type",
        "terms",
    ]

    @property
    def mode_chart_type(self) -> Optional[str]:
        return self.attributes.mode_chart_type

    @mode_chart_type.setter
    def mode_chart_type(self, mode_chart_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_chart_type = mode_chart_type

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ModeChart", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeChart":
            raise ValueError("must be ModeChart")
        return v

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

    def __setattr__(self, name, value):
        if name in ModeWorkspace._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "mode_collection_count",
        "terms",
    ]

    @property
    def mode_collection_count(self) -> Optional[int]:
        return self.attributes.mode_collection_count

    @mode_collection_count.setter
    def mode_collection_count(self, mode_collection_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_count = mode_collection_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ModeWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeWorkspace":
            raise ValueError("must be ModeWorkspace")
        return v

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

    def __setattr__(self, name, value):
        if name in ModeCollection._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "mode_collection_type",
        "mode_collection_state",
        "terms",
    ]

    @property
    def mode_collection_type(self) -> Optional[str]:
        return self.attributes.mode_collection_type

    @mode_collection_type.setter
    def mode_collection_type(self, mode_collection_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_type = mode_collection_type

    @property
    def mode_collection_state(self) -> Optional[str]:
        return self.attributes.mode_collection_state

    @mode_collection_state.setter
    def mode_collection_state(self, mode_collection_state: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_state = mode_collection_state

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("ModeCollection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeCollection":
            raise ValueError("must be ModeCollection")
        return v

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


class SigmaDatasetColumn(Sigma):
    """Description"""

    def __setattr__(self, name, value):
        if name in SigmaDatasetColumn._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "sigma_dataset_qualified_name",
        "sigma_dataset_name",
        "terms",
    ]

    @property
    def sigma_dataset_qualified_name(self) -> Optional[str]:
        return self.attributes.sigma_dataset_qualified_name

    @sigma_dataset_qualified_name.setter
    def sigma_dataset_qualified_name(self, sigma_dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset_qualified_name = sigma_dataset_qualified_name

    @property
    def sigma_dataset_name(self) -> Optional[str]:
        return self.attributes.sigma_dataset_name

    @sigma_dataset_name.setter
    def sigma_dataset_name(self, sigma_dataset_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset_name = sigma_dataset_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SigmaDatasetColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDatasetColumn":
            raise ValueError("must be SigmaDatasetColumn")
        return v

    class Attributes(Sigma.Attributes):
        sigma_dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="sigmaDatasetQualifiedName"
        )
        sigma_dataset_name: Optional[str] = Field(
            None, description="", alias="sigmaDatasetName"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        sigma_dataset: Optional[SigmaDataset] = Field(
            None, description="", alias="sigmaDataset"
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

    attributes: "SigmaDatasetColumn.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaDataset(Sigma):
    """Description"""

    def __setattr__(self, name, value):
        if name in SigmaDataset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "sigma_dataset_column_count",
        "terms",
    ]

    @property
    def sigma_dataset_column_count(self) -> Optional[int]:
        return self.attributes.sigma_dataset_column_count

    @sigma_dataset_column_count.setter
    def sigma_dataset_column_count(self, sigma_dataset_column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset_column_count = sigma_dataset_column_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SigmaDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDataset":
            raise ValueError("must be SigmaDataset")
        return v

    class Attributes(Sigma.Attributes):
        sigma_dataset_column_count: Optional[int] = Field(
            None, description="", alias="sigmaDatasetColumnCount"
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
        sigma_dataset_columns: Optional[list[SigmaDatasetColumn]] = Field(
            None, description="", alias="sigmaDatasetColumns"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "SigmaDataset.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaWorkbook(Sigma):
    """Description"""

    def __setattr__(self, name, value):
        if name in SigmaWorkbook._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "sigma_page_count",
        "terms",
    ]

    @property
    def sigma_page_count(self) -> Optional[int]:
        return self.attributes.sigma_page_count

    @sigma_page_count.setter
    def sigma_page_count(self, sigma_page_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_page_count = sigma_page_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SigmaWorkbook", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaWorkbook":
            raise ValueError("must be SigmaWorkbook")
        return v

    class Attributes(Sigma.Attributes):
        sigma_page_count: Optional[int] = Field(
            None, description="", alias="sigmaPageCount"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        sigma_pages: Optional[list[SigmaPage]] = Field(
            None, description="", alias="sigmaPages"
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

    attributes: "SigmaWorkbook.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaDataElementField(Sigma):
    """Description"""

    def __setattr__(self, name, value):
        if name in SigmaDataElementField._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "sigma_data_element_field_is_hidden",
        "sigma_data_element_field_formula",
        "terms",
    ]

    @property
    def sigma_data_element_field_is_hidden(self) -> Optional[bool]:
        return self.attributes.sigma_data_element_field_is_hidden

    @sigma_data_element_field_is_hidden.setter
    def sigma_data_element_field_is_hidden(
        self, sigma_data_element_field_is_hidden: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_field_is_hidden = (
            sigma_data_element_field_is_hidden
        )

    @property
    def sigma_data_element_field_formula(self) -> Optional[str]:
        return self.attributes.sigma_data_element_field_formula

    @sigma_data_element_field_formula.setter
    def sigma_data_element_field_formula(
        self, sigma_data_element_field_formula: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_field_formula = (
            sigma_data_element_field_formula
        )

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SigmaDataElementField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDataElementField":
            raise ValueError("must be SigmaDataElementField")
        return v

    class Attributes(Sigma.Attributes):
        sigma_data_element_field_is_hidden: Optional[bool] = Field(
            None, description="", alias="sigmaDataElementFieldIsHidden"
        )
        sigma_data_element_field_formula: Optional[str] = Field(
            None, description="", alias="sigmaDataElementFieldFormula"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        sigma_data_element: Optional[SigmaDataElement] = Field(
            None, description="", alias="sigmaDataElement"
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

    attributes: "SigmaDataElementField.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaPage(Sigma):
    """Description"""

    def __setattr__(self, name, value):
        if name in SigmaPage._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "sigma_data_element_count",
        "terms",
    ]

    @property
    def sigma_data_element_count(self) -> Optional[int]:
        return self.attributes.sigma_data_element_count

    @sigma_data_element_count.setter
    def sigma_data_element_count(self, sigma_data_element_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_count = sigma_data_element_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SigmaPage", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaPage":
            raise ValueError("must be SigmaPage")
        return v

    class Attributes(Sigma.Attributes):
        sigma_data_element_count: Optional[int] = Field(
            None, description="", alias="sigmaDataElementCount"
        )
        sigma_data_elements: Optional[list[SigmaDataElement]] = Field(
            None, description="", alias="sigmaDataElements"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        sigma_workbook: Optional[SigmaWorkbook] = Field(
            None, description="", alias="sigmaWorkbook"
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

    attributes: "SigmaPage.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaDataElement(Sigma):
    """Description"""

    def __setattr__(self, name, value):
        if name in SigmaDataElement._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "sigma_data_element_query",
        "sigma_data_element_type",
        "sigma_data_element_field_count",
        "terms",
    ]

    @property
    def sigma_data_element_query(self) -> Optional[str]:
        return self.attributes.sigma_data_element_query

    @sigma_data_element_query.setter
    def sigma_data_element_query(self, sigma_data_element_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_query = sigma_data_element_query

    @property
    def sigma_data_element_type(self) -> Optional[str]:
        return self.attributes.sigma_data_element_type

    @sigma_data_element_type.setter
    def sigma_data_element_type(self, sigma_data_element_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_type = sigma_data_element_type

    @property
    def sigma_data_element_field_count(self) -> Optional[int]:
        return self.attributes.sigma_data_element_field_count

    @sigma_data_element_field_count.setter
    def sigma_data_element_field_count(
        self, sigma_data_element_field_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_field_count = sigma_data_element_field_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SigmaDataElement", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDataElement":
            raise ValueError("must be SigmaDataElement")
        return v

    class Attributes(Sigma.Attributes):
        sigma_data_element_query: Optional[str] = Field(
            None, description="", alias="sigmaDataElementQuery"
        )
        sigma_data_element_type: Optional[str] = Field(
            None, description="", alias="sigmaDataElementType"
        )
        sigma_data_element_field_count: Optional[int] = Field(
            None, description="", alias="sigmaDataElementFieldCount"
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
        sigma_page: Optional[SigmaPage] = Field(
            None, description="", alias="sigmaPage"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship
        sigma_data_element_fields: Optional[list[SigmaDataElementField]] = Field(
            None, description="", alias="sigmaDataElementFields"
        )  # relationship

    attributes: "SigmaDataElement.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikSpace(Qlik):
    """Description"""

    def __setattr__(self, name, value):
        if name in QlikSpace._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "qlik_space_type",
        "terms",
    ]

    @property
    def qlik_space_type(self) -> Optional[str]:
        return self.attributes.qlik_space_type

    @qlik_space_type.setter
    def qlik_space_type(self, qlik_space_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space_type = qlik_space_type

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QlikSpace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikSpace":
            raise ValueError("must be QlikSpace")
        return v

    class Attributes(Qlik.Attributes):
        qlik_space_type: Optional[str] = Field(
            None, description="", alias="qlikSpaceType"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        qlik_datasets: Optional[list[QlikDataset]] = Field(
            None, description="", alias="qlikDatasets"
        )  # relationship
        qlik_apps: Optional[list[QlikApp]] = Field(
            None, description="", alias="qlikApps"
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

    attributes: "QlikSpace.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikApp(Qlik):
    """Description"""

    def __setattr__(self, name, value):
        if name in QlikApp._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "qlik_has_section_access",
        "qlik_origin_app_id",
        "qlik_is_encrypted",
        "qlik_is_direct_query_mode",
        "qlik_app_static_byte_size",
        "terms",
    ]

    @property
    def qlik_has_section_access(self) -> Optional[bool]:
        return self.attributes.qlik_has_section_access

    @qlik_has_section_access.setter
    def qlik_has_section_access(self, qlik_has_section_access: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_has_section_access = qlik_has_section_access

    @property
    def qlik_origin_app_id(self) -> Optional[str]:
        return self.attributes.qlik_origin_app_id

    @qlik_origin_app_id.setter
    def qlik_origin_app_id(self, qlik_origin_app_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_origin_app_id = qlik_origin_app_id

    @property
    def qlik_is_encrypted(self) -> Optional[bool]:
        return self.attributes.qlik_is_encrypted

    @qlik_is_encrypted.setter
    def qlik_is_encrypted(self, qlik_is_encrypted: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_is_encrypted = qlik_is_encrypted

    @property
    def qlik_is_direct_query_mode(self) -> Optional[bool]:
        return self.attributes.qlik_is_direct_query_mode

    @qlik_is_direct_query_mode.setter
    def qlik_is_direct_query_mode(self, qlik_is_direct_query_mode: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_is_direct_query_mode = qlik_is_direct_query_mode

    @property
    def qlik_app_static_byte_size(self) -> Optional[int]:
        return self.attributes.qlik_app_static_byte_size

    @qlik_app_static_byte_size.setter
    def qlik_app_static_byte_size(self, qlik_app_static_byte_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_app_static_byte_size = qlik_app_static_byte_size

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QlikApp", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikApp":
            raise ValueError("must be QlikApp")
        return v

    class Attributes(Qlik.Attributes):
        qlik_has_section_access: Optional[bool] = Field(
            None, description="", alias="qlikHasSectionAccess"
        )
        qlik_origin_app_id: Optional[str] = Field(
            None, description="", alias="qlikOriginAppId"
        )
        qlik_is_encrypted: Optional[bool] = Field(
            None, description="", alias="qlikIsEncrypted"
        )
        qlik_is_direct_query_mode: Optional[bool] = Field(
            None, description="", alias="qlikIsDirectQueryMode"
        )
        qlik_app_static_byte_size: Optional[int] = Field(
            None, description="", alias="qlikAppStaticByteSize"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        qlik_space: Optional[QlikSpace] = Field(
            None, description="", alias="qlikSpace"
        )  # relationship
        qlik_sheets: Optional[list[QlikSheet]] = Field(
            None, description="", alias="qlikSheets"
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

    attributes: "QlikApp.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikChart(Qlik):
    """Description"""

    def __setattr__(self, name, value):
        if name in QlikChart._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "qlik_chart_subtitle",
        "qlik_chart_footnote",
        "qlik_chart_orientation",
        "qlik_chart_type",
        "terms",
    ]

    @property
    def qlik_chart_subtitle(self) -> Optional[str]:
        return self.attributes.qlik_chart_subtitle

    @qlik_chart_subtitle.setter
    def qlik_chart_subtitle(self, qlik_chart_subtitle: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_chart_subtitle = qlik_chart_subtitle

    @property
    def qlik_chart_footnote(self) -> Optional[str]:
        return self.attributes.qlik_chart_footnote

    @qlik_chart_footnote.setter
    def qlik_chart_footnote(self, qlik_chart_footnote: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_chart_footnote = qlik_chart_footnote

    @property
    def qlik_chart_orientation(self) -> Optional[str]:
        return self.attributes.qlik_chart_orientation

    @qlik_chart_orientation.setter
    def qlik_chart_orientation(self, qlik_chart_orientation: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_chart_orientation = qlik_chart_orientation

    @property
    def qlik_chart_type(self) -> Optional[str]:
        return self.attributes.qlik_chart_type

    @qlik_chart_type.setter
    def qlik_chart_type(self, qlik_chart_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_chart_type = qlik_chart_type

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QlikChart", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikChart":
            raise ValueError("must be QlikChart")
        return v

    class Attributes(Qlik.Attributes):
        qlik_chart_subtitle: Optional[str] = Field(
            None, description="", alias="qlikChartSubtitle"
        )
        qlik_chart_footnote: Optional[str] = Field(
            None, description="", alias="qlikChartFootnote"
        )
        qlik_chart_orientation: Optional[str] = Field(
            None, description="", alias="qlikChartOrientation"
        )
        qlik_chart_type: Optional[str] = Field(
            None, description="", alias="qlikChartType"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        qlik_sheet: Optional[QlikSheet] = Field(
            None, description="", alias="qlikSheet"
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

    attributes: "QlikChart.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikDataset(Qlik):
    """Description"""

    def __setattr__(self, name, value):
        if name in QlikDataset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "qlik_dataset_technical_name",
        "qlik_dataset_type",
        "qlik_dataset_uri",
        "qlik_dataset_subtype",
        "terms",
    ]

    @property
    def qlik_dataset_technical_name(self) -> Optional[str]:
        return self.attributes.qlik_dataset_technical_name

    @qlik_dataset_technical_name.setter
    def qlik_dataset_technical_name(self, qlik_dataset_technical_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_technical_name = qlik_dataset_technical_name

    @property
    def qlik_dataset_type(self) -> Optional[str]:
        return self.attributes.qlik_dataset_type

    @qlik_dataset_type.setter
    def qlik_dataset_type(self, qlik_dataset_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_type = qlik_dataset_type

    @property
    def qlik_dataset_uri(self) -> Optional[str]:
        return self.attributes.qlik_dataset_uri

    @qlik_dataset_uri.setter
    def qlik_dataset_uri(self, qlik_dataset_uri: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_uri = qlik_dataset_uri

    @property
    def qlik_dataset_subtype(self) -> Optional[str]:
        return self.attributes.qlik_dataset_subtype

    @qlik_dataset_subtype.setter
    def qlik_dataset_subtype(self, qlik_dataset_subtype: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_subtype = qlik_dataset_subtype

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QlikDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikDataset":
            raise ValueError("must be QlikDataset")
        return v

    class Attributes(Qlik.Attributes):
        qlik_dataset_technical_name: Optional[str] = Field(
            None, description="", alias="qlikDatasetTechnicalName"
        )
        qlik_dataset_type: Optional[str] = Field(
            None, description="", alias="qlikDatasetType"
        )
        qlik_dataset_uri: Optional[str] = Field(
            None, description="", alias="qlikDatasetUri"
        )
        qlik_dataset_subtype: Optional[str] = Field(
            None, description="", alias="qlikDatasetSubtype"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        qlik_space: Optional[QlikSpace] = Field(
            None, description="", alias="qlikSpace"
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

    attributes: "QlikDataset.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikSheet(Qlik):
    """Description"""

    def __setattr__(self, name, value):
        if name in QlikSheet._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "qlik_sheet_is_approved",
        "terms",
    ]

    @property
    def qlik_sheet_is_approved(self) -> Optional[bool]:
        return self.attributes.qlik_sheet_is_approved

    @qlik_sheet_is_approved.setter
    def qlik_sheet_is_approved(self, qlik_sheet_is_approved: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_sheet_is_approved = qlik_sheet_is_approved

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QlikSheet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikSheet":
            raise ValueError("must be QlikSheet")
        return v

    class Attributes(Qlik.Attributes):
        qlik_sheet_is_approved: Optional[bool] = Field(
            None, description="", alias="qlikSheetIsApproved"
        )
        qlik_app: Optional[QlikApp] = Field(
            None, description="", alias="qlikApp"
        )  # relationship
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        qlik_charts: Optional[list[QlikChart]] = Field(
            None, description="", alias="qlikCharts"
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

    attributes: "QlikSheet.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauWorkbook(Tableau):
    """Description"""

    def __setattr__(self, name, value):
        if name in TableauWorkbook._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_name",
        "top_level_project_qualified_name",
        "project_hierarchy",
        "terms",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return self.attributes.project_qualified_name

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_name(self) -> Optional[str]:
        return self.attributes.top_level_project_name

    @top_level_project_name.setter
    def top_level_project_name(self, top_level_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_name = top_level_project_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return self.attributes.top_level_project_qualified_name

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("TableauWorkbook", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauWorkbook":
            raise ValueError("must be TableauWorkbook")
        return v

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

    def __setattr__(self, name, value):
        if name in TableauDatasourceField._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_qualified_name",
        "workbook_qualified_name",
        "datasource_qualified_name",
        "project_hierarchy",
        "fully_qualified_name",
        "tableau_datasource_field_data_category",
        "tableau_datasource_field_role",
        "tableau_datasource_field_data_type",
        "upstream_tables",
        "tableau_datasource_field_formula",
        "tableau_datasource_field_bin_size",
        "upstream_columns",
        "upstream_fields",
        "datasource_field_type",
        "terms",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return self.attributes.project_qualified_name

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return self.attributes.top_level_project_qualified_name

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def workbook_qualified_name(self) -> Optional[str]:
        return self.attributes.workbook_qualified_name

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def datasource_qualified_name(self) -> Optional[str]:
        return self.attributes.datasource_qualified_name

    @datasource_qualified_name.setter
    def datasource_qualified_name(self, datasource_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource_qualified_name = datasource_qualified_name

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def fully_qualified_name(self) -> Optional[str]:
        return self.attributes.fully_qualified_name

    @fully_qualified_name.setter
    def fully_qualified_name(self, fully_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fully_qualified_name = fully_qualified_name

    @property
    def tableau_datasource_field_data_category(self) -> Optional[str]:
        return self.attributes.tableau_datasource_field_data_category

    @tableau_datasource_field_data_category.setter
    def tableau_datasource_field_data_category(
        self, tableau_datasource_field_data_category: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_datasource_field_data_category = (
            tableau_datasource_field_data_category
        )

    @property
    def tableau_datasource_field_role(self) -> Optional[str]:
        return self.attributes.tableau_datasource_field_role

    @tableau_datasource_field_role.setter
    def tableau_datasource_field_role(
        self, tableau_datasource_field_role: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_datasource_field_role = tableau_datasource_field_role

    @property
    def tableau_datasource_field_data_type(self) -> Optional[str]:
        return self.attributes.tableau_datasource_field_data_type

    @tableau_datasource_field_data_type.setter
    def tableau_datasource_field_data_type(
        self, tableau_datasource_field_data_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_datasource_field_data_type = (
            tableau_datasource_field_data_type
        )

    @property
    def upstream_tables(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.upstream_tables

    @upstream_tables.setter
    def upstream_tables(self, upstream_tables: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_tables = upstream_tables

    @property
    def tableau_datasource_field_formula(self) -> Optional[str]:
        return self.attributes.tableau_datasource_field_formula

    @tableau_datasource_field_formula.setter
    def tableau_datasource_field_formula(
        self, tableau_datasource_field_formula: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_datasource_field_formula = (
            tableau_datasource_field_formula
        )

    @property
    def tableau_datasource_field_bin_size(self) -> Optional[str]:
        return self.attributes.tableau_datasource_field_bin_size

    @tableau_datasource_field_bin_size.setter
    def tableau_datasource_field_bin_size(
        self, tableau_datasource_field_bin_size: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_datasource_field_bin_size = (
            tableau_datasource_field_bin_size
        )

    @property
    def upstream_columns(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.upstream_columns

    @upstream_columns.setter
    def upstream_columns(self, upstream_columns: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_columns = upstream_columns

    @property
    def upstream_fields(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.upstream_fields

    @upstream_fields.setter
    def upstream_fields(self, upstream_fields: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_fields = upstream_fields

    @property
    def datasource_field_type(self) -> Optional[str]:
        return self.attributes.datasource_field_type

    @datasource_field_type.setter
    def datasource_field_type(self, datasource_field_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource_field_type = datasource_field_type

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("TableauDatasourceField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauDatasourceField":
            raise ValueError("must be TableauDatasourceField")
        return v

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

    def __setattr__(self, name, value):
        if name in TableauCalculatedField._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_qualified_name",
        "workbook_qualified_name",
        "datasource_qualified_name",
        "project_hierarchy",
        "data_category",
        "role",
        "tableau_data_type",
        "formula",
        "upstream_fields",
        "terms",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return self.attributes.project_qualified_name

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return self.attributes.top_level_project_qualified_name

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def workbook_qualified_name(self) -> Optional[str]:
        return self.attributes.workbook_qualified_name

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def datasource_qualified_name(self) -> Optional[str]:
        return self.attributes.datasource_qualified_name

    @datasource_qualified_name.setter
    def datasource_qualified_name(self, datasource_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource_qualified_name = datasource_qualified_name

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def data_category(self) -> Optional[str]:
        return self.attributes.data_category

    @data_category.setter
    def data_category(self, data_category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_category = data_category

    @property
    def role(self) -> Optional[str]:
        return self.attributes.role

    @role.setter
    def role(self, role: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.role = role

    @property
    def tableau_data_type(self) -> Optional[str]:
        return self.attributes.tableau_data_type

    @tableau_data_type.setter
    def tableau_data_type(self, tableau_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_data_type = tableau_data_type

    @property
    def formula(self) -> Optional[str]:
        return self.attributes.formula

    @formula.setter
    def formula(self, formula: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.formula = formula

    @property
    def upstream_fields(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.upstream_fields

    @upstream_fields.setter
    def upstream_fields(self, upstream_fields: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_fields = upstream_fields

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("TableauCalculatedField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauCalculatedField":
            raise ValueError("must be TableauCalculatedField")
        return v

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

    def __setattr__(self, name, value):
        if name in TableauProject._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "top_level_project_qualified_name",
        "is_top_level_project",
        "project_hierarchy",
        "terms",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return self.attributes.top_level_project_qualified_name

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def is_top_level_project(self) -> Optional[bool]:
        return self.attributes.is_top_level_project

    @is_top_level_project.setter
    def is_top_level_project(self, is_top_level_project: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_top_level_project = is_top_level_project

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("TableauProject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauProject":
            raise ValueError("must be TableauProject")
        return v

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

    def __setattr__(self, name, value):
        if name in TableauMetric._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_qualified_name",
        "project_hierarchy",
        "terms",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return self.attributes.project_qualified_name

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return self.attributes.top_level_project_qualified_name

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("TableauMetric", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauMetric":
            raise ValueError("must be TableauMetric")
        return v

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


class TableauSite(Tableau):
    """Description"""

    def __setattr__(self, name, value):
        if name in TableauSite._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("TableauSite", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauSite":
            raise ValueError("must be TableauSite")
        return v

    class Attributes(Tableau.Attributes):
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        projects: Optional[list[TableauProject]] = Field(
            None, description="", alias="projects"
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

    attributes: "TableauSite.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauDatasource(Tableau):
    """Description"""

    def __setattr__(self, name, value):
        if name in TableauDatasource._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_qualified_name",
        "workbook_qualified_name",
        "project_hierarchy",
        "is_published",
        "has_extracts",
        "is_certified",
        "certifier",
        "certification_note",
        "certifier_display_name",
        "upstream_tables",
        "upstream_datasources",
        "terms",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return self.attributes.project_qualified_name

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return self.attributes.top_level_project_qualified_name

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def workbook_qualified_name(self) -> Optional[str]:
        return self.attributes.workbook_qualified_name

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def is_published(self) -> Optional[bool]:
        return self.attributes.is_published

    @is_published.setter
    def is_published(self, is_published: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_published = is_published

    @property
    def has_extracts(self) -> Optional[bool]:
        return self.attributes.has_extracts

    @has_extracts.setter
    def has_extracts(self, has_extracts: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.has_extracts = has_extracts

    @property
    def is_certified(self) -> Optional[bool]:
        return self.attributes.is_certified

    @is_certified.setter
    def is_certified(self, is_certified: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_certified = is_certified

    @property
    def certifier(self) -> Optional[dict[str, str]]:
        return self.attributes.certifier

    @certifier.setter
    def certifier(self, certifier: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certifier = certifier

    @property
    def certification_note(self) -> Optional[str]:
        return self.attributes.certification_note

    @certification_note.setter
    def certification_note(self, certification_note: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certification_note = certification_note

    @property
    def certifier_display_name(self) -> Optional[str]:
        return self.attributes.certifier_display_name

    @certifier_display_name.setter
    def certifier_display_name(self, certifier_display_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certifier_display_name = certifier_display_name

    @property
    def upstream_tables(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.upstream_tables

    @upstream_tables.setter
    def upstream_tables(self, upstream_tables: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_tables = upstream_tables

    @property
    def upstream_datasources(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.upstream_datasources

    @upstream_datasources.setter
    def upstream_datasources(
        self, upstream_datasources: Optional[list[dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_datasources = upstream_datasources

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("TableauDatasource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauDatasource":
            raise ValueError("must be TableauDatasource")
        return v

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


class TableauDashboard(Tableau):
    """Description"""

    def __setattr__(self, name, value):
        if name in TableauDashboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "workbook_qualified_name",
        "top_level_project_qualified_name",
        "project_hierarchy",
        "terms",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return self.attributes.project_qualified_name

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def workbook_qualified_name(self) -> Optional[str]:
        return self.attributes.workbook_qualified_name

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return self.attributes.top_level_project_qualified_name

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("TableauDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauDashboard":
            raise ValueError("must be TableauDashboard")
        return v

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

    def __setattr__(self, name, value):
        if name in TableauFlow._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_qualified_name",
        "project_hierarchy",
        "input_fields",
        "output_fields",
        "output_steps",
        "terms",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return self.attributes.project_qualified_name

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return self.attributes.top_level_project_qualified_name

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def input_fields(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.input_fields

    @input_fields.setter
    def input_fields(self, input_fields: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_fields = input_fields

    @property
    def output_fields(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.output_fields

    @output_fields.setter
    def output_fields(self, output_fields: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_fields = output_fields

    @property
    def output_steps(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.output_steps

    @output_steps.setter
    def output_steps(self, output_steps: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_steps = output_steps

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("TableauFlow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauFlow":
            raise ValueError("must be TableauFlow")
        return v

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

    def __setattr__(self, name, value):
        if name in TableauWorksheet._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_qualified_name",
        "project_hierarchy",
        "workbook_qualified_name",
        "terms",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return self.attributes.project_qualified_name

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return self.attributes.top_level_project_qualified_name

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def workbook_qualified_name(self) -> Optional[str]:
        return self.attributes.workbook_qualified_name

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("TableauWorksheet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauWorksheet":
            raise ValueError("must be TableauWorksheet")
        return v

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

    def __setattr__(self, name, value):
        if name in LookerLook._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "folder_name",
        "source_user_id",
        "source_view_count",
        "sourcelast_updater_id",
        "source_last_accessed_at",
        "source_last_viewed_at",
        "source_content_metadata_id",
        "source_query_id",
        "model_name",
        "terms",
    ]

    @property
    def folder_name(self) -> Optional[str]:
        return self.attributes.folder_name

    @folder_name.setter
    def folder_name(self, folder_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.folder_name = folder_name

    @property
    def source_user_id(self) -> Optional[int]:
        return self.attributes.source_user_id

    @source_user_id.setter
    def source_user_id(self, source_user_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_user_id = source_user_id

    @property
    def source_view_count(self) -> Optional[int]:
        return self.attributes.source_view_count

    @source_view_count.setter
    def source_view_count(self, source_view_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_view_count = source_view_count

    @property
    def sourcelast_updater_id(self) -> Optional[int]:
        return self.attributes.sourcelast_updater_id

    @sourcelast_updater_id.setter
    def sourcelast_updater_id(self, sourcelast_updater_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sourcelast_updater_id = sourcelast_updater_id

    @property
    def source_last_accessed_at(self) -> Optional[datetime]:
        return self.attributes.source_last_accessed_at

    @source_last_accessed_at.setter
    def source_last_accessed_at(self, source_last_accessed_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_last_accessed_at = source_last_accessed_at

    @property
    def source_last_viewed_at(self) -> Optional[datetime]:
        return self.attributes.source_last_viewed_at

    @source_last_viewed_at.setter
    def source_last_viewed_at(self, source_last_viewed_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_last_viewed_at = source_last_viewed_at

    @property
    def source_content_metadata_id(self) -> Optional[int]:
        return self.attributes.source_content_metadata_id

    @source_content_metadata_id.setter
    def source_content_metadata_id(self, source_content_metadata_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_content_metadata_id = source_content_metadata_id

    @property
    def source_query_id(self) -> Optional[int]:
        return self.attributes.source_query_id

    @source_query_id.setter
    def source_query_id(self, source_query_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_query_id = source_query_id

    @property
    def model_name(self) -> Optional[str]:
        return self.attributes.model_name

    @model_name.setter
    def model_name(self, model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_name = model_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("LookerLook", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerLook":
            raise ValueError("must be LookerLook")
        return v

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
        source_last_accessed_at: Optional[datetime] = Field(
            None, description="", alias="sourceLastAccessedAt"
        )
        source_last_viewed_at: Optional[datetime] = Field(
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

    def __setattr__(self, name, value):
        if name in LookerDashboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "folder_name",
        "source_user_id",
        "source_view_count",
        "source_metadata_id",
        "sourcelast_updater_id",
        "source_last_accessed_at",
        "source_last_viewed_at",
        "terms",
    ]

    @property
    def folder_name(self) -> Optional[str]:
        return self.attributes.folder_name

    @folder_name.setter
    def folder_name(self, folder_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.folder_name = folder_name

    @property
    def source_user_id(self) -> Optional[int]:
        return self.attributes.source_user_id

    @source_user_id.setter
    def source_user_id(self, source_user_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_user_id = source_user_id

    @property
    def source_view_count(self) -> Optional[int]:
        return self.attributes.source_view_count

    @source_view_count.setter
    def source_view_count(self, source_view_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_view_count = source_view_count

    @property
    def source_metadata_id(self) -> Optional[int]:
        return self.attributes.source_metadata_id

    @source_metadata_id.setter
    def source_metadata_id(self, source_metadata_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_metadata_id = source_metadata_id

    @property
    def sourcelast_updater_id(self) -> Optional[int]:
        return self.attributes.sourcelast_updater_id

    @sourcelast_updater_id.setter
    def sourcelast_updater_id(self, sourcelast_updater_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sourcelast_updater_id = sourcelast_updater_id

    @property
    def source_last_accessed_at(self) -> Optional[datetime]:
        return self.attributes.source_last_accessed_at

    @source_last_accessed_at.setter
    def source_last_accessed_at(self, source_last_accessed_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_last_accessed_at = source_last_accessed_at

    @property
    def source_last_viewed_at(self) -> Optional[datetime]:
        return self.attributes.source_last_viewed_at

    @source_last_viewed_at.setter
    def source_last_viewed_at(self, source_last_viewed_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_last_viewed_at = source_last_viewed_at

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("LookerDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerDashboard":
            raise ValueError("must be LookerDashboard")
        return v

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
        source_last_accessed_at: Optional[datetime] = Field(
            None, description="", alias="sourceLastAccessedAt"
        )
        source_last_viewed_at: Optional[datetime] = Field(
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

    def __setattr__(self, name, value):
        if name in LookerFolder._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "source_content_metadata_id",
        "source_creator_id",
        "source_child_count",
        "source_parent_i_d",
        "terms",
    ]

    @property
    def source_content_metadata_id(self) -> Optional[int]:
        return self.attributes.source_content_metadata_id

    @source_content_metadata_id.setter
    def source_content_metadata_id(self, source_content_metadata_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_content_metadata_id = source_content_metadata_id

    @property
    def source_creator_id(self) -> Optional[int]:
        return self.attributes.source_creator_id

    @source_creator_id.setter
    def source_creator_id(self, source_creator_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_creator_id = source_creator_id

    @property
    def source_child_count(self) -> Optional[int]:
        return self.attributes.source_child_count

    @source_child_count.setter
    def source_child_count(self, source_child_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_child_count = source_child_count

    @property
    def source_parent_i_d(self) -> Optional[int]:
        return self.attributes.source_parent_i_d

    @source_parent_i_d.setter
    def source_parent_i_d(self, source_parent_i_d: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_parent_i_d = source_parent_i_d

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("LookerFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerFolder":
            raise ValueError("must be LookerFolder")
        return v

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

    def __setattr__(self, name, value):
        if name in LookerTile._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "lookml_link_id",
        "merge_result_id",
        "note_text",
        "query_i_d",
        "result_maker_i_d",
        "subtitle_text",
        "look_id",
        "terms",
    ]

    @property
    def lookml_link_id(self) -> Optional[str]:
        return self.attributes.lookml_link_id

    @lookml_link_id.setter
    def lookml_link_id(self, lookml_link_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.lookml_link_id = lookml_link_id

    @property
    def merge_result_id(self) -> Optional[str]:
        return self.attributes.merge_result_id

    @merge_result_id.setter
    def merge_result_id(self, merge_result_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.merge_result_id = merge_result_id

    @property
    def note_text(self) -> Optional[str]:
        return self.attributes.note_text

    @note_text.setter
    def note_text(self, note_text: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.note_text = note_text

    @property
    def query_i_d(self) -> Optional[int]:
        return self.attributes.query_i_d

    @query_i_d.setter
    def query_i_d(self, query_i_d: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_i_d = query_i_d

    @property
    def result_maker_i_d(self) -> Optional[int]:
        return self.attributes.result_maker_i_d

    @result_maker_i_d.setter
    def result_maker_i_d(self, result_maker_i_d: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.result_maker_i_d = result_maker_i_d

    @property
    def subtitle_text(self) -> Optional[str]:
        return self.attributes.subtitle_text

    @subtitle_text.setter
    def subtitle_text(self, subtitle_text: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.subtitle_text = subtitle_text

    @property
    def look_id(self) -> Optional[int]:
        return self.attributes.look_id

    @look_id.setter
    def look_id(self, look_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.look_id = look_id

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("LookerTile", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerTile":
            raise ValueError("must be LookerTile")
        return v

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

    def __setattr__(self, name, value):
        if name in LookerModel._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "project_name",
        "terms",
    ]

    @property
    def project_name(self) -> Optional[str]:
        return self.attributes.project_name

    @project_name.setter
    def project_name(self, project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_name = project_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("LookerModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerModel":
            raise ValueError("must be LookerModel")
        return v

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

    def __setattr__(self, name, value):
        if name in LookerExplore._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "project_name",
        "model_name",
        "source_connection_name",
        "view_name",
        "sql_table_name",
        "terms",
    ]

    @property
    def project_name(self) -> Optional[str]:
        return self.attributes.project_name

    @project_name.setter
    def project_name(self, project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_name = project_name

    @property
    def model_name(self) -> Optional[str]:
        return self.attributes.model_name

    @model_name.setter
    def model_name(self, model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_name = model_name

    @property
    def source_connection_name(self) -> Optional[str]:
        return self.attributes.source_connection_name

    @source_connection_name.setter
    def source_connection_name(self, source_connection_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_connection_name = source_connection_name

    @property
    def view_name(self) -> Optional[str]:
        return self.attributes.view_name

    @view_name.setter
    def view_name(self, view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_name = view_name

    @property
    def sql_table_name(self) -> Optional[str]:
        return self.attributes.sql_table_name

    @sql_table_name.setter
    def sql_table_name(self, sql_table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_table_name = sql_table_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("LookerExplore", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerExplore":
            raise ValueError("must be LookerExplore")
        return v

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

    def __setattr__(self, name, value):
        if name in LookerProject._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("LookerProject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerProject":
            raise ValueError("must be LookerProject")
        return v

    class Attributes(Looker.Attributes):
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        models: Optional[list[LookerModel]] = Field(
            None, description="", alias="models"
        )  # relationship
        explores: Optional[list[LookerExplore]] = Field(
            None, description="", alias="explores"
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
        views: Optional[list[LookerView]] = Field(
            None, description="", alias="views"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "LookerProject.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerQuery(Looker):
    """Description"""

    def __setattr__(self, name, value):
        if name in LookerQuery._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "source_definition",
        "source_definition_database",
        "source_definition_schema",
        "fields",
        "terms",
    ]

    @property
    def source_definition(self) -> Optional[str]:
        return self.attributes.source_definition

    @source_definition.setter
    def source_definition(self, source_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_definition = source_definition

    @property
    def source_definition_database(self) -> Optional[str]:
        return self.attributes.source_definition_database

    @source_definition_database.setter
    def source_definition_database(self, source_definition_database: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_definition_database = source_definition_database

    @property
    def source_definition_schema(self) -> Optional[str]:
        return self.attributes.source_definition_schema

    @source_definition_schema.setter
    def source_definition_schema(self, source_definition_schema: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_definition_schema = source_definition_schema

    @property
    def fields(self) -> Optional[set[str]]:
        return self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("LookerQuery", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerQuery":
            raise ValueError("must be LookerQuery")
        return v

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
        fields: Optional[set[str]] = Field(None, description="", alias="fields")
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

    def __setattr__(self, name, value):
        if name in LookerField._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "project_name",
        "looker_explore_qualified_name",
        "looker_view_qualified_name",
        "model_name",
        "source_definition",
        "looker_field_data_type",
        "looker_times_used",
        "terms",
    ]

    @property
    def project_name(self) -> Optional[str]:
        return self.attributes.project_name

    @project_name.setter
    def project_name(self, project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_name = project_name

    @property
    def looker_explore_qualified_name(self) -> Optional[str]:
        return self.attributes.looker_explore_qualified_name

    @looker_explore_qualified_name.setter
    def looker_explore_qualified_name(
        self, looker_explore_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_explore_qualified_name = looker_explore_qualified_name

    @property
    def looker_view_qualified_name(self) -> Optional[str]:
        return self.attributes.looker_view_qualified_name

    @looker_view_qualified_name.setter
    def looker_view_qualified_name(self, looker_view_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_view_qualified_name = looker_view_qualified_name

    @property
    def model_name(self) -> Optional[str]:
        return self.attributes.model_name

    @model_name.setter
    def model_name(self, model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_name = model_name

    @property
    def source_definition(self) -> Optional[str]:
        return self.attributes.source_definition

    @source_definition.setter
    def source_definition(self, source_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_definition = source_definition

    @property
    def looker_field_data_type(self) -> Optional[str]:
        return self.attributes.looker_field_data_type

    @looker_field_data_type.setter
    def looker_field_data_type(self, looker_field_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_field_data_type = looker_field_data_type

    @property
    def looker_times_used(self) -> Optional[int]:
        return self.attributes.looker_times_used

    @looker_times_used.setter
    def looker_times_used(self, looker_times_used: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_times_used = looker_times_used

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("LookerField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerField":
            raise ValueError("must be LookerField")
        return v

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

    def __setattr__(self, name, value):
        if name in LookerView._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "project_name",
        "terms",
    ]

    @property
    def project_name(self) -> Optional[str]:
        return self.attributes.project_name

    @project_name.setter
    def project_name(self, project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_name = project_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("LookerView", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerView":
            raise ValueError("must be LookerView")
        return v

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


class RedashDashboard(Redash):
    """Description"""

    def __setattr__(self, name, value):
        if name in RedashDashboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "redash_dashboard_widget_count",
        "terms",
    ]

    @property
    def redash_dashboard_widget_count(self) -> Optional[int]:
        return self.attributes.redash_dashboard_widget_count

    @redash_dashboard_widget_count.setter
    def redash_dashboard_widget_count(
        self, redash_dashboard_widget_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_dashboard_widget_count = redash_dashboard_widget_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("RedashDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "RedashDashboard":
            raise ValueError("must be RedashDashboard")
        return v

    class Attributes(Redash.Attributes):
        redash_dashboard_widget_count: Optional[int] = Field(
            None, description="", alias="redashDashboardWidgetCount"
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

    attributes: "RedashDashboard.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class RedashQuery(Redash):
    """Description"""

    def __setattr__(self, name, value):
        if name in RedashQuery._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "redash_query_s_q_l",
        "redash_query_parameters",
        "redash_query_schedule",
        "redash_query_last_execution_runtime",
        "redash_query_last_executed_at",
        "redash_query_schedule_humanized",
        "terms",
    ]

    @property
    def redash_query_s_q_l(self) -> Optional[str]:
        return self.attributes.redash_query_s_q_l

    @redash_query_s_q_l.setter
    def redash_query_s_q_l(self, redash_query_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_s_q_l = redash_query_s_q_l

    @property
    def redash_query_parameters(self) -> Optional[str]:
        return self.attributes.redash_query_parameters

    @redash_query_parameters.setter
    def redash_query_parameters(self, redash_query_parameters: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_parameters = redash_query_parameters

    @property
    def redash_query_schedule(self) -> Optional[dict[str, str]]:
        return self.attributes.redash_query_schedule

    @redash_query_schedule.setter
    def redash_query_schedule(self, redash_query_schedule: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_schedule = redash_query_schedule

    @property
    def redash_query_last_execution_runtime(self) -> Optional[float]:
        return self.attributes.redash_query_last_execution_runtime

    @redash_query_last_execution_runtime.setter
    def redash_query_last_execution_runtime(
        self, redash_query_last_execution_runtime: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_last_execution_runtime = (
            redash_query_last_execution_runtime
        )

    @property
    def redash_query_last_executed_at(self) -> Optional[datetime]:
        return self.attributes.redash_query_last_executed_at

    @redash_query_last_executed_at.setter
    def redash_query_last_executed_at(
        self, redash_query_last_executed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_last_executed_at = redash_query_last_executed_at

    @property
    def redash_query_schedule_humanized(self) -> Optional[str]:
        return self.attributes.redash_query_schedule_humanized

    @redash_query_schedule_humanized.setter
    def redash_query_schedule_humanized(
        self, redash_query_schedule_humanized: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_schedule_humanized = (
            redash_query_schedule_humanized
        )

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("RedashQuery", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "RedashQuery":
            raise ValueError("must be RedashQuery")
        return v

    class Attributes(Redash.Attributes):
        redash_query_s_q_l: Optional[str] = Field(
            None, description="", alias="redashQuerySQL"
        )
        redash_query_parameters: Optional[str] = Field(
            None, description="", alias="redashQueryParameters"
        )
        redash_query_schedule: Optional[dict[str, str]] = Field(
            None, description="", alias="redashQuerySchedule"
        )
        redash_query_last_execution_runtime: Optional[float] = Field(
            None, description="", alias="redashQueryLastExecutionRuntime"
        )
        redash_query_last_executed_at: Optional[datetime] = Field(
            None, description="", alias="redashQueryLastExecutedAt"
        )
        redash_query_schedule_humanized: Optional[str] = Field(
            None, description="", alias="redashQueryScheduleHumanized"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        redash_visualizations: Optional[list[RedashVisualization]] = Field(
            None, description="", alias="redashVisualizations"
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

    attributes: "RedashQuery.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class RedashVisualization(Redash):
    """Description"""

    def __setattr__(self, name, value):
        if name in RedashVisualization._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "redash_visualization_type",
        "redash_query_name",
        "redash_query_qualified_name",
        "terms",
    ]

    @property
    def redash_visualization_type(self) -> Optional[str]:
        return self.attributes.redash_visualization_type

    @redash_visualization_type.setter
    def redash_visualization_type(self, redash_visualization_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_visualization_type = redash_visualization_type

    @property
    def redash_query_name(self) -> Optional[str]:
        return self.attributes.redash_query_name

    @redash_query_name.setter
    def redash_query_name(self, redash_query_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_name = redash_query_name

    @property
    def redash_query_qualified_name(self) -> Optional[str]:
        return self.attributes.redash_query_qualified_name

    @redash_query_qualified_name.setter
    def redash_query_qualified_name(self, redash_query_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_qualified_name = redash_query_qualified_name

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("RedashVisualization", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "RedashVisualization":
            raise ValueError("must be RedashVisualization")
        return v

    class Attributes(Redash.Attributes):
        redash_visualization_type: Optional[str] = Field(
            None, description="", alias="redashVisualizationType"
        )
        redash_query_name: Optional[str] = Field(
            None, description="", alias="redashQueryName"
        )
        redash_query_qualified_name: Optional[str] = Field(
            None, description="", alias="redashQueryQualifiedName"
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
        redash_query: Optional[RedashQuery] = Field(
            None, description="", alias="redashQuery"
        )  # relationship
        meanings: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="meanings"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "RedashVisualization.Attributes" = Field(
        None,
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceObject(Salesforce):
    """Description"""

    def __setattr__(self, name, value):
        if name in SalesforceObject._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "is_custom",
        "is_mergable",
        "is_queryable",
        "field_count",
        "terms",
    ]

    @property
    def is_custom(self) -> Optional[bool]:
        return self.attributes.is_custom

    @is_custom.setter
    def is_custom(self, is_custom: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_custom = is_custom

    @property
    def is_mergable(self) -> Optional[bool]:
        return self.attributes.is_mergable

    @is_mergable.setter
    def is_mergable(self, is_mergable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_mergable = is_mergable

    @property
    def is_queryable(self) -> Optional[bool]:
        return self.attributes.is_queryable

    @is_queryable.setter
    def is_queryable(self, is_queryable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_queryable = is_queryable

    @property
    def field_count(self) -> Optional[int]:
        return self.attributes.field_count

    @field_count.setter
    def field_count(self, field_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.field_count = field_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SalesforceObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceObject":
            raise ValueError("must be SalesforceObject")
        return v

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

    def __setattr__(self, name, value):
        if name in SalesforceField._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "data_type",
        "object_qualified_name",
        "order",
        "inline_help_text",
        "is_calculated",
        "formula",
        "is_case_sensitive",
        "is_encrypted",
        "max_length",
        "is_nullable",
        "precision",
        "numeric_scale",
        "is_unique",
        "picklist_values",
        "is_polymorphic_foreign_key",
        "default_value_formula",
        "terms",
    ]

    @property
    def data_type(self) -> Optional[str]:
        return self.attributes.data_type

    @data_type.setter
    def data_type(self, data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_type = data_type

    @property
    def object_qualified_name(self) -> Optional[str]:
        return self.attributes.object_qualified_name

    @object_qualified_name.setter
    def object_qualified_name(self, object_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.object_qualified_name = object_qualified_name

    @property
    def order(self) -> Optional[int]:
        return self.attributes.order

    @order.setter
    def order(self, order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.order = order

    @property
    def inline_help_text(self) -> Optional[str]:
        return self.attributes.inline_help_text

    @inline_help_text.setter
    def inline_help_text(self, inline_help_text: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inline_help_text = inline_help_text

    @property
    def is_calculated(self) -> Optional[bool]:
        return self.attributes.is_calculated

    @is_calculated.setter
    def is_calculated(self, is_calculated: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_calculated = is_calculated

    @property
    def formula(self) -> Optional[str]:
        return self.attributes.formula

    @formula.setter
    def formula(self, formula: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.formula = formula

    @property
    def is_case_sensitive(self) -> Optional[bool]:
        return self.attributes.is_case_sensitive

    @is_case_sensitive.setter
    def is_case_sensitive(self, is_case_sensitive: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_case_sensitive = is_case_sensitive

    @property
    def is_encrypted(self) -> Optional[bool]:
        return self.attributes.is_encrypted

    @is_encrypted.setter
    def is_encrypted(self, is_encrypted: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_encrypted = is_encrypted

    @property
    def max_length(self) -> Optional[int]:
        return self.attributes.max_length

    @max_length.setter
    def max_length(self, max_length: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.max_length = max_length

    @property
    def is_nullable(self) -> Optional[bool]:
        return self.attributes.is_nullable

    @is_nullable.setter
    def is_nullable(self, is_nullable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_nullable = is_nullable

    @property
    def precision(self) -> Optional[int]:
        return self.attributes.precision

    @precision.setter
    def precision(self, precision: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.precision = precision

    @property
    def numeric_scale(self) -> Optional[float]:
        return self.attributes.numeric_scale

    @numeric_scale.setter
    def numeric_scale(self, numeric_scale: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.numeric_scale = numeric_scale

    @property
    def is_unique(self) -> Optional[bool]:
        return self.attributes.is_unique

    @is_unique.setter
    def is_unique(self, is_unique: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_unique = is_unique

    @property
    def picklist_values(self) -> Optional[set[str]]:
        return self.attributes.picklist_values

    @picklist_values.setter
    def picklist_values(self, picklist_values: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.picklist_values = picklist_values

    @property
    def is_polymorphic_foreign_key(self) -> Optional[bool]:
        return self.attributes.is_polymorphic_foreign_key

    @is_polymorphic_foreign_key.setter
    def is_polymorphic_foreign_key(self, is_polymorphic_foreign_key: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_polymorphic_foreign_key = is_polymorphic_foreign_key

    @property
    def default_value_formula(self) -> Optional[str]:
        return self.attributes.default_value_formula

    @default_value_formula.setter
    def default_value_formula(self, default_value_formula: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.default_value_formula = default_value_formula

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SalesforceField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceField":
            raise ValueError("must be SalesforceField")
        return v

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
        picklist_values: Optional[set[str]] = Field(
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

    def __setattr__(self, name, value):
        if name in SalesforceOrganization._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "source_id",
        "terms",
    ]

    @property
    def source_id(self) -> Optional[str]:
        return self.attributes.source_id

    @source_id.setter
    def source_id(self, source_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_id = source_id

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SalesforceOrganization", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceOrganization":
            raise ValueError("must be SalesforceOrganization")
        return v

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

    def __setattr__(self, name, value):
        if name in SalesforceDashboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "source_id",
        "dashboard_type",
        "report_count",
        "terms",
    ]

    @property
    def source_id(self) -> Optional[str]:
        return self.attributes.source_id

    @source_id.setter
    def source_id(self, source_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_id = source_id

    @property
    def dashboard_type(self) -> Optional[str]:
        return self.attributes.dashboard_type

    @dashboard_type.setter
    def dashboard_type(self, dashboard_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard_type = dashboard_type

    @property
    def report_count(self) -> Optional[int]:
        return self.attributes.report_count

    @report_count.setter
    def report_count(self, report_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_count = report_count

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SalesforceDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceDashboard":
            raise ValueError("must be SalesforceDashboard")
        return v

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

    def __setattr__(self, name, value):
        if name in SalesforceReport._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "source_id",
        "report_type",
        "detail_columns",
        "terms",
    ]

    @property
    def source_id(self) -> Optional[str]:
        return self.attributes.source_id

    @source_id.setter
    def source_id(self, source_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_id = source_id

    @property
    def report_type(self) -> Optional[dict[str, str]]:
        return self.attributes.report_type

    @report_type.setter
    def report_type(self, report_type: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_type = report_type

    @property
    def detail_columns(self) -> Optional[set[str]]:
        return self.attributes.detail_columns

    @detail_columns.setter
    def detail_columns(self, detail_columns: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.detail_columns = detail_columns

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("SalesforceReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceReport":
            raise ValueError("must be SalesforceReport")
        return v

    class Attributes(Salesforce.Attributes):
        source_id: Optional[str] = Field(None, description="", alias="sourceId")
        report_type: Optional[dict[str, str]] = Field(
            None, description="", alias="reportType"
        )
        detail_columns: Optional[set[str]] = Field(
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


class QlikStream(QlikSpace):
    """Description"""

    def __setattr__(self, name, value):
        if name in QlikStream._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "terms",
    ]

    @property
    def terms(self) -> list[AtlasGlossaryTerm]:
        if self.attributes is None:
            self.attributes = self.Attributes()
        return [] if self.attributes.meanings is None else self.attributes.meanings

    @terms.setter
    def terms(self, terms: list[AtlasGlossaryTerm]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = terms

    type_name: str = Field("QlikStream", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikStream":
            raise ValueError("must be QlikStream")
        return v

    class Attributes(QlikSpace.Attributes):
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        qlik_datasets: Optional[list[QlikDataset]] = Field(
            None, description="", alias="qlikDatasets"
        )  # relationship
        links: Optional[list[Link]] = Field(
            None, description="", alias="links"
        )  # relationship
        qlik_apps: Optional[list[QlikApp]] = Field(
            None, description="", alias="qlikApps"
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

    attributes: "QlikStream.Attributes" = Field(
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

Azure.Attributes.update_forward_refs()

AWS.Attributes.update_forward_refs()

BIProcess.Attributes.update_forward_refs()

ColumnProcess.Attributes.update_forward_refs()

Collection.Attributes.update_forward_refs()

Folder.Attributes.update_forward_refs()

EventStore.Attributes.update_forward_refs()

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

ADLS.Attributes.update_forward_refs()

S3.Attributes.update_forward_refs()

DbtColumnProcess.Attributes.update_forward_refs()

Kafka.Attributes.update_forward_refs()

Metric.Attributes.update_forward_refs()

Metabase.Attributes.update_forward_refs()

QuickSight.Attributes.update_forward_refs()

Thoughtspot.Attributes.update_forward_refs()

PowerBI.Attributes.update_forward_refs()

Preset.Attributes.update_forward_refs()

Mode.Attributes.update_forward_refs()

Sigma.Attributes.update_forward_refs()

Qlik.Attributes.update_forward_refs()

Tableau.Attributes.update_forward_refs()

Looker.Attributes.update_forward_refs()

Redash.Attributes.update_forward_refs()

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

SnowflakeStream.Attributes.update_forward_refs()

SnowflakePipe.Attributes.update_forward_refs()

Database.Attributes.update_forward_refs()

Procedure.Attributes.update_forward_refs()

View.Attributes.update_forward_refs()

MaterialisedView.Attributes.update_forward_refs()

GCSObject.Attributes.update_forward_refs()

GCSBucket.Attributes.update_forward_refs()

ADLSAccount.Attributes.update_forward_refs()

ADLSContainer.Attributes.update_forward_refs()

ADLSObject.Attributes.update_forward_refs()

S3Bucket.Attributes.update_forward_refs()

S3Object.Attributes.update_forward_refs()

KafkaTopic.Attributes.update_forward_refs()

KafkaConsumerGroup.Attributes.update_forward_refs()

MetabaseQuestion.Attributes.update_forward_refs()

MetabaseCollection.Attributes.update_forward_refs()

MetabaseDashboard.Attributes.update_forward_refs()

QuickSightFolder.Attributes.update_forward_refs()

QuickSightDashboardVisual.Attributes.update_forward_refs()

QuickSightAnalysisVisual.Attributes.update_forward_refs()

QuickSightDatasetField.Attributes.update_forward_refs()

QuickSightAnalysis.Attributes.update_forward_refs()

QuickSightDashboard.Attributes.update_forward_refs()

QuickSightDataset.Attributes.update_forward_refs()

ThoughtspotLiveboard.Attributes.update_forward_refs()

ThoughtspotDashlet.Attributes.update_forward_refs()

ThoughtspotAnswer.Attributes.update_forward_refs()

PowerBIReport.Attributes.update_forward_refs()

PowerBIMeasure.Attributes.update_forward_refs()

PowerBIColumn.Attributes.update_forward_refs()

PowerBITable.Attributes.update_forward_refs()

PowerBITile.Attributes.update_forward_refs()

PowerBIDatasource.Attributes.update_forward_refs()

PowerBIWorkspace.Attributes.update_forward_refs()

PowerBIDataset.Attributes.update_forward_refs()

PowerBIDashboard.Attributes.update_forward_refs()

PowerBIDataflow.Attributes.update_forward_refs()

PowerBIPage.Attributes.update_forward_refs()

PresetChart.Attributes.update_forward_refs()

PresetDataset.Attributes.update_forward_refs()

PresetDashboard.Attributes.update_forward_refs()

PresetWorkspace.Attributes.update_forward_refs()

ModeReport.Attributes.update_forward_refs()

ModeQuery.Attributes.update_forward_refs()

ModeChart.Attributes.update_forward_refs()

ModeWorkspace.Attributes.update_forward_refs()

ModeCollection.Attributes.update_forward_refs()

SigmaDatasetColumn.Attributes.update_forward_refs()

SigmaDataset.Attributes.update_forward_refs()

SigmaWorkbook.Attributes.update_forward_refs()

SigmaDataElementField.Attributes.update_forward_refs()

SigmaPage.Attributes.update_forward_refs()

SigmaDataElement.Attributes.update_forward_refs()

QlikSpace.Attributes.update_forward_refs()

QlikApp.Attributes.update_forward_refs()

QlikChart.Attributes.update_forward_refs()

QlikDataset.Attributes.update_forward_refs()

QlikSheet.Attributes.update_forward_refs()

TableauWorkbook.Attributes.update_forward_refs()

TableauDatasourceField.Attributes.update_forward_refs()

TableauCalculatedField.Attributes.update_forward_refs()

TableauProject.Attributes.update_forward_refs()

TableauMetric.Attributes.update_forward_refs()

TableauSite.Attributes.update_forward_refs()

TableauDatasource.Attributes.update_forward_refs()

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

RedashDashboard.Attributes.update_forward_refs()

RedashQuery.Attributes.update_forward_refs()

RedashVisualization.Attributes.update_forward_refs()

SalesforceObject.Attributes.update_forward_refs()

SalesforceField.Attributes.update_forward_refs()

SalesforceOrganization.Attributes.update_forward_refs()

SalesforceDashboard.Attributes.update_forward_refs()

SalesforceReport.Attributes.update_forward_refs()

QlikStream.Attributes.update_forward_refs()
