# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.




from __future__ import annotations

import hashlib
import sys
import uuid
from datetime import datetime
from io import StringIO
from typing import Any, ClassVar, Dict, List, Optional, Set, Type, TypeVar
from urllib.parse import quote, unquote

from pydantic import Field, PrivateAttr, StrictStr, root_validator, validator

from pyatlan.model.core import Announcement, AtlanObject, AtlanTag, Meaning
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
    KafkaTopicCleanupPolicy,
    KafkaTopicCompressionType,
    MatillionJobType,
    OpenLineageRunState,
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
    KeywordField,
    KeywordTextField,
    KeywordTextStemmedField,
    NumericField,
    NumericRankField,
    RelationField,
    TextField,
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
    StarredDetails,
)
from pyatlan.utils import next_id, validate_required_fields

from. asset80 import KafkaTopic


    
    
    




    

class AzureEventHub(KafkaTopic):
    """Description"""

    
    

    type_name: str = Field("AzureEventHub", allow_mutation=False)

    @validator('type_name')
    def validate_type_name(cls, v):
        if v != "AzureEventHub":
            raise ValueError('must be AzureEventHub')
        return v

    
    def __setattr__(self, name, value):
            if name in AzureEventHub._convenience_properties:
                return object.__setattr__(self, name, value)
            super().__setattr__( name, value)
    
    AZURE_EVENT_HUB_STATUS: ClassVar[KeywordField] = KeywordField("azureEventHubStatus", "azureEventHubStatus")
    """
    TBC
    """

    


    
    _convenience_properties: ClassVar[list[str]] = [
        "azure_event_hub_status",]
    @property
    def azure_event_hub_status(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.azure_event_hub_status

    @azure_event_hub_status.setter
    def azure_event_hub_status(self, azure_event_hub_status:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_event_hub_status = azure_event_hub_status

    class Attributes(KafkaTopic.Attributes):
        azure_event_hub_status: Optional[str] = Field(None, description='' , alias='azureEventHubStatus')
        
        
    attributes: 'AzureEventHub.Attributes' = Field(
        default_factory = lambda: AzureEventHub.Attributes(),
        description='Map of attributes in the instance and their values. The specific keys of this map will vary by '
                    'type, so are described in the sub-types of this schema.\n',
    )




    
AzureEventHub.Attributes.update_forward_refs()
