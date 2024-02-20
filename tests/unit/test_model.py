# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import json
from datetime import datetime
from inspect import signature
from pathlib import Path
from unittest.mock import create_autospec

import pytest

# from deepdiff import DeepDiff
from pydantic.v1.error_wrappers import ValidationError

import pyatlan.cache.atlan_tag_cache
from pyatlan.errors import InvalidRequestError
from pyatlan.model.assets import (
    SQL,
    AccessControl,
    ADLSAccount,
    ADLSContainer,
    ADLSObject,
    AirflowDag,
    AirflowTask,
    APIPath,
    APISpec,
    Asset,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    AuthPolicy,
    Column,
    ColumnProcess,
    Database,
    DbtMetric,
    DbtModel,
    DbtModelColumn,
    DbtSource,
    DbtTest,
    File,
    Folder,
    Function,
    GCSBucket,
    GCSObject,
    KafkaConsumerGroup,
    KafkaTopic,
    Link,
    LookerDashboard,
    LookerExplore,
    LookerField,
    LookerFolder,
    LookerLook,
    LookerModel,
    LookerProject,
    LookerQuery,
    LookerTile,
    LookerView,
    MaterialisedView,
    MatillionComponent,
    MatillionGroup,
    MatillionJob,
    MatillionProject,
    MCIncident,
    MCMonitor,
    MetabaseCollection,
    MetabaseDashboard,
    MetabaseQuestion,
    Metric,
    MicroStrategyAttribute,
    MicroStrategyCube,
    MicroStrategyDocument,
    MicroStrategyDossier,
    MicroStrategyFact,
    MicroStrategyMetric,
    MicroStrategyProject,
    MicroStrategyReport,
    MicroStrategyVisualization,
    ModeChart,
    ModeCollection,
    ModeQuery,
    ModeReport,
    ModeWorkspace,
    MongoDBCollection,
    MongoDBDatabase,
    Namespace,
    PowerBIColumn,
    PowerBIDashboard,
    PowerBIDataflow,
    PowerBIDataset,
    PowerBIDatasource,
    PowerBIMeasure,
    PowerBIPage,
    PowerBIReport,
    PowerBITable,
    PowerBITile,
    PowerBIWorkspace,
    PresetChart,
    PresetDashboard,
    PresetDataset,
    PresetWorkspace,
    Procedure,
    Process,
    QlikApp,
    QlikChart,
    QlikDataset,
    QlikSheet,
    QlikSpace,
    Query,
    QuickSightAnalysis,
    QuickSightAnalysisVisual,
    QuickSightDashboard,
    QuickSightDashboardVisual,
    QuickSightDataset,
    QuickSightDatasetField,
    QuickSightFolder,
    Readme,
    RedashQuery,
    RedashVisualization,
    Referenceable,
    S3Bucket,
    S3Object,
    SalesforceDashboard,
    SalesforceField,
    SalesforceObject,
    SalesforceOrganization,
    SalesforceReport,
    Schema,
    SchemaRegistrySubject,
    SigmaDataElement,
    SigmaDataElementField,
    SigmaDataset,
    SigmaDatasetColumn,
    SigmaPage,
    SigmaWorkbook,
    SnowflakeDynamicTable,
    SnowflakePipe,
    SnowflakeStream,
    SnowflakeTag,
    SodaCheck,
    Table,
    TableauCalculatedField,
    TableauDashboard,
    TableauDatasource,
    TableauDatasourceField,
    TableauFlow,
    TableauProject,
    TableauSite,
    TableauWorkbook,
    TableauWorksheet,
    TablePartition,
    ThoughtspotDashlet,
    ThoughtspotLiveboard,
    View,
)
from pyatlan.model.constants import DELETED_
from pyatlan.model.core import Announcement
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
    AuthPolicyType,
    BadgeComparisonOperator,
    BadgeConditionColor,
    CertificateStatus,
    FileType,
    GoogleDatastudioAssetType,
    IconType,
    KafkaTopicCleanupPolicy,
    KafkaTopicCompressionType,
    MatillionJobType,
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
from pyatlan.model.typedef import TypeDefResponse
from pyatlan.utils import validate_single_required_field

CM_ATTR_ID = "WQ6XGXwq9o7UnZlkWyKhQN"

CM_ID = "scAesIb5UhKQdTwu4GuCSN"

SCHEMA_QUALIFIED_NAME = "default/snowflake/1646836521/ATLAN_SAMPLE_DATA/FOOD_BEVERAGE"

