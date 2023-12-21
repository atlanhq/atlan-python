from typing import Optional

from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class SnowflakeCrawler(AbstractCrawler):
    _CONNECTOR_TYPE = AtlanConnectorType.SNOWFLAKE
    _PACKAGE_PREFIX = WorkflowPackage.SNOWFLAKE.value
    _PACKAGE_NAME = "@atlan/snowflake"

    def __init__(
        self,
        connection_name: str,
        admin_roles: Optional[list[Optional[str]]] = None,
        admin_groups: Optional[list[str]] = None,
        admin_users: Optional[list[str]] = None,
        allow_query: bool = True,
        allow_query_preview: bool = True,
        row_limit: int = 10000,
    ):
        self.connection_name = connection_name
        self.admin_roles = admin_roles
        self.admin_groups = admin_groups
        self.admin_users = admin_users
        self.allow_query = allow_query
        self.allow_query_preview = allow_query_preview
        self.row_limit = row_limit
        self._epoch = self.get_epoch()

    def _get_connection(self):
        return self.get_connection(
            connection_name=self.connection_name,
            connection_type=self._CONNECTOR_TYPE,
            roles=self.admin_roles,
            groups=self.admin_groups,
            users=self.admin_users,
            allow_query=self.allow_query,
            allow_query_preview=self.allow_query_preview,
        )

    def basic_auth(self, username, password, role, warehouse):
        self._credentials_body = {
            "name": f"default-snowflake-{self._epoch}-0",
            "port": 443,
            "authType": "basic",
            "username": username,
            "password": password,
            "extra": {"role": role, "warehouse": warehouse},
        }
        return self

    def keypair_auth(
        self, username, private_key, private_key_password, role, warehouse
    ):
        self._credentials_body = {
            "name": f"default-snowflake-{self._epoch}-0",
            "port": 443,
            "authType": "keypair",
            "username": username,
            "password": private_key,
            "extra": {
                "role": role,
                "warehouse": warehouse,
                "private_key_password": private_key_password,
            },
        }
        return self

    def information_schema(self, hostname):
        local_creds = {
            "host": hostname,
            "name": f"default-snowflake-{self._epoch}-0",
            "connectorConfigName": "atlan-connectors-snowflake",
        }
        parameters = {"name": "extract-strategy", "value": "information-schema"}
        self._credentials_body.update(local_creds)
        self._parameters.append(parameters)
        return self

    def account_usage(self, hostname, database_name, schema_name):
        local_creds = {
            "hostname": hostname,
            "name": f"default-snowflake-{self._epoch}-0",
            "connectorConfigName": "atlan-connectors-snowflake",
        }
        self._credentials_body.update(info_schema)
        self._parameters.append(
            {"name": "account-usage-database-name", "value": database_name}
        )
        self._parameters.append(
            {"name": "account-usage-schema-name", "value": schema_name}
        )
        return self

    def lineage(self, include=True):
        self._parameters.append({"name": "enable-lineage", "value": include})
        return self

    def tags(self, include=False):
        self._parameters.append({"name": "enable-snowflake-tag", "value": include})
        return self

    def include(self, include_assets):
        if include_assets:
            to_include = self.build_hierarchical_filter(include_assets)
            self._parameters.append(dict(name="include-filter", value=to_include))
        return self

    def exclude(self, exclude_assets):
        if to_exclude:
            to_exclude = self.build_hierarchical_filter(exclude_assets)
            self._parameters.append(dict(name="exclude-filter", value=to_exclude))
        return self

    def _get_metadata(self):
        return WorkflowMetadata(
            labels={
                "orchestration.atlan.com/certified": "true",
                "orchestration.atlan.com/source": "snowflake",
                "orchestration.atlan.com/sourceCategory": "warehouse",
                "orchestration.atlan.com/type": "connector",
                "orchestration.atlan.com/verified": "true",
                "package.argoproj.io/installer": "argopm",
                "package.argoproj.io/name": "a-t-ratlans-l-a-s-hsnowflake",
                "package.argoproj.io/registry": "httpsc-o-l-o-ns-l-a-s-hs-l-a-s-hpackages.atlan.com",
                f"orchestration.atlan.com/default-snowflake-{self._epoch}": "true",
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
                "orchestration.atlan.com/atlanName": f"{self._PACKAGE_PREFIX}-default-snowflake-{self._epoch}",
            },
            name=f"{self._PACKAGE_PREFIX}-{self._epoch}",
            namespace="default",
        )
