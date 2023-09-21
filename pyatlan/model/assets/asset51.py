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

from. asset19 import SaaS


    
    
    




    

class Salesforce(SaaS):
    """Description"""

    
    

    type_name: str = Field("Salesforce", allow_mutation=False)

    @validator('type_name')
    def validate_type_name(cls, v):
        if v != "Salesforce":
            raise ValueError('must be Salesforce')
        return v

    
    def __setattr__(self, name, value):
            if name in Salesforce._convenience_properties:
                return object.__setattr__(self, name, value)
            super().__setattr__( name, value)
    
    ORGANIZATION_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField("organizationQualifiedName", "organizationQualifiedName")
    """
    TBC
    """
    API_NAME: ClassVar[KeywordTextField] = KeywordTextField("apiName", "apiName.keyword", "apiName")
    """
    TBC
    """

    


    
    _convenience_properties: ClassVar[list[str]] = [
        "organization_qualified_name",
        "api_name",]
    @property
    def organization_qualified_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.organization_qualified_name

    @organization_qualified_name.setter
    def organization_qualified_name(self, organization_qualified_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.organization_qualified_name = organization_qualified_name
    @property
    def api_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.api_name

    @api_name.setter
    def api_name(self, api_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_name = api_name

    class Attributes(SaaS.Attributes):
        organization_qualified_name: Optional[str] = Field(None, description='' , alias='organizationQualifiedName')
        api_name: Optional[str] = Field(None, description='' , alias='apiName')
        
        
    attributes: 'Salesforce.Attributes' = Field(
        default_factory = lambda: Salesforce.Attributes(),
        description='Map of attributes in the instance and their values. The specific keys of this map will vary by '
                    'type, so are described in the sub-types of this schema.\n',
    )




    
Salesforce.Attributes.update_forward_refs()
