from __future__ import annotations

from typing import List, Optional

from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.base.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class OracleCrawler(AbstractCrawler):
    """
    Base configuration for a new Oracle crawler.

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

    _NAME = "oracle"
    _PACKAGE_NAME = "@atlan/oracle"
    _PACKAGE_PREFIX = WorkflowPackage.ORACLE.value
    _CONNECTOR_TYPE = AtlanConnectorType.ORACLE
    _PACKAGE_ICON = (
        "https://docs.oracle.com/sp_common/book-template/ohc-common/img/favicon.ico"
    )
    _PACKAGE_LOGO = (
        "https://docs.oracle.com/sp_common/book-template/ohc-common/img/favicon.ico"
    )

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
        self._advanced_config = False
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

    def direct(
        self,
        hostname: str,
        port: int = 1521,
    ) -> OracleCrawler:
        """
        Set up the crawler to extract directly from Oracle.

        :param hostname: hostname of the Oracle instance
        :param port: port number of Oracle instance, defaults to `1521`
        :returns: crawler, set up to extract directly from Oracle.
        """
        local_creds = {
            "name": f"default-{self._NAME}-{self._epoch}-0",
            "host": hostname,
            "port": port,
            "connector_config_name": f"atlan-connectors-{self._NAME}",
        }
        self._credentials_body.update(local_creds)
        self._parameters.append(dict(name="extraction-method", value="direct"))
        return self

    def basic_auth(
        self,
        username: str,
        password: str,
        sid: str,
        database_name: str,
    ) -> OracleCrawler:
        """
        Set up the crawler to use basic authentication.

        :param username: through which to access Oracle
        :param password: through which to access Oracle
        :param sid: SID (system identifier) of the Oracle instance
        :param database: database name to crawl
        :returns: crawler, set up to use basic authentication
        """
        local_creds = {
            "name": f"default-{self._NAME}-{self._epoch}-0",
            "auth_type": "basic",
            "username": username,
            "password": password,
            "extra": {"sid": sid, "databaseName": database_name},
        }
        self._credentials_body.update(local_creds)
        return self

    def include(self, assets: dict) -> OracleCrawler:
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

    def exclude(self, assets: dict) -> OracleCrawler:
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

    def exclude_regex(self, regex: str) -> OracleCrawler:
        """
        Defines the exclude regex for crawler ignore
        tables and views based on a naming convention.

        :param regex: exclude regex for the crawler
        :returns: crawler, set to exclude
        only those assets specified in the regex
        """
        self._parameters.append(dict(name="temp-table-regex", value=regex))
        return self

    def jdbc_internal_methods(self, enable: bool) -> OracleCrawler:
        """
        Defines whether to enable or disable JDBC
        internal methods for data extraction.

        :param enable: whether to whether to enable (`True`) or
        disable (`False`) JDBC internal methods for data extraction
        :returns: crawler, with jdbc internal methods for data extraction
        """
        self._advanced_config = True
        self._parameters.append(
            dict(name="use-jdbc-internal-methods", value="true" if enable else "false")
        )
        return self

    def source_level_filtering(self, enable: bool) -> OracleCrawler:
        """
        Defines whether to enable or disable schema level filtering on source.
        schemas selected in the include filter will be fetched.

        :param enable: whether to enable (`True`) or
        disable (`False`) schema level filtering on source
        :returns: crawler, with schema level filtering on source
        """
        self._advanced_config = True
        self._parameters.append(
            dict(
                name="use-source-schema-filtering", value="true" if enable else "false"
            )
        )
        return self

    def _set_required_metadata_params(self):
        self._parameters.append(
            {"name": "credentials-fetch-strategy", "value": "credential_guid"}
        )
        self._parameters.append(
            {"name": "credential-guid", "value": "{{credentialGuid}}"}
        )
        self._parameters.append(dict(name="publish-mode", value="production"))
        self._parameters.append(dict(name="atlas-auth-type", value="internal"))
        self._parameters.append(
            dict(
                name="advanced-config-strategy",
                value="custom" if self._advanced_config else "default",
            )
        )
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
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/6849958872861",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": "Oracle Assets",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": "Package to crawl Oracle assets and publish to Atlan for discovery",
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": "[\"oracle\",\"warehouse\",\"connector\",\"crawler\"]",  # fmt: skip
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "git+https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"{self._PACKAGE_PREFIX}-default-{self._NAME}-{self._epoch}",
            },
            name=f"{self._PACKAGE_PREFIX}-{self._epoch}",
            namespace="default",
        )
