from json import JSONDecodeError, dumps
from typing import Optional

from pyatlan.model.assets import Connection
from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class GlueCrawler(AbstractCrawler):
    _NAME = "glue"
    _PACKAGE_NAME = "@atlan/glue"
    _PACKAGE_PREFIX = WorkflowPackage.GLUE.value
    _CONNECTOR_TYPE = AtlanConnectorType.GLUE
    _PACKAGE_ICON = (
        "https://atlan-public.s3.eu-west-1.amazonaws.com/atlan/logos/aws-glue.png"
    )
    _PACKAGE_LOGO = (
        "https://atlan-public.s3.eu-west-1.amazonaws.com/atlan/logos/aws-glue.png"
    )

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

    def direct(
        self,
        region: str,
    ) -> "GlueCrawler":
        local_creds = {
            "name": f"default-{self._NAME}-{self._epoch}-0",
            "extra": {"region": region},
            "connectorConfigName": f"atlan-connectors-{self._NAME}",
        }
        self._credentials_body.update(local_creds)
        return self

    def iam_user_auth(self, access_key: str, secret_key: str) -> "GlueCrawler":
        local_creds = {
            "authType": "iam",
            "username": access_key,
            "password": secret_key,
        }
        self._credentials_body.update(local_creds)
        return self

    def _build_asset_filter(self, filter_type: str, filter_assets: list[str]) -> None:
        if not filter_assets:
            self._parameters.append({"name": f"{filter_type}-filter", "value": {}})
            return
        filter_dict: dict = {"AwsDataCatalog": {}}
        for asset in filter_assets:
            filter_dict["AwsDataCatalog"][asset] = {}
            try:
                filter_values = dumps(filter_dict)
                self._parameters.append(
                    {"name": f"{filter_type}-filter", "value": filter_values}
                )
            except JSONDecodeError as e:
                # TODO: Use logger here
                print(f"Error while encoding JSON for {filter_type} filter: {e}")

    def include(self, include_assets: list[str]) -> "GlueCrawler":
        self._build_asset_filter("include", include_assets)
        return self

    def exclude(self, exclude_assets: list[str]) -> "GlueCrawler":
        self._build_asset_filter("exclude", exclude_assets)
        return self

    def _get_metadata(self) -> WorkflowMetadata:
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
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/6335637665681",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": f"{self._NAME} Assets",
                "orchestration.atlan.com/usecase": "crawling,auto-classifications",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": f"Package to crawl AWS {self._NAME.capitalize()} assets and publish to Atlan for discovery.",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": '["lake","connector","crawler","glue","aws","s3"]',  # fmt: skip # noqa
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "git+https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"{self._PACKAGE_PREFIX}-default-{self._NAME}-{self._epoch}",
            },
            name=f"{self._PACKAGE_PREFIX}-{self._epoch}",
            namespace="default",
        )
