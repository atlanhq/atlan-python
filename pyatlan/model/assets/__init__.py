# Copyright 2022 Atlan Pte. Ltd.
# isort: skip_file
import lazy_loader as lazy

submod_attrs = {
    "asset": ["Asset"],
    "referenceable": ["Referenceable"],
    "atlas_glossary": ["AtlasGlossary"],
    "atlas_glossary_term": ["AtlasGlossaryTerm"],
    "atlas_glossary_category": ["AtlasGlossaryCategory"],
    "database": ["Database"],
    "table": ["Table"],
    "column": ["Column"],
    "view": ["View"],
    "materialised_view": ["MaterialisedView"],
    "tag_attachment": ["TagAttachment"],
    "connection": ["Connection"],
    "workflow": ["Workflow"],
    "process": ["Process"],
    "stakeholder_title": ["StakeholderTitle"],
    "badge": ["Badge"],
    "access_control": ["AccessControl"],
    "namespace": ["Namespace"],
    "workflow_run": ["WorkflowRun"],
    "catalog": ["Catalog"],
    "auth_policy": ["AuthPolicy"],
    "process_execution": ["ProcessExecution"],
    "auth_service": ["AuthService"],
    "cloud": ["Cloud"],
    "infrastructure": ["Infrastructure"],
    "bi_process": ["BIProcess"],
    "dbt_process": ["DbtProcess"],
    "column_process": ["ColumnProcess"],
    "persona": ["Persona"],
    "purpose": ["Purpose"],
    "collection": ["Collection"],
    "folder": ["Folder"],
    "airflow": ["Airflow"],
    "data_contract": ["DataContract"],
    "object_store": ["ObjectStore"],
    "data_quality": ["DataQuality"],
    "b_i": ["BI"],
    "saas": ["SaaS"],
    "resource": ["Resource"],
    "multi_dimensional_dataset": ["MultiDimensionalDataset"],
    "data_mesh": ["DataMesh"],
    "s_q_l": ["SQL"],
    "event_store": ["EventStore"],
    "no_s_q_l": ["NoSQL"],
    "matillion": ["Matillion"],
    "dbt": ["Dbt"],
    "insight": ["Insight"],
    "a_p_i": ["API"],
    "spark": ["Spark"],
    "tag": ["Tag"],
    "schema_registry": ["SchemaRegistry"],
    "google": ["Google"],
    "azure": ["Azure"],
    "a_w_s": ["A_W_S"],
    "dbt_column_process": ["DbtColumnProcess"],
    "stakeholder": ["Stakeholder"],
    "airflow_dag": ["AirflowDag"],
    "airflow_task": ["AirflowTask"],
    "s3": ["S3"],
    "a_d_l_s": ["ADLS"],
    "g_c_s": ["GCS"],
    "monte_carlo": ["MonteCarlo"],
    "metric": ["Metric"],
    "soda": ["Soda"],
    "preset": ["Preset"],
    "mode": ["Mode"],
    "sigma": ["Sigma"],
    "tableau": ["Tableau"],
    "looker": ["Looker"],
    "domo": ["Domo"],
    "redash": ["Redash"],
    "sisense": ["Sisense"],
    "data_studio": ["DataStudio"],
    "metabase": ["Metabase"],
    "quick_sight": ["QuickSight"],
    "thoughtspot": ["Thoughtspot"],
    "power_b_i": ["PowerBI"],
    "micro_strategy": ["MicroStrategy"],
    "cognos": ["Cognos"],
    "superset": ["Superset"],
    "qlik": ["Qlik"],
    "cognite": ["Cognite"],
    "salesforce": ["Salesforce"],
    "readme_template": ["ReadmeTemplate"],
    "readme": ["Readme"],
    "file": ["File"],
    "link": ["Link"],
    "cube": ["Cube"],
    "cube_hierarchy": ["CubeHierarchy"],
    "cube_field": ["CubeField"],
    "cube_dimension": ["CubeDimension"],
    "data_domain": ["DataDomain"],
    "data_product": ["DataProduct"],
    "query": ["Query"],
    "schema": ["Schema"],
    "snowflake_pipe": ["SnowflakePipe"],
    "function": ["Function"],
    "table_partition": ["TablePartition"],
    "snowflake_stream": ["SnowflakeStream"],
    "databricks_unity_catalog_tag": ["DatabricksUnityCatalogTag"],
    "calculation_view": ["CalculationView"],
    "procedure": ["Procedure"],
    "snowflake_tag": ["SnowflakeTag"],
    "kafka": ["Kafka"],
    "azure_service_bus": ["AzureServiceBus"],
    "cosmos_mongo_d_b": ["CosmosMongoDB"],
    "dynamo_d_b": ["DynamoDB"],
    "mongo_d_b": ["MongoDB"],
    "matillion_group": ["MatillionGroup"],
    "matillion_job": ["MatillionJob"],
    "matillion_project": ["MatillionProject"],
    "matillion_component": ["MatillionComponent"],
    "dbt_model_column": ["DbtModelColumn"],
    "dbt_tag": ["DbtTag"],
    "dbt_test": ["DbtTest"],
    "dbt_model": ["DbtModel"],
    "dbt_metric": ["DbtMetric"],
    "dbt_source": ["DbtSource"],
    "a_p_i_spec": ["APISpec"],
    "a_p_i_path": ["APIPath"],
    "spark_job": ["SparkJob"],
    "schema_registry_subject": ["SchemaRegistrySubject"],
    "data_studio_asset": ["DataStudioAsset"],
    "s3_bucket": ["S3Bucket"],
    "s3_object": ["S3Object"],
    "a_d_l_s_account": ["ADLSAccount"],
    "a_d_l_s_container": ["ADLSContainer"],
    "a_d_l_s_object": ["ADLSObject"],
    "g_c_s_object": ["GCSObject"],
    "g_c_s_bucket": ["GCSBucket"],
    "m_c_incident": ["MCIncident"],
    "m_c_monitor": ["MCMonitor"],
    "soda_check": ["SodaCheck"],
    "preset_chart": ["PresetChart"],
    "preset_dataset": ["PresetDataset"],
    "preset_dashboard": ["PresetDashboard"],
    "preset_workspace": ["PresetWorkspace"],
    "mode_report": ["ModeReport"],
    "mode_query": ["ModeQuery"],
    "mode_chart": ["ModeChart"],
    "mode_workspace": ["ModeWorkspace"],
    "mode_collection": ["ModeCollection"],
    "sigma_dataset_column": ["SigmaDatasetColumn"],
    "sigma_dataset": ["SigmaDataset"],
    "sigma_workbook": ["SigmaWorkbook"],
    "sigma_data_element_field": ["SigmaDataElementField"],
    "sigma_page": ["SigmaPage"],
    "sigma_data_element": ["SigmaDataElement"],
    "tableau_workbook": ["TableauWorkbook"],
    "tableau_datasource_field": ["TableauDatasourceField"],
    "tableau_calculated_field": ["TableauCalculatedField"],
    "tableau_project": ["TableauProject"],
    "tableau_metric": ["TableauMetric"],
    "tableau_site": ["TableauSite"],
    "tableau_datasource": ["TableauDatasource"],
    "tableau_dashboard": ["TableauDashboard"],
    "tableau_flow": ["TableauFlow"],
    "tableau_worksheet": ["TableauWorksheet"],
    "looker_look": ["LookerLook"],
    "looker_dashboard": ["LookerDashboard"],
    "looker_folder": ["LookerFolder"],
    "looker_tile": ["LookerTile"],
    "looker_model": ["LookerModel"],
    "looker_explore": ["LookerExplore"],
    "looker_project": ["LookerProject"],
    "looker_query": ["LookerQuery"],
    "looker_field": ["LookerField"],
    "looker_view": ["LookerView"],
    "domo_dataset": ["DomoDataset"],
    "domo_card": ["DomoCard"],
    "domo_dataset_column": ["DomoDatasetColumn"],
    "domo_dashboard": ["DomoDashboard"],
    "redash_dashboard": ["RedashDashboard"],
    "redash_query": ["RedashQuery"],
    "redash_visualization": ["RedashVisualization"],
    "sisense_folder": ["SisenseFolder"],
    "sisense_widget": ["SisenseWidget"],
    "sisense_datamodel": ["SisenseDatamodel"],
    "sisense_datamodel_table": ["SisenseDatamodelTable"],
    "sisense_dashboard": ["SisenseDashboard"],
    "metabase_question": ["MetabaseQuestion"],
    "metabase_collection": ["MetabaseCollection"],
    "metabase_dashboard": ["MetabaseDashboard"],
    "quick_sight_folder": ["QuickSightFolder"],
    "quick_sight_dashboard_visual": ["QuickSightDashboardVisual"],
    "quick_sight_analysis_visual": ["QuickSightAnalysisVisual"],
    "quick_sight_dataset_field": ["QuickSightDatasetField"],
    "quick_sight_analysis": ["QuickSightAnalysis"],
    "quick_sight_dashboard": ["QuickSightDashboard"],
    "quick_sight_dataset": ["QuickSightDataset"],
    "thoughtspot_worksheet": ["ThoughtspotWorksheet"],
    "thoughtspot_liveboard": ["ThoughtspotLiveboard"],
    "thoughtspot_table": ["ThoughtspotTable"],
    "thoughtspot_column": ["ThoughtspotColumn"],
    "thoughtspot_view": ["ThoughtspotView"],
    "thoughtspot_dashlet": ["ThoughtspotDashlet"],
    "thoughtspot_answer": ["ThoughtspotAnswer"],
    "power_b_i_report": ["PowerBIReport"],
    "power_b_i_measure": ["PowerBIMeasure"],
    "power_b_i_column": ["PowerBIColumn"],
    "power_b_i_table": ["PowerBITable"],
    "power_b_i_tile": ["PowerBITile"],
    "power_b_i_datasource": ["PowerBIDatasource"],
    "power_b_i_workspace": ["PowerBIWorkspace"],
    "power_b_i_dataset": ["PowerBIDataset"],
    "power_b_i_dashboard": ["PowerBIDashboard"],
    "power_b_i_dataflow": ["PowerBIDataflow"],
    "power_b_i_page": ["PowerBIPage"],
    "micro_strategy_report": ["MicroStrategyReport"],
    "micro_strategy_project": ["MicroStrategyProject"],
    "micro_strategy_metric": ["MicroStrategyMetric"],
    "micro_strategy_cube": ["MicroStrategyCube"],
    "micro_strategy_dossier": ["MicroStrategyDossier"],
    "micro_strategy_fact": ["MicroStrategyFact"],
    "micro_strategy_document": ["MicroStrategyDocument"],
    "micro_strategy_attribute": ["MicroStrategyAttribute"],
    "micro_strategy_visualization": ["MicroStrategyVisualization"],
    "cognos_exploration": ["CognosExploration"],
    "cognos_dashboard": ["CognosDashboard"],
    "cognos_report": ["CognosReport"],
    "cognos_module": ["CognosModule"],
    "cognos_file": ["CognosFile"],
    "cognos_folder": ["CognosFolder"],
    "cognos_package": ["CognosPackage"],
    "cognos_datasource": ["CognosDatasource"],
    "superset_dataset": ["SupersetDataset"],
    "superset_chart": ["SupersetChart"],
    "superset_dashboard": ["SupersetDashboard"],
    "qlik_space": ["QlikSpace"],
    "qlik_app": ["QlikApp"],
    "qlik_chart": ["QlikChart"],
    "qlik_dataset": ["QlikDataset"],
    "qlik_sheet": ["QlikSheet"],
    "cognite_event": ["CogniteEvent"],
    "cognite_asset": ["CogniteAsset"],
    "cognite_sequence": ["CogniteSequence"],
    "cognite_3d_model": ["Cognite3DModel"],
    "cognite_time_series": ["CogniteTimeSeries"],
    "cognite_file": ["CogniteFile"],
    "salesforce_object": ["SalesforceObject"],
    "salesforce_field": ["SalesforceField"],
    "salesforce_organization": ["SalesforceOrganization"],
    "salesforce_dashboard": ["SalesforceDashboard"],
    "salesforce_report": ["SalesforceReport"],
    "snowflake_dynamic_table": ["SnowflakeDynamicTable"],
    "mongo_d_b_collection": ["MongoDBCollection"],
    "dynamo_d_b_secondary_index": ["DynamoDBSecondaryIndex"],
    "dynamo_d_b_table": ["DynamoDBTable"],
    "mongo_d_b_database": ["MongoDBDatabase"],
    "kafka_topic": ["KafkaTopic"],
    "kafka_consumer_group": ["KafkaConsumerGroup"],
    "azure_service_bus_namespace": ["AzureServiceBusNamespace"],
    "azure_service_bus_topic": ["AzureServiceBusTopic"],
    "cosmos_mongo_d_b_collection": ["CosmosMongoDBCollection"],
    "cosmos_mongo_d_b_database": ["CosmosMongoDBDatabase"],
    "qlik_stream": ["QlikStream"],
    "dynamo_d_b_local_secondary_index": ["DynamoDBLocalSecondaryIndex"],
    "dynamo_d_b_global_secondary_index": ["DynamoDBGlobalSecondaryIndex"],
    "azure_event_hub": ["AzureEventHub"],
    "azure_event_hub_consumer_group": ["AzureEventHubConsumerGroup"],
}

