from typing import Optional

from pyatlan.model.assets import Connection
from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class SnowflakeCrawler(AbstractCrawler):
    _NAME = "snowflake"
    _PACKAGE_NAME = "@atlan/snowflake"
    _PACKAGE_PREFIX = WorkflowPackage.SNOWFLAKE.value
    _CONNECTOR_TYPE = AtlanConnectorType.SNOWFLAKE
    _PACKAGE_ICON = "https://docs.snowflake.com/en/_images/logo-snowflake-sans-text.png"
    _PACKAGE_LOGO = "https://1amiydhcmj36tz3733v94f15-wpengine.netdna-ssl.com/wp-content/themes/snowflake/assets/img/logo-blue.svg"  # noqa

    def __init__(
        self,
        connection_name: str,
        admin_roles: Optional[list[str]],
        admin_groups: Optional[list[str]],
        admin_users: Optional[list[str]],
        allow_query: bool = True,
        allow_query_preview: bool = True,
        row_limit: int = 10000,
    ):
        self._epoch = self.get_epoch()
        self.connection_name = connection_name
        self.admin_roles = admin_roles
        self.admin_groups = admin_groups
        self.admin_users = admin_users
        self.allow_query = allow_query
        self.allow_query_preview = allow_query_preview
        self.row_limit = row_limit

    def _get_connection(self) -> Connection:
        return self.get_connection(
            connection_name=self.connection_name,
            connection_type=self._CONNECTOR_TYPE,
            roles=self.admin_roles,
            groups=self.admin_groups,
            users=self.admin_users,
            allow_query=self.allow_query,
            allow_query_preview=self.allow_query_preview,
            row_limit=self.row_limit,
            source_logo=self._PACKAGE_LOGO,
        )

    def basic_auth(
        self, username: str, password: str, role: str, warehouse: str
    ) -> "SnowflakeCrawler":
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
        self,
        username: str,
        private_key: str,
        private_key_password: str,
        role: str,
        warehouse: str,
    ) -> "SnowflakeCrawler":
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

    def information_schema(self, hostname: str) -> "SnowflakeCrawler":
        local_creds = {
            "host": hostname,
            "name": f"default-snowflake-{self._epoch}-0",
            "connectorConfigName": "atlan-connectors-snowflake",
        }
        parameters = {"name": "extract-strategy", "value": "information-schema"}
        self._credentials_body.update(local_creds)
        self._parameters.append(parameters)
        return self

    def account_usage(
        self, hostname: str, database_name: str, schema_name: str
    ) -> "SnowflakeCrawler":
        local_creds = {
            "hostname": hostname,
            "name": f"default-snowflake-{self._epoch}-0",
            "connectorConfigName": "atlan-connectors-snowflake",
        }
        self._credentials_body.update(local_creds)
        self._parameters.append(
            {"name": "account-usage-database-name", "value": database_name}
        )
        self._parameters.append(
            {"name": "account-usage-schema-name", "value": schema_name}
        )
        return self

    def lineage(self, include: bool = True) -> "SnowflakeCrawler":
        self._parameters.append(
            {"name": "enable-lineage", "value": "true" if include else "false"}
        )
        return self

    def tags(self, include: bool = False) -> "SnowflakeCrawler":
        self._parameters.append(
            {"name": "enable-snowflake-tag", "value": "true" if include else "false"}
        )
        return self

    def include(self, include_assets: dict) -> "SnowflakeCrawler":
        include_assets = include_assets or {}
        to_include = self.build_hierarchical_filter(include_assets)
        if to_include:
            self._parameters.append(dict(name="include-filter", value=to_include))
        return self

    def exclude(self, exclude_assets: dict) -> "SnowflakeCrawler":
        exclude_assets = exclude_assets or {}
        to_exclude = self.build_hierarchical_filter(exclude_assets)
        if to_exclude:
            self._parameters.append(dict(name="exclude-filter", value=to_exclude))
        return self

    def _get_metadata(self) -> WorkflowMetadata:
        return WorkflowMetadata(
            labels={
                "orchestration.atlan.com/certified": "true",
                "orchestration.atlan.com/source": self._NAME,
                "orchestration.atlan.com/sourceCategory": "warehouse",
                "orchestration.atlan.com/type": "connector",
                "orchestration.atlan.com/verified": "true",
                "package.argoproj.io/installer": "argopm",
                "package.argoproj.io/name": f"a-t-ratlans-l-a-s-h{self._NAME}",
                "package.argoproj.io/registry": "httpsc-o-l-o-ns-l-a-s-hs-l-a-s-hpackages.atlan.com",
                f"orchestration.atlan.com/default-{self._NAME}-{self._epoch}": "true",
                "orchestration.atlan.com/atlan-ui": "true",
            },
            annotations={
                "orchestration.atlan.com/allowSchedule": "true",
                "orchestration.atlan.com/categories": "warehouse,crawler",
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/6037440864145",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_LOGO,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": f"{self._NAME.capitalize()} Assets",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": f"Package to crawl {self._NAME.capitalize()} assets and publish to Atlan for discovery",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": "[\"snowflake\",\"warehouse\",\"connector\",\"crawler\"]",  # fmt: skip
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "git+https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"{self._PACKAGE_PREFIX}-default-{self._NAME}-{self._epoch}",
            },
            name=f"{self._PACKAGE_PREFIX}-{self._epoch}",
            namespace="default",
        )
