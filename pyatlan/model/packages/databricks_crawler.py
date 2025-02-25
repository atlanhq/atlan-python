from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.base.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class DatabricksCrawler(AbstractCrawler):
    """
    Base configuration for a new Databricks crawler.

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

    _NAME = "databricks"
    _PACKAGE_NAME = "@atlan/databricks"
    _PACKAGE_PREFIX = WorkflowPackage.DATABRICKS.value
    _CONNECTOR_TYPE = AtlanConnectorType.DATABRICKS
    _PACKAGE_ICON = "https://assets.atlan.com/assets/databricks.svg"
    _PACKAGE_LOGO = "https://assets.atlan.com/assets/databricks.svg"

    class ExtractionMethod(str, Enum):
        JDBC = "jdbc"
        REST = "rest"

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

    def direct(self, hostname: str, port: int = 443) -> DatabricksCrawler:
        """
        Set up the crawler to extract directly from the Databricks.

        :param hostname: hostname of the Databricks instance
        :param port: port number of the Databricks instance. default: `443`
        :returns: crawler, set up to extract directly from the Databricks
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

    def s3(
        self,
        bucket_name: str,
        bucket_prefix: str,
        bucket_region: Optional[str] = None,
    ) -> DatabricksCrawler:
        """
        Set up the crawler to extract from S3 bucket.

        :param bucket_name: name of the bucket/storage
        that contains the extracted metadata files
        :param bucket_prefix: prefix is everything after the
        bucket/storage name, including the `path`
        :param bucket_region: (Optional) name of the region if applicable
        :returns: crawler, set up to extract from S3 bucket
        """
        self._parameters.append(dict(name="extraction-method", value="s3"))
        self._parameters.append(
            dict(name="offline-extraction-bucket", value=bucket_name)
        )
        self._parameters.append(
            dict(name="offline-extraction-prefix", value=bucket_prefix)
        )
        self._parameters.append(
            dict(name="offline-extraction-region", value=bucket_region)
        )
        return self

    def basic_auth(
        self, personal_access_token: str, http_path: str
    ) -> DatabricksCrawler:
        """
        Set up the crawler to use basic authentication.

        :param personal_access_token: through which to access Databricks instance
        :param http_path: HTTP path of your Databricks instance
        :returns: crawler, set up to use basic authentication
        """
        local_creds = {
            "authType": "basic",
            "username": "",
            "password": personal_access_token,
            "connector_type": "dual",
            "extra": {
                "__http_path": http_path,
            },
        }
        self._credentials_body.update(local_creds)
        return self

    def aws_service(self, client_id: str, client_secret: str) -> DatabricksCrawler:
        """
        Set up the crawler to use AWS service principal.

        :param client_id: client ID for your AWS service principal
        :param client_secret: client secret for your AWS service principal
        :returns: crawler, set up to use AWS service principal
        """
        local_creds = {
            "authType": "aws_service",
            "username": "",
            "connector_type": "rest",
            "extra": {"client_id": client_id, "client_secret": client_secret},
        }
        self._credentials_body.update(local_creds)
        return self

    def azure_service(
        self, client_id: str, client_secret: str, tenant_id: str
    ) -> DatabricksCrawler:
        """
        Set up the crawler to use Azure service principal.

        :param client_id: client ID for Azure service principal
        :param client_secret: client secret for your Azure service principal
        :param tenant_id: tenant ID (directory ID) for Azure service principal
        :returns: crawler, set up to use Azure service principal
        """
        local_creds = {
            "authType": "azure_service",
            "username": "",
            "connector_type": "rest",
            "extra": {
                "client_id": client_id,
                "client_secret": client_secret,
                "tenant_id": tenant_id,
            },
        }
        self._credentials_body.update(local_creds)
        return self

    def metadata_extraction_method(
        self,
        type: DatabricksCrawler.ExtractionMethod = ExtractionMethod.JDBC,
    ) -> DatabricksCrawler:
        """
        Determines the interface that the package
        will use to extract metadata from Databricks.
        JDBC is the recommended method (`default`).
        REST API method is supported only
        by Unity Catalog enabled instances.

        :param type: extraction method to use.
        Defaults to `DatabricksCrawler.ExtractionMethod.JDBC`
        """
        self._parameters.append({"name": "extract-strategy", "value": type.value})
        return self

    def enable_view_lineage(self, include: bool = True) -> DatabricksCrawler:
        """
        Whether to enable view lineage as part of crawling Databricks.

        :param include: if True, view lineage will be included while crawling Databricks, default: True
        :returns: crawler, set to include or exclude view lineage
        """
        self._parameters.append({"name": "enable-view-lineage", "value": include})
        return self

    def enable_source_level_filtering(self, include: bool = False) -> DatabricksCrawler:
        """
        Whether to enable or disable schema level filtering on source.
        schemas selected in the include filter will be fetched.

        :param include: if True, schemas selected in the include
        filter will be fetched while crawling Databricks, default: False
        :returns: crawler, set to include or exclude source level filtering
        """
        self._parameters.append(
            {
                "name": "use-source-schema-filtering",
                "value": "true" if include else "false",
            }
        )
        self._advanced_config = True
        return self

    def include(self, assets: dict) -> DatabricksCrawler:
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

    def exclude(self, assets: dict) -> DatabricksCrawler:
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

    def include_for_rest_api(self, assets: List[str]) -> DatabricksCrawler:
        """
        Defines the filter for assets to include when crawling
        (When using REST API extraction method).

        :param assets: list of databases names to include when crawling
        :returns: crawler, set to include only those assets specified
        :raises InvalidRequestException: In the unlikely
        event the provided filter cannot be translated
        """
        include_assets = assets or []
        to_include = self.build_flat_hierarchical_filter(include_assets)
        self._parameters.append(
            dict(dict(name="include-filter-rest", value=to_include or "{}"))
        )
        return self

    def exclude_for_rest_api(self, assets: List[str]) -> DatabricksCrawler:
        """
        Defines the filter for assets to exclude when crawling.
        (When using REST API extraction method).

        :param assets: list of databases names to exclude when crawling
        :returns: crawler, set to exclude only those assets specified
        :raises InvalidRequestException: In the unlikely
        event the provided filter cannot be translated
        """
        exclude_assets = assets or []
        to_exclude = self.build_flat_hierarchical_filter(exclude_assets)
        self._parameters.append(
            dict(name="exclude-filter-rest", value=to_exclude or "{}")
        )
        return self

    def sql_warehouse(self, warehouse_ids: List[str]) -> DatabricksCrawler:
        """
        Defines the filter for SQL warehouses to include when crawling.
        (When using REST API extraction method).

        :param assets: list of `warehose_id` to include when crawling eg: [`3d939b0cc668be06`, `9a289b0cc838ce62`]
        ref: https://docs.databricks.com/api/workspace/datasources/list#warehouse_id
        :returns: crawler, set to include only those assets specified
        :raises InvalidRequestException: In the unlikely
        event the provided filter cannot be translated
        """
        warehouse_ids = warehouse_ids or []
        to_include = self.build_flat_hierarchical_filter(warehouse_ids)
        self._parameters.append(dict(name="sql-warehouse", value=to_include or "{}"))
        return self

    def import_tags(self, include: bool = False) -> DatabricksCrawler:
        """
        Whether to import tags from Databricks Unity Catalog to Atlan.
        Tags attached in Databricks will be automatically attached to your Databricks assets in Atlan.
        (When using REST API extraction method).

        :param include: if True, tags will be imported from Databricks Unity Catalog to Atlan, default: False
        :returns: crawler, set to whether to import tags from Databricks Unity Catalog to Atlan
        """
        self._parameters.append({"name": "enable-tag-sync", "value": include})
        return self

    def exclude_regex(self, regex: str) -> DatabricksCrawler:
        """
        Defines the exclude regex for crawler
        ignore tables & views based on a naming convention.

        :param regex: exclude regex for the crawler
        :returns: crawler, set to exclude
        only those assets specified in the regex
        """
        self._parameters.append(dict(name="temp-table-regex", value=regex))
        return self

    def _set_required_metadata_params(self):
        self._parameters.append(
            {"name": "credentials-fetch-strategy", "value": "credential_guid"}
        )
        self._parameters.append(
            {"name": "credential-guid", "value": "{{credentialGuid}}"}
        )
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
                "orchestration.atlan.com/sourceCategory": "lake",
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
                "orchestration.atlan.com/categories": "lake,crawler",
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/6328311007377",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": "Databricks Assets",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": f"Package to crawl databricks assets and publish to Atlan for discovery",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": '["databricks","lake","connector","crawler"]',  # fmt: skip # noqa
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "git+https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"{self._PACKAGE_PREFIX}-default-{self._NAME}-{self._epoch}",
            },
            name=f"{self._PACKAGE_PREFIX}-{self._epoch}",
            namespace="default",
        )
