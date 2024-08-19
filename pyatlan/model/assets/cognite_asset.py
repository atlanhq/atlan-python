# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

import hashlib
import sys
import uuid
from json import loads
from json.decoder import JSONDecodeError
from datetime import datetime
from io import StringIO
from typing import Any, ClassVar, Dict, List, Optional, Set, Type, TypeVar, TYPE_CHECKING, cast, overload
from warnings import warn

from urllib.parse import quote, unquote

from pydantic.v1 import Field, PrivateAttr, StrictStr, root_validator, validator

from pyatlan.errors import ErrorCode
from pyatlan.model.core import Announcement, AtlanObject, AtlanTag, AtlanTagName, Meaning
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
    AtlanIcon,
    AtlasGlossaryCategoryType,
    AtlasGlossaryTermType,
    AtlasGlossaryType,
    AuthPolicyCategory,
    AuthPolicyResourceCategory,
    AuthPolicyType,
    CertificateStatus,
    DataProductCriticality,
    DataProductSensitivity,
    DataProductStatus,
    DataProductVisibility,
    DataAction,
    DynamoDBStatus,
    DynamoDBSecondaryIndexProjectionType,
    EntityStatus,
    FileType,
    GoogleDatastudioAssetType,
    IconType,
    KafkaTopicCleanupPolicy,
    KafkaTopicCompressionType,
    MatillionJobType,
    OpenLineageRunState,
    SaveSemantic,
    PersonaDomainAction,
    PersonaGlossaryAction,
    PersonaMetadataAction,
    PowerbiEndorsement,
    PurposeMetadataAction,
    QueryUsernameStrategy,
    QuickSightAnalysisStatus,
    QuickSightDatasetFieldType,
    QuickSightDatasetImportMode,
    QuickSightFolderType,
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
from pyatlan.model.internal import AtlasServer, Internal
from pyatlan.model.search import IndexSearchRequest
from pyatlan.model.structs import (
    Action,
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
    StarredDetails,
)
from pyatlan.utils import (
    init_guid,
    next_id,
    validate_required_fields,
    validate_single_required_field,
    get_parent_qualified_name,
)
from pyatlan.model.data_mesh import DataProductsAssetsDSL

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

    AtlasGlossaryCategoryType,

    AtlasGlossaryTermAssignmentStatus,

    AtlasGlossaryTermRelationshipStatus,

    AtlasGlossaryTermType,

    AtlasGlossaryType,

    AtlasOperation,

    AuthPolicyCategory,

    AuthPolicyResourceCategory,

    AuthPolicyType,

    CertificateStatus,

    DataProductCriticality,

    DataProductSensitivity,

    DataProductStatus,

    DataProductVisibility,

    DomoCardType,

    DynamoDBSecondaryIndexProjectionType,

    DynamoDBStatus,

    FileType,

    GoogleDatastudioAssetType,

    IconType,

    KafkaTopicCleanupPolicy,

    KafkaTopicCompressionType,

    MatillionJobType,

    MongoDBCollectionValidationAction,

    MongoDBCollectionValidationLevel,

    OpenLineageRunState,

    PowerbiEndorsement,

    QueryUsernameStrategy,

    QuickSightAnalysisStatus,

    QuickSightDatasetFieldType,

    QuickSightDatasetImportMode,

    QuickSightFolderType,

    SchemaRegistrySchemaCompatibility,

    SchemaRegistrySchemaType,

    SourceCostUnitType,

    WorkflowRunStatus,

    WorkflowRunType,

    WorkflowStatus,

    WorkflowType,

)

from .asset import SelfAsset

from .cognite import Cognite


