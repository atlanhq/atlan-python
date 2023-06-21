# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)

from __future__ import annotations

import hashlib
import sys
from datetime import datetime
from io import StringIO
from typing import Any, ClassVar, Dict, List, Optional, Set, Type, TypeVar
from urllib.parse import quote, unquote

from pydantic import Field, PrivateAttr, StrictStr, root_validator, validator

from pyatlan.model.core import Announcement, AtlanObject, Classification, Meaning
from pyatlan.model.custom_metadata import CustomMetadataDict, CustomMetadataProxy
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
    AuthPolicyCategory,
    AuthPolicyResourceCategory,
    AuthPolicyType,
    CertificateStatus,
    DataAction,
    EntityStatus,
    FileType,
    GoogleDatastudioAssetType,
    IconType,
    KafkaTopicCompressionType,
    PersonaGlossaryAction,
    PersonaMetadataAction,
    PowerbiEndorsement,
    PurposeMetadataAction,
    QueryUsernameStrategy,
    QuickSightAnalysisStatus,
    QuickSightDatasetFieldType,
    QuickSightDatasetImportMode,
    QuickSightFolderType,
    SourceCostUnitType,
)
from pyatlan.model.internal import AtlasServer, Internal
from pyatlan.model.structs import (
    AuthPolicyCondition,
    AuthPolicyValiditySchedule,
    AwsTag,
    AzureTag,
    BadgeCondition,
    ColumnValueFrequencyMap,
    DbtMetricFilter,
    GoogleLabel,
    GoogleTag,
    Histogram,
    KafkaTopicConsumption,
    MCRuleComparison,
    MCRuleSchedule,
    PopularityInsights,
    SourceTagAttribute,
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
        if name in Referenceable._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "qualified_name",
        "replicated_from",
        "replicated_to",
        "assigned_terms",
    ]

    @property
    def qualified_name(self) -> str:
        return None if self.attributes is None else self.attributes.qualified_name

    @qualified_name.setter
    def qualified_name(self, qualified_name: str):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qualified_name = qualified_name

    @property
    def replicated_from(self) -> Optional[list[AtlasServer]]:
        return None if self.attributes is None else self.attributes.replicated_from

    @replicated_from.setter
    def replicated_from(self, replicated_from: Optional[list[AtlasServer]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.replicated_from = replicated_from

    @property
    def replicated_to(self) -> Optional[list[AtlasServer]]:
        return None if self.attributes is None else self.attributes.replicated_to

    @replicated_to.setter
    def replicated_to(self, replicated_to: Optional[list[AtlasServer]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.replicated_to = replicated_to

    @property
    def assigned_terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.meanings

    @assigned_terms.setter
    def assigned_terms(self, assigned_terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = assigned_terms

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

    _metadata_proxy: CustomMetadataProxy = PrivateAttr()
    attributes: "Referenceable.Attributes" = Field(
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
            qualified_name=self.qualified_name, name=self.name
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
        "mc_monitors",
        "files",
        "mc_incidents",
        "links",
        "metrics",
        "readme",
        "assigned_terms",
    ]

    @property
    def name(self) -> str:
        return None if self.attributes is None else self.attributes.name

    @name.setter
    def name(self, name: str):
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
    def assigned_terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.meanings

    @assigned_terms.setter
    def assigned_terms(self, assigned_terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.meanings = assigned_terms

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


class DataSet(Asset, type_name="DataSet"):
    """Description"""

    type_name: str = Field("DataSet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataSet":
            raise ValueError("must be DataSet")
        return v

    def __setattr__(self, name, value):
        if name in DataSet._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


class Connection(Asset, type_name="Connection"):
    """Description"""

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
        if not admin_users and not admin_groups and not admin_roles:
            raise ValueError(
                "One of admin_user, admin_groups or admin_roles is required"
            )
        if admin_roles:
            from pyatlan.cache.role_cache import RoleCache

            for role_id in admin_roles:
                if not RoleCache.get_name_for_id(role_id):
                    raise ValueError(
                        f"Provided role ID {role_id} was not found in Atlan."
                    )
        if admin_groups:
            from pyatlan.cache.group_cache import GroupCache

            for group_alias in admin_groups:
                if not GroupCache.get_id_for_alias(group_alias):
                    raise ValueError(
                        f"Provided group name {group_alias} was not found in Atlan."
                    )
        if admin_users:
            from pyatlan.cache.user_cache import UserCache

            for username in admin_users:
                if not UserCache.get_id_for_name(username):
                    raise ValueError(
                        f"Provided username {username} was not found in Atlan."
                    )
        attr = cls.Attributes(
            name=name,
            qualified_name=connector_type.to_qualified_name(),
            connector_name=connector_type.value,
            category=connector_type.category.value,
            admin_users=admin_users or [],
            admin_groups=admin_groups or [],
            admin_roles=admin_roles or [],
        )
        return cls(attributes=attr)

    type_name: str = Field("Connection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Connection":
            raise ValueError("must be Connection")
        return v

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
        "query_timeout",
        "default_credential_guid",
        "connector_icon",
        "connector_image",
        "source_logo",
        "is_sample_data_preview_enabled",
        "popularity_insights_timeframe",
        "has_popularity_insights",
        "connection_dbt_environments",
        "connection_s_s_o_credential_guid",
    ]

    @property
    def category(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.category

    @category.setter
    def category(self, category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.category = category

    @property
    def sub_category(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sub_category

    @sub_category.setter
    def sub_category(self, sub_category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sub_category = sub_category

    @property
    def host(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.host

    @host.setter
    def host(self, host: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.host = host

    @property
    def port(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.port

    @port.setter
    def port(self, port: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.port = port

    @property
    def allow_query(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.allow_query

    @allow_query.setter
    def allow_query(self, allow_query: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.allow_query = allow_query

    @property
    def allow_query_preview(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.allow_query_preview

    @allow_query_preview.setter
    def allow_query_preview(self, allow_query_preview: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.allow_query_preview = allow_query_preview

    @property
    def query_preview_config(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.query_preview_config

    @query_preview_config.setter
    def query_preview_config(self, query_preview_config: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_preview_config = query_preview_config

    @property
    def query_config(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.query_config

    @query_config.setter
    def query_config(self, query_config: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_config = query_config

    @property
    def credential_strategy(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.credential_strategy

    @credential_strategy.setter
    def credential_strategy(self, credential_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.credential_strategy = credential_strategy

    @property
    def preview_credential_strategy(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preview_credential_strategy
        )

    @preview_credential_strategy.setter
    def preview_credential_strategy(self, preview_credential_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preview_credential_strategy = preview_credential_strategy

    @property
    def policy_strategy(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.policy_strategy

    @policy_strategy.setter
    def policy_strategy(self, policy_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_strategy = policy_strategy

    @property
    def query_username_strategy(self) -> Optional[QueryUsernameStrategy]:
        return (
            None if self.attributes is None else self.attributes.query_username_strategy
        )

    @query_username_strategy.setter
    def query_username_strategy(
        self, query_username_strategy: Optional[QueryUsernameStrategy]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_username_strategy = query_username_strategy

    @property
    def row_limit(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.row_limit

    @row_limit.setter
    def row_limit(self, row_limit: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.row_limit = row_limit

    @property
    def query_timeout(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_timeout

    @query_timeout.setter
    def query_timeout(self, query_timeout: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_timeout = query_timeout

    @property
    def default_credential_guid(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.default_credential_guid
        )

    @default_credential_guid.setter
    def default_credential_guid(self, default_credential_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.default_credential_guid = default_credential_guid

    @property
    def connector_icon(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.connector_icon

    @connector_icon.setter
    def connector_icon(self, connector_icon: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connector_icon = connector_icon

    @property
    def connector_image(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.connector_image

    @connector_image.setter
    def connector_image(self, connector_image: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connector_image = connector_image

    @property
    def source_logo(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_logo

    @source_logo.setter
    def source_logo(self, source_logo: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_logo = source_logo

    @property
    def is_sample_data_preview_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.is_sample_data_preview_enabled
        )

    @is_sample_data_preview_enabled.setter
    def is_sample_data_preview_enabled(
        self, is_sample_data_preview_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_sample_data_preview_enabled = is_sample_data_preview_enabled

    @property
    def popularity_insights_timeframe(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.popularity_insights_timeframe
        )

    @popularity_insights_timeframe.setter
    def popularity_insights_timeframe(
        self, popularity_insights_timeframe: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.popularity_insights_timeframe = popularity_insights_timeframe

    @property
    def has_popularity_insights(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.has_popularity_insights
        )

    @has_popularity_insights.setter
    def has_popularity_insights(self, has_popularity_insights: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.has_popularity_insights = has_popularity_insights

    @property
    def connection_dbt_environments(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.connection_dbt_environments
        )

    @connection_dbt_environments.setter
    def connection_dbt_environments(
        self, connection_dbt_environments: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connection_dbt_environments = connection_dbt_environments

    @property
    def connection_s_s_o_credential_guid(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.connection_s_s_o_credential_guid
        )

    @connection_s_s_o_credential_guid.setter
    def connection_s_s_o_credential_guid(
        self, connection_s_s_o_credential_guid: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connection_s_s_o_credential_guid = (
            connection_s_s_o_credential_guid
        )

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
        query_timeout: Optional[int] = Field(None, description="", alias="queryTimeout")
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
        connection_s_s_o_credential_guid: Optional[str] = Field(
            None, description="", alias="connectionSSOCredentialGuid"
        )

    attributes: "Connection.Attributes" = Field(
        default_factory=lambda: Connection.Attributes(),
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
        if name in Process._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "inputs",
        "outputs",
        "code",
        "sql",
        "ast",
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
            qualified_name=self.qualified_name,
            name=self.name,
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

    type_name: str = Field("AtlasGlossaryCategory", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlasGlossaryCategory":
            raise ValueError("must be AtlasGlossaryCategory")
        return v

    def __setattr__(self, name, value):
        if name in AtlasGlossaryCategory._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
    def anchor(self) -> AtlasGlossary:
        return None if self.attributes is None else self.attributes.anchor

    @anchor.setter
    def anchor(self, anchor: AtlasGlossary):
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
        anchor: AtlasGlossary = Field(
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


class Badge(Asset, type_name="Badge"):
    """Description"""

    @classmethod
    # @validate_arguments()
    def create(
        cls,
        *,
        name: StrictStr,
        cm_name: str,
        cm_attribute: str,
        badge_conditions: list[BadgeCondition],
    ) -> Badge:
        return cls(
            status=EntityStatus.ACTIVE,
            attributes=Badge.Attributes.create(
                name=name,
                cm_name=cm_name,
                cm_attribute=cm_attribute,
                badge_conditions=badge_conditions,
            ),
        )

    type_name: str = Field("Badge", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Badge":
            raise ValueError("must be Badge")
        return v

    def __setattr__(self, name, value):
        if name in Badge._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "badge_conditions",
        "badge_metadata_attribute",
    ]

    @property
    def badge_conditions(self) -> Optional[list[BadgeCondition]]:
        return None if self.attributes is None else self.attributes.badge_conditions

    @badge_conditions.setter
    def badge_conditions(self, badge_conditions: Optional[list[BadgeCondition]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.badge_conditions = badge_conditions

    @property
    def badge_metadata_attribute(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.badge_metadata_attribute
        )

    @badge_metadata_attribute.setter
    def badge_metadata_attribute(self, badge_metadata_attribute: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.badge_metadata_attribute = badge_metadata_attribute

    class Attributes(Asset.Attributes):
        badge_conditions: Optional[list[BadgeCondition]] = Field(
            None, description="", alias="badgeConditions"
        )
        badge_metadata_attribute: Optional[str] = Field(
            None, description="", alias="badgeMetadataAttribute"
        )

        @classmethod
        # @validate_arguments()
        def create(
            cls,
            *,
            name: StrictStr,
            cm_name: str,
            cm_attribute: str,
            badge_conditions: list[BadgeCondition],
        ) -> Badge.Attributes:
            validate_required_fields(
                ["name", "cm_name", "cm_attribute", "badge_conditions"],
                [name, cm_name, cm_attribute, badge_conditions],
            )
            from pyatlan.cache.custom_metadata_cache import CustomMetadataCache

            cm_id = CustomMetadataCache.get_id_for_name(cm_name)
            cm_attr_id = CustomMetadataCache.get_attr_id_for_name(
                set_name=cm_name, attr_name=cm_attribute
            )
            return Badge.Attributes(
                name=name,
                qualified_name=f"badges/global/{cm_id}.{cm_attr_id}",
                badge_metadata_attribute=f"{cm_id}.{cm_attr_id}",
                badge_conditions=badge_conditions,
            )

    attributes: "Badge.Attributes" = Field(
        default_factory=lambda: Badge.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AccessControl(Asset, type_name="AccessControl"):
    """Description"""

    type_name: str = Field("AccessControl", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AccessControl":
            raise ValueError("must be AccessControl")
        return v

    def __setattr__(self, name, value):
        if name in AccessControl._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "is_access_control_enabled",
        "deny_custom_metadata_guids",
        "deny_asset_tabs",
        "channel_link",
        "policies",
    ]

    @property
    def is_access_control_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.is_access_control_enabled
        )

    @is_access_control_enabled.setter
    def is_access_control_enabled(self, is_access_control_enabled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_access_control_enabled = is_access_control_enabled

    @property
    def deny_custom_metadata_guids(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.deny_custom_metadata_guids
        )

    @deny_custom_metadata_guids.setter
    def deny_custom_metadata_guids(
        self, deny_custom_metadata_guids: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.deny_custom_metadata_guids = deny_custom_metadata_guids

    @property
    def deny_asset_tabs(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.deny_asset_tabs

    @deny_asset_tabs.setter
    def deny_asset_tabs(self, deny_asset_tabs: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.deny_asset_tabs = deny_asset_tabs

    @property
    def channel_link(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.channel_link

    @channel_link.setter
    def channel_link(self, channel_link: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.channel_link = channel_link

    @property
    def policies(self) -> Optional[list[AuthPolicy]]:
        return None if self.attributes is None else self.attributes.policies

    @policies.setter
    def policies(self, policies: Optional[list[AuthPolicy]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policies = policies

    class Attributes(Asset.Attributes):
        is_access_control_enabled: Optional[bool] = Field(
            None, description="", alias="isAccessControlEnabled"
        )
        deny_custom_metadata_guids: Optional[set[str]] = Field(
            None, description="", alias="denyCustomMetadataGuids"
        )
        deny_asset_tabs: Optional[set[str]] = Field(
            None, description="", alias="denyAssetTabs"
        )
        channel_link: Optional[str] = Field(None, description="", alias="channelLink")
        policies: Optional[list[AuthPolicy]] = Field(
            None, description="", alias="policies"
        )  # relationship

    attributes: "AccessControl.Attributes" = Field(
        default_factory=lambda: AccessControl.Attributes(),
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
        if name in Namespace._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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


class Catalog(Asset, type_name="Catalog"):
    """Description"""

    type_name: str = Field("Catalog", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Catalog":
            raise ValueError("must be Catalog")
        return v

    def __setattr__(self, name, value):
        if name in Catalog._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "input_to_processes",
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
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "Catalog.Attributes" = Field(
        default_factory=lambda: Catalog.Attributes(),
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


class AuthPolicy(Asset, type_name="AuthPolicy"):
    """Description"""

    @classmethod
    # @validate_arguments()
    def create(cls, *, name: str) -> AuthPolicy:
        validate_required_fields(["name"], [name])
        attributes = AuthPolicy.Attributes.create(name=name)
        return cls(attributes=attributes)

    type_name: str = Field("AuthPolicy", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AuthPolicy":
            raise ValueError("must be AuthPolicy")
        return v

    def __setattr__(self, name, value):
        if name in AuthPolicy._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "policy_type",
        "policy_service_name",
        "policy_category",
        "policy_sub_category",
        "policy_users",
        "policy_groups",
        "policy_roles",
        "policy_actions",
        "policy_resources",
        "policy_resource_category",
        "policy_priority",
        "is_policy_enabled",
        "policy_mask_type",
        "policy_validity_schedule",
        "policy_resource_signature",
        "policy_delegate_admin",
        "policy_conditions",
        "access_control",
    ]

    @property
    def policy_type(self) -> Optional[AuthPolicyType]:
        return None if self.attributes is None else self.attributes.policy_type

    @policy_type.setter
    def policy_type(self, policy_type: Optional[AuthPolicyType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_type = policy_type

    @property
    def policy_service_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.policy_service_name

    @policy_service_name.setter
    def policy_service_name(self, policy_service_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_service_name = policy_service_name

    @property
    def policy_category(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.policy_category

    @policy_category.setter
    def policy_category(self, policy_category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_category = policy_category

    @property
    def policy_sub_category(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.policy_sub_category

    @policy_sub_category.setter
    def policy_sub_category(self, policy_sub_category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_sub_category = policy_sub_category

    @property
    def policy_users(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.policy_users

    @policy_users.setter
    def policy_users(self, policy_users: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_users = policy_users

    @property
    def policy_groups(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.policy_groups

    @policy_groups.setter
    def policy_groups(self, policy_groups: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_groups = policy_groups

    @property
    def policy_roles(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.policy_roles

    @policy_roles.setter
    def policy_roles(self, policy_roles: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_roles = policy_roles

    @property
    def policy_actions(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.policy_actions

    @policy_actions.setter
    def policy_actions(self, policy_actions: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_actions = policy_actions

    @property
    def policy_resources(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.policy_resources

    @policy_resources.setter
    def policy_resources(self, policy_resources: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_resources = policy_resources

    @property
    def policy_resource_category(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.policy_resource_category
        )

    @policy_resource_category.setter
    def policy_resource_category(self, policy_resource_category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_resource_category = policy_resource_category

    @property
    def policy_priority(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.policy_priority

    @policy_priority.setter
    def policy_priority(self, policy_priority: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_priority = policy_priority

    @property
    def is_policy_enabled(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_policy_enabled

    @is_policy_enabled.setter
    def is_policy_enabled(self, is_policy_enabled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_policy_enabled = is_policy_enabled

    @property
    def policy_mask_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.policy_mask_type

    @policy_mask_type.setter
    def policy_mask_type(self, policy_mask_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_mask_type = policy_mask_type

    @property
    def policy_validity_schedule(self) -> Optional[list[AuthPolicyValiditySchedule]]:
        return (
            None
            if self.attributes is None
            else self.attributes.policy_validity_schedule
        )

    @policy_validity_schedule.setter
    def policy_validity_schedule(
        self, policy_validity_schedule: Optional[list[AuthPolicyValiditySchedule]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_validity_schedule = policy_validity_schedule

    @property
    def policy_resource_signature(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.policy_resource_signature
        )

    @policy_resource_signature.setter
    def policy_resource_signature(self, policy_resource_signature: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_resource_signature = policy_resource_signature

    @property
    def policy_delegate_admin(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.policy_delegate_admin
        )

    @policy_delegate_admin.setter
    def policy_delegate_admin(self, policy_delegate_admin: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_delegate_admin = policy_delegate_admin

    @property
    def policy_conditions(self) -> Optional[list[AuthPolicyCondition]]:
        return None if self.attributes is None else self.attributes.policy_conditions

    @policy_conditions.setter
    def policy_conditions(self, policy_conditions: Optional[list[AuthPolicyCondition]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_conditions = policy_conditions

    @property
    def access_control(self) -> Optional[AccessControl]:
        return None if self.attributes is None else self.attributes.access_control

    @access_control.setter
    def access_control(self, access_control: Optional[AccessControl]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.access_control = access_control

    class Attributes(Asset.Attributes):
        policy_type: Optional[AuthPolicyType] = Field(
            None, description="", alias="policyType"
        )
        policy_service_name: Optional[str] = Field(
            None, description="", alias="policyServiceName"
        )
        policy_category: Optional[str] = Field(
            None, description="", alias="policyCategory"
        )
        policy_sub_category: Optional[str] = Field(
            None, description="", alias="policySubCategory"
        )
        policy_users: Optional[set[str]] = Field(
            None, description="", alias="policyUsers"
        )
        policy_groups: Optional[set[str]] = Field(
            None, description="", alias="policyGroups"
        )
        policy_roles: Optional[set[str]] = Field(
            None, description="", alias="policyRoles"
        )
        policy_actions: Optional[set[str]] = Field(
            None, description="", alias="policyActions"
        )
        policy_resources: Optional[set[str]] = Field(
            None, description="", alias="policyResources"
        )
        policy_resource_category: Optional[str] = Field(
            None, description="", alias="policyResourceCategory"
        )
        policy_priority: Optional[int] = Field(
            None, description="", alias="policyPriority"
        )
        is_policy_enabled: Optional[bool] = Field(
            None, description="", alias="isPolicyEnabled"
        )
        policy_mask_type: Optional[str] = Field(
            None, description="", alias="policyMaskType"
        )
        policy_validity_schedule: Optional[list[AuthPolicyValiditySchedule]] = Field(
            None, description="", alias="policyValiditySchedule"
        )
        policy_resource_signature: Optional[str] = Field(
            None, description="", alias="policyResourceSignature"
        )
        policy_delegate_admin: Optional[bool] = Field(
            None, description="", alias="policyDelegateAdmin"
        )
        policy_conditions: Optional[list[AuthPolicyCondition]] = Field(
            None, description="", alias="policyConditions"
        )
        access_control: Optional[AccessControl] = Field(
            None, description="", alias="accessControl"
        )  # relationship

        @classmethod
        # @validate_arguments()
        def create(cls, name: str) -> AuthPolicy.Attributes:
            if not name:
                raise ValueError("name cannot be blank")
            validate_required_fields(["name"], [name])
            return AuthPolicy.Attributes(
                qualified_name=name, name=name, display_name=""
            )

    attributes: "AuthPolicy.Attributes" = Field(
        default_factory=lambda: AuthPolicy.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ProcessExecution(Asset, type_name="ProcessExecution"):
    """Description"""

    type_name: str = Field("ProcessExecution", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ProcessExecution":
            raise ValueError("must be ProcessExecution")
        return v

    def __setattr__(self, name, value):
        if name in ProcessExecution._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


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
            qualified_name=self.qualified_name,
            name=self.name,
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

    type_name: str = Field("AtlasGlossaryTerm", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlasGlossaryTerm":
            raise ValueError("must be AtlasGlossaryTerm")
        return v

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
        "translation_terms",
        "valid_values_for",
        "synonyms",
        "replaced_by",
        "valid_values",
        "replacement_terms",
        "see_also",
        "translated_terms",
        "is_a",
        "anchor",
        "antonyms",
        "assigned_entities",
        "classifies",
        "categories",
        "preferred_to_terms",
        "preferred_terms",
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
    def translation_terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.translation_terms

    @translation_terms.setter
    def translation_terms(self, translation_terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.translation_terms = translation_terms

    @property
    def valid_values_for(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.valid_values_for

    @valid_values_for.setter
    def valid_values_for(self, valid_values_for: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.valid_values_for = valid_values_for

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
    def valid_values(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.valid_values

    @valid_values.setter
    def valid_values(self, valid_values: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.valid_values = valid_values

    @property
    def replacement_terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.replacement_terms

    @replacement_terms.setter
    def replacement_terms(self, replacement_terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.replacement_terms = replacement_terms

    @property
    def see_also(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.see_also

    @see_also.setter
    def see_also(self, see_also: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.see_also = see_also

    @property
    def translated_terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.translated_terms

    @translated_terms.setter
    def translated_terms(self, translated_terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.translated_terms = translated_terms

    @property
    def is_a(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.is_a

    @is_a.setter
    def is_a(self, is_a: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_a = is_a

    @property
    def anchor(self) -> AtlasGlossary:
        return None if self.attributes is None else self.attributes.anchor

    @anchor.setter
    def anchor(self, anchor: AtlasGlossary):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anchor = anchor

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
        valid_values: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="validValues"
        )  # relationship
        replacement_terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="replacementTerms"
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


class AuthService(Asset, type_name="AuthService"):
    """Description"""

    type_name: str = Field("AuthService", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AuthService":
            raise ValueError("must be AuthService")
        return v

    def __setattr__(self, name, value):
        if name in AuthService._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "auth_service_type",
        "tag_service",
        "auth_service_is_enabled",
        "auth_service_config",
        "auth_service_policy_last_sync",
    ]

    @property
    def auth_service_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.auth_service_type

    @auth_service_type.setter
    def auth_service_type(self, auth_service_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.auth_service_type = auth_service_type

    @property
    def tag_service(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.tag_service

    @tag_service.setter
    def tag_service(self, tag_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tag_service = tag_service

    @property
    def auth_service_is_enabled(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.auth_service_is_enabled
        )

    @auth_service_is_enabled.setter
    def auth_service_is_enabled(self, auth_service_is_enabled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.auth_service_is_enabled = auth_service_is_enabled

    @property
    def auth_service_config(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.auth_service_config

    @auth_service_config.setter
    def auth_service_config(self, auth_service_config: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.auth_service_config = auth_service_config

    @property
    def auth_service_policy_last_sync(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.auth_service_policy_last_sync
        )

    @auth_service_policy_last_sync.setter
    def auth_service_policy_last_sync(
        self, auth_service_policy_last_sync: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.auth_service_policy_last_sync = auth_service_policy_last_sync

    class Attributes(Asset.Attributes):
        auth_service_type: Optional[str] = Field(
            None, description="", alias="authServiceType"
        )
        tag_service: Optional[str] = Field(None, description="", alias="tagService")
        auth_service_is_enabled: Optional[bool] = Field(
            None, description="", alias="authServiceIsEnabled"
        )
        auth_service_config: Optional[dict[str, str]] = Field(
            None, description="", alias="authServiceConfig"
        )
        auth_service_policy_last_sync: Optional[int] = Field(
            None, description="", alias="authServicePolicyLastSync"
        )

    attributes: "AuthService.Attributes" = Field(
        default_factory=lambda: AuthService.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Cloud(Asset, type_name="Cloud"):
    """Description"""

    type_name: str = Field("Cloud", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Cloud":
            raise ValueError("must be Cloud")
        return v

    def __setattr__(self, name, value):
        if name in Cloud._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


class Infrastructure(Asset, type_name="Infrastructure"):
    """Description"""

    type_name: str = Field("Infrastructure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Infrastructure":
            raise ValueError("must be Infrastructure")
        return v

    def __setattr__(self, name, value):
        if name in Infrastructure._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


class BIProcess(Process):
    """Description"""

    type_name: str = Field("BIProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "BIProcess":
            raise ValueError("must be BIProcess")
        return v

    def __setattr__(self, name, value):
        if name in BIProcess._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "outputs",
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
        inputs: Optional[list[Catalog]] = Field(
            None, description="", alias="inputs"
        )  # relationship

    attributes: "BIProcess.Attributes" = Field(
        default_factory=lambda: BIProcess.Attributes(),
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
        if name in ColumnProcess._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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


class Persona(AccessControl):
    """Description"""

    @classmethod
    # @validate_arguments()
    def create(cls, *, name: str) -> Persona:
        validate_required_fields(["name"], [name])
        attributes = Persona.Attributes.create(name=name)
        return cls(attributes=attributes)

    @classmethod
    # @validate_arguments()
    def create_metadata_policy(
        cls,
        *,
        name: str,
        persona_id: str,
        policy_type: AuthPolicyType,
        actions: Set[PersonaMetadataAction],
        connection_qualified_name: str,
        resources: Set[str],
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "persona_id", "policy_type", "actions", "resources"],
            [name, persona_id, policy_type, actions, resources],
        )
        policy = AuthPolicy.create(name=name)
        policy.policy_actions = {x.value for x in actions}
        policy.policy_category = AuthPolicyCategory.PERSONA.value
        policy.policy_type = policy_type
        policy.connection_qualified_name = connection_qualified_name
        policy.policy_resources = resources
        policy.policy_resource_category = AuthPolicyResourceCategory.CUSTOM.value
        policy.policy_service_name = "atlas"
        policy.policy_sub_category = "metadata"
        persona = Persona()
        persona.guid = persona_id
        policy.access_control = persona
        return policy

    @classmethod
    # @validate_arguments()
    def create_data_policy(
        cls,
        *,
        name: str,
        persona_id: str,
        policy_type: AuthPolicyType,
        connection_qualified_name: str,
        resources: Set[str],
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "persona_id", "policy_type", "resources"],
            [name, persona_id, policy_type, resources],
        )
        policy = AuthPolicy.create(name=name)
        policy.policy_actions = {DataAction.SELECT.value}
        policy.policy_category = AuthPolicyCategory.PERSONA.value
        policy.policy_type = policy_type
        policy.connection_qualified_name = connection_qualified_name
        policy.policy_resources = resources
        policy.policy_resources.add("entity-type:*")
        policy.policy_resource_category = AuthPolicyResourceCategory.ENTITY.value
        policy.policy_service_name = "heka"
        policy.policy_sub_category = "data"
        persona = Persona()
        persona.guid = persona_id
        policy.access_control = persona
        return policy

    @classmethod
    # @validate_arguments()
    def create_glossary_policy(
        cls,
        *,
        name: str,
        persona_id: str,
        policy_type: AuthPolicyType,
        actions: Set[PersonaGlossaryAction],
        resources: Set[str],
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "persona_id", "policy_type", "actions", "resources"],
            [name, persona_id, policy_type, actions, resources],
        )
        policy = AuthPolicy.create(name=name)
        policy.policy_actions = {x.value for x in actions}
        policy.policy_category = AuthPolicyCategory.PERSONA.value
        policy.policy_type = policy_type
        policy.policy_resources = resources
        policy.policy_resource_category = AuthPolicyResourceCategory.CUSTOM.value
        policy.policy_service_name = "atlas"
        policy.policy_sub_category = "glossary"
        persona = Persona()
        persona.guid = persona_id
        policy.access_control = persona
        return policy

    @classmethod
    def create_for_modification(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = "",
        is_enabled: bool = True,
    ) -> SelfAsset:
        validate_required_fields(
            ["name", "qualified_name", "is_enabled"],
            [name, qualified_name, is_enabled],
        )
        return cls(
            attributes=cls.Attributes(
                qualified_name=qualified_name,
                name=name,
                is_access_control_enabled=is_enabled,
            )
        )

    type_name: str = Field("Persona", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Persona":
            raise ValueError("must be Persona")
        return v

    def __setattr__(self, name, value):
        if name in Persona._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "persona_groups",
        "persona_users",
        "role_id",
    ]

    @property
    def persona_groups(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.persona_groups

    @persona_groups.setter
    def persona_groups(self, persona_groups: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.persona_groups = persona_groups

    @property
    def persona_users(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.persona_users

    @persona_users.setter
    def persona_users(self, persona_users: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.persona_users = persona_users

    @property
    def role_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.role_id

    @role_id.setter
    def role_id(self, role_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.role_id = role_id

    class Attributes(AccessControl.Attributes):
        persona_groups: Optional[set[str]] = Field(
            None, description="", alias="personaGroups"
        )
        persona_users: Optional[set[str]] = Field(
            None, description="", alias="personaUsers"
        )
        role_id: Optional[str] = Field(None, description="", alias="roleId")

        @classmethod
        # @validate_arguments()
        def create(cls, name: str) -> Persona.Attributes:
            if not name:
                raise ValueError("name cannot be blank")
            validate_required_fields(["name"], [name])
            return Persona.Attributes(
                qualified_name=name,
                name=name,
                display_name=name,
                is_access_control_enabled=True,
                description="",
            )

    attributes: "Persona.Attributes" = Field(
        default_factory=lambda: Persona.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Purpose(AccessControl):
    """Description"""

    @classmethod
    # @validate_arguments()
    def create(cls, *, name: str, classifications: list[str]) -> Purpose:
        validate_required_fields(["name", "classifications"], [name, classifications])
        attributes = Purpose.Attributes.create(
            name=name, classifications=classifications
        )
        return cls(attributes=attributes)

    @classmethod
    # @validate_arguments()
    def create_metadata_policy(
        cls,
        *,
        name: str,
        purpose_id: str,
        policy_type: AuthPolicyType,
        actions: Set[PurposeMetadataAction],
        policy_groups: Optional[Set[str]] = None,
        policy_users: Optional[Set[str]] = None,
        all_users: bool = False,
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "purpose_id", "policy_type", "actions"],
            [name, purpose_id, policy_type, actions],
        )
        target_found = False
        policy = AuthPolicy.create(name=name)
        policy.policy_actions = {x.value for x in actions}
        policy.policy_category = AuthPolicyCategory.PURPOSE.value
        policy.policy_type = policy_type
        policy.policy_resource_category = AuthPolicyResourceCategory.TAG.value
        policy.policy_service_name = "atlas_tag"
        policy.policy_sub_category = "metadata"
        purpose = Purpose()
        purpose.guid = purpose_id
        policy.access_control = purpose
        if all_users:
            target_found = True
            policy.policy_groups = {"public"}
        else:
            if policy_groups:
                from pyatlan.cache.group_cache import GroupCache

                for group_alias in policy_groups:
                    if not GroupCache.get_id_for_alias(group_alias):
                        raise ValueError(
                            f"Provided group name {group_alias} was not found in Atlan."
                        )
                target_found = True
                policy.policy_groups = policy_groups
            else:
                policy.policy_groups = None
            if policy_users:
                from pyatlan.cache.user_cache import UserCache

                for username in policy_users:
                    if not UserCache.get_id_for_name(username):
                        raise ValueError(
                            f"Provided username {username} was not found in Atlan."
                        )
                target_found = True
                policy.policy_users = policy_users
            else:
                policy.policy_users = None
        if target_found:
            return policy
        else:
            raise ValueError("No user or group specified for the policy.")

    @classmethod
    # @validate_arguments()
    def create_data_policy(
        cls,
        *,
        name: str,
        purpose_id: str,
        policy_type: AuthPolicyType,
        policy_groups: Optional[Set[str]] = None,
        policy_users: Optional[Set[str]] = None,
        all_users: bool = False,
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "purpose_id", "policy_type"], [name, purpose_id, policy_type]
        )
        policy = AuthPolicy.create(name=name)
        policy.policy_actions = {DataAction.SELECT.value}
        policy.policy_category = AuthPolicyCategory.PURPOSE.value
        policy.policy_type = policy_type
        policy.policy_resource_category = AuthPolicyResourceCategory.TAG.value
        policy.policy_service_name = "atlas_tag"
        policy.policy_sub_category = "data"
        purpose = Purpose()
        purpose.guid = purpose_id
        policy.access_control = purpose
        if all_users:
            target_found = True
            policy.policy_groups = {"public"}
        else:
            if policy_groups:
                from pyatlan.cache.group_cache import GroupCache

                for group_alias in policy_groups:
                    if not GroupCache.get_id_for_alias(group_alias):
                        raise ValueError(
                            f"Provided group name {group_alias} was not found in Atlan."
                        )
                target_found = True
                policy.policy_groups = policy_groups
            else:
                policy.policy_groups = None
            if policy_users:
                from pyatlan.cache.user_cache import UserCache

                for username in policy_users:
                    if not UserCache.get_id_for_name(username):
                        raise ValueError(
                            f"Provided username {username} was not found in Atlan."
                        )
                target_found = True
                policy.policy_users = policy_users
            else:
                policy.policy_users = None
        if target_found:
            return policy
        else:
            raise ValueError("No user or group specified for the policy.")

    @classmethod
    def create_for_modification(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = "",
        is_enabled: bool = True,
    ) -> SelfAsset:
        validate_required_fields(
            ["name", "qualified_name", "is_enabled"],
            [name, qualified_name, is_enabled],
        )
        return cls(
            attributes=cls.Attributes(
                qualified_name=qualified_name,
                name=name,
                is_access_control_enabled=is_enabled,
            )
        )

    type_name: str = Field("Purpose", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Purpose":
            raise ValueError("must be Purpose")
        return v

    def __setattr__(self, name, value):
        if name in Purpose._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "purpose_classifications",
    ]

    @property
    def purpose_classifications(self) -> Optional[set[str]]:
        return (
            None if self.attributes is None else self.attributes.purpose_classifications
        )

    @purpose_classifications.setter
    def purpose_classifications(self, purpose_classifications: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.purpose_classifications = purpose_classifications

    class Attributes(AccessControl.Attributes):
        purpose_classifications: Optional[set[str]] = Field(
            None, description="", alias="purposeClassifications"
        )

        @classmethod
        # @validate_arguments()
        def create(cls, name: str, classifications: list[str]) -> Purpose.Attributes:
            validate_required_fields(
                ["name", "classifications"], [name, classifications]
            )
            return Purpose.Attributes(
                qualified_name=name,
                name=name,
                display_name=name,
                is_access_control_enabled=True,
                description="",
                purpose_classifications=classifications,
            )

    attributes: "Purpose.Attributes" = Field(
        default_factory=lambda: Purpose.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Collection(Namespace):
    """Description"""

    type_name: str = Field("Collection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Collection":
            raise ValueError("must be Collection")
        return v

    def __setattr__(self, name, value):
        if name in Collection._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "icon",
        "icon_type",
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

    class Attributes(Namespace.Attributes):
        icon: Optional[str] = Field(None, description="", alias="icon")
        icon_type: Optional[IconType] = Field(None, description="", alias="iconType")

    attributes: "Collection.Attributes" = Field(
        default_factory=lambda: Collection.Attributes(),
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
        if name in Folder._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "parent_qualified_name",
        "collection_qualified_name",
        "parent",
    ]

    @property
    def parent_qualified_name(self) -> str:
        return (
            None if self.attributes is None else self.attributes.parent_qualified_name
        )

    @parent_qualified_name.setter
    def parent_qualified_name(self, parent_qualified_name: str):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_qualified_name = parent_qualified_name

    @property
    def collection_qualified_name(self) -> str:
        return (
            None
            if self.attributes is None
            else self.attributes.collection_qualified_name
        )

    @collection_qualified_name.setter
    def collection_qualified_name(self, collection_qualified_name: str):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.collection_qualified_name = collection_qualified_name

    @property
    def parent(self) -> Namespace:
        return None if self.attributes is None else self.attributes.parent

    @parent.setter
    def parent(self, parent: Namespace):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent = parent

    class Attributes(Namespace.Attributes):
        parent_qualified_name: str = Field(
            None, description="", alias="parentQualifiedName"
        )
        collection_qualified_name: str = Field(
            None, description="", alias="collectionQualifiedName"
        )
        parent: Namespace = Field(None, description="", alias="parent")  # relationship

    attributes: "Folder.Attributes" = Field(
        default_factory=lambda: Folder.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class EventStore(Catalog):
    """Description"""

    type_name: str = Field("EventStore", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "EventStore":
            raise ValueError("must be EventStore")
        return v

    def __setattr__(self, name, value):
        if name in EventStore._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


class ObjectStore(Catalog):
    """Description"""

    type_name: str = Field("ObjectStore", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ObjectStore":
            raise ValueError("must be ObjectStore")
        return v

    def __setattr__(self, name, value):
        if name in ObjectStore._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


class DataQuality(Catalog):
    """Description"""

    type_name: str = Field("DataQuality", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataQuality":
            raise ValueError("must be DataQuality")
        return v

    def __setattr__(self, name, value):
        if name in DataQuality._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


class BI(Catalog):
    """Description"""

    type_name: str = Field("BI", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "BI":
            raise ValueError("must be BI")
        return v

    def __setattr__(self, name, value):
        if name in BI._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


class SaaS(Catalog):
    """Description"""

    type_name: str = Field("SaaS", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SaaS":
            raise ValueError("must be SaaS")
        return v

    def __setattr__(self, name, value):
        if name in SaaS._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


class Dbt(Catalog):
    """Description"""

    type_name: str = Field("Dbt", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Dbt":
            raise ValueError("must be Dbt")
        return v

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


class Resource(Catalog):
    """Description"""

    type_name: str = Field("Resource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Resource":
            raise ValueError("must be Resource")
        return v

    def __setattr__(self, name, value):
        if name in Resource._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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


class Insight(Catalog):
    """Description"""

    type_name: str = Field("Insight", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Insight":
            raise ValueError("must be Insight")
        return v

    def __setattr__(self, name, value):
        if name in Insight._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


class API(Catalog):
    """Description"""

    type_name: str = Field("API", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "API":
            raise ValueError("must be API")
        return v

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
    ]

    @property
    def api_spec_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_spec_type

    @api_spec_type.setter
    def api_spec_type(self, api_spec_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_type = api_spec_type

    @property
    def api_spec_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_spec_version

    @api_spec_version.setter
    def api_spec_version(self, api_spec_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_version = api_spec_version

    @property
    def api_spec_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_spec_name

    @api_spec_name.setter
    def api_spec_name(self, api_spec_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_name = api_spec_name

    @property
    def api_spec_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.api_spec_qualified_name
        )

    @api_spec_qualified_name.setter
    def api_spec_qualified_name(self, api_spec_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_qualified_name = api_spec_qualified_name

    @property
    def api_external_docs(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.api_external_docs

    @api_external_docs.setter
    def api_external_docs(self, api_external_docs: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_external_docs = api_external_docs

    @property
    def api_is_auth_optional(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.api_is_auth_optional

    @api_is_auth_optional.setter
    def api_is_auth_optional(self, api_is_auth_optional: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_is_auth_optional = api_is_auth_optional

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

    attributes: "API.Attributes" = Field(
        default_factory=lambda: API.Attributes(),
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
        if name in Tag._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "tag_id",
        "tag_attributes",
        "tag_allowed_values",
        "mapped_classification_name",
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
    def mapped_classification_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mapped_classification_name
        )

    @mapped_classification_name.setter
    def mapped_classification_name(self, mapped_classification_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mapped_classification_name = mapped_classification_name

    class Attributes(Catalog.Attributes):
        tag_id: Optional[str] = Field(None, description="", alias="tagId")
        tag_attributes: Optional[list[SourceTagAttribute]] = Field(
            None, description="", alias="tagAttributes"
        )
        tag_allowed_values: Optional[set[str]] = Field(
            None, description="", alias="tagAllowedValues"
        )
        mapped_classification_name: Optional[str] = Field(
            None, description="", alias="mappedClassificationName"
        )

    attributes: "Tag.Attributes" = Field(
        default_factory=lambda: Tag.Attributes(),
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
        "dbt_sources",
        "sql_dbt_models",
        "sql_dbt_sources",
        "dbt_models",
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

    attributes: "SQL.Attributes" = Field(
        default_factory=lambda: SQL.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Google(Cloud):
    """Description"""

    type_name: str = Field("Google", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Google":
            raise ValueError("must be Google")
        return v

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
    ]

    @property
    def google_service(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_service

    @google_service.setter
    def google_service(self, google_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_service = google_service

    @property
    def google_project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_project_name

    @google_project_name.setter
    def google_project_name(self, google_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_name = google_project_name

    @property
    def google_project_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_project_id

    @google_project_id.setter
    def google_project_id(self, google_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_id = google_project_id

    @property
    def google_project_number(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.google_project_number
        )

    @google_project_number.setter
    def google_project_number(self, google_project_number: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_number = google_project_number

    @property
    def google_location(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_location

    @google_location.setter
    def google_location(self, google_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location = google_location

    @property
    def google_location_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_location_type

    @google_location_type.setter
    def google_location_type(self, google_location_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location_type = google_location_type

    @property
    def google_labels(self) -> Optional[list[GoogleLabel]]:
        return None if self.attributes is None else self.attributes.google_labels

    @google_labels.setter
    def google_labels(self, google_labels: Optional[list[GoogleLabel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_labels = google_labels

    @property
    def google_tags(self) -> Optional[list[GoogleTag]]:
        return None if self.attributes is None else self.attributes.google_tags

    @google_tags.setter
    def google_tags(self, google_tags: Optional[list[GoogleTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_tags = google_tags

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

    attributes: "Google.Attributes" = Field(
        default_factory=lambda: Google.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Azure(Cloud):
    """Description"""

    type_name: str = Field("Azure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Azure":
            raise ValueError("must be Azure")
        return v

    def __setattr__(self, name, value):
        if name in Azure._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "azure_resource_id",
        "azure_location",
        "adls_account_secondary_location",
        "azure_tags",
    ]

    @property
    def azure_resource_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.azure_resource_id

    @azure_resource_id.setter
    def azure_resource_id(self, azure_resource_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_resource_id = azure_resource_id

    @property
    def azure_location(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.azure_location

    @azure_location.setter
    def azure_location(self, azure_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_location = azure_location

    @property
    def adls_account_secondary_location(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_secondary_location
        )

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
        return None if self.attributes is None else self.attributes.azure_tags

    @azure_tags.setter
    def azure_tags(self, azure_tags: Optional[list[AzureTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_tags = azure_tags

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

    attributes: "Azure.Attributes" = Field(
        default_factory=lambda: Azure.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AWS(Cloud):
    """Description"""

    type_name: str = Field("AWS", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AWS":
            raise ValueError("must be AWS")
        return v

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
    ]

    @property
    def aws_arn(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_arn

    @aws_arn.setter
    def aws_arn(self, aws_arn: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_arn = aws_arn

    @property
    def aws_partition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_partition

    @aws_partition.setter
    def aws_partition(self, aws_partition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_partition = aws_partition

    @property
    def aws_service(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_service

    @aws_service.setter
    def aws_service(self, aws_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_service = aws_service

    @property
    def aws_region(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_region

    @aws_region.setter
    def aws_region(self, aws_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_region = aws_region

    @property
    def aws_account_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_account_id

    @aws_account_id.setter
    def aws_account_id(self, aws_account_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_account_id = aws_account_id

    @property
    def aws_resource_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_resource_id

    @aws_resource_id.setter
    def aws_resource_id(self, aws_resource_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_resource_id = aws_resource_id

    @property
    def aws_owner_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_owner_name

    @aws_owner_name.setter
    def aws_owner_name(self, aws_owner_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_owner_name = aws_owner_name

    @property
    def aws_owner_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_owner_id

    @aws_owner_id.setter
    def aws_owner_id(self, aws_owner_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_owner_id = aws_owner_id

    @property
    def aws_tags(self) -> Optional[list[AwsTag]]:
        return None if self.attributes is None else self.attributes.aws_tags

    @aws_tags.setter
    def aws_tags(self, aws_tags: Optional[list[AwsTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_tags = aws_tags

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

    attributes: "AWS.Attributes" = Field(
        default_factory=lambda: AWS.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtColumnProcess(Dbt):
    """Description"""

    type_name: str = Field("DbtColumnProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtColumnProcess":
            raise ValueError("must be DbtColumnProcess")
        return v

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
        "process",
        "column_processes",
    ]

    @property
    def dbt_column_process_job_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_column_process_job_status
        )

    @dbt_column_process_job_status.setter
    def dbt_column_process_job_status(
        self, dbt_column_process_job_status: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_column_process_job_status = dbt_column_process_job_status

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
    def process(self) -> Optional[Process]:
        return None if self.attributes is None else self.attributes.process

    @process.setter
    def process(self, process: Optional[Process]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.process = process

    @property
    def column_processes(self) -> Optional[list[ColumnProcess]]:
        return None if self.attributes is None else self.attributes.column_processes

    @column_processes.setter
    def column_processes(self, column_processes: Optional[list[ColumnProcess]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_processes = column_processes

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
        process: Optional[Process] = Field(
            None, description="", alias="process"
        )  # relationship
        column_processes: Optional[list[ColumnProcess]] = Field(
            None, description="", alias="columnProcesses"
        )  # relationship

    attributes: "DbtColumnProcess.Attributes" = Field(
        default_factory=lambda: DbtColumnProcess.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Kafka(EventStore):
    """Description"""

    type_name: str = Field("Kafka", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Kafka":
            raise ValueError("must be Kafka")
        return v

    def __setattr__(self, name, value):
        if name in Kafka._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


class S3(ObjectStore):
    """Description"""

    type_name: str = Field("S3", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "S3":
            raise ValueError("must be S3")
        return v

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
    ]

    @property
    def s3_e_tag(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.s3_e_tag

    @s3_e_tag.setter
    def s3_e_tag(self, s3_e_tag: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_e_tag = s3_e_tag

    @property
    def s3_encryption(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.s3_encryption

    @s3_encryption.setter
    def s3_encryption(self, s3_encryption: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_encryption = s3_encryption

    @property
    def aws_arn(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_arn

    @aws_arn.setter
    def aws_arn(self, aws_arn: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_arn = aws_arn

    @property
    def aws_partition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_partition

    @aws_partition.setter
    def aws_partition(self, aws_partition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_partition = aws_partition

    @property
    def aws_service(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_service

    @aws_service.setter
    def aws_service(self, aws_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_service = aws_service

    @property
    def aws_region(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_region

    @aws_region.setter
    def aws_region(self, aws_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_region = aws_region

    @property
    def aws_account_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_account_id

    @aws_account_id.setter
    def aws_account_id(self, aws_account_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_account_id = aws_account_id

    @property
    def aws_resource_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_resource_id

    @aws_resource_id.setter
    def aws_resource_id(self, aws_resource_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_resource_id = aws_resource_id

    @property
    def aws_owner_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_owner_name

    @aws_owner_name.setter
    def aws_owner_name(self, aws_owner_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_owner_name = aws_owner_name

    @property
    def aws_owner_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_owner_id

    @aws_owner_id.setter
    def aws_owner_id(self, aws_owner_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_owner_id = aws_owner_id

    @property
    def aws_tags(self) -> Optional[list[AwsTag]]:
        return None if self.attributes is None else self.attributes.aws_tags

    @aws_tags.setter
    def aws_tags(self, aws_tags: Optional[list[AwsTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_tags = aws_tags

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

    attributes: "S3.Attributes" = Field(
        default_factory=lambda: S3.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ADLS(ObjectStore):
    """Description"""

    type_name: str = Field("ADLS", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADLS":
            raise ValueError("must be ADLS")
        return v

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
    ]

    @property
    def adls_account_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_qualified_name
        )

    @adls_account_qualified_name.setter
    def adls_account_qualified_name(self, adls_account_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_qualified_name = adls_account_qualified_name

    @property
    def azure_resource_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.azure_resource_id

    @azure_resource_id.setter
    def azure_resource_id(self, azure_resource_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_resource_id = azure_resource_id

    @property
    def azure_location(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.azure_location

    @azure_location.setter
    def azure_location(self, azure_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_location = azure_location

    @property
    def adls_account_secondary_location(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_secondary_location
        )

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
        return None if self.attributes is None else self.attributes.azure_tags

    @azure_tags.setter
    def azure_tags(self, azure_tags: Optional[list[AzureTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_tags = azure_tags

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

    attributes: "ADLS.Attributes" = Field(
        default_factory=lambda: ADLS.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class GCS(Google):
    """Description"""

    type_name: str = Field("GCS", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "GCS":
            raise ValueError("must be GCS")
        return v

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
        "input_to_processes",
        "output_from_processes",
    ]

    @property
    def gcs_storage_class(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_storage_class

    @gcs_storage_class.setter
    def gcs_storage_class(self, gcs_storage_class: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_storage_class = gcs_storage_class

    @property
    def gcs_encryption_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_encryption_type

    @gcs_encryption_type.setter
    def gcs_encryption_type(self, gcs_encryption_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_encryption_type = gcs_encryption_type

    @property
    def gcs_e_tag(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_e_tag

    @gcs_e_tag.setter
    def gcs_e_tag(self, gcs_e_tag: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_e_tag = gcs_e_tag

    @property
    def gcs_requester_pays(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.gcs_requester_pays

    @gcs_requester_pays.setter
    def gcs_requester_pays(self, gcs_requester_pays: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_requester_pays = gcs_requester_pays

    @property
    def gcs_access_control(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_access_control

    @gcs_access_control.setter
    def gcs_access_control(self, gcs_access_control: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_access_control = gcs_access_control

    @property
    def gcs_meta_generation_id(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.gcs_meta_generation_id
        )

    @gcs_meta_generation_id.setter
    def gcs_meta_generation_id(self, gcs_meta_generation_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_meta_generation_id = gcs_meta_generation_id

    @property
    def google_service(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_service

    @google_service.setter
    def google_service(self, google_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_service = google_service

    @property
    def google_project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_project_name

    @google_project_name.setter
    def google_project_name(self, google_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_name = google_project_name

    @property
    def google_project_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_project_id

    @google_project_id.setter
    def google_project_id(self, google_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_id = google_project_id

    @property
    def google_project_number(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.google_project_number
        )

    @google_project_number.setter
    def google_project_number(self, google_project_number: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_number = google_project_number

    @property
    def google_location(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_location

    @google_location.setter
    def google_location(self, google_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location = google_location

    @property
    def google_location_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_location_type

    @google_location_type.setter
    def google_location_type(self, google_location_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location_type = google_location_type

    @property
    def google_labels(self) -> Optional[list[GoogleLabel]]:
        return None if self.attributes is None else self.attributes.google_labels

    @google_labels.setter
    def google_labels(self, google_labels: Optional[list[GoogleLabel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_labels = google_labels

    @property
    def google_tags(self) -> Optional[list[GoogleTag]]:
        return None if self.attributes is None else self.attributes.google_tags

    @google_tags.setter
    def google_tags(self, google_tags: Optional[list[GoogleTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_tags = google_tags

    @property
    def input_to_processes(self) -> Optional[list[Process]]:
        return None if self.attributes is None else self.attributes.input_to_processes

    @input_to_processes.setter
    def input_to_processes(self, input_to_processes: Optional[list[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_processes = input_to_processes

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
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "GCS.Attributes" = Field(
        default_factory=lambda: GCS.Attributes(),
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
        if name in MonteCarlo._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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


class Metric(DataQuality):
    """Description"""

    type_name: str = Field("Metric", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Metric":
            raise ValueError("must be Metric")
        return v

    def __setattr__(self, name, value):
        if name in Metric._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "metric_type",
        "metric_s_q_l",
        "metric_filters",
        "metric_time_grains",
        "assets",
        "metric_dimension_columns",
        "metric_timestamp_column",
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
    def metric_timestamp_column(self) -> Optional[Column]:
        return (
            None if self.attributes is None else self.attributes.metric_timestamp_column
        )

    @metric_timestamp_column.setter
    def metric_timestamp_column(self, metric_timestamp_column: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_timestamp_column = metric_timestamp_column

    class Attributes(DataQuality.Attributes):
        metric_type: Optional[str] = Field(None, description="", alias="metricType")
        metric_s_q_l: Optional[str] = Field(None, description="", alias="metricSQL")
        metric_filters: Optional[str] = Field(
            None, description="", alias="metricFilters"
        )
        metric_time_grains: Optional[set[str]] = Field(
            None, description="", alias="metricTimeGrains"
        )
        assets: Optional[list[Asset]] = Field(
            None, description="", alias="assets"
        )  # relationship
        metric_dimension_columns: Optional[list[Column]] = Field(
            None, description="", alias="metricDimensionColumns"
        )  # relationship
        metric_timestamp_column: Optional[Column] = Field(
            None, description="", alias="metricTimestampColumn"
        )  # relationship

    attributes: "Metric.Attributes" = Field(
        default_factory=lambda: Metric.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Preset(BI):
    """Description"""

    type_name: str = Field("Preset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Preset":
            raise ValueError("must be Preset")
        return v

    def __setattr__(self, name, value):
        if name in Preset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "preset_workspace_id",
        "preset_workspace_qualified_name",
        "preset_dashboard_id",
        "preset_dashboard_qualified_name",
    ]

    @property
    def preset_workspace_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.preset_workspace_id

    @preset_workspace_id.setter
    def preset_workspace_id(self, preset_workspace_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_id = preset_workspace_id

    @property
    def preset_workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_qualified_name
        )

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
        return None if self.attributes is None else self.attributes.preset_dashboard_id

    @preset_dashboard_id.setter
    def preset_dashboard_id(self, preset_dashboard_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_id = preset_dashboard_id

    @property
    def preset_dashboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_qualified_name
        )

    @preset_dashboard_qualified_name.setter
    def preset_dashboard_qualified_name(
        self, preset_dashboard_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_qualified_name = (
            preset_dashboard_qualified_name
        )

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

    attributes: "Preset.Attributes" = Field(
        default_factory=lambda: Preset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Mode(BI):
    """Description"""

    type_name: str = Field("Mode", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Mode":
            raise ValueError("must be Mode")
        return v

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
    ]

    @property
    def mode_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_id

    @mode_id.setter
    def mode_id(self, mode_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_id = mode_id

    @property
    def mode_token(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_token

    @mode_token.setter
    def mode_token(self, mode_token: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_token = mode_token

    @property
    def mode_workspace_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_workspace_name

    @mode_workspace_name.setter
    def mode_workspace_name(self, mode_workspace_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_workspace_name = mode_workspace_name

    @property
    def mode_workspace_username(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.mode_workspace_username
        )

    @mode_workspace_username.setter
    def mode_workspace_username(self, mode_workspace_username: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_workspace_username = mode_workspace_username

    @property
    def mode_workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mode_workspace_qualified_name
        )

    @mode_workspace_qualified_name.setter
    def mode_workspace_qualified_name(
        self, mode_workspace_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_workspace_qualified_name = mode_workspace_qualified_name

    @property
    def mode_report_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_report_name

    @mode_report_name.setter
    def mode_report_name(self, mode_report_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report_name = mode_report_name

    @property
    def mode_report_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mode_report_qualified_name
        )

    @mode_report_qualified_name.setter
    def mode_report_qualified_name(self, mode_report_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report_qualified_name = mode_report_qualified_name

    @property
    def mode_query_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_query_name

    @mode_query_name.setter
    def mode_query_name(self, mode_query_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_name = mode_query_name

    @property
    def mode_query_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mode_query_qualified_name
        )

    @mode_query_qualified_name.setter
    def mode_query_qualified_name(self, mode_query_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_qualified_name = mode_query_qualified_name

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

    attributes: "Mode.Attributes" = Field(
        default_factory=lambda: Mode.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Sigma(BI):
    """Description"""

    type_name: str = Field("Sigma", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Sigma":
            raise ValueError("must be Sigma")
        return v

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
    ]

    @property
    def sigma_workbook_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_workbook_qualified_name
        )

    @sigma_workbook_qualified_name.setter
    def sigma_workbook_qualified_name(
        self, sigma_workbook_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_workbook_qualified_name = sigma_workbook_qualified_name

    @property
    def sigma_workbook_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sigma_workbook_name

    @sigma_workbook_name.setter
    def sigma_workbook_name(self, sigma_workbook_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_workbook_name = sigma_workbook_name

    @property
    def sigma_page_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_page_qualified_name
        )

    @sigma_page_qualified_name.setter
    def sigma_page_qualified_name(self, sigma_page_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_page_qualified_name = sigma_page_qualified_name

    @property
    def sigma_page_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sigma_page_name

    @sigma_page_name.setter
    def sigma_page_name(self, sigma_page_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_page_name = sigma_page_name

    @property
    def sigma_data_element_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_qualified_name
        )

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
        return (
            None if self.attributes is None else self.attributes.sigma_data_element_name
        )

    @sigma_data_element_name.setter
    def sigma_data_element_name(self, sigma_data_element_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_name = sigma_data_element_name

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

    attributes: "Sigma.Attributes" = Field(
        default_factory=lambda: Sigma.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Tableau(BI):
    """Description"""

    type_name: str = Field("Tableau", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Tableau":
            raise ValueError("must be Tableau")
        return v

    def __setattr__(self, name, value):
        if name in Tableau._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


class Looker(BI):
    """Description"""

    type_name: str = Field("Looker", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Looker":
            raise ValueError("must be Looker")
        return v

    def __setattr__(self, name, value):
        if name in Looker._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


class Redash(BI):
    """Description"""

    type_name: str = Field("Redash", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Redash":
            raise ValueError("must be Redash")
        return v

    def __setattr__(self, name, value):
        if name in Redash._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "redash_is_published",
    ]

    @property
    def redash_is_published(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.redash_is_published

    @redash_is_published.setter
    def redash_is_published(self, redash_is_published: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_is_published = redash_is_published

    class Attributes(BI.Attributes):
        redash_is_published: Optional[bool] = Field(
            None, description="", alias="redashIsPublished"
        )

    attributes: "Redash.Attributes" = Field(
        default_factory=lambda: Redash.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DataStudio(Google):
    """Description"""

    type_name: str = Field("DataStudio", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataStudio":
            raise ValueError("must be DataStudio")
        return v

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
        "input_to_processes",
        "output_from_processes",
    ]

    @property
    def google_service(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_service

    @google_service.setter
    def google_service(self, google_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_service = google_service

    @property
    def google_project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_project_name

    @google_project_name.setter
    def google_project_name(self, google_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_name = google_project_name

    @property
    def google_project_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_project_id

    @google_project_id.setter
    def google_project_id(self, google_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_id = google_project_id

    @property
    def google_project_number(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.google_project_number
        )

    @google_project_number.setter
    def google_project_number(self, google_project_number: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_number = google_project_number

    @property
    def google_location(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_location

    @google_location.setter
    def google_location(self, google_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location = google_location

    @property
    def google_location_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_location_type

    @google_location_type.setter
    def google_location_type(self, google_location_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location_type = google_location_type

    @property
    def google_labels(self) -> Optional[list[GoogleLabel]]:
        return None if self.attributes is None else self.attributes.google_labels

    @google_labels.setter
    def google_labels(self, google_labels: Optional[list[GoogleLabel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_labels = google_labels

    @property
    def google_tags(self) -> Optional[list[GoogleTag]]:
        return None if self.attributes is None else self.attributes.google_tags

    @google_tags.setter
    def google_tags(self, google_tags: Optional[list[GoogleTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_tags = google_tags

    @property
    def input_to_processes(self) -> Optional[list[Process]]:
        return None if self.attributes is None else self.attributes.input_to_processes

    @input_to_processes.setter
    def input_to_processes(self, input_to_processes: Optional[list[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_processes = input_to_processes

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
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "DataStudio.Attributes" = Field(
        default_factory=lambda: DataStudio.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Metabase(BI):
    """Description"""

    type_name: str = Field("Metabase", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Metabase":
            raise ValueError("must be Metabase")
        return v

    def __setattr__(self, name, value):
        if name in Metabase._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "metabase_collection_name",
        "metabase_collection_qualified_name",
    ]

    @property
    def metabase_collection_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.metabase_collection_name
        )

    @metabase_collection_name.setter
    def metabase_collection_name(self, metabase_collection_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_collection_name = metabase_collection_name

    @property
    def metabase_collection_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.metabase_collection_qualified_name
        )

    @metabase_collection_qualified_name.setter
    def metabase_collection_qualified_name(
        self, metabase_collection_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_collection_qualified_name = (
            metabase_collection_qualified_name
        )

    class Attributes(BI.Attributes):
        metabase_collection_name: Optional[str] = Field(
            None, description="", alias="metabaseCollectionName"
        )
        metabase_collection_qualified_name: Optional[str] = Field(
            None, description="", alias="metabaseCollectionQualifiedName"
        )

    attributes: "Metabase.Attributes" = Field(
        default_factory=lambda: Metabase.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSight(BI):
    """Description"""

    type_name: str = Field("QuickSight", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSight":
            raise ValueError("must be QuickSight")
        return v

    def __setattr__(self, name, value):
        if name in QuickSight._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_id",
        "quick_sight_sheet_id",
        "quick_sight_sheet_name",
    ]

    @property
    def quick_sight_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.quick_sight_id

    @quick_sight_id.setter
    def quick_sight_id(self, quick_sight_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_id = quick_sight_id

    @property
    def quick_sight_sheet_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.quick_sight_sheet_id

    @quick_sight_sheet_id.setter
    def quick_sight_sheet_id(self, quick_sight_sheet_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_sheet_id = quick_sight_sheet_id

    @property
    def quick_sight_sheet_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.quick_sight_sheet_name
        )

    @quick_sight_sheet_name.setter
    def quick_sight_sheet_name(self, quick_sight_sheet_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_sheet_name = quick_sight_sheet_name

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

    attributes: "QuickSight.Attributes" = Field(
        default_factory=lambda: QuickSight.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Thoughtspot(BI):
    """Description"""

    type_name: str = Field("Thoughtspot", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Thoughtspot":
            raise ValueError("must be Thoughtspot")
        return v

    def __setattr__(self, name, value):
        if name in Thoughtspot._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "thoughtspot_chart_type",
        "thoughtspot_question_text",
    ]

    @property
    def thoughtspot_chart_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.thoughtspot_chart_type
        )

    @thoughtspot_chart_type.setter
    def thoughtspot_chart_type(self, thoughtspot_chart_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_chart_type = thoughtspot_chart_type

    @property
    def thoughtspot_question_text(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.thoughtspot_question_text
        )

    @thoughtspot_question_text.setter
    def thoughtspot_question_text(self, thoughtspot_question_text: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_question_text = thoughtspot_question_text

    class Attributes(BI.Attributes):
        thoughtspot_chart_type: Optional[str] = Field(
            None, description="", alias="thoughtspotChartType"
        )
        thoughtspot_question_text: Optional[str] = Field(
            None, description="", alias="thoughtspotQuestionText"
        )

    attributes: "Thoughtspot.Attributes" = Field(
        default_factory=lambda: Thoughtspot.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBI(BI):
    """Description"""

    type_name: str = Field("PowerBI", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBI":
            raise ValueError("must be PowerBI")
        return v

    def __setattr__(self, name, value):
        if name in PowerBI._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "power_b_i_is_hidden",
        "power_b_i_table_qualified_name",
        "power_b_i_format_string",
        "power_b_i_endorsement",
    ]

    @property
    def power_b_i_is_hidden(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.power_b_i_is_hidden

    @power_b_i_is_hidden.setter
    def power_b_i_is_hidden(self, power_b_i_is_hidden: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_is_hidden = power_b_i_is_hidden

    @property
    def power_b_i_table_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_table_qualified_name
        )

    @power_b_i_table_qualified_name.setter
    def power_b_i_table_qualified_name(
        self, power_b_i_table_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_table_qualified_name = power_b_i_table_qualified_name

    @property
    def power_b_i_format_string(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.power_b_i_format_string
        )

    @power_b_i_format_string.setter
    def power_b_i_format_string(self, power_b_i_format_string: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_format_string = power_b_i_format_string

    @property
    def power_b_i_endorsement(self) -> Optional[PowerbiEndorsement]:
        return (
            None if self.attributes is None else self.attributes.power_b_i_endorsement
        )

    @power_b_i_endorsement.setter
    def power_b_i_endorsement(
        self, power_b_i_endorsement: Optional[PowerbiEndorsement]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_endorsement = power_b_i_endorsement

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

    attributes: "PowerBI.Attributes" = Field(
        default_factory=lambda: PowerBI.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategy(BI):
    """Description"""

    type_name: str = Field("MicroStrategy", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategy":
            raise ValueError("must be MicroStrategy")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategy._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "micro_strategy_project_qualified_name",
        "micro_strategy_project_name",
        "micro_strategy_cube_qualified_names",
        "micro_strategy_cube_names",
        "micro_strategy_report_qualified_names",
        "micro_strategy_report_names",
        "micro_strategy_is_certified",
        "micro_strategy_certified_by",
        "micro_strategy_certified_at",
        "micro_strategy_location",
    ]

    @property
    def micro_strategy_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_project_qualified_name
        )

    @micro_strategy_project_qualified_name.setter
    def micro_strategy_project_qualified_name(
        self, micro_strategy_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project_qualified_name = (
            micro_strategy_project_qualified_name
        )

    @property
    def micro_strategy_project_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_project_name
        )

    @micro_strategy_project_name.setter
    def micro_strategy_project_name(self, micro_strategy_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project_name = micro_strategy_project_name

    @property
    def micro_strategy_cube_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_cube_qualified_names
        )

    @micro_strategy_cube_qualified_names.setter
    def micro_strategy_cube_qualified_names(
        self, micro_strategy_cube_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cube_qualified_names = (
            micro_strategy_cube_qualified_names
        )

    @property
    def micro_strategy_cube_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_cube_names
        )

    @micro_strategy_cube_names.setter
    def micro_strategy_cube_names(self, micro_strategy_cube_names: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cube_names = micro_strategy_cube_names

    @property
    def micro_strategy_report_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_report_qualified_names
        )

    @micro_strategy_report_qualified_names.setter
    def micro_strategy_report_qualified_names(
        self, micro_strategy_report_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_report_qualified_names = (
            micro_strategy_report_qualified_names
        )

    @property
    def micro_strategy_report_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_report_names
        )

    @micro_strategy_report_names.setter
    def micro_strategy_report_names(
        self, micro_strategy_report_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_report_names = micro_strategy_report_names

    @property
    def micro_strategy_is_certified(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_is_certified
        )

    @micro_strategy_is_certified.setter
    def micro_strategy_is_certified(self, micro_strategy_is_certified: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_is_certified = micro_strategy_is_certified

    @property
    def micro_strategy_certified_by(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_certified_by
        )

    @micro_strategy_certified_by.setter
    def micro_strategy_certified_by(self, micro_strategy_certified_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_certified_by = micro_strategy_certified_by

    @property
    def micro_strategy_certified_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_certified_at
        )

    @micro_strategy_certified_at.setter
    def micro_strategy_certified_at(
        self, micro_strategy_certified_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_certified_at = micro_strategy_certified_at

    @property
    def micro_strategy_location(self) -> Optional[list[dict[str, str]]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_location
        )

    @micro_strategy_location.setter
    def micro_strategy_location(
        self, micro_strategy_location: Optional[list[dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_location = micro_strategy_location

    class Attributes(BI.Attributes):
        micro_strategy_project_qualified_name: Optional[str] = Field(
            None, description="", alias="microStrategyProjectQualifiedName"
        )
        micro_strategy_project_name: Optional[str] = Field(
            None, description="", alias="microStrategyProjectName"
        )
        micro_strategy_cube_qualified_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyCubeQualifiedNames"
        )
        micro_strategy_cube_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyCubeNames"
        )
        micro_strategy_report_qualified_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyReportQualifiedNames"
        )
        micro_strategy_report_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyReportNames"
        )
        micro_strategy_is_certified: Optional[bool] = Field(
            None, description="", alias="microStrategyIsCertified"
        )
        micro_strategy_certified_by: Optional[str] = Field(
            None, description="", alias="microStrategyCertifiedBy"
        )
        micro_strategy_certified_at: Optional[datetime] = Field(
            None, description="", alias="microStrategyCertifiedAt"
        )
        micro_strategy_location: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="microStrategyLocation"
        )

    attributes: "MicroStrategy.Attributes" = Field(
        default_factory=lambda: MicroStrategy.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Qlik(BI):
    """Description"""

    type_name: str = Field("Qlik", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Qlik":
            raise ValueError("must be Qlik")
        return v

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
    ]

    @property
    def qlik_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_id

    @qlik_id.setter
    def qlik_id(self, qlik_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_id = qlik_id

    @property
    def qlik_q_r_i(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_q_r_i

    @qlik_q_r_i.setter
    def qlik_q_r_i(self, qlik_q_r_i: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_q_r_i = qlik_q_r_i

    @property
    def qlik_space_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_space_id

    @qlik_space_id.setter
    def qlik_space_id(self, qlik_space_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space_id = qlik_space_id

    @property
    def qlik_space_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.qlik_space_qualified_name
        )

    @qlik_space_qualified_name.setter
    def qlik_space_qualified_name(self, qlik_space_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space_qualified_name = qlik_space_qualified_name

    @property
    def qlik_app_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_app_id

    @qlik_app_id.setter
    def qlik_app_id(self, qlik_app_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_app_id = qlik_app_id

    @property
    def qlik_app_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.qlik_app_qualified_name
        )

    @qlik_app_qualified_name.setter
    def qlik_app_qualified_name(self, qlik_app_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_app_qualified_name = qlik_app_qualified_name

    @property
    def qlik_owner_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_owner_id

    @qlik_owner_id.setter
    def qlik_owner_id(self, qlik_owner_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_owner_id = qlik_owner_id

    @property
    def qlik_is_published(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.qlik_is_published

    @qlik_is_published.setter
    def qlik_is_published(self, qlik_is_published: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_is_published = qlik_is_published

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

    attributes: "Qlik.Attributes" = Field(
        default_factory=lambda: Qlik.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Salesforce(SaaS):
    """Description"""

    type_name: str = Field("Salesforce", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Salesforce":
            raise ValueError("must be Salesforce")
        return v

    def __setattr__(self, name, value):
        if name in Salesforce._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "organization_qualified_name",
        "api_name",
    ]

    @property
    def organization_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.organization_qualified_name
        )

    @organization_qualified_name.setter
    def organization_qualified_name(self, organization_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.organization_qualified_name = organization_qualified_name

    @property
    def api_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_name

    @api_name.setter
    def api_name(self, api_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_name = api_name

    class Attributes(SaaS.Attributes):
        organization_qualified_name: Optional[str] = Field(
            None, description="", alias="organizationQualifiedName"
        )
        api_name: Optional[str] = Field(None, description="", alias="apiName")

    attributes: "Salesforce.Attributes" = Field(
        default_factory=lambda: Salesforce.Attributes(),
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
        if name in DbtModelColumn._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "dbt_model_qualified_name",
        "dbt_model_column_data_type",
        "dbt_model_column_order",
        "dbt_model_column_sql_columns",
        "sql_column",
        "dbt_model",
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
        sql_column: Optional[Column] = Field(
            None, description="", alias="sqlColumn"
        )  # relationship
        dbt_model: Optional[DbtModel] = Field(
            None, description="", alias="dbtModel"
        )  # relationship

    attributes: "DbtModelColumn.Attributes" = Field(
        default_factory=lambda: DbtModelColumn.Attributes(),
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
        "dbt_metrics",
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
        if name in DbtSource._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "dbt_state",
        "dbt_freshness_criteria",
        "sql_assets",
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
        sql_asset: Optional[SQL] = Field(
            None, description="", alias="sqlAsset"
        )  # relationship

    attributes: "DbtSource.Attributes" = Field(
        default_factory=lambda: DbtSource.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DbtProcess(Dbt):
    """Description"""

    type_name: str = Field("DbtProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtProcess":
            raise ValueError("must be DbtProcess")
        return v

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
        "column_processes",
    ]

    @property
    def dbt_process_job_status(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dbt_process_job_status
        )

    @dbt_process_job_status.setter
    def dbt_process_job_status(self, dbt_process_job_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_process_job_status = dbt_process_job_status

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
    def column_processes(self) -> Optional[list[ColumnProcess]]:
        return None if self.attributes is None else self.attributes.column_processes

    @column_processes.setter
    def column_processes(self, column_processes: Optional[list[ColumnProcess]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_processes = column_processes

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
        column_processes: Optional[list[ColumnProcess]] = Field(
            None, description="", alias="columnProcesses"
        )  # relationship

    attributes: "DbtProcess.Attributes" = Field(
        default_factory=lambda: DbtProcess.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ReadmeTemplate(Resource):
    """Description"""

    type_name: str = Field("ReadmeTemplate", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ReadmeTemplate":
            raise ValueError("must be ReadmeTemplate")
        return v

    def __setattr__(self, name, value):
        if name in ReadmeTemplate._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "icon",
        "icon_type",
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

    class Attributes(Resource.Attributes):
        icon: Optional[str] = Field(None, description="", alias="icon")
        icon_type: Optional[IconType] = Field(None, description="", alias="iconType")

    attributes: "ReadmeTemplate.Attributes" = Field(
        default_factory=lambda: ReadmeTemplate.Attributes(),
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
        if name in Readme._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "internal",
        "asset",
        "see_also",
    ]

    @property
    def internal(self) -> Optional[Internal]:
        return None if self.attributes is None else self.attributes.internal

    @internal.setter
    def internal(self, internal: Optional[Internal]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.internal = internal

    @property
    def asset(self) -> Optional[Asset]:
        return None if self.attributes is None else self.attributes.asset

    @asset.setter
    def asset(self, asset: Optional[Asset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset = asset

    @property
    def see_also(self) -> Optional[list[Readme]]:
        return None if self.attributes is None else self.attributes.see_also

    @see_also.setter
    def see_also(self, see_also: Optional[list[Readme]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.see_also = see_also

    class Attributes(Resource.Attributes):
        internal: Optional[Internal] = Field(
            None, description="", alias="__internal"
        )  # relationship
        asset: Optional[Asset] = Field(
            None, description="", alias="asset"
        )  # relationship
        see_also: Optional[list[Readme]] = Field(
            None, description="", alias="seeAlso"
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
        default_factory=lambda: Readme.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class File(Resource):
    """Description"""

    type_name: str = Field("File", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "File":
            raise ValueError("must be File")
        return v

    def __setattr__(self, name, value):
        if name in File._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
        if name in Link._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "icon",
        "icon_type",
        "internal",
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
    def internal(self) -> Optional[Internal]:
        return None if self.attributes is None else self.attributes.internal

    @internal.setter
    def internal(self, internal: Optional[Internal]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.internal = internal

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
        internal: Optional[Internal] = Field(
            None, description="", alias="internal"
        )  # relationship
        asset: Optional[Asset] = Field(
            None, description="", alias="asset"
        )  # relationship

    attributes: "Link.Attributes" = Field(
        default_factory=lambda: Link.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class APISpec(API):
    """Description"""

    type_name: str = Field("APISpec", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "APISpec":
            raise ValueError("must be APISpec")
        return v

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
        "api_paths",
    ]

    @property
    def api_spec_terms_of_service_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.api_spec_terms_of_service_url
        )

    @api_spec_terms_of_service_url.setter
    def api_spec_terms_of_service_url(
        self, api_spec_terms_of_service_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_terms_of_service_url = api_spec_terms_of_service_url

    @property
    def api_spec_contact_email(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.api_spec_contact_email
        )

    @api_spec_contact_email.setter
    def api_spec_contact_email(self, api_spec_contact_email: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_contact_email = api_spec_contact_email

    @property
    def api_spec_contact_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.api_spec_contact_name
        )

    @api_spec_contact_name.setter
    def api_spec_contact_name(self, api_spec_contact_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_contact_name = api_spec_contact_name

    @property
    def api_spec_contact_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_spec_contact_url

    @api_spec_contact_url.setter
    def api_spec_contact_url(self, api_spec_contact_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_contact_url = api_spec_contact_url

    @property
    def api_spec_license_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.api_spec_license_name
        )

    @api_spec_license_name.setter
    def api_spec_license_name(self, api_spec_license_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_license_name = api_spec_license_name

    @property
    def api_spec_license_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_spec_license_url

    @api_spec_license_url.setter
    def api_spec_license_url(self, api_spec_license_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_license_url = api_spec_license_url

    @property
    def api_spec_contract_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.api_spec_contract_version
        )

    @api_spec_contract_version.setter
    def api_spec_contract_version(self, api_spec_contract_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_contract_version = api_spec_contract_version

    @property
    def api_spec_service_alias(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.api_spec_service_alias
        )

    @api_spec_service_alias.setter
    def api_spec_service_alias(self, api_spec_service_alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_service_alias = api_spec_service_alias

    @property
    def api_paths(self) -> Optional[list[APIPath]]:
        return None if self.attributes is None else self.attributes.api_paths

    @api_paths.setter
    def api_paths(self, api_paths: Optional[list[APIPath]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_paths = api_paths

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
        api_paths: Optional[list[APIPath]] = Field(
            None, description="", alias="apiPaths"
        )  # relationship

    attributes: "APISpec.Attributes" = Field(
        default_factory=lambda: APISpec.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class APIPath(API):
    """Description"""

    type_name: str = Field("APIPath", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "APIPath":
            raise ValueError("must be APIPath")
        return v

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
        "api_spec",
    ]

    @property
    def api_path_summary(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_path_summary

    @api_path_summary.setter
    def api_path_summary(self, api_path_summary: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_summary = api_path_summary

    @property
    def api_path_raw_u_r_i(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_path_raw_u_r_i

    @api_path_raw_u_r_i.setter
    def api_path_raw_u_r_i(self, api_path_raw_u_r_i: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_raw_u_r_i = api_path_raw_u_r_i

    @property
    def api_path_is_templated(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.api_path_is_templated
        )

    @api_path_is_templated.setter
    def api_path_is_templated(self, api_path_is_templated: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_is_templated = api_path_is_templated

    @property
    def api_path_available_operations(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.api_path_available_operations
        )

    @api_path_available_operations.setter
    def api_path_available_operations(
        self, api_path_available_operations: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_available_operations = api_path_available_operations

    @property
    def api_path_available_response_codes(self) -> Optional[dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.api_path_available_response_codes
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.api_path_is_ingress_exposed
        )

    @api_path_is_ingress_exposed.setter
    def api_path_is_ingress_exposed(self, api_path_is_ingress_exposed: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_is_ingress_exposed = api_path_is_ingress_exposed

    @property
    def api_spec(self) -> Optional[APISpec]:
        return None if self.attributes is None else self.attributes.api_spec

    @api_spec.setter
    def api_spec(self, api_spec: Optional[APISpec]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec = api_spec

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
        api_spec: Optional[APISpec] = Field(
            None, description="", alias="apiSpec"
        )  # relationship

    attributes: "APIPath.Attributes" = Field(
        default_factory=lambda: APIPath.Attributes(),
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
        if name in SnowflakeTag._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "tag_id",
        "tag_attributes",
        "tag_allowed_values",
        "mapped_classification_name",
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
    def mapped_classification_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mapped_classification_name
        )

    @mapped_classification_name.setter
    def mapped_classification_name(self, mapped_classification_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mapped_classification_name = mapped_classification_name

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
        mapped_classification_name: Optional[str] = Field(
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
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
        )  # relationship

    attributes: "SnowflakeTag.Attributes" = Field(
        default_factory=lambda: SnowflakeTag.Attributes(),
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
        "columns",
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
    def columns(self) -> Optional[list[Column]]:
        return None if self.attributes is None else self.attributes.columns

    @columns.setter
    def columns(self, columns: Optional[list[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.columns = columns

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
        columns: Optional[list[Column]] = Field(
            None, description="", alias="columns"
        )  # relationship
        parent_table: Optional[Table] = Field(
            None, description="", alias="parentTable"
        )  # relationship

    attributes: "TablePartition.Attributes" = Field(
        default_factory=lambda: TablePartition.Attributes(),
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


class Query(SQL):
    """Description"""

    type_name: str = Field("Query", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Query":
            raise ValueError("must be Query")
        return v

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
    def parent_qualified_name(self) -> str:
        return (
            None if self.attributes is None else self.attributes.parent_qualified_name
        )

    @parent_qualified_name.setter
    def parent_qualified_name(self, parent_qualified_name: str):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_qualified_name = parent_qualified_name

    @property
    def collection_qualified_name(self) -> str:
        return (
            None
            if self.attributes is None
            else self.attributes.collection_qualified_name
        )

    @collection_qualified_name.setter
    def collection_qualified_name(self, collection_qualified_name: str):
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
    def parent(self) -> Namespace:
        return None if self.attributes is None else self.attributes.parent

    @parent.setter
    def parent(self, parent: Namespace):
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
        parent: Namespace = Field(None, description="", alias="parent")  # relationship
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
        if name in Column._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
        if name in Schema._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "table_count",
        "views_count",
        "snowflake_tags",
        "materialised_views",
        "tables",
        "database",
        "snowflake_pipes",
        "snowflake_streams",
        "procedures",
        "views",
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
    def materialised_views(self) -> Optional[list[MaterialisedView]]:
        return None if self.attributes is None else self.attributes.materialised_views

    @materialised_views.setter
    def materialised_views(self, materialised_views: Optional[list[MaterialisedView]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.materialised_views = materialised_views

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

    class Attributes(SQL.Attributes):
        table_count: Optional[int] = Field(None, description="", alias="tableCount")
        views_count: Optional[int] = Field(None, description="", alias="viewsCount")
        snowflake_tags: Optional[list[SnowflakeTag]] = Field(
            None, description="", alias="snowflakeTags"
        )  # relationship
        materialised_views: Optional[list[MaterialisedView]] = Field(
            None, description="", alias="materialisedViews"
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
        views: Optional[list[View]] = Field(
            None, description="", alias="views"
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


class SnowflakeStream(SQL):
    """Description"""

    type_name: str = Field("SnowflakeStream", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakeStream":
            raise ValueError("must be SnowflakeStream")
        return v

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


class SnowflakePipe(SQL):
    """Description"""

    type_name: str = Field("SnowflakePipe", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakePipe":
            raise ValueError("must be SnowflakePipe")
        return v

    def __setattr__(self, name, value):
        if name in SnowflakePipe._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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


class Database(SQL):
    """Description"""

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

    type_name: str = Field("Database", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Database":
            raise ValueError("must be Database")
        return v

    def __setattr__(self, name, value):
        if name in Database._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
        if name in Procedure._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "definition",
        "atlan_schema",
    ]

    @property
    def definition(self) -> str:
        return None if self.attributes is None else self.attributes.definition

    @definition.setter
    def definition(self, definition: str):
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
        definition: str = Field(None, description="", alias="definition")
        atlan_schema: Optional[Schema] = Field(
            None, description="", alias="atlanSchema"
        )  # relationship

    attributes: "Procedure.Attributes" = Field(
        default_factory=lambda: Procedure.Attributes(),
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


class DataStudioAsset(DataStudio):
    """Description"""

    type_name: str = Field("DataStudioAsset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataStudioAsset":
            raise ValueError("must be DataStudioAsset")
        return v

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
    ]

    @property
    def data_studio_asset_type(self) -> Optional[GoogleDatastudioAssetType]:
        return (
            None if self.attributes is None else self.attributes.data_studio_asset_type
        )

    @data_studio_asset_type.setter
    def data_studio_asset_type(
        self, data_studio_asset_type: Optional[GoogleDatastudioAssetType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_studio_asset_type = data_studio_asset_type

    @property
    def data_studio_asset_title(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.data_studio_asset_title
        )

    @data_studio_asset_title.setter
    def data_studio_asset_title(self, data_studio_asset_title: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_studio_asset_title = data_studio_asset_title

    @property
    def data_studio_asset_owner(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.data_studio_asset_owner
        )

    @data_studio_asset_owner.setter
    def data_studio_asset_owner(self, data_studio_asset_owner: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_studio_asset_owner = data_studio_asset_owner

    @property
    def is_trashed_data_studio_asset(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.is_trashed_data_studio_asset
        )

    @is_trashed_data_studio_asset.setter
    def is_trashed_data_studio_asset(
        self, is_trashed_data_studio_asset: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_trashed_data_studio_asset = is_trashed_data_studio_asset

    @property
    def google_service(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_service

    @google_service.setter
    def google_service(self, google_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_service = google_service

    @property
    def google_project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_project_name

    @google_project_name.setter
    def google_project_name(self, google_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_name = google_project_name

    @property
    def google_project_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_project_id

    @google_project_id.setter
    def google_project_id(self, google_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_id = google_project_id

    @property
    def google_project_number(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.google_project_number
        )

    @google_project_number.setter
    def google_project_number(self, google_project_number: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_number = google_project_number

    @property
    def google_location(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_location

    @google_location.setter
    def google_location(self, google_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location = google_location

    @property
    def google_location_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_location_type

    @google_location_type.setter
    def google_location_type(self, google_location_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location_type = google_location_type

    @property
    def google_labels(self) -> Optional[list[GoogleLabel]]:
        return None if self.attributes is None else self.attributes.google_labels

    @google_labels.setter
    def google_labels(self, google_labels: Optional[list[GoogleLabel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_labels = google_labels

    @property
    def google_tags(self) -> Optional[list[GoogleTag]]:
        return None if self.attributes is None else self.attributes.google_tags

    @google_tags.setter
    def google_tags(self, google_tags: Optional[list[GoogleTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_tags = google_tags

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

    attributes: "DataStudioAsset.Attributes" = Field(
        default_factory=lambda: DataStudioAsset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class KafkaTopic(Kafka):
    """Description"""

    type_name: str = Field("KafkaTopic", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "KafkaTopic":
            raise ValueError("must be KafkaTopic")
        return v

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
        "kafka_consumer_groups",
    ]

    @property
    def kafka_topic_is_internal(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.kafka_topic_is_internal
        )

    @kafka_topic_is_internal.setter
    def kafka_topic_is_internal(self, kafka_topic_is_internal: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_is_internal = kafka_topic_is_internal

    @property
    def kafka_topic_compression_type(self) -> Optional[KafkaTopicCompressionType]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_compression_type
        )

    @kafka_topic_compression_type.setter
    def kafka_topic_compression_type(
        self, kafka_topic_compression_type: Optional[KafkaTopicCompressionType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_compression_type = kafka_topic_compression_type

    @property
    def kafka_topic_replication_factor(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_replication_factor
        )

    @kafka_topic_replication_factor.setter
    def kafka_topic_replication_factor(
        self, kafka_topic_replication_factor: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_replication_factor = kafka_topic_replication_factor

    @property
    def kafka_topic_segment_bytes(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_segment_bytes
        )

    @kafka_topic_segment_bytes.setter
    def kafka_topic_segment_bytes(self, kafka_topic_segment_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_segment_bytes = kafka_topic_segment_bytes

    @property
    def kafka_topic_partitions_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_partitions_count
        )

    @kafka_topic_partitions_count.setter
    def kafka_topic_partitions_count(self, kafka_topic_partitions_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_partitions_count = kafka_topic_partitions_count

    @property
    def kafka_topic_size_in_bytes(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_size_in_bytes
        )

    @kafka_topic_size_in_bytes.setter
    def kafka_topic_size_in_bytes(self, kafka_topic_size_in_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_size_in_bytes = kafka_topic_size_in_bytes

    @property
    def kafka_topic_record_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_record_count
        )

    @kafka_topic_record_count.setter
    def kafka_topic_record_count(self, kafka_topic_record_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_record_count = kafka_topic_record_count

    @property
    def kafka_topic_cleanup_policy(self) -> Optional[PowerbiEndorsement]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_cleanup_policy
        )

    @kafka_topic_cleanup_policy.setter
    def kafka_topic_cleanup_policy(
        self, kafka_topic_cleanup_policy: Optional[PowerbiEndorsement]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_cleanup_policy = kafka_topic_cleanup_policy

    @property
    def kafka_consumer_groups(self) -> Optional[list[KafkaConsumerGroup]]:
        return (
            None if self.attributes is None else self.attributes.kafka_consumer_groups
        )

    @kafka_consumer_groups.setter
    def kafka_consumer_groups(
        self, kafka_consumer_groups: Optional[list[KafkaConsumerGroup]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_consumer_groups = kafka_consumer_groups

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
        kafka_consumer_groups: Optional[list[KafkaConsumerGroup]] = Field(
            None, description="", alias="kafkaConsumerGroups"
        )  # relationship

    attributes: "KafkaTopic.Attributes" = Field(
        default_factory=lambda: KafkaTopic.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class KafkaConsumerGroup(Kafka):
    """Description"""

    type_name: str = Field("KafkaConsumerGroup", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "KafkaConsumerGroup":
            raise ValueError("must be KafkaConsumerGroup")
        return v

    def __setattr__(self, name, value):
        if name in KafkaConsumerGroup._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "kafka_consumer_group_topic_consumption_properties",
        "kafka_consumer_group_member_count",
        "kafka_topic_names",
        "kafka_topic_qualified_names",
        "kafka_topics",
    ]

    @property
    def kafka_consumer_group_topic_consumption_properties(
        self,
    ) -> Optional[list[KafkaTopicConsumption]]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_consumer_group_topic_consumption_properties
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_consumer_group_member_count
        )

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
        return None if self.attributes is None else self.attributes.kafka_topic_names

    @kafka_topic_names.setter
    def kafka_topic_names(self, kafka_topic_names: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_names = kafka_topic_names

    @property
    def kafka_topic_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_qualified_names
        )

    @kafka_topic_qualified_names.setter
    def kafka_topic_qualified_names(
        self, kafka_topic_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_qualified_names = kafka_topic_qualified_names

    @property
    def kafka_topics(self) -> Optional[list[KafkaTopic]]:
        return None if self.attributes is None else self.attributes.kafka_topics

    @kafka_topics.setter
    def kafka_topics(self, kafka_topics: Optional[list[KafkaTopic]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topics = kafka_topics

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
        kafka_topics: Optional[list[KafkaTopic]] = Field(
            None, description="", alias="kafkaTopics"
        )  # relationship

    attributes: "KafkaConsumerGroup.Attributes" = Field(
        default_factory=lambda: KafkaConsumerGroup.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class S3Bucket(S3):
    """Description"""

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

    type_name: str = Field("S3Bucket", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "S3Bucket":
            raise ValueError("must be S3Bucket")
        return v

    def __setattr__(self, name, value):
        if name in S3Bucket._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "s3_object_count",
        "s3_bucket_versioning_enabled",
        "objects",
    ]

    @property
    def s3_object_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.s3_object_count

    @s3_object_count.setter
    def s3_object_count(self, s3_object_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_count = s3_object_count

    @property
    def s3_bucket_versioning_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.s3_bucket_versioning_enabled
        )

    @s3_bucket_versioning_enabled.setter
    def s3_bucket_versioning_enabled(
        self, s3_bucket_versioning_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_bucket_versioning_enabled = s3_bucket_versioning_enabled

    @property
    def objects(self) -> Optional[list[S3Object]]:
        return None if self.attributes is None else self.attributes.objects

    @objects.setter
    def objects(self, objects: Optional[list[S3Object]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.objects = objects

    class Attributes(S3.Attributes):
        s3_object_count: Optional[int] = Field(
            None, description="", alias="s3ObjectCount"
        )
        s3_bucket_versioning_enabled: Optional[bool] = Field(
            None, description="", alias="s3BucketVersioningEnabled"
        )
        objects: Optional[list[S3Object]] = Field(
            None, description="", alias="objects"
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
        default_factory=lambda: S3Bucket.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class S3Object(S3):
    """Description"""

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

    type_name: str = Field("S3Object", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "S3Object":
            raise ValueError("must be S3Object")
        return v

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
        "bucket",
    ]

    @property
    def s3_object_last_modified_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.s3_object_last_modified_time
        )

    @s3_object_last_modified_time.setter
    def s3_object_last_modified_time(
        self, s3_object_last_modified_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_last_modified_time = s3_object_last_modified_time

    @property
    def s3_bucket_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.s3_bucket_name

    @s3_bucket_name.setter
    def s3_bucket_name(self, s3_bucket_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_bucket_name = s3_bucket_name

    @property
    def s3_bucket_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.s3_bucket_qualified_name
        )

    @s3_bucket_qualified_name.setter
    def s3_bucket_qualified_name(self, s3_bucket_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_bucket_qualified_name = s3_bucket_qualified_name

    @property
    def s3_object_size(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.s3_object_size

    @s3_object_size.setter
    def s3_object_size(self, s3_object_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_size = s3_object_size

    @property
    def s3_object_storage_class(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.s3_object_storage_class
        )

    @s3_object_storage_class.setter
    def s3_object_storage_class(self, s3_object_storage_class: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_storage_class = s3_object_storage_class

    @property
    def s3_object_key(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.s3_object_key

    @s3_object_key.setter
    def s3_object_key(self, s3_object_key: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_key = s3_object_key

    @property
    def s3_object_content_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.s3_object_content_type
        )

    @s3_object_content_type.setter
    def s3_object_content_type(self, s3_object_content_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_content_type = s3_object_content_type

    @property
    def s3_object_content_disposition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.s3_object_content_disposition
        )

    @s3_object_content_disposition.setter
    def s3_object_content_disposition(
        self, s3_object_content_disposition: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_content_disposition = s3_object_content_disposition

    @property
    def s3_object_version_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.s3_object_version_id

    @s3_object_version_id.setter
    def s3_object_version_id(self, s3_object_version_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_version_id = s3_object_version_id

    @property
    def bucket(self) -> Optional[S3Bucket]:
        return None if self.attributes is None else self.attributes.bucket

    @bucket.setter
    def bucket(self, bucket: Optional[S3Bucket]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.bucket = bucket

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
        default_factory=lambda: S3Object.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ADLSAccount(ADLS):
    """Description"""

    type_name: str = Field("ADLSAccount", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADLSAccount":
            raise ValueError("must be ADLSAccount")
        return v

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
        "adls_containers",
    ]

    @property
    def adls_e_tag(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.adls_e_tag

    @adls_e_tag.setter
    def adls_e_tag(self, adls_e_tag: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_e_tag = adls_e_tag

    @property
    def adls_encryption_type(self) -> Optional[ADLSEncryptionTypes]:
        return None if self.attributes is None else self.attributes.adls_encryption_type

    @adls_encryption_type.setter
    def adls_encryption_type(self, adls_encryption_type: Optional[ADLSEncryptionTypes]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_encryption_type = adls_encryption_type

    @property
    def adls_account_resource_group(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_resource_group
        )

    @adls_account_resource_group.setter
    def adls_account_resource_group(self, adls_account_resource_group: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_resource_group = adls_account_resource_group

    @property
    def adls_account_subscription(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_subscription
        )

    @adls_account_subscription.setter
    def adls_account_subscription(self, adls_account_subscription: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_subscription = adls_account_subscription

    @property
    def adls_account_performance(self) -> Optional[ADLSPerformance]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_performance
        )

    @adls_account_performance.setter
    def adls_account_performance(
        self, adls_account_performance: Optional[ADLSPerformance]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_performance = adls_account_performance

    @property
    def adls_account_replication(self) -> Optional[ADLSReplicationType]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_replication
        )

    @adls_account_replication.setter
    def adls_account_replication(
        self, adls_account_replication: Optional[ADLSReplicationType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_replication = adls_account_replication

    @property
    def adls_account_kind(self) -> Optional[ADLSStorageKind]:
        return None if self.attributes is None else self.attributes.adls_account_kind

    @adls_account_kind.setter
    def adls_account_kind(self, adls_account_kind: Optional[ADLSStorageKind]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_kind = adls_account_kind

    @property
    def adls_primary_disk_state(self) -> Optional[ADLSAccountStatus]:
        return (
            None if self.attributes is None else self.attributes.adls_primary_disk_state
        )

    @adls_primary_disk_state.setter
    def adls_primary_disk_state(
        self, adls_primary_disk_state: Optional[ADLSAccountStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_primary_disk_state = adls_primary_disk_state

    @property
    def adls_account_provision_state(self) -> Optional[ADLSProvisionState]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_provision_state
        )

    @adls_account_provision_state.setter
    def adls_account_provision_state(
        self, adls_account_provision_state: Optional[ADLSProvisionState]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_provision_state = adls_account_provision_state

    @property
    def adls_account_access_tier(self) -> Optional[ADLSAccessTier]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_access_tier
        )

    @adls_account_access_tier.setter
    def adls_account_access_tier(
        self, adls_account_access_tier: Optional[ADLSAccessTier]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_access_tier = adls_account_access_tier

    @property
    def adls_containers(self) -> Optional[list[ADLSContainer]]:
        return None if self.attributes is None else self.attributes.adls_containers

    @adls_containers.setter
    def adls_containers(self, adls_containers: Optional[list[ADLSContainer]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_containers = adls_containers

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
        adls_containers: Optional[list[ADLSContainer]] = Field(
            None, description="", alias="adlsContainers"
        )  # relationship

    attributes: "ADLSAccount.Attributes" = Field(
        default_factory=lambda: ADLSAccount.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ADLSContainer(ADLS):
    """Description"""

    type_name: str = Field("ADLSContainer", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADLSContainer":
            raise ValueError("must be ADLSContainer")
        return v

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
        "adls_objects",
        "adls_account",
    ]

    @property
    def adls_container_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.adls_container_url

    @adls_container_url.setter
    def adls_container_url(self, adls_container_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_url = adls_container_url

    @property
    def adls_container_lease_state(self) -> Optional[ADLSLeaseState]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_container_lease_state
        )

    @adls_container_lease_state.setter
    def adls_container_lease_state(
        self, adls_container_lease_state: Optional[ADLSLeaseState]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_lease_state = adls_container_lease_state

    @property
    def adls_container_lease_status(self) -> Optional[ADLSLeaseStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_container_lease_status
        )

    @adls_container_lease_status.setter
    def adls_container_lease_status(
        self, adls_container_lease_status: Optional[ADLSLeaseStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_lease_status = adls_container_lease_status

    @property
    def adls_container_encryption_scope(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_container_encryption_scope
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.adls_container_version_level_immutability_support
        )

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
        return None if self.attributes is None else self.attributes.adls_object_count

    @adls_object_count.setter
    def adls_object_count(self, adls_object_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_count = adls_object_count

    @property
    def adls_objects(self) -> Optional[list[ADLSObject]]:
        return None if self.attributes is None else self.attributes.adls_objects

    @adls_objects.setter
    def adls_objects(self, adls_objects: Optional[list[ADLSObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_objects = adls_objects

    @property
    def adls_account(self) -> Optional[ADLSAccount]:
        return None if self.attributes is None else self.attributes.adls_account

    @adls_account.setter
    def adls_account(self, adls_account: Optional[ADLSAccount]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account = adls_account

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
        adls_account: Optional[ADLSAccount] = Field(
            None, description="", alias="adlsAccount"
        )  # relationship

    attributes: "ADLSContainer.Attributes" = Field(
        default_factory=lambda: ADLSContainer.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ADLSObject(ADLS):
    """Description"""

    type_name: str = Field("ADLSObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADLSObject":
            raise ValueError("must be ADLSObject")
        return v

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
        "adls_container",
    ]

    @property
    def adls_object_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.adls_object_url

    @adls_object_url.setter
    def adls_object_url(self, adls_object_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_url = adls_object_url

    @property
    def adls_object_version_id(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.adls_object_version_id
        )

    @adls_object_version_id.setter
    def adls_object_version_id(self, adls_object_version_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_version_id = adls_object_version_id

    @property
    def adls_object_type(self) -> Optional[ADLSObjectType]:
        return None if self.attributes is None else self.attributes.adls_object_type

    @adls_object_type.setter
    def adls_object_type(self, adls_object_type: Optional[ADLSObjectType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_type = adls_object_type

    @property
    def adls_object_size(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.adls_object_size

    @adls_object_size.setter
    def adls_object_size(self, adls_object_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_size = adls_object_size

    @property
    def adls_object_access_tier(self) -> Optional[ADLSAccessTier]:
        return (
            None if self.attributes is None else self.attributes.adls_object_access_tier
        )

    @adls_object_access_tier.setter
    def adls_object_access_tier(
        self, adls_object_access_tier: Optional[ADLSAccessTier]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_access_tier = adls_object_access_tier

    @property
    def adls_object_access_tier_last_modified_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_access_tier_last_modified_time
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_archive_status
        )

    @adls_object_archive_status.setter
    def adls_object_archive_status(
        self, adls_object_archive_status: Optional[ADLSObjectArchiveStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_archive_status = adls_object_archive_status

    @property
    def adls_object_server_encrypted(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_server_encrypted
        )

    @adls_object_server_encrypted.setter
    def adls_object_server_encrypted(
        self, adls_object_server_encrypted: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_server_encrypted = adls_object_server_encrypted

    @property
    def adls_object_version_level_immutability_support(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_version_level_immutability_support
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_cache_control
        )

    @adls_object_cache_control.setter
    def adls_object_cache_control(self, adls_object_cache_control: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_cache_control = adls_object_cache_control

    @property
    def adls_object_content_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_content_type
        )

    @adls_object_content_type.setter
    def adls_object_content_type(self, adls_object_content_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_content_type = adls_object_content_type

    @property
    def adls_object_content_m_d5_hash(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_content_m_d5_hash
        )

    @adls_object_content_m_d5_hash.setter
    def adls_object_content_m_d5_hash(
        self, adls_object_content_m_d5_hash: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_content_m_d5_hash = adls_object_content_m_d5_hash

    @property
    def adls_object_content_language(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_content_language
        )

    @adls_object_content_language.setter
    def adls_object_content_language(self, adls_object_content_language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_content_language = adls_object_content_language

    @property
    def adls_object_lease_status(self) -> Optional[ADLSLeaseStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_lease_status
        )

    @adls_object_lease_status.setter
    def adls_object_lease_status(
        self, adls_object_lease_status: Optional[ADLSLeaseStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_lease_status = adls_object_lease_status

    @property
    def adls_object_lease_state(self) -> Optional[ADLSLeaseState]:
        return (
            None if self.attributes is None else self.attributes.adls_object_lease_state
        )

    @adls_object_lease_state.setter
    def adls_object_lease_state(
        self, adls_object_lease_state: Optional[ADLSLeaseState]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_lease_state = adls_object_lease_state

    @property
    def adls_object_metadata(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.adls_object_metadata

    @adls_object_metadata.setter
    def adls_object_metadata(self, adls_object_metadata: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_metadata = adls_object_metadata

    @property
    def adls_container_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_container_qualified_name
        )

    @adls_container_qualified_name.setter
    def adls_container_qualified_name(
        self, adls_container_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_qualified_name = adls_container_qualified_name

    @property
    def adls_container(self) -> Optional[ADLSContainer]:
        return None if self.attributes is None else self.attributes.adls_container

    @adls_container.setter
    def adls_container(self, adls_container: Optional[ADLSContainer]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container = adls_container

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
        adls_container: Optional[ADLSContainer] = Field(
            None, description="", alias="adlsContainer"
        )  # relationship

    attributes: "ADLSObject.Attributes" = Field(
        default_factory=lambda: ADLSObject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class GCSObject(GCS):
    """Description"""

    type_name: str = Field("GCSObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "GCSObject":
            raise ValueError("must be GCSObject")
        return v

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
        "gcs_bucket",
    ]

    @property
    def gcs_bucket_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_bucket_name

    @gcs_bucket_name.setter
    def gcs_bucket_name(self, gcs_bucket_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_name = gcs_bucket_name

    @property
    def gcs_bucket_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_qualified_name
        )

    @gcs_bucket_qualified_name.setter
    def gcs_bucket_qualified_name(self, gcs_bucket_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_qualified_name = gcs_bucket_qualified_name

    @property
    def gcs_object_size(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.gcs_object_size

    @gcs_object_size.setter
    def gcs_object_size(self, gcs_object_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_size = gcs_object_size

    @property
    def gcs_object_key(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_object_key

    @gcs_object_key.setter
    def gcs_object_key(self, gcs_object_key: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_key = gcs_object_key

    @property
    def gcs_object_media_link(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.gcs_object_media_link
        )

    @gcs_object_media_link.setter
    def gcs_object_media_link(self, gcs_object_media_link: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_media_link = gcs_object_media_link

    @property
    def gcs_object_hold_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_object_hold_type

    @gcs_object_hold_type.setter
    def gcs_object_hold_type(self, gcs_object_hold_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_hold_type = gcs_object_hold_type

    @property
    def gcs_object_generation_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_generation_id
        )

    @gcs_object_generation_id.setter
    def gcs_object_generation_id(self, gcs_object_generation_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_generation_id = gcs_object_generation_id

    @property
    def gcs_object_c_r_c32_c_hash(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_c_r_c32_c_hash
        )

    @gcs_object_c_r_c32_c_hash.setter
    def gcs_object_c_r_c32_c_hash(self, gcs_object_c_r_c32_c_hash: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_c_r_c32_c_hash = gcs_object_c_r_c32_c_hash

    @property
    def gcs_object_m_d5_hash(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_object_m_d5_hash

    @gcs_object_m_d5_hash.setter
    def gcs_object_m_d5_hash(self, gcs_object_m_d5_hash: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_m_d5_hash = gcs_object_m_d5_hash

    @property
    def gcs_object_data_last_modified_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_data_last_modified_time
        )

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
        return (
            None if self.attributes is None else self.attributes.gcs_object_content_type
        )

    @gcs_object_content_type.setter
    def gcs_object_content_type(self, gcs_object_content_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_type = gcs_object_content_type

    @property
    def gcs_object_content_encoding(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_content_encoding
        )

    @gcs_object_content_encoding.setter
    def gcs_object_content_encoding(self, gcs_object_content_encoding: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_encoding = gcs_object_content_encoding

    @property
    def gcs_object_content_disposition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_content_disposition
        )

    @gcs_object_content_disposition.setter
    def gcs_object_content_disposition(
        self, gcs_object_content_disposition: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_disposition = gcs_object_content_disposition

    @property
    def gcs_object_content_language(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_content_language
        )

    @gcs_object_content_language.setter
    def gcs_object_content_language(self, gcs_object_content_language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_language = gcs_object_content_language

    @property
    def gcs_object_retention_expiration_date(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_retention_expiration_date
        )

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
    def gcs_bucket(self) -> Optional[GCSBucket]:
        return None if self.attributes is None else self.attributes.gcs_bucket

    @gcs_bucket.setter
    def gcs_bucket(self, gcs_bucket: Optional[GCSBucket]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket = gcs_bucket

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
        gcs_bucket: Optional[GCSBucket] = Field(
            None, description="", alias="gcsBucket"
        )  # relationship

    attributes: "GCSObject.Attributes" = Field(
        default_factory=lambda: GCSObject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class GCSBucket(GCS):
    """Description"""

    type_name: str = Field("GCSBucket", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "GCSBucket":
            raise ValueError("must be GCSBucket")
        return v

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
        "gcs_objects",
    ]

    @property
    def gcs_object_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.gcs_object_count

    @gcs_object_count.setter
    def gcs_object_count(self, gcs_object_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_count = gcs_object_count

    @property
    def gcs_bucket_versioning_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_versioning_enabled
        )

    @gcs_bucket_versioning_enabled.setter
    def gcs_bucket_versioning_enabled(
        self, gcs_bucket_versioning_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_versioning_enabled = gcs_bucket_versioning_enabled

    @property
    def gcs_bucket_retention_locked(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_retention_locked
        )

    @gcs_bucket_retention_locked.setter
    def gcs_bucket_retention_locked(self, gcs_bucket_retention_locked: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_locked = gcs_bucket_retention_locked

    @property
    def gcs_bucket_retention_period(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_retention_period
        )

    @gcs_bucket_retention_period.setter
    def gcs_bucket_retention_period(self, gcs_bucket_retention_period: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_period = gcs_bucket_retention_period

    @property
    def gcs_bucket_retention_effective_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_retention_effective_time
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_lifecycle_rules
        )

    @gcs_bucket_lifecycle_rules.setter
    def gcs_bucket_lifecycle_rules(self, gcs_bucket_lifecycle_rules: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_lifecycle_rules = gcs_bucket_lifecycle_rules

    @property
    def gcs_bucket_retention_policy(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_retention_policy
        )

    @gcs_bucket_retention_policy.setter
    def gcs_bucket_retention_policy(self, gcs_bucket_retention_policy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_policy = gcs_bucket_retention_policy

    @property
    def gcs_objects(self) -> Optional[list[GCSObject]]:
        return None if self.attributes is None else self.attributes.gcs_objects

    @gcs_objects.setter
    def gcs_objects(self, gcs_objects: Optional[list[GCSObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_objects = gcs_objects

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
        gcs_objects: Optional[list[GCSObject]] = Field(
            None, description="", alias="gcsObjects"
        )  # relationship

    attributes: "GCSBucket.Attributes" = Field(
        default_factory=lambda: GCSBucket.Attributes(),
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
        if name in MCIncident._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "mc_incident_id",
        "mc_incident_type",
        "mc_incident_sub_types",
        "mc_incident_severity",
        "mc_incident_state",
        "mc_incident_warehouse",
        "mc_incident_assets",
        "mc_monitor",
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
    def mc_incident_assets(self) -> Optional[list[Asset]]:
        return None if self.attributes is None else self.attributes.mc_incident_assets

    @mc_incident_assets.setter
    def mc_incident_assets(self, mc_incident_assets: Optional[list[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_assets = mc_incident_assets

    @property
    def mc_monitor(self) -> Optional[MCMonitor]:
        return None if self.attributes is None else self.attributes.mc_monitor

    @mc_monitor.setter
    def mc_monitor(self, mc_monitor: Optional[MCMonitor]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor = mc_monitor

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
        mc_incident_assets: Optional[list[Asset]] = Field(
            None, description="", alias="mcIncidentAssets"
        )  # relationship
        mc_monitor: Optional[MCMonitor] = Field(
            None, description="", alias="mcMonitor"
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
        if name in MCMonitor._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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


class PresetChart(Preset):
    """Description"""

    type_name: str = Field("PresetChart", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetChart":
            raise ValueError("must be PresetChart")
        return v

    def __setattr__(self, name, value):
        if name in PresetChart._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "preset_chart_description_markdown",
        "preset_chart_form_data",
        "preset_dashboard",
    ]

    @property
    def preset_chart_description_markdown(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_chart_description_markdown
        )

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
        return (
            None if self.attributes is None else self.attributes.preset_chart_form_data
        )

    @preset_chart_form_data.setter
    def preset_chart_form_data(self, preset_chart_form_data: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_chart_form_data = preset_chart_form_data

    @property
    def preset_dashboard(self) -> Optional[PresetDashboard]:
        return None if self.attributes is None else self.attributes.preset_dashboard

    @preset_dashboard.setter
    def preset_dashboard(self, preset_dashboard: Optional[PresetDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard = preset_dashboard

    class Attributes(Preset.Attributes):
        preset_chart_description_markdown: Optional[str] = Field(
            None, description="", alias="presetChartDescriptionMarkdown"
        )
        preset_chart_form_data: Optional[dict[str, str]] = Field(
            None, description="", alias="presetChartFormData"
        )
        preset_dashboard: Optional[PresetDashboard] = Field(
            None, description="", alias="presetDashboard"
        )  # relationship

    attributes: "PresetChart.Attributes" = Field(
        default_factory=lambda: PresetChart.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PresetDataset(Preset):
    """Description"""

    type_name: str = Field("PresetDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetDataset":
            raise ValueError("must be PresetDataset")
        return v

    def __setattr__(self, name, value):
        if name in PresetDataset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "preset_dataset_datasource_name",
        "preset_dataset_id",
        "preset_dataset_type",
        "preset_dashboard",
    ]

    @property
    def preset_dataset_datasource_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dataset_datasource_name
        )

    @preset_dataset_datasource_name.setter
    def preset_dataset_datasource_name(
        self, preset_dataset_datasource_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dataset_datasource_name = preset_dataset_datasource_name

    @property
    def preset_dataset_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.preset_dataset_id

    @preset_dataset_id.setter
    def preset_dataset_id(self, preset_dataset_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dataset_id = preset_dataset_id

    @property
    def preset_dataset_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.preset_dataset_type

    @preset_dataset_type.setter
    def preset_dataset_type(self, preset_dataset_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dataset_type = preset_dataset_type

    @property
    def preset_dashboard(self) -> Optional[PresetDashboard]:
        return None if self.attributes is None else self.attributes.preset_dashboard

    @preset_dashboard.setter
    def preset_dashboard(self, preset_dashboard: Optional[PresetDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard = preset_dashboard

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
        preset_dashboard: Optional[PresetDashboard] = Field(
            None, description="", alias="presetDashboard"
        )  # relationship

    attributes: "PresetDataset.Attributes" = Field(
        default_factory=lambda: PresetDataset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PresetDashboard(Preset):
    """Description"""

    type_name: str = Field("PresetDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetDashboard":
            raise ValueError("must be PresetDashboard")
        return v

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
        "preset_datasets",
        "preset_charts",
        "preset_workspace",
    ]

    @property
    def preset_dashboard_changed_by_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_changed_by_name
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_changed_by_url
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_is_managed_externally
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_is_published
        )

    @preset_dashboard_is_published.setter
    def preset_dashboard_is_published(
        self, preset_dashboard_is_published: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_is_published = preset_dashboard_is_published

    @property
    def preset_dashboard_thumbnail_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_thumbnail_url
        )

    @preset_dashboard_thumbnail_url.setter
    def preset_dashboard_thumbnail_url(
        self, preset_dashboard_thumbnail_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_thumbnail_url = preset_dashboard_thumbnail_url

    @property
    def preset_dashboard_chart_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_chart_count
        )

    @preset_dashboard_chart_count.setter
    def preset_dashboard_chart_count(self, preset_dashboard_chart_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_chart_count = preset_dashboard_chart_count

    @property
    def preset_datasets(self) -> Optional[list[PresetDataset]]:
        return None if self.attributes is None else self.attributes.preset_datasets

    @preset_datasets.setter
    def preset_datasets(self, preset_datasets: Optional[list[PresetDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_datasets = preset_datasets

    @property
    def preset_charts(self) -> Optional[list[PresetChart]]:
        return None if self.attributes is None else self.attributes.preset_charts

    @preset_charts.setter
    def preset_charts(self, preset_charts: Optional[list[PresetChart]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_charts = preset_charts

    @property
    def preset_workspace(self) -> Optional[PresetWorkspace]:
        return None if self.attributes is None else self.attributes.preset_workspace

    @preset_workspace.setter
    def preset_workspace(self, preset_workspace: Optional[PresetWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace = preset_workspace

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
        preset_charts: Optional[list[PresetChart]] = Field(
            None, description="", alias="presetCharts"
        )  # relationship
        preset_workspace: Optional[PresetWorkspace] = Field(
            None, description="", alias="presetWorkspace"
        )  # relationship

    attributes: "PresetDashboard.Attributes" = Field(
        default_factory=lambda: PresetDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PresetWorkspace(Preset):
    """Description"""

    type_name: str = Field("PresetWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetWorkspace":
            raise ValueError("must be PresetWorkspace")
        return v

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
        "preset_dashboards",
    ]

    @property
    def preset_workspace_public_dashboards_allowed(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_public_dashboards_allowed
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_cluster_id
        )

    @preset_workspace_cluster_id.setter
    def preset_workspace_cluster_id(self, preset_workspace_cluster_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_cluster_id = preset_workspace_cluster_id

    @property
    def preset_workspace_hostname(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_hostname
        )

    @preset_workspace_hostname.setter
    def preset_workspace_hostname(self, preset_workspace_hostname: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_hostname = preset_workspace_hostname

    @property
    def preset_workspace_is_in_maintenance_mode(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_is_in_maintenance_mode
        )

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
        return (
            None if self.attributes is None else self.attributes.preset_workspace_region
        )

    @preset_workspace_region.setter
    def preset_workspace_region(self, preset_workspace_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_region = preset_workspace_region

    @property
    def preset_workspace_status(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.preset_workspace_status
        )

    @preset_workspace_status.setter
    def preset_workspace_status(self, preset_workspace_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_status = preset_workspace_status

    @property
    def preset_workspace_deployment_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_deployment_id
        )

    @preset_workspace_deployment_id.setter
    def preset_workspace_deployment_id(
        self, preset_workspace_deployment_id: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_deployment_id = preset_workspace_deployment_id

    @property
    def preset_workspace_dashboard_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_dashboard_count
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_dataset_count
        )

    @preset_workspace_dataset_count.setter
    def preset_workspace_dataset_count(
        self, preset_workspace_dataset_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_dataset_count = preset_workspace_dataset_count

    @property
    def preset_dashboards(self) -> Optional[list[PresetDashboard]]:
        return None if self.attributes is None else self.attributes.preset_dashboards

    @preset_dashboards.setter
    def preset_dashboards(self, preset_dashboards: Optional[list[PresetDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboards = preset_dashboards

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

    attributes: "PresetWorkspace.Attributes" = Field(
        default_factory=lambda: PresetWorkspace.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeReport(Mode):
    """Description"""

    type_name: str = Field("ModeReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeReport":
            raise ValueError("must be ModeReport")
        return v

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
        "mode_collections",
        "mode_queries",
    ]

    @property
    def mode_collection_token(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.mode_collection_token
        )

    @mode_collection_token.setter
    def mode_collection_token(self, mode_collection_token: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_token = mode_collection_token

    @property
    def mode_report_published_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.mode_report_published_at
        )

    @mode_report_published_at.setter
    def mode_report_published_at(self, mode_report_published_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report_published_at = mode_report_published_at

    @property
    def mode_query_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.mode_query_count

    @mode_query_count.setter
    def mode_query_count(self, mode_query_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_count = mode_query_count

    @property
    def mode_chart_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.mode_chart_count

    @mode_chart_count.setter
    def mode_chart_count(self, mode_chart_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_chart_count = mode_chart_count

    @property
    def mode_query_preview(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_query_preview

    @mode_query_preview.setter
    def mode_query_preview(self, mode_query_preview: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_preview = mode_query_preview

    @property
    def mode_is_public(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.mode_is_public

    @mode_is_public.setter
    def mode_is_public(self, mode_is_public: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_is_public = mode_is_public

    @property
    def mode_is_shared(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.mode_is_shared

    @mode_is_shared.setter
    def mode_is_shared(self, mode_is_shared: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_is_shared = mode_is_shared

    @property
    def mode_collections(self) -> Optional[list[ModeCollection]]:
        return None if self.attributes is None else self.attributes.mode_collections

    @mode_collections.setter
    def mode_collections(self, mode_collections: Optional[list[ModeCollection]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collections = mode_collections

    @property
    def mode_queries(self) -> Optional[list[ModeQuery]]:
        return None if self.attributes is None else self.attributes.mode_queries

    @mode_queries.setter
    def mode_queries(self, mode_queries: Optional[list[ModeQuery]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_queries = mode_queries

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
        mode_collections: Optional[list[ModeCollection]] = Field(
            None, description="", alias="modeCollections"
        )  # relationship
        mode_queries: Optional[list[ModeQuery]] = Field(
            None, description="", alias="modeQueries"
        )  # relationship

    attributes: "ModeReport.Attributes" = Field(
        default_factory=lambda: ModeReport.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeQuery(Mode):
    """Description"""

    type_name: str = Field("ModeQuery", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeQuery":
            raise ValueError("must be ModeQuery")
        return v

    def __setattr__(self, name, value):
        if name in ModeQuery._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "mode_raw_query",
        "mode_report_import_count",
        "mode_charts",
        "mode_report",
    ]

    @property
    def mode_raw_query(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_raw_query

    @mode_raw_query.setter
    def mode_raw_query(self, mode_raw_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_raw_query = mode_raw_query

    @property
    def mode_report_import_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.mode_report_import_count
        )

    @mode_report_import_count.setter
    def mode_report_import_count(self, mode_report_import_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report_import_count = mode_report_import_count

    @property
    def mode_charts(self) -> Optional[list[ModeChart]]:
        return None if self.attributes is None else self.attributes.mode_charts

    @mode_charts.setter
    def mode_charts(self, mode_charts: Optional[list[ModeChart]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_charts = mode_charts

    @property
    def mode_report(self) -> Optional[ModeReport]:
        return None if self.attributes is None else self.attributes.mode_report

    @mode_report.setter
    def mode_report(self, mode_report: Optional[ModeReport]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report = mode_report

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
        mode_report: Optional[ModeReport] = Field(
            None, description="", alias="modeReport"
        )  # relationship

    attributes: "ModeQuery.Attributes" = Field(
        default_factory=lambda: ModeQuery.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeChart(Mode):
    """Description"""

    type_name: str = Field("ModeChart", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeChart":
            raise ValueError("must be ModeChart")
        return v

    def __setattr__(self, name, value):
        if name in ModeChart._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "mode_chart_type",
        "mode_query",
    ]

    @property
    def mode_chart_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_chart_type

    @mode_chart_type.setter
    def mode_chart_type(self, mode_chart_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_chart_type = mode_chart_type

    @property
    def mode_query(self) -> Optional[ModeQuery]:
        return None if self.attributes is None else self.attributes.mode_query

    @mode_query.setter
    def mode_query(self, mode_query: Optional[ModeQuery]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query = mode_query

    class Attributes(Mode.Attributes):
        mode_chart_type: Optional[str] = Field(
            None, description="", alias="modeChartType"
        )
        mode_query: Optional[ModeQuery] = Field(
            None, description="", alias="modeQuery"
        )  # relationship

    attributes: "ModeChart.Attributes" = Field(
        default_factory=lambda: ModeChart.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeWorkspace(Mode):
    """Description"""

    type_name: str = Field("ModeWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeWorkspace":
            raise ValueError("must be ModeWorkspace")
        return v

    def __setattr__(self, name, value):
        if name in ModeWorkspace._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "mode_collection_count",
        "mode_collections",
    ]

    @property
    def mode_collection_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.mode_collection_count
        )

    @mode_collection_count.setter
    def mode_collection_count(self, mode_collection_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_count = mode_collection_count

    @property
    def mode_collections(self) -> Optional[list[ModeCollection]]:
        return None if self.attributes is None else self.attributes.mode_collections

    @mode_collections.setter
    def mode_collections(self, mode_collections: Optional[list[ModeCollection]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collections = mode_collections

    class Attributes(Mode.Attributes):
        mode_collection_count: Optional[int] = Field(
            None, description="", alias="modeCollectionCount"
        )
        mode_collections: Optional[list[ModeCollection]] = Field(
            None, description="", alias="modeCollections"
        )  # relationship

    attributes: "ModeWorkspace.Attributes" = Field(
        default_factory=lambda: ModeWorkspace.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeCollection(Mode):
    """Description"""

    type_name: str = Field("ModeCollection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeCollection":
            raise ValueError("must be ModeCollection")
        return v

    def __setattr__(self, name, value):
        if name in ModeCollection._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "mode_collection_type",
        "mode_collection_state",
        "mode_workspace",
        "mode_reports",
    ]

    @property
    def mode_collection_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_collection_type

    @mode_collection_type.setter
    def mode_collection_type(self, mode_collection_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_type = mode_collection_type

    @property
    def mode_collection_state(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.mode_collection_state
        )

    @mode_collection_state.setter
    def mode_collection_state(self, mode_collection_state: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_state = mode_collection_state

    @property
    def mode_workspace(self) -> Optional[ModeWorkspace]:
        return None if self.attributes is None else self.attributes.mode_workspace

    @mode_workspace.setter
    def mode_workspace(self, mode_workspace: Optional[ModeWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_workspace = mode_workspace

    @property
    def mode_reports(self) -> Optional[list[ModeReport]]:
        return None if self.attributes is None else self.attributes.mode_reports

    @mode_reports.setter
    def mode_reports(self, mode_reports: Optional[list[ModeReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_reports = mode_reports

    class Attributes(Mode.Attributes):
        mode_collection_type: Optional[str] = Field(
            None, description="", alias="modeCollectionType"
        )
        mode_collection_state: Optional[str] = Field(
            None, description="", alias="modeCollectionState"
        )
        mode_workspace: Optional[ModeWorkspace] = Field(
            None, description="", alias="modeWorkspace"
        )  # relationship
        mode_reports: Optional[list[ModeReport]] = Field(
            None, description="", alias="modeReports"
        )  # relationship

    attributes: "ModeCollection.Attributes" = Field(
        default_factory=lambda: ModeCollection.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaDatasetColumn(Sigma):
    """Description"""

    type_name: str = Field("SigmaDatasetColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDatasetColumn":
            raise ValueError("must be SigmaDatasetColumn")
        return v

    def __setattr__(self, name, value):
        if name in SigmaDatasetColumn._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "sigma_dataset_qualified_name",
        "sigma_dataset_name",
        "sigma_dataset",
    ]

    @property
    def sigma_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_dataset_qualified_name
        )

    @sigma_dataset_qualified_name.setter
    def sigma_dataset_qualified_name(self, sigma_dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset_qualified_name = sigma_dataset_qualified_name

    @property
    def sigma_dataset_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sigma_dataset_name

    @sigma_dataset_name.setter
    def sigma_dataset_name(self, sigma_dataset_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset_name = sigma_dataset_name

    @property
    def sigma_dataset(self) -> Optional[SigmaDataset]:
        return None if self.attributes is None else self.attributes.sigma_dataset

    @sigma_dataset.setter
    def sigma_dataset(self, sigma_dataset: Optional[SigmaDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset = sigma_dataset

    class Attributes(Sigma.Attributes):
        sigma_dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="sigmaDatasetQualifiedName"
        )
        sigma_dataset_name: Optional[str] = Field(
            None, description="", alias="sigmaDatasetName"
        )
        sigma_dataset: Optional[SigmaDataset] = Field(
            None, description="", alias="sigmaDataset"
        )  # relationship

    attributes: "SigmaDatasetColumn.Attributes" = Field(
        default_factory=lambda: SigmaDatasetColumn.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaDataset(Sigma):
    """Description"""

    type_name: str = Field("SigmaDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDataset":
            raise ValueError("must be SigmaDataset")
        return v

    def __setattr__(self, name, value):
        if name in SigmaDataset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "sigma_dataset_column_count",
        "sigma_dataset_columns",
    ]

    @property
    def sigma_dataset_column_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_dataset_column_count
        )

    @sigma_dataset_column_count.setter
    def sigma_dataset_column_count(self, sigma_dataset_column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset_column_count = sigma_dataset_column_count

    @property
    def sigma_dataset_columns(self) -> Optional[list[SigmaDatasetColumn]]:
        return (
            None if self.attributes is None else self.attributes.sigma_dataset_columns
        )

    @sigma_dataset_columns.setter
    def sigma_dataset_columns(
        self, sigma_dataset_columns: Optional[list[SigmaDatasetColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset_columns = sigma_dataset_columns

    class Attributes(Sigma.Attributes):
        sigma_dataset_column_count: Optional[int] = Field(
            None, description="", alias="sigmaDatasetColumnCount"
        )
        sigma_dataset_columns: Optional[list[SigmaDatasetColumn]] = Field(
            None, description="", alias="sigmaDatasetColumns"
        )  # relationship

    attributes: "SigmaDataset.Attributes" = Field(
        default_factory=lambda: SigmaDataset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaWorkbook(Sigma):
    """Description"""

    type_name: str = Field("SigmaWorkbook", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaWorkbook":
            raise ValueError("must be SigmaWorkbook")
        return v

    def __setattr__(self, name, value):
        if name in SigmaWorkbook._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "sigma_page_count",
        "sigma_pages",
    ]

    @property
    def sigma_page_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.sigma_page_count

    @sigma_page_count.setter
    def sigma_page_count(self, sigma_page_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_page_count = sigma_page_count

    @property
    def sigma_pages(self) -> Optional[list[SigmaPage]]:
        return None if self.attributes is None else self.attributes.sigma_pages

    @sigma_pages.setter
    def sigma_pages(self, sigma_pages: Optional[list[SigmaPage]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_pages = sigma_pages

    class Attributes(Sigma.Attributes):
        sigma_page_count: Optional[int] = Field(
            None, description="", alias="sigmaPageCount"
        )
        sigma_pages: Optional[list[SigmaPage]] = Field(
            None, description="", alias="sigmaPages"
        )  # relationship

    attributes: "SigmaWorkbook.Attributes" = Field(
        default_factory=lambda: SigmaWorkbook.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaDataElementField(Sigma):
    """Description"""

    type_name: str = Field("SigmaDataElementField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDataElementField":
            raise ValueError("must be SigmaDataElementField")
        return v

    def __setattr__(self, name, value):
        if name in SigmaDataElementField._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "sigma_data_element_field_is_hidden",
        "sigma_data_element_field_formula",
        "sigma_data_element",
    ]

    @property
    def sigma_data_element_field_is_hidden(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_field_is_hidden
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_field_formula
        )

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
    def sigma_data_element(self) -> Optional[SigmaDataElement]:
        return None if self.attributes is None else self.attributes.sigma_data_element

    @sigma_data_element.setter
    def sigma_data_element(self, sigma_data_element: Optional[SigmaDataElement]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element = sigma_data_element

    class Attributes(Sigma.Attributes):
        sigma_data_element_field_is_hidden: Optional[bool] = Field(
            None, description="", alias="sigmaDataElementFieldIsHidden"
        )
        sigma_data_element_field_formula: Optional[str] = Field(
            None, description="", alias="sigmaDataElementFieldFormula"
        )
        sigma_data_element: Optional[SigmaDataElement] = Field(
            None, description="", alias="sigmaDataElement"
        )  # relationship

    attributes: "SigmaDataElementField.Attributes" = Field(
        default_factory=lambda: SigmaDataElementField.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaPage(Sigma):
    """Description"""

    type_name: str = Field("SigmaPage", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaPage":
            raise ValueError("must be SigmaPage")
        return v

    def __setattr__(self, name, value):
        if name in SigmaPage._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "sigma_data_element_count",
        "sigma_data_elements",
        "sigma_workbook",
    ]

    @property
    def sigma_data_element_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_count
        )

    @sigma_data_element_count.setter
    def sigma_data_element_count(self, sigma_data_element_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_count = sigma_data_element_count

    @property
    def sigma_data_elements(self) -> Optional[list[SigmaDataElement]]:
        return None if self.attributes is None else self.attributes.sigma_data_elements

    @sigma_data_elements.setter
    def sigma_data_elements(
        self, sigma_data_elements: Optional[list[SigmaDataElement]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_elements = sigma_data_elements

    @property
    def sigma_workbook(self) -> Optional[SigmaWorkbook]:
        return None if self.attributes is None else self.attributes.sigma_workbook

    @sigma_workbook.setter
    def sigma_workbook(self, sigma_workbook: Optional[SigmaWorkbook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_workbook = sigma_workbook

    class Attributes(Sigma.Attributes):
        sigma_data_element_count: Optional[int] = Field(
            None, description="", alias="sigmaDataElementCount"
        )
        sigma_data_elements: Optional[list[SigmaDataElement]] = Field(
            None, description="", alias="sigmaDataElements"
        )  # relationship
        sigma_workbook: Optional[SigmaWorkbook] = Field(
            None, description="", alias="sigmaWorkbook"
        )  # relationship

    attributes: "SigmaPage.Attributes" = Field(
        default_factory=lambda: SigmaPage.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaDataElement(Sigma):
    """Description"""

    type_name: str = Field("SigmaDataElement", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDataElement":
            raise ValueError("must be SigmaDataElement")
        return v

    def __setattr__(self, name, value):
        if name in SigmaDataElement._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "sigma_data_element_query",
        "sigma_data_element_type",
        "sigma_data_element_field_count",
        "sigma_page",
        "sigma_data_element_fields",
    ]

    @property
    def sigma_data_element_query(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_query
        )

    @sigma_data_element_query.setter
    def sigma_data_element_query(self, sigma_data_element_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_query = sigma_data_element_query

    @property
    def sigma_data_element_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sigma_data_element_type
        )

    @sigma_data_element_type.setter
    def sigma_data_element_type(self, sigma_data_element_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_type = sigma_data_element_type

    @property
    def sigma_data_element_field_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_field_count
        )

    @sigma_data_element_field_count.setter
    def sigma_data_element_field_count(
        self, sigma_data_element_field_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_field_count = sigma_data_element_field_count

    @property
    def sigma_page(self) -> Optional[SigmaPage]:
        return None if self.attributes is None else self.attributes.sigma_page

    @sigma_page.setter
    def sigma_page(self, sigma_page: Optional[SigmaPage]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_page = sigma_page

    @property
    def sigma_data_element_fields(self) -> Optional[list[SigmaDataElementField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_fields
        )

    @sigma_data_element_fields.setter
    def sigma_data_element_fields(
        self, sigma_data_element_fields: Optional[list[SigmaDataElementField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_fields = sigma_data_element_fields

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
        sigma_page: Optional[SigmaPage] = Field(
            None, description="", alias="sigmaPage"
        )  # relationship
        sigma_data_element_fields: Optional[list[SigmaDataElementField]] = Field(
            None, description="", alias="sigmaDataElementFields"
        )  # relationship

    attributes: "SigmaDataElement.Attributes" = Field(
        default_factory=lambda: SigmaDataElement.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauWorkbook(Tableau):
    """Description"""

    type_name: str = Field("TableauWorkbook", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauWorkbook":
            raise ValueError("must be TableauWorkbook")
        return v

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
        "project",
        "dashboards",
        "worksheets",
        "datasources",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.top_level_project_name
        )

    @top_level_project_name.setter
    def top_level_project_name(self, top_level_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_name = top_level_project_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

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
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def project(self) -> Optional[TableauProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[TableauProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def dashboards(self) -> Optional[list[TableauDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[list[TableauDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    @property
    def worksheets(self) -> Optional[list[TableauWorksheet]]:
        return None if self.attributes is None else self.attributes.worksheets

    @worksheets.setter
    def worksheets(self, worksheets: Optional[list[TableauWorksheet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.worksheets = worksheets

    @property
    def datasources(self) -> Optional[list[TableauDatasource]]:
        return None if self.attributes is None else self.attributes.datasources

    @datasources.setter
    def datasources(self, datasources: Optional[list[TableauDatasource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasources = datasources

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
        project: Optional[TableauProject] = Field(
            None, description="", alias="project"
        )  # relationship
        dashboards: Optional[list[TableauDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship
        worksheets: Optional[list[TableauWorksheet]] = Field(
            None, description="", alias="worksheets"
        )  # relationship
        datasources: Optional[list[TableauDatasource]] = Field(
            None, description="", alias="datasources"
        )  # relationship

    attributes: "TableauWorkbook.Attributes" = Field(
        default_factory=lambda: TableauWorkbook.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauDatasourceField(Tableau):
    """Description"""

    type_name: str = Field("TableauDatasourceField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauDatasourceField":
            raise ValueError("must be TableauDatasourceField")
        return v

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
        "worksheets",
        "datasource",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

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
        return (
            None if self.attributes is None else self.attributes.workbook_qualified_name
        )

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def datasource_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.datasource_qualified_name
        )

    @datasource_qualified_name.setter
    def datasource_qualified_name(self, datasource_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource_qualified_name = datasource_qualified_name

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def fully_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.fully_qualified_name

    @fully_qualified_name.setter
    def fully_qualified_name(self, fully_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fully_qualified_name = fully_qualified_name

    @property
    def tableau_datasource_field_data_category(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_datasource_field_data_category
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_datasource_field_role
        )

    @tableau_datasource_field_role.setter
    def tableau_datasource_field_role(
        self, tableau_datasource_field_role: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_datasource_field_role = tableau_datasource_field_role

    @property
    def tableau_datasource_field_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_datasource_field_data_type
        )

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
        return None if self.attributes is None else self.attributes.upstream_tables

    @upstream_tables.setter
    def upstream_tables(self, upstream_tables: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_tables = upstream_tables

    @property
    def tableau_datasource_field_formula(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_datasource_field_formula
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_datasource_field_bin_size
        )

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
        return None if self.attributes is None else self.attributes.upstream_columns

    @upstream_columns.setter
    def upstream_columns(self, upstream_columns: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_columns = upstream_columns

    @property
    def upstream_fields(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_fields

    @upstream_fields.setter
    def upstream_fields(self, upstream_fields: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_fields = upstream_fields

    @property
    def datasource_field_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.datasource_field_type
        )

    @datasource_field_type.setter
    def datasource_field_type(self, datasource_field_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource_field_type = datasource_field_type

    @property
    def worksheets(self) -> Optional[list[TableauWorksheet]]:
        return None if self.attributes is None else self.attributes.worksheets

    @worksheets.setter
    def worksheets(self, worksheets: Optional[list[TableauWorksheet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.worksheets = worksheets

    @property
    def datasource(self) -> Optional[TableauDatasource]:
        return None if self.attributes is None else self.attributes.datasource

    @datasource.setter
    def datasource(self, datasource: Optional[TableauDatasource]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource = datasource

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
        worksheets: Optional[list[TableauWorksheet]] = Field(
            None, description="", alias="worksheets"
        )  # relationship
        datasource: Optional[TableauDatasource] = Field(
            None, description="", alias="datasource"
        )  # relationship

    attributes: "TableauDatasourceField.Attributes" = Field(
        default_factory=lambda: TableauDatasourceField.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauCalculatedField(Tableau):
    """Description"""

    type_name: str = Field("TableauCalculatedField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauCalculatedField":
            raise ValueError("must be TableauCalculatedField")
        return v

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
        "worksheets",
        "datasource",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

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
        return (
            None if self.attributes is None else self.attributes.workbook_qualified_name
        )

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def datasource_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.datasource_qualified_name
        )

    @datasource_qualified_name.setter
    def datasource_qualified_name(self, datasource_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource_qualified_name = datasource_qualified_name

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def data_category(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_category

    @data_category.setter
    def data_category(self, data_category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_category = data_category

    @property
    def role(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.role

    @role.setter
    def role(self, role: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.role = role

    @property
    def tableau_data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.tableau_data_type

    @tableau_data_type.setter
    def tableau_data_type(self, tableau_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_data_type = tableau_data_type

    @property
    def formula(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.formula

    @formula.setter
    def formula(self, formula: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.formula = formula

    @property
    def upstream_fields(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_fields

    @upstream_fields.setter
    def upstream_fields(self, upstream_fields: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_fields = upstream_fields

    @property
    def worksheets(self) -> Optional[list[TableauWorksheet]]:
        return None if self.attributes is None else self.attributes.worksheets

    @worksheets.setter
    def worksheets(self, worksheets: Optional[list[TableauWorksheet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.worksheets = worksheets

    @property
    def datasource(self) -> Optional[TableauDatasource]:
        return None if self.attributes is None else self.attributes.datasource

    @datasource.setter
    def datasource(self, datasource: Optional[TableauDatasource]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource = datasource

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
        worksheets: Optional[list[TableauWorksheet]] = Field(
            None, description="", alias="worksheets"
        )  # relationship
        datasource: Optional[TableauDatasource] = Field(
            None, description="", alias="datasource"
        )  # relationship

    attributes: "TableauCalculatedField.Attributes" = Field(
        default_factory=lambda: TableauCalculatedField.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauProject(Tableau):
    """Description"""

    type_name: str = Field("TableauProject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauProject":
            raise ValueError("must be TableauProject")
        return v

    def __setattr__(self, name, value):
        if name in TableauProject._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "top_level_project_qualified_name",
        "is_top_level_project",
        "project_hierarchy",
        "parent_project",
        "workbooks",
        "site",
        "datasources",
        "flows",
        "child_projects",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

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
        return None if self.attributes is None else self.attributes.is_top_level_project

    @is_top_level_project.setter
    def is_top_level_project(self, is_top_level_project: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_top_level_project = is_top_level_project

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def parent_project(self) -> Optional[TableauProject]:
        return None if self.attributes is None else self.attributes.parent_project

    @parent_project.setter
    def parent_project(self, parent_project: Optional[TableauProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_project = parent_project

    @property
    def workbooks(self) -> Optional[list[TableauWorkbook]]:
        return None if self.attributes is None else self.attributes.workbooks

    @workbooks.setter
    def workbooks(self, workbooks: Optional[list[TableauWorkbook]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbooks = workbooks

    @property
    def site(self) -> Optional[TableauSite]:
        return None if self.attributes is None else self.attributes.site

    @site.setter
    def site(self, site: Optional[TableauSite]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site = site

    @property
    def datasources(self) -> Optional[list[TableauDatasource]]:
        return None if self.attributes is None else self.attributes.datasources

    @datasources.setter
    def datasources(self, datasources: Optional[list[TableauDatasource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasources = datasources

    @property
    def flows(self) -> Optional[list[TableauFlow]]:
        return None if self.attributes is None else self.attributes.flows

    @flows.setter
    def flows(self, flows: Optional[list[TableauFlow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flows = flows

    @property
    def child_projects(self) -> Optional[list[TableauProject]]:
        return None if self.attributes is None else self.attributes.child_projects

    @child_projects.setter
    def child_projects(self, child_projects: Optional[list[TableauProject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.child_projects = child_projects

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
        parent_project: Optional[TableauProject] = Field(
            None, description="", alias="parentProject"
        )  # relationship
        workbooks: Optional[list[TableauWorkbook]] = Field(
            None, description="", alias="workbooks"
        )  # relationship
        site: Optional[TableauSite] = Field(
            None, description="", alias="site"
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

    attributes: "TableauProject.Attributes" = Field(
        default_factory=lambda: TableauProject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauMetric(Tableau):
    """Description"""

    type_name: str = Field("TableauMetric", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauMetric":
            raise ValueError("must be TableauMetric")
        return v

    def __setattr__(self, name, value):
        if name in TableauMetric._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_qualified_name",
        "project_hierarchy",
        "project",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

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
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def project(self) -> Optional[TableauProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[TableauProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

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
        project: Optional[TableauProject] = Field(
            None, description="", alias="project"
        )  # relationship

    attributes: "TableauMetric.Attributes" = Field(
        default_factory=lambda: TableauMetric.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauSite(Tableau):
    """Description"""

    type_name: str = Field("TableauSite", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauSite":
            raise ValueError("must be TableauSite")
        return v

    def __setattr__(self, name, value):
        if name in TableauSite._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "projects",
    ]

    @property
    def projects(self) -> Optional[list[TableauProject]]:
        return None if self.attributes is None else self.attributes.projects

    @projects.setter
    def projects(self, projects: Optional[list[TableauProject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.projects = projects

    class Attributes(Tableau.Attributes):
        projects: Optional[list[TableauProject]] = Field(
            None, description="", alias="projects"
        )  # relationship

    attributes: "TableauSite.Attributes" = Field(
        default_factory=lambda: TableauSite.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauDatasource(Tableau):
    """Description"""

    type_name: str = Field("TableauDatasource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauDatasource":
            raise ValueError("must be TableauDatasource")
        return v

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
        "workbook",
        "project",
        "fields",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

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
        return (
            None if self.attributes is None else self.attributes.workbook_qualified_name
        )

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def is_published(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_published

    @is_published.setter
    def is_published(self, is_published: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_published = is_published

    @property
    def has_extracts(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.has_extracts

    @has_extracts.setter
    def has_extracts(self, has_extracts: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.has_extracts = has_extracts

    @property
    def is_certified(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_certified

    @is_certified.setter
    def is_certified(self, is_certified: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_certified = is_certified

    @property
    def certifier(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.certifier

    @certifier.setter
    def certifier(self, certifier: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certifier = certifier

    @property
    def certification_note(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.certification_note

    @certification_note.setter
    def certification_note(self, certification_note: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certification_note = certification_note

    @property
    def certifier_display_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.certifier_display_name
        )

    @certifier_display_name.setter
    def certifier_display_name(self, certifier_display_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certifier_display_name = certifier_display_name

    @property
    def upstream_tables(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_tables

    @upstream_tables.setter
    def upstream_tables(self, upstream_tables: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_tables = upstream_tables

    @property
    def upstream_datasources(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_datasources

    @upstream_datasources.setter
    def upstream_datasources(
        self, upstream_datasources: Optional[list[dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_datasources = upstream_datasources

    @property
    def workbook(self) -> Optional[TableauWorkbook]:
        return None if self.attributes is None else self.attributes.workbook

    @workbook.setter
    def workbook(self, workbook: Optional[TableauWorkbook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook = workbook

    @property
    def project(self) -> Optional[TableauProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[TableauProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def fields(self) -> Optional[list[TableauDatasourceField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[list[TableauDatasourceField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

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
        project: Optional[TableauProject] = Field(
            None, description="", alias="project"
        )  # relationship
        fields: Optional[list[TableauDatasourceField]] = Field(
            None, description="", alias="fields"
        )  # relationship

    attributes: "TableauDatasource.Attributes" = Field(
        default_factory=lambda: TableauDatasource.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauDashboard(Tableau):
    """Description"""

    type_name: str = Field("TableauDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauDashboard":
            raise ValueError("must be TableauDashboard")
        return v

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
        "workbook",
        "worksheets",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def workbook_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.workbook_qualified_name
        )

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

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
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def workbook(self) -> Optional[TableauWorkbook]:
        return None if self.attributes is None else self.attributes.workbook

    @workbook.setter
    def workbook(self, workbook: Optional[TableauWorkbook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook = workbook

    @property
    def worksheets(self) -> Optional[list[TableauWorksheet]]:
        return None if self.attributes is None else self.attributes.worksheets

    @worksheets.setter
    def worksheets(self, worksheets: Optional[list[TableauWorksheet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.worksheets = worksheets

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
        worksheets: Optional[list[TableauWorksheet]] = Field(
            None, description="", alias="worksheets"
        )  # relationship

    attributes: "TableauDashboard.Attributes" = Field(
        default_factory=lambda: TableauDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauFlow(Tableau):
    """Description"""

    type_name: str = Field("TableauFlow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauFlow":
            raise ValueError("must be TableauFlow")
        return v

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
        "project",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

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
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def input_fields(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.input_fields

    @input_fields.setter
    def input_fields(self, input_fields: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_fields = input_fields

    @property
    def output_fields(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.output_fields

    @output_fields.setter
    def output_fields(self, output_fields: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_fields = output_fields

    @property
    def output_steps(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.output_steps

    @output_steps.setter
    def output_steps(self, output_steps: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_steps = output_steps

    @property
    def project(self) -> Optional[TableauProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[TableauProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

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
        project: Optional[TableauProject] = Field(
            None, description="", alias="project"
        )  # relationship

    attributes: "TableauFlow.Attributes" = Field(
        default_factory=lambda: TableauFlow.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauWorksheet(Tableau):
    """Description"""

    type_name: str = Field("TableauWorksheet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauWorksheet":
            raise ValueError("must be TableauWorksheet")
        return v

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
        "workbook",
        "datasource_fields",
        "calculated_fields",
        "dashboards",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

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
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def workbook_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.workbook_qualified_name
        )

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def workbook(self) -> Optional[TableauWorkbook]:
        return None if self.attributes is None else self.attributes.workbook

    @workbook.setter
    def workbook(self, workbook: Optional[TableauWorkbook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook = workbook

    @property
    def datasource_fields(self) -> Optional[list[TableauDatasourceField]]:
        return None if self.attributes is None else self.attributes.datasource_fields

    @datasource_fields.setter
    def datasource_fields(
        self, datasource_fields: Optional[list[TableauDatasourceField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource_fields = datasource_fields

    @property
    def calculated_fields(self) -> Optional[list[TableauCalculatedField]]:
        return None if self.attributes is None else self.attributes.calculated_fields

    @calculated_fields.setter
    def calculated_fields(
        self, calculated_fields: Optional[list[TableauCalculatedField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculated_fields = calculated_fields

    @property
    def dashboards(self) -> Optional[list[TableauDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[list[TableauDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

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
        datasource_fields: Optional[list[TableauDatasourceField]] = Field(
            None, description="", alias="datasourceFields"
        )  # relationship
        calculated_fields: Optional[list[TableauCalculatedField]] = Field(
            None, description="", alias="calculatedFields"
        )  # relationship
        dashboards: Optional[list[TableauDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship

    attributes: "TableauWorksheet.Attributes" = Field(
        default_factory=lambda: TableauWorksheet.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerLook(Looker):
    """Description"""

    type_name: str = Field("LookerLook", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerLook":
            raise ValueError("must be LookerLook")
        return v

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
        "query",
        "folder",
        "tile",
        "model",
        "dashboard",
    ]

    @property
    def folder_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.folder_name

    @folder_name.setter
    def folder_name(self, folder_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.folder_name = folder_name

    @property
    def source_user_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_user_id

    @source_user_id.setter
    def source_user_id(self, source_user_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_user_id = source_user_id

    @property
    def source_view_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_view_count

    @source_view_count.setter
    def source_view_count(self, source_view_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_view_count = source_view_count

    @property
    def sourcelast_updater_id(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.sourcelast_updater_id
        )

    @sourcelast_updater_id.setter
    def sourcelast_updater_id(self, sourcelast_updater_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sourcelast_updater_id = sourcelast_updater_id

    @property
    def source_last_accessed_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.source_last_accessed_at
        )

    @source_last_accessed_at.setter
    def source_last_accessed_at(self, source_last_accessed_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_last_accessed_at = source_last_accessed_at

    @property
    def source_last_viewed_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.source_last_viewed_at
        )

    @source_last_viewed_at.setter
    def source_last_viewed_at(self, source_last_viewed_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_last_viewed_at = source_last_viewed_at

    @property
    def source_content_metadata_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_content_metadata_id
        )

    @source_content_metadata_id.setter
    def source_content_metadata_id(self, source_content_metadata_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_content_metadata_id = source_content_metadata_id

    @property
    def source_query_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_query_id

    @source_query_id.setter
    def source_query_id(self, source_query_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_query_id = source_query_id

    @property
    def model_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_name

    @model_name.setter
    def model_name(self, model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_name = model_name

    @property
    def query(self) -> Optional[LookerQuery]:
        return None if self.attributes is None else self.attributes.query

    @query.setter
    def query(self, query: Optional[LookerQuery]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query = query

    @property
    def folder(self) -> Optional[LookerFolder]:
        return None if self.attributes is None else self.attributes.folder

    @folder.setter
    def folder(self, folder: Optional[LookerFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.folder = folder

    @property
    def tile(self) -> Optional[LookerTile]:
        return None if self.attributes is None else self.attributes.tile

    @tile.setter
    def tile(self, tile: Optional[LookerTile]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tile = tile

    @property
    def model(self) -> Optional[LookerModel]:
        return None if self.attributes is None else self.attributes.model

    @model.setter
    def model(self, model: Optional[LookerModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model = model

    @property
    def dashboard(self) -> Optional[LookerDashboard]:
        return None if self.attributes is None else self.attributes.dashboard

    @dashboard.setter
    def dashboard(self, dashboard: Optional[LookerDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard = dashboard

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
        query: Optional[LookerQuery] = Field(
            None, description="", alias="query"
        )  # relationship
        folder: Optional[LookerFolder] = Field(
            None, description="", alias="folder"
        )  # relationship
        tile: Optional[LookerTile] = Field(
            None, description="", alias="tile"
        )  # relationship
        model: Optional[LookerModel] = Field(
            None, description="", alias="model"
        )  # relationship
        dashboard: Optional[LookerDashboard] = Field(
            None, description="", alias="dashboard"
        )  # relationship

    attributes: "LookerLook.Attributes" = Field(
        default_factory=lambda: LookerLook.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerDashboard(Looker):
    """Description"""

    type_name: str = Field("LookerDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerDashboard":
            raise ValueError("must be LookerDashboard")
        return v

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
        "tiles",
        "looks",
        "folder",
    ]

    @property
    def folder_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.folder_name

    @folder_name.setter
    def folder_name(self, folder_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.folder_name = folder_name

    @property
    def source_user_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_user_id

    @source_user_id.setter
    def source_user_id(self, source_user_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_user_id = source_user_id

    @property
    def source_view_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_view_count

    @source_view_count.setter
    def source_view_count(self, source_view_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_view_count = source_view_count

    @property
    def source_metadata_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_metadata_id

    @source_metadata_id.setter
    def source_metadata_id(self, source_metadata_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_metadata_id = source_metadata_id

    @property
    def sourcelast_updater_id(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.sourcelast_updater_id
        )

    @sourcelast_updater_id.setter
    def sourcelast_updater_id(self, sourcelast_updater_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sourcelast_updater_id = sourcelast_updater_id

    @property
    def source_last_accessed_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.source_last_accessed_at
        )

    @source_last_accessed_at.setter
    def source_last_accessed_at(self, source_last_accessed_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_last_accessed_at = source_last_accessed_at

    @property
    def source_last_viewed_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.source_last_viewed_at
        )

    @source_last_viewed_at.setter
    def source_last_viewed_at(self, source_last_viewed_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_last_viewed_at = source_last_viewed_at

    @property
    def tiles(self) -> Optional[list[LookerTile]]:
        return None if self.attributes is None else self.attributes.tiles

    @tiles.setter
    def tiles(self, tiles: Optional[list[LookerTile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tiles = tiles

    @property
    def looks(self) -> Optional[list[LookerLook]]:
        return None if self.attributes is None else self.attributes.looks

    @looks.setter
    def looks(self, looks: Optional[list[LookerLook]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looks = looks

    @property
    def folder(self) -> Optional[LookerFolder]:
        return None if self.attributes is None else self.attributes.folder

    @folder.setter
    def folder(self, folder: Optional[LookerFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.folder = folder

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
        tiles: Optional[list[LookerTile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        looks: Optional[list[LookerLook]] = Field(
            None, description="", alias="looks"
        )  # relationship
        folder: Optional[LookerFolder] = Field(
            None, description="", alias="folder"
        )  # relationship

    attributes: "LookerDashboard.Attributes" = Field(
        default_factory=lambda: LookerDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerFolder(Looker):
    """Description"""

    type_name: str = Field("LookerFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerFolder":
            raise ValueError("must be LookerFolder")
        return v

    def __setattr__(self, name, value):
        if name in LookerFolder._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "source_content_metadata_id",
        "source_creator_id",
        "source_child_count",
        "source_parent_i_d",
        "looks",
        "dashboards",
    ]

    @property
    def source_content_metadata_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_content_metadata_id
        )

    @source_content_metadata_id.setter
    def source_content_metadata_id(self, source_content_metadata_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_content_metadata_id = source_content_metadata_id

    @property
    def source_creator_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_creator_id

    @source_creator_id.setter
    def source_creator_id(self, source_creator_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_creator_id = source_creator_id

    @property
    def source_child_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_child_count

    @source_child_count.setter
    def source_child_count(self, source_child_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_child_count = source_child_count

    @property
    def source_parent_i_d(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_parent_i_d

    @source_parent_i_d.setter
    def source_parent_i_d(self, source_parent_i_d: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_parent_i_d = source_parent_i_d

    @property
    def looks(self) -> Optional[list[LookerLook]]:
        return None if self.attributes is None else self.attributes.looks

    @looks.setter
    def looks(self, looks: Optional[list[LookerLook]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looks = looks

    @property
    def dashboards(self) -> Optional[list[LookerDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[list[LookerDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

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
        looks: Optional[list[LookerLook]] = Field(
            None, description="", alias="looks"
        )  # relationship
        dashboards: Optional[list[LookerDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship

    attributes: "LookerFolder.Attributes" = Field(
        default_factory=lambda: LookerFolder.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerTile(Looker):
    """Description"""

    type_name: str = Field("LookerTile", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerTile":
            raise ValueError("must be LookerTile")
        return v

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
        "query",
        "look",
        "dashboard",
    ]

    @property
    def lookml_link_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.lookml_link_id

    @lookml_link_id.setter
    def lookml_link_id(self, lookml_link_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.lookml_link_id = lookml_link_id

    @property
    def merge_result_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.merge_result_id

    @merge_result_id.setter
    def merge_result_id(self, merge_result_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.merge_result_id = merge_result_id

    @property
    def note_text(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.note_text

    @note_text.setter
    def note_text(self, note_text: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.note_text = note_text

    @property
    def query_i_d(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_i_d

    @query_i_d.setter
    def query_i_d(self, query_i_d: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_i_d = query_i_d

    @property
    def result_maker_i_d(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.result_maker_i_d

    @result_maker_i_d.setter
    def result_maker_i_d(self, result_maker_i_d: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.result_maker_i_d = result_maker_i_d

    @property
    def subtitle_text(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.subtitle_text

    @subtitle_text.setter
    def subtitle_text(self, subtitle_text: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.subtitle_text = subtitle_text

    @property
    def look_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.look_id

    @look_id.setter
    def look_id(self, look_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.look_id = look_id

    @property
    def query(self) -> Optional[LookerQuery]:
        return None if self.attributes is None else self.attributes.query

    @query.setter
    def query(self, query: Optional[LookerQuery]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query = query

    @property
    def look(self) -> Optional[LookerLook]:
        return None if self.attributes is None else self.attributes.look

    @look.setter
    def look(self, look: Optional[LookerLook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.look = look

    @property
    def dashboard(self) -> Optional[LookerDashboard]:
        return None if self.attributes is None else self.attributes.dashboard

    @dashboard.setter
    def dashboard(self, dashboard: Optional[LookerDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard = dashboard

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
        query: Optional[LookerQuery] = Field(
            None, description="", alias="query"
        )  # relationship
        look: Optional[LookerLook] = Field(
            None, description="", alias="look"
        )  # relationship
        dashboard: Optional[LookerDashboard] = Field(
            None, description="", alias="dashboard"
        )  # relationship

    attributes: "LookerTile.Attributes" = Field(
        default_factory=lambda: LookerTile.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerModel(Looker):
    """Description"""

    type_name: str = Field("LookerModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerModel":
            raise ValueError("must be LookerModel")
        return v

    def __setattr__(self, name, value):
        if name in LookerModel._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "project_name",
        "explores",
        "project",
        "look",
        "queries",
        "fields",
    ]

    @property
    def project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.project_name

    @project_name.setter
    def project_name(self, project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_name = project_name

    @property
    def explores(self) -> Optional[list[LookerExplore]]:
        return None if self.attributes is None else self.attributes.explores

    @explores.setter
    def explores(self, explores: Optional[list[LookerExplore]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.explores = explores

    @property
    def project(self) -> Optional[LookerProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[LookerProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def look(self) -> Optional[LookerLook]:
        return None if self.attributes is None else self.attributes.look

    @look.setter
    def look(self, look: Optional[LookerLook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.look = look

    @property
    def queries(self) -> Optional[list[LookerQuery]]:
        return None if self.attributes is None else self.attributes.queries

    @queries.setter
    def queries(self, queries: Optional[list[LookerQuery]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.queries = queries

    @property
    def fields(self) -> Optional[list[LookerField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[list[LookerField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    class Attributes(Looker.Attributes):
        project_name: Optional[str] = Field(None, description="", alias="projectName")
        explores: Optional[list[LookerExplore]] = Field(
            None, description="", alias="explores"
        )  # relationship
        project: Optional[LookerProject] = Field(
            None, description="", alias="project"
        )  # relationship
        look: Optional[LookerLook] = Field(
            None, description="", alias="look"
        )  # relationship
        queries: Optional[list[LookerQuery]] = Field(
            None, description="", alias="queries"
        )  # relationship
        fields: Optional[list[LookerField]] = Field(
            None, description="", alias="fields"
        )  # relationship

    attributes: "LookerModel.Attributes" = Field(
        default_factory=lambda: LookerModel.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerExplore(Looker):
    """Description"""

    type_name: str = Field("LookerExplore", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerExplore":
            raise ValueError("must be LookerExplore")
        return v

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
        "project",
        "model",
        "fields",
    ]

    @property
    def project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.project_name

    @project_name.setter
    def project_name(self, project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_name = project_name

    @property
    def model_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_name

    @model_name.setter
    def model_name(self, model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_name = model_name

    @property
    def source_connection_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.source_connection_name
        )

    @source_connection_name.setter
    def source_connection_name(self, source_connection_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_connection_name = source_connection_name

    @property
    def view_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.view_name

    @view_name.setter
    def view_name(self, view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_name = view_name

    @property
    def sql_table_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sql_table_name

    @sql_table_name.setter
    def sql_table_name(self, sql_table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_table_name = sql_table_name

    @property
    def project(self) -> Optional[LookerProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[LookerProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def model(self) -> Optional[LookerModel]:
        return None if self.attributes is None else self.attributes.model

    @model.setter
    def model(self, model: Optional[LookerModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model = model

    @property
    def fields(self) -> Optional[list[LookerField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[list[LookerField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

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
        project: Optional[LookerProject] = Field(
            None, description="", alias="project"
        )  # relationship
        model: Optional[LookerModel] = Field(
            None, description="", alias="model"
        )  # relationship
        fields: Optional[list[LookerField]] = Field(
            None, description="", alias="fields"
        )  # relationship

    attributes: "LookerExplore.Attributes" = Field(
        default_factory=lambda: LookerExplore.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerProject(Looker):
    """Description"""

    type_name: str = Field("LookerProject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerProject":
            raise ValueError("must be LookerProject")
        return v

    def __setattr__(self, name, value):
        if name in LookerProject._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "models",
        "explores",
        "fields",
        "views",
    ]

    @property
    def models(self) -> Optional[list[LookerModel]]:
        return None if self.attributes is None else self.attributes.models

    @models.setter
    def models(self, models: Optional[list[LookerModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.models = models

    @property
    def explores(self) -> Optional[list[LookerExplore]]:
        return None if self.attributes is None else self.attributes.explores

    @explores.setter
    def explores(self, explores: Optional[list[LookerExplore]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.explores = explores

    @property
    def fields(self) -> Optional[list[LookerField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[list[LookerField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    @property
    def views(self) -> Optional[list[LookerView]]:
        return None if self.attributes is None else self.attributes.views

    @views.setter
    def views(self, views: Optional[list[LookerView]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.views = views

    class Attributes(Looker.Attributes):
        models: Optional[list[LookerModel]] = Field(
            None, description="", alias="models"
        )  # relationship
        explores: Optional[list[LookerExplore]] = Field(
            None, description="", alias="explores"
        )  # relationship
        fields: Optional[list[LookerField]] = Field(
            None, description="", alias="fields"
        )  # relationship
        views: Optional[list[LookerView]] = Field(
            None, description="", alias="views"
        )  # relationship

    attributes: "LookerProject.Attributes" = Field(
        default_factory=lambda: LookerProject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerQuery(Looker):
    """Description"""

    type_name: str = Field("LookerQuery", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerQuery":
            raise ValueError("must be LookerQuery")
        return v

    def __setattr__(self, name, value):
        if name in LookerQuery._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "source_definition",
        "source_definition_database",
        "source_definition_schema",
        "fields",
        "tiles",
        "looks",
        "model",
    ]

    @property
    def source_definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_definition

    @source_definition.setter
    def source_definition(self, source_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_definition = source_definition

    @property
    def source_definition_database(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_definition_database
        )

    @source_definition_database.setter
    def source_definition_database(self, source_definition_database: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_definition_database = source_definition_database

    @property
    def source_definition_schema(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_definition_schema
        )

    @source_definition_schema.setter
    def source_definition_schema(self, source_definition_schema: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_definition_schema = source_definition_schema

    @property
    def fields(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    @property
    def tiles(self) -> Optional[list[LookerTile]]:
        return None if self.attributes is None else self.attributes.tiles

    @tiles.setter
    def tiles(self, tiles: Optional[list[LookerTile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tiles = tiles

    @property
    def looks(self) -> Optional[list[LookerLook]]:
        return None if self.attributes is None else self.attributes.looks

    @looks.setter
    def looks(self, looks: Optional[list[LookerLook]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looks = looks

    @property
    def model(self) -> Optional[LookerModel]:
        return None if self.attributes is None else self.attributes.model

    @model.setter
    def model(self, model: Optional[LookerModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model = model

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
        tiles: Optional[list[LookerTile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        looks: Optional[list[LookerLook]] = Field(
            None, description="", alias="looks"
        )  # relationship
        model: Optional[LookerModel] = Field(
            None, description="", alias="model"
        )  # relationship

    attributes: "LookerQuery.Attributes" = Field(
        default_factory=lambda: LookerQuery.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerField(Looker):
    """Description"""

    type_name: str = Field("LookerField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerField":
            raise ValueError("must be LookerField")
        return v

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
        "explore",
        "project",
        "view",
        "model",
    ]

    @property
    def project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.project_name

    @project_name.setter
    def project_name(self, project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_name = project_name

    @property
    def looker_explore_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.looker_explore_qualified_name
        )

    @looker_explore_qualified_name.setter
    def looker_explore_qualified_name(
        self, looker_explore_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_explore_qualified_name = looker_explore_qualified_name

    @property
    def looker_view_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.looker_view_qualified_name
        )

    @looker_view_qualified_name.setter
    def looker_view_qualified_name(self, looker_view_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_view_qualified_name = looker_view_qualified_name

    @property
    def model_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_name

    @model_name.setter
    def model_name(self, model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_name = model_name

    @property
    def source_definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_definition

    @source_definition.setter
    def source_definition(self, source_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_definition = source_definition

    @property
    def looker_field_data_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.looker_field_data_type
        )

    @looker_field_data_type.setter
    def looker_field_data_type(self, looker_field_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_field_data_type = looker_field_data_type

    @property
    def looker_times_used(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.looker_times_used

    @looker_times_used.setter
    def looker_times_used(self, looker_times_used: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_times_used = looker_times_used

    @property
    def explore(self) -> Optional[LookerExplore]:
        return None if self.attributes is None else self.attributes.explore

    @explore.setter
    def explore(self, explore: Optional[LookerExplore]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.explore = explore

    @property
    def project(self) -> Optional[LookerProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[LookerProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def view(self) -> Optional[LookerView]:
        return None if self.attributes is None else self.attributes.view

    @view.setter
    def view(self, view: Optional[LookerView]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view = view

    @property
    def model(self) -> Optional[LookerModel]:
        return None if self.attributes is None else self.attributes.model

    @model.setter
    def model(self, model: Optional[LookerModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model = model

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
        explore: Optional[LookerExplore] = Field(
            None, description="", alias="explore"
        )  # relationship
        project: Optional[LookerProject] = Field(
            None, description="", alias="project"
        )  # relationship
        view: Optional[LookerView] = Field(
            None, description="", alias="view"
        )  # relationship
        model: Optional[LookerModel] = Field(
            None, description="", alias="model"
        )  # relationship

    attributes: "LookerField.Attributes" = Field(
        default_factory=lambda: LookerField.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerView(Looker):
    """Description"""

    type_name: str = Field("LookerView", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerView":
            raise ValueError("must be LookerView")
        return v

    def __setattr__(self, name, value):
        if name in LookerView._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "project_name",
        "project",
        "fields",
    ]

    @property
    def project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.project_name

    @project_name.setter
    def project_name(self, project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_name = project_name

    @property
    def project(self) -> Optional[LookerProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[LookerProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def fields(self) -> Optional[list[LookerField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[list[LookerField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    class Attributes(Looker.Attributes):
        project_name: Optional[str] = Field(None, description="", alias="projectName")
        project: Optional[LookerProject] = Field(
            None, description="", alias="project"
        )  # relationship
        fields: Optional[list[LookerField]] = Field(
            None, description="", alias="fields"
        )  # relationship

    attributes: "LookerView.Attributes" = Field(
        default_factory=lambda: LookerView.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class RedashDashboard(Redash):
    """Description"""

    type_name: str = Field("RedashDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "RedashDashboard":
            raise ValueError("must be RedashDashboard")
        return v

    def __setattr__(self, name, value):
        if name in RedashDashboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "redash_dashboard_widget_count",
    ]

    @property
    def redash_dashboard_widget_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.redash_dashboard_widget_count
        )

    @redash_dashboard_widget_count.setter
    def redash_dashboard_widget_count(
        self, redash_dashboard_widget_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_dashboard_widget_count = redash_dashboard_widget_count

    class Attributes(Redash.Attributes):
        redash_dashboard_widget_count: Optional[int] = Field(
            None, description="", alias="redashDashboardWidgetCount"
        )

    attributes: "RedashDashboard.Attributes" = Field(
        default_factory=lambda: RedashDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class RedashQuery(Redash):
    """Description"""

    type_name: str = Field("RedashQuery", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "RedashQuery":
            raise ValueError("must be RedashQuery")
        return v

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
        "redash_visualizations",
    ]

    @property
    def redash_query_s_q_l(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.redash_query_s_q_l

    @redash_query_s_q_l.setter
    def redash_query_s_q_l(self, redash_query_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_s_q_l = redash_query_s_q_l

    @property
    def redash_query_parameters(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.redash_query_parameters
        )

    @redash_query_parameters.setter
    def redash_query_parameters(self, redash_query_parameters: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_parameters = redash_query_parameters

    @property
    def redash_query_schedule(self) -> Optional[dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.redash_query_schedule
        )

    @redash_query_schedule.setter
    def redash_query_schedule(self, redash_query_schedule: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_schedule = redash_query_schedule

    @property
    def redash_query_last_execution_runtime(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.redash_query_last_execution_runtime
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.redash_query_last_executed_at
        )

    @redash_query_last_executed_at.setter
    def redash_query_last_executed_at(
        self, redash_query_last_executed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_last_executed_at = redash_query_last_executed_at

    @property
    def redash_query_schedule_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.redash_query_schedule_humanized
        )

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
    def redash_visualizations(self) -> Optional[list[RedashVisualization]]:
        return (
            None if self.attributes is None else self.attributes.redash_visualizations
        )

    @redash_visualizations.setter
    def redash_visualizations(
        self, redash_visualizations: Optional[list[RedashVisualization]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_visualizations = redash_visualizations

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
        redash_visualizations: Optional[list[RedashVisualization]] = Field(
            None, description="", alias="redashVisualizations"
        )  # relationship

    attributes: "RedashQuery.Attributes" = Field(
        default_factory=lambda: RedashQuery.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class RedashVisualization(Redash):
    """Description"""

    type_name: str = Field("RedashVisualization", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "RedashVisualization":
            raise ValueError("must be RedashVisualization")
        return v

    def __setattr__(self, name, value):
        if name in RedashVisualization._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "redash_visualization_type",
        "redash_query_name",
        "redash_query_qualified_name",
        "redash_query",
    ]

    @property
    def redash_visualization_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.redash_visualization_type
        )

    @redash_visualization_type.setter
    def redash_visualization_type(self, redash_visualization_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_visualization_type = redash_visualization_type

    @property
    def redash_query_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.redash_query_name

    @redash_query_name.setter
    def redash_query_name(self, redash_query_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_name = redash_query_name

    @property
    def redash_query_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.redash_query_qualified_name
        )

    @redash_query_qualified_name.setter
    def redash_query_qualified_name(self, redash_query_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_qualified_name = redash_query_qualified_name

    @property
    def redash_query(self) -> Optional[RedashQuery]:
        return None if self.attributes is None else self.attributes.redash_query

    @redash_query.setter
    def redash_query(self, redash_query: Optional[RedashQuery]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query = redash_query

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
        redash_query: Optional[RedashQuery] = Field(
            None, description="", alias="redashQuery"
        )  # relationship

    attributes: "RedashVisualization.Attributes" = Field(
        default_factory=lambda: RedashVisualization.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MetabaseQuestion(Metabase):
    """Description"""

    type_name: str = Field("MetabaseQuestion", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MetabaseQuestion":
            raise ValueError("must be MetabaseQuestion")
        return v

    def __setattr__(self, name, value):
        if name in MetabaseQuestion._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "metabase_dashboard_count",
        "metabase_query_type",
        "metabase_query",
        "metabase_dashboards",
        "metabase_collection",
    ]

    @property
    def metabase_dashboard_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.metabase_dashboard_count
        )

    @metabase_dashboard_count.setter
    def metabase_dashboard_count(self, metabase_dashboard_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_dashboard_count = metabase_dashboard_count

    @property
    def metabase_query_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_query_type

    @metabase_query_type.setter
    def metabase_query_type(self, metabase_query_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_query_type = metabase_query_type

    @property
    def metabase_query(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_query

    @metabase_query.setter
    def metabase_query(self, metabase_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_query = metabase_query

    @property
    def metabase_dashboards(self) -> Optional[list[MetabaseDashboard]]:
        return None if self.attributes is None else self.attributes.metabase_dashboards

    @metabase_dashboards.setter
    def metabase_dashboards(
        self, metabase_dashboards: Optional[list[MetabaseDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_dashboards = metabase_dashboards

    @property
    def metabase_collection(self) -> Optional[MetabaseCollection]:
        return None if self.attributes is None else self.attributes.metabase_collection

    @metabase_collection.setter
    def metabase_collection(self, metabase_collection: Optional[MetabaseCollection]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_collection = metabase_collection

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
        metabase_dashboards: Optional[list[MetabaseDashboard]] = Field(
            None, description="", alias="metabaseDashboards"
        )  # relationship
        metabase_collection: Optional[MetabaseCollection] = Field(
            None, description="", alias="metabaseCollection"
        )  # relationship

    attributes: "MetabaseQuestion.Attributes" = Field(
        default_factory=lambda: MetabaseQuestion.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MetabaseCollection(Metabase):
    """Description"""

    type_name: str = Field("MetabaseCollection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MetabaseCollection":
            raise ValueError("must be MetabaseCollection")
        return v

    def __setattr__(self, name, value):
        if name in MetabaseCollection._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "metabase_slug",
        "metabase_color",
        "metabase_namespace",
        "metabase_is_personal_collection",
        "metabase_dashboards",
        "metabase_questions",
    ]

    @property
    def metabase_slug(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_slug

    @metabase_slug.setter
    def metabase_slug(self, metabase_slug: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_slug = metabase_slug

    @property
    def metabase_color(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_color

    @metabase_color.setter
    def metabase_color(self, metabase_color: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_color = metabase_color

    @property
    def metabase_namespace(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_namespace

    @metabase_namespace.setter
    def metabase_namespace(self, metabase_namespace: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_namespace = metabase_namespace

    @property
    def metabase_is_personal_collection(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.metabase_is_personal_collection
        )

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
    def metabase_dashboards(self) -> Optional[list[MetabaseDashboard]]:
        return None if self.attributes is None else self.attributes.metabase_dashboards

    @metabase_dashboards.setter
    def metabase_dashboards(
        self, metabase_dashboards: Optional[list[MetabaseDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_dashboards = metabase_dashboards

    @property
    def metabase_questions(self) -> Optional[list[MetabaseQuestion]]:
        return None if self.attributes is None else self.attributes.metabase_questions

    @metabase_questions.setter
    def metabase_questions(self, metabase_questions: Optional[list[MetabaseQuestion]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_questions = metabase_questions

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
        metabase_dashboards: Optional[list[MetabaseDashboard]] = Field(
            None, description="", alias="metabaseDashboards"
        )  # relationship
        metabase_questions: Optional[list[MetabaseQuestion]] = Field(
            None, description="", alias="metabaseQuestions"
        )  # relationship

    attributes: "MetabaseCollection.Attributes" = Field(
        default_factory=lambda: MetabaseCollection.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MetabaseDashboard(Metabase):
    """Description"""

    type_name: str = Field("MetabaseDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MetabaseDashboard":
            raise ValueError("must be MetabaseDashboard")
        return v

    def __setattr__(self, name, value):
        if name in MetabaseDashboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "metabase_question_count",
        "metabase_questions",
        "metabase_collection",
    ]

    @property
    def metabase_question_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.metabase_question_count
        )

    @metabase_question_count.setter
    def metabase_question_count(self, metabase_question_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_question_count = metabase_question_count

    @property
    def metabase_questions(self) -> Optional[list[MetabaseQuestion]]:
        return None if self.attributes is None else self.attributes.metabase_questions

    @metabase_questions.setter
    def metabase_questions(self, metabase_questions: Optional[list[MetabaseQuestion]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_questions = metabase_questions

    @property
    def metabase_collection(self) -> Optional[MetabaseCollection]:
        return None if self.attributes is None else self.attributes.metabase_collection

    @metabase_collection.setter
    def metabase_collection(self, metabase_collection: Optional[MetabaseCollection]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_collection = metabase_collection

    class Attributes(Metabase.Attributes):
        metabase_question_count: Optional[int] = Field(
            None, description="", alias="metabaseQuestionCount"
        )
        metabase_questions: Optional[list[MetabaseQuestion]] = Field(
            None, description="", alias="metabaseQuestions"
        )  # relationship
        metabase_collection: Optional[MetabaseCollection] = Field(
            None, description="", alias="metabaseCollection"
        )  # relationship

    attributes: "MetabaseDashboard.Attributes" = Field(
        default_factory=lambda: MetabaseDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightFolder(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightFolder":
            raise ValueError("must be QuickSightFolder")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightFolder._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_folder_type",
        "quick_sight_folder_hierarchy",
        "quick_sight_dashboards",
        "quick_sight_analyses",
        "quick_sight_datasets",
    ]

    @property
    def quick_sight_folder_type(self) -> Optional[QuickSightFolderType]:
        return (
            None if self.attributes is None else self.attributes.quick_sight_folder_type
        )

    @quick_sight_folder_type.setter
    def quick_sight_folder_type(
        self, quick_sight_folder_type: Optional[QuickSightFolderType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_folder_type = quick_sight_folder_type

    @property
    def quick_sight_folder_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_folder_hierarchy
        )

    @quick_sight_folder_hierarchy.setter
    def quick_sight_folder_hierarchy(
        self, quick_sight_folder_hierarchy: Optional[list[dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_folder_hierarchy = quick_sight_folder_hierarchy

    @property
    def quick_sight_dashboards(self) -> Optional[list[QuickSightDashboard]]:
        return (
            None if self.attributes is None else self.attributes.quick_sight_dashboards
        )

    @quick_sight_dashboards.setter
    def quick_sight_dashboards(
        self, quick_sight_dashboards: Optional[list[QuickSightDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboards = quick_sight_dashboards

    @property
    def quick_sight_analyses(self) -> Optional[list[QuickSightAnalysis]]:
        return None if self.attributes is None else self.attributes.quick_sight_analyses

    @quick_sight_analyses.setter
    def quick_sight_analyses(
        self, quick_sight_analyses: Optional[list[QuickSightAnalysis]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analyses = quick_sight_analyses

    @property
    def quick_sight_datasets(self) -> Optional[list[QuickSightDataset]]:
        return None if self.attributes is None else self.attributes.quick_sight_datasets

    @quick_sight_datasets.setter
    def quick_sight_datasets(
        self, quick_sight_datasets: Optional[list[QuickSightDataset]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_datasets = quick_sight_datasets

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
        quick_sight_analyses: Optional[list[QuickSightAnalysis]] = Field(
            None, description="", alias="quickSightAnalyses"
        )  # relationship
        quick_sight_datasets: Optional[list[QuickSightDataset]] = Field(
            None, description="", alias="quickSightDatasets"
        )  # relationship

    attributes: "QuickSightFolder.Attributes" = Field(
        default_factory=lambda: QuickSightFolder.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightDashboardVisual(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightDashboardVisual", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDashboardVisual":
            raise ValueError("must be QuickSightDashboardVisual")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightDashboardVisual._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_dashboard_qualified_name",
        "quick_sight_dashboard",
    ]

    @property
    def quick_sight_dashboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_qualified_name
        )

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
    def quick_sight_dashboard(self) -> Optional[QuickSightDashboard]:
        return (
            None if self.attributes is None else self.attributes.quick_sight_dashboard
        )

    @quick_sight_dashboard.setter
    def quick_sight_dashboard(
        self, quick_sight_dashboard: Optional[QuickSightDashboard]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard = quick_sight_dashboard

    class Attributes(QuickSight.Attributes):
        quick_sight_dashboard_qualified_name: Optional[str] = Field(
            None, description="", alias="quickSightDashboardQualifiedName"
        )
        quick_sight_dashboard: Optional[QuickSightDashboard] = Field(
            None, description="", alias="quickSightDashboard"
        )  # relationship

    attributes: "QuickSightDashboardVisual.Attributes" = Field(
        default_factory=lambda: QuickSightDashboardVisual.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightAnalysisVisual(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightAnalysisVisual", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightAnalysisVisual":
            raise ValueError("must be QuickSightAnalysisVisual")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightAnalysisVisual._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_analysis_qualified_name",
        "quick_sight_analysis",
    ]

    @property
    def quick_sight_analysis_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_qualified_name
        )

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
    def quick_sight_analysis(self) -> Optional[QuickSightAnalysis]:
        return None if self.attributes is None else self.attributes.quick_sight_analysis

    @quick_sight_analysis.setter
    def quick_sight_analysis(self, quick_sight_analysis: Optional[QuickSightAnalysis]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis = quick_sight_analysis

    class Attributes(QuickSight.Attributes):
        quick_sight_analysis_qualified_name: Optional[str] = Field(
            None, description="", alias="quickSightAnalysisQualifiedName"
        )
        quick_sight_analysis: Optional[QuickSightAnalysis] = Field(
            None, description="", alias="quickSightAnalysis"
        )  # relationship

    attributes: "QuickSightAnalysisVisual.Attributes" = Field(
        default_factory=lambda: QuickSightAnalysisVisual.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightDatasetField(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightDatasetField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDatasetField":
            raise ValueError("must be QuickSightDatasetField")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightDatasetField._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_dataset_field_type",
        "quick_sight_dataset_qualified_name",
        "quick_sight_dataset",
    ]

    @property
    def quick_sight_dataset_field_type(self) -> Optional[QuickSightDatasetFieldType]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_field_type
        )

    @quick_sight_dataset_field_type.setter
    def quick_sight_dataset_field_type(
        self, quick_sight_dataset_field_type: Optional[QuickSightDatasetFieldType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_field_type = quick_sight_dataset_field_type

    @property
    def quick_sight_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_qualified_name
        )

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
    def quick_sight_dataset(self) -> Optional[QuickSightDataset]:
        return None if self.attributes is None else self.attributes.quick_sight_dataset

    @quick_sight_dataset.setter
    def quick_sight_dataset(self, quick_sight_dataset: Optional[QuickSightDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset = quick_sight_dataset

    class Attributes(QuickSight.Attributes):
        quick_sight_dataset_field_type: Optional[QuickSightDatasetFieldType] = Field(
            None, description="", alias="quickSightDatasetFieldType"
        )
        quick_sight_dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="quickSightDatasetQualifiedName"
        )
        quick_sight_dataset: Optional[QuickSightDataset] = Field(
            None, description="", alias="quickSightDataset"
        )  # relationship

    attributes: "QuickSightDatasetField.Attributes" = Field(
        default_factory=lambda: QuickSightDatasetField.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightAnalysis(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightAnalysis", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightAnalysis":
            raise ValueError("must be QuickSightAnalysis")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightAnalysis._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_analysis_status",
        "quick_sight_analysis_calculated_fields",
        "quick_sight_analysis_parameter_declarations",
        "quick_sight_analysis_filter_groups",
        "quick_sight_analysis_visuals",
        "quick_sight_analysis_folders",
    ]

    @property
    def quick_sight_analysis_status(self) -> Optional[QuickSightAnalysisStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_status
        )

    @quick_sight_analysis_status.setter
    def quick_sight_analysis_status(
        self, quick_sight_analysis_status: Optional[QuickSightAnalysisStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_status = quick_sight_analysis_status

    @property
    def quick_sight_analysis_calculated_fields(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_calculated_fields
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_parameter_declarations
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_filter_groups
        )

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
    def quick_sight_analysis_visuals(self) -> Optional[list[QuickSightAnalysisVisual]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_visuals
        )

    @quick_sight_analysis_visuals.setter
    def quick_sight_analysis_visuals(
        self, quick_sight_analysis_visuals: Optional[list[QuickSightAnalysisVisual]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_visuals = quick_sight_analysis_visuals

    @property
    def quick_sight_analysis_folders(self) -> Optional[list[QuickSightFolder]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_folders
        )

    @quick_sight_analysis_folders.setter
    def quick_sight_analysis_folders(
        self, quick_sight_analysis_folders: Optional[list[QuickSightFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_folders = quick_sight_analysis_folders

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
        quick_sight_analysis_visuals: Optional[list[QuickSightAnalysisVisual]] = Field(
            None, description="", alias="quickSightAnalysisVisuals"
        )  # relationship
        quick_sight_analysis_folders: Optional[list[QuickSightFolder]] = Field(
            None, description="", alias="quickSightAnalysisFolders"
        )  # relationship

    attributes: "QuickSightAnalysis.Attributes" = Field(
        default_factory=lambda: QuickSightAnalysis.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightDashboard(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDashboard":
            raise ValueError("must be QuickSightDashboard")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightDashboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_dashboard_published_version_number",
        "quick_sight_dashboard_last_published_time",
        "quick_sight_dashboard_folders",
        "quick_sight_dashboard_visuals",
    ]

    @property
    def quick_sight_dashboard_published_version_number(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_published_version_number
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_last_published_time
        )

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
    def quick_sight_dashboard_folders(self) -> Optional[list[QuickSightFolder]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_folders
        )

    @quick_sight_dashboard_folders.setter
    def quick_sight_dashboard_folders(
        self, quick_sight_dashboard_folders: Optional[list[QuickSightFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_folders = quick_sight_dashboard_folders

    @property
    def quick_sight_dashboard_visuals(
        self,
    ) -> Optional[list[QuickSightDashboardVisual]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_visuals
        )

    @quick_sight_dashboard_visuals.setter
    def quick_sight_dashboard_visuals(
        self, quick_sight_dashboard_visuals: Optional[list[QuickSightDashboardVisual]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_visuals = quick_sight_dashboard_visuals

    class Attributes(QuickSight.Attributes):
        quick_sight_dashboard_published_version_number: Optional[int] = Field(
            None, description="", alias="quickSightDashboardPublishedVersionNumber"
        )
        quick_sight_dashboard_last_published_time: Optional[datetime] = Field(
            None, description="", alias="quickSightDashboardLastPublishedTime"
        )
        quick_sight_dashboard_folders: Optional[list[QuickSightFolder]] = Field(
            None, description="", alias="quickSightDashboardFolders"
        )  # relationship
        quick_sight_dashboard_visuals: Optional[
            list[QuickSightDashboardVisual]
        ] = Field(
            None, description="", alias="quickSightDashboardVisuals"
        )  # relationship

    attributes: "QuickSightDashboard.Attributes" = Field(
        default_factory=lambda: QuickSightDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightDataset(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDataset":
            raise ValueError("must be QuickSightDataset")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightDataset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "quick_sight_dataset_import_mode",
        "quick_sight_dataset_column_count",
        "quick_sight_dataset_folders",
        "quick_sight_dataset_fields",
    ]

    @property
    def quick_sight_dataset_import_mode(self) -> Optional[QuickSightDatasetImportMode]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_import_mode
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_column_count
        )

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
    def quick_sight_dataset_folders(self) -> Optional[list[QuickSightFolder]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_folders
        )

    @quick_sight_dataset_folders.setter
    def quick_sight_dataset_folders(
        self, quick_sight_dataset_folders: Optional[list[QuickSightFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_folders = quick_sight_dataset_folders

    @property
    def quick_sight_dataset_fields(self) -> Optional[list[QuickSightDatasetField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_fields
        )

    @quick_sight_dataset_fields.setter
    def quick_sight_dataset_fields(
        self, quick_sight_dataset_fields: Optional[list[QuickSightDatasetField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_fields = quick_sight_dataset_fields

    class Attributes(QuickSight.Attributes):
        quick_sight_dataset_import_mode: Optional[QuickSightDatasetImportMode] = Field(
            None, description="", alias="quickSightDatasetImportMode"
        )
        quick_sight_dataset_column_count: Optional[int] = Field(
            None, description="", alias="quickSightDatasetColumnCount"
        )
        quick_sight_dataset_folders: Optional[list[QuickSightFolder]] = Field(
            None, description="", alias="quickSightDatasetFolders"
        )  # relationship
        quick_sight_dataset_fields: Optional[list[QuickSightDatasetField]] = Field(
            None, description="", alias="quickSightDatasetFields"
        )  # relationship

    attributes: "QuickSightDataset.Attributes" = Field(
        default_factory=lambda: QuickSightDataset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ThoughtspotLiveboard(Thoughtspot):
    """Description"""

    type_name: str = Field("ThoughtspotLiveboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotLiveboard":
            raise ValueError("must be ThoughtspotLiveboard")
        return v

    def __setattr__(self, name, value):
        if name in ThoughtspotLiveboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "thoughtspot_dashlets",
    ]

    @property
    def thoughtspot_dashlets(self) -> Optional[list[ThoughtspotDashlet]]:
        return None if self.attributes is None else self.attributes.thoughtspot_dashlets

    @thoughtspot_dashlets.setter
    def thoughtspot_dashlets(
        self, thoughtspot_dashlets: Optional[list[ThoughtspotDashlet]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_dashlets = thoughtspot_dashlets

    class Attributes(Thoughtspot.Attributes):
        thoughtspot_dashlets: Optional[list[ThoughtspotDashlet]] = Field(
            None, description="", alias="thoughtspotDashlets"
        )  # relationship

    attributes: "ThoughtspotLiveboard.Attributes" = Field(
        default_factory=lambda: ThoughtspotLiveboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ThoughtspotDashlet(Thoughtspot):
    """Description"""

    type_name: str = Field("ThoughtspotDashlet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotDashlet":
            raise ValueError("must be ThoughtspotDashlet")
        return v

    def __setattr__(self, name, value):
        if name in ThoughtspotDashlet._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "thoughtspot_liveboard_name",
        "thoughtspot_liveboard_qualified_name",
        "thoughtspot_liveboard",
    ]

    @property
    def thoughtspot_liveboard_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.thoughtspot_liveboard_name
        )

    @thoughtspot_liveboard_name.setter
    def thoughtspot_liveboard_name(self, thoughtspot_liveboard_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_liveboard_name = thoughtspot_liveboard_name

    @property
    def thoughtspot_liveboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.thoughtspot_liveboard_qualified_name
        )

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
    def thoughtspot_liveboard(self) -> Optional[ThoughtspotLiveboard]:
        return (
            None if self.attributes is None else self.attributes.thoughtspot_liveboard
        )

    @thoughtspot_liveboard.setter
    def thoughtspot_liveboard(
        self, thoughtspot_liveboard: Optional[ThoughtspotLiveboard]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_liveboard = thoughtspot_liveboard

    class Attributes(Thoughtspot.Attributes):
        thoughtspot_liveboard_name: Optional[str] = Field(
            None, description="", alias="thoughtspotLiveboardName"
        )
        thoughtspot_liveboard_qualified_name: Optional[str] = Field(
            None, description="", alias="thoughtspotLiveboardQualifiedName"
        )
        thoughtspot_liveboard: Optional[ThoughtspotLiveboard] = Field(
            None, description="", alias="thoughtspotLiveboard"
        )  # relationship

    attributes: "ThoughtspotDashlet.Attributes" = Field(
        default_factory=lambda: ThoughtspotDashlet.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ThoughtspotAnswer(Thoughtspot):
    """Description"""

    type_name: str = Field("ThoughtspotAnswer", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotAnswer":
            raise ValueError("must be ThoughtspotAnswer")
        return v

    def __setattr__(self, name, value):
        if name in ThoughtspotAnswer._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


class PowerBIReport(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIReport":
            raise ValueError("must be PowerBIReport")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIReport._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "dataset_qualified_name",
        "web_url",
        "page_count",
        "workspace",
        "tiles",
        "pages",
        "dataset",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def dataset_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dataset_qualified_name
        )

    @dataset_qualified_name.setter
    def dataset_qualified_name(self, dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_qualified_name = dataset_qualified_name

    @property
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def page_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.page_count

    @page_count.setter
    def page_count(self, page_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.page_count = page_count

    @property
    def workspace(self) -> Optional[PowerBIWorkspace]:
        return None if self.attributes is None else self.attributes.workspace

    @workspace.setter
    def workspace(self, workspace: Optional[PowerBIWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace = workspace

    @property
    def tiles(self) -> Optional[list[PowerBITile]]:
        return None if self.attributes is None else self.attributes.tiles

    @tiles.setter
    def tiles(self, tiles: Optional[list[PowerBITile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tiles = tiles

    @property
    def pages(self) -> Optional[list[PowerBIPage]]:
        return None if self.attributes is None else self.attributes.pages

    @pages.setter
    def pages(self, pages: Optional[list[PowerBIPage]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.pages = pages

    @property
    def dataset(self) -> Optional[PowerBIDataset]:
        return None if self.attributes is None else self.attributes.dataset

    @dataset.setter
    def dataset(self, dataset: Optional[PowerBIDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset = dataset

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="datasetQualifiedName"
        )
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        page_count: Optional[int] = Field(None, description="", alias="pageCount")
        workspace: Optional[PowerBIWorkspace] = Field(
            None, description="", alias="workspace"
        )  # relationship
        tiles: Optional[list[PowerBITile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        pages: Optional[list[PowerBIPage]] = Field(
            None, description="", alias="pages"
        )  # relationship
        dataset: Optional[PowerBIDataset] = Field(
            None, description="", alias="dataset"
        )  # relationship

    attributes: "PowerBIReport.Attributes" = Field(
        default_factory=lambda: PowerBIReport.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIMeasure(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIMeasure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIMeasure":
            raise ValueError("must be PowerBIMeasure")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIMeasure._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "dataset_qualified_name",
        "power_b_i_measure_expression",
        "power_b_i_is_external_measure",
        "table",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def dataset_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dataset_qualified_name
        )

    @dataset_qualified_name.setter
    def dataset_qualified_name(self, dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_qualified_name = dataset_qualified_name

    @property
    def power_b_i_measure_expression(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_measure_expression
        )

    @power_b_i_measure_expression.setter
    def power_b_i_measure_expression(self, power_b_i_measure_expression: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_measure_expression = power_b_i_measure_expression

    @property
    def power_b_i_is_external_measure(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_is_external_measure
        )

    @power_b_i_is_external_measure.setter
    def power_b_i_is_external_measure(
        self, power_b_i_is_external_measure: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_is_external_measure = power_b_i_is_external_measure

    @property
    def table(self) -> Optional[PowerBITable]:
        return None if self.attributes is None else self.attributes.table

    @table.setter
    def table(self, table: Optional[PowerBITable]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table = table

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
        table: Optional[PowerBITable] = Field(
            None, description="", alias="table"
        )  # relationship

    attributes: "PowerBIMeasure.Attributes" = Field(
        default_factory=lambda: PowerBIMeasure.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIColumn(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIColumn":
            raise ValueError("must be PowerBIColumn")
        return v

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
        "table",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def dataset_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dataset_qualified_name
        )

    @dataset_qualified_name.setter
    def dataset_qualified_name(self, dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_qualified_name = dataset_qualified_name

    @property
    def power_b_i_column_data_category(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_column_data_category
        )

    @power_b_i_column_data_category.setter
    def power_b_i_column_data_category(
        self, power_b_i_column_data_category: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_column_data_category = power_b_i_column_data_category

    @property
    def power_b_i_column_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_column_data_type
        )

    @power_b_i_column_data_type.setter
    def power_b_i_column_data_type(self, power_b_i_column_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_column_data_type = power_b_i_column_data_type

    @property
    def power_b_i_sort_by_column(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_sort_by_column
        )

    @power_b_i_sort_by_column.setter
    def power_b_i_sort_by_column(self, power_b_i_sort_by_column: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_sort_by_column = power_b_i_sort_by_column

    @property
    def power_b_i_column_summarize_by(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_column_summarize_by
        )

    @power_b_i_column_summarize_by.setter
    def power_b_i_column_summarize_by(
        self, power_b_i_column_summarize_by: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_column_summarize_by = power_b_i_column_summarize_by

    @property
    def table(self) -> Optional[PowerBITable]:
        return None if self.attributes is None else self.attributes.table

    @table.setter
    def table(self, table: Optional[PowerBITable]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table = table

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
        table: Optional[PowerBITable] = Field(
            None, description="", alias="table"
        )  # relationship

    attributes: "PowerBIColumn.Attributes" = Field(
        default_factory=lambda: PowerBIColumn.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBITable(PowerBI):
    """Description"""

    type_name: str = Field("PowerBITable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBITable":
            raise ValueError("must be PowerBITable")
        return v

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
        "measures",
        "columns",
        "dataset",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def dataset_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dataset_qualified_name
        )

    @dataset_qualified_name.setter
    def dataset_qualified_name(self, dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_qualified_name = dataset_qualified_name

    @property
    def power_b_i_table_source_expressions(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_table_source_expressions
        )

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
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_table_column_count
        )

    @power_b_i_table_column_count.setter
    def power_b_i_table_column_count(self, power_b_i_table_column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_table_column_count = power_b_i_table_column_count

    @property
    def power_b_i_table_measure_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_table_measure_count
        )

    @power_b_i_table_measure_count.setter
    def power_b_i_table_measure_count(
        self, power_b_i_table_measure_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_table_measure_count = power_b_i_table_measure_count

    @property
    def measures(self) -> Optional[list[PowerBIMeasure]]:
        return None if self.attributes is None else self.attributes.measures

    @measures.setter
    def measures(self, measures: Optional[list[PowerBIMeasure]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.measures = measures

    @property
    def columns(self) -> Optional[list[PowerBIColumn]]:
        return None if self.attributes is None else self.attributes.columns

    @columns.setter
    def columns(self, columns: Optional[list[PowerBIColumn]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.columns = columns

    @property
    def dataset(self) -> Optional[PowerBIDataset]:
        return None if self.attributes is None else self.attributes.dataset

    @dataset.setter
    def dataset(self, dataset: Optional[PowerBIDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset = dataset

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
        measures: Optional[list[PowerBIMeasure]] = Field(
            None, description="", alias="measures"
        )  # relationship
        columns: Optional[list[PowerBIColumn]] = Field(
            None, description="", alias="columns"
        )  # relationship
        dataset: Optional[PowerBIDataset] = Field(
            None, description="", alias="dataset"
        )  # relationship

    attributes: "PowerBITable.Attributes" = Field(
        default_factory=lambda: PowerBITable.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBITile(PowerBI):
    """Description"""

    type_name: str = Field("PowerBITile", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBITile":
            raise ValueError("must be PowerBITile")
        return v

    def __setattr__(self, name, value):
        if name in PowerBITile._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "dashboard_qualified_name",
        "report",
        "dataset",
        "dashboard",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def dashboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dashboard_qualified_name
        )

    @dashboard_qualified_name.setter
    def dashboard_qualified_name(self, dashboard_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard_qualified_name = dashboard_qualified_name

    @property
    def report(self) -> Optional[PowerBIReport]:
        return None if self.attributes is None else self.attributes.report

    @report.setter
    def report(self, report: Optional[PowerBIReport]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report = report

    @property
    def dataset(self) -> Optional[PowerBIDataset]:
        return None if self.attributes is None else self.attributes.dataset

    @dataset.setter
    def dataset(self, dataset: Optional[PowerBIDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset = dataset

    @property
    def dashboard(self) -> Optional[PowerBIDashboard]:
        return None if self.attributes is None else self.attributes.dashboard

    @dashboard.setter
    def dashboard(self, dashboard: Optional[PowerBIDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard = dashboard

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        dashboard_qualified_name: Optional[str] = Field(
            None, description="", alias="dashboardQualifiedName"
        )
        report: Optional[PowerBIReport] = Field(
            None, description="", alias="report"
        )  # relationship
        dataset: Optional[PowerBIDataset] = Field(
            None, description="", alias="dataset"
        )  # relationship
        dashboard: Optional[PowerBIDashboard] = Field(
            None, description="", alias="dashboard"
        )  # relationship

    attributes: "PowerBITile.Attributes" = Field(
        default_factory=lambda: PowerBITile.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIDatasource(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIDatasource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDatasource":
            raise ValueError("must be PowerBIDatasource")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDatasource._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "connection_details",
        "datasets",
    ]

    @property
    def connection_details(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.connection_details

    @connection_details.setter
    def connection_details(self, connection_details: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connection_details = connection_details

    @property
    def datasets(self) -> Optional[list[PowerBIDataset]]:
        return None if self.attributes is None else self.attributes.datasets

    @datasets.setter
    def datasets(self, datasets: Optional[list[PowerBIDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasets = datasets

    class Attributes(PowerBI.Attributes):
        connection_details: Optional[dict[str, str]] = Field(
            None, description="", alias="connectionDetails"
        )
        datasets: Optional[list[PowerBIDataset]] = Field(
            None, description="", alias="datasets"
        )  # relationship

    attributes: "PowerBIDatasource.Attributes" = Field(
        default_factory=lambda: PowerBIDatasource.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIWorkspace(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIWorkspace":
            raise ValueError("must be PowerBIWorkspace")
        return v

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
        "reports",
        "datasets",
        "dashboards",
        "dataflows",
    ]

    @property
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def report_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.report_count

    @report_count.setter
    def report_count(self, report_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_count = report_count

    @property
    def dashboard_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.dashboard_count

    @dashboard_count.setter
    def dashboard_count(self, dashboard_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard_count = dashboard_count

    @property
    def dataset_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.dataset_count

    @dataset_count.setter
    def dataset_count(self, dataset_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_count = dataset_count

    @property
    def dataflow_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.dataflow_count

    @dataflow_count.setter
    def dataflow_count(self, dataflow_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataflow_count = dataflow_count

    @property
    def reports(self) -> Optional[list[PowerBIReport]]:
        return None if self.attributes is None else self.attributes.reports

    @reports.setter
    def reports(self, reports: Optional[list[PowerBIReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reports = reports

    @property
    def datasets(self) -> Optional[list[PowerBIDataset]]:
        return None if self.attributes is None else self.attributes.datasets

    @datasets.setter
    def datasets(self, datasets: Optional[list[PowerBIDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasets = datasets

    @property
    def dashboards(self) -> Optional[list[PowerBIDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[list[PowerBIDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    @property
    def dataflows(self) -> Optional[list[PowerBIDataflow]]:
        return None if self.attributes is None else self.attributes.dataflows

    @dataflows.setter
    def dataflows(self, dataflows: Optional[list[PowerBIDataflow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataflows = dataflows

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
        reports: Optional[list[PowerBIReport]] = Field(
            None, description="", alias="reports"
        )  # relationship
        datasets: Optional[list[PowerBIDataset]] = Field(
            None, description="", alias="datasets"
        )  # relationship
        dashboards: Optional[list[PowerBIDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship
        dataflows: Optional[list[PowerBIDataflow]] = Field(
            None, description="", alias="dataflows"
        )  # relationship

    attributes: "PowerBIWorkspace.Attributes" = Field(
        default_factory=lambda: PowerBIWorkspace.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIDataset(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDataset":
            raise ValueError("must be PowerBIDataset")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDataset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "web_url",
        "reports",
        "workspace",
        "dataflows",
        "tiles",
        "tables",
        "datasources",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def reports(self) -> Optional[list[PowerBIReport]]:
        return None if self.attributes is None else self.attributes.reports

    @reports.setter
    def reports(self, reports: Optional[list[PowerBIReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reports = reports

    @property
    def workspace(self) -> Optional[PowerBIWorkspace]:
        return None if self.attributes is None else self.attributes.workspace

    @workspace.setter
    def workspace(self, workspace: Optional[PowerBIWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace = workspace

    @property
    def dataflows(self) -> Optional[list[PowerBIDataflow]]:
        return None if self.attributes is None else self.attributes.dataflows

    @dataflows.setter
    def dataflows(self, dataflows: Optional[list[PowerBIDataflow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataflows = dataflows

    @property
    def tiles(self) -> Optional[list[PowerBITile]]:
        return None if self.attributes is None else self.attributes.tiles

    @tiles.setter
    def tiles(self, tiles: Optional[list[PowerBITile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tiles = tiles

    @property
    def tables(self) -> Optional[list[PowerBITable]]:
        return None if self.attributes is None else self.attributes.tables

    @tables.setter
    def tables(self, tables: Optional[list[PowerBITable]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tables = tables

    @property
    def datasources(self) -> Optional[list[PowerBIDatasource]]:
        return None if self.attributes is None else self.attributes.datasources

    @datasources.setter
    def datasources(self, datasources: Optional[list[PowerBIDatasource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasources = datasources

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        reports: Optional[list[PowerBIReport]] = Field(
            None, description="", alias="reports"
        )  # relationship
        workspace: Optional[PowerBIWorkspace] = Field(
            None, description="", alias="workspace"
        )  # relationship
        dataflows: Optional[list[PowerBIDataflow]] = Field(
            None, description="", alias="dataflows"
        )  # relationship
        tiles: Optional[list[PowerBITile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        tables: Optional[list[PowerBITable]] = Field(
            None, description="", alias="tables"
        )  # relationship
        datasources: Optional[list[PowerBIDatasource]] = Field(
            None, description="", alias="datasources"
        )  # relationship

    attributes: "PowerBIDataset.Attributes" = Field(
        default_factory=lambda: PowerBIDataset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIDashboard(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDashboard":
            raise ValueError("must be PowerBIDashboard")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDashboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "web_url",
        "tile_count",
        "tiles",
        "workspace",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def tile_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.tile_count

    @tile_count.setter
    def tile_count(self, tile_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tile_count = tile_count

    @property
    def tiles(self) -> Optional[list[PowerBITile]]:
        return None if self.attributes is None else self.attributes.tiles

    @tiles.setter
    def tiles(self, tiles: Optional[list[PowerBITile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tiles = tiles

    @property
    def workspace(self) -> Optional[PowerBIWorkspace]:
        return None if self.attributes is None else self.attributes.workspace

    @workspace.setter
    def workspace(self, workspace: Optional[PowerBIWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace = workspace

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        tile_count: Optional[int] = Field(None, description="", alias="tileCount")
        tiles: Optional[list[PowerBITile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        workspace: Optional[PowerBIWorkspace] = Field(
            None, description="", alias="workspace"
        )  # relationship

    attributes: "PowerBIDashboard.Attributes" = Field(
        default_factory=lambda: PowerBIDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIDataflow(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIDataflow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDataflow":
            raise ValueError("must be PowerBIDataflow")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDataflow._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "web_url",
        "workspace",
        "datasets",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def workspace(self) -> Optional[PowerBIWorkspace]:
        return None if self.attributes is None else self.attributes.workspace

    @workspace.setter
    def workspace(self, workspace: Optional[PowerBIWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace = workspace

    @property
    def datasets(self) -> Optional[list[PowerBIDataset]]:
        return None if self.attributes is None else self.attributes.datasets

    @datasets.setter
    def datasets(self, datasets: Optional[list[PowerBIDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasets = datasets

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        workspace: Optional[PowerBIWorkspace] = Field(
            None, description="", alias="workspace"
        )  # relationship
        datasets: Optional[list[PowerBIDataset]] = Field(
            None, description="", alias="datasets"
        )  # relationship

    attributes: "PowerBIDataflow.Attributes" = Field(
        default_factory=lambda: PowerBIDataflow.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIPage(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIPage", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIPage":
            raise ValueError("must be PowerBIPage")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIPage._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "report_qualified_name",
        "report",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def report_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.report_qualified_name
        )

    @report_qualified_name.setter
    def report_qualified_name(self, report_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_qualified_name = report_qualified_name

    @property
    def report(self) -> Optional[PowerBIReport]:
        return None if self.attributes is None else self.attributes.report

    @report.setter
    def report(self, report: Optional[PowerBIReport]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report = report

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        report_qualified_name: Optional[str] = Field(
            None, description="", alias="reportQualifiedName"
        )
        report: Optional[PowerBIReport] = Field(
            None, description="", alias="report"
        )  # relationship

    attributes: "PowerBIPage.Attributes" = Field(
        default_factory=lambda: PowerBIPage.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyReport(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyReport":
            raise ValueError("must be MicroStrategyReport")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyReport._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "micro_strategy_report_type",
        "micro_strategy_metrics",
        "micro_strategy_project",
        "micro_strategy_attributes",
    ]

    @property
    def micro_strategy_report_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_report_type
        )

    @micro_strategy_report_type.setter
    def micro_strategy_report_type(self, micro_strategy_report_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_report_type = micro_strategy_report_type

    @property
    def micro_strategy_metrics(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_metrics
        )

    @micro_strategy_metrics.setter
    def micro_strategy_metrics(
        self, micro_strategy_metrics: Optional[list[MicroStrategyMetric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metrics = micro_strategy_metrics

    @property
    def micro_strategy_project(self) -> Optional[MicroStrategyProject]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_project
        )

    @micro_strategy_project.setter
    def micro_strategy_project(
        self, micro_strategy_project: Optional[MicroStrategyProject]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project = micro_strategy_project

    @property
    def micro_strategy_attributes(self) -> Optional[list[MicroStrategyAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attributes
        )

    @micro_strategy_attributes.setter
    def micro_strategy_attributes(
        self, micro_strategy_attributes: Optional[list[MicroStrategyAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attributes = micro_strategy_attributes

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_report_type: Optional[str] = Field(
            None, description="", alias="microStrategyReportType"
        )
        micro_strategy_metrics: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetrics"
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship
        micro_strategy_attributes: Optional[list[MicroStrategyAttribute]] = Field(
            None, description="", alias="microStrategyAttributes"
        )  # relationship

    attributes: "MicroStrategyReport.Attributes" = Field(
        default_factory=lambda: MicroStrategyReport.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyProject(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyProject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyProject":
            raise ValueError("must be MicroStrategyProject")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyProject._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "micro_strategy_reports",
        "micro_strategy_facts",
        "micro_strategy_metrics",
        "micro_strategy_visualizations",
        "micro_strategy_documents",
        "micro_strategy_cubes",
        "micro_strategy_dossiers",
        "micro_strategy_attributes",
    ]

    @property
    def micro_strategy_reports(self) -> Optional[list[MicroStrategyReport]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_reports
        )

    @micro_strategy_reports.setter
    def micro_strategy_reports(
        self, micro_strategy_reports: Optional[list[MicroStrategyReport]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_reports = micro_strategy_reports

    @property
    def micro_strategy_facts(self) -> Optional[list[MicroStrategyFact]]:
        return None if self.attributes is None else self.attributes.micro_strategy_facts

    @micro_strategy_facts.setter
    def micro_strategy_facts(
        self, micro_strategy_facts: Optional[list[MicroStrategyFact]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_facts = micro_strategy_facts

    @property
    def micro_strategy_metrics(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_metrics
        )

    @micro_strategy_metrics.setter
    def micro_strategy_metrics(
        self, micro_strategy_metrics: Optional[list[MicroStrategyMetric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metrics = micro_strategy_metrics

    @property
    def micro_strategy_visualizations(
        self,
    ) -> Optional[list[MicroStrategyVisualization]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_visualizations
        )

    @micro_strategy_visualizations.setter
    def micro_strategy_visualizations(
        self, micro_strategy_visualizations: Optional[list[MicroStrategyVisualization]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_visualizations = micro_strategy_visualizations

    @property
    def micro_strategy_documents(self) -> Optional[list[MicroStrategyDocument]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_documents
        )

    @micro_strategy_documents.setter
    def micro_strategy_documents(
        self, micro_strategy_documents: Optional[list[MicroStrategyDocument]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_documents = micro_strategy_documents

    @property
    def micro_strategy_cubes(self) -> Optional[list[MicroStrategyCube]]:
        return None if self.attributes is None else self.attributes.micro_strategy_cubes

    @micro_strategy_cubes.setter
    def micro_strategy_cubes(
        self, micro_strategy_cubes: Optional[list[MicroStrategyCube]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cubes = micro_strategy_cubes

    @property
    def micro_strategy_dossiers(self) -> Optional[list[MicroStrategyDossier]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_dossiers
        )

    @micro_strategy_dossiers.setter
    def micro_strategy_dossiers(
        self, micro_strategy_dossiers: Optional[list[MicroStrategyDossier]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_dossiers = micro_strategy_dossiers

    @property
    def micro_strategy_attributes(self) -> Optional[list[MicroStrategyAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attributes
        )

    @micro_strategy_attributes.setter
    def micro_strategy_attributes(
        self, micro_strategy_attributes: Optional[list[MicroStrategyAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attributes = micro_strategy_attributes

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_reports: Optional[list[MicroStrategyReport]] = Field(
            None, description="", alias="microStrategyReports"
        )  # relationship
        micro_strategy_facts: Optional[list[MicroStrategyFact]] = Field(
            None, description="", alias="microStrategyFacts"
        )  # relationship
        micro_strategy_metrics: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetrics"
        )  # relationship
        micro_strategy_visualizations: Optional[
            list[MicroStrategyVisualization]
        ] = Field(
            None, description="", alias="microStrategyVisualizations"
        )  # relationship
        micro_strategy_documents: Optional[list[MicroStrategyDocument]] = Field(
            None, description="", alias="microStrategyDocuments"
        )  # relationship
        micro_strategy_cubes: Optional[list[MicroStrategyCube]] = Field(
            None, description="", alias="microStrategyCubes"
        )  # relationship
        micro_strategy_dossiers: Optional[list[MicroStrategyDossier]] = Field(
            None, description="", alias="microStrategyDossiers"
        )  # relationship
        micro_strategy_attributes: Optional[list[MicroStrategyAttribute]] = Field(
            None, description="", alias="microStrategyAttributes"
        )  # relationship

    attributes: "MicroStrategyProject.Attributes" = Field(
        default_factory=lambda: MicroStrategyProject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyMetric(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyMetric", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyMetric":
            raise ValueError("must be MicroStrategyMetric")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyMetric._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "micro_strategy_metric_expression",
        "micro_strategy_attribute_qualified_names",
        "micro_strategy_attribute_names",
        "micro_strategy_fact_qualified_names",
        "micro_strategy_fact_names",
        "micro_strategy_metric_parent_qualified_names",
        "micro_strategy_metric_parent_names",
        "micro_strategy_metric_parents",
        "micro_strategy_facts",
        "micro_strategy_reports",
        "micro_strategy_cubes",
        "micro_strategy_metric_children",
        "micro_strategy_project",
        "micro_strategy_attributes",
    ]

    @property
    def micro_strategy_metric_expression(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_expression
        )

    @micro_strategy_metric_expression.setter
    def micro_strategy_metric_expression(
        self, micro_strategy_metric_expression: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric_expression = (
            micro_strategy_metric_expression
        )

    @property
    def micro_strategy_attribute_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attribute_qualified_names
        )

    @micro_strategy_attribute_qualified_names.setter
    def micro_strategy_attribute_qualified_names(
        self, micro_strategy_attribute_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attribute_qualified_names = (
            micro_strategy_attribute_qualified_names
        )

    @property
    def micro_strategy_attribute_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attribute_names
        )

    @micro_strategy_attribute_names.setter
    def micro_strategy_attribute_names(
        self, micro_strategy_attribute_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attribute_names = micro_strategy_attribute_names

    @property
    def micro_strategy_fact_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_fact_qualified_names
        )

    @micro_strategy_fact_qualified_names.setter
    def micro_strategy_fact_qualified_names(
        self, micro_strategy_fact_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_fact_qualified_names = (
            micro_strategy_fact_qualified_names
        )

    @property
    def micro_strategy_fact_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_fact_names
        )

    @micro_strategy_fact_names.setter
    def micro_strategy_fact_names(self, micro_strategy_fact_names: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_fact_names = micro_strategy_fact_names

    @property
    def micro_strategy_metric_parent_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_parent_qualified_names
        )

    @micro_strategy_metric_parent_qualified_names.setter
    def micro_strategy_metric_parent_qualified_names(
        self, micro_strategy_metric_parent_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric_parent_qualified_names = (
            micro_strategy_metric_parent_qualified_names
        )

    @property
    def micro_strategy_metric_parent_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_parent_names
        )

    @micro_strategy_metric_parent_names.setter
    def micro_strategy_metric_parent_names(
        self, micro_strategy_metric_parent_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric_parent_names = (
            micro_strategy_metric_parent_names
        )

    @property
    def micro_strategy_metric_parents(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_parents
        )

    @micro_strategy_metric_parents.setter
    def micro_strategy_metric_parents(
        self, micro_strategy_metric_parents: Optional[list[MicroStrategyMetric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric_parents = micro_strategy_metric_parents

    @property
    def micro_strategy_facts(self) -> Optional[list[MicroStrategyFact]]:
        return None if self.attributes is None else self.attributes.micro_strategy_facts

    @micro_strategy_facts.setter
    def micro_strategy_facts(
        self, micro_strategy_facts: Optional[list[MicroStrategyFact]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_facts = micro_strategy_facts

    @property
    def micro_strategy_reports(self) -> Optional[list[MicroStrategyReport]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_reports
        )

    @micro_strategy_reports.setter
    def micro_strategy_reports(
        self, micro_strategy_reports: Optional[list[MicroStrategyReport]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_reports = micro_strategy_reports

    @property
    def micro_strategy_cubes(self) -> Optional[list[MicroStrategyCube]]:
        return None if self.attributes is None else self.attributes.micro_strategy_cubes

    @micro_strategy_cubes.setter
    def micro_strategy_cubes(
        self, micro_strategy_cubes: Optional[list[MicroStrategyCube]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cubes = micro_strategy_cubes

    @property
    def micro_strategy_metric_children(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_children
        )

    @micro_strategy_metric_children.setter
    def micro_strategy_metric_children(
        self, micro_strategy_metric_children: Optional[list[MicroStrategyMetric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric_children = micro_strategy_metric_children

    @property
    def micro_strategy_project(self) -> Optional[MicroStrategyProject]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_project
        )

    @micro_strategy_project.setter
    def micro_strategy_project(
        self, micro_strategy_project: Optional[MicroStrategyProject]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project = micro_strategy_project

    @property
    def micro_strategy_attributes(self) -> Optional[list[MicroStrategyAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attributes
        )

    @micro_strategy_attributes.setter
    def micro_strategy_attributes(
        self, micro_strategy_attributes: Optional[list[MicroStrategyAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attributes = micro_strategy_attributes

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_metric_expression: Optional[str] = Field(
            None, description="", alias="microStrategyMetricExpression"
        )
        micro_strategy_attribute_qualified_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyAttributeQualifiedNames"
        )
        micro_strategy_attribute_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyAttributeNames"
        )
        micro_strategy_fact_qualified_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyFactQualifiedNames"
        )
        micro_strategy_fact_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyFactNames"
        )
        micro_strategy_metric_parent_qualified_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyMetricParentQualifiedNames"
        )
        micro_strategy_metric_parent_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyMetricParentNames"
        )
        micro_strategy_metric_parents: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetricParents"
        )  # relationship
        micro_strategy_facts: Optional[list[MicroStrategyFact]] = Field(
            None, description="", alias="microStrategyFacts"
        )  # relationship
        micro_strategy_reports: Optional[list[MicroStrategyReport]] = Field(
            None, description="", alias="microStrategyReports"
        )  # relationship
        micro_strategy_cubes: Optional[list[MicroStrategyCube]] = Field(
            None, description="", alias="microStrategyCubes"
        )  # relationship
        micro_strategy_metric_children: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetricChildren"
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship
        micro_strategy_attributes: Optional[list[MicroStrategyAttribute]] = Field(
            None, description="", alias="microStrategyAttributes"
        )  # relationship

    attributes: "MicroStrategyMetric.Attributes" = Field(
        default_factory=lambda: MicroStrategyMetric.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyCube(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyCube", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyCube":
            raise ValueError("must be MicroStrategyCube")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyCube._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "micro_strategy_cube_type",
        "micro_strategy_cube_query",
        "micro_strategy_metrics",
        "micro_strategy_project",
        "micro_strategy_attributes",
    ]

    @property
    def micro_strategy_cube_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_cube_type
        )

    @micro_strategy_cube_type.setter
    def micro_strategy_cube_type(self, micro_strategy_cube_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cube_type = micro_strategy_cube_type

    @property
    def micro_strategy_cube_query(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_cube_query
        )

    @micro_strategy_cube_query.setter
    def micro_strategy_cube_query(self, micro_strategy_cube_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cube_query = micro_strategy_cube_query

    @property
    def micro_strategy_metrics(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_metrics
        )

    @micro_strategy_metrics.setter
    def micro_strategy_metrics(
        self, micro_strategy_metrics: Optional[list[MicroStrategyMetric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metrics = micro_strategy_metrics

    @property
    def micro_strategy_project(self) -> Optional[MicroStrategyProject]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_project
        )

    @micro_strategy_project.setter
    def micro_strategy_project(
        self, micro_strategy_project: Optional[MicroStrategyProject]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project = micro_strategy_project

    @property
    def micro_strategy_attributes(self) -> Optional[list[MicroStrategyAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attributes
        )

    @micro_strategy_attributes.setter
    def micro_strategy_attributes(
        self, micro_strategy_attributes: Optional[list[MicroStrategyAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attributes = micro_strategy_attributes

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_cube_type: Optional[str] = Field(
            None, description="", alias="microStrategyCubeType"
        )
        micro_strategy_cube_query: Optional[str] = Field(
            None, description="", alias="microStrategyCubeQuery"
        )
        micro_strategy_metrics: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetrics"
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship
        micro_strategy_attributes: Optional[list[MicroStrategyAttribute]] = Field(
            None, description="", alias="microStrategyAttributes"
        )  # relationship

    attributes: "MicroStrategyCube.Attributes" = Field(
        default_factory=lambda: MicroStrategyCube.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyDossier(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyDossier", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyDossier":
            raise ValueError("must be MicroStrategyDossier")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyDossier._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "micro_strategy_dossier_chapter_names",
        "micro_strategy_project",
        "micro_strategy_visualizations",
    ]

    @property
    def micro_strategy_dossier_chapter_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_dossier_chapter_names
        )

    @micro_strategy_dossier_chapter_names.setter
    def micro_strategy_dossier_chapter_names(
        self, micro_strategy_dossier_chapter_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_dossier_chapter_names = (
            micro_strategy_dossier_chapter_names
        )

    @property
    def micro_strategy_project(self) -> Optional[MicroStrategyProject]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_project
        )

    @micro_strategy_project.setter
    def micro_strategy_project(
        self, micro_strategy_project: Optional[MicroStrategyProject]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project = micro_strategy_project

    @property
    def micro_strategy_visualizations(
        self,
    ) -> Optional[list[MicroStrategyVisualization]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_visualizations
        )

    @micro_strategy_visualizations.setter
    def micro_strategy_visualizations(
        self, micro_strategy_visualizations: Optional[list[MicroStrategyVisualization]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_visualizations = micro_strategy_visualizations

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_dossier_chapter_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyDossierChapterNames"
        )
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship
        micro_strategy_visualizations: Optional[
            list[MicroStrategyVisualization]
        ] = Field(
            None, description="", alias="microStrategyVisualizations"
        )  # relationship

    attributes: "MicroStrategyDossier.Attributes" = Field(
        default_factory=lambda: MicroStrategyDossier.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyFact(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyFact", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyFact":
            raise ValueError("must be MicroStrategyFact")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyFact._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "micro_strategy_fact_expressions",
        "micro_strategy_metrics",
        "micro_strategy_project",
    ]

    @property
    def micro_strategy_fact_expressions(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_fact_expressions
        )

    @micro_strategy_fact_expressions.setter
    def micro_strategy_fact_expressions(
        self, micro_strategy_fact_expressions: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_fact_expressions = (
            micro_strategy_fact_expressions
        )

    @property
    def micro_strategy_metrics(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_metrics
        )

    @micro_strategy_metrics.setter
    def micro_strategy_metrics(
        self, micro_strategy_metrics: Optional[list[MicroStrategyMetric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metrics = micro_strategy_metrics

    @property
    def micro_strategy_project(self) -> Optional[MicroStrategyProject]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_project
        )

    @micro_strategy_project.setter
    def micro_strategy_project(
        self, micro_strategy_project: Optional[MicroStrategyProject]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project = micro_strategy_project

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_fact_expressions: Optional[set[str]] = Field(
            None, description="", alias="microStrategyFactExpressions"
        )
        micro_strategy_metrics: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetrics"
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship

    attributes: "MicroStrategyFact.Attributes" = Field(
        default_factory=lambda: MicroStrategyFact.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyDocument(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyDocument", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyDocument":
            raise ValueError("must be MicroStrategyDocument")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyDocument._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "micro_strategy_project",
    ]

    @property
    def micro_strategy_project(self) -> Optional[MicroStrategyProject]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_project
        )

    @micro_strategy_project.setter
    def micro_strategy_project(
        self, micro_strategy_project: Optional[MicroStrategyProject]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project = micro_strategy_project

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship

    attributes: "MicroStrategyDocument.Attributes" = Field(
        default_factory=lambda: MicroStrategyDocument.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyAttribute(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyAttribute", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyAttribute":
            raise ValueError("must be MicroStrategyAttribute")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyAttribute._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "micro_strategy_attribute_forms",
        "micro_strategy_reports",
        "micro_strategy_metrics",
        "micro_strategy_cubes",
        "micro_strategy_project",
    ]

    @property
    def micro_strategy_attribute_forms(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attribute_forms
        )

    @micro_strategy_attribute_forms.setter
    def micro_strategy_attribute_forms(
        self, micro_strategy_attribute_forms: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attribute_forms = micro_strategy_attribute_forms

    @property
    def micro_strategy_reports(self) -> Optional[list[MicroStrategyReport]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_reports
        )

    @micro_strategy_reports.setter
    def micro_strategy_reports(
        self, micro_strategy_reports: Optional[list[MicroStrategyReport]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_reports = micro_strategy_reports

    @property
    def micro_strategy_metrics(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_metrics
        )

    @micro_strategy_metrics.setter
    def micro_strategy_metrics(
        self, micro_strategy_metrics: Optional[list[MicroStrategyMetric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metrics = micro_strategy_metrics

    @property
    def micro_strategy_cubes(self) -> Optional[list[MicroStrategyCube]]:
        return None if self.attributes is None else self.attributes.micro_strategy_cubes

    @micro_strategy_cubes.setter
    def micro_strategy_cubes(
        self, micro_strategy_cubes: Optional[list[MicroStrategyCube]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cubes = micro_strategy_cubes

    @property
    def micro_strategy_project(self) -> Optional[MicroStrategyProject]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_project
        )

    @micro_strategy_project.setter
    def micro_strategy_project(
        self, micro_strategy_project: Optional[MicroStrategyProject]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project = micro_strategy_project

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_attribute_forms: Optional[str] = Field(
            None, description="", alias="microStrategyAttributeForms"
        )
        micro_strategy_reports: Optional[list[MicroStrategyReport]] = Field(
            None, description="", alias="microStrategyReports"
        )  # relationship
        micro_strategy_metrics: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetrics"
        )  # relationship
        micro_strategy_cubes: Optional[list[MicroStrategyCube]] = Field(
            None, description="", alias="microStrategyCubes"
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship

    attributes: "MicroStrategyAttribute.Attributes" = Field(
        default_factory=lambda: MicroStrategyAttribute.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyVisualization(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyVisualization", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyVisualization":
            raise ValueError("must be MicroStrategyVisualization")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyVisualization._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "micro_strategy_visualization_type",
        "micro_strategy_dossier_qualified_name",
        "micro_strategy_dossier_name",
        "micro_strategy_dossier",
        "micro_strategy_project",
    ]

    @property
    def micro_strategy_visualization_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_visualization_type
        )

    @micro_strategy_visualization_type.setter
    def micro_strategy_visualization_type(
        self, micro_strategy_visualization_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_visualization_type = (
            micro_strategy_visualization_type
        )

    @property
    def micro_strategy_dossier_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_dossier_qualified_name
        )

    @micro_strategy_dossier_qualified_name.setter
    def micro_strategy_dossier_qualified_name(
        self, micro_strategy_dossier_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_dossier_qualified_name = (
            micro_strategy_dossier_qualified_name
        )

    @property
    def micro_strategy_dossier_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_dossier_name
        )

    @micro_strategy_dossier_name.setter
    def micro_strategy_dossier_name(self, micro_strategy_dossier_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_dossier_name = micro_strategy_dossier_name

    @property
    def micro_strategy_dossier(self) -> Optional[MicroStrategyDossier]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_dossier
        )

    @micro_strategy_dossier.setter
    def micro_strategy_dossier(
        self, micro_strategy_dossier: Optional[MicroStrategyDossier]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_dossier = micro_strategy_dossier

    @property
    def micro_strategy_project(self) -> Optional[MicroStrategyProject]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_project
        )

    @micro_strategy_project.setter
    def micro_strategy_project(
        self, micro_strategy_project: Optional[MicroStrategyProject]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project = micro_strategy_project

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_visualization_type: Optional[str] = Field(
            None, description="", alias="microStrategyVisualizationType"
        )
        micro_strategy_dossier_qualified_name: Optional[str] = Field(
            None, description="", alias="microStrategyDossierQualifiedName"
        )
        micro_strategy_dossier_name: Optional[str] = Field(
            None, description="", alias="microStrategyDossierName"
        )
        micro_strategy_dossier: Optional[MicroStrategyDossier] = Field(
            None, description="", alias="microStrategyDossier"
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship

    attributes: "MicroStrategyVisualization.Attributes" = Field(
        default_factory=lambda: MicroStrategyVisualization.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikSpace(Qlik):
    """Description"""

    type_name: str = Field("QlikSpace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikSpace":
            raise ValueError("must be QlikSpace")
        return v

    def __setattr__(self, name, value):
        if name in QlikSpace._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "qlik_space_type",
        "qlik_datasets",
        "qlik_apps",
    ]

    @property
    def qlik_space_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_space_type

    @qlik_space_type.setter
    def qlik_space_type(self, qlik_space_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space_type = qlik_space_type

    @property
    def qlik_datasets(self) -> Optional[list[QlikDataset]]:
        return None if self.attributes is None else self.attributes.qlik_datasets

    @qlik_datasets.setter
    def qlik_datasets(self, qlik_datasets: Optional[list[QlikDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_datasets = qlik_datasets

    @property
    def qlik_apps(self) -> Optional[list[QlikApp]]:
        return None if self.attributes is None else self.attributes.qlik_apps

    @qlik_apps.setter
    def qlik_apps(self, qlik_apps: Optional[list[QlikApp]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_apps = qlik_apps

    class Attributes(Qlik.Attributes):
        qlik_space_type: Optional[str] = Field(
            None, description="", alias="qlikSpaceType"
        )
        qlik_datasets: Optional[list[QlikDataset]] = Field(
            None, description="", alias="qlikDatasets"
        )  # relationship
        qlik_apps: Optional[list[QlikApp]] = Field(
            None, description="", alias="qlikApps"
        )  # relationship

    attributes: "QlikSpace.Attributes" = Field(
        default_factory=lambda: QlikSpace.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikApp(Qlik):
    """Description"""

    type_name: str = Field("QlikApp", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikApp":
            raise ValueError("must be QlikApp")
        return v

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
        "qlik_space",
        "qlik_sheets",
    ]

    @property
    def qlik_has_section_access(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.qlik_has_section_access
        )

    @qlik_has_section_access.setter
    def qlik_has_section_access(self, qlik_has_section_access: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_has_section_access = qlik_has_section_access

    @property
    def qlik_origin_app_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_origin_app_id

    @qlik_origin_app_id.setter
    def qlik_origin_app_id(self, qlik_origin_app_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_origin_app_id = qlik_origin_app_id

    @property
    def qlik_is_encrypted(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.qlik_is_encrypted

    @qlik_is_encrypted.setter
    def qlik_is_encrypted(self, qlik_is_encrypted: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_is_encrypted = qlik_is_encrypted

    @property
    def qlik_is_direct_query_mode(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.qlik_is_direct_query_mode
        )

    @qlik_is_direct_query_mode.setter
    def qlik_is_direct_query_mode(self, qlik_is_direct_query_mode: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_is_direct_query_mode = qlik_is_direct_query_mode

    @property
    def qlik_app_static_byte_size(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.qlik_app_static_byte_size
        )

    @qlik_app_static_byte_size.setter
    def qlik_app_static_byte_size(self, qlik_app_static_byte_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_app_static_byte_size = qlik_app_static_byte_size

    @property
    def qlik_space(self) -> Optional[QlikSpace]:
        return None if self.attributes is None else self.attributes.qlik_space

    @qlik_space.setter
    def qlik_space(self, qlik_space: Optional[QlikSpace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space = qlik_space

    @property
    def qlik_sheets(self) -> Optional[list[QlikSheet]]:
        return None if self.attributes is None else self.attributes.qlik_sheets

    @qlik_sheets.setter
    def qlik_sheets(self, qlik_sheets: Optional[list[QlikSheet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_sheets = qlik_sheets

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
        qlik_space: Optional[QlikSpace] = Field(
            None, description="", alias="qlikSpace"
        )  # relationship
        qlik_sheets: Optional[list[QlikSheet]] = Field(
            None, description="", alias="qlikSheets"
        )  # relationship

    attributes: "QlikApp.Attributes" = Field(
        default_factory=lambda: QlikApp.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikChart(Qlik):
    """Description"""

    type_name: str = Field("QlikChart", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikChart":
            raise ValueError("must be QlikChart")
        return v

    def __setattr__(self, name, value):
        if name in QlikChart._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "qlik_chart_subtitle",
        "qlik_chart_footnote",
        "qlik_chart_orientation",
        "qlik_chart_type",
        "qlik_sheet",
    ]

    @property
    def qlik_chart_subtitle(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_chart_subtitle

    @qlik_chart_subtitle.setter
    def qlik_chart_subtitle(self, qlik_chart_subtitle: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_chart_subtitle = qlik_chart_subtitle

    @property
    def qlik_chart_footnote(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_chart_footnote

    @qlik_chart_footnote.setter
    def qlik_chart_footnote(self, qlik_chart_footnote: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_chart_footnote = qlik_chart_footnote

    @property
    def qlik_chart_orientation(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.qlik_chart_orientation
        )

    @qlik_chart_orientation.setter
    def qlik_chart_orientation(self, qlik_chart_orientation: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_chart_orientation = qlik_chart_orientation

    @property
    def qlik_chart_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_chart_type

    @qlik_chart_type.setter
    def qlik_chart_type(self, qlik_chart_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_chart_type = qlik_chart_type

    @property
    def qlik_sheet(self) -> Optional[QlikSheet]:
        return None if self.attributes is None else self.attributes.qlik_sheet

    @qlik_sheet.setter
    def qlik_sheet(self, qlik_sheet: Optional[QlikSheet]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_sheet = qlik_sheet

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
        qlik_sheet: Optional[QlikSheet] = Field(
            None, description="", alias="qlikSheet"
        )  # relationship

    attributes: "QlikChart.Attributes" = Field(
        default_factory=lambda: QlikChart.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikDataset(Qlik):
    """Description"""

    type_name: str = Field("QlikDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikDataset":
            raise ValueError("must be QlikDataset")
        return v

    def __setattr__(self, name, value):
        if name in QlikDataset._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "qlik_dataset_technical_name",
        "qlik_dataset_type",
        "qlik_dataset_uri",
        "qlik_dataset_subtype",
        "qlik_space",
    ]

    @property
    def qlik_dataset_technical_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.qlik_dataset_technical_name
        )

    @qlik_dataset_technical_name.setter
    def qlik_dataset_technical_name(self, qlik_dataset_technical_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_technical_name = qlik_dataset_technical_name

    @property
    def qlik_dataset_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_dataset_type

    @qlik_dataset_type.setter
    def qlik_dataset_type(self, qlik_dataset_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_type = qlik_dataset_type

    @property
    def qlik_dataset_uri(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_dataset_uri

    @qlik_dataset_uri.setter
    def qlik_dataset_uri(self, qlik_dataset_uri: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_uri = qlik_dataset_uri

    @property
    def qlik_dataset_subtype(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_dataset_subtype

    @qlik_dataset_subtype.setter
    def qlik_dataset_subtype(self, qlik_dataset_subtype: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_subtype = qlik_dataset_subtype

    @property
    def qlik_space(self) -> Optional[QlikSpace]:
        return None if self.attributes is None else self.attributes.qlik_space

    @qlik_space.setter
    def qlik_space(self, qlik_space: Optional[QlikSpace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space = qlik_space

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
        qlik_space: Optional[QlikSpace] = Field(
            None, description="", alias="qlikSpace"
        )  # relationship

    attributes: "QlikDataset.Attributes" = Field(
        default_factory=lambda: QlikDataset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikSheet(Qlik):
    """Description"""

    type_name: str = Field("QlikSheet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikSheet":
            raise ValueError("must be QlikSheet")
        return v

    def __setattr__(self, name, value):
        if name in QlikSheet._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "qlik_sheet_is_approved",
        "qlik_app",
        "qlik_charts",
    ]

    @property
    def qlik_sheet_is_approved(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.qlik_sheet_is_approved
        )

    @qlik_sheet_is_approved.setter
    def qlik_sheet_is_approved(self, qlik_sheet_is_approved: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_sheet_is_approved = qlik_sheet_is_approved

    @property
    def qlik_app(self) -> Optional[QlikApp]:
        return None if self.attributes is None else self.attributes.qlik_app

    @qlik_app.setter
    def qlik_app(self, qlik_app: Optional[QlikApp]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_app = qlik_app

    @property
    def qlik_charts(self) -> Optional[list[QlikChart]]:
        return None if self.attributes is None else self.attributes.qlik_charts

    @qlik_charts.setter
    def qlik_charts(self, qlik_charts: Optional[list[QlikChart]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_charts = qlik_charts

    class Attributes(Qlik.Attributes):
        qlik_sheet_is_approved: Optional[bool] = Field(
            None, description="", alias="qlikSheetIsApproved"
        )
        qlik_app: Optional[QlikApp] = Field(
            None, description="", alias="qlikApp"
        )  # relationship
        qlik_charts: Optional[list[QlikChart]] = Field(
            None, description="", alias="qlikCharts"
        )  # relationship

    attributes: "QlikSheet.Attributes" = Field(
        default_factory=lambda: QlikSheet.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceObject(Salesforce):
    """Description"""

    type_name: str = Field("SalesforceObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceObject":
            raise ValueError("must be SalesforceObject")
        return v

    def __setattr__(self, name, value):
        if name in SalesforceObject._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "is_custom",
        "is_mergable",
        "is_queryable",
        "field_count",
        "organization",
        "lookup_fields",
        "fields",
    ]

    @property
    def is_custom(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_custom

    @is_custom.setter
    def is_custom(self, is_custom: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_custom = is_custom

    @property
    def is_mergable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_mergable

    @is_mergable.setter
    def is_mergable(self, is_mergable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_mergable = is_mergable

    @property
    def is_queryable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_queryable

    @is_queryable.setter
    def is_queryable(self, is_queryable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_queryable = is_queryable

    @property
    def field_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.field_count

    @field_count.setter
    def field_count(self, field_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.field_count = field_count

    @property
    def organization(self) -> Optional[SalesforceOrganization]:
        return None if self.attributes is None else self.attributes.organization

    @organization.setter
    def organization(self, organization: Optional[SalesforceOrganization]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.organization = organization

    @property
    def lookup_fields(self) -> Optional[list[SalesforceField]]:
        return None if self.attributes is None else self.attributes.lookup_fields

    @lookup_fields.setter
    def lookup_fields(self, lookup_fields: Optional[list[SalesforceField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.lookup_fields = lookup_fields

    @property
    def fields(self) -> Optional[list[SalesforceField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[list[SalesforceField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    class Attributes(Salesforce.Attributes):
        is_custom: Optional[bool] = Field(None, description="", alias="isCustom")
        is_mergable: Optional[bool] = Field(None, description="", alias="isMergable")
        is_queryable: Optional[bool] = Field(None, description="", alias="isQueryable")
        field_count: Optional[int] = Field(None, description="", alias="fieldCount")
        organization: Optional[SalesforceOrganization] = Field(
            None, description="", alias="organization"
        )  # relationship
        lookup_fields: Optional[list[SalesforceField]] = Field(
            None, description="", alias="lookupFields"
        )  # relationship
        fields: Optional[list[SalesforceField]] = Field(
            None, description="", alias="fields"
        )  # relationship

    attributes: "SalesforceObject.Attributes" = Field(
        default_factory=lambda: SalesforceObject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceField(Salesforce):
    """Description"""

    type_name: str = Field("SalesforceField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceField":
            raise ValueError("must be SalesforceField")
        return v

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
        "lookup_objects",
        "object",
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
    def object_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.object_qualified_name
        )

    @object_qualified_name.setter
    def object_qualified_name(self, object_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.object_qualified_name = object_qualified_name

    @property
    def order(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.order

    @order.setter
    def order(self, order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.order = order

    @property
    def inline_help_text(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.inline_help_text

    @inline_help_text.setter
    def inline_help_text(self, inline_help_text: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inline_help_text = inline_help_text

    @property
    def is_calculated(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_calculated

    @is_calculated.setter
    def is_calculated(self, is_calculated: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_calculated = is_calculated

    @property
    def formula(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.formula

    @formula.setter
    def formula(self, formula: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.formula = formula

    @property
    def is_case_sensitive(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_case_sensitive

    @is_case_sensitive.setter
    def is_case_sensitive(self, is_case_sensitive: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_case_sensitive = is_case_sensitive

    @property
    def is_encrypted(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_encrypted

    @is_encrypted.setter
    def is_encrypted(self, is_encrypted: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_encrypted = is_encrypted

    @property
    def max_length(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.max_length

    @max_length.setter
    def max_length(self, max_length: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.max_length = max_length

    @property
    def is_nullable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_nullable

    @is_nullable.setter
    def is_nullable(self, is_nullable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_nullable = is_nullable

    @property
    def precision(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.precision

    @precision.setter
    def precision(self, precision: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.precision = precision

    @property
    def numeric_scale(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.numeric_scale

    @numeric_scale.setter
    def numeric_scale(self, numeric_scale: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.numeric_scale = numeric_scale

    @property
    def is_unique(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_unique

    @is_unique.setter
    def is_unique(self, is_unique: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_unique = is_unique

    @property
    def picklist_values(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.picklist_values

    @picklist_values.setter
    def picklist_values(self, picklist_values: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.picklist_values = picklist_values

    @property
    def is_polymorphic_foreign_key(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.is_polymorphic_foreign_key
        )

    @is_polymorphic_foreign_key.setter
    def is_polymorphic_foreign_key(self, is_polymorphic_foreign_key: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_polymorphic_foreign_key = is_polymorphic_foreign_key

    @property
    def default_value_formula(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.default_value_formula
        )

    @default_value_formula.setter
    def default_value_formula(self, default_value_formula: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.default_value_formula = default_value_formula

    @property
    def lookup_objects(self) -> Optional[list[SalesforceObject]]:
        return None if self.attributes is None else self.attributes.lookup_objects

    @lookup_objects.setter
    def lookup_objects(self, lookup_objects: Optional[list[SalesforceObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.lookup_objects = lookup_objects

    @property
    def object(self) -> Optional[SalesforceObject]:
        return None if self.attributes is None else self.attributes.object

    @object.setter
    def object(self, object: Optional[SalesforceObject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.object = object

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
        lookup_objects: Optional[list[SalesforceObject]] = Field(
            None, description="", alias="lookupObjects"
        )  # relationship
        object: Optional[SalesforceObject] = Field(
            None, description="", alias="object"
        )  # relationship

    attributes: "SalesforceField.Attributes" = Field(
        default_factory=lambda: SalesforceField.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceOrganization(Salesforce):
    """Description"""

    type_name: str = Field("SalesforceOrganization", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceOrganization":
            raise ValueError("must be SalesforceOrganization")
        return v

    def __setattr__(self, name, value):
        if name in SalesforceOrganization._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "source_id",
        "reports",
        "objects",
        "dashboards",
    ]

    @property
    def source_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_id

    @source_id.setter
    def source_id(self, source_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_id = source_id

    @property
    def reports(self) -> Optional[list[SalesforceReport]]:
        return None if self.attributes is None else self.attributes.reports

    @reports.setter
    def reports(self, reports: Optional[list[SalesforceReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reports = reports

    @property
    def objects(self) -> Optional[list[SalesforceObject]]:
        return None if self.attributes is None else self.attributes.objects

    @objects.setter
    def objects(self, objects: Optional[list[SalesforceObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.objects = objects

    @property
    def dashboards(self) -> Optional[list[SalesforceDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[list[SalesforceDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    class Attributes(Salesforce.Attributes):
        source_id: Optional[str] = Field(None, description="", alias="sourceId")
        reports: Optional[list[SalesforceReport]] = Field(
            None, description="", alias="reports"
        )  # relationship
        objects: Optional[list[SalesforceObject]] = Field(
            None, description="", alias="objects"
        )  # relationship
        dashboards: Optional[list[SalesforceDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship

    attributes: "SalesforceOrganization.Attributes" = Field(
        default_factory=lambda: SalesforceOrganization.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceDashboard(Salesforce):
    """Description"""

    type_name: str = Field("SalesforceDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceDashboard":
            raise ValueError("must be SalesforceDashboard")
        return v

    def __setattr__(self, name, value):
        if name in SalesforceDashboard._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "source_id",
        "dashboard_type",
        "report_count",
        "reports",
        "organization",
    ]

    @property
    def source_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_id

    @source_id.setter
    def source_id(self, source_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_id = source_id

    @property
    def dashboard_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dashboard_type

    @dashboard_type.setter
    def dashboard_type(self, dashboard_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard_type = dashboard_type

    @property
    def report_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.report_count

    @report_count.setter
    def report_count(self, report_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_count = report_count

    @property
    def reports(self) -> Optional[list[SalesforceReport]]:
        return None if self.attributes is None else self.attributes.reports

    @reports.setter
    def reports(self, reports: Optional[list[SalesforceReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reports = reports

    @property
    def organization(self) -> Optional[SalesforceOrganization]:
        return None if self.attributes is None else self.attributes.organization

    @organization.setter
    def organization(self, organization: Optional[SalesforceOrganization]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.organization = organization

    class Attributes(Salesforce.Attributes):
        source_id: Optional[str] = Field(None, description="", alias="sourceId")
        dashboard_type: Optional[str] = Field(
            None, description="", alias="dashboardType"
        )
        report_count: Optional[int] = Field(None, description="", alias="reportCount")
        reports: Optional[list[SalesforceReport]] = Field(
            None, description="", alias="reports"
        )  # relationship
        organization: Optional[SalesforceOrganization] = Field(
            None, description="", alias="organization"
        )  # relationship

    attributes: "SalesforceDashboard.Attributes" = Field(
        default_factory=lambda: SalesforceDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceReport(Salesforce):
    """Description"""

    type_name: str = Field("SalesforceReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceReport":
            raise ValueError("must be SalesforceReport")
        return v

    def __setattr__(self, name, value):
        if name in SalesforceReport._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "source_id",
        "report_type",
        "detail_columns",
        "organization",
        "dashboards",
    ]

    @property
    def source_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_id

    @source_id.setter
    def source_id(self, source_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_id = source_id

    @property
    def report_type(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.report_type

    @report_type.setter
    def report_type(self, report_type: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_type = report_type

    @property
    def detail_columns(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.detail_columns

    @detail_columns.setter
    def detail_columns(self, detail_columns: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.detail_columns = detail_columns

    @property
    def organization(self) -> Optional[SalesforceOrganization]:
        return None if self.attributes is None else self.attributes.organization

    @organization.setter
    def organization(self, organization: Optional[SalesforceOrganization]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.organization = organization

    @property
    def dashboards(self) -> Optional[list[SalesforceDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[list[SalesforceDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    class Attributes(Salesforce.Attributes):
        source_id: Optional[str] = Field(None, description="", alias="sourceId")
        report_type: Optional[dict[str, str]] = Field(
            None, description="", alias="reportType"
        )
        detail_columns: Optional[set[str]] = Field(
            None, description="", alias="detailColumns"
        )
        organization: Optional[SalesforceOrganization] = Field(
            None, description="", alias="organization"
        )  # relationship
        dashboards: Optional[list[SalesforceDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship

    attributes: "SalesforceReport.Attributes" = Field(
        default_factory=lambda: SalesforceReport.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikStream(QlikSpace):
    """Description"""

    type_name: str = Field("QlikStream", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikStream":
            raise ValueError("must be QlikStream")
        return v

    def __setattr__(self, name, value):
        if name in QlikStream._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


Referenceable.update_forward_refs()
AtlasGlossary.update_forward_refs()

Referenceable.Attributes.update_forward_refs()

Asset.Attributes.update_forward_refs()

DataSet.Attributes.update_forward_refs()

Connection.Attributes.update_forward_refs()

Process.Attributes.update_forward_refs()

AtlasGlossaryCategory.Attributes.update_forward_refs()

Badge.Attributes.update_forward_refs()

AccessControl.Attributes.update_forward_refs()

Namespace.Attributes.update_forward_refs()

Catalog.Attributes.update_forward_refs()

AtlasGlossary.Attributes.update_forward_refs()

AuthPolicy.Attributes.update_forward_refs()

ProcessExecution.Attributes.update_forward_refs()

AtlasGlossaryTerm.Attributes.update_forward_refs()

AuthService.Attributes.update_forward_refs()

Cloud.Attributes.update_forward_refs()

Infrastructure.Attributes.update_forward_refs()

BIProcess.Attributes.update_forward_refs()

ColumnProcess.Attributes.update_forward_refs()

Persona.Attributes.update_forward_refs()

Purpose.Attributes.update_forward_refs()

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

Tag.Attributes.update_forward_refs()

SQL.Attributes.update_forward_refs()

Google.Attributes.update_forward_refs()

Azure.Attributes.update_forward_refs()

AWS.Attributes.update_forward_refs()

DbtColumnProcess.Attributes.update_forward_refs()

Kafka.Attributes.update_forward_refs()

S3.Attributes.update_forward_refs()

ADLS.Attributes.update_forward_refs()

GCS.Attributes.update_forward_refs()

MonteCarlo.Attributes.update_forward_refs()

Metric.Attributes.update_forward_refs()

Preset.Attributes.update_forward_refs()

Mode.Attributes.update_forward_refs()

Sigma.Attributes.update_forward_refs()

Tableau.Attributes.update_forward_refs()

Looker.Attributes.update_forward_refs()

Redash.Attributes.update_forward_refs()

DataStudio.Attributes.update_forward_refs()

Metabase.Attributes.update_forward_refs()

QuickSight.Attributes.update_forward_refs()

Thoughtspot.Attributes.update_forward_refs()

PowerBI.Attributes.update_forward_refs()

MicroStrategy.Attributes.update_forward_refs()

Qlik.Attributes.update_forward_refs()

Salesforce.Attributes.update_forward_refs()

DbtModelColumn.Attributes.update_forward_refs()

DbtModel.Attributes.update_forward_refs()

DbtMetric.Attributes.update_forward_refs()

DbtSource.Attributes.update_forward_refs()

DbtProcess.Attributes.update_forward_refs()

ReadmeTemplate.Attributes.update_forward_refs()

Readme.Attributes.update_forward_refs()

File.Attributes.update_forward_refs()

Link.Attributes.update_forward_refs()

APISpec.Attributes.update_forward_refs()

APIPath.Attributes.update_forward_refs()

SnowflakeTag.Attributes.update_forward_refs()

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

DataStudioAsset.Attributes.update_forward_refs()

KafkaTopic.Attributes.update_forward_refs()

KafkaConsumerGroup.Attributes.update_forward_refs()

S3Bucket.Attributes.update_forward_refs()

S3Object.Attributes.update_forward_refs()

ADLSAccount.Attributes.update_forward_refs()

ADLSContainer.Attributes.update_forward_refs()

ADLSObject.Attributes.update_forward_refs()

GCSObject.Attributes.update_forward_refs()

GCSBucket.Attributes.update_forward_refs()

MCIncident.Attributes.update_forward_refs()

MCMonitor.Attributes.update_forward_refs()

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

MicroStrategyReport.Attributes.update_forward_refs()

MicroStrategyProject.Attributes.update_forward_refs()

MicroStrategyMetric.Attributes.update_forward_refs()

MicroStrategyCube.Attributes.update_forward_refs()

MicroStrategyDossier.Attributes.update_forward_refs()

MicroStrategyFact.Attributes.update_forward_refs()

MicroStrategyDocument.Attributes.update_forward_refs()

MicroStrategyAttribute.Attributes.update_forward_refs()

MicroStrategyVisualization.Attributes.update_forward_refs()

QlikSpace.Attributes.update_forward_refs()

QlikApp.Attributes.update_forward_refs()

QlikChart.Attributes.update_forward_refs()

QlikDataset.Attributes.update_forward_refs()

QlikSheet.Attributes.update_forward_refs()

SalesforceObject.Attributes.update_forward_refs()

SalesforceField.Attributes.update_forward_refs()

SalesforceOrganization.Attributes.update_forward_refs()

SalesforceDashboard.Attributes.update_forward_refs()

SalesforceReport.Attributes.update_forward_refs()

QlikStream.Attributes.update_forward_refs()
