from __future__ import annotations

from enum import Enum
from json import dumps
from typing import List, Optional

from pyatlan.model.enums import WorkflowPackage
from pyatlan.model.packages.base.miner import AbstractMiner
from pyatlan.model.workflow import WorkflowMetadata


class DatabricksMiner(AbstractMiner):
    """
    Base configuration for a new Databricks miner.

    :param connection_qualified_name: unique name of the
    Databricks connection whose assets should be mined
    """

    _NAME = "databricks"
    _PACKAGE_NAME = "@atlan/databricks-lineage"
    _PACKAGE_PREFIX = WorkflowPackage.DATABRICKS_LINEAGE.value
    _PACKAGE_ICON = "https://assets.atlan.com/assets/databricks.svg"
    _PACKAGE_LOGO = "https://assets.atlan.com/assets/databricks.svg"

    class ExtractionMethod(str, Enum):
        REST_API = "rest-api"
        SYSTEM_TABLE = "system-table"

    def __init__(
        self,
        connection_qualified_name: str,
    ):
        self._advanced_config = False
        super().__init__(connection_qualified_name=connection_qualified_name)
        self._parameters.append(dict(name="calculate-popularity", value=False))
        self._parameters.append(dict(name="popularity-window-days", value=30))
        self._parameters.append(dict(name="miner-start-time-epoch", value=0))
        self._parameters.append(
            dict(
                name="extraction-method-popularity",
                value=self.ExtractionMethod.REST_API.value,
            )
        )

    def rest_api(self):
        """
        Sets up the Databricks miner to use the REST API method for fetching lineage.

        :returns: miner, configured to use the REST API extraction method from Databricks.
        """
        self._parameters.append(
            dict(name="extraction-method", value=self.ExtractionMethod.REST_API.value)
        )
        return self

    def offline(self, bucket_name: str, bucket_prefix: str):
        """
        Sets up the Databricks miner to use the offline extraction method.

        This method sets up the miner to extract data from an S3 bucket by specifying
        the bucket name and prefix.

        :param bucket_name: name of the S3 bucket to extract data from.
        :param bucket_prefix: prefix within the S3 bucket to narrow the extraction scope.
        :returns: miner, configured for offline extraction.
        """
        self._parameters.append(dict(name="extraction-method", value="offline"))
        self._parameters.append(
            dict(name="offline-extraction-bucket", value=bucket_name)
        )
        self._parameters.append(
            dict(name="offline-extraction-prefix", value=bucket_prefix)
        )
        return self

    def system_table(self, warehouse_id: str):
        """
        Sets up the Databricks miner to use the system table extraction method.

        This method sets up the miner to extract data
        using a specific SQL warehouse by providing its unique ID.

        :param warehouse_id: unique identifier of the SQL
        warehouse to be used for system table extraction.
        :returns: miner, configured for system table extraction.
        """
        self._parameters.append(
            dict(name="extraction-method", value=self.ExtractionMethod.SYSTEM_TABLE)
        )
        self._parameters.append(dict(name="sql-warehouse", value=warehouse_id))
        return self

    def popularity_configuration(
        self,
        start_date: str,
        extraction_method: DatabricksMiner.ExtractionMethod = ExtractionMethod.REST_API,
        window_days: Optional[int] = None,
        excluded_users: Optional[List[str]] = None,
        warehouse_id: Optional[str] = None,
    ) -> DatabricksMiner:
        """
        Configures the Databricks miner to calculate asset popularity metrics.

        This method sets up the miner to fetch query history and calculate
        popularity metrics based on the specified configuration.

        :param start_date: epoch timestamp from which queries will be fetched
        for calculating popularity. This does not affect lineage generation.
        :param extraction_method: method used to fetch popularity data.
        Defaults to `ExtractionMethod.REST_API`.
        :param window_days: (Optional) number of days to consider for calculating popularity metrics.
        :param excluded_users: (Optional) list of usernames to exclude from usage metrics calculations.
        :param warehouse_id: (Optional) unique identifier of the SQL warehouse to use for
        popularity calculations. Required if `extraction_method` is `ExtractionMethod.SYSTEM_TABLE`.
        :returns: miner, configured with popularity settings.
        """
        excluded_users = excluded_users or []
        config_map = {
            "calculate-popularity": True,
            "extraction-method-popularity": extraction_method.value,
            "miner-start-time-epoch": start_date,
            "popularity-window-days": window_days,
        }
        for param in self._parameters:
            if param["name"] in config_map:
                param["value"] = config_map[param["name"]]
        self._parameters.append(
            dict(name="popularity-exclude-user-config", value=dumps(excluded_users))
        )
        if extraction_method == self.ExtractionMethod.SYSTEM_TABLE:
            self._parameters.append(
                dict(name="sql-warehouse-popularity", value=warehouse_id)
            )
        return self

    def _get_metadata(self) -> WorkflowMetadata:
        return WorkflowMetadata(
            labels={
                "orchestration.atlan.com/certified": "true",
                "orchestration.atlan.com/source": self._NAME,
                "orchestration.atlan.com/sourceCategory": "lake",
                "orchestration.atlan.com/type": "miner",
                "orchestration.atlan.com/verified": "true",
                "package.argoproj.io/installer": "argopm",
                "package.argoproj.io/name": f"a-t-ratlans-l-a-s-h{self._NAME}-miner",
                "package.argoproj.io/registry": "httpsc-o-l-o-ns-l-a-s-hs-l-a-s-hpackages.atlan.com",
                "orchestration.atlan.com/atlan-ui": "true",
            },
            annotations={
                "orchestration.atlan.com/allowSchedule": "true",
                "orchestration.atlan.com/categories": "lake,miner",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/7034583224081",
                "orchestration.atlan.com/emoji": "\ud83d\ude80",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": "Databricks Miner",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": "Package to extract lineage information and usage metrics from Databricks.",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": '["databricks","lake","connector","miner"]',  # fmt: skip
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "git+https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"{self._PACKAGE_PREFIX}-{self._epoch}",
            },
            name=f"{self._PACKAGE_PREFIX}-{self._epoch}",
            namespace="default",
        )
