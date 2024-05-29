from __future__ import annotations

from pyatlan.model.enums import WorkflowPackage
from pyatlan.model.packages.base.miner import AbstractMiner
from pyatlan.model.workflow import WorkflowMetadata


class ConnectionDelete(AbstractMiner):
    """
    Base configuration for a new connection delete workflow.

    :param qualified_name: unique name of the
    connection whose assets should be deleted
    :param purge: if `True`, permanently delete the connection
    and its assets, otherwise only archive (soft-delete) them `False`
    """

    _NAME = "connection-delete"
    _PACKAGE_NAME = "@atlan/connection-delete"
    _PACKAGE_PREFIX = WorkflowPackage.CONNECTION_DELETE.value
    _PACKAGE_ICON = "https://assets.atlan.com/assets/connection-delete.svg"
    _PACKAGE_LOGO = "https://assets.atlan.com/assets/connection-delete.svg"

    def __init__(
        self,
        qualified_name: str,
        purge: bool,
    ):
        super().__init__(connection_qualified_name=qualified_name)
        self._parameters.append(dict(name="delete-assets", value="true"))
        self._parameters.append(
            dict(name="delete-type", value="PURGE" if purge else "SOFT")
        )

    def _get_metadata(self) -> WorkflowMetadata:
        return WorkflowMetadata(
            labels={
                "orchestration.atlan.com/certified": "true",
                "orchestration.atlan.com/type": "utility",
                "orchestration.atlan.com/verified": "true",
                "package.argoproj.io/installer": "argopm",
                "package.argoproj.io/name": f"a-t-ratlans-l-a-s-h{self._NAME}",
                "package.argoproj.io/registry": "httpsc-o-l-o-ns-l-a-s-hs-l-a-s-hpackages.atlan.com",
                "orchestration.atlan.com/atlan-ui": "true",
            },
            annotations={
                "orchestration.atlan.com/allowSchedule": "false",
                "orchestration.atlan.com/categories": "utility,admin,connection,delete",
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/6755306791697",
                "orchestration.atlan.com/emoji": "🗑️",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": "Connection Delete",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": "Deletes a connection and all its related assets",
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": '["delete","admin","utility"]',
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "git+https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"{self._PACKAGE_PREFIX}-{self._epoch}",
            },
            name=f"{self._PACKAGE_PREFIX}-{self._epoch}",
            namespace="default",
        )
