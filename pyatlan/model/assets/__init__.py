# Copyright 2022 Atlan Pte. Ltd.
# isort: skip_file
from .referenceable import Referenceable
from .asset import Asset
from .data_set import DataSet
from .tag_attachment import TagAttachment
from .connection import Connection
from .process import Process
from .atlas_glossary_category import AtlasGlossaryCategory
from .badge import Badge
from .access_control import AccessControl
from .namespace import Namespace
from .catalog import Catalog
from .atlas_glossary import AtlasGlossary
from .auth_policy import AuthPolicy
from .process_execution import ProcessExecution
from .atlas_glossary_term import AtlasGlossaryTerm
from .auth_service import AuthService
from .cloud import Cloud
from .infrastructure import Infrastructure
from .b_i_process import BIProcess
from .dbt_process import DbtProcess
from .column_process import ColumnProcess
from .persona import Persona
from .purpose import Purpose
from .collection import Collection
from .folder import Folder
from .airflow import Airflow
from .object_store import ObjectStore
from .data_quality import DataQuality
from .b_i import BI
from .saa_s import SaaS
from .resource import Resource
from .multi_dimensional_dataset import MultiDimensionalDataset
from .data_mesh import DataMesh
from .s_q_l import SQL
from .event_store import EventStore
from .no_s_q_l import NoSQL
from .matillion import Matillion
from .dbt import Dbt
from .insight import Insight
from .a_p_i import API
from .spark import Spark
from .tag import Tag
from .schema_registry import SchemaRegistry
from .google import Google
from .azure import Azure
from .a_w_s import AWS
from .dbt_column_process import DbtColumnProcess
from .airflow_dag import AirflowDag
from .airflow_task import AirflowTask
# from .s3 import S3
from .a_d_l_s import ADLS
from .g_c_s import GCS
from .monte_carlo import MonteCarlo
from .metric import Metric
from .soda import Soda
from .preset import Preset
from .mode import Mode
from .sigma import Sigma
from .tableau import Tableau
from .looker import Looker
from .domo import Domo
from .redash import Redash
from .sisense import Sisense
from .data_studio import DataStudio
from .metabase import Metabase
from .quick_sight import QuickSight
from .thoughtspot import Thoughtspot
from .power_b_i import PowerBI
from .micro_strategy import MicroStrategy
from .qlik import Qlik
from .cognite import Cognite
from .salesforce import Salesforce
from .readme_template import ReadmeTemplate
from .readme import Readme
from .file import File
from .link import Link
from .cube import Cube
from .cube_hierarchy import CubeHierarchy
from .cube_field import CubeField
from .cube_dimension import CubeDimension
from .data_domain import DataDomain
from .data_product import DataProduct
from .table import Table
from .query import Query
from .schema import Schema
from .snowflake_pipe import SnowflakePipe
from .view import View
from .materialised_view import MaterialisedView
from .function import Function
from .table_partition import TablePartition
from .column import Column
from .snowflake_stream import SnowflakeStream
from .calculation_view import CalculationView
from .database import Database
from .procedure import Procedure
from .snowflake_tag import SnowflakeTag
from .kafka import Kafka
from .dynamo_d_b import DynamoDB
from .mongo_d_b import MongoDB
from .matillion_group import MatillionGroup
from .matillion_job import MatillionJob
from .matillion_project import MatillionProject
from .matillion_component import MatillionComponent
from .dbt_model_column import DbtModelColumn
from .dbt_tag import DbtTag
from .dbt_test import DbtTest
from .dbt_model import DbtModel
from .dbt_metric import DbtMetric
from .dbt_source import DbtSource
from .a_p_i_spec import APISpec
from .a_p_i_path import APIPath
from .spark_job import SparkJob
from .schema_registry_subject import SchemaRegistrySubject
from .data_studio_asset import DataStudioAsset
# from .s3_bucket import S3Bucket
# from .s3_object import S3Object
from .a_d_l_s_account import ADLSAccount
from .a_d_l_s_container import ADLSContainer
from .a_d_l_s_object import ADLSObject
from .g_c_s_object import GCSObject
from .g_c_s_bucket import GCSBucket
from .m_c_incident import MCIncident
from .m_c_monitor import MCMonitor
from .soda_check import SodaCheck
from .preset_chart import PresetChart
from .preset_dataset import PresetDataset
from .preset_dashboard import PresetDashboard
from .preset_workspace import PresetWorkspace
from .mode_report import ModeReport
from .mode_query import ModeQuery
from .mode_chart import ModeChart
from .mode_workspace import ModeWorkspace
from .mode_collection import ModeCollection
from .sigma_dataset_column import SigmaDatasetColumn
from .sigma_dataset import SigmaDataset
from .sigma_workbook import SigmaWorkbook
from .sigma_data_element_field import SigmaDataElementField
from .sigma_page import SigmaPage
from .sigma_data_element import SigmaDataElement
from .tableau_workbook import TableauWorkbook
from .tableau_datasource_field import TableauDatasourceField
from .tableau_calculated_field import TableauCalculatedField
from .tableau_project import TableauProject
from .tableau_metric import TableauMetric
from .tableau_site import TableauSite
from .tableau_datasource import TableauDatasource
from .tableau_dashboard import TableauDashboard
from .tableau_flow import TableauFlow
from .tableau_worksheet import TableauWorksheet
from .looker_look import LookerLook
from .looker_dashboard import LookerDashboard
from .looker_folder import LookerFolder
from .looker_tile import LookerTile
from .looker_model import LookerModel
from .looker_explore import LookerExplore
from .looker_project import LookerProject
from .looker_query import LookerQuery
from .looker_field import LookerField
from .looker_view import LookerView
from .domo_dataset import DomoDataset
from .domo_card import DomoCard
from .domo_dataset_column import DomoDatasetColumn
from .domo_dashboard import DomoDashboard
from .redash_dashboard import RedashDashboard
from .redash_query import RedashQuery
from .redash_visualization import RedashVisualization
from .sisense_folder import SisenseFolder
from .sisense_widget import SisenseWidget
from .sisense_datamodel import SisenseDatamodel
from .sisense_datamodel_table import SisenseDatamodelTable
from .sisense_dashboard import SisenseDashboard
from .metabase_question import MetabaseQuestion
from .metabase_collection import MetabaseCollection
from .metabase_dashboard import MetabaseDashboard
from .quick_sight_folder import QuickSightFolder
from .quick_sight_dashboard_visual import QuickSightDashboardVisual
from .quick_sight_analysis_visual import QuickSightAnalysisVisual
from .quick_sight_dataset_field import QuickSightDatasetField
from .quick_sight_analysis import QuickSightAnalysis
from .quick_sight_dashboard import QuickSightDashboard
from .quick_sight_dataset import QuickSightDataset
from .thoughtspot_worksheet import ThoughtspotWorksheet
from .thoughtspot_liveboard import ThoughtspotLiveboard
from .thoughtspot_table import ThoughtspotTable
from .thoughtspot_column import ThoughtspotColumn
from .thoughtspot_view import ThoughtspotView
from .thoughtspot_dashlet import ThoughtspotDashlet
from .thoughtspot_answer import ThoughtspotAnswer
from .power_b_i_report import PowerBIReport
from .power_b_i_measure import PowerBIMeasure
from .power_b_i_column import PowerBIColumn
from .power_b_i_table import PowerBITable
from .power_b_i_tile import PowerBITile
from .power_b_i_datasource import PowerBIDatasource
from .power_b_i_workspace import PowerBIWorkspace
from .power_b_i_dataset import PowerBIDataset
from .power_b_i_dashboard import PowerBIDashboard
from .power_b_i_dataflow import PowerBIDataflow
from .power_b_i_page import PowerBIPage
from .micro_strategy_report import MicroStrategyReport
from .micro_strategy_project import MicroStrategyProject
from .micro_strategy_metric import MicroStrategyMetric
from .micro_strategy_cube import MicroStrategyCube
from .micro_strategy_dossier import MicroStrategyDossier
from .micro_strategy_fact import MicroStrategyFact
from .micro_strategy_document import MicroStrategyDocument
from .micro_strategy_attribute import MicroStrategyAttribute
from .micro_strategy_visualization import MicroStrategyVisualization
from .qlik_space import QlikSpace
from .qlik_app import QlikApp
from .qlik_chart import QlikChart
from .qlik_dataset import QlikDataset
from .qlik_sheet import QlikSheet
from .cognite_event import CogniteEvent
from .cognite_asset import CogniteAsset
from .cognite_sequence import CogniteSequence
from .cognite3_d_model import Cognite3DModel
from .cognite_time_series import CogniteTimeSeries
from .cognite_file import CogniteFile
from .salesforce_object import SalesforceObject
from .salesforce_field import SalesforceField
from .salesforce_organization import SalesforceOrganization
from .salesforce_dashboard import SalesforceDashboard
from .salesforce_report import SalesforceReport
from .snowflake_dynamic_table import SnowflakeDynamicTable
from .mongo_d_b_collection import MongoDBCollection
from .dynamo_d_b_secondary_index import DynamoDBSecondaryIndex
from .dynamo_dbtable import DynamoDBTable
from .mongo_d_b_database import MongoDBDatabase
from .kafka_topic import KafkaTopic
from .kafka_consumer_group import KafkaConsumerGroup
from .qlik_stream import QlikStream
from .dynamo_d_b_local_secondary_index import DynamoDBLocalSecondaryIndex
from .dynamo_d_b_global_secondary_index import DynamoDBGlobalSecondaryIndex
from .azure_event_hub import AzureEventHub
from .azure_event_hub_consumer_group import AzureEventHubConsumerGroup