TABLE_NAME = "MKT_EXPENSES"

TABLE_URL = "POsWut55wIYsXZ5v4z3K98"

FRESHNESS = "VdRC4dyNdTJHfFjCiNaKt9"

MONTE_CARLO = "AFq4ctARP76ctapiTbuT92"

MOON = "FAq4ctARP76ctapiTbuT92"

BADGE_CONDITION = BadgeCondition.create(
    badge_condition_operator=BadgeComparisonOperator.EQ,
    badge_condition_value="1",
    badge_condition_colorhex=BadgeConditionColor.RED,
)
DATA_DIR = Path(__file__).parent / "data"
GLOSSARY_JSON = "glossary.json"
GLOSSARY_TERM_JSON = "glossary_term.json"
GLOSSARY_CATEGORY_JSON = "glossary_category.json"
STRING_VALUE = "Bob"
INT_VALUE = 42
FLOAT_VALUE = 42.00
ATTRIBUTE_VALUES_BY_TYPE = {
    "str": STRING_VALUE,
    "Optional[Set[str]]": {STRING_VALUE},
    "Optional[str]": STRING_VALUE,
    "Optional[datetime]": datetime.now(),
    "Optional[bool]": True,
    "Optional[CertificateStatus]": CertificateStatus.DRAFT,
    "Optional[int]": INT_VALUE,
    "Optional[float]": FLOAT_VALUE,
    "Optional[Dict[str, str]]": {STRING_VALUE: STRING_VALUE},
    "Optional[Dict[str, int]]": {STRING_VALUE: INT_VALUE},
    "Optional[List[AtlasServer]]": [AtlasServer()],
    "Optional[SourceCostUnitType]": SourceCostUnitType.CREDITS,
    "Optional[List[PopularityInsights]]": [PopularityInsights()],
    "Optional[QueryUsernameStrategy]": QueryUsernameStrategy.CONNECTION_USERNAME,
    "Optional[List[GoogleLabel]]": [
        GoogleLabel(google_label_key="", google_label_value="")
    ],
    "Optional[List[GoogleTag]]": [GoogleTag(google_tag_key="", google_tag_value="")],
    "Optional[GoogleDatastudioAssetType]": GoogleDatastudioAssetType.REPORT,
    "Optional[List[AzureTag]]": [AzureTag(azure_tag_key="", azure_tag_value="")],
    "Optional[List[AwsTag]]": [AwsTag(aws_tag_key="", aws_tag_value="")],
    "Optional[List[Catalog]]": [S3Object()],
    "Optional[List[BadgeCondition]]": [BadgeCondition()],
    "Optional[IconType]": IconType.EMOJI,
    "Optional[ADLSAccessTier]": ADLSAccessTier.HOT,
    "Optional[ADLSStorageKind]": ADLSStorageKind.STORAGE_V2,
    "Optional[ADLSPerformance]": ADLSPerformance.STANDARD,
    "Optional[ADLSProvisionState]": ADLSProvisionState.SUCCEEDED,
    "Optional[ADLSReplicationType]": ADLSReplicationType.GRS,
    "Optional[ADLSEncryptionTypes]": ADLSEncryptionTypes.MICROSOFT_STORAGE,
    "Optional[ADLSAccountStatus]": ADLSAccountStatus.AVAILABLE,
    "Optional[ADLSLeaseState]": ADLSLeaseState.LEASED,
    "Optional[ADLSLeaseStatus]": ADLSLeaseStatus.LOCKED,
    "Optional[ADLSObjectArchiveStatus]": ADLSObjectArchiveStatus.REHYDRATE_PENDING_TO_HOT,
    "Optional[ADLSObjectType]": ADLSObjectType.PAGE_BLOB,
    "Optional[PowerbiEndorsement]": PowerbiEndorsement.PROMOTED,
    "Optional[List[Dict[str, str]]]": [{STRING_VALUE: STRING_VALUE}],
    "Optional[List[DbtMetricFilter]]": [DbtMetricFilter()],
    "Optional[List[SourceTagAttribute]]": [SourceTagAttribute()],
    "Optional[Histogram]": Histogram(boundaries={0.0}, frequencies={0.0}),
    "Optional[List[ColumnValueFrequencyMap]]": [ColumnValueFrequencyMap()],
    "Optional[KafkaTopicCompressionType]": KafkaTopicCompressionType.GZIP,
    "Optional[MCRuleSchedule]": MCRuleSchedule(),
    "Optional[List[MCRuleComparison]]": [MCRuleComparison()],
    "Optional[QuickSightFolderType]": QuickSightFolderType.SHARED,
    "Optional[QuickSightDatasetFieldType]": QuickSightDatasetFieldType.STRING,
    "Optional[QuickSightAnalysisStatus]": QuickSightAnalysisStatus.CREATION_FAILED,
    "Optional[QuickSightDatasetImportMode]": QuickSightDatasetImportMode.SPICE,
    "Optional[List[KafkaTopicConsumption]]": [KafkaTopicConsumption()],
    "List[AtlasGlossaryTerm]": [AtlasGlossaryTerm()],
    "Optional[List[AtlasGlossaryTerm]]": [AtlasGlossaryTerm()],
    "Optional[List[AtlasGlossaryCategory]]": [AtlasGlossaryCategory()],
    "Optional[List[File]]": [File()],
    "Optional[List[Link]]": [Link()],
    "Optional[List[MCIncident]]": [MCIncident()],
    "Optional[List[MCMonitor]]": [MCMonitor()],
    "Optional[List[Metric]]": [Metric()],
    "Optional[Readme]": Readme(),
    "AtlasGlossary": AtlasGlossary(),
    "Optional[List[Referenceable]]": [Referenceable()],
    "Optional[List[Process]]": [Process()],
    "Optional[GCSBucket]": GCSBucket(),
    "Optional[List[GCSObject]]": [GCSObject()],
    "Optional[List[ColumnProcess]]": [ColumnProcess()],
    "Optional[Process]": Process(),
    "Optional[AtlasGlossaryCategory]": AtlasGlossaryCategory(),
    "Optional[List[Folder]]": [Folder()],
    "Optional[List[Query]]": [Query()],
    "Namespace": Namespace(),
    "Optional[List[KafkaConsumerGroup]]": [KafkaConsumerGroup()],
    "Optional[List[KafkaTopic]]": [KafkaTopic()],
    "Optional[List[ADLSContainer]]": [ADLSContainer()],
    "Optional[ADLSAccount]": ADLSAccount(),
    "Optional[List[ADLSObject]]": [ADLSObject()],
    "Optional[ADLSContainer]": ADLSContainer(),
    "Optional[List[S3Object]]": [S3Object()],
    "Optional[S3Bucket]": S3Bucket(),
    "Optional[List[Asset]]": [Asset()],
    "Optional[MCMonitor]": MCMonitor(),
    "Optional[List[Column]]": [Column()],
    "Optional[Column]": Column(),
    "Optional[MetabaseCollection]": MetabaseCollection(),
    "Optional[List[MetabaseDashboard]]": [MetabaseDashboard()],
    "Optional[List[MetabaseQuestion]]": [MetabaseQuestion()],
    "Optional[List[QuickSightAnalysis]]": [QuickSightAnalysis()],
    "Optional[List[QuickSightDashboard]]": [QuickSightDashboard()],
    "Optional[List[QuickSightDataset]]": [QuickSightDataset()],
    "Optional[QuickSightDataset]": QuickSightDataset(),
    "Optional[List[QuickSightFolder]]": [QuickSightFolder()],
    "Optional[List[QuickSightAnalysisVisual]]": [QuickSightAnalysisVisual()],
    "Optional[List[QuickSightDashboardVisual]]": [QuickSightDashboardVisual()],
    "Optional[List[QuickSightDatasetField]]": [QuickSightDatasetField()],
    "Optional[QuickSightDashboard]": QuickSightDashboard(),
    "Optional[QuickSightAnalysis]": QuickSightAnalysis(),
    "Optional[List[ThoughtspotDashlet]]": [ThoughtspotDashlet()],
    "Optional[ThoughtspotLiveboard]": ThoughtspotLiveboard(),
    "Optional[PowerBIDataset]": PowerBIDataset(),
    "Optional[List[PowerBIPage]]": [PowerBIPage()],
    "Optional[List[PowerBITile]]": [PowerBITile()],
    "Optional[PowerBIWorkspace]": PowerBIWorkspace(),
    "Optional[PowerBITable]": PowerBITable(),
    "Optional[List[PowerBIColumn]]": [PowerBIColumn()],
    "Optional[List[PowerBIMeasure]]": [PowerBIMeasure()],
    "Optional[PowerBIDashboard]": PowerBIDashboard(),
    "Optional[PowerBIReport]": PowerBIReport(),
    "Optional[List[PowerBIDataset]]": [PowerBIDataset()],
    "Optional[List[PowerBIDashboard]]": [PowerBIDashboard()],
    "Optional[List[PowerBIDataflow]]": [PowerBIDataflow()],
    "Optional[List[PowerBIReport]]": [PowerBIReport()],
    "Optional[List[PowerBIDatasource]]": [PowerBIDatasource()],
    "Optional[List[PowerBITable]]": [PowerBITable()],
    "Optional[PresetDashboard]": PresetDashboard(),
    "Optional[List[PresetChart]]": [PresetChart()],
    "Optional[List[PresetDataset]]": [PresetDataset()],
    "Optional[PresetWorkspace]": PresetWorkspace(),
    "Optional[List[PresetDashboard]]": [PresetDashboard()],
    "Optional[List[ModeCollection]]": [ModeCollection()],
    "Optional[List[ModeQuery]]": [ModeQuery()],
    "Optional[List[ModeChart]]": [ModeChart()],
    "Optional[ModeReport]": ModeReport(),
    "Optional[ModeQuery]": ModeQuery(),
    "Optional[List[ModeReport]]": [ModeReport()],
    "Optional[ModeWorkspace]": ModeWorkspace(),
    "Optional[SigmaDataset]": SigmaDataset(),
    "Optional[List[SigmaDatasetColumn]]": [SigmaDatasetColumn()],
    "Optional[List[SigmaPage]]": [SigmaPage()],
    "Optional[SigmaDataElement]": SigmaDataElement(),
    "Optional[List[SigmaDataElement]]": [SigmaDataElement()],
    "Optional[SigmaWorkbook]": SigmaWorkbook(),
    "Optional[List[SigmaDataElementField]]": [SigmaDataElementField()],
    "Optional[SigmaPage]": SigmaPage(),
    "Optional[List[QlikApp]]": [QlikApp()],
    "Optional[List[QlikDataset]]": [QlikDataset()],
    "Optional[List[QlikSheet]]": [QlikSheet()],
    "Optional[QlikSpace]": QlikSpace(),
    "Optional[QlikSheet]": QlikSheet(),
    "Optional[QlikApp]": QlikApp(),
    "Optional[List[QlikChart]]": [QlikChart()],
    "Optional[List[TableauDashboard]]": [TableauDashboard()],
    "Optional[List[TableauDatasource]]": [TableauDatasource()],
    "Optional[TableauProject]": TableauProject(),
    "Optional[List[TableauWorksheet]]": [TableauWorksheet()],
    "Optional[TableauDatasource]": TableauDatasource(),
    "Optional[List[TableauProject]]": [TableauProject()],
    "Optional[List[TableauFlow]]": [TableauFlow()],
    "Optional[TableauSite]": TableauSite(),
    "Optional[List[TableauWorkbook]]": [TableauWorkbook()],
    "Optional[List[TableauDatasourceField]]": [TableauDatasourceField()],
    "Optional[TableauWorkbook]": TableauWorkbook(),
    "Optional[List[TableauCalculatedField]]": [TableauCalculatedField()],
    "Optional[LookerDashboard]": LookerDashboard(),
    "Optional[LookerFolder]": LookerFolder(),
    "Optional[LookerModel]": LookerModel(),
    "Optional[LookerQuery]": LookerQuery(),
    "Optional[LookerTile]": LookerTile(),
    "Optional[List[LookerTile]]": [LookerTile()],
    "Optional[List[LookerDashboard]]": [LookerDashboard()],
    "Optional[List[LookerLook]]": [LookerLook()],
    "Optional[LookerLook]": LookerLook(),
    "Optional[List[LookerExplore]]": [LookerExplore()],
    "Optional[List[LookerField]]": [LookerField()],
    "Optional[LookerProject]": LookerProject(),
    "Optional[List[LookerQuery]]": [LookerQuery()],
    "Optional[List[LookerModel]]": [LookerModel()],
    "Optional[List[LookerView]]": [LookerView()],
    "Optional[LookerView]": LookerView(),
    "Optional[LookerExplore]": LookerExplore(),
    "Optional[List[RedashVisualization]]": [RedashVisualization()],
    "Optional[RedashQuery]": RedashQuery(),
    "Optional[List[SalesforceField]]": [SalesforceField()],
    "Optional[SalesforceOrganization]": SalesforceOrganization(),
    "Optional[List[SalesforceObject]]": [SalesforceObject()],
    "Optional[SalesforceObject]": SalesforceObject(),
    "Optional[List[SalesforceDashboard]]": [SalesforceDashboard()],
    "Optional[List[SalesforceReport]]": [SalesforceReport()],
    "Optional[DbtModel]": DbtModel(),
    "Optional[List[DbtMetric]]": [DbtMetric()],
    "Optional[List[DbtModelColumn]]": [DbtModelColumn()],
    "Optional[List[SQL]]": [SQL()],
    "Optional[SQL]": SQL(),
    "Optional[Asset]": Asset(),
    "Optional[Internal]": Internal(),
    "Optional[List[Readme]]": [Readme()],
    "Optional[FileType]": FileType.CSV,
    "Optional[List[APIPath]]": [APIPath()],
    "Optional[APISpec]": APISpec(),
    "Optional[Schema]": Schema(),
    "Optional[List[DbtModel]]": [DbtModel()],
    "Optional[List[DbtSource]]": [DbtSource()],
    "Optional[Table]": Table(),
    "Optional[List[TablePartition]]": [TablePartition()],
    "Optional[List[Table]]": [Table()],
    "Optional[List[View]]": [View()],
    "Optional[MaterialisedView]": MaterialisedView(),
    "Optional[TablePartition]": TablePartition(),
    "Optional[View]": View(),
    "Optional[Database]": Database(),
    "Optional[List[MaterialisedView]]": [MaterialisedView()],
    "Optional[List[Procedure]]": [Procedure()],
    "Optional[List[SnowflakePipe]]": [SnowflakePipe()],
    "Optional[List[SnowflakeStream]]": [SnowflakeStream()],
    "Optional[List[SnowflakeTag]]": [SnowflakeTag()],
    "Optional[List[Schema]]": [Schema()],
    "Optional[AuthPolicyType]": AuthPolicyType.ALLOW,
    "Optional[List[MicroStrategyAttribute]]": [MicroStrategyAttribute()],
    "Optional[List[MicroStrategyMetric]]": [MicroStrategyMetric()],
    "Optional[MicroStrategyProject]": MicroStrategyProject(),
    "Optional[List[MicroStrategyCube]]": [MicroStrategyCube()],
    "Optional[List[MicroStrategyDocument]]": [MicroStrategyDocument()],
    "Optional[List[MicroStrategyDossier]]": [MicroStrategyDossier()],
    "Optional[List[MicroStrategyFact]]": [MicroStrategyFact()],
    "Optional[List[MicroStrategyReport]]": [MicroStrategyReport()],
    "Optional[List[MicroStrategyVisualization]]": [MicroStrategyVisualization()],
    "Optional[MicroStrategyDossier]": MicroStrategyDossier(),
    "Optional[List[AuthPolicy]]": [AuthPolicy()],
    "Optional[AccessControl]": AccessControl(),
    "Optional[List[AuthPolicyCondition]]": [
        AuthPolicyCondition(policy_condition_type="", policy_condition_values={""})
    ],
    "Optional[List[AuthPolicyValiditySchedule]]": [
        AuthPolicyValiditySchedule(
            policy_validity_schedule_start_time="",
            policy_validity_schedule_timezone="",
            policy_validity_schedule_end_time="",
        )
    ],
    "Optional[List[SchemaRegistrySubject]]": [SchemaRegistrySubject()],
    "Optional[List[StarredDetails]]": [StarredDetails()],
    "Optional[List[SodaCheck]]": [SodaCheck()],
    "Optional[SchemaRegistrySchemaCompatibility]": SchemaRegistrySchemaCompatibility.FULL,
    "Optional[List[DbtTest]]": [DbtTest()],
    "Optional[AirflowTask]": AirflowTask(),
    "Optional[List[AirflowTask]]": [AirflowTask()],
    "Optional[AirflowDag]": AirflowDag(),
    "Optional[OpenLineageRunState]": OpenLineageRunState.RUNNING,
    "Optional[List[Function]]": [Function()],
    "Optional[SchemaRegistrySchemaType]": SchemaRegistrySchemaType.PROTOBUF,
    "Optional[KafkaTopicCleanupPolicy]": KafkaTopicCleanupPolicy.DELETE,
    "Optional[List[SnowflakeDynamicTable]]": [SnowflakeDynamicTable()],
    "Optional[SnowflakeDynamicTable]": SnowflakeDynamicTable(),
    "Optional[AtlasGlossary]": AtlasGlossary(),
    "Optional[Namespace]": Namespace(),
    "Optional[MatillionComponent]": MatillionComponent(),
    "Optional[MongoDBDatabase]": MongoDBDatabase(),
    "Optional[List[MatillionProject]]": [MatillionProject()],
    "Optional[MatillionProject]": MatillionProject(),
    "Optional[List[MatillionComponent]]": [MatillionComponent()],
    "Optional[List[MongoDBCollection]]": [MongoDBCollection()],
    "Optional[MatillionJobType]": MatillionJobType.ORCHESTRATION,
    "Optional[MatillionGroup]": MatillionGroup(),
    "Optional[List[MatillionJob]]": [MatillionJob()],
    "Optional[MatillionJob]": MatillionJob(),
    "Optional[List[LookerFolder]]": [LookerFolder()],
    "Optional[List[AtlanTagName]]": [],
    "List[str]": [],
}


