from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.base.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class SigmaCrawler(AbstractCrawler):
    """
    Base configuration for a new Sigma crawler.

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

    _NAME = "sigma"
    _PACKAGE_NAME = "@atlan/sigma"
    _PACKAGE_PREFIX = WorkflowPackage.SIGMA.value
    _CONNECTOR_TYPE = AtlanConnectorType.SIGMA
    _PACKAGE_ICON = "http://assets.atlan.com/assets/sigma.svg"
    _PACKAGE_LOGO = "http://assets.atlan.com/assets/sigma.svg"

    class Hostname(str, Enum):
        GCP = "api.sigmacomputing.com"
        AZURE = "api.us.azure.sigmacomputing.com"
        AWS = "aws-api.sigmacomputing.com"
        AWS_CANADA = "api.ca.aws.sigmacomputing.com"
        AWS_EUROPE = "api.eu.aws.sigmacomputing.com"

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

    def direct(self, hostname: SigmaCrawler.Hostname, port: int = 443) -> SigmaCrawler:
        """
        Set up the crawler to extract directly from Sigma.

        :param hostname: of the Sigma host, for example `SigmaCrawler.Hostname.AWS`
        :param port: of the Sigma host, default: `443`
        :returns: crawler, set up to extract directly from Sigma
        """
        local_creds = {
            "name": f"default-{self._NAME}-{self._epoch}-0",
            "host": hostname,
            "port": port,
            "extra": {},
            "connector_config_name": f"atlan-connectors-{self._NAME}",
        }
        self._credentials_body.update(local_creds)
        return self

    def api_token(
        self,
        client_id: str,
        api_token: str,
    ) -> SigmaCrawler:
        """
        Set up the crawler to use API token-based authentication.

        :param client_id: through which to access Sigma
        :param api_token: through which to access Sigma
        :returns: crawler, set up to use API token-based authentication
        """
        local_creds = {
            "username": client_id,
            "password": api_token,
            "auth_type": "api_token",
        }
        self._credentials_body.update(local_creds)
        return self

    def include(self, workbooks: List[str]) -> SigmaCrawler:
        """
        Defines the filter for Sigma workbooks to include when crawling.

        :param workbooks: the GUIDs of workbooks to include when crawling,
        default to no workbooks if `None` are specified
        :returns: crawler, set to include only those workbooks specified
        :raises InvalidRequestException: In the unlikely
        event the provided filter cannot be translated
        """
        include_workbooks = workbooks or []
        to_include = self.build_flat_filter(include_workbooks)
        self._parameters.append(
            dict(dict(name="include-filter", value=to_include or "{}"))
        )
        return self

    def exclude(self, workbooks: List[str]) -> SigmaCrawler:
        """
        Defines the filter for Sigma workbooks to exclude when crawling.

        :param workbooks: the GUIDs of workbooks to exclude when crawling,
        default to no workbooks if `None` are specified
        :returns: crawler, set to exclude only those workbooks specified
        :raises InvalidRequestException: In the unlikely
        event the provided filter cannot be translated
        """
        exclude_workbooks = workbooks or []
        to_exclude = self.build_flat_filter(exclude_workbooks)
        self._parameters.append(dict(name="exclude-filter", value=to_exclude or "{}"))
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
        self._parameters.append(dict(name="atlas-auth-type", value="internal"))

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
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/8731744918813",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": "Sigma Assets",
                "orchestration.atlan.com/categories": "sigma,crawler",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": "Package to crawl Sigma assets and publish to Atlan for discovery",
                "package.argoproj.io/homepage": "",
                "package.argoproj.io/keywords": '[\"sigma\",\"bi\",\"connector\",\"crawler\"]',  # fmt: skip
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
