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


    
    
    




    

class Thoughtspot(BI):
    """Description"""

    
    

    type_name: str = Field("Thoughtspot", allow_mutation=False)

    @validator('type_name')
    def validate_type_name(cls, v):
        if v != "Thoughtspot":
            raise ValueError('must be Thoughtspot')
        return v

    
    def __setattr__(self, name, value):
            if name in Thoughtspot._convenience_properties:
                return object.__setattr__(self, name, value)
            super().__setattr__( name, value)
    
    THOUGHTSPOT_CHART_TYPE: ClassVar[KeywordField] = KeywordField("thoughtspotChartType", "thoughtspotChartType")
    """
    TBC
    """
    THOUGHTSPOT_QUESTION_TEXT: ClassVar[TextField] = TextField("thoughtspotQuestionText", "thoughtspotQuestionText")
    """
    TBC
    """

    


    
    _convenience_properties: ClassVar[list[str]] = [
        "thoughtspot_chart_type",
        "thoughtspot_question_text",]
    @property
    def thoughtspot_chart_type(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.thoughtspot_chart_type

    @thoughtspot_chart_type.setter
    def thoughtspot_chart_type(self, thoughtspot_chart_type:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_chart_type = thoughtspot_chart_type
    @property
    def thoughtspot_question_text(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.thoughtspot_question_text

    @thoughtspot_question_text.setter
    def thoughtspot_question_text(self, thoughtspot_question_text:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_question_text = thoughtspot_question_text

    class Attributes(BI.Attributes):
        thoughtspot_chart_type: Optional[str] = Field(None, description='' , alias='thoughtspotChartType')
        thoughtspot_question_text: Optional[str] = Field(None, description='' , alias='thoughtspotQuestionText')
        
        
    attributes: 'Thoughtspot.Attributes' = Field(
        default_factory = lambda: Thoughtspot.Attributes(),
        description='Map of attributes in the instance and their values. The specific keys of this map will vary by '
                    'type, so are described in the sub-types of this schema.\n',
    )




    
Thoughtspot.Attributes.update_forward_refs()
