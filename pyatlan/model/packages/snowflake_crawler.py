from typing import Dict, Optional

from pyatlan.cache.role_cache import RoleCache
from pyatlan.model.assets import Connection
from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.crawler import AbstractCrawler
from pyatlan.model.workflow import (
    PackageParameter,
    Workflow,
    WorkflowDAG,
    WorkflowMetadata,
    WorkflowParameters,
    WorkflowSpec,
    WorkflowTask,
    WorkflowTemplate,
    WorkflowTemplateRef,
)


class SnowflakeCrawler(AbstractCrawler):
    PREFIX = WorkflowPackage.SNOWFLAKE.value

    @classmethod
    def info_schema_basic_auth(
        cls,
        connection_name: str,
        hostname: str,
        username: str,
        password: str,
        role: str,
        warehouse: str,
        port: int = 443,
        admin_roles: Optional[list[Optional[str]]] = None,
        admin_groups: Optional[list[str]] = None,
        admin_users: Optional[list[str]] = None,
        allow_query: bool = True,
        allow_query_preview: bool = True,
        row_limit: int = 10000,
        include_assets: Optional[Dict[str, list[str]]] = None,
        exclude_assets: Optional[Dict[str, list[str]]] = None,
    ) -> Workflow:
        if not admin_roles:
            admin_roles = [RoleCache.get_id_for_name("$admin")]

        connection = Connection.create(
            name=connection_name,
            connector_type=AtlanConnectorType.SNOWFLAKE,
            admin_roles=admin_roles,
            admin_groups=admin_groups,
            admin_users=admin_users,
        )
        connection.allow_query = allow_query
        connection.allow_query_preview = allow_query_preview
        connection.row_limit = row_limit
        connection.default_credential_guid = "{{credentialGuid}}"
        connection.source_logo = (
            "https://docs.snowflake.com/en/_images/logo-snowflake-sans-text.png"
        )
        connection.is_discoverable = True
        connection.is_editable = False
        epoch = connection.qualified_name.split("/")[-1]
        credential_body = {
            "name": f"default-snowflake-{epoch}-0",
            "host": hostname,
            "port": port,
            "authType": "basic",
            "username": username,
            "password": password,
            "extra": {"role": role, "warehouse": warehouse},
            "connectorConfigName": "atlan-connectors-snowflake",
        }
        parameters = [
            {"name": "credential-guid", "value": "{{credentialGuid}}"},
            {"name": "extract-strategy", "value": "information-schema"},
            {"name": "account-usage-database-name", "value": "SNOWFLAKE"},
            {"name": "account-usage-schema-name", "value": "ACCOUNT_USAGE"},
            {"name": "control-config-strategy", "value": "default"},
            {"name": "enable-lineage", "value": True},
            {"name": "enable-snowflake-tags", "value": False},
            {
                "name": "connection",
                "value": connection.json(
                    by_alias=True, exclude_unset=True, exclude_none=True
                ),
            },
        ]
        to_include = cls.build_hierarchical_filter(include_assets)
        to_exclude = cls.build_hierarchical_filter(exclude_assets)

        if to_include:
            parameters.append(dict(name="include-filter", value=to_include))
        if to_exclude:
            parameters.append(dict(name="exclude-filter", value=to_exclude))

        workflow_parameters = WorkflowParameters(parameters=parameters)
        atlan_name = f"{SnowflakeCrawler.PREFIX}-default-snowflake-{epoch}"
        run_name = f"{SnowflakeCrawler.PREFIX}-{epoch}"

        workflow_metadata = WorkflowMetadata(
            labels={
                "orchestration.atlan.com/certified": "true",
                "orchestration.atlan.com/source": "snowflake",
                "orchestration.atlan.com/sourceCategory": "warehouse",
                "orchestration.atlan.com/type": "connector",
                "orchestration.atlan.com/verified": "true",
                "package.argoproj.io/installer": "argopm",
                "package.argoproj.io/name": "a-t-ratlans-l-a-s-hsnowflake",
                "package.argoproj.io/registry": "httpsc-o-l-o-ns-l-a-s-hs-l-a-s-hpackages.atlan.com",
                f"orchestration.atlan.com/default-snowflake-{epoch}": "true",
                "orchestration.atlan.com/atlan-ui": "true",
            },
            annotations={
                "orchestration.atlan.com/allowSchedule": "true",
                "orchestration.atlan.com/categories": "warehouse,crawler",
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/6037440864145",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": "https://docs.snowflake.com/en/_images/logo-snowflake-sans-text.png",
                "orchestration.atlan.com/logo": "https://1amiydhcmj36tz3733v94f15-wpengine.netdna-ssl.com/wp-content/themes/snowflake/assets/img/logo-blue.svg",  # noqa
                "orchestration.atlan.com/marketplaceLink": "https://packages.atlan.com/-/web/detail/@atlan/snowflake",
                "orchestration.atlan.com/name": "Snowflake Assets",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": "Package to crawl snowflake assets and publish to Atlan for discovery",  # noqa
                "package.argoproj.io/homepage": "https://packages.atlan.com/-/web/detail/@atlan/snowflake",
                "package.argoproj.io/keywords": '["snowflake","warehouse","connector","crawler"]',
                "package.argoproj.io/name": "@atlan/snowflake",
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "git+https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": atlan_name,
            },
            name=run_name,
            namespace="default",
        )
        workflow_spec = WorkflowSpec(
            entrypoint="main",
            templates=[
                WorkflowTemplate(
                    name="main",
                    dag=WorkflowDAG(
                        tasks=[
                            WorkflowTask(
                                name="run",
                                arguments=workflow_parameters,
                                template_ref=WorkflowTemplateRef(
                                    name=cls.PREFIX,
                                    template="main",
                                    cluster_scope=True,
                                ),
                            )
                        ]
                    ),
                )
            ],
            workflow_metadata=WorkflowMetadata(
                annotations={"package.argoproj.io/name": "@atlan/snowflake"}
            ),
        )
        payload = [
            PackageParameter(
                parameter="credentialGuid", type="credential", body=credential_body
            )
        ]
        return Workflow(
            metadata=workflow_metadata,
            spec=workflow_spec,
            payload=payload,
        )