class CogniteAsset(Cognite):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> CogniteAsset:
        validate_required_fields(
            ["name", "connection_qualified_name"],
            [name, connection_qualified_name],
        )
        attributes = CogniteAsset.Attributes.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, connection_qualified_name: str) -> CogniteAsset:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )

    type_name: str = Field(default="CogniteAsset", allow_mutation=False)

    @validator('type_name')
    def validate_type_name(cls, v):
        if v != "CogniteAsset":
            raise ValueError('must be CogniteAsset')
        return v

    def __setattr__(self, name, value):
        if name in CogniteAsset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    EXTERNAL_ID: ClassVar[KeywordField] = KeywordField("externalId", "externalId")
    """
    external id for an asset
    """
    COGNITE_ASSET_PARENT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField("cogniteAssetParentQualifiedName",
                                                                               "cogniteAssetParentQualifiedName")
    """
    Parent QualifiedName for an asset
    """
    COGNITE_CHILD_ASSET_COUNT: ClassVar[NumericField] = NumericField("cogniteChildAssetCount", "cogniteChildAssetCount")
    """
    Number of child in the Asset
    """

    COGNITE_EVENTS: ClassVar[RelationField] = RelationField("cogniteEvents")
    """
    TBC
    """
    COGNITE_ASSET: ClassVar[RelationField] = RelationField("cogniteAsset")
    """
    TBC
    """
    COGNITE_FILES: ClassVar[RelationField] = RelationField("cogniteFiles")
    """
    TBC
    """
    COGNITE_TIMESERIES: ClassVar[RelationField] = RelationField("cogniteTimeseries")
    """
    TBC
    """
    COGNITE_SEQUENCES: ClassVar[RelationField] = RelationField("cogniteSequences")
    """
    TBC
    """
    COGNITE3DMODELS: ClassVar[RelationField] = RelationField("cognite3dmodels")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "external_id",
        "cognite_asset_parent_qualified_name",
        "cognite_child_asset_count",
        "cognite_events",
        "cognite_asset",
        "cognite_files",
        "cognite_timeseries",
        "cognite_sequences",
        "cognite3dmodels", ]

    @property
    def external_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.external_id

    @external_id.setter
    def external_id(self, external_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_id = external_id

    @property
    def cognite_asset_parent_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cognite_asset_parent_qualified_name

    @cognite_asset_parent_qualified_name.setter
    def cognite_asset_parent_qualified_name(self, cognite_asset_parent_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_asset_parent_qualified_name = cognite_asset_parent_qualified_name

    @property
    def cognite_child_asset_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.cognite_child_asset_count

    @cognite_child_asset_count.setter
    def cognite_child_asset_count(self, cognite_child_asset_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_child_asset_count = cognite_child_asset_count

    @property
    def cognite_events(self) -> Optional[List[CogniteEvent]]:
        return None if self.attributes is None else self.attributes.cognite_events

    @cognite_events.setter
    def cognite_events(self, cognite_events: Optional[List[CogniteEvent]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_events = cognite_events

    @property
    def cognite_asset(self) -> Optional[CogniteAsset]:
        return None if self.attributes is None else self.attributes.cognite_asset

    @cognite_asset.setter
    def cognite_asset(self, cognite_asset: Optional[CogniteAsset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_asset = cognite_asset

    @property
    def cognite_files(self) -> Optional[List[CogniteFile]]:
        return None if self.attributes is None else self.attributes.cognite_files

    @cognite_files.setter
    def cognite_files(self, cognite_files: Optional[List[CogniteFile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_files = cognite_files

    @property
    def cognite_timeseries(self) -> Optional[List[CogniteTimeSeries]]:
        return None if self.attributes is None else self.attributes.cognite_timeseries

    @cognite_timeseries.setter
    def cognite_timeseries(self, cognite_timeseries: Optional[List[CogniteTimeSeries]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_timeseries = cognite_timeseries

    @property
    def cognite_sequences(self) -> Optional[List[CogniteSequence]]:
        return None if self.attributes is None else self.attributes.cognite_sequences

    @cognite_sequences.setter
    def cognite_sequences(self, cognite_sequences: Optional[List[CogniteSequence]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_sequences = cognite_sequences

    @property
    def cognite3dmodels(self) -> Optional[List[Cognite3DModel]]:
        return None if self.attributes is None else self.attributes.cognite3dmodels

    @cognite3dmodels.setter
    def cognite3dmodels(self, cognite3dmodels: Optional[List[Cognite3DModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite3dmodels = cognite3dmodels

    class Attributes(Cognite.Attributes):
        external_id: Optional[str] = Field(default=None, description='')
        cognite_asset_parent_qualified_name: Optional[str] = Field(default=None, description='')
        cognite_child_asset_count: Optional[int] = Field(default=None, description='')
        cognite_events: Optional[List[CogniteEvent]] = Field(default=None, description='')  # relationship
        cognite_asset: Optional[CogniteAsset] = Field(default=None, description='')  # relationship
        cognite_files: Optional[List[CogniteFile]] = Field(default=None, description='')  # relationship
        cognite_timeseries: Optional[List[CogniteTimeSeries]] = Field(default=None, description='')  # relationship
        cognite_sequences: Optional[List[CogniteSequence]] = Field(default=None, description='')  # relationship
        cognite3dmodels: Optional[List[Cognite3DModel]] = Field(default=None, description='')  # relationship

        @classmethod
        @init_guid
        def create(
                cls, *, name: str, connection_qualified_name: str
        ) -> CogniteAsset.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"],
                [name, connection_qualified_name],
            )
            return CogniteAsset.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: CogniteAsset.Attributes = Field(
        default_factory=lambda: CogniteAsset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cognite3_d_model import Cognite3DModel  # noqa

from .cognite_file import CogniteFile  # noqa

from .cognite_time_series import CogniteTimeSeries  # noqa

from .cognite_event import CogniteEvent  # noqa

from .cognite_sequence import CogniteSequence  # noqa

CogniteAsset.Attributes.update_forward_refs()
