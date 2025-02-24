from __future__ import annotations

from typing import List, Optional

from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.base.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class PostgresCrawler(AbstractCrawler):
    """
    Base configuration for a new PostgreSQL crawler.

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

    _NAME = "postgres"
    _PACKAGE_NAME = "@atlan/postgres"
    _PACKAGE_PREFIX = WorkflowPackage.POSTGRES.value
    _CONNECTOR_TYPE = AtlanConnectorType.POSTGRES
    _PACKAGE_ICON = "https://www.postgresql.org/media/img/about/press/elephant.png"
    _PACKAGE_LOGO = "https://www.postgresql.org/media/img/about/press/elephant.png"

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

    def s3(
        self,
        bucket_name: str,
        bucket_prefix: str,
        bucket_region: Optional[str] = None,
    ) -> PostgresCrawler:
        """
        Set up the crawler to extract from S3 bucket

        :param bucket_name: name of the bucket/storage
        that contains the extracted metadata files
        :param bucket_prefix: prefix is everything after the
        bucket/storage name, including the `path`
        :param bucket_region: (Optional) name of the region if applicable
        :returns: crawler, set up to extract from S3 bucket
        """
        self._parameters.append(dict(name="extraction-method", value="s3"))
        self._parameters.append(dict(name="metadata-s3-bucket", value=bucket_name))
        self._parameters.append(dict(name="metadata-s3-prefix", value=bucket_prefix))
        self._parameters.append(dict(name="metadata-s3-region", value=bucket_region))
        return self

    def direct(
        self,
        hostname: str,
        database: str,
        port: int = 5432,
    ) -> PostgresCrawler:
        """
        Set up the crawler to extract directly from PostgreSQL.

        :param hostname: hostname of the PostgreSQL instance
        :param database: database name to crawl
        :param port: port number of PostgreSQL instance, defaults to `5432`
        :returns: crawler, set up to extract directly from PostgreSQL
        """
        local_creds = {
            "name": f"default-{self._NAME}-{self._epoch}-0",
            "host": hostname,
            "port": port,
            "extra": {"database": database},
            "connector_config_name": f"atlan-connectors-{self._NAME}",
        }
        self._credentials_body.update(local_creds)
        self._parameters.append(dict(name="extraction-method", value="direct"))
        return self

    def basic_auth(self, username: str, password: str) -> PostgresCrawler:
        """
        Set up the crawler to use basic authentication.

        :param username: through which to access PostgreSQL
        :param password: through which to access PostgreSQL
        :returns: crawler, set up to use basic authentication
        """
        local_creds = {
            "auth_type": "basic",
            "username": username,
            "password": password,
        }
        self._credentials_body.update(local_creds)
        return self

    def iam_user_auth(
        self, username: str, access_key: str, secret_key: str
    ) -> PostgresCrawler:
        """
        Set up the crawler to use IAM user-based authentication.

        :param username: database username to extract from
        :param access_key: through which to access PostgreSQL
        :param secret_key: through which to access PostgreSQL
        :returns: crawler, set up to use IAM user-based authentication
        """
        local_creds = {
            "auth_type": "iam_user",
            "connector_type": "jdbc",
            "username": access_key,
            "password": secret_key,
        }
        self._credentials_body["extra"].update({"username": username})
        self._credentials_body.update(local_creds)
        return self

    def iam_role_auth(
        self, username: str, arn: str, external_id: str
    ) -> PostgresCrawler:
        """
        Set up the crawler to use IAM role-based authentication.

        :param username: database username to extract from
        :param arn: ARN of the AWS role
        :param external_id: AWS external ID
        :returns: crawler, set up to use IAM user role-based authentication
        """
        local_creds = {
            "auth_type": "iam_role",
            "connector_type": "jdbc",
        }
        self._credentials_body["extra"].update(
            {"username": username, "aws_role_arn": arn, "aws_external_id": external_id}
        )
        self._credentials_body.update(local_creds)
        return self

    def include(self, assets: dict) -> PostgresCrawler:
        """
        Defines the filter for assets to include when crawling.

        :param assets: Map keyed by database name with each value being a list of schemas
        :returns: crawler, set to include only those assets specified
        :raises InvalidRequestException: In the unlikely
        event the provided filter cannot be translated
        """
        include_assets = assets or {}
        to_include = self.build_hierarchical_filter(include_assets)
        self._parameters.append(dict(name="include-filter", value=to_include or "{}"))
        return self

    def exclude(self, assets: dict) -> PostgresCrawler:
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

    def exclude_regex(self, regex: str) -> PostgresCrawler:
        """
        Defines the exclude regex for crawler ignore
        tables and views based on a naming convention.

        :param regex: exclude regex for the crawler
        :returns: crawler, set to exclude
        only those assets specified in the regex
        """
        self._parameters.append(dict(name="temp-table-regex", value=regex))
        return self

    def source_level_filtering(self, enable: bool) -> PostgresCrawler:
        """
        Defines whether to enable or disable schema level filtering on source.
        schemas selected in the include filter will be fetched.

        :param enable: whether to enable (`True`) or
        disable (`False`) schema level filtering on source
        :returns: crawler, with schema level filtering on source
        """
        self._parameters.append(dict(name="use-source-schema-filtering", value=enable))
        return self

    def jdbc_internal_methods(self, enable: bool) -> PostgresCrawler:
        """
        Defines whether to enable or disable JDBC
        internal methods for data extraction.

        :param enable: whether to whether to enable (`True`) or
        disable (`False`) JDBC internal methods for data extraction
        :returns: crawler, with jdbc internal methods for data extraction
        """
        self._parameters.append(dict(name="use-jdbc-internal-methods", value=enable))
        return self

    def _set_required_metadata_params(self):
        self._parameters.append(
            {"name": "credential-guid", "value": "{{credentialGuid}}"}
        )
        self._parameters.append(
            {
                "name": "connection",
                "value": self._get_connection().json(
                    by_alias=True, exclude_unset=True, exclude_none=True
                ),
            }
        )
        self._parameters.append(dict(name="publish-mode", value="production"))

    def _get_metadata(self) -> WorkflowMetadata:
        self._set_required_metadata_params()
        return WorkflowMetadata(
            labels={
                "orchestration.atlan.com/certified": "true",
                "orchestration.atlan.com/source": self._NAME,
                "orchestration.atlan.com/sourceCategory": "database",
                "orchestration.atlan.com/type": "connector",
                "orchestration.atlan.com/verified": "true",
                "package.argoproj.io/installer": "argopm",
                "package.argoproj.io/name": f"a-t-ratlans-l-a-s-h{self._NAME}",
                "package.argoproj.io/registry": "httpsc-o-l-o-ns-l-a-s-hs-l-a-s-hpackages.atlan.com",
                f"orchestration.atlan.com/default-{self._NAME}-{self._epoch}": "true",
                "orchestration.atlan.com/atlan-ui": "true",
                "orchestration.atlan.com/dependentPackage": "",
            },
            annotations={
                "orchestration.atlan.com/allowSchedule": "true",
                "orchestration.atlan.com/categories": "postgres,crawler",
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/6329557275793",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": "Postgres Assets",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": "Package to crawl PostgreSQL assets and publish to Atlan for discovery",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": '["postgres","database","sql","connector","crawler"]',  # fmt: skip  # noqa
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"{self._PACKAGE_PREFIX}-default-{self._NAME}-{self._epoch}",
            },
            name=f"{self._PACKAGE_PREFIX}-{self._epoch}",
            namespace="default",
        )
