from __future__ import annotations

from typing import List, Optional

from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.base.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class DbtCrawler(AbstractCrawler):
    """
    Base configuration for a new Dbt crawler.

    :param connection_name: name for the connection
    :param admin_roles: admin roles for the connection
    :param admin_groups: admin groups for the connection
    :param admin_users: admin users for the connection
    :param allow_query: allow data to be queried in the
    connection (True) or not (False), default: False
    :param allow_query_preview: allow sample data viewing for
    assets in the connection (True) or not (False), default: False
    :param row_limit: maximum number of rows
    that can be returned by a query, default: 0
    """

    _NAME = "dbt"
    _PACKAGE_NAME = "@atlan/dbt"
    _PACKAGE_PREFIX = WorkflowPackage.DBT.value
    _CONNECTOR_TYPE = AtlanConnectorType.DBT
    _PACKAGE_ICON = "https://assets.atlan.com/assets/dbt-new.svg"
    _PACKAGE_LOGO = "https://assets.atlan.com/assets/dbt-new.svg"

    def __init__(
        self,
        connection_name: str,
        admin_roles: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
        admin_users: Optional[List[str]] = None,
        allow_query: bool = False,
        allow_query_preview: bool = False,
        row_limit: int = 0,
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

    def cloud(
        self,
        service_token: str,
        hostname: str = "https://cloud.getdbt.com",
        multi_tenant: bool = True,
    ) -> DbtCrawler:
        """
        Set up the crawler to extract using dbt Cloud.

        :param service_token: token to use to authenticate against dbt
        :param hostname: of dbt, default: https://cloud.getdbt.com
        :param multi_tenant: if True, use a multi-tenant
        cloud config, otherwise a single-tenant cloud config
        :returns: crawler, set up to extract using dbt Cloud
        """
        local_creds = {
            "name": f"default-{self._NAME}-{self._epoch}-1",
            "host": hostname,
            "port": 443,
            "auth_type": "token",
            "username": "",
            "password": service_token,
            "connector_config_name": f"atlan-connectors-{self._NAME}",
        }
        self._credentials_body.update(local_creds)
        self._parameters.append(dict(name="extraction-method", value="api"))
        self._parameters.append(
            dict(name="deployment-type", value="multi" if multi_tenant else "single")
        )
        self._parameters.append(
            {"name": "api-credential-guid", "value": "{{credentialGuid}}"}
        )
        self._parameters.append(dict(name="control-config-strategy", value="default"))
        return self

    def core(self, s3_bucket: str, s3_prefix: str, s3_region: str) -> DbtCrawler:
        """
        Set up the crawler to extract using dbt Core files in S3.

        :param s3_bucket: S3 bucket containing the dbt Core files
        :param s3_prefix: prefix within the S3 bucket where the dbt Core files are located
        :param s3_region: S3 region where the bucket is located
        :returns: crawler, set up to extract using dbt Core files in S3
        """
        self._parameters.append(dict(name="extraction-method", value="core"))
        self._parameters.append(dict(name="deployment-type", value="single"))
        self._parameters.append(dict(name="core-extraction-s3-bucket", value=s3_bucket))
        self._parameters.append(dict(name="core-extraction-s3-prefix", value=s3_prefix))
        self._parameters.append(dict(name="core-extraction-s3-region", value=s3_region))
        return self

    def enrich_materialized_assets(self, enabled: bool = False) -> DbtCrawler:
        """
        Whether to enable the enrichment of
        materialized SQL assets as part of crawling dbt.

        :param enabled: if True, any assets that dbt materializes
        will also be enriched with details from dbt, default: False
        :returns: crawler, set up to include
        or exclude enrichment of materialized assets
        """
        self._parameters.append(
            {
                "name": "enrich-materialised-sql-assets",
                "value": "true" if enabled else "false",
            }
        )
        return self

    def tags(self, include: bool = False) -> DbtCrawler:
        """
        Whether to enable dbt tag syncing as part of crawling dbt.

        :param include: if True, tags in dbt will
        be included while crawling dbt, default: False
        :returns: crawler, set to include or exclude dbt tags
        """
        self._parameters.append(
            {
                "name": "enable-dbt-tagsync",
                "value": "true" if include else "false",
            }
        )
        return self

    def limit_to_connection(self, connection_qualified_name: str) -> DbtCrawler:
        """
        Limit the crawling to a single connection's assets.
        If not specified, crawling will be
        attempted across all connection's assets.

        :param connection_qualified_name: unique name
        of the connection for whose assets to limit crawling
        :returns: crawler, set to limit crawling
        to only those assets in the specified connection
        """
        self._parameters.append(
            {
                "name": "connection-qualified-name",
                "value": connection_qualified_name,
            }
        )
        return self

    def include(self, filter: str = "") -> DbtCrawler:
        """
        Defines the filter for assets to include when crawling.

        :param filter: for dbt Core provide a wildcard
        expression and for dbt Cloud provide a string-encoded map
        :returns: crawler, set to include only those assets specified
        """
        self._parameters.append(
            dict(name="include-filter", value=filter if filter else "{}")
        )
        self._parameters.append(
            dict(name="include-filter-core", value=filter if filter else "*")
        )
        return self

    def exclude(self, filter: str = "") -> DbtCrawler:
        """
        Defines the filter for assets to exclude when crawling.

        :param filter: for dbt Core provide a wildcard
        expression and for dbt Cloud provide a string-encoded map
        :return: the builder, set to exclude only those assets specified
        """
        self._parameters.append(
            dict(name="exclude-filter", value=filter if filter else "{}")
        )
        self._parameters.append(
            dict(name="exclude-filter-core", value=filter if filter else "*")
        )
        return self

    def _set_required_metadata_params(self):
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
                "orchestration.atlan.com/sourceCategory": "elt",
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
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/6335824578705",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,  # noqa
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": f"{self._NAME} Assets",
                "orchestration.atlan.com/usecase": "crawling",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": f"Package to crawl {self._NAME} assets and publish to Atlan for discovery.",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": "[\"connector\",\"crawler\",\"dbt\"]",  # fmt: skip
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "git+https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"{self._PACKAGE_PREFIX}-default-{self._NAME}-{self._epoch}",
            },
            name=f"{self._PACKAGE_PREFIX}-{self._epoch}",
            namespace="default",
        )
