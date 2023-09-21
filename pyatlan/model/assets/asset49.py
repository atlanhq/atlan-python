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


    
    
    




    

class MicroStrategy(BI):
    """Description"""

    
    

    type_name: str = Field("MicroStrategy", allow_mutation=False)

    @validator('type_name')
    def validate_type_name(cls, v):
        if v != "MicroStrategy":
            raise ValueError('must be MicroStrategy')
        return v

    
    def __setattr__(self, name, value):
            if name in MicroStrategy._convenience_properties:
                return object.__setattr__(self, name, value)
            super().__setattr__( name, value)
    
    MICRO_STRATEGY_PROJECT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField("microStrategyProjectQualifiedName", "microStrategyProjectQualifiedName", "microStrategyProjectQualifiedName.text")
    """
    Related project qualified name
    """
    MICRO_STRATEGY_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField("microStrategyProjectName", "microStrategyProjectName.keyword", "microStrategyProjectName")
    """
    Related project name
    """
    MICRO_STRATEGY_CUBE_QUALIFIED_NAMES: ClassVar[KeywordTextField] = KeywordTextField("microStrategyCubeQualifiedNames", "microStrategyCubeQualifiedNames", "microStrategyCubeQualifiedNames.text")
    """
    Related cube qualified name list
    """
    MICRO_STRATEGY_CUBE_NAMES: ClassVar[KeywordTextField] = KeywordTextField("microStrategyCubeNames", "microStrategyCubeNames.keyword", "microStrategyCubeNames")
    """
    Related cube name list
    """
    MICRO_STRATEGY_REPORT_QUALIFIED_NAMES: ClassVar[KeywordTextField] = KeywordTextField("microStrategyReportQualifiedNames", "microStrategyReportQualifiedNames", "microStrategyReportQualifiedNames.text")
    """
    Related report qualified name list
    """
    MICRO_STRATEGY_REPORT_NAMES: ClassVar[KeywordTextField] = KeywordTextField("microStrategyReportNames", "microStrategyReportNames.keyword", "microStrategyReportNames")
    """
    Related report name list
    """
    MICRO_STRATEGY_IS_CERTIFIED: ClassVar[BooleanField] = BooleanField("microStrategyIsCertified", "microStrategyIsCertified")
    """
    Whether certified in MicroStrategy
    """
    MICRO_STRATEGY_CERTIFIED_BY: ClassVar[KeywordField] = KeywordField("microStrategyCertifiedBy", "microStrategyCertifiedBy")
    """
    User who certified in MicroStrategy
    """
    MICRO_STRATEGY_CERTIFIED_AT: ClassVar[NumericField] = NumericField("microStrategyCertifiedAt", "microStrategyCertifiedAt")
    """
    Certified date in MicroStrategy
    """
    MICRO_STRATEGY_LOCATION: ClassVar[KeywordField] = KeywordField("microStrategyLocation", "microStrategyLocation")
    """
    Location path in MicroStrategy
    """

    


    
    _convenience_properties: ClassVar[list[str]] = [
        "micro_strategy_project_qualified_name",
        "micro_strategy_project_name",
        "micro_strategy_cube_qualified_names",
        "micro_strategy_cube_names",
        "micro_strategy_report_qualified_names",
        "micro_strategy_report_names",
        "micro_strategy_is_certified",
        "micro_strategy_certified_by",
        "micro_strategy_certified_at",
        "micro_strategy_location",]
    @property
    def micro_strategy_project_qualified_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.micro_strategy_project_qualified_name

    @micro_strategy_project_qualified_name.setter
    def micro_strategy_project_qualified_name(self, micro_strategy_project_qualified_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project_qualified_name = micro_strategy_project_qualified_name
    @property
    def micro_strategy_project_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.micro_strategy_project_name

    @micro_strategy_project_name.setter
    def micro_strategy_project_name(self, micro_strategy_project_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project_name = micro_strategy_project_name
    @property
    def micro_strategy_cube_qualified_names(self)->Optional[set[str]]:
        return None if self.attributes is None else self.attributes.micro_strategy_cube_qualified_names

    @micro_strategy_cube_qualified_names.setter
    def micro_strategy_cube_qualified_names(self, micro_strategy_cube_qualified_names:Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cube_qualified_names = micro_strategy_cube_qualified_names
    @property
    def micro_strategy_cube_names(self)->Optional[set[str]]:
        return None if self.attributes is None else self.attributes.micro_strategy_cube_names

    @micro_strategy_cube_names.setter
    def micro_strategy_cube_names(self, micro_strategy_cube_names:Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cube_names = micro_strategy_cube_names
    @property
    def micro_strategy_report_qualified_names(self)->Optional[set[str]]:
        return None if self.attributes is None else self.attributes.micro_strategy_report_qualified_names

    @micro_strategy_report_qualified_names.setter
    def micro_strategy_report_qualified_names(self, micro_strategy_report_qualified_names:Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_report_qualified_names = micro_strategy_report_qualified_names
    @property
    def micro_strategy_report_names(self)->Optional[set[str]]:
        return None if self.attributes is None else self.attributes.micro_strategy_report_names

    @micro_strategy_report_names.setter
    def micro_strategy_report_names(self, micro_strategy_report_names:Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_report_names = micro_strategy_report_names
    @property
    def micro_strategy_is_certified(self)->Optional[bool]:
        return None if self.attributes is None else self.attributes.micro_strategy_is_certified

    @micro_strategy_is_certified.setter
    def micro_strategy_is_certified(self, micro_strategy_is_certified:Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_is_certified = micro_strategy_is_certified
    @property
    def micro_strategy_certified_by(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.micro_strategy_certified_by

    @micro_strategy_certified_by.setter
    def micro_strategy_certified_by(self, micro_strategy_certified_by:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_certified_by = micro_strategy_certified_by
    @property
    def micro_strategy_certified_at(self)->Optional[datetime]:
        return None if self.attributes is None else self.attributes.micro_strategy_certified_at

    @micro_strategy_certified_at.setter
    def micro_strategy_certified_at(self, micro_strategy_certified_at:Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_certified_at = micro_strategy_certified_at
    @property
    def micro_strategy_location(self)->Optional[list[dict[str,str]]]:
        return None if self.attributes is None else self.attributes.micro_strategy_location

    @micro_strategy_location.setter
    def micro_strategy_location(self, micro_strategy_location:Optional[list[dict[str,str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_location = micro_strategy_location

    class Attributes(BI.Attributes):
        micro_strategy_project_qualified_name: Optional[str] = Field(None, description='' , alias='microStrategyProjectQualifiedName')
        micro_strategy_project_name: Optional[str] = Field(None, description='' , alias='microStrategyProjectName')
        micro_strategy_cube_qualified_names: Optional[set[str]] = Field(None, description='' , alias='microStrategyCubeQualifiedNames')
        micro_strategy_cube_names: Optional[set[str]] = Field(None, description='' , alias='microStrategyCubeNames')
        micro_strategy_report_qualified_names: Optional[set[str]] = Field(None, description='' , alias='microStrategyReportQualifiedNames')
        micro_strategy_report_names: Optional[set[str]] = Field(None, description='' , alias='microStrategyReportNames')
        micro_strategy_is_certified: Optional[bool] = Field(None, description='' , alias='microStrategyIsCertified')
        micro_strategy_certified_by: Optional[str] = Field(None, description='' , alias='microStrategyCertifiedBy')
        micro_strategy_certified_at: Optional[datetime] = Field(None, description='' , alias='microStrategyCertifiedAt')
        micro_strategy_location: Optional[list[dict[str,str]]] = Field(None, description='' , alias='microStrategyLocation')
        
        
    attributes: 'MicroStrategy.Attributes' = Field(
        default_factory = lambda: MicroStrategy.Attributes(),
        description='Map of attributes in the instance and their values. The specific keys of this map will vary by '
                    'type, so are described in the sub-types of this schema.\n',
    )




    
MicroStrategy.Attributes.update_forward_refs()
