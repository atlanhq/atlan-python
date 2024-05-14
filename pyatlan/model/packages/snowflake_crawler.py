from __future__ import annotations

from typing import List, Optional

from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.base.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class SnowflakeCrawler(AbstractCrawler):
    """
    Base configuration for a new Snowflake crawler.

    :param connection_name: name for the connection
    :param admin_roles: admin roles for the connection
    :param admin_groups: admin groups for the connection
    :param admin_users: admin users for the connection
    :param allow_query: allow data to be queried in the
    connection (True) or not (False), default: True
    :param allow_query_preview: allow sample data viewing for
    assets in the connection (True) or not (False), default: True
    :param row_limit: maximum number of rows
    that can be returned by a query, default: 10000
    """

    _NAME = "snowflake"
    _PACKAGE_NAME = "@atlan/snowflake"
    _PACKAGE_PREFIX = WorkflowPackage.SNOWFLAKE.value
    _CONNECTOR_TYPE = AtlanConnectorType.SNOWFLAKE
    _PACKAGE_ICON = "https://docs.snowflake.com/en/_images/logo-snowflake-sans-text.png"
    _PACKAGE_LOGO = "https://1amiydhcmj36tz3733v94f15-wpengine.netdna-ssl.com/wp-content/themes/snowflake/assets/img/logo-blue.svg"  # noqa

    def __init__(
        self,
        connection_name: str,
        admin_roles: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
        admin_users: Optional[List[str]] = None,
        allow_query: bool = True,
        allow_query_preview: bool = True,
        row_limit: int = 10000,
    ):
        super().__init__(
            connection_name=connection_name,
            connection_type=self._CONNECTOR_TYPE,
            admin_roles=admin_roles,
            admin_groups=admin_groups,
            admin_users=admin_users,
            allow_query=allow_query,
            allow_query_preview=allow_query_preview,
            row_limit=row_limit,
            source_logo=self._PACKAGE_LOGO,
        )

    def basic_auth(
        self, username: str, password: str, role: str, warehouse: str
    ) -> SnowflakeCrawler:
        """
        Set up the crawler to use basic authentication.

        :param username: through which to access Snowflake
        :param password: through which to access Snowflake
        :param role: name of the role within Snowflake to crawl through
        :param warehouse: name of the warehouse within Snowflake to crawl through
        :returns: crawler, set up to use basic authentication
        """
        local_creds = {
            "name": f"default-snowflake-{self._epoch}-0",
            "port": 443,
            "auth_type": "basic",
            "username": username,
            "password": password,
            "extras": {"role": role, "warehouse": warehouse},
        }
        self._credentials_body.update(local_creds)
        return self

    def keypair_auth(
        self,
        username: str,
        private_key: str,
        private_key_password: str,
        role: str,
        warehouse: str,
    ) -> SnowflakeCrawler:
        """
        Set up the crawler to use keypair-based authentication.

        :param username: through which to access Snowflake
        :param private_key: encrypted private key for authenticating with Snowflake
        :param private_key_password: password for the encrypted private key
        :param role: name of the role within Snowflake to crawl through
        :param warehouse: name of the warehouse within Snowflake to crawl through
        :returns: crawler, set up to use keypair-based authentication
        """
        local_creds = {
            "name": f"default-snowflake-{self._epoch}-0",
            "port": 443,
            "auth_type": "keypair",
            "username": username,
            "password": private_key,
            "extras": {
                "role": role,
                "warehouse": warehouse,
                "private_key_password": private_key_password,
            },
        }
        self._credentials_body.update(local_creds)
        return self

    def information_schema(self, hostname: str) -> SnowflakeCrawler:
        """
        Set the crawler to extract using Snowflake's information schema.

        :param hostname: hostname of the Snowflake instance
        :returns: crawler, set to extract using information schema
        """
        local_creds = {
            "host": hostname,
            "name": f"default-snowflake-{self._epoch}-0",
            "connector_config_name": "atlan-connectors-snowflake",
        }
        parameters = {"name": "extract-strategy", "value": "information-schema"}
        self._credentials_body.update(local_creds)
        self._parameters.append(parameters)
        return self

    def account_usage(
        self, hostname: str, database_name: str, schema_name: str
    ) -> SnowflakeCrawler:
        """
        Set the crawler to extract using Snowflake's account usage database and schema.

        :param hostname: hostname of the Snowflake instance
        :param database_name: name of the database to use
        :param schema_name: name of the schema to use
        :returns: crawler, set to extract using account usage
        """
        local_creds = {
            "host": hostname,
            "name": f"default-snowflake-{self._epoch}-0",
            "connector_config_name": "atlan-connectors-snowflake",
        }
        self._credentials_body.update(local_creds)
        self._parameters.append(
            {"name": "account-usage-database-name", "value": database_name}
        )
        self._parameters.append(
            {"name": "account-usage-schema-name", "value": schema_name}
        )
        return self

    def lineage(self, include: bool = True) -> SnowflakeCrawler:
        """
        Whether to enable lineage as part of crawling Snowflake.

        :param include: if True, lineage will be included while crawling Snowflake, default: True
        :returns: crawler, set to include or exclude lineage
        """
        self._parameters.append(
            {"name": "enable-lineage", "value": "true" if include else "false"}
        )
        return self

    def tags(self, include: bool = False) -> SnowflakeCrawler:
        """
        Whether to enable Snowflake tag syncing as part of crawling Snowflake.

        :param include: Whether true, tags in Snowflake will be included while crawling Snowflake
        :returns: crawler, set to include or exclude Snowflake tags
        """
        self._parameters.append(
            {"name": "enable-snowflake-tag", "value": "true" if include else "false"}
        )
        return self

    def include(self, assets: dict) -> SnowflakeCrawler:
        """
        Defines the filter for assets to include when crawling.

        :param assets: Map keyed by database name with each value being a list of schemas
        :returns: crawler, set to include only those assets specified
        :raises InvalidRequestException: In the unlikely
        event the provided filter cannot be translated
        """
        include_assets = assets or {}
        to_include = self.build_hierarchical_filter(include_assets)
        self._parameters.append(
            dict(dict(name="include-filter", value=to_include or "{}"))
        )
        return self

    def exclude(self, assets: dict) -> SnowflakeCrawler:
        """
        Defines the filter for assets to exclude when crawling.

        :param assets: Map keyed by database name with each value being a list of schemas
        :returns: crawler, set to exclude only those assets specified
        :raises InvalidRequestException: In the unlikely
        event the provided filter cannot be translated
        """
        exclude_assets = assets or {}
        to_exclude = self.build_hierarchical_filter(exclude_assets)
        self._parameters.append(dict(name="exclude-filter", value=to_exclude or "{}"))
        return self

    def _set_required_metadata_params(self):
        self._parameters.append(
            {"name": "credential-guid", "value": "{{credentialGuid}}"}
        )
        self._parameters.append(dict(name="control-config-strategy", value="default"))
        self._parameters.append(
            {
                "name": "connection",
                "value": self._get_connection().json(
                    by_alias=True, exclude_unset=True, exclude_none=True
                ),
            }
        )

    def _get_metadata(self) -> WorkflowMetadata:
        self._set_required_metadata_params()
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
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
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
