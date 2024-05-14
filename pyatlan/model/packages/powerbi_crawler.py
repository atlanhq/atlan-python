from __future__ import annotations

from typing import List, Optional

from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.base.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class PowerBICrawler(AbstractCrawler):
    """
    Base configuration for a new PowerBI crawler.

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

    _NAME = "powerbi"
    _PACKAGE_NAME = "@atlan/powerbi"
    _PACKAGE_PREFIX = WorkflowPackage.POWERBI.value
    _CONNECTOR_TYPE = AtlanConnectorType.POWERBI
    _PACKAGE_ICON = (
        "https://powerbi.microsoft.com/pictures/application-logos/svg/powerbi.svg"
    )
    _PACKAGE_LOGO = (
        "https://powerbi.microsoft.com/pictures/application-logos/svg/powerbi.svg"
    )

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

    def direct(self) -> PowerBICrawler:
        """
        Set up the crawler to extract directly from Power BI.

        :returns: rawler, set up to extract directly from Power BI
        """
        local_creds = {
            "name": f"default-{self._NAME}-{self._epoch}-0",
            "host": "api.powerbi.com",
            "port": 443,
            "connector_config_name": f"atlan-connectors-{self._NAME}",
        }
        self._credentials_body.update(local_creds)
        return self

    def delegated_user(
        self,
        username: str,
        password: str,
        tenant_id: str,
        client_id: str,
        client_secret: str,
    ) -> PowerBICrawler:
        """
        Set up the crawler to use delegated user authentication.

        :param username: through which to access Power BI
        :param password: through which to access Power BI
        :param tenant_id: unique ID (GUID) of the tenant for Power BI
        :param client_id: unique ID (GUID) of the client for Power BI
        :param client_secret: through which to access Power BI
        :returns: crawler, set up to use delegated user authentication
        """
        local_creds = {
            "authType": "basic",
            "username": username,
            "password": password,
            "extra": {
                "tenantId": tenant_id,
                "clientId": client_id,
                "clientSecret": client_secret,
            },
        }
        self._credentials_body.update(local_creds)
        return self

    def service_principal(
        self, tenant_id: str, client_id: str, client_secret: str
    ) -> PowerBICrawler:
        """
        Set up the crawler to use service principal authentication.

        :param tenant_id: unique ID (GUID) of the tenant for Power BI
        :param client_id: unique ID (GUID) of the client for Power BI
        :param client_secret: through which to access Power BI
        :returns: crawler, set up to use service principal authentication
        """
        local_creds = {
            "authType": "service_principal",
            "connectorType": "rest",
            "extra": {
                "tenantId": tenant_id,
                "clientId": client_id,
                "clientSecret": client_secret,
            },
        }
        self._credentials_body.update(local_creds)
        return self

    def include(self, workspaces: List[str]) -> PowerBICrawler:
        """
        Defines the filter for workspaces to include when crawling.

        :param workspaces: the GUIDs of workspaces to include when crawling
        :return: crawler, set to include only those workspaces specified
        :raises InvalidRequestException: In the unlikely
        event the provided filter cannot be translated
        """
        include_workspaces = workspaces or []
        to_include = self.build_flat_filter(include_workspaces)
        self._parameters.append(
            dict(dict(name="include-filter", value=to_include or "{}"))
        )
        return self

    def exclude(self, workspaces: List[str]) -> PowerBICrawler:
        """
        Defines the filter for workspaces to exclude when crawling.

        :param workspaces: the GUIDs of workspaces to exclude when crawling
        :return: crawler, set to exclude only those workspaces specified
        :raises InvalidRequestException: In the unlikely
        event the provided filter cannot be translated
        """
        exclude_workspaces = workspaces or []
        to_exclude = self.build_flat_filter(exclude_workspaces)
        self._parameters.append(dict(name="exclude-filter", value=to_exclude or "{}"))
        return self

    def direct_endorsements(self, enabled: bool = True) -> PowerBICrawler:
        """
        Whether to directly attach endorsements as
        certificates (True), or instead raise these as requests

        :param enabled: if True, endorsements will be directly set as
        certificates on assets, otherwise requests will be raised, default: True
        :returns: crawler, set to directly (or not) set certificates on assets for endorsements
        """
        self._parameters.append(
            {
                "name": "endorsement-attach-mode",
                "value": "metastore" if enabled else "requests",
            }
        )
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
                "orchestration.atlan.com/categories": "powerbi,crawler",
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/6332245668881",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,  # noqa
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": f"{self._NAME} Assets",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": "Package to crawl PowerBI assets and publish to Atlan for discovery.",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": "[\"powerbi\",\"bi\",\"connector\",\"crawler\"]",  # fmt: skip
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
