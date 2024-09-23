# Copyright 2024 Atlan Pte. Ltd.
# isort: skip_file
import lazy_loader as lazy

__PYATLAN_ASSETS__ = {
    "core": [
        "Referenceable",
        "Asset",
        "Process",
        "AtlasGlossaryCategory",
        "StakeholderTitle",
        "AccessControl",
        "Namespace",
        "Catalog",
        "AtlasGlossary",
        "AuthPolicy",
        "AtlasGlossaryTerm",
        "BIProcess",
        "ColumnProcess",
        "Persona",
        "Folder",
        "Airflow",
        "DataContract",
        "DataQuality",
        "BI",
        "Resource",
        "DataMesh",
        "SQL",
        "Matillion",
        "Dbt",
        "Spark",
        "Tag",
        "SchemaRegistry",
        "Stakeholder",
        "AirflowDag",
        "AirflowTask",
        "Anomalo",
        "MonteCarlo",
        "Metric",
        "Soda",
        "PowerBI",
        "Readme",
        "File",
        "Link",
        "DataDomain",
        "DataProduct",
        "Table",
        "Query",
        "Schema",
        "SnowflakePipe",
        "View",
        "MaterialisedView",
        "Function",
        "TablePartition",
        "Column",
        "DatabricksUnityCatalogTag",
        "SnowflakeStream",
        "Database",
        "CalculationView",
        "Procedure",
        "SnowflakeTag",
        "MatillionGroup",
        "MatillionJob",
        "MatillionProject",
        "MatillionComponent",
        "DbtModelColumn",
        "DbtTest",
        "DbtModel",
        "DbtMetric",
        "DbtSource",
        "SparkJob",
        "SchemaRegistrySubject",
        "AnomaloCheck",
        "MCIncident",
        "MCMonitor",
        "SodaCheck",
        "PowerBIReport",
        "PowerBIMeasure",
        "PowerBIColumn",
        "PowerBITable",
        "PowerBITile",
        "PowerBIDatasource",
        "PowerBIWorkspace",
        "PowerBIDataset",
        "PowerBIDashboard",
        "PowerBIDataflow",
        "PowerBIPage",
        "SnowflakeDynamicTable",
        "DynamoDBSecondaryIndex",
    ],
    "task": ["Task"],
    "data_set": ["DataSet"],
    "tag_attachment": ["TagAttachment"],
    "connection": ["Connection"],
    "workflow": ["Workflow"],
    "business_policy_log": ["BusinessPolicyLog"],
    "badge": ["Badge"],
    "business_policy": ["BusinessPolicy"],
    "workflow_run": ["WorkflowRun"],
    "process_execution": ["ProcessExecution"],
    "auth_service": ["AuthService"],
    "cloud": ["Cloud"],
    "infrastructure": ["Infrastructure"],
    "incident": ["Incident"],
    "business_policy_exception": ["BusinessPolicyException"],
    "dbt_process": ["DbtProcess"],
    "purpose": ["Purpose"],
    "collection": ["Collection"],
    "object_store": ["ObjectStore"],
    "saa_s": ["SaaS"],
    "d_m": ["DM"],
    "multi_dimensional_dataset": ["MultiDimensionalDataset"],
    "event_store": ["EventStore"],
    "no_s_q_l": ["NoSQL"],
    "model": ["Model"],
    "insight": ["Insight"],
    "a_p_i": ["API"],
    "google": ["Google"],
    "azure": ["Azure"],
    "a_w_s": ["AWS"],
    "business_policy_incident": ["BusinessPolicyIncident"],
    "dbt_column_process": ["DbtColumnProcess"],
    "s3": ["S3"],
    "a_d_l_s": ["ADLS"],
    "g_c_s": ["GCS"],
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
    "micro_strategy": ["MicroStrategy"],
    "cognos": ["Cognos"],
    "superset": ["Superset"],
    "qlik": ["Qlik"],
    "cognite": ["Cognite"],
    "salesforce": ["Salesforce"],
    "readme_template": ["ReadmeTemplate"],
    "d_m_entity_association": ["DMEntityAssociation"],
    "d_m_attribute": ["DMAttribute"],
    "d_m_attribute_association": ["DMAttributeAssociation"],
    "d_m_data_model": ["DMDataModel"],
    "d_m_version": ["DMVersion"],
    "d_m_entity": ["DMEntity"],
    "cube": ["Cube"],
    "cube_hierarchy": ["CubeHierarchy"],
    "cube_field": ["CubeField"],
    "cube_dimension": ["CubeDimension"],
    "kafka": ["Kafka"],
    "azure_service_bus": ["AzureServiceBus"],
    "cosmos_mongo_d_b": ["CosmosMongoDB"],
    "dynamo_d_b": ["DynamoDB"],
    "mongo_d_b": ["MongoDB"],
    "dbt_tag": ["DbtTag"],
    "model_attribute": ["ModelAttribute"],
    "model_entity": ["ModelEntity"],
    "model_version": ["ModelVersion"],
    "model_entity_association": ["ModelEntityAssociation"],
    "model_attribute_association": ["ModelAttributeAssociation"],
    "model_data_model": ["ModelDataModel"],
    "a_p_i_spec": ["APISpec"],
    "a_p_i_path": ["APIPath"],
    "data_studio_asset": ["DataStudioAsset"],
    "s3_bucket": ["S3Bucket"],
    "s3_object": ["S3Object"],
    "a_d_l_s_account": ["ADLSAccount"],
    "a_d_l_s_container": ["ADLSContainer"],
    "a_d_l_s_object": ["ADLSObject"],
    "g_c_s_object": ["GCSObject"],
    "g_c_s_bucket": ["GCSBucket"],
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
    "cognite3_d_model": ["Cognite3DModel"],
    "cognite_time_series": ["CogniteTimeSeries"],
    "cognite_file": ["CogniteFile"],
    "salesforce_object": ["SalesforceObject"],
    "salesforce_field": ["SalesforceField"],
    "salesforce_organization": ["SalesforceOrganization"],
    "salesforce_dashboard": ["SalesforceDashboard"],
    "salesforce_report": ["SalesforceReport"],
    "mongo_d_b_collection": ["MongoDBCollection"],
    "dynamo_dbtable": ["DynamoDBTable"],
    "mongo_d_b_database": ["MongoDBDatabase"],
    "kafka_topic": ["KafkaTopic"],
    "kafka_consumer_group": ["KafkaConsumerGroup"],
    "azure_service_bus_namespace": ["AzureServiceBusNamespace"],
    "azure_service_bus_topic": ["AzureServiceBusTopic"],
    "cosmos_mongo_d_b_account": ["CosmosMongoDBAccount"],
    "cosmos_mongo_d_b_collection": ["CosmosMongoDBCollection"],
    "cosmos_mongo_d_b_database": ["CosmosMongoDBDatabase"],
    "qlik_stream": ["QlikStream"],
    "dynamo_d_b_local_secondary_index": ["DynamoDBLocalSecondaryIndex"],
    "dynamo_d_b_global_secondary_index": ["DynamoDBGlobalSecondaryIndex"],
    "azure_event_hub": ["AzureEventHub"],
    "azure_event_hub_consumer_group": ["AzureEventHubConsumerGroup"],
}

lazy_loader = lazy.attach(__name__, submod_attrs=__PYATLAN_ASSETS__)
__getattr__, __dir__, __all__ = lazy_loader
