# Copyright 2024 Atlan Pte. Ltd.

from .referenceable import Referenceable  # isort: skip

from .a_d_f import ADF
from .a_i import AI
from .a_i_application import AIApplication
from .a_i_model import AIModel
from .a_i_model_version import AIModelVersion
from .access_control import AccessControl
from .adf_activity import AdfActivity
from .adf_dataflow import AdfDataflow
from .adf_dataset import AdfDataset
from .adf_linkedservice import AdfLinkedservice
from .adf_pipeline import AdfPipeline
from .airflow import Airflow
from .airflow_dag import AirflowDag
from .airflow_task import AirflowTask
from .anomalo import Anomalo
from .anomalo_check import AnomaloCheck
from .app import App
from .application import Application
from .application_field import ApplicationField
from .asset import Asset
from .atlas_glossary import AtlasGlossary
from .atlas_glossary_category import AtlasGlossaryCategory
from .atlas_glossary_term import AtlasGlossaryTerm
from .auth_policy import AuthPolicy
from .b_i import BI
from .b_i_process import BIProcess
from .calculation_view import CalculationView
from .catalog import Catalog
from .column import Column
from .column_process import ColumnProcess
from .cosmos_mongo_d_b import CosmosMongoDB
from .cosmos_mongo_d_b_account import CosmosMongoDBAccount
from .cosmos_mongo_d_b_collection import CosmosMongoDBCollection
from .cosmos_mongo_d_b_database import CosmosMongoDBDatabase
from .data_contract import DataContract
from .data_domain import DataDomain
from .data_mesh import DataMesh
from .data_product import DataProduct
from .data_quality import DataQuality
from .database import Database
from .databricks_a_i_model_context import DatabricksAIModelContext
from .databricks_a_i_model_version import DatabricksAIModelVersion
from .databricks_unity_catalog_tag import DatabricksUnityCatalogTag
from .dbt import Dbt
from .dbt_metric import DbtMetric
from .dbt_model import DbtModel
from .dbt_model_column import DbtModelColumn
from .dbt_seed import DbtSeed
from .dbt_source import DbtSource
from .dbt_test import DbtTest
from .document_d_b import DocumentDB
from .document_d_b_collection import DocumentDBCollection
from .document_d_b_database import DocumentDBDatabase
from .dynamo_d_b_secondary_index import DynamoDBSecondaryIndex
from .file import File
from .fivetran import Fivetran
from .fivetran_connector import FivetranConnector
from .flow import Flow
from .flow_control_operation import FlowControlOperation
from .flow_dataset import FlowDataset
from .flow_dataset_operation import FlowDatasetOperation
from .flow_field import FlowField
from .flow_field_operation import FlowFieldOperation
from .flow_reusable_unit import FlowReusableUnit
from .folder import Folder
from .function import Function
from .indistinct_asset import IndistinctAsset  # noqa: F401
from .link import Link
from .m_c_incident import MCIncident
from .m_c_monitor import MCMonitor
from .materialised_view import MaterialisedView
from .matillion import Matillion
from .matillion_component import MatillionComponent
from .matillion_group import MatillionGroup
from .matillion_job import MatillionJob
from .matillion_project import MatillionProject
from .metric import Metric
from .model import Model
from .model_attribute import ModelAttribute
from .model_attribute_association import ModelAttributeAssociation
from .model_data_model import ModelDataModel
from .model_entity import ModelEntity
from .model_entity_association import ModelEntityAssociation
from .model_version import ModelVersion
from .mongo_d_b_collection import MongoDBCollection
from .mongo_d_b_database import MongoDBDatabase
from .monte_carlo import MonteCarlo
from .namespace import Namespace
from .no_s_q_l import NoSQL
from .persona import Persona
from .power_b_i import PowerBI
from .power_b_i_app import PowerBIApp
from .power_b_i_column import PowerBIColumn
from .power_b_i_dashboard import PowerBIDashboard
from .power_b_i_dataflow import PowerBIDataflow
from .power_b_i_dataflow_entity_column import PowerBIDataflowEntityColumn
from .power_b_i_dataset import PowerBIDataset
from .power_b_i_datasource import PowerBIDatasource
from .power_b_i_measure import PowerBIMeasure
from .power_b_i_page import PowerBIPage
from .power_b_i_report import PowerBIReport
from .power_b_i_table import PowerBITable
from .power_b_i_tile import PowerBITile
from .power_b_i_workspace import PowerBIWorkspace
from .procedure import Procedure
from .process import Process
from .query import Query
from .readme import Readme
from .resource import Resource
from .s_q_l import SQL
from .schema import Schema
from .schema_registry import SchemaRegistry
from .schema_registry_subject import SchemaRegistrySubject
from .snowflake_a_i_model_context import SnowflakeAIModelContext
from .snowflake_a_i_model_version import SnowflakeAIModelVersion
from .snowflake_dynamic_table import SnowflakeDynamicTable
from .snowflake_pipe import SnowflakePipe
from .snowflake_stage import SnowflakeStage
from .snowflake_stream import SnowflakeStream
from .snowflake_tag import SnowflakeTag
from .soda import Soda
from .soda_check import SodaCheck
from .spark import Spark
from .spark_job import SparkJob
from .stakeholder import Stakeholder
from .stakeholder_title import StakeholderTitle
from .table import Table
from .table_partition import TablePartition
from .tag import Tag
from .view import View

