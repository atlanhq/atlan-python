from typing import Optional

from pyatlan.model.assets import Connection
from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class DbtCrawler(AbstractCrawler):
    _NAME = "dbt"
    _PACKAGE_NAME = "@atlan/dbt"
    _PACKAGE_PREFIX = WorkflowPackage.DBT.value
    _CONNECTOR_TYPE = AtlanConnectorType.DBT
    _PACKAGE_ICON = "https://assets.atlan.com/assets/dbt-new.svg"
    _PACKAGE_LOGO = "https://assets.atlan.com/assets/dbt-new.svg"

    def __init__(
        self,
        connection_name: str,
        admin_roles: Optional[list[str]],
        admin_groups: Optional[list[str]],
        admin_users: Optional[list[str]],
        allow_query: bool = False,
        allow_query_preview: bool = False,
        row_limit: int = 0,
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

    def cloud(
        self, hostname: str, service_token: str, multi_tenant: bool = True
    ) -> "DbtCrawler":
        local_creds = {
            "name": f"default-{self._NAME}-{self._epoch}-1",
            "host": hostname if hostname else "https://cloud.getdbt.com",
            "port": 443,
            "authType": "token",
            "username": "",
            "password": service_token,
            "connectorConfigName": f"atlan-connectors-{self._NAME}",
        }
        self._credentials_body.update(local_creds)
        self._parameters.append(dict(name="extraction-method", value="api"))
        self._parameters.append(
            dict(name="deployment-type", value="multi" if multi_tenant else "single")
        )
        return self

    def core(self, s3_bucket: str, s3_prefix: str, s3_region: str) -> "DbtCrawler":
        self._parameters.append(dict(name="extraction-method", value="core"))
        self._parameters.append(dict(name="deployment-type", value="single"))
        self._parameters.append(dict(name="core-extraction-s3-bucket", value=s3_bucket))
        self._parameters.append(dict(name="core-extraction-s3-prefix", value=s3_prefix))
        self._parameters.append(dict(name="core-extraction-s3-region", value=s3_region))
        return self

    def enrich_materialized_assets(self, enabled: bool = False) -> "DbtCrawler":
        self._parameters.append(
            {
                "name": "enrich-materialised-sql-assets",
                "value": "true" if enabled else "false",
            }
        )
        return self

    def tags(self, include: bool = False) -> "DbtCrawler":
        self._parameters.append(
            {
                "name": "enable-dbt-tagsync",
                "value": "true" if include else "false",
            }
        )
        return self

    def limit_to_connection(self, connection_qualified_name: str) -> "DbtCrawler":
        self._parameters.append(
            {
                "name": "connection-qualified-name",
                "value": connection_qualified_name,
            }
        )
        return self

    def include(self, filter: str = "") -> "DbtCrawler":
        self._parameters.append(
            dict(name="include-filter", value=filter if filter else "{}")
        )
        self._parameters.append(
            dict(name="include-filter-core", value=filter if filter else "*")
        )
        return self

    def exclude(self, filter: str = "") -> "DbtCrawler":
        self._parameters.append(
            dict(name="exclude-filter", value=filter if filter else "{}")
        )
        self._parameters.append(
            dict(name="exclude-filter-core", value=filter if filter else "*")
        )
        return self

    def _get_metadata(self) -> WorkflowMetadata:
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