# Update asset forward references:
localns = locals()
Referenceable.Attributes.update_forward_refs(**localns)
Asset.Attributes.update_forward_refs(**localns)
DataSet.Attributes.update_forward_refs(**localns)
TagAttachment.Attributes.update_forward_refs(**localns)
Connection.Attributes.update_forward_refs(**localns)
Process.Attributes.update_forward_refs(**localns)
AtlasGlossaryCategory.Attributes.update_forward_refs(**localns)
Badge.Attributes.update_forward_refs(**localns)
AccessControl.Attributes.update_forward_refs(**localns)
Namespace.Attributes.update_forward_refs(**localns)
Catalog.Attributes.update_forward_refs(**localns)
AtlasGlossary.Attributes.update_forward_refs(**localns)
AuthPolicy.Attributes.update_forward_refs(**localns)
ProcessExecution.Attributes.update_forward_refs(**localns)
AtlasGlossaryTerm.Attributes.update_forward_refs(**localns)
AuthService.Attributes.update_forward_refs(**localns)
Cloud.Attributes.update_forward_refs(**localns)
Infrastructure.Attributes.update_forward_refs(**localns)
BIProcess.Attributes.update_forward_refs(**localns)
DbtProcess.Attributes.update_forward_refs(**localns)
ColumnProcess.Attributes.update_forward_refs(**localns)
Persona.Attributes.update_forward_refs(**localns)
Purpose.Attributes.update_forward_refs(**localns)
Collection.Attributes.update_forward_refs(**localns)
Folder.Attributes.update_forward_refs(**localns)
Airflow.Attributes.update_forward_refs(**localns)
ObjectStore.Attributes.update_forward_refs(**localns)
DataQuality.Attributes.update_forward_refs(**localns)
BI.Attributes.update_forward_refs(**localns)
SaaS.Attributes.update_forward_refs(**localns)
Resource.Attributes.update_forward_refs(**localns)
MultiDimensionalDataset.Attributes.update_forward_refs(**localns)
DataMesh.Attributes.update_forward_refs(**localns)
SQL.Attributes.update_forward_refs(**localns)
EventStore.Attributes.update_forward_refs(**localns)
NoSQL.Attributes.update_forward_refs(**localns)
Matillion.Attributes.update_forward_refs(**localns)
Dbt.Attributes.update_forward_refs(**localns)
Insight.Attributes.update_forward_refs(**localns)
API.Attributes.update_forward_refs(**localns)
Spark.Attributes.update_forward_refs(**localns)
Tag.Attributes.update_forward_refs(**localns)
SchemaRegistry.Attributes.update_forward_refs(**localns)
Google.Attributes.update_forward_refs(**localns)
Azure.Attributes.update_forward_refs(**localns)
AWS.Attributes.update_forward_refs(**localns)
DbtColumnProcess.Attributes.update_forward_refs(**localns)
AirflowDag.Attributes.update_forward_refs(**localns)
AirflowTask.Attributes.update_forward_refs(**localns)
# S3.Attributes.update_forward_refs(**localns)
ADLS.Attributes.update_forward_refs(**localns)
GCS.Attributes.update_forward_refs(**localns)
MonteCarlo.Attributes.update_forward_refs(**localns)
Metric.Attributes.update_forward_refs(**localns)
Soda.Attributes.update_forward_refs(**localns)
Preset.Attributes.update_forward_refs(**localns)
Mode.Attributes.update_forward_refs(**localns)
Sigma.Attributes.update_forward_refs(**localns)
Tableau.Attributes.update_forward_refs(**localns)
Looker.Attributes.update_forward_refs(**localns)
Domo.Attributes.update_forward_refs(**localns)
Redash.Attributes.update_forward_refs(**localns)
Sisense.Attributes.update_forward_refs(**localns)
DataStudio.Attributes.update_forward_refs(**localns)
Metabase.Attributes.update_forward_refs(**localns)
QuickSight.Attributes.update_forward_refs(**localns)
Thoughtspot.Attributes.update_forward_refs(**localns)
PowerBI.Attributes.update_forward_refs(**localns)
MicroStrategy.Attributes.update_forward_refs(**localns)
Qlik.Attributes.update_forward_refs(**localns)
Cognite.Attributes.update_forward_refs(**localns)
Salesforce.Attributes.update_forward_refs(**localns)
ReadmeTemplate.Attributes.update_forward_refs(**localns)
Readme.Attributes.update_forward_refs(**localns)
File.Attributes.update_forward_refs(**localns)
Link.Attributes.update_forward_refs(**localns)
Cube.Attributes.update_forward_refs(**localns)
CubeHierarchy.Attributes.update_forward_refs(**localns)
CubeField.Attributes.update_forward_refs(**localns)
CubeDimension.Attributes.update_forward_refs(**localns)
DataDomain.Attributes.update_forward_refs(**localns)
DataProduct.Attributes.update_forward_refs(**localns)
Table.Attributes.update_forward_refs(**localns)
Query.Attributes.update_forward_refs(**localns)
Schema.Attributes.update_forward_refs(**localns)
SnowflakePipe.Attributes.update_forward_refs(**localns)
View.Attributes.update_forward_refs(**localns)
MaterialisedView.Attributes.update_forward_refs(**localns)
Function.Attributes.update_forward_refs(**localns)
TablePartition.Attributes.update_forward_refs(**localns)
Column.Attributes.update_forward_refs(**localns)
SnowflakeStream.Attributes.update_forward_refs(**localns)
CalculationView.Attributes.update_forward_refs(**localns)
Database.Attributes.update_forward_refs(**localns)
Procedure.Attributes.update_forward_refs(**localns)
SnowflakeTag.Attributes.update_forward_refs(**localns)
Kafka.Attributes.update_forward_refs(**localns)
DynamoDB.Attributes.update_forward_refs(**localns)
MongoDB.Attributes.update_forward_refs(**localns)
MatillionGroup.Attributes.update_forward_refs(**localns)
MatillionJob.Attributes.update_forward_refs(**localns)
MatillionProject.Attributes.update_forward_refs(**localns)
MatillionComponent.Attributes.update_forward_refs(**localns)
DbtModelColumn.Attributes.update_forward_refs(**localns)
DbtTag.Attributes.update_forward_refs(**localns)
DbtTest.Attributes.update_forward_refs(**localns)
DbtModel.Attributes.update_forward_refs(**localns)
DbtMetric.Attributes.update_forward_refs(**localns)
DbtSource.Attributes.update_forward_refs(**localns)
APISpec.Attributes.update_forward_refs(**localns)
APIPath.Attributes.update_forward_refs(**localns)
SparkJob.Attributes.update_forward_refs(**localns)
SchemaRegistrySubject.Attributes.update_forward_refs(**localns)
DataStudioAsset.Attributes.update_forward_refs(**localns)
# S3Bucket.Attributes.update_forward_refs(**localns)
# S3Object.Attributes.update_forward_refs(**localns)
ADLSAccount.Attributes.update_forward_refs(**localns)
ADLSContainer.Attributes.update_forward_refs(**localns)
ADLSObject.Attributes.update_forward_refs(**localns)
GCSObject.Attributes.update_forward_refs(**localns)
GCSBucket.Attributes.update_forward_refs(**localns)
MCIncident.Attributes.update_forward_refs(**localns)
MCMonitor.Attributes.update_forward_refs(**localns)
SodaCheck.Attributes.update_forward_refs(**localns)
PresetChart.Attributes.update_forward_refs(**localns)
PresetDataset.Attributes.update_forward_refs(**localns)
PresetDashboard.Attributes.update_forward_refs(**localns)
PresetWorkspace.Attributes.update_forward_refs(**localns)
ModeReport.Attributes.update_forward_refs(**localns)
ModeQuery.Attributes.update_forward_refs(**localns)
ModeChart.Attributes.update_forward_refs(**localns)
ModeWorkspace.Attributes.update_forward_refs(**localns)
ModeCollection.Attributes.update_forward_refs(**localns)
SigmaDatasetColumn.Attributes.update_forward_refs(**localns)
SigmaDataset.Attributes.update_forward_refs(**localns)
SigmaWorkbook.Attributes.update_forward_refs(**localns)
SigmaDataElementField.Attributes.update_forward_refs(**localns)
SigmaPage.Attributes.update_forward_refs(**localns)
SigmaDataElement.Attributes.update_forward_refs(**localns)
TableauWorkbook.Attributes.update_forward_refs(**localns)
TableauDatasourceField.Attributes.update_forward_refs(**localns)
TableauCalculatedField.Attributes.update_forward_refs(**localns)
TableauProject.Attributes.update_forward_refs(**localns)
TableauMetric.Attributes.update_forward_refs(**localns)
TableauSite.Attributes.update_forward_refs(**localns)
TableauDatasource.Attributes.update_forward_refs(**localns)
TableauDashboard.Attributes.update_forward_refs(**localns)
TableauFlow.Attributes.update_forward_refs(**localns)
TableauWorksheet.Attributes.update_forward_refs(**localns)
LookerLook.Attributes.update_forward_refs(**localns)
LookerDashboard.Attributes.update_forward_refs(**localns)
LookerFolder.Attributes.update_forward_refs(**localns)
LookerTile.Attributes.update_forward_refs(**localns)
LookerModel.Attributes.update_forward_refs(**localns)
LookerExplore.Attributes.update_forward_refs(**localns)
LookerProject.Attributes.update_forward_refs(**localns)
LookerQuery.Attributes.update_forward_refs(**localns)
LookerField.Attributes.update_forward_refs(**localns)
LookerView.Attributes.update_forward_refs(**localns)
DomoDataset.Attributes.update_forward_refs(**localns)
DomoCard.Attributes.update_forward_refs(**localns)
DomoDatasetColumn.Attributes.update_forward_refs(**localns)
DomoDashboard.Attributes.update_forward_refs(**localns)
RedashDashboard.Attributes.update_forward_refs(**localns)
RedashQuery.Attributes.update_forward_refs(**localns)
RedashVisualization.Attributes.update_forward_refs(**localns)
SisenseFolder.Attributes.update_forward_refs(**localns)
SisenseWidget.Attributes.update_forward_refs(**localns)
SisenseDatamodel.Attributes.update_forward_refs(**localns)
SisenseDatamodelTable.Attributes.update_forward_refs(**localns)
SisenseDashboard.Attributes.update_forward_refs(**localns)
MetabaseQuestion.Attributes.update_forward_refs(**localns)
MetabaseCollection.Attributes.update_forward_refs(**localns)
MetabaseDashboard.Attributes.update_forward_refs(**localns)
QuickSightFolder.Attributes.update_forward_refs(**localns)
QuickSightDashboardVisual.Attributes.update_forward_refs(**localns)
QuickSightAnalysisVisual.Attributes.update_forward_refs(**localns)
QuickSightDatasetField.Attributes.update_forward_refs(**localns)
QuickSightAnalysis.Attributes.update_forward_refs(**localns)
QuickSightDashboard.Attributes.update_forward_refs(**localns)
QuickSightDataset.Attributes.update_forward_refs(**localns)
ThoughtspotWorksheet.Attributes.update_forward_refs(**localns)
ThoughtspotLiveboard.Attributes.update_forward_refs(**localns)
ThoughtspotTable.Attributes.update_forward_refs(**localns)
ThoughtspotColumn.Attributes.update_forward_refs(**localns)
ThoughtspotView.Attributes.update_forward_refs(**localns)
ThoughtspotDashlet.Attributes.update_forward_refs(**localns)
ThoughtspotAnswer.Attributes.update_forward_refs(**localns)
PowerBIReport.Attributes.update_forward_refs(**localns)
PowerBIMeasure.Attributes.update_forward_refs(**localns)
PowerBIColumn.Attributes.update_forward_refs(**localns)
PowerBITable.Attributes.update_forward_refs(**localns)
PowerBITile.Attributes.update_forward_refs(**localns)
PowerBIDatasource.Attributes.update_forward_refs(**localns)
PowerBIWorkspace.Attributes.update_forward_refs(**localns)
PowerBIDataset.Attributes.update_forward_refs(**localns)
PowerBIDashboard.Attributes.update_forward_refs(**localns)
PowerBIDataflow.Attributes.update_forward_refs(**localns)
PowerBIPage.Attributes.update_forward_refs(**localns)
MicroStrategyReport.Attributes.update_forward_refs(**localns)
MicroStrategyProject.Attributes.update_forward_refs(**localns)
MicroStrategyMetric.Attributes.update_forward_refs(**localns)
MicroStrategyCube.Attributes.update_forward_refs(**localns)
MicroStrategyDossier.Attributes.update_forward_refs(**localns)
MicroStrategyFact.Attributes.update_forward_refs(**localns)
MicroStrategyDocument.Attributes.update_forward_refs(**localns)
MicroStrategyAttribute.Attributes.update_forward_refs(**localns)
MicroStrategyVisualization.Attributes.update_forward_refs(**localns)
QlikSpace.Attributes.update_forward_refs(**localns)
QlikApp.Attributes.update_forward_refs(**localns)
QlikChart.Attributes.update_forward_refs(**localns)
QlikDataset.Attributes.update_forward_refs(**localns)
QlikSheet.Attributes.update_forward_refs(**localns)
CogniteEvent.Attributes.update_forward_refs(**localns)
CogniteAsset.Attributes.update_forward_refs(**localns)
CogniteSequence.Attributes.update_forward_refs(**localns)
Cognite3DModel.Attributes.update_forward_refs(**localns)
CogniteTimeSeries.Attributes.update_forward_refs(**localns)
CogniteFile.Attributes.update_forward_refs(**localns)
SalesforceObject.Attributes.update_forward_refs(**localns)
SalesforceField.Attributes.update_forward_refs(**localns)
SalesforceOrganization.Attributes.update_forward_refs(**localns)
SalesforceDashboard.Attributes.update_forward_refs(**localns)
SalesforceReport.Attributes.update_forward_refs(**localns)
SnowflakeDynamicTable.Attributes.update_forward_refs(**localns)
MongoDBCollection.Attributes.update_forward_refs(**localns)
DynamoDBSecondaryIndex.Attributes.update_forward_refs(**localns)
DynamoDBTable.Attributes.update_forward_refs(**localns)
MongoDBDatabase.Attributes.update_forward_refs(**localns)
KafkaTopic.Attributes.update_forward_refs(**localns)
KafkaConsumerGroup.Attributes.update_forward_refs(**localns)
QlikStream.Attributes.update_forward_refs(**localns)
DynamoDBLocalSecondaryIndex.Attributes.update_forward_refs(**localns)
DynamoDBGlobalSecondaryIndex.Attributes.update_forward_refs(**localns)
AzureEventHub.Attributes.update_forward_refs(**localns)
AzureEventHubConsumerGroup.Attributes.update_forward_refs(**localns)