lazy_loader = lazy.attach(__name__, submod_attrs=submod_attrs)
__getattr__, __dir__, __all__ = lazy_loader
from .referenceable import Referenceable

# from .data_contract import DataContract


# from .referenceable import Referenceable
# from .asset import Asset
# from .task import Task
# from .data_set import DataSet
# from .tag_attachment import TagAttachment
# from .connection import Connection
# from .workflow import Workflow
# from .process import Process
# from .atlas_glossary_category import AtlasGlossaryCategory
# from .stakeholder_title import StakeholderTitle
# from .badge import Badge
# from .access_control import AccessControl
# from .namespace import Namespace
# from .workflow_run import WorkflowRun
# from .catalog import Catalog
# from .atlas_glossary import AtlasGlossary
# from .auth_policy import AuthPolicy
# from .process_execution import ProcessExecution
# from .atlas_glossary_term import AtlasGlossaryTerm
# from .auth_service import AuthService
# from .cloud import Cloud
# from .infrastructure import Infrastructure
# from .b_i_process import BIProcess
# from .dbt_process import DbtProcess
# from .column_process import ColumnProcess
# from .persona import Persona
# from .purpose import Purpose
# from .collection import Collection
# from .folder import Folder
# from .airflow import Airflow
# from .data_contract import DataContract
# from .object_store import ObjectStore
# from .data_quality import DataQuality
# from .b_i import BI
# from .saa_s import SaaS
# from .resource import Resource
# from .multi_dimensional_dataset import MultiDimensionalDataset
# from .data_mesh import DataMesh
# from .s_q_l import SQL
# from .event_store import EventStore
# from .no_s_q_l import NoSQL
# from .matillion import Matillion
# from .dbt import Dbt
# from .insight import Insight
# from .a_p_i import API
# from .spark import Spark
# from .tag import Tag
# from .schema_registry import SchemaRegistry
# from .google import Google
# from .azure import Azure
# from .a_w_s import A_W_S
# from .dbt_column_process import DbtColumnProcess
# from .stakeholder import Stakeholder
# from .airflow_dag import AirflowDag
# from .airflow_task import AirflowTask
# from .s3 import S3
# from .a_d_l_s import ADLS
# from .g_c_s import GCS
# from .monte_carlo import MonteCarlo
# from .metric import Metric
# from .soda import Soda
# from .preset import Preset
# from .mode import Mode
# from .sigma import Sigma
# from .tableau import Tableau
# from .looker import Looker
# from .domo import Domo
# from .redash import Redash
# from .sisense import Sisense
# from .data_studio import DataStudio
# from .metabase import Metabase
# from .quick_sight import QuickSight
# from .thoughtspot import Thoughtspot
# from .power_b_i import PowerBI
# from .micro_strategy import MicroStrategy
# from .cognos import Cognos
# from .superset import Superset
# from .qlik import Qlik
# from .cognite import Cognite
# from .salesforce import Salesforce
# from .readme_template import ReadmeTemplate
# from .readme import Readme
# from .file import File
# from .link import Link
# from .cube import Cube
# from .cube_hierarchy import CubeHierarchy
# from .cube_field import CubeField
# from .cube_dimension import CubeDimension
# from .data_domain import DataDomain
# from .data_product import DataProduct
# from .table import Table
# from .query import Query
# from .schema import Schema
# from .snowflake_pipe import SnowflakePipe
# from .view import View
# from .materialised_view import MaterialisedView
# from .function import Function
# from .table_partition import TablePartition
# from .column import Column
# from .snowflake_stream import SnowflakeStream
# from .databricks_unity_catalog_tag import DatabricksUnityCatalogTag
# from .database import Database
# from .calculation_view import CalculationView
# from .procedure import Procedure
# from .snowflake_tag import SnowflakeTag
# from .kafka import Kafka
# from .azure_service_bus import AzureServiceBus
# from .cosmos_mongo_d_b import CosmosMongoDB
# from .dynamo_d_b import DynamoDB
# from .mongo_d_b import MongoDB
# from .matillion_group import MatillionGroup
# from .matillion_job import MatillionJob
# from .matillion_project import MatillionProject
# from .matillion_component import MatillionComponent
# from .dbt_model_column import DbtModelColumn
# from .dbt_tag import DbtTag
# from .dbt_test import DbtTest
# from .dbt_model import DbtModel
# from .dbt_metric import DbtMetric
# from .dbt_source import DbtSource
# from .a_p_i_spec import APISpec
# from .a_p_i_path import APIPath
# from .spark_job import SparkJob
# from .schema_registry_subject import SchemaRegistrySubject
# from .data_studio_asset import DataStudioAsset
# from .s3_bucket import S3Bucket
# from .s3_object import S3Object
# from .a_d_l_s_account import ADLSAccount
# from .a_d_l_s_container import ADLSContainer
# from .a_d_l_s_object import ADLSObject
# from .g_c_s_object import GCSObject
# from .g_c_s_bucket import GCSBucket
# from .m_c_incident import MCIncident
# from .m_c_monitor import MCMonitor
# from .soda_check import SodaCheck
# from .preset_chart import PresetChart
# from .preset_dataset import PresetDataset
# from .preset_dashboard import PresetDashboard
# from .preset_workspace import PresetWorkspace
# from .mode_report import ModeReport
# from .mode_query import ModeQuery
# from .mode_chart import ModeChart
# from .mode_workspace import ModeWorkspace
# from .mode_collection import ModeCollection
# from .sigma_dataset_column import SigmaDatasetColumn
# from .sigma_dataset import SigmaDataset
# from .sigma_workbook import SigmaWorkbook
# from .sigma_data_element_field import SigmaDataElementField
# from .sigma_page import SigmaPage
# from .sigma_data_element import SigmaDataElement
# from .tableau_workbook import TableauWorkbook
# from .tableau_datasource_field import TableauDatasourceField
# from .tableau_calculated_field import TableauCalculatedField
# from .tableau_project import TableauProject
# from .tableau_metric import TableauMetric
# from .tableau_site import TableauSite
# from .tableau_datasource import TableauDatasource
# from .tableau_dashboard import TableauDashboard
# from .tableau_flow import TableauFlow
# from .tableau_worksheet import TableauWorksheet
# from .looker_look import LookerLook
# from .looker_dashboard import LookerDashboard
# from .looker_folder import LookerFolder
# from .looker_tile import LookerTile
# from .looker_model import LookerModel
# from .looker_explore import LookerExplore
# from .looker_project import LookerProject
# from .looker_query import LookerQuery
# from .looker_field import LookerField
# from .looker_view import LookerView
# from .domo_dataset import DomoDataset
# from .domo_card import DomoCard
# from .domo_dataset_column import DomoDatasetColumn
# from .domo_dashboard import DomoDashboard
# from .redash_dashboard import RedashDashboard
# from .redash_query import RedashQuery
# from .redash_visualization import RedashVisualization
# from .sisense_folder import SisenseFolder
# from .sisense_widget import SisenseWidget
# from .sisense_datamodel import SisenseDatamodel
# from .sisense_datamodel_table import SisenseDatamodelTable
# from .sisense_dashboard import SisenseDashboard
# from .metabase_question import MetabaseQuestion
# from .metabase_collection import MetabaseCollection
# from .metabase_dashboard import MetabaseDashboard
# from .quick_sight_folder import QuickSightFolder
# from .quick_sight_dashboard_visual import QuickSightDashboardVisual
# from .quick_sight_analysis_visual import QuickSightAnalysisVisual
# from .quick_sight_dataset_field import QuickSightDatasetField
# from .quick_sight_analysis import QuickSightAnalysis
# from .quick_sight_dashboard import QuickSightDashboard
# from .quick_sight_dataset import QuickSightDataset
# from .thoughtspot_worksheet import ThoughtspotWorksheet
# from .thoughtspot_liveboard import ThoughtspotLiveboard
# from .thoughtspot_table import ThoughtspotTable
# from .thoughtspot_column import ThoughtspotColumn
# from .thoughtspot_view import ThoughtspotView
# from .thoughtspot_dashlet import ThoughtspotDashlet
# from .thoughtspot_answer import ThoughtspotAnswer
# from .power_b_i_report import PowerBIReport
# from .power_b_i_measure import PowerBIMeasure
# from .power_b_i_column import PowerBIColumn
# from .power_b_i_table import PowerBITable
# from .power_b_i_tile import PowerBITile
# from .power_b_i_datasource import PowerBIDatasource
# from .power_b_i_workspace import PowerBIWorkspace
# from .power_b_i_dataset import PowerBIDataset
# from .power_b_i_dashboard import PowerBIDashboard
# from .power_b_i_dataflow import PowerBIDataflow
# from .power_b_i_page import PowerBIPage
# from .micro_strategy_report import MicroStrategyReport
# from .micro_strategy_project import MicroStrategyProject
# from .micro_strategy_metric import MicroStrategyMetric
# from .micro_strategy_cube import MicroStrategyCube
# from .micro_strategy_dossier import MicroStrategyDossier
# from .micro_strategy_fact import MicroStrategyFact
# from .micro_strategy_document import MicroStrategyDocument
# from .micro_strategy_attribute import MicroStrategyAttribute
# from .micro_strategy_visualization import MicroStrategyVisualization
# from .cognos_exploration import CognosExploration
# from .cognos_dashboard import CognosDashboard
# from .cognos_report import CognosReport
# from .cognos_module import CognosModule
# from .cognos_file import CognosFile
# from .cognos_folder import CognosFolder
# from .cognos_package import CognosPackage
# from .cognos_datasource import CognosDatasource
# from .superset_dataset import SupersetDataset
# from .superset_chart import SupersetChart
# from .superset_dashboard import SupersetDashboard
# from .qlik_space import QlikSpace
# from .qlik_app import QlikApp
# from .qlik_chart import QlikChart
# from .qlik_dataset import QlikDataset
# from .qlik_sheet import QlikSheet
# from .cognite_event import CogniteEvent
# from .cognite_asset import CogniteAsset
# from .cognite_sequence import CogniteSequence
# from .cognite3_d_model import Cognite3DModel
# from .cognite_time_series import CogniteTimeSeries
# from .cognite_file import CogniteFile
# from .salesforce_object import SalesforceObject
# from .salesforce_field import SalesforceField
# from .salesforce_organization import SalesforceOrganization
# from .salesforce_dashboard import SalesforceDashboard
# from .salesforce_report import SalesforceReport
# from .snowflake_dynamic_table import SnowflakeDynamicTable
# from .mongo_d_b_collection import MongoDBCollection
# from .dynamo_d_b_secondary_index import DynamoDBSecondaryIndex
# from .dynamo_d_btable import DynamoDBTable
# from .mongo_d_b_database import MongoDBDatabase
# from .kafka_topic import KafkaTopic
# from .kafka_consumer_group import KafkaConsumerGroup
# from .azure_service_bus_namespace import AzureServiceBusNamespace
# from .azure_service_bus_topic import AzureServiceBusTopic
# from .cosmos_mongo_d_b_collection import CosmosMongoDBCollection
# from .cosmos_mongo_d_b_database import CosmosMongoDBDatabase
# from .qlik_stream import QlikStream
# from .dynamo_d_b_local_secondary_index import DynamoDBLocalSecondaryIndex
# from .dynamo_d_b_global_secondary_index import DynamoDBGlobalSecondaryIndex
# from .azure_event_hub import AzureEventHub
# from .azure_event_hub_consumer_group import AzureEventHubConsumerGroup