# Update asset forward references:
localns = locals()
Referenceable.Attributes.update_forward_refs(**localns)
Asset.Attributes.update_forward_refs(**localns)
Process.Attributes.update_forward_refs(**localns)
AtlasGlossaryCategory.Attributes.update_forward_refs(**localns)
AccessControl.Attributes.update_forward_refs(**localns)
AuthPolicy.Attributes.update_forward_refs(**localns)
StakeholderTitle.Attributes.update_forward_refs(**localns)
Catalog.Attributes.update_forward_refs(**localns)
Namespace.Attributes.update_forward_refs(**localns)
Flow.Attributes.update_forward_refs(**localns)
AtlasGlossary.Attributes.update_forward_refs(**localns)
AtlasGlossaryTerm.Attributes.update_forward_refs(**localns)
FlowDatasetOperation.Attributes.update_forward_refs(**localns)
BIProcess.Attributes.update_forward_refs(**localns)
ColumnProcess.Attributes.update_forward_refs(**localns)
Persona.Attributes.update_forward_refs(**localns)
App.Attributes.update_forward_refs(**localns)
Airflow.Attributes.update_forward_refs(**localns)
ADF.Attributes.update_forward_refs(**localns)
BI.Attributes.update_forward_refs(**localns)
FlowDataset.Attributes.update_forward_refs(**localns)
NoSQL.Attributes.update_forward_refs(**localns)
Dbt.Attributes.update_forward_refs(**localns)
Fivetran.Attributes.update_forward_refs(**localns)
DataContract.Attributes.update_forward_refs(**localns)
DataQuality.Attributes.update_forward_refs(**localns)
AI.Attributes.update_forward_refs(**localns)
Resource.Attributes.update_forward_refs(**localns)
FlowField.Attributes.update_forward_refs(**localns)
DataMesh.Attributes.update_forward_refs(**localns)
SQL.Attributes.update_forward_refs(**localns)
Matillion.Attributes.update_forward_refs(**localns)
Model.Attributes.update_forward_refs(**localns)
Spark.Attributes.update_forward_refs(**localns)
Tag.Attributes.update_forward_refs(**localns)
SchemaRegistry.Attributes.update_forward_refs(**localns)
Folder.Attributes.update_forward_refs(**localns)
FlowReusableUnit.Attributes.update_forward_refs(**localns)
FlowFieldOperation.Attributes.update_forward_refs(**localns)
FlowControlOperation.Attributes.update_forward_refs(**localns)
Stakeholder.Attributes.update_forward_refs(**localns)
ApplicationField.Attributes.update_forward_refs(**localns)
Application.Attributes.update_forward_refs(**localns)
AirflowDag.Attributes.update_forward_refs(**localns)
AirflowTask.Attributes.update_forward_refs(**localns)
AdfDataflow.Attributes.update_forward_refs(**localns)
AdfDataset.Attributes.update_forward_refs(**localns)
AdfPipeline.Attributes.update_forward_refs(**localns)
AdfLinkedservice.Attributes.update_forward_refs(**localns)
AdfActivity.Attributes.update_forward_refs(**localns)
PowerBI.Attributes.update_forward_refs(**localns)
CosmosMongoDB.Attributes.update_forward_refs(**localns)
DocumentDB.Attributes.update_forward_refs(**localns)
DbtModelColumn.Attributes.update_forward_refs(**localns)
DbtTest.Attributes.update_forward_refs(**localns)
DbtModel.Attributes.update_forward_refs(**localns)
DbtMetric.Attributes.update_forward_refs(**localns)
DbtSource.Attributes.update_forward_refs(**localns)
DbtSeed.Attributes.update_forward_refs(**localns)
FivetranConnector.Attributes.update_forward_refs(**localns)
Anomalo.Attributes.update_forward_refs(**localns)
MonteCarlo.Attributes.update_forward_refs(**localns)
Metric.Attributes.update_forward_refs(**localns)
Soda.Attributes.update_forward_refs(**localns)
AIApplication.Attributes.update_forward_refs(**localns)
AIModelVersion.Attributes.update_forward_refs(**localns)
AIModel.Attributes.update_forward_refs(**localns)
Readme.Attributes.update_forward_refs(**localns)
File.Attributes.update_forward_refs(**localns)
Link.Attributes.update_forward_refs(**localns)
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
SnowflakeStage.Attributes.update_forward_refs(**localns)
DatabricksUnityCatalogTag.Attributes.update_forward_refs(**localns)
SnowflakeStream.Attributes.update_forward_refs(**localns)
Database.Attributes.update_forward_refs(**localns)
CalculationView.Attributes.update_forward_refs(**localns)
Procedure.Attributes.update_forward_refs(**localns)
SnowflakeTag.Attributes.update_forward_refs(**localns)
MatillionGroup.Attributes.update_forward_refs(**localns)
MatillionJob.Attributes.update_forward_refs(**localns)
MatillionProject.Attributes.update_forward_refs(**localns)
MatillionComponent.Attributes.update_forward_refs(**localns)
ModelAttribute.Attributes.update_forward_refs(**localns)
ModelEntity.Attributes.update_forward_refs(**localns)
ModelVersion.Attributes.update_forward_refs(**localns)
ModelEntityAssociation.Attributes.update_forward_refs(**localns)
ModelAttributeAssociation.Attributes.update_forward_refs(**localns)
ModelDataModel.Attributes.update_forward_refs(**localns)
SparkJob.Attributes.update_forward_refs(**localns)
SchemaRegistrySubject.Attributes.update_forward_refs(**localns)
PowerBIReport.Attributes.update_forward_refs(**localns)
PowerBIDatasource.Attributes.update_forward_refs(**localns)
PowerBIWorkspace.Attributes.update_forward_refs(**localns)
PowerBIDashboard.Attributes.update_forward_refs(**localns)
PowerBIDataflow.Attributes.update_forward_refs(**localns)
PowerBIDataflowEntityColumn.Attributes.update_forward_refs(**localns)
PowerBIMeasure.Attributes.update_forward_refs(**localns)
PowerBIColumn.Attributes.update_forward_refs(**localns)
PowerBITable.Attributes.update_forward_refs(**localns)
PowerBITile.Attributes.update_forward_refs(**localns)
PowerBIDataset.Attributes.update_forward_refs(**localns)
PowerBIApp.Attributes.update_forward_refs(**localns)
PowerBIPage.Attributes.update_forward_refs(**localns)
CosmosMongoDBCollection.Attributes.update_forward_refs(**localns)
CosmosMongoDBAccount.Attributes.update_forward_refs(**localns)
CosmosMongoDBDatabase.Attributes.update_forward_refs(**localns)
DocumentDBCollection.Attributes.update_forward_refs(**localns)
DocumentDBDatabase.Attributes.update_forward_refs(**localns)
DynamoDBSecondaryIndex.Attributes.update_forward_refs(**localns)
MongoDBCollection.Attributes.update_forward_refs(**localns)
MongoDBDatabase.Attributes.update_forward_refs(**localns)
AnomaloCheck.Attributes.update_forward_refs(**localns)
MCIncident.Attributes.update_forward_refs(**localns)
MCMonitor.Attributes.update_forward_refs(**localns)
SodaCheck.Attributes.update_forward_refs(**localns)
DatabricksAIModelVersion.Attributes.update_forward_refs(**localns)
SnowflakeAIModelVersion.Attributes.update_forward_refs(**localns)
SnowflakeAIModelContext.Attributes.update_forward_refs(**localns)
DatabricksAIModelContext.Attributes.update_forward_refs(**localns)
SnowflakeDynamicTable.Attributes.update_forward_refs(**localns)
