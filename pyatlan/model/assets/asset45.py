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


    
    
    




    

class Metabase(BI):
    """Description"""

    
    

    type_name: str = Field("Metabase", allow_mutation=False)

    @validator('type_name')
    def validate_type_name(cls, v):
        if v != "Metabase":
            raise ValueError('must be Metabase')
        return v

    
    def __setattr__(self, name, value):
            if name in Metabase._convenience_properties:
                return object.__setattr__(self, name, value)
            super().__setattr__( name, value)
    
    METABASE_COLLECTION_NAME: ClassVar[KeywordTextField] = KeywordTextField("metabaseCollectionName", "metabaseCollectionName.keyword", "metabaseCollectionName")
    """
    TBC
    """
    METABASE_COLLECTION_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField("metabaseCollectionQualifiedName", "metabaseCollectionQualifiedName", "metabaseCollectionQualifiedName.text")
    """
    TBC
    """

    


    
    _convenience_properties: ClassVar[list[str]] = [
        "metabase_collection_name",
        "metabase_collection_qualified_name",]
    @property
    def metabase_collection_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_collection_name

    @metabase_collection_name.setter
    def metabase_collection_name(self, metabase_collection_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_collection_name = metabase_collection_name
    @property
    def metabase_collection_qualified_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_collection_qualified_name

    @metabase_collection_qualified_name.setter
    def metabase_collection_qualified_name(self, metabase_collection_qualified_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_collection_qualified_name = metabase_collection_qualified_name

    class Attributes(BI.Attributes):
        metabase_collection_name: Optional[str] = Field(None, description='' , alias='metabaseCollectionName')
        metabase_collection_qualified_name: Optional[str] = Field(None, description='' , alias='metabaseCollectionQualifiedName')
        
        
    attributes: 'Metabase.Attributes' = Field(
        default_factory = lambda: Metabase.Attributes(),
        description='Map of attributes in the instance and their values. The specific keys of this map will vary by '
                    'type, so are described in the sub-types of this schema.\n',
    )




    
Metabase.Attributes.update_forward_refs()
