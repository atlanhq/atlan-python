from __future__ import annotations

from pyatlan.model.enums import WorkflowPackage
from pyatlan.model.packages.base.custom_package import AbstractCustomPackage
from pyatlan.model.workflow import WorkflowMetadata


class APITokenConnectionAdmin(AbstractCustomPackage):
    """
    Base configuration for a new API token connection admin package.
    """

    _NAME = "api-token-connection-admin"
    _PACKAGE_NAME = f"@csa/{_NAME}"
    _PACKAGE_PREFIX = WorkflowPackage.API_TOKEN_CONNECTION_ADMIN.value
    _PACKAGE_ICON = "http://assets.atlan.com/assets/ph-key-light.svg"
    _PACKAGE_LOGO = "http://assets.atlan.com/assets/ph-key-light.svg"

    def config(
        self, connection_qualified_name: str, api_token_guid: str
    ) -> APITokenConnectionAdmin:
        """
        Set up the API token connection admin with the specified configuration.

        :param connection_qualified_name: connection qualified name
        to which you want to add the API token as a connection admin.
        :param api_token_guid: guid of the API token

        :returns: package, with the specified configuration.
        """
        self._parameters.append(
            {"name": "connection_qualified_name", "value": connection_qualified_name}
        )
        self._parameters.append({"name": "api_token_guid", "value": api_token_guid})
        return self

    def _get_metadata(self) -> WorkflowMetadata:
        return WorkflowMetadata(
            labels={
                "orchestration.atlan.com/certified": "true",
                "orchestration.atlan.com/source": "atlan",
                "orchestration.atlan.com/sourceCategory": "utility",
                "orchestration.atlan.com/type": "custom",
                "orchestration.atlan.com/preview": "true",
                "orchestration.atlan.com/verified": "true",
                "package.argoproj.io/installer": "argopm",
                "package.argoproj.io/name": f"a-t-rcsas-l-a-s-h{self._NAME}",
                "package.argoproj.io/registry": "httpsc-o-l-o-ns-l-a-s-hs-l-a-s-hpackages.atlan.com",
                "orchestration.atlan.com/atlan-ui": "true",
            },
            annotations={
                "orchestration.atlan.com/allowSchedule": "true",
                "orchestration.atlan.com/categories": "kotlin,utility",
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": f"https://solutions.atlan.com/{self._NAME}/",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,
                "orchestration.atlan.com/name": "API Token Connection Admin",
                "package.argoproj.io/author": "Atlan CSA",
                "package.argoproj.io/description": "Assigns an API token as a connection admin for an existing connection.",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": '["kotlin","utility"]',  # fmt: skip
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/parent": ".",
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "git+https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"csa-{self._NAME}-{self._epoch}",
            },
            name=f"csa-{self._NAME}-{self._epoch}",
            namespace="default",
        )
