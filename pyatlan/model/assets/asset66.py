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

from. asset41 import Tableau

from. asset65 import TableauProject


    
    
    




    

class TableauMetric(Tableau):
    """Description"""

    
    

    type_name: str = Field("TableauMetric", allow_mutation=False)

    @validator('type_name')
    def validate_type_name(cls, v):
        if v != "TableauMetric":
            raise ValueError('must be TableauMetric')
        return v

    
    def __setattr__(self, name, value):
            if name in TableauMetric._convenience_properties:
                return object.__setattr__(self, name, value)
            super().__setattr__( name, value)
    
    SITE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField("siteQualifiedName", "siteQualifiedName")
    """
    TBC
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField("projectQualifiedName", "projectQualifiedName")
    """
    TBC
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField("topLevelProjectQualifiedName", "topLevelProjectQualifiedName")
    """
    TBC
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField("projectHierarchy", "projectHierarchy")
    """
    TBC
    """

    
    PROJECT: ClassVar[RelationField] = RelationField("project")
    """
    TBC
    """


    
    _convenience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_qualified_name",
        "project_hierarchy",
        "project",]
    @property
    def site_qualified_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name
    @property
    def project_qualified_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.project_qualified_name

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name
    @property
    def top_level_project_qualified_name(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.top_level_project_qualified_name

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(self, top_level_project_qualified_name:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = top_level_project_qualified_name
    @property
    def project_hierarchy(self)->Optional[list[dict[str,str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy:Optional[list[dict[str,str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy
    @property
    def project(self)->Optional[TableauProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project:Optional[TableauProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(None, description='' , alias='siteQualifiedName')
        project_qualified_name: Optional[str] = Field(None, description='' , alias='projectQualifiedName')
        top_level_project_qualified_name: Optional[str] = Field(None, description='' , alias='topLevelProjectQualifiedName')
        project_hierarchy: Optional[list[dict[str,str]]] = Field(None, description='' , alias='projectHierarchy')
        project: Optional[TableauProject]= Field(None, description='',  alias='project') # relationship
        
        
    attributes: 'TableauMetric.Attributes' = Field(
        default_factory = lambda: TableauMetric.Attributes(),
        description='Map of attributes in the instance and their values. The specific keys of this map will vary by '
                    'type, so are described in the sub-types of this schema.\n',
    )




    
TableauMetric.Attributes.update_forward_refs()
