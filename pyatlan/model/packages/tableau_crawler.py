from typing import Optional

from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class TableauCrawler(AbstractCrawler):
    _NAME = "tableau"
    _PACKAGE_NAME = "@atlan/tableau"
    _PACKAGE_PREFIX = WorkflowPackage.TABLEAU.value
    _CONNECTOR_TYPE = AtlanConnectorType.TABLEAU
    _PACKAGE_ICON = "https://img.icons8.com/color/480/000000/tableau-software.png"
    _PACKAGE_LOGO = "https://img.icons8.com/color/480/000000/tableau-software.png"

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
        site: str,
        port: int = 443,
        ssl_enabled: bool = True,
    ) -> "TableauCrawler":
        local_creds = {
            "name": f"default-{self._NAME}-{self._epoch}-0",
            "host": hostname,
            "port": port,
            "extra": {
                "protocol": "https" if ssl_enabled else "http",
                "defaultSite": site,
            },
            "connectorConfigName": f"atlan-connectors-{self._NAME}",
        }
        self._credentials_body.update(local_creds)
        self._parameters.append({"name": "extraction-method", "value": "direct"})
        return self

    def basic_auth(self, username: str, password: str) -> "TableauCrawler":
        local_creds = {
            "authType": "basic",
            "username": username,
            "password": password,
        }
        self._credentials_body.update(local_creds)
        return self

    def personal_access_token(
        self, username: str, access_token: str
    ) -> "TableauCrawler":
        local_creds = {
            "authType": "personal_access_token",
            "username": username,
            "password": access_token,
        }
        self._credentials_body.update(local_creds)
        return self

    def include(self, projects: list[str]) -> "TableauCrawler":
        include_projects = projects or []
        to_include = self.build_flat_filter(include_projects)
        if to_include:
            self._parameters.append(dict(name="include-filter", value=to_include))
        return self

    def exclude(self, projects: list[str]) -> "TableauCrawler":
        exclude_projects = projects or []
        to_exclude = self.build_flat_filter(exclude_projects)
        if to_exclude:
            self._parameters.append(dict(name="exclude-filter", value=to_exclude))
        return self

    def crawl_hidden_fields(self, enabled: bool = True) -> "TableauCrawler":
        self._parameters.append(
            {
                "name": "crawl-hidden-datasource-fields",
                "value": "true" if enabled else "false",
            }
        )
        return self

    def crawl_unpublished(self, enabled: bool = True) -> "TableauCrawler":
        self._parameters.append(
            {
                "name": "crawl-unpublished-worksheets-dashboard",
                "value": "true" if enabled else "false",
            }
        )
        return self

    def alternate_host(self, hostname: str) -> "TableauCrawler":
        self._parameters.append({"name": "tableau-alternate-host", "value": hostname})
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
        self._parameters.append(dict(name="atlas-auth-type", value="internal"))
        self._parameters.append(dict(name="publish-mode", value="production"))

    def _get_metadata(self) -> WorkflowMetadata:
        self._set_required_metadata_params()
        return WorkflowMetadata(
            labels={
                "orchestration.atlan.com/certified": "true",
                "orchestration.atlan.com/source": self._NAME,
                "orchestration.atlan.com/sourceCategory": "bi",
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
                "orchestration.atlan.com/categories": "tableau,crawler",
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/6332449996689",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,  # noqa
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": f"{self._NAME} Assets",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": f"Package to crawl {self._NAME.capitalize()} assets and publish to Atlan for discovery.",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": "[\"tableau\",\"bi\",\"connector\",\"crawler\"]",  # fmt: skip
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/parent": ".",
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "git+https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"{self._PACKAGE_PREFIX}-default-{self._NAME}-{self._epoch}",
            },
            name=f"{self._PACKAGE_PREFIX}-{self._epoch}",
            namespace="default",
        )
