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

from. asset18 import BI


    
    
    




    

class QuickSight(BI):
    """Description"""

    
    

    type_name: str = Field("QuickSight", allow_mutation=False)

    @validator('type_name')
    def validate_type_name(cls, v):
        if v != "QuickSight":
            raise ValueError('must be QuickSight')
        return v

    
    def __setattr__(self, name, value):
            if name in QuickSight._convenience_properties:
                return object.__setattr__(self, name, value)
            super().__setattr__( name, value)
    
    QUICK_SIGHT_ID: ClassVar[KeywordField] = KeywordField("quickSightId", "quickSightId")
    """
    TBC
    """
    QUICK_SIGHT_SHEET_ID: ClassVar[KeywordField] = KeywordField("quickSightSheetId", "quickSightSheetId")
    """
    TBC
    """
    QUICK_SIGHT_SHEET_NAME: ClassVar[KeywordTextField] = KeywordTextField("quickSightSheetName", "quickSightSheetName.keyword", "quickSightSheetName")
    """
    TBC
    """

    


    
    _convenience_properties: ClassVar[list[str]] = [
        "quick_sight_id",
        "quick_sight_sheet_id",
        "quick_sight_sheet_name",]
    @property
    def quick_sight_id(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.quick_sight_id

    @quick_sight_id.setter
    def quick_sight_id(self, quick_sight_id:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_id = quick_sight_id
    @property
    def quick_sight_sheet_id(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.quick_sight_sheet_id

    @quick_sight_sheet_id.setter
    def quick_sight_sheet_id(self, quick_sight_sheet_id:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_sheet_id = quick_sight_sheet_id
    @property
    def quick_sight_sheet_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.quick_sight_sheet_name

    @quick_sight_sheet_name.setter
    def quick_sight_sheet_name(self, quick_sight_sheet_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_sheet_name = quick_sight_sheet_name

    class Attributes(BI.Attributes):
        quick_sight_id: Optional[str] = Field(None, description='' , alias='quickSightId')
        quick_sight_sheet_id: Optional[str] = Field(None, description='' , alias='quickSightSheetId')
        quick_sight_sheet_name: Optional[str] = Field(None, description='' , alias='quickSightSheetName')
        
        
    attributes: 'QuickSight.Attributes' = Field(
        default_factory = lambda: QuickSight.Attributes(),
        description='Map of attributes in the instance and their values. The specific keys of this map will vary by '
                    'type, so are described in the sub-types of this schema.\n',
    )




    
QuickSight.Attributes.update_forward_refs()
