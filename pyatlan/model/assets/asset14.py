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

from. asset00 import Namespace


    
    
    




    

class Collection(Namespace):
    """Description"""

    
    

    type_name: str = Field("Collection", allow_mutation=False)

    @validator('type_name')
    def validate_type_name(cls, v):
        if v != "Collection":
            raise ValueError('must be Collection')
        return v

    
    def __setattr__(self, name, value):
            if name in Collection._convenience_properties:
                return object.__setattr__(self, name, value)
            super().__setattr__( name, value)
    
    ICON: ClassVar[KeywordField] = KeywordField("icon", "icon")
    """
    TBC
    """
    ICON_TYPE: ClassVar[KeywordField] = KeywordField("iconType", "iconType")
    """
    TBC
    """

    


    
    _convenience_properties: ClassVar[list[str]] = [
        "icon",
        "icon_type",]
    @property
    def icon(self)->Optional[str]:
        return None if self.attributes is None else self.attributes.icon

    @icon.setter
    def icon(self, icon:Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon = icon
    @property
    def icon_type(self)->Optional[IconType]:
        return None if self.attributes is None else self.attributes.icon_type

    @icon_type.setter
    def icon_type(self, icon_type:Optional[IconType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon_type = icon_type

    class Attributes(Namespace.Attributes):
        icon: Optional[str] = Field(None, description='' , alias='icon')
        icon_type: Optional[IconType] = Field(None, description='' , alias='iconType')
        
        
    attributes: 'Collection.Attributes' = Field(
        default_factory = lambda: Collection.Attributes(),
        description='Map of attributes in the instance and their values. The specific keys of this map will vary by '
                    'type, so are described in the sub-types of this schema.\n',
    )




    
Collection.Attributes.update_forward_refs()
