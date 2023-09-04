# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import json
from datetime import datetime
from inspect import signature
from pathlib import Path
from unittest.mock import create_autospec

import pytest

# from deepdiff import DeepDiff
from pydantic.error_wrappers import ValidationError

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
    validate_single_required_field,
)
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
    "Optional[set[str]]": {STRING_VALUE},
    "Optional[str]": STRING_VALUE,
    "Optional[datetime]": datetime.now(),
    "Optional[bool]": True,
    "Optional[CertificateStatus]": CertificateStatus.DRAFT,
    "Optional[int]": INT_VALUE,
    "Optional[float]": FLOAT_VALUE,
    "Optional[dict[str, str]]": {STRING_VALUE: STRING_VALUE},
    "Optional[dict[str, int]]": {STRING_VALUE: INT_VALUE},
    "Optional[list[AtlasServer]]": [AtlasServer()],
    "Optional[SourceCostUnitType]": SourceCostUnitType.CREDITS,
    "Optional[list[PopularityInsights]]": [PopularityInsights()],
    "Optional[QueryUsernameStrategy]": QueryUsernameStrategy.CONNECTION_USERNAME,
    "Optional[list[GoogleLabel]]": [
        GoogleLabel(google_label_key="", google_label_value="")
    ],
    "Optional[list[GoogleTag]]": [GoogleTag(google_tag_key="", google_tag_value="")],
    "Optional[GoogleDatastudioAssetType]": GoogleDatastudioAssetType.REPORT,
    "Optional[list[AzureTag]]": [AzureTag(azure_tag_key="", azure_tag_value="")],
    "Optional[list[AwsTag]]": [AwsTag(aws_tag_key="", aws_tag_value="")],
    "Optional[list[Catalog]]": [S3Object()],
    "Optional[list[BadgeCondition]]": [BadgeCondition()],
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
    "Optional[list[dict[str, str]]]": [{STRING_VALUE: STRING_VALUE}],
    "Optional[list[DbtMetricFilter]]": [DbtMetricFilter()],
    "Optional[list[SourceTagAttribute]]": [SourceTagAttribute()],
    "Optional[Histogram]": Histogram(boundaries={0.0}, frequencies={0.0}),
    "Optional[list[ColumnValueFrequencyMap]]": [ColumnValueFrequencyMap()],
    "Optional[KafkaTopicCompressionType]": KafkaTopicCompressionType.GZIP,
    "Optional[MCRuleSchedule]": MCRuleSchedule(),
    "Optional[list[MCRuleComparison]]": [MCRuleComparison()],
    "Optional[QuickSightFolderType]": QuickSightFolderType.SHARED,
    "Optional[QuickSightDatasetFieldType]": QuickSightDatasetFieldType.STRING,
    "Optional[QuickSightAnalysisStatus]": QuickSightAnalysisStatus.CREATION_FAILED,
    "Optional[QuickSightDatasetImportMode]": QuickSightDatasetImportMode.SPICE,
    "Optional[list[KafkaTopicConsumption]]": [KafkaTopicConsumption()],
    "list[AtlasGlossaryTerm]": [AtlasGlossaryTerm()],
    "Optional[list[AtlasGlossaryTerm]]": [AtlasGlossaryTerm()],
    "Optional[list[AtlasGlossaryCategory]]": [AtlasGlossaryCategory()],
    "Optional[list[File]]": [File()],
    "Optional[list[Link]]": [Link()],
    "Optional[list[MCIncident]]": [MCIncident()],
    "Optional[list[MCMonitor]]": [MCMonitor()],
    "Optional[list[Metric]]": [Metric()],
    "Optional[Readme]": Readme(),
    "AtlasGlossary": AtlasGlossary(),
    "Optional[list[Referenceable]]": [Referenceable()],
    "Optional[list[Process]]": [Process()],
    "Optional[GCSBucket]": GCSBucket(),
    "Optional[list[GCSObject]]": [GCSObject()],
    "Optional[list[ColumnProcess]]": [ColumnProcess()],
    "Optional[Process]": Process(),
    "Optional[AtlasGlossaryCategory]": AtlasGlossaryCategory(),
    "Optional[list[Folder]]": [Folder()],
    "Optional[list[Query]]": [Query()],
    "Namespace": Namespace(),
    "Optional[list[KafkaConsumerGroup]]": [KafkaConsumerGroup()],
    "Optional[list[KafkaTopic]]": [KafkaTopic()],
    "Optional[list[ADLSContainer]]": [ADLSContainer()],
    "Optional[ADLSAccount]": ADLSAccount(),
    "Optional[list[ADLSObject]]": [ADLSObject()],
    "Optional[ADLSContainer]": ADLSContainer(),
    "Optional[list[S3Object]]": [S3Object()],
    "Optional[S3Bucket]": S3Bucket(),
    "Optional[list[Asset]]": [Asset()],
    "Optional[MCMonitor]": MCMonitor(),
    "Optional[list[Column]]": [Column()],
    "Optional[Column]": Column(),
    "Optional[MetabaseCollection]": MetabaseCollection(),
    "Optional[list[MetabaseDashboard]]": [MetabaseDashboard()],
    "Optional[list[MetabaseQuestion]]": [MetabaseQuestion()],
    "Optional[list[QuickSightAnalysis]]": [QuickSightAnalysis()],
    "Optional[list[QuickSightDashboard]]": [QuickSightDashboard()],
    "Optional[list[QuickSightDataset]]": [QuickSightDataset()],
    "Optional[QuickSightDataset]": QuickSightDataset(),
    "Optional[list[QuickSightFolder]]": [QuickSightFolder()],
    "Optional[list[QuickSightAnalysisVisual]]": [QuickSightAnalysisVisual()],
    "Optional[list[QuickSightDashboardVisual]]": [QuickSightDashboardVisual()],
    "Optional[list[QuickSightDatasetField]]": [QuickSightDatasetField()],
    "Optional[QuickSightDashboard]": QuickSightDashboard(),
    "Optional[QuickSightAnalysis]": QuickSightAnalysis(),
    "Optional[list[ThoughtspotDashlet]]": [ThoughtspotDashlet()],
    "Optional[ThoughtspotLiveboard]": ThoughtspotLiveboard(),
    "Optional[PowerBIDataset]": PowerBIDataset(),
    "Optional[list[PowerBIPage]]": [PowerBIPage()],
    "Optional[list[PowerBITile]]": [PowerBITile()],
    "Optional[PowerBIWorkspace]": PowerBIWorkspace(),
    "Optional[PowerBITable]": PowerBITable(),
    "Optional[list[PowerBIColumn]]": [PowerBIColumn()],
    "Optional[list[PowerBIMeasure]]": [PowerBIMeasure()],
    "Optional[PowerBIDashboard]": PowerBIDashboard(),
    "Optional[PowerBIReport]": PowerBIReport(),
    "Optional[list[PowerBIDataset]]": [PowerBIDataset()],
    "Optional[list[PowerBIDashboard]]": [PowerBIDashboard()],
    "Optional[list[PowerBIDataflow]]": [PowerBIDataflow()],
    "Optional[list[PowerBIReport]]": [PowerBIReport()],
    "Optional[list[PowerBIDatasource]]": [PowerBIDatasource()],
    "Optional[list[PowerBITable]]": [PowerBITable()],
    "Optional[PresetDashboard]": PresetDashboard(),
    "Optional[list[PresetChart]]": [PresetChart()],
    "Optional[list[PresetDataset]]": [PresetDataset()],
    "Optional[PresetWorkspace]": PresetWorkspace(),
    "Optional[list[PresetDashboard]]": [PresetDashboard()],
    "Optional[list[ModeCollection]]": [ModeCollection()],
    "Optional[list[ModeQuery]]": [ModeQuery()],
    "Optional[list[ModeChart]]": [ModeChart()],
    "Optional[ModeReport]": ModeReport(),
    "Optional[ModeQuery]": ModeQuery(),
    "Optional[list[ModeReport]]": [ModeReport()],
    "Optional[ModeWorkspace]": ModeWorkspace(),
    "Optional[SigmaDataset]": SigmaDataset(),
    "Optional[list[SigmaDatasetColumn]]": [SigmaDatasetColumn()],
    "Optional[list[SigmaPage]]": [SigmaPage()],
    "Optional[SigmaDataElement]": SigmaDataElement(),
    "Optional[list[SigmaDataElement]]": [SigmaDataElement()],
    "Optional[SigmaWorkbook]": SigmaWorkbook(),
    "Optional[list[SigmaDataElementField]]": [SigmaDataElementField()],
    "Optional[SigmaPage]": SigmaPage(),
    "Optional[list[QlikApp]]": [QlikApp()],
    "Optional[list[QlikDataset]]": [QlikDataset()],
    "Optional[list[QlikSheet]]": [QlikSheet()],
    "Optional[QlikSpace]": QlikSpace(),
    "Optional[QlikSheet]": QlikSheet(),
    "Optional[QlikApp]": QlikApp(),
    "Optional[list[QlikChart]]": [QlikChart()],
    "Optional[list[TableauDashboard]]": [TableauDashboard()],
    "Optional[list[TableauDatasource]]": [TableauDatasource()],
    "Optional[TableauProject]": TableauProject(),
    "Optional[list[TableauWorksheet]]": [TableauWorksheet()],
    "Optional[TableauDatasource]": TableauDatasource(),
    "Optional[list[TableauProject]]": [TableauProject()],
    "Optional[list[TableauFlow]]": [TableauFlow()],
    "Optional[TableauSite]": TableauSite(),
    "Optional[list[TableauWorkbook]]": [TableauWorkbook()],
    "Optional[list[TableauDatasourceField]]": [TableauDatasourceField()],
    "Optional[TableauWorkbook]": TableauWorkbook(),
    "Optional[list[TableauCalculatedField]]": [TableauCalculatedField()],
    "Optional[LookerDashboard]": LookerDashboard(),
    "Optional[LookerFolder]": LookerFolder(),
    "Optional[LookerModel]": LookerModel(),
    "Optional[LookerQuery]": LookerQuery(),
    "Optional[LookerTile]": LookerTile(),
    "Optional[list[LookerTile]]": [LookerTile()],
    "Optional[list[LookerDashboard]]": [LookerDashboard()],
    "Optional[list[LookerLook]]": [LookerLook()],
    "Optional[LookerLook]": LookerLook(),
    "Optional[list[LookerExplore]]": [LookerExplore()],
    "Optional[list[LookerField]]": [LookerField()],
    "Optional[LookerProject]": LookerProject(),
    "Optional[list[LookerQuery]]": [LookerQuery()],
    "Optional[list[LookerModel]]": [LookerModel()],
    "Optional[list[LookerView]]": [LookerView()],
    "Optional[LookerView]": LookerView(),
    "Optional[LookerExplore]": LookerExplore(),
    "Optional[list[RedashVisualization]]": [RedashVisualization()],
    "Optional[RedashQuery]": RedashQuery(),
    "Optional[list[SalesforceField]]": [SalesforceField()],
    "Optional[SalesforceOrganization]": SalesforceOrganization(),
    "Optional[list[SalesforceObject]]": [SalesforceObject()],
    "Optional[SalesforceObject]": SalesforceObject(),
    "Optional[list[SalesforceDashboard]]": [SalesforceDashboard()],
    "Optional[list[SalesforceReport]]": [SalesforceReport()],
    "Optional[DbtModel]": DbtModel(),
    "Optional[list[DbtMetric]]": [DbtMetric()],
    "Optional[list[DbtModelColumn]]": [DbtModelColumn()],
    "Optional[list[SQL]]": [SQL()],
    "Optional[SQL]": SQL(),
    "Optional[Asset]": Asset(),
    "Optional[Internal]": Internal(),
    "Optional[list[Readme]]": [Readme()],
    "Optional[FileType]": FileType.CSV,
    "Optional[list[APIPath]]": [APIPath()],
    "Optional[APISpec]": APISpec(),
    "Optional[Schema]": Schema(),
    "Optional[list[DbtModel]]": [DbtModel()],
    "Optional[list[DbtSource]]": [DbtSource()],
    "Optional[Table]": Table(),
    "Optional[list[TablePartition]]": [TablePartition()],
    "Optional[list[Table]]": [Table()],
    "Optional[list[View]]": [View()],
    "Optional[MaterialisedView]": MaterialisedView(),
    "Optional[TablePartition]": TablePartition(),
    "Optional[View]": View(),
    "Optional[Database]": Database(),
    "Optional[list[MaterialisedView]]": [MaterialisedView()],
    "Optional[list[Procedure]]": [Procedure()],
    "Optional[list[SnowflakePipe]]": [SnowflakePipe()],
    "Optional[list[SnowflakeStream]]": [SnowflakeStream()],
    "Optional[list[SnowflakeTag]]": [SnowflakeTag()],
    "Optional[list[Schema]]": [Schema()],
    "Optional[AuthPolicyType]": AuthPolicyType.ALLOW,
    "Optional[list[MicroStrategyAttribute]]": [MicroStrategyAttribute()],
    "Optional[list[MicroStrategyMetric]]": [MicroStrategyMetric()],
    "Optional[MicroStrategyProject]": MicroStrategyProject(),
    "Optional[list[MicroStrategyCube]]": [MicroStrategyCube()],
    "Optional[list[MicroStrategyDocument]]": [MicroStrategyDocument()],
    "Optional[list[MicroStrategyDossier]]": [MicroStrategyDossier()],
    "Optional[list[MicroStrategyFact]]": [MicroStrategyFact()],
    "Optional[list[MicroStrategyReport]]": [MicroStrategyReport()],
    "Optional[list[MicroStrategyVisualization]]": [MicroStrategyVisualization()],
    "Optional[MicroStrategyDossier]": MicroStrategyDossier(),
    "Optional[list[AuthPolicy]]": [AuthPolicy()],
    "Optional[AccessControl]": AccessControl(),
    "Optional[list[AuthPolicyCondition]]": [
        AuthPolicyCondition(policy_condition_type="", policy_condition_values={""})
    ],
    "Optional[list[AuthPolicyValiditySchedule]]": [
        AuthPolicyValiditySchedule(
            policy_validity_schedule_start_time="",
            policy_validity_schedule_timezone="",
            policy_validity_schedule_end_time="",
        )
    ],
    "Optional[list[SchemaRegistrySubject]]": [SchemaRegistrySubject()],
    "Optional[list[StarredDetails]]": [StarredDetails()],
    "Optional[list[SodaCheck]]": [SodaCheck()],
    "Optional[SchemaRegistrySchemaCompatibility]": SchemaRegistrySchemaCompatibility.FULL,
    "Optional[list[DbtTest]]": [DbtTest()],
    "Optional[AirflowTask]": AirflowTask(),
    "Optional[list[AirflowTask]]": [AirflowTask()],
    "Optional[AirflowDag]": AirflowDag(),
    "Optional[OpenLineageRunState]": OpenLineageRunState.RUNNING,
    "Optional[list[Function]]": [Function()],
    "Optional[SchemaRegistrySchemaType]": SchemaRegistrySchemaType.PROTOBUF,
    "Optional[KafkaTopicCleanupPolicy]": KafkaTopicCleanupPolicy.DELETE,
    "Optional[list[SnowflakeDynamicTable]]": [SnowflakeDynamicTable()],
    "Optional[SnowflakeDynamicTable]": SnowflakeDynamicTable(),
    "Optional[AtlasGlossary]": AtlasGlossary(),
    "Optional[Namespace]": Namespace(),
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
            p for p in dir(asset_type) if isinstance(getattr(asset_type, p), property)
        ]
    ],
    indirect=["attribute_value"],
)
def test_attributes(clazz, property_name, attribute_value):
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
