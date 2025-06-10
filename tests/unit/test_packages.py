from json import load, loads
from pathlib import Path
from unittest.mock import patch

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.assets.core import Asset
from pyatlan.model.enums import AssetDeltaHandling, AssetInputHandling, AssetRemovalType
from pyatlan.model.packages import (
    APITokenConnectionAdmin,
    AssetExportBasic,
    AssetImport,
    BigQueryCrawler,
    ConfluentKafkaCrawler,
    ConnectionDelete,
    DatabricksCrawler,
    DatabricksMiner,
    DbtCrawler,
    DynamoDBCrawler,
    GlueCrawler,
    LineageBuilder,
    LineageGenerator,
    MongoDBCrawler,
    OracleCrawler,
    PostgresCrawler,
    PowerBICrawler,
    RelationalAssetsBuilder,
    SigmaCrawler,
    SnowflakeCrawler,
    SnowflakeMiner,
    SQLServerCrawler,
    TableauCrawler,
)

PACKAGE_REQUESTS_DIR = Path(__file__).parent / "data" / "package_requests"
SNOWFLAKE_BASIC = "snowflake_basic.json"
SNOWFLAKE_KEYPAIR = "snowflake_keypair.json"
SNOWFLAKE_MINER_DEFAULT = "snowflake_miner_default.json"
SNOWFLAKE_MINER_SOURCE = "snowflake_miner_source.json"
SNOWFLAKE_MINER_S3_OFFLINE = "snowflake_miner_s3_offline.json"
GLUE_IAM_USER = "glue_iam_user.json"
TABLEAU_BASIC = "tableau_basic.json"
TABLEAU_ACCESS_TOKEN = "tableau_access_token.json"
TABLEAU_OFFLINE = "tableau_offline.json"
POWERBI_DELEGATED_USER = "powerbi_delegated_user.json"
POWEBI_SERVICE_PRINCIPAL = "powerbi_service_principal.json"
CONFLUENT_KAFKA_DIRECT = "confluent_kafka_direct.json"
DBT_CORE = "dbt_core.json"
DBT_CLOUD = "dbt_cloud.json"
SIGMA_API_TOKEN = "sigma_api_token.json"
SQL_SERVER_BASIC = "sql_server_basic.json"
BIG_QUERY_DIRECT = "big_query_direct.json"
DYNAMO_DB_IAM_USER = "dynamo_db_iam_user.json"
DYNAMO_DB_IAM_USER_ROLE = "dynamo_db_iam_user_role.json"
POSTGRES_DIRECT_BASIC = "postgres_direct_basic.json"
POSTGRES_DIRECT_IAM_USER = "postgres_direct_iam_user.json"
POSTGRES_DIRECT_IAM_ROLE = "postgres_direct_iam_role.json"
POSTGRES_S3_OFFLINE = "postgres_s3_offline.json"
CONNECTION_DELETE_HARD = "connection_delete_hard.json"
CONNECTION_DELETE_SOFT = "connection_delete_soft.json"
ASSET_IMPORT_S3 = "asset_import_s3.json"
ASSET_IMPORT_GCS = "asset_import_gcs.json"
ASSET_EXPORT_BASIC_GLOSSARIES = "asset_export_glossaries.json"
ASSET_IMPORT_ADLS = "asset_import_adls.json"
ASSET_IMPORT_DEFAULT = "asset_import_default.json"
ASSET_EXPORT_BASIC_GLOSSARIES_ONLY_S3 = "asset_export_basic_glossaries_s3.json"
ASSET_EXPORT_BASIC_PRODUCTS_ONLY_S3 = "asset_export_basic_products_s3.json"
ASSET_EXPORT_BASIC_ENRICHED_ONLY_S3 = "asset_export_basic_enriched_s3.json"
ASSET_EXPORT_BASIC_ALL_ASSETS_S3 = "asset_export_basic_all_assets_s3.json"
ASSET_EXPORT_BASIC_GLOSSARIES_ONLY_ADLS = "asset_export_basic_glossaries_adls.json"
ASSET_EXPORT_BASIC_ALL_ASSETS_ADLS = "asset_export_basic_all_assets_adls.json"
ASSET_EXPORT_BASIC_PRODUCTS_ONLY_ADLS = "asset_export_basic_products_adls.json"
ASSET_EXPORT_BASIC_ENRICHED_ONLY_ADLS = "asset_export_basic_enriched_adls.json"
ASSET_EXPORT_BASIC_ALL_ASSETS_GCS = "asset_export_basic_all_assets_gcs.json"
ASSET_EXPORT_BASIC_GLOSSARIES_ONLY_GCS = "asset_export_basic_glossaries_gcs.json"
ASSET_EXPORT_BASIC_PRODUCTS_ONLY_GCS = "asset_export_basic_products_gcs.json"
ASSET_EXPORT_BASIC_ENRICHED_ONLY_GCS = "asset_export_basic_enriched_gcs.json"
RELATIONAL_ASSETS_BUILDER_S3 = "relational_assets_builder_s3.json"
RELATIONAL_ASSETS_BUILDER_ADLS = "relational_assets_builder_adls.json"
RELATIONAL_ASSETS_BUILDER_GCS = "relational_assets_builder_gcs.json"
MONGODB_BASIC = "mongodb_basic.json"
DATABRICKS_BASIC_JDBC = "databricks_basic_jdbc.json"
DATABRICKS_BASIC_REST = "databricks_basic_rest.json"
DATABRICKS_AWS = "databricks_aws.json"
DATABRICKS_AZURE = "databricks_azure.json"
DATABRICKS_OFFLINE = "databricks_offline.json"
DATABRICKS_MINER_REST = "databricks_miner_rest.json"
DATABRICKS_MINER_OFFLINE = "databricks_miner_offline.json"
DATABRICKS_MINER_SYSTEM_TABLE = "databricks_miner_system_table.json"
DATABRICKS_MINER_POPULARITY_REST = "databricks_miner_popularity_rest.json"
DATABRICKS_MINER_POPULARITY_SYSTEM_TABLE = (
    "databricks_miner_popularity_system_table.json"
)
ORACLE_CRAWLER_BASIC = "oracle_crawler_basic.json"
ORACLE_CRAWLER_OFFLINE = "oracle_crawler_offline.json"
ORACLE_CRAWLER_BASIC_AGENT = "oracle_crawler_basic_agent.json"
ORACLE_CRAWLER_KERBEROS_AGENT = "oracle_crawler_kerberos_agent.json"
LINEAGE_BUILDER_S3 = "lineage_builder_s3.json"
LINEAGE_BUILDER_GCS = "lineage_builder_gcs.json"
LINEAGE_BUILDER_ADLS = "lineage_builder_adls.json"
LINEAGE_GENERATOR_DEFAULT = "lineage_generator_default.json"
LINEAGE_GENERATOR_FULL = "lineage_generator_full.json"
API_TOKEN_CONNECTION_ADMIN = "api_token_connection_admin.json"


