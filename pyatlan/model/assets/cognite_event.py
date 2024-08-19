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


class CogniteEvent(Cognite):
    """Description"""

    @overload
    @classmethod
    def creator(
            cls,
            *,
            name: str,
            cognite_asset_qualified_name: str,
    ) -> CogniteEvent:
        ...

    @overload
    @classmethod
    def creator(
            cls,
            *,
            name: str,
            cognite_asset_qualified_name: str,
            connection_qualified_name: str,
    ) -> CogniteEvent:
        ...

    @classmethod
    @init_guid
    def creator(
            cls,
            *,
            name: str,
            cognite_asset_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
    ) -> CogniteEvent:
        validate_required_fields(
            ["name", "cognite_asset_qualified_name"],
            [name, cognite_asset_qualified_name],
        )
        attributes = CogniteEvent.Attributes.create(
            name=name,
            cognite_asset_qualified_name=cognite_asset_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(
            cls, *, name: str, cognite_asset_qualified_name: str
    ) -> CogniteEvent:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name,
            cognite_asset_qualified_name=cognite_asset_qualified_name,
        )

    type_name: str = Field(default="CogniteEvent", allow_mutation=False)

    @validator('type_name')
    def validate_type_name(cls, v):
        if v != "CogniteEvent":
            raise ValueError('must be CogniteEvent')
        return v

    def __setattr__(self, name, value):
        if name in CogniteEvent._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    EXTERNAL_ID: ClassVar[KeywordField] = KeywordField("externalId", "externalId")
    """

    """

    COGNITE_ASSET: ClassVar[RelationField] = RelationField("cogniteAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "external_id",
        "cognite_asset", ]

    @property
    def external_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.external_id

    @external_id.setter
    def external_id(self, external_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_id = external_id

    @property
    def cognite_asset(self) -> Optional[List[CogniteAsset]]:
        return None if self.attributes is None else self.attributes.cognite_asset

    @cognite_asset.setter
    def cognite_asset(self, cognite_asset: Optional[List[CogniteAsset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_asset = cognite_asset

    class Attributes(Cognite.Attributes):
        external_id: Optional[str] = Field(default=None, description='')
        cognite_asset: Optional[List[CogniteAsset]] = Field(default=None, description='')  # relationship

        @classmethod
        @init_guid
        def create(
                cls,
                *,
                name: str,
                cognite_asset_qualified_name: str,
                connection_qualified_name: Optional[str] = None,
        ) -> CogniteEvent.Attributes:
            validate_required_fields(
                ["name", "cognite_asset_qualified_name"],
                [name, cognite_asset_qualified_name],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    cognite_asset_qualified_name,
                    "cognite_asset_qualified_name",
                    4,
                )

            return CogniteEvent.Attributes(
                name=name,
                cognite_asset_qualified_name=cognite_asset_qualified_name,
                connection_qualified_name=connection_qualified_name or connection_qn,
                qualified_name=f"{cognite_asset_qualified_name}/{name}",
                connector_name=connector_name,
                cognite_asset=CogniteAsset.ref_by_qualified_name(
                    cognite_asset_qualified_name
                ),
            )

    attributes: CogniteEvent.Attributes = Field(
        default_factory=lambda: CogniteEvent.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cognite_asset import CogniteAsset  # noqa

CogniteEvent.Attributes.update_forward_refs()
