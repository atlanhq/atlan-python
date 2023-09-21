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


    
    
    




    

class Sigma(BI):
    """Description"""

    
    

    type_name: str = Field("Sigma", allow_mutation=False)

    @validator('type_name')
    def validate_type_name(cls, v):
        if v != "Sigma":
            raise ValueError('must be Sigma')
        return v

    
    def __setattr__(self, name, value):
            if name in Sigma._convenience_properties:
                return object.__setattr__(self, name, value)
            super().__setattr__( name, value)
    
    SIGMA_WORKBOOK_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField("sigmaWorkbookQualifiedName", "sigmaWorkbookQualifiedName", "sigmaWorkbookQualifiedName.text")
    """
    TBC
    """
    SIGMA_WORKBOOK_NAME: ClassVar[KeywordTextField] = KeywordTextField("sigmaWorkbookName", "sigmaWorkbookName.keyword", "sigmaWorkbookName")
    """
    TBC
    """
    SIGMA_PAGE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField("sigmaPageQualifiedName", "sigmaPageQualifiedName", "sigmaPageQualifiedName.text")
    """
    TBC
    """
    SIGMA_PAGE_NAME: ClassVar[KeywordTextField] = KeywordTextField("sigmaPageName", "sigmaPageName.keyword", "sigmaPageName")
    """
    TBC
    """
    SIGMA_DATA_ELEMENT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField("sigmaDataElementQualifiedName", "sigmaDataElementQualifiedName", "sigmaDataElementQualifiedName.text")
    """
    TBC
    """
    SIGMA_DATA_ELEMENT_NAME: ClassVar[KeywordTextField] = KeywordTextField("sigmaDataElementName", "sigmaDataElementName.keyword", "sigmaDataElementName")
    """
    TBC
    """

    


    
    _convenience_properties: ClassVar[list[str]] = [
        "sigma_workbook_qualified_name",
        "sigma_workbook_name",
        "sigma_page_qualified_name",
        "sigma_page_name",
        "sigma_data_element_qualified_name",
        "sigma_data_element_name",]
    @property
    def sigma_workbook_qualified_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.sigma_workbook_qualified_name

    @sigma_workbook_qualified_name.setter
    def sigma_workbook_qualified_name(self, sigma_workbook_qualified_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_workbook_qualified_name = sigma_workbook_qualified_name
    @property
    def sigma_workbook_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.sigma_workbook_name

    @sigma_workbook_name.setter
    def sigma_workbook_name(self, sigma_workbook_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_workbook_name = sigma_workbook_name
    @property
    def sigma_page_qualified_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.sigma_page_qualified_name

    @sigma_page_qualified_name.setter
    def sigma_page_qualified_name(self, sigma_page_qualified_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_page_qualified_name = sigma_page_qualified_name
    @property
    def sigma_page_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.sigma_page_name

    @sigma_page_name.setter
    def sigma_page_name(self, sigma_page_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_page_name = sigma_page_name
    @property
    def sigma_data_element_qualified_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.sigma_data_element_qualified_name

    @sigma_data_element_qualified_name.setter
    def sigma_data_element_qualified_name(self, sigma_data_element_qualified_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_qualified_name = sigma_data_element_qualified_name
    @property
    def sigma_data_element_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.sigma_data_element_name

    @sigma_data_element_name.setter
    def sigma_data_element_name(self, sigma_data_element_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_name = sigma_data_element_name

    class Attributes(BI.Attributes):
        sigma_workbook_qualified_name: Optional[str] = Field(None, description='' , alias='sigmaWorkbookQualifiedName')
        sigma_workbook_name: Optional[str] = Field(None, description='' , alias='sigmaWorkbookName')
        sigma_page_qualified_name: Optional[str] = Field(None, description='' , alias='sigmaPageQualifiedName')
        sigma_page_name: Optional[str] = Field(None, description='' , alias='sigmaPageName')
        sigma_data_element_qualified_name: Optional[str] = Field(None, description='' , alias='sigmaDataElementQualifiedName')
        sigma_data_element_name: Optional[str] = Field(None, description='' , alias='sigmaDataElementName')
        
        
    attributes: 'Sigma.Attributes' = Field(
        default_factory = lambda: Sigma.Attributes(),
        description='Map of attributes in the instance and their values. The specific keys of this map will vary by '
                    'type, so are described in the sub-types of this schema.\n',
    )




    
Sigma.Attributes.update_forward_refs()
