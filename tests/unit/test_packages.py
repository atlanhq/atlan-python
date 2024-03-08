from json import load, loads
from pathlib import Path
from unittest.mock import patch

import pytest

from pyatlan.errors import InvalidRequestError
from pyatlan.model.packages import (
    ConfluentKafkaCrawler,
    DbtCrawler,
    GlueCrawler,
    PowerBICrawler,
    SigmaCrawler,
    SnowflakeCrawler,
    SQLServerCrawler,
    TableauCrawler,
)

PACKAGE_REQUESTS_DIR = Path(__file__).parent / "data" / "package_requests"
SNOWFLAKE_BASIC = "snowflake_basic.json"
SNOWFLAKE_KEYPAIR = "snowflake_keypair.json"
GLUE_IAM_USER = "glue_iam_user.json"
TABLEAU_BASIC = "tableau_basic.json"
TABLEAU_ACCESS_TOKEN = "tableau_access_token.json"
POWERBI_DELEGATED_USER = "powerbi_delegated_user.json"
POWEBI_SERVICE_PRINCIPAL = "powerbi_service_principal.json"
CONFLUENT_KAFKA_DIRECT = "confluent_kafka_direct.json"
DBT_CORE = "dbt_core.json"
DBT_CLOUD = "dbt_cloud.json"
SIGMA_API_TOKEN = "sigma_api_token.json"
SQL_SERVER_BASIC = "sql_server_basic.json"


class NonSerializable:
    pass


INVALID_REQ_ERROR = (
    "ATLAN-PYTHON-400-014 Unable to translate "
    "the provided include/exclude asset filters into JSON"
)


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


def test_snowflake_package(
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
    mock_connection_guid,
    mock_get_epoch_timestamp,
):
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    snowflake_basic_auth = (
        SnowflakeCrawler(
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
        .exclude(assets=None)
        .lineage(True)
        .tags(True)
        .to_workflow()
    )
    request_json = loads(snowflake_basic_auth.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(SNOWFLAKE_BASIC)

    snowflake_keypair_auth = (
        SnowflakeCrawler(
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
        .exclude(assets=None)
        .lineage(True)
        .tags(False)
        .to_workflow()
    )
    request_json = loads(snowflake_keypair_auth.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(SNOWFLAKE_KEYPAIR)


def test_glue_package(
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
    mock_connection_guid,
    mock_get_epoch_timestamp,
):
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    glue_iam_user_auth = (
        GlueCrawler(
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
        .exclude(assets=None)
        .to_workflow()
    )
    request_json = loads(glue_iam_user_auth.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(GLUE_IAM_USER)


def test_tableau_package(
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
    mock_connection_guid,
    mock_get_epoch_timestamp,
):
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    tableau_basic_auth = (
        TableauCrawler(
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
        .exclude(projects=None)
        .crawl_unpublished(True)
        .crawl_hidden_fields(False)
        .to_workflow()
    )
    request_json = loads(tableau_basic_auth.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(TABLEAU_BASIC)

    tableau_access_token_auth = (
        TableauCrawler(
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
        .exclude(projects=None)
        .crawl_unpublished(True)
        .crawl_hidden_fields(False)
        .to_workflow()
    )
    request_json = loads(
        tableau_access_token_auth.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(TABLEAU_ACCESS_TOKEN)


def test_powerbi_package(
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
    mock_connection_guid,
    mock_get_epoch_timestamp,
):
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    powerbi_delegated_user = (
        PowerBICrawler(
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
        .exclude(workspaces=None)
        .to_workflow()
    )
    request_json = loads(powerbi_delegated_user.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(POWERBI_DELEGATED_USER)

    powerbi_service_principal = (
        PowerBICrawler(
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
        .exclude(workspaces=None)
        .to_workflow()
    )
    request_json = loads(
        powerbi_service_principal.json(by_alias=True, exclude_none=True)
    )
    assert request_json == load_json(POWEBI_SERVICE_PRINCIPAL)


def test_confluent_kafka_package(
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
    mock_connection_guid,
    mock_get_epoch_timestamp,
):
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    conf_kafka_direct = (
        ConfluentKafkaCrawler(
            connection_name="test-conf-kafka-direct-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        )
        .direct(bootstrap="test-bootstrap-server:9092", encrypted=True)
        .api_token(api_key="test-api-key", api_secret="test-api-secret")
        .skip_internal(False)
        .include(regex=".*_TEST")
        .exclude(regex=None)
        .to_workflow()
    )
    request_json = loads(conf_kafka_direct.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(CONFLUENT_KAFKA_DIRECT)


def test_dbt_package(
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
    mock_connection_guid,
    mock_get_epoch_timestamp,
):
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    dbt_core = (
        DbtCrawler(
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
        .exclude(filter=None)
        .tags(True)
        .enrich_materialized_assets(False)
        .to_workflow()
    )
    request_json = loads(dbt_cloud.json(by_alias=True, exclude_none=True))
    assert request_json == load_json(DBT_CLOUD)


def test_sigma_package(
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
    mock_connection_guid,
    mock_get_epoch_timestamp,
):
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    sigma_api_token = (
        SigmaCrawler(
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


def test_sql_server_package(
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
    mock_connection_guid,
    mock_get_epoch_timestamp,
):
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    sql_server_basic = (
        SQLServerCrawler(
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
    test_assets,
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
    mock_get_epoch_timestamp,
):
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    with pytest.raises(
        InvalidRequestError,
        match=INVALID_REQ_ERROR,
    ):
        SnowflakeCrawler(
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
    test_projects,
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
    mock_get_epoch_timestamp,
):
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    with pytest.raises(
        InvalidRequestError,
        match=INVALID_REQ_ERROR,
    ):
        TableauCrawler(
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
    test_assets,
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
    mock_get_epoch_timestamp,
):
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    with pytest.raises(
        InvalidRequestError,
        match=INVALID_REQ_ERROR,
    ):
        GlueCrawler(
            connection_name="test-glue-conn",
            admin_roles=["admin-guid-1234"],
            admin_groups=None,
            admin_users=None,
        ).include(assets=test_assets)
