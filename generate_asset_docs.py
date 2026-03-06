"""One-off script to generate docs/api/assets/ pages from __PYATLAN_ASSETS__."""
import os
import sys

sys.path.insert(0, ".")

from pyatlan.model.assets import __PYATLAN_ASSETS__

# ── Module-path helpers ───────────────────────────────────────────────────────

CORE_CLASS_TO_FILE = {
    # map class name → file stem in pyatlan/model/assets/core/
    "Referenceable": "referenceable",
    "Asset": "asset",
    "Process": "process",
    "AtlasGlossaryCategory": "atlas_glossary_category",
    "AccessControl": "access_control",
    "AuthPolicy": "auth_policy",
    "StakeholderTitle": "stakeholder_title",
    "Catalog": "catalog",
    "Namespace": "namespace",
    "Flow": "flow",
    "AtlasGlossary": "atlas_glossary",
    "AtlasGlossaryTerm": "atlas_glossary_term",
    "FlowDatasetOperation": "flow_dataset_operation",
    "BIProcess": "b_i_process",
    "ColumnProcess": "column_process",
    "Persona": "persona",
    "App": "app",
    "Airflow": "airflow",
    "ADF": "a_d_f",
    "BI": "b_i",
    "Semantic": "semantic",
    "FlowDataset": "flow_dataset",
    "NoSQL": "no_s_q_l",
    "Partial": "partial",
    "Dbt": "dbt",
    "Fivetran": "fivetran",
    "DataContract": "data_contract",
    "DataQuality": "data_quality",
    "PartialV01": "partial_v01",
    "PartialV02": "partial_v02",
    "AI": "a_i",
    "Resource": "resource",
    "FlowField": "flow_field",
    "DataMesh": "data_mesh",
    "SQL": "s_q_l",
    "Matillion": "matillion",
    "Model": "model",
    "Spark": "spark",
    "Tag": "tag",
    "SchemaRegistry": "schema_registry",
    "Folder": "folder",
    "FlowReusableUnit": "flow_reusable_unit",
    "FlowFieldOperation": "flow_field_operation",
    "FlowControlOperation": "flow_control_operation",
    "Stakeholder": "stakeholder",
    "ApplicationField": "application_field",
    "Application": "application",
    "AirflowDag": "airflow_dag",
    "AirflowTask": "airflow_task",
    "AdfDataflow": "adf_dataflow",
    "AdfDataset": "adf_dataset",
    "AdfPipeline": "adf_pipeline",
    "AdfLinkedservice": "adf_linkedservice",
    "AdfActivity": "adf_activity",
    "PowerBI": "power_b_i",
    "Fabric": "fabric",
    "CosmosMongoDB": "cosmos_mongo_d_b",
    "DocumentDB": "document_d_b",
    "PartialField": "partial_field",
    "PartialObject": "partial_object",
    "DbtModelColumn": "dbt_model_column",
    "DbtTest": "dbt_test",
    "DbtModel": "dbt_model",
    "DbtSeed": "dbt_seed",
    "DbtMetric": "dbt_metric",
    "DbtSource": "dbt_source",
    "FivetranConnector": "fivetran_connector",
    "Anomalo": "anomalo",
    "MonteCarlo": "monte_carlo",
    "DataQualityRuleTemplate": "data_quality_rule_template",
    "Metric": "metric",
    "DataQualityRule": "data_quality_rule",
    "Soda": "soda",
    "PartialV01Field": "partial_v01_field",
    "PartialV02Field": "partial_v02_field",
    "PartialV02Object": "partial_v02_object",
    "AIApplication": "a_i_application",
    "AIModelVersion": "a_i_model_version",
    "AIModel": "a_i_model",
    "Readme": "readme",
    "File": "file",
    "Link": "link",
    "DataDomain": "data_domain",
    "DataProduct": "data_product",
    "Table": "table",
    "Query": "query",
    "Schema": "schema",
    "SnowflakePipe": "snowflake_pipe",
    "View": "view",
    "MaterialisedView": "materialised_view",
    "Function": "function",
    "TablePartition": "table_partition",
    "Column": "column",
    "SnowflakeStage": "snowflake_stage",
    "DatabricksUnityCatalogTag": "databricks_unity_catalog_tag",
    "SnowflakeStream": "snowflake_stream",
    "CalculationView": "calculation_view",
    "Database": "database",
    "Procedure": "procedure",
    "Databricks": "databricks",
    "SnowflakeTag": "snowflake_tag",
    "MatillionGroup": "matillion_group",
    "MatillionJob": "matillion_job",
    "MatillionProject": "matillion_project",
    "MatillionComponent": "matillion_component",
    "ModelAttribute": "model_attribute",
    "ModelEntity": "model_entity",
    "ModelVersion": "model_version",
    "ModelEntityAssociation": "model_entity_association",
    "ModelAttributeAssociation": "model_attribute_association",
    "ModelDataModel": "model_data_model",
    "SparkJob": "spark_job",
    "SchemaRegistrySubject": "schema_registry_subject",
    "PowerBIReport": "power_b_i_report",
    "PowerBIDatasource": "power_b_i_datasource",
    "PowerBIWorkspace": "power_b_i_workspace",
    "PowerBIDashboard": "power_b_i_dashboard",
    "PowerBIDataflow": "power_b_i_dataflow",
    "PowerBIDataflowEntityColumn": "power_b_i_dataflow_entity_column",
    "PowerBIMeasure": "power_b_i_measure",
    "PowerBIColumn": "power_b_i_column",
    "PowerBITable": "power_b_i_table",
    "PowerBITile": "power_b_i_tile",
    "PowerBIDataset": "power_b_i_dataset",
    "PowerBIApp": "power_b_i_app",
    "PowerBIPage": "power_b_i_page",
    "FabricVisual": "fabric_visual",
    "FabricDashboard": "fabric_dashboard",
    "FabricDataflow": "fabric_dataflow",
    "FabricActivity": "fabric_activity",
    "FabricPage": "fabric_page",
    "FabricWorkspace": "fabric_workspace",
    "FabricDataPipeline": "fabric_data_pipeline",
    "FabricSemanticModelTable": "fabric_semantic_model_table",
    "FabricSemanticModelTableColumn": "fabric_semantic_model_table_column",
    "FabricDataflowEntityColumn": "fabric_dataflow_entity_column",
    "FabricReport": "fabric_report",
    "FabricSemanticModel": "fabric_semantic_model",
    "CosmosMongoDBCollection": "cosmos_mongo_d_b_collection",
    "CosmosMongoDBAccount": "cosmos_mongo_d_b_account",
    "CosmosMongoDBDatabase": "cosmos_mongo_d_b_database",
    "DocumentDBCollection": "document_d_b_collection",
    "DocumentDBDatabase": "document_d_b_database",
    "DynamoDBSecondaryIndex": "dynamo_d_b_secondary_index",
    "MongoDBCollection": "mongo_d_b_collection",
    "MongoDBDatabase": "mongo_d_b_database",
    "AnomaloCheck": "anomalo_check",
    "MCIncident": "m_c_incident",
    "MCMonitor": "m_c_monitor",
    "SodaCheck": "soda_check",
    "DatabricksAIModelVersion": "databricks_a_i_model_version",
    "SnowflakeAIModelVersion": "snowflake_a_i_model_version",
    "SnowflakeAIModelContext": "snowflake_a_i_model_context",
    "DatabricksAIModelContext": "databricks_a_i_model_context",
    "SnowflakeDynamicTable": "snowflake_dynamic_table",
    "DatabricksMetricView": "databricks_metric_view",
    "BigqueryRoutine": "bigquery_routine",
    "DatabricksVolume": "databricks_volume",
    "DatabricksVolumePath": "databricks_volume_path",
    "IndistinctAsset": "indistinct_asset",
}