def load_json(filename):
    with (DATA_DIR / filename).open() as input_file:
        return json.load(input_file)


def get_all_subclasses(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


@pytest.fixture()
def glossary_json():
    return load_json(GLOSSARY_JSON)


@pytest.fixture()
def glossary(glossary_json):
    return AtlasGlossary(**glossary_json)


@pytest.fixture()
def announcement():
    return Announcement(
        announcement_title="Important Announcement",
        announcement_message="Very important info",
        announcement_type=AnnouncementType.ISSUE,
    )


@pytest.fixture()
def table():
    return Table.create(
        name=TABLE_NAME,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    )


@pytest.fixture()
def type_def_response():
    data = {
        "enumDefs": [],
        "structDefs": [],
        "classificationDefs": [],
        "entityDefs": [],
        "relationshipDefs": [],
        "businessMetadataDefs": [
            {
                "category": "BUSINESS_METADATA",
                "guid": "733fcf3a-30f3-4ecc-8e4a-02a8bac775ea",
                "createdBy": "markpavletich",
                "updatedBy": "ernest",
                "createTime": 1649133333317,
                "updateTime": 1659328396300,
                "version": 7,
                "name": "AFq4ctARP76ctapiTbuT92",
                "description": "Data from Monte Carlo",
                "typeVersion": "1.0",
                "options": {
                    "imageId": "b053efca-c5b1-43f3-8dd3-b1e81dc47b70",
                    "logoType": "image",
                    "emoji": None,
                },
                "attributeDefs": [
                    {
                        "name": "POsWut55wIYsXZ5v4z3K98",
                        "typeName": "string",
                        "isOptional": True,
                        "cardinality": "SINGLE",
                        "valuesMinCount": 0,
                        "valuesMaxCount": 1,
                        "isUnique": False,
                        "isIndexable": True,
                        "includeInNotification": False,
                        "skipScrubbing": False,
                        "searchWeight": -1,
                        "indexType": "STRING",
                        "options": {
                            "showInOverview": "false",
                            "enumType": "",
                            "isEnum": "false",
                            "description": "https://getmontecarlo.com/catalog/",
                            "multiValueSelect": "false",
                            "customType": "url",
                            "customApplicableEntityTypes": '["Query","Folder","Collection",'
                            '"Database","Schema","View","Table","TablePartition",'
                            '"MaterialisedView","Column"]',
                            "allowSearch": "false",
                            "maxStrLength": "100000000",
                            "allowFiltering": "true",
                            "applicableEntityTypes": '["Asset"]',
                            "primitiveType": "url",
                        },
                        "displayName": "Table URL",
                        "isDefaultValueNull": False,
                        "indexTypeESConfig": {"normalizer": "atlan_normalizer"},
                        "indexTypeESFields": {
                            "text": {"analyzer": "atlan_text_analyzer", "type": "text"}
                        },
                    },
                    {
                        "name": "VdRC4dyNdTJHfFjCiNaKt9",
                        "typeName": "Data Freshness",
                        "isOptional": True,
                        "cardinality": "SINGLE",
                        "valuesMinCount": 0,
                        "valuesMaxCount": 1,
                        "isUnique": False,
                        "isIndexable": True,
                        "includeInNotification": False,
                        "skipScrubbing": False,
                        "searchWeight": -1,
                        "indexType": "STRING",
                        "options": {
                            "customApplicableEntityTypes": '["Database","Schema","View","Table","TablePartition",'
                            '"MaterialisedView","Column"]',
                            "showInOverview": "false",
                            "enumType": "Data Freshness",
                            "allowSearch": "false",
                            "maxStrLength": "100000000",
                            "isEnum": "true",
                            "allowFiltering": "true",
                            "applicableEntityTypes": '["Asset"]',
                            "multiValueSelect": "false",
                            "primitiveType": "enum",
                        },
                        "displayName": "Freshness",
                        "isDefaultValueNull": False,
                        "indexTypeESConfig": {"normalizer": "atlan_normalizer"},
                        "indexTypeESFields": {
                            "text": {"analyzer": "atlan_text_analyzer", "type": "text"}
                        },
                    },
                    {
                        "name": "loYJQi6ycokTirQTGVCHpD",
                        "typeName": "date",
                        "isOptional": True,
                        "cardinality": "SINGLE",
                        "valuesMinCount": 0,
                        "valuesMaxCount": 1,
                        "isUnique": False,
                        "isIndexable": True,
                        "includeInNotification": False,
                        "skipScrubbing": False,
                        "searchWeight": -1,
                        "options": {
                            "customApplicableEntityTypes": '["Database","Schema","View","Table","TablePartition",'
                            '"MaterialisedView","Column","Query","Folder","Collection",'
                            '"Process","ColumnProcess","BIProcess","AtlasGlossary","AtlasGlossaryTerm",'
                            '"AtlasGlossaryCategory"]',
                            "showInOverview": "false",
                            "enumType": "",
                            "allowSearch": "false",
                            "maxStrLength": "100000000",
                            "isEnum": "false",
                            "allowFiltering": "true",
                            "applicableEntityTypes": '["Asset"]',
                            "multiValueSelect": "false",
                            "primitiveType": "date",
                        },
                        "displayName": "Freshness Date",
                        "isDefaultValueNull": False,
                        "indexTypeESFields": {
                            "date": {"format": "epoch_millis", "type": "date"}
                        },
                    },
                ],
                "displayName": "Monte Carlo",
            },
            {
                "category": "BUSINESS_METADATA",
                "guid": "833fcf3a-30f3-4ecc-8e4a-02a8bac775ea",
                "createdBy": "markpavletich",
                "updatedBy": "ernest",
                "createTime": 1649133333317,
                "updateTime": 1659328396300,
                "version": 7,
                "name": "FAq4ctARP76ctapiTbuT92",
                "description": "Data from Moon",
                "typeVersion": "1.0",
                "options": {
                    "imageId": "b053efca-c5b1-43f3-8dd3-b1e81dc47b70",
                    "logoType": "image",
                    "emoji": None,
                },
                "attributeDefs": [
                    {
                        "name": "dVRC4dyNdTJHfFjCiNaKt9",
                        "typeName": "Data Freshness",
                        "isOptional": True,
                        "cardinality": "SINGLE",
                        "valuesMinCount": 0,
                        "valuesMaxCount": 1,
                        "isUnique": False,
                        "isIndexable": True,
                        "includeInNotification": False,
                        "skipScrubbing": False,
                        "searchWeight": -1,
                        "indexType": "STRING",
                        "options": {
                            "customApplicableEntityTypes": '["Database"]',
                            "showInOverview": "false",
                            "enumType": "",
                            "allowSearch": "false",
                            "maxStrLength": "100000000",
                            "isEnum": "true",
                            "allowFiltering": "true",
                            "applicableEntityTypes": '["Database"]',
                            "multiValueSelect": "false",
                            "primitiveType": "text",
                        },
                        "displayName": "Name",
                        "isDefaultValueNull": False,
                        "indexTypeESConfig": {"normalizer": "atlan_normalizer"},
                        "indexTypeESFields": {
                            "text": {"analyzer": "atlan_text_analyzer", "type": "text"}
                        },
                    }
                ],
                "displayName": "Moon",
            },
        ],
    }
    return TypeDefResponse(**data)


@pytest.fixture()
def glossary_term_json():
    return load_json(GLOSSARY_TERM_JSON)


@pytest.fixture()
def glossary_category_json():
    return load_json(GLOSSARY_CATEGORY_JSON)


def test_wrong_json(glossary_json):
    with pytest.raises(ValidationError):
        AtlasGlossaryTerm(**glossary_json)


@pytest.fixture(scope="function")
def the_json(request):
    return load_json(request.param)


@pytest.mark.parametrize(
    "clazz, method_name, property_names, values",
    [
        (clazz, attribute_info[1], attribute_info[2:], attribute_info[0])
        for clazz in get_all_subclasses(Asset.Attributes)
        for attribute_info in [
            (["abc"], "remove_description", "description"),
            (["abc"], "remove_user_description", "user_description"),
            ([["bob"], ["dave"]], "remove_owners", "owner_groups", "owner_users"),
            (
                [CertificateStatus.DRAFT, "some message"],
                "remove_certificate",
                "certificate_status",
                "certificate_status_message",
            ),
            (
                ["a message", "a title", "issue"],
                "remove_announcement",
                "announcement_message",
                "announcement_title",
                "announcement_type",
            ),
        ]
    ],
)
def test_remove_desscription(clazz, method_name, property_names, values):
    attributes = clazz()
    for property, value in zip(property_names, values):
        setattr(attributes, property, value)
    getattr(attributes, method_name)()
    for property in property_names:
        assert getattr(attributes, property) is None


@pytest.mark.parametrize(
    "clazz, method_name",
    [
        (clazz, method_name)
        for clazz in get_all_subclasses(Asset)
        for method_name in [
            "remove_description",
            "remove_user_description",
            "remove_owners",
            "remove_certificate",
            "remove_owners",
            "remove_announcement",
        ]
    ],
)
def test_class_remove_methods(clazz, method_name):
    mock_attributes = create_autospec(clazz.Attributes)
    sut = clazz(attributes=mock_attributes)
    sut.remove_owners()
    sut.attributes.remove_owners.assert_called_once()


@pytest.fixture()
def attribute_value(request):
    sig = signature(getattr(request.param[0], request.param[1]).fget)
    return ATTRIBUTE_VALUES_BY_TYPE[sig.return_annotation]


@pytest.mark.parametrize(
    "clazz, property_name, attribute_value",
    [
        (asset_type, property_name, (asset_type, property_name))
        for asset_type in get_all_subclasses(Asset)
        for property_name in [
            p
            for p in dir(asset_type)
            if isinstance(getattr(asset_type, p) and p != "atlan_tag_names", property)
        ]
    ],
    indirect=["attribute_value"],
)
def test_attributes(
    clazz,
    property_name,
    attribute_value,
    mock_group_cache,
    mock_role_cache,
    mock_user_cache,
):
    local_ns = {}
    sut = clazz(attributes=clazz.Attributes())
    exec(f"sut.{property_name} = attribute_value")
    exec(
        f"ret_value = sut.{property_name}",
        {"sut": sut, "property_name": property_name},
        local_ns,
    )
    assert attribute_value == local_ns["ret_value"]
    exec(
        f"ret_value = sut.attributes.{property_name if property_name != 'assigned_terms' else 'meanings'}",
        {"sut": sut, "property_name": property_name},
        local_ns,
    )
    assert attribute_value == local_ns["ret_value"]


@pytest.mark.parametrize(
    "names, values, message",
    [
        (
            ("one", "two"),
            (None, None),
            "One of the following parameters are required: one, two",
        ),
        (
            ("one", "two"),
            (1, 2),
            "Only one of the following parameters are allowed: one, two",
        ),
        (
            ("one", "two", "three"),
            (1, None, 3),
            "Only one of the following parameters are allowed: one, three",
        ),
    ],
)
def test_validate_single_required_field_with_bad_values_raises_value_error(
    names, values, message
):
    with pytest.raises(ValueError, match=message):
        validate_single_required_field(names, values)


def test_validate_single_required_field_with_only_one_field_does_not_raise_value_error():
    validate_single_required_field(["One", "Two", "Three"], [None, None, 3])


def test_atlan_tag_names(monkeypatch):
    tag_name = "Issue"
    tag_id = "123"

    def get_name_for_id(value):
        if value == tag_id:
            return tag_name
        return ""

    monkeypatch.setattr(
        pyatlan.cache.atlan_tag_cache.AtlanTagCache,
        "get_name_for_id",
        get_name_for_id,
    )

    referenceable = Referenceable()
    referenceable.classification_names = [tag_id, "456"]

    assert referenceable.atlan_tag_names == [tag_name, DELETED_]


def test_create_for_modification_on_asset_raises_exception():
    with pytest.raises(
        InvalidRequestError,
        match="ATLAN-PYTHON-400-053 This method cannot be invoked on the Asset "
        "class. Please invoke on a specific asset type",
    ):
        Asset.create_for_modification(qualified_name="", name="")