class NonSerializable:
    pass


INVALID_REQ_ERROR = "ATLAN-PYTHON-400-014 Unable to translate the provided include/exclude asset filters into JSON"


def load_json(filename):
    with (PACKAGE_REQUESTS_DIR / filename).open() as input_file:
        return load(input_file)


@pytest.fixture()
def mock_get_epoch_timestamp():
    with patch("pyatlan.utils.get_epoch_timestamp") as mock_datetime:
        mock_datetime.return_value = 123456.123456
        yield mock_datetime


@pytest.fixture()
def mock_connection_guid():
    with patch("pyatlan.utils.random") as mock_random:
        mock_random.random.return_value = 123456789
        yield mock_random


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture()
def client():
    return AtlanClient()


@pytest.fixture()
def mock_package_env(
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
    mock_connection_guid,
    mock_get_epoch_timestamp,
):
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases


def test_snowflake_package(mock_package_env, client: AtlanClient):
    snowflake_with_connection_default = (
        SnowflakeCrawler(
            client=client,
            connection_name="test-snowflake-basic-conn",
            admin_roles=["admin-guid-1234"],
        )
        .information_schema(hostname="test-hostname")
        .basic_auth(
            username="test-user",
            password="test-pass",
            role="test-role",
            warehouse="test-warehouse",
        )
        .include(assets={"test-include": ["test-asset-1", "test-asset-2"]})
        .exclude(assets={})
        .lineage(True)
        .tags(True)
        .to_workflow()
    )
    request_json = loads(
        snowflake_with_connection_default.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(SNOWFLAKE_BASIC)

    snowflake_basic_auth = (
        SnowflakeCrawler(
            client=client,
            connection_name="test-snowflake-basic-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .information_schema(hostname="test-hostname")
        .basic_auth(
            username="test-user",
            password="test-pass",
            role="test-role",
            warehouse="test-warehouse",
        )
        .include(assets={"test-include": ["test-asset-1", "test-asset-2"]})
        .exclude(assets={})
        .lineage(True)
        .tags(True)
        .to_workflow()
    )
    request_json = loads(snowflake_basic_auth.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(SNOWFLAKE_BASIC)

    snowflake_keypair_auth = (
        SnowflakeCrawler(
            client=client,
            connection_name="test-snowflake-keypair-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .account_usage(
            hostname="test-hostname", database_name="test-db", schema_name="test-schema"
        )
        .keypair_auth(
            username="test-user",
            private_key="test-key",
            private_key_password="test-key-pass",
            role="test-role",
            warehouse="test-warehouse",
        )
        .include(assets={"test-include": ["test-asset-1", "test-asset-2"]})
        .exclude(assets={})
        .lineage(True)
        .tags(False)
        .to_workflow()
    )
    request_json = loads(snowflake_keypair_auth.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(SNOWFLAKE_KEYPAIR)


def test_glue_package(mock_package_env, client: AtlanClient):
    glue_iam_user_auth = (
        GlueCrawler(
            client=client,
            connection_name="test-glue-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .iam_user_auth(
            access_key="test-access-key",
            secret_key="test-secret-key",
        )
        .direct(region="test-region")
        .include(assets=["test-asset-1", "test-asset-2"])
        .exclude(assets=[])
        .to_workflow()
    )
    request_json = loads(glue_iam_user_auth.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(GLUE_IAM_USER)


def test_tableau_package(mock_package_env, client: AtlanClient):
    tableau_basic_auth = (
        TableauCrawler(
            client=client,
            connection_name="test-tableau-basic-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .direct(
            hostname="test.tableau.com", port=444, site="test-site", ssl_enabled=True
        )
        .basic_auth(
            username="test-username",
            password="test-password",
        )
        .include(projects=["test-project-guid-1", "test-project-guid-2"])
        .exclude(projects=[])
        .crawl_unpublished(True)
        .crawl_hidden_fields(False)
        .to_workflow()
    )
    request_json = loads(tableau_basic_auth.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(TABLEAU_BASIC)

    tableau_access_token_auth = (
        TableauCrawler(
            client=client,
            connection_name="test-tableau-access-token-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .direct(hostname="test.tableau.com", site="test-site", ssl_enabled=False)
        .personal_access_token(
            username="test-username",
            access_token="test-access-token",
        )
        .include(projects=["test-project-guid-1", "test-project-guid-2"])
        .exclude(projects=[])
        .crawl_unpublished(True)
        .crawl_hidden_fields(False)
        .to_workflow()
    )
    request_json = loads(
        tableau_access_token_auth.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(TABLEAU_ACCESS_TOKEN)

    tableau_offline = (
        TableauCrawler(
            client=client,
            connection_name="test-tableau-offline-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .s3(
            bucket_name="test-bucket",
            bucket_prefix="test-prefix",
            bucket_region="test-region",
        )
        .to_workflow()
    )
    request_json = loads(tableau_offline.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(TABLEAU_OFFLINE)


def test_powerbi_package(mock_package_env, client: AtlanClient):
    powerbi_delegated_user = (
        PowerBICrawler(
            client=client,
            connection_name="test-powerbi-du-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .direct()
        .delegated_user(
            username="test-username",
            password="test-password",
            tenant_id="test-tenant-id",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )
        .include(workspaces=["test-workspace-guid"])
        .exclude(workspaces=[])
        .to_workflow()
    )
    request_json = loads(powerbi_delegated_user.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(POWERBI_DELEGATED_USER)

    powerbi_service_principal = (
        PowerBICrawler(
            client=client,
            connection_name="test-powerbi-sp-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .direct()
        .service_principal(
            tenant_id="test-tenant-id",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )
        .include(workspaces=["test-workspace-guid"])
        .exclude(workspaces=[])
        .to_workflow()
    )
    request_json = loads(
        powerbi_service_principal.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(POWEBI_SERVICE_PRINCIPAL)


def test_confluent_kafka_package(mock_package_env, client: AtlanClient):
    conf_kafka_direct = (
        ConfluentKafkaCrawler(
            client=client,
            connection_name="test-conf-kafka-direct-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .direct(bootstrap="test-bootstrap-server:9092", encrypted=True)
        .api_token(api_key="test-api-key", api_secret="test-api-secret")
        .skip_internal(False)
        .include(regex=".*_TEST")
        .exclude(regex="")
        .to_workflow()
    )
    request_json = loads(conf_kafka_direct.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(CONFLUENT_KAFKA_DIRECT)


def test_dbt_package(mock_package_env, client: AtlanClient):
    dbt_core = (
        DbtCrawler(
            client=client,
            connection_name="test-dbt-core-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .core(
            s3_bucket="test-s3-bucket",
            s3_prefix="test-s3-prefix",
            s3_region="test-s3-region",
        )
        .limit_to_connection(connection_qualified_name="default/dbt/1234567890")
        .tags(True)
        .enrich_materialized_assets(True)
        .to_workflow()
    )
    request_json = loads(dbt_core.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(DBT_CORE)

    dbt_cloud = (
        DbtCrawler(
            client=client,
            connection_name="test-dbt-cloud-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .cloud(
            hostname="test-hostname",
            service_token="test-service-token",
            multi_tenant=False,
        )
        .limit_to_connection(connection_qualified_name="default/dbt/1234567890")
        .include(filter='{"1234":{"4321":{}}}')
        .exclude(filter="")
        .tags(True)
        .enrich_materialized_assets(False)
        .to_workflow()
    )
    request_json = loads(dbt_cloud.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(DBT_CLOUD)


def test_sigma_package(mock_package_env, client: AtlanClient):
    sigma_api_token = (
        SigmaCrawler(
            client=client,
            connection_name="test-sigma-basic-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .direct(hostname=SigmaCrawler.Hostname.AWS, port=1234)
        .api_token(client_id="test-client-id", api_token="test-api-token")
        .include(workbooks=["test-workbook-1", "test-workbook-2"])
        .exclude(workbooks=[])
        .to_workflow()
    )
    request_json = loads(sigma_api_token.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(SIGMA_API_TOKEN)


def test_sql_server_package(mock_package_env, client: AtlanClient):
    sql_server_basic = (
        SQLServerCrawler(
            client=client,
            connection_name="test-sigma-basic-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .direct(hostname="11.22.33.44", database="test-db", port=1234)
        .basic_auth(username="test-user", password="test-pass")
        .include(
            assets={
                "test-db": [
                    "test-schema-1",
                    "test-schema-2",
                ]
            }
        )
        .exclude(assets={})
        .to_workflow()
    )
    request_json = loads(sql_server_basic.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(SQL_SERVER_BASIC)


def test_snowflake_miner_package(mock_package_env):
    # With default configuration
    snowflake_miner_default = (
        SnowflakeMiner(connection_qualified_name="default/snowflake/1234567890")
        .direct(start_epoch=9876543210, database="TEST_SNOWFLAKE", schema="TEST_SCHEMA")
        .exclude_users(users=["test-user-1", "test-user-2"])
        .to_workflow()
    )
    request_json = loads(snowflake_miner_default.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(SNOWFLAKE_MINER_DEFAULT)

    # With advanced configuration (source)
    snowflake_miner_source = (
        SnowflakeMiner(connection_qualified_name="default/snowflake/1234567890")
        .direct(start_epoch=9876543210, database="TEST_SNOWFLAKE", schema="TEST_SCHEMA")
        .exclude_users(users=["test-user-1", "test-user-2"])
        .popularity_window(days=15)
        .native_lineage(enabled=True)
        .custom_config(config={"test": True, "feature": 1234})
        .to_workflow()
    )
    request_json = loads(snowflake_miner_source.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(SNOWFLAKE_MINER_SOURCE)

    # With advanced configuration (offline)
    snowflake_miner_s3_offline = (
        SnowflakeMiner(connection_qualified_name="default/snowflake/1234567890")
        .s3(
            s3_bucket="test-s3-bucket",
            s3_prefix="test-s3-prefix",
            s3_bucket_region="test-s3-bucket-region",
            sql_query_key="TEST_QUERY",
            default_database_key="TEST_SNOWFLAKE",
            default_schema_key="TEST_SCHEMA",
            session_id_key="TEST_SESSION_ID",
        )
        .popularity_window(days=15)
        .native_lineage(enabled=True)
        .custom_config(config={"test": True, "feature": 1234})
        .to_workflow()
    )
    request_json = loads(
        snowflake_miner_s3_offline.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(SNOWFLAKE_MINER_S3_OFFLINE)


def test_databricks_miner_package(mock_package_env):
    databricks_miner_rest = (
        DatabricksMiner(connection_qualified_name="default/databricks/1234567890")
        .rest_api()
        .to_workflow()
    )
    request_json = loads(databricks_miner_rest.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(DATABRICKS_MINER_REST)

    databricks_miner_offline = (
        DatabricksMiner(connection_qualified_name="default/databricks/1234567890")
        .offline(bucket_name="test-bucket", bucket_prefix="test-prefix")
        .to_workflow()
    )
    request_json = loads(
        databricks_miner_offline.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(DATABRICKS_MINER_OFFLINE)

    databricks_miner_system_table = (
        DatabricksMiner(connection_qualified_name="default/databricks/1234567890")
        .system_table(warehouse_id="test-warehouse-id")
        .to_workflow()
    )
    request_json = loads(
        databricks_miner_system_table.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(DATABRICKS_MINER_SYSTEM_TABLE)

    databricks_miner_popularity_rest = (
        DatabricksMiner(connection_qualified_name="default/databricks/1234567890")
        .rest_api()
        .popularity_configuration(
            start_date="1234567890",
            window_days=10,
            excluded_users=["test-user-1", "test-user-2"],
        )
        .to_workflow()
    )
    request_json = loads(
        databricks_miner_popularity_rest.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(DATABRICKS_MINER_POPULARITY_REST)

    databricks_miner_popularity_system_table = (
        DatabricksMiner(connection_qualified_name="default/databricks/1234567890")
        .rest_api()
        .popularity_configuration(
            start_date="1234567890",
            window_days=10,
            excluded_users=["test-user-1", "test-user-2"],
            warehouse_id="test-warehouse-id",
            extraction_method=DatabricksMiner.ExtractionMethod.SYSTEM_TABLE,
        )
        .to_workflow()
    )
    request_json = loads(
        databricks_miner_popularity_system_table.json(by_alias=True, exclude_none=True)
    )

    assert request_json == load_json(DATABRICKS_MINER_POPULARITY_SYSTEM_TABLE)


def test_big_query_package(mock_package_env, client: AtlanClient):
    big_query_direct = (
        BigQueryCrawler(
            client=client,
            connection_name="test-big-query-conn",
            admin_roles=["admin-guid-1234"],
        )
        .service_account_auth(
            project_id="test-project-id",
            service_account_json="test-account-json",
            service_account_email="test@test.com",
        )
        .include(assets={"test-include": ["test-asset-1", "test-asset-2"]})
        .exclude(assets={})
        .exclude_regex(regex=".*_TEST")
        .custom_config(config={"test": True, "feature": 1234})
        .to_workflow()
    )
    request_json = loads(big_query_direct.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(BIG_QUERY_DIRECT)


def test_dynamo_db_package(mock_package_env, client: AtlanClient):
    dynamo_db_direct_iam_user = (
        DynamoDBCrawler(
            client=client,
            connection_name="test-dynamodb-conn",
            admin_roles=["admin-guid-1234"],
        )
        .direct(region="test-region")
        .iam_user_auth(access_key="test-access-key", secret_key="test-secret-key")
        .include_regex(regex=".*_TEST_INCLUDE")
        .exclude_regex(regex=".*_TEST_EXCLUDE")
        .to_workflow()
    )
    request_json = loads(
        dynamo_db_direct_iam_user.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(DYNAMO_DB_IAM_USER)

    dynamo_db_direct_iam_user_role = (
        DynamoDBCrawler(
            client=client,
            connection_name="test-dynamodb-conn",
            admin_roles=["admin-guid-1234"],
        )
        .direct(region="test-region")
        .iam_role_auth(
            arn="arn:aws:iam::123456789012:user/test", external_id="test-ext-id"
        )
        .include_regex(regex=".*_TEST_INCLUDE")
        .exclude_regex(regex=".*_TEST_EXCLUDE")
        .to_workflow()
    )
    request_json = loads(
        dynamo_db_direct_iam_user_role.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(DYNAMO_DB_IAM_USER_ROLE)


def test_postgres_package(mock_package_env, client: AtlanClient):
    postgres_direct_basic = (
        PostgresCrawler(
            client=client,
            connection_name="test-sdk-postgresql",
            admin_roles=["admin-guid-1234"],
        )
        .direct(hostname="test.com", database="test-db")
        .basic_auth(
            username="test-user",
            password="test-password",
        )
        .include(assets={"test-include": ["test-asset-1", "test-asset-2"]})
        .exclude(assets={})
        .exclude_regex(regex=".*_TEST")
        .source_level_filtering(enable=True)
        .jdbc_internal_methods(enable=True)
        .to_workflow()
    )

    request_json = loads(postgres_direct_basic.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(POSTGRES_DIRECT_BASIC)

    postgres_direct_iam_user = (
        PostgresCrawler(
            client=client,
            connection_name="test-sdk-postgresql",
            admin_roles=["admin-guid-1234"],
        )
        .direct(hostname="test.com", database="test-db")
        .iam_user_auth(
            username="test-user",
            access_key="test-access-key",
            secret_key="test-secret-key",
        )
        .include(assets={"test-include": ["test-asset-1", "test-asset-2"]})
        .exclude(assets={})
        .exclude_regex(regex=".*_TEST")
        .source_level_filtering(enable=True)
        .jdbc_internal_methods(enable=True)
        .to_workflow()
    )

    request_json = loads(
        postgres_direct_iam_user.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(POSTGRES_DIRECT_IAM_USER)

    postgres_direct_iam_role = (
        PostgresCrawler(
            client=client,
            connection_name="test-sdk-postgresql",
            admin_roles=["admin-guid-1234"],
        )
        .direct(hostname="test.com", database="test-db")
        .iam_role_auth(
            username="test-user",
            arn="arn:aws:iam::123456789012:user/test",
            external_id="test-ext-id",
        )
        .include(assets={"test-include": ["test-asset-1", "test-asset-2"]})
        .exclude(assets={})
        .exclude_regex(regex=".*_TEST")
        .source_level_filtering(enable=True)
        .jdbc_internal_methods(enable=True)
        .to_workflow()
    )

    request_json = loads(
        postgres_direct_iam_role.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(POSTGRES_DIRECT_IAM_ROLE)

    postgres_s3_offline = (
        PostgresCrawler(
            client=client,
            connection_name="test-sdk-postgresql",
            admin_roles=["admin-guid-1234"],
        )
        .s3(
            bucket_name="test-bucket",
            bucket_prefix="test-prefix",
            bucket_region="test-region",
        )
        .include(assets={"test-include": ["test-asset-1", "test-asset-2"]})
        .exclude(assets={})
        .exclude_regex(regex=".*_TEST")
        .source_level_filtering(enable=True)
        .jdbc_internal_methods(enable=True)
        .to_workflow()
    )

    request_json = loads(postgres_s3_offline.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(POSTGRES_S3_OFFLINE)


def test_mongodb_package(mock_package_env, client: AtlanClient):
    mongodb_basic = (
        MongoDBCrawler(
            client=client,
            connection_name="test-sdk-mongodb",
            admin_roles=["admin-guid-1234"],
        )
        .direct(hostname="test-hostname", port=1234)
        .basic_auth(
            username="test-user",
            password="test-pass",
            native_host="test-native-host",
            default_db="test-default-db",
            auth_db="test-auth-db",
            is_ssl=False,
        )
        .include(assets=["test-asset-1", "test-asset-2"])
        .exclude(assets=["test-asset-1", "test-asset-2"])
        .exclude_regex(regex="TEST*")
        .to_workflow()
    )

    request_json = loads(mongodb_basic.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(MONGODB_BASIC)


def test_connection_delete_package(mock_package_env):
    # With PURGE (hard delete)
    connection_delete_hard = ConnectionDelete(
        qualified_name="default/snowflake/1234567890", purge=True
    ).to_workflow()
    request_json = loads(connection_delete_hard.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(CONNECTION_DELETE_HARD)

    # Without PURGE (soft delete)
    connection_delete_soft = ConnectionDelete(
        qualified_name="default/snowflake/1234567890", purge=False
    ).to_workflow()
    request_json = loads(connection_delete_soft.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(CONNECTION_DELETE_SOFT)


def test_databricks_crawler(mock_package_env, client: AtlanClient):
    databricks_basic_jdbc = (
        DatabricksCrawler(
            client=client,
            connection_name="test-databricks-basic",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
            row_limit=10000,
            allow_query=True,
            allow_query_preview=True,
        )
        .direct(hostname="test-hostname")
        .basic_auth(
            personal_access_token="test-pat",
            http_path="test-http-path",
        )
        .metadata_extraction_method(type=DatabricksCrawler.ExtractionMethod.JDBC)
        .include(assets={"test-include": ["ti1", "ti2"]})
        .exclude(assets={"test-exclude": ["te1", "te2"]})
        .exclude_regex(regex="TEST*")
        .enable_view_lineage(False)
        .enable_source_level_filtering(True)
        .to_workflow()
    )
    request_json = loads(databricks_basic_jdbc.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(DATABRICKS_BASIC_JDBC)

    databricks_basic_rest = (
        DatabricksCrawler(
            client=client,
            connection_name="test-databricks-basic",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
            row_limit=10000,
            allow_query=True,
            allow_query_preview=True,
        )
        .direct(hostname="test-hostname")
        .basic_auth(
            personal_access_token="test-pat",
            http_path="test-http-path",
        )
        .metadata_extraction_method(type=DatabricksCrawler.ExtractionMethod.REST)
        .include_for_rest_api(assets=["ti1", "ti2"])
        .exclude_for_rest_api(assets=["te1", "te2"])
        .sql_warehouse(warehouse_ids=["3d939b0cc668be06", "9a289b0cc838ce62"])
        .import_tags(True)
        .enable_source_level_filtering(False)
        .to_workflow()
    )
    request_json = loads(databricks_basic_rest.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(DATABRICKS_BASIC_REST)

    databricks_aws = (
        DatabricksCrawler(
            client=client,
            connection_name="test-databricks-basic",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
            row_limit=10000,
            allow_query=True,
            allow_query_preview=True,
        )
        .direct(hostname="test-hostname")
        .aws_service(
            client_id="test-client-id",
            client_secret="test-client-secret",
        )
        .metadata_extraction_method(type=DatabricksCrawler.ExtractionMethod.REST)
        .include_for_rest_api(assets=["ti1", "ti2"])
        .exclude_for_rest_api(assets=["te1", "te2"])
        .sql_warehouse(warehouse_ids=["3d939b0cc668be06", "9a289b0cc838ce62"])
        .import_tags(True)
        .enable_source_level_filtering(False)
        .to_workflow()
    )
    request_json = loads(databricks_aws.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(DATABRICKS_AWS)

    databricks_azure = (
        DatabricksCrawler(
            client=client,
            connection_name="test-databricks-basic",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
            row_limit=10000,
            allow_query=True,
            allow_query_preview=True,
        )
        .direct(hostname="test-hostname")
        .azure_service(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        .metadata_extraction_method(type=DatabricksCrawler.ExtractionMethod.REST)
        .include_for_rest_api(assets=["ti1", "ti2"])
        .exclude_for_rest_api(assets=["te1", "te2"])
        .sql_warehouse(warehouse_ids=["3d939b0cc668be06", "9a289b0cc838ce62"])
        .import_tags(True)
        .enable_source_level_filtering(False)
        .to_workflow()
    )
    request_json = loads(databricks_azure.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(DATABRICKS_AZURE)

    databricks_offline = (
        DatabricksCrawler(
            client=client,
            connection_name="test-databricks-basic",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
            row_limit=10000,
            allow_query=True,
            allow_query_preview=True,
        )
        .s3(
            bucket_name="test-bucket",
            bucket_prefix="test-prefix",
            bucket_region="test-region",
        )
        .to_workflow()
    )
    request_json = loads(databricks_offline.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(DATABRICKS_OFFLINE)


def test_asset_import(mock_package_env):
    # Case 1: Importing assets, glossaries, and data products from S3 with advanced configuration
    asset_import_s3 = (
        AssetImport()
        .object_store()
        .s3(
            access_key="test-access-key",
            secret_key="test-secret-key",
            bucket="my-bucket",
            region="us-west-1",
        )
        .assets(
            prefix="/test/prefix",
            object_key="assets-test.csv",
            input_handling=AssetInputHandling.PARTIAL,
        )
        .assets_advanced(
            remove_attributes=[Asset.CERTIFICATE_STATUS, Asset.ANNOUNCEMENT_TYPE],
            fail_on_errors=True,
            case_sensitive_match=False,
            field_separator=",",
            batch_size=20,
        )
        .glossaries(
            prefix="/test/prefix",
            object_key="glossaries-test.csv",
            input_handling=AssetInputHandling.UPDATE,
        )
        .glossaries_advanced(
            remove_attributes=[Asset.CERTIFICATE_STATUS, Asset.ANNOUNCEMENT_TYPE],
            fail_on_errors=True,
            field_separator=",",
            batch_size=20,
        )
        .data_products(
            prefix="/test/prefix",
            object_key="data-products-test.csv",
            input_handling=AssetInputHandling.UPDATE,
        )
        .data_product_advanced(
            remove_attributes=[Asset.CERTIFICATE_STATUS, Asset.ANNOUNCEMENT_TYPE],
            fail_on_errors=True,
            field_separator=",",
            batch_size=20,
        )
    ).to_workflow()

    request_json_s3 = loads(asset_import_s3.json(by_alias=True, exclude_none=True))
    assert request_json_s3 == load_json(ASSET_IMPORT_S3)

    # Case 2: Importing assets, glossaries, and data products from GCS with advanced configuration
    asset_import_gcs = (
        AssetImport()
        .object_store()
        .gcs(
            service_account_json="test-service-account-json",
            project_id="test-project-id",
            bucket="my-bucket",
        )
        .assets(
            prefix="/test/prefix",
            object_key="assets-test.csv",
            input_handling=AssetInputHandling.UPSERT,
        )
        .assets_advanced(
            remove_attributes=[Asset.CERTIFICATE_STATUS, Asset.ANNOUNCEMENT_TYPE],
            fail_on_errors=True,
            case_sensitive_match=False,
            field_separator=",",
            batch_size=20,
        )
        .glossaries(
            prefix="/test/prefix",
            object_key="glossaries-test.csv",
            input_handling=AssetInputHandling.UPDATE,
        )
        .glossaries_advanced(
            remove_attributes=[Asset.CERTIFICATE_STATUS, Asset.ANNOUNCEMENT_TYPE],
            fail_on_errors=True,
            field_separator=",",
            batch_size=20,
        )
        .data_products(
            prefix="/test/prefix",
            object_key="data-products-test.csv",
            input_handling=AssetInputHandling.UPDATE,
        )
        .data_product_advanced(
            remove_attributes=[Asset.CERTIFICATE_STATUS, Asset.ANNOUNCEMENT_TYPE],
            fail_on_errors=True,
            field_separator=",",
            batch_size=20,
        )
    ).to_workflow()

    request_json_gcs = loads(asset_import_gcs.json(by_alias=True, exclude_none=True))
    assert request_json_gcs == load_json(ASSET_IMPORT_GCS)

    # Case 3: Importing assets, glossaries, and data products from Adls with advanced configuration
    asset_import_adls = (
        AssetImport()
        .object_store()
        .adls(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
            account_name="test-storage-account",
            container="test-adls-container",
        )
        .assets(
            prefix="/test/prefix",
            object_key="assets-test.csv",
            input_handling=AssetInputHandling.UPSERT,
        )
        .assets_advanced(
            remove_attributes=[Asset.CERTIFICATE_STATUS, Asset.ANNOUNCEMENT_TYPE],
            fail_on_errors=True,
            case_sensitive_match=False,
            field_separator=",",
            batch_size=20,
        )
        .glossaries(
            prefix="/test/prefix",
            object_key="glossaries-test.csv",
            input_handling=AssetInputHandling.UPDATE,
        )
        .glossaries_advanced(
            remove_attributes=[Asset.CERTIFICATE_STATUS, Asset.ANNOUNCEMENT_TYPE],
            fail_on_errors=True,
            field_separator=",",
            batch_size=20,
        )
        .data_products(
            prefix="/test/prefix",
            object_key="data-products-test.csv",
            input_handling=AssetInputHandling.UPDATE,
        )
        .data_product_advanced(
            remove_attributes=[Asset.CERTIFICATE_STATUS, Asset.ANNOUNCEMENT_TYPE],
            fail_on_errors=True,
            field_separator=",",
            batch_size=20,
        )
    ).to_workflow()

    request_json_adls = loads(asset_import_adls.json(by_alias=True, exclude_none=True))
    assert request_json_adls == load_json(ASSET_IMPORT_ADLS)

    # Case 4: Importing assets, glossaries, and data products from S3 with default configuration
    asset_import_default = (
        AssetImport()
        .object_store()
        .s3(
            access_key="test-access-key",
            secret_key="test-secret-key",
            bucket="my-bucket",
            region="us-west-1",
        )
        .assets(
            prefix="/test/prefix",
            object_key="assets-test.csv",
            input_handling=AssetInputHandling.UPDATE,
        )
        .glossaries(
            prefix="/test/prefix",
            object_key="glossaries-test.csv",
            input_handling=AssetInputHandling.UPSERT,
        )
        .data_products(
            prefix="/test/prefix",
            object_key="data-products-test.csv",
            input_handling=AssetInputHandling.UPSERT,
        )
    ).to_workflow()

    request_json_default = loads(
        asset_import_default.json(by_alias=True, exclude_none=True)
    )
    assert request_json_default == load_json(ASSET_IMPORT_DEFAULT)


def test_asset_export_basic(mock_package_env):
    # Case 1: Export assets with glossaries only using s3
    asset_export_basic_glossaries_only_s3 = (
        AssetExportBasic()
        .glossaries_only(include_archived=True)
        .object_store(prefix="/test/prefix")
        .s3(
            access_key="test-access-key",
            secret_key="test-secret-key",
            bucket="my-bucket",
            region="us-west-1",
        )
    ).to_workflow()

    request_json_s3 = loads(
        asset_export_basic_glossaries_only_s3.json(by_alias=True, exclude_none=True)
    )
    assert request_json_s3 == load_json(ASSET_EXPORT_BASIC_GLOSSARIES_ONLY_S3)

    # Case 2: Export assets with Products only using s3
    asset_export_basic_products_only_s3 = (
        AssetExportBasic()
        .products_only(include_archived=True)
        .object_store(prefix="/test/prefix")
        .s3(
            access_key="test-access-key",
            secret_key="test-secret-key",
            bucket="my-bucket",
            region="us-west-1",
        )
    ).to_workflow()

    request_json_s3 = loads(
        asset_export_basic_products_only_s3.json(by_alias=True, exclude_none=True)
    )
    assert request_json_s3 == load_json(ASSET_EXPORT_BASIC_PRODUCTS_ONLY_S3)

    # Case 3: Export assets with Enriched only using s3
    asset_export_basic_enriched_only_s3 = (
        AssetExportBasic()
        .enriched_only(
            prefix="/test/prefix",
            include_description=True,
            include_glossaries=True,
            include_data_products=True,
            include_archived=True,
        )
        .object_store(prefix="/test/prefix")
        .s3(
            access_key="test-access-key",
            secret_key="test-secret-key",
            bucket="my-bucket",
            region="us-west-1",
        )
    ).to_workflow()

    request_json_s3 = loads(
        asset_export_basic_enriched_only_s3.json(by_alias=True, exclude_none=True)
    )
    assert request_json_s3 == load_json(ASSET_EXPORT_BASIC_ENRICHED_ONLY_S3)

    # Case 4: Export all assets using s3
    asset_export_basic_all_assets_s3 = (
        AssetExportBasic()
        .all_assets(
            prefix="/test/prefix",
            include_description=True,
            include_glossaries=True,
            include_data_products=True,
            include_archived=True,
        )
        .object_store(prefix="/test/prefix")
        .s3(
            access_key="test-access-key",
            secret_key="test-secret-key",
            bucket="my-bucket",
            region="us-west-1",
        )
    ).to_workflow()

    request_json_s3 = loads(
        asset_export_basic_all_assets_s3.json(by_alias=True, exclude_none=True)
    )
    assert request_json_s3 == load_json(ASSET_EXPORT_BASIC_ALL_ASSETS_S3)

    # Case 1: Export assets with glossaries only using adls
    asset_export_basic_glossaries_only_adls = (
        AssetExportBasic()
        .glossaries_only(include_archived=True)
        .object_store(prefix="/test/prefix")
        .adls(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
            account_name="test-storage-account",
            container="test-adls-container",
        )
    ).to_workflow()

    request_json_adls = loads(
        asset_export_basic_glossaries_only_adls.json(by_alias=True, exclude_none=True)
    )
    assert request_json_adls == load_json(ASSET_EXPORT_BASIC_GLOSSARIES_ONLY_ADLS)

    # Case 2: Export assets with Products only using adls
    asset_export_basic_products_only_adls = (
        AssetExportBasic()
        .products_only(include_archived=True)
        .object_store(prefix="/test/prefix")
        .adls(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
            account_name="test-storage-account",
            container="test-adls-container",
        )
    ).to_workflow()

    request_json_adls = loads(
        asset_export_basic_products_only_adls.json(by_alias=True, exclude_none=True)
    )
    assert request_json_adls == load_json(ASSET_EXPORT_BASIC_PRODUCTS_ONLY_ADLS)

    # Case 3: Export assets with Enriched only using adls
    asset_export_basic_enriched_only_adls = (
        AssetExportBasic()
        .enriched_only(
            prefix="/test/prefix",
            include_description=True,
            include_glossaries=True,
            include_data_products=True,
            include_archived=True,
        )
        .object_store(prefix="/test/prefix")
        .adls(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
            account_name="test-storage-account",
            container="test-adls-container",
        )
    ).to_workflow()

    request_json_adls = loads(
        asset_export_basic_enriched_only_adls.json(by_alias=True, exclude_none=True)
    )
    assert request_json_adls == load_json(ASSET_EXPORT_BASIC_ENRICHED_ONLY_ADLS)

    # Case 4: Export all assets using adls
    asset_export_basic_all_assets_adls = (
        AssetExportBasic()
        .all_assets(
            prefix="/test/prefix",
            include_description=True,
            include_glossaries=True,
            include_data_products=True,
            include_archived=True,
        )
        .object_store(prefix="/test/prefix")
        .adls(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
            account_name="test-storage-account",
            container="test-adls-container",
        )
    ).to_workflow()

    request_json_adls = loads(
        asset_export_basic_all_assets_adls.json(by_alias=True, exclude_none=True)
    )
    assert request_json_adls == load_json(ASSET_EXPORT_BASIC_ALL_ASSETS_ADLS)

    # Case 1: Export assets with glossaries only using gcs
    asset_export_basic_glossaries_only_gcs = (
        AssetExportBasic()
        .glossaries_only(include_archived=True)
        .object_store(prefix="/test/prefix")
        .gcs(
            service_account_json="test-service-account-json",
            project_id="test-project-id",
            bucket="my-bucket",
        )
    ).to_workflow()

    request_json_gcs = loads(
        asset_export_basic_glossaries_only_gcs.json(by_alias=True, exclude_none=True)
    )
    assert request_json_gcs == load_json(ASSET_EXPORT_BASIC_GLOSSARIES_ONLY_GCS)

    # Case 2: Export assets with Products only using gcs
    asset_export_basic_products_only_gcs = (
        AssetExportBasic()
        .products_only(include_archived=True)
        .object_store(prefix="/test/prefix")
        .gcs(
            service_account_json="test-service-account-json",
            project_id="test-project-id",
            bucket="my-bucket",
        )
    ).to_workflow()

    request_json_gcs = loads(
        asset_export_basic_products_only_gcs.json(by_alias=True, exclude_none=True)
    )
    assert request_json_gcs == load_json(ASSET_EXPORT_BASIC_PRODUCTS_ONLY_GCS)

    # Case 3: Export assets with Enriched only using adls
    asset_export_basic_enriched_only_gcs = (
        AssetExportBasic()
        .enriched_only(
            prefix="/test/prefix",
            include_description=True,
            include_glossaries=True,
            include_data_products=True,
            include_archived=True,
        )
        .object_store(prefix="/test/prefix")
        .gcs(
            service_account_json="test-service-account-json",
            project_id="test-project-id",
            bucket="my-bucket",
        )
    ).to_workflow()

    request_json_gcs = loads(
        asset_export_basic_enriched_only_gcs.json(by_alias=True, exclude_none=True)
    )
    assert request_json_gcs == load_json(ASSET_EXPORT_BASIC_ENRICHED_ONLY_GCS)

    # Case 4: Export all assets using adls
    asset_export_basic_all_assets_gcs = (
        AssetExportBasic()
        .all_assets(
            prefix="/test/prefix",
            include_description=True,
            include_glossaries=True,
            include_data_products=True,
            include_archived=True,
        )
        .object_store(prefix="/test/prefix")
        .gcs(
            service_account_json="test-service-account-json",
            project_id="test-project-id",
            bucket="my-bucket",
        )
    ).to_workflow()

    request_json_gcs = loads(
        asset_export_basic_all_assets_gcs.json(by_alias=True, exclude_none=True)
    )
    assert request_json_gcs == load_json(ASSET_EXPORT_BASIC_ALL_ASSETS_GCS)


def test_relational_assets_builder(mock_package_env):
    # Case 1: Build/Update relational assets from S3 with advanced configuration
    relational_assets_builder_s3 = (
        RelationalAssetsBuilder()
        .object_store(
            prefix="/test/prefix",
            object_key="assets-test.csv",
        )
        .s3(
            access_key="test-access-key",
            secret_key="test-secret-key",
            bucket="my-bucket",
            region="us-west-1",
        )
        .assets_semantics(
            input_handling=AssetInputHandling.UPSERT,
            delta_handling=AssetDeltaHandling.INCREMENTAL,
        )
        .options(
            remove_attributes=[Asset.CERTIFICATE_STATUS, Asset.ANNOUNCEMENT_TYPE],
            fail_on_errors=True,
            field_separator=",",
            batch_size=20,
        )
    ).to_workflow()

    request_json_s3 = loads(
        relational_assets_builder_s3.json(by_alias=True, exclude_none=True)
    )
    assert request_json_s3 == load_json(RELATIONAL_ASSETS_BUILDER_S3)

    # Case 2: Build/Update relational assets from adls with advanced configuration
    relational_assets_builder_adls = (
        RelationalAssetsBuilder()
        .object_store(
            prefix="/test/prefix",
            object_key="assets-test.csv",
        )
        .adls(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
            account_name="test-storage-account",
            container="test-adls-container",
        )
        .assets_semantics(
            input_handling=AssetInputHandling.PARTIAL,
            delta_handling=AssetDeltaHandling.FULL_REPLACEMENT,
            removal_type=AssetRemovalType.ARCHIVE,
        )
        .options(
            remove_attributes=[Asset.CERTIFICATE_STATUS, Asset.ANNOUNCEMENT_TYPE],
            fail_on_errors=True,
            field_separator=",",
            batch_size=20,
        )
    ).to_workflow()

    request_json_adls = loads(
        relational_assets_builder_adls.json(by_alias=True, exclude_none=True)
    )
    assert request_json_adls == load_json(RELATIONAL_ASSETS_BUILDER_ADLS)

    # Case 3: Build/Update relational assets from gcs with advanced configuration
    relational_assets_builder_gcs = (
        RelationalAssetsBuilder()
        .object_store(
            prefix="/test/prefix",
            object_key="assets-test.csv",
        )
        .gcs(
            service_account_json="test-service-account-json",
            project_id="test-project-id",
            bucket="my-bucket",
        )
        .assets_semantics(
            input_handling=AssetInputHandling.UPDATE,
            delta_handling=AssetDeltaHandling.FULL_REPLACEMENT,
            removal_type=AssetRemovalType.PURGE,
        )
        .options(
            remove_attributes=[Asset.CERTIFICATE_STATUS, Asset.ANNOUNCEMENT_TYPE],
            fail_on_errors=True,
            field_separator=",",
            batch_size=20,
        )
    ).to_workflow()

    request_json_gcs = loads(
        relational_assets_builder_gcs.json(by_alias=True, exclude_none=True)
    )
    assert request_json_gcs == load_json(RELATIONAL_ASSETS_BUILDER_GCS)


def test_oracle_crawler(mock_package_env, client: AtlanClient):
    oracle_crawler_basic = (
        OracleCrawler(
            client=client,
            connection_name="test-oracle-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .direct(hostname="test-hostname", port=1234)
        .basic_auth(
            username="test-username",
            password="test-password",
            sid="test-sid",
            database_name="test-db",
        )
        .include(assets={"t1": ["t11", "t12", "t13"]})
        .exclude(assets={"t2": ["t21", "t22", "t23"]})
        .exclude_regex("TEST*")
        .jdbc_internal_methods(True)
        .source_level_filtering(True)
        .to_workflow()
    )
    request_json = loads(oracle_crawler_basic.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(ORACLE_CRAWLER_BASIC)

    oracle_crawler_offline = (
        OracleCrawler(
            client=client,
            connection_name="test-oracle-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .s3(bucket_name="test-bucket", bucket_prefix="test-prefix")
        .to_workflow()
    )
    request_json = loads(oracle_crawler_offline.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(ORACLE_CRAWLER_OFFLINE)

    oracle_crawler_basic_agent = (
        OracleCrawler(
            client=client,
            connection_name="test-oracle-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .agent_config(
            hostname="test.oracle.com",
            port=1234,
            auth_type=OracleCrawler.AuthType.BASIC,
            default_db_name="test-db",
            sid="test-sid",
            agent_name="test-agent",
            aws_region="us-east-1",
            aws_auth_method=OracleCrawler.AwsAuthMethod.IAM_ASSUME_ROLE,
            secret_store=OracleCrawler.SecretStore.AWS_SECRET_MANAGER,
            secret_path="some/test/path",
            agent_custom_config={"test": "config"},
        )
        .include(assets={"t1": ["t11", "t12", "t13"]})
        .exclude(assets={"t2": ["t21", "t22", "t23"]})
        .jdbc_internal_methods(True)
        .source_level_filtering(False)
        .to_workflow()
    )
    request_json = loads(
        oracle_crawler_basic_agent.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(ORACLE_CRAWLER_BASIC_AGENT)

    oracle_crawler_kerberos_agent = (
        OracleCrawler(
            client=client,
            connection_name="test-oracle-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .agent_config(
            hostname="test.oracle.com",
            port=1234,
            auth_type=OracleCrawler.AuthType.KERBEROS,
            default_db_name="test-db",
            sid="test-sid",
            agent_name="test-agent",
            principal="test-principal",
            secret_store=OracleCrawler.SecretStore.SECRET_INJECTION_ENV,
            user_env_var="test-user-env",
            password_env_var="test-pass-env",
            agent_custom_config={"test": "config"},
        )
        .include(assets={"t1": ["t11", "t12", "t13"]})
        .exclude(assets={"t2": ["t21", "t22", "t23"]})
        .jdbc_internal_methods(True)
        .source_level_filtering(False)
        .to_workflow()
    )
    request_json = loads(
        oracle_crawler_kerberos_agent.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(ORACLE_CRAWLER_KERBEROS_AGENT)


def test_lineage_builder(mock_package_env):
    lineage_builder_s3 = (
        LineageBuilder()
        .object_store(prefix="text-prefix", object_key="test-object-key")
        .s3(
            access_key="test-access-key",
            secret_key="test-secret-key",
            region="test-region",
            bucket="test-bucket",
        )
        .options(
            input_handling=AssetInputHandling.UPSERT,
            fail_on_errors=True,
            case_sensitive_match=False,
            field_separator=",",
            batch_size=25,
        )
    ).to_workflow()

    request_json = loads(lineage_builder_s3.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(LINEAGE_BUILDER_S3)

    lineage_builder_gcs = (
        LineageBuilder()
        .object_store(prefix="text-prefix", object_key="test-object-key")
        .gcs(
            project_id="test-project-id",
            service_account_json="test-service-account-json",
            bucket="test-bucket",
        )
        .options(
            input_handling=AssetInputHandling.UPSERT,
            fail_on_errors=True,
            case_sensitive_match=False,
            field_separator=",",
            batch_size=25,
        )
    ).to_workflow()

    request_json = loads(lineage_builder_gcs.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(LINEAGE_BUILDER_GCS)

    lineage_builder_adls = (
        LineageBuilder()
        .object_store(prefix="text-prefix", object_key="test-object-key")
        .adls(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
            account_name="test-account-name",
            container="test-container",
        )
        .options(
            input_handling=AssetInputHandling.UPSERT,
            fail_on_errors=True,
            case_sensitive_match=False,
            field_separator=",",
            batch_size=25,
        )
    ).to_workflow()

    request_json = loads(lineage_builder_adls.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(LINEAGE_BUILDER_ADLS)


def test_lineage_generator_nt(mock_package_env):
    lineage_generator_default = (
        LineageGenerator().config(
            source_asset_type=LineageGenerator.SourceAssetType.MongoDBCollection,
            source_qualified_name="mongo/qn",
            target_asset_type=LineageGenerator.TargetAssetType.View,
            target_qualified_name="view/qn",
        )
    ).to_workflow()

    request_json = loads(
        lineage_generator_default.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(LINEAGE_GENERATOR_DEFAULT)

    lineage_generator_full = (
        LineageGenerator().config(
            source_asset_type=LineageGenerator.SourceAssetType.MongoDBCollection,
            source_qualified_name="mongo/qn",
            target_asset_type=LineageGenerator.TargetAssetType.View,
            target_qualified_name="view/qn",
            case_sensitive_match=True,
            match_on_schema=True,
            output_type=LineageGenerator.OutputType.DELETE,
            generate_on_child_assets=True,
            regex_match="t1",
            regex_replace="t2",
            regex_match_schema="t3",
            regex_replace_schema="t4",
            regex_match_schema_name="t5",
            regex_replace_schema_name="t6",
            match_prefix="t7",
            match_suffix="t8",
            file_advanced_seperator="t9",
            file_advanced_position="10",
            process_connection_qn="test/qn",
        )
    ).to_workflow()

    request_json = loads(lineage_generator_full.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(LINEAGE_GENERATOR_FULL)


def test_api_token_connection_admin(mock_package_env):
    token_connection_admin = (
        APITokenConnectionAdmin()
        .config(
            connection_qualified_name="default/snowflake/1234567890",
            api_token_guid="92588c67-5ddf-4a45-8b5c-dd92f4b84e99",
        )
        .to_workflow()
    )
    request_json = loads(token_connection_admin.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(API_TOKEN_CONNECTION_ADMIN)


@pytest.mark.parametrize(
    "test_assets",
    [
        "abc",
        123,
        {"abc": 123},
        [123],
        NonSerializable(),
        [NonSerializable()],
        {"abc": NonSerializable()},
    ],
)
def test_wrong_hierarchical_filter_raises_invalid_req_err(
    test_assets, mock_package_env, client: AtlanClient
):
    with pytest.raises(
        InvalidRequestError,
        match=INVALID_REQ_ERROR,
    ):
        SnowflakeCrawler(
            client=client,
            connection_name="test-snowflake-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        ).include(assets=test_assets)


@pytest.mark.parametrize(
    "test_projects",
    [[NonSerializable()], NonSerializable()],
)
def test_wrong_flat_filter_raises_invalid_req_err(
    test_projects, mock_package_env, client: AtlanClient
):
    with pytest.raises(
        InvalidRequestError,
        match=INVALID_REQ_ERROR,
    ):
        TableauCrawler(
            client=client,
            connection_name="test-tableau-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        ).include(projects=test_projects)


@pytest.mark.parametrize(
    "test_assets",
    [NonSerializable(), [NonSerializable()]],
)
def test_wrong_glue_package_filter_raises_invalid_req_err(
    test_assets, mock_package_env, client: AtlanClient
):
    with pytest.raises(
        InvalidRequestError,
        match=INVALID_REQ_ERROR,
    ):
        GlueCrawler(
            client=client,
            connection_name="test-glue-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        ).include(assets=test_assets)