def core_ref(cls: str) -> str:
    file = CORE_CLASS_TO_FILE[cls]
    return f"pyatlan.model.assets.core.{file}.{cls}"


def asset_ref(module_key: str, cls: str) -> str:
    return f"pyatlan.model.assets.{module_key}.{cls}"


# ── Group definitions ─────────────────────────────────────────────────────────
# Each group → (page_file, title, list_of_(module_path, class) pairs)

def build_groups():
    # helper: resolve all classes for a given module key from __PYATLAN_ASSETS__
    def from_key(key):
        classes = __PYATLAN_ASSETS__.get(key, [])
        return [(asset_ref(key, c), c) for c in classes]

    def from_core(*names):
        return [(core_ref(n), n) for n in names]

    groups = []

    # Core Base
    groups.append(("core.md", "Core Base Classes", (
        from_core("Referenceable", "Asset", "Catalog", "Namespace", "Folder",
                  "Resource", "Process", "ColumnProcess", "BIProcess",
                  "FlowDataset", "FlowField", "Flow", "FlowReusableUnit",
                  "FlowControlOperation", "FlowDatasetOperation", "FlowFieldOperation",
                  "Tag", "SchemaRegistry", "SchemaRegistrySubject",
                  "IndistinctAsset")
    )))

    # Glossary
    groups.append(("glossary.md", "Glossary", (
        from_core("AtlasGlossary", "AtlasGlossaryTerm", "AtlasGlossaryCategory")
    )))

    # Access Control
    groups.append(("access-control.md", "Access Control", (
        from_core("AccessControl", "AuthPolicy", "Persona", "Stakeholder",
                  "StakeholderTitle")
        + from_key("purpose")
        + from_key("business_policy")
        + from_key("business_policy_exception")
        + from_key("business_policy_incident")
        + from_key("business_policy_log")
        + from_key("auth_service")
    )))

    # SQL Databases
    groups.append(("sql.md", "SQL Databases", (
        from_core("SQL", "Database", "Schema", "Table", "View",
                  "MaterialisedView", "Column", "Function", "Procedure",
                  "Query", "TablePartition", "CalculationView", "DataContract",
                  "Partial", "PartialField", "PartialObject",
                  "PartialV01", "PartialV01Field",
                  "PartialV02", "PartialV02Field", "PartialV02Object")
    )))

    # Snowflake
    groups.append(("snowflake.md", "Snowflake", (
        from_key("snowflake")
        + from_core("SnowflakePipe", "SnowflakeStage", "SnowflakeStream",
                    "SnowflakeTag", "SnowflakeDynamicTable",
                    "SnowflakeAIModelContext", "SnowflakeAIModelVersion")
        + from_key("bigquery_tag")  # BigQuery lumped here as small
        + from_core("BigqueryRoutine")
    )))

    # Databricks
    groups.append(("databricks.md", "Databricks", (
        from_core("Databricks", "DatabricksUnityCatalogTag",
                  "DatabricksVolume", "DatabricksVolumePath",
                  "DatabricksMetricView", "DatabricksAIModelContext",
                  "DatabricksAIModelVersion")
        + from_key("databricks_notebook")
        + from_key("databricks_external_location")
        + from_key("databricks_external_location_path")
    )))

    # NoSQL
    groups.append(("nosql.md", "NoSQL Databases", (
        from_core("NoSQL")
        + from_core("CosmosMongoDB", "CosmosMongoDBAccount", "CosmosMongoDBCollection",
                    "CosmosMongoDBDatabase")
        + from_key("mongo_d_b")
        + from_core("MongoDBCollection", "MongoDBDatabase")
        + from_core("DocumentDB", "DocumentDBCollection", "DocumentDBDatabase")
        + from_key("dynamo_d_b")
        + from_key("dynamo_dbtable")
        + from_core("DynamoDBSecondaryIndex")
        + from_key("dynamo_d_b_local_secondary_index")
        + from_key("dynamo_d_b_global_secondary_index")
        + from_key("dynamo_d_b_attribute")
        + from_key("cassandra")
        + from_key("cassandra_table")
        + from_key("cassandra_view")
        + from_key("cassandra_column")
        + from_key("cassandra_index")
        + from_key("cassandra_keyspace")
    )))

    # Streaming
    groups.append(("streaming.md", "Streaming & Events", (
        from_key("kafka")
        + from_key("kafka_topic")
        + from_key("kafka_consumer_group")
        + from_key("azure_service_bus")
        + from_key("azure_service_bus_namespace")
        + from_key("azure_service_bus_schema")
        + from_key("azure_service_bus_topic")
        + from_key("azure_event_hub")
        + from_key("azure_event_hub_consumer_group")
        + from_key("event_store")
    )))

    # Cloud Storage
    groups.append(("cloud-storage.md", "Cloud Storage", (
        from_key("s3")
        + from_key("s3_bucket")
        + from_key("s3_prefix")
        + from_key("s3_object")
        + from_key("a_d_l_s")
        + from_key("a_d_l_s_account")
        + from_key("a_d_l_s_container")
        + from_key("a_d_l_s_object")
        + from_key("g_c_s")
        + from_key("g_c_s_bucket")
        + from_key("g_c_s_object")
        + from_key("object_store")
        + from_key("a_w_s")
        + from_key("google")
        + from_key("azure")
        + from_key("cloud")
    )))

    # DBT
    groups.append(("dbt.md", "dbt", (
        from_core("Dbt", "DbtModel", "DbtModelColumn", "DbtTest",
                  "DbtSeed", "DbtMetric", "DbtSource")
        + from_key("dbt_tag")
        + from_key("dbt_dimension")
        + from_key("dbt_measure")
        + from_key("dbt_semantic_model")
        + from_key("dbt_entity")
        + from_key("dbt_column_process")
        + from_key("dbt_process")
    )))

    # Airflow + ADF
    groups.append(("orchestration.md", "Orchestration", (
        from_core("Airflow", "AirflowDag", "AirflowTask")
        + from_core("ADF", "AdfDataflow", "AdfDataset", "AdfPipeline",
                    "AdfLinkedservice", "AdfActivity")
        + from_core("Matillion", "MatillionGroup", "MatillionJob",
                    "MatillionProject", "MatillionComponent")
        + from_core("Fivetran", "FivetranConnector")
        + from_core("Spark", "SparkJob")
    )))

    # PowerBI + Fabric
    groups.append(("microsoft-bi.md", "Microsoft BI", (
        from_core("PowerBI", "PowerBIApp", "PowerBIColumn", "PowerBIDashboard",
                  "PowerBIDataflow", "PowerBIDataflowEntityColumn",
                  "PowerBIDataset", "PowerBIDatasource", "PowerBIMeasure",
                  "PowerBIPage", "PowerBIReport", "PowerBITable",
                  "PowerBITile", "PowerBIWorkspace")
        + from_core("Fabric", "FabricActivity", "FabricDashboard",
                    "FabricDataflow", "FabricDataflowEntityColumn",
                    "FabricDataPipeline", "FabricPage", "FabricReport",
                    "FabricSemanticModel", "FabricSemanticModelTable",
                    "FabricSemanticModelTableColumn", "FabricVisual",
                    "FabricWorkspace")
    )))

    # Tableau
    groups.append(("tableau.md", "Tableau", (
        from_key("tableau")
        + from_key("tableau_workbook")
        + from_key("tableau_worksheet")
        + from_key("tableau_worksheet_field")
        + from_key("tableau_dashboard")
        + from_key("tableau_dashboard_field")
        + from_key("tableau_datasource")
        + from_key("tableau_datasource_field")
        + from_key("tableau_calculated_field")
        + from_key("tableau_project")
        + from_key("tableau_site")
        + from_key("tableau_flow")
        + from_key("tableau_metric")
    )))

    # Looker
    groups.append(("looker.md", "Looker", (
        from_key("looker")
        + from_key("looker_look")
        + from_key("looker_dashboard")
        + from_key("looker_folder")
        + from_key("looker_tile")
        + from_key("looker_model")
        + from_key("looker_explore")
        + from_key("looker_project")
        + from_key("looker_query")
        + from_key("looker_field")
        + from_key("looker_view")
    )))

    # Other BI Tools
    groups.append(("other-bi.md", "Other BI Tools", (
        from_key("metabase")
        + from_key("metabase_collection")
        + from_key("metabase_dashboard")
        + from_key("metabase_question")
        + from_key("mode")
        + from_key("mode_report")
        + from_key("mode_query")
        + from_key("mode_chart")
        + from_key("mode_workspace")
        + from_key("mode_collection")
        + from_key("preset")
        + from_key("preset_chart")
        + from_key("preset_dashboard")
        + from_key("preset_dataset")
        + from_key("preset_workspace")
        + from_key("sigma")
        + from_key("sigma_workbook")
        + from_key("sigma_page")
        + from_key("sigma_dataset")
        + from_key("sigma_dataset_column")
        + from_key("sigma_data_element")
        + from_key("sigma_data_element_field")
        + from_key("quick_sight")
        + from_key("quick_sight_analysis")
        + from_key("quick_sight_analysis_visual")
        + from_key("quick_sight_dashboard")
        + from_key("quick_sight_dashboard_visual")
        + from_key("quick_sight_dataset")
        + from_key("quick_sight_dataset_field")
        + from_key("quick_sight_folder")
        + from_key("thoughtspot")
        + from_key("thoughtspot_worksheet")
        + from_key("thoughtspot_liveboard")
        + from_key("thoughtspot_table")
        + from_key("thoughtspot_view")
        + from_key("thoughtspot_column")
        + from_key("thoughtspot_dashlet")
        + from_key("thoughtspot_answer")
        + from_key("micro_strategy")
        + from_key("micro_strategy_report")
        + from_key("micro_strategy_project")
        + from_key("micro_strategy_metric")
        + from_key("micro_strategy_dossier")
        + from_key("micro_strategy_fact")
        + from_key("micro_strategy_cube")
        + from_key("micro_strategy_column")
        + from_key("micro_strategy_document")
        + from_key("micro_strategy_attribute")
        + from_key("micro_strategy_visualization")
        + from_key("cognos")
        + from_key("cognos_column")
        + from_key("cognos_exploration")
        + from_key("cognos_dataset")
        + from_key("cognos_dashboard")
        + from_key("cognos_report")
        + from_key("cognos_module")
        + from_key("cognos_file")
        + from_key("cognos_folder")
        + from_key("cognos_package")
        + from_key("cognos_datasource")
        + from_key("superset")
        + from_key("superset_chart")
        + from_key("superset_dashboard")
        + from_key("superset_dataset")
        + from_key("qlik")
        + from_key("qlik_app")
        + from_key("qlik_chart")
        + from_key("qlik_column")
        + from_key("qlik_dataset")
        + from_key("qlik_sheet")
        + from_key("qlik_space")
        + from_key("qlik_stream")
        + from_key("domo")
        + from_key("domo_card")
        + from_key("domo_dashboard")
        + from_key("domo_dataset")
        + from_key("domo_dataset_column")
        + from_key("redash")
        + from_key("redash_dashboard")
        + from_key("redash_query")
        + from_key("redash_visualization")
        + from_key("sisense")
        + from_key("sisense_dashboard")
        + from_key("sisense_datamodel")
        + from_key("sisense_datamodel_table")
        + from_key("sisense_folder")
        + from_key("sisense_widget")
        + from_key("data_studio")
        + from_key("data_studio_asset")
        + from_key("anaplan")
        + from_key("anaplan_app")
        + from_key("anaplan_dimension")
        + from_key("anaplan_line_item")
        + from_key("anaplan_list")
        + from_key("anaplan_model")
        + from_key("anaplan_module")
        + from_key("anaplan_page")
        + from_key("anaplan_system_dimension")
        + from_key("anaplan_view")
        + from_key("anaplan_workspace")
    )))

    # Data Quality
    groups.append(("data-quality.md", "Data Quality", (
        from_core("DataQuality", "DataQualityRule", "DataQualityRuleTemplate", "Metric")
        + from_core("Anomalo", "AnomaloCheck")
        + from_core("MonteCarlo", "MCMonitor", "MCIncident")
        + from_core("Soda", "SodaCheck")
    )))

    # Data Mesh
    groups.append(("data-mesh.md", "Data Mesh", (
        from_core("DataMesh", "DataDomain", "DataProduct")
    )))

    # AI / ML
    groups.append(("ai.md", "AI / ML", (
        from_core("AI", "AIModel", "AIModelVersion", "AIApplication")
        + from_core("DatabricksAIModelContext", "DatabricksAIModelVersion")
        + from_core("SnowflakeAIModelContext", "SnowflakeAIModelVersion")
    )))

    # API
    groups.append(("api.md", "API", (
        from_key("a_p_i")
        + from_key("a_p_i_spec")
        + from_key("a_p_i_query")
        + from_key("a_p_i_object")
        + from_key("a_p_i_path")
        + from_key("a_p_i_field")
    )))

    # Data Modeling + Semantic
    groups.append(("modeling.md", "Data Modeling & Semantic", (
        from_core("Model", "ModelDataModel", "ModelVersion", "ModelEntity",
                  "ModelEntityAssociation", "ModelAttribute", "ModelAttributeAssociation")
        + from_key("semantic_model")
        + from_key("semantic_dimension")
        + from_key("semantic_entity")
        + from_key("semantic_field")
        + from_key("semantic_measure")
        + from_key("cube")
        + from_key("cube_hierarchy")
        + from_key("cube_dimension")
        + from_key("cube_field")
    )))

    # SAP
    groups.append(("sap.md", "SAP", (
        from_key("s_a_p")
        + from_key("sap_erp_table")
        + from_key("sap_erp_column")
        + from_key("sap_erp_cds_view")
        + from_key("sap_erp_abap_program")
        + from_key("sap_erp_transaction_code")
        + from_key("sap_erp_component")
        + from_key("sap_erp_function_module")
        + from_key("sap_erp_view")
    )))

    # Salesforce
    groups.append(("salesforce.md", "Salesforce", (
        from_key("salesforce")
        + from_key("salesforce_object")
        + from_key("salesforce_field")
        + from_key("salesforce_organization")
        + from_key("salesforce_dashboard")
        + from_key("salesforce_report")
    )))

    # Cognite
    groups.append(("cognite.md", "Cognite", (
        from_key("cognite")
        + from_key("cognite_asset")
        + from_key("cognite_event")
        + from_key("cognite3_d_model")
        + from_key("cognite_sequence")
        + from_key("cognite_time_series")
        + from_key("cognite_file")
    )))

    # SageMaker
    groups.append(("sagemaker.md", "AWS SageMaker", (
        from_key("sage_maker_unified_studio")
        + from_key("sage_maker_unified_studio_project")
        + from_key("sage_maker_unified_studio_asset")
        + from_key("sage_maker_unified_studio_subscribed_asset")
        + from_key("sage_maker_unified_studio_published_asset")
        + from_key("sage_maker_unified_studio_asset_schema")
    )))

    # Dataverse + Dremio
    groups.append(("other-connectors.md", "Other Connectors", (
        from_key("dataverse")
        + from_key("dataverse_attribute")
        + from_key("dataverse_entity")
        + from_key("dremio")
        + from_key("dremio_virtual_dataset")
        + from_key("dremio_column")
        + from_key("dremio_space")
        + from_key("dremio_physical_dataset")
        + from_key("dremio_folder")
        + from_key("dremio_source")
    )))

    # Other assets
    groups.append(("other.md", "Other", (
        from_key("connection")
        + from_key("connection_process")
        + from_key("workflow")
        + from_key("workflow_run")
        + from_key("app_workflow_run")
        + from_key("notebook")
        + from_key("collection")
        + from_key("custom")
        + from_key("custom_entity")
        + from_key("badge")
        + from_key("tag_attachment")
        + from_key("source_tag")
        + from_key("task")
        + from_key("form")
        + from_key("data_set")
        + from_key("response")
        + from_key("incident")
        + from_key("insight")
        + from_key("saa_s")
        + from_key("multi_dimensional_dataset")
        + from_key("infrastructure")
        + from_key("process_execution")
        + from_key("readme_template")
        + from_key("atlan_app")
        + from_key("atlan_app_deployment")
        + from_key("atlan_app_installed")
        + from_key("flow_folder")
        + from_key("flow_project")
        + from_key("partial_v01_object")
        + from_core("App", "Application", "ApplicationField")
        + from_core("Stakeholder", "StakeholderTitle")
    )))

    return groups


def generate_page(title: str, entries: list) -> str:
    lines = [f"# {title}", ""]
    for ref, cls in entries:
        lines.append(f"## {cls}", )
        lines.append("")
        lines.append(f"::: {ref}")
        lines.append("")
    return "\n".join(lines)


def main():
    out_dir = "docs/api/assets"
    os.makedirs(out_dir, exist_ok=True)

    groups = build_groups()

    # Write overview index
    with open(f"{out_dir}/index.md", "w") as f:
        f.write("# Asset Models\n\n")
        f.write("All Atlan asset types, organised by connector or platform.\n\n")
        f.write("Use the navigation to browse assets by category.\n")

    nav_entries = []
    for filename, title, entries in groups:
        content = generate_page(title, entries)
        path = f"{out_dir}/{filename}"
        with open(path, "w") as f:
            f.write(content)
        nav_entries.append((title, f"api/assets/{filename}"))
        print(f"  wrote {path}  ({len(entries)} classes)")

    # Print mkdocs nav snippet
    print("\n── mkdocs.yml nav snippet ────────────────────────────────")
    print("    - Asset Models:")
    print("      - Overview: api/assets/index.md")
    for title, path in nav_entries:
        print(f"      - {title}: {path}")


if __name__ == "__main__":
    main()
