from __future__ import annotations

from json import dumps
from typing import Dict, List, Optional

from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.base.miner import AbstractMiner
from pyatlan.model.workflow import WorkflowMetadata


class SnowflakeMiner(AbstractMiner):
    """
    Base configuration for a new Snowflake miner.

    :param connection_qualified_name: unique name of the
    Snowflake connection whose assets should be mined
    """

    _NAME = "snowflake"
    _PACKAGE_NAME = "@atlan/snowflake-miner"
    _PACKAGE_PREFIX = WorkflowPackage.SNOWFLAKE_MINER.value
    _CONNECTOR_TYPE = AtlanConnectorType.SNOWFLAKE
    _PACKAGE_ICON = "https://docs.snowflake.com/en/_images/logo-snowflake-sans-text.png"
    _PACKAGE_LOGO = "https://1amiydhcmj36tz3733v94f15-wpengine.netdna-ssl.com/wp-content/themes/snowflake/assets/img/logo-blue.svg"  # noqa

    def __init__(
        self,
        connection_qualified_name: str,
    ):
        self._advanced_config = False
        super().__init__(connection_qualified_name=connection_qualified_name)

    def direct(
        self,
        start_epoch: int,
        database: Optional[str] = None,
        schema: Optional[str] = None,
    ) -> SnowflakeMiner:
        """
        Set up the miner to extract directly from Snowflake.

        :param start_epoch: date and time from which to start mining, as an epoch
        :param database: name of the database to extract from (cloned database)
        :param schema: name of the schema to extract from (cloned database)
        :returns: miner, set up to extract directly from Snowflake
        """
        # In case of default database
        if not (database or schema):
            self._parameters.append(dict(name="snowflake-database", value="default"))
        # In case of cloned database
        else:
            self._parameters.append(dict(name="database-name", value=database))
            self._parameters.append(dict(name="schema-name", value=schema))
        self._parameters.append(dict(name="extraction-method", value="query_history"))
        self._parameters.append(
            dict(name="miner-start-time-epoch", value=str(start_epoch))
        )
        return self

    def s3(
        self,
        s3_bucket: str,
        s3_prefix: str,
        sql_query_key: str,
        default_database_key: str,
        default_schema_key: str,
        session_id_key: str,
        s3_bucket_region: Optional[str] = None,
    ) -> SnowflakeMiner:
        """
        Set up the miner to extract from S3 (using JSON line-separated files).

        :param s3_bucket: S3 bucket where the JSON line-separated files are located
        :param s3_prefix: prefix within the S3 bucket in
        which the JSON line-separated files are located
        :param sql_query_key: JSON key containing the query definition
        :param default_database_key: JSON key containing the default
        database name to use if a query is not qualified with database name
        :param default_schema_key: JSON key containing the default schema name
        to use if a query is not qualified with schema name
        :param session_id_key: JSON key containing the session ID of the SQL query
        :param s3_bucket_region: (Optional) region of the S3 bucket if applicable
        :returns: miner, set up to extract from a set of JSON line-separated files in S3
        """
        self._parameters.append(dict(name="extraction-method", value="s3"))
        self._parameters.append(dict(name="extraction-s3-bucket", value=s3_bucket))
        self._parameters.append(dict(name="extraction-s3-prefix", value=s3_prefix))
        self._parameters.append(dict(name="sql-json-key", value=sql_query_key))
        self._parameters.append(
            dict(name="catalog-json-key", value=default_database_key)
        )
        self._parameters.append(dict(name="schema-json-key", value=default_schema_key))
        self._parameters.append(dict(name="session-json-key", value=session_id_key))
        s3_bucket_region and self._parameters.append(
            dict(name="extraction-s3-region", value=s3_bucket_region)
        )
        return self

    def exclude_users(self, users: List[str]) -> SnowflakeMiner:
        """
        Defines users who should be excluded when calculating
        usage metrics for assets (for example, system accounts).

        :param users: list of users to exclude when calculating usage metrics
        :returns: miner, set to exclude the specified users from usage metrics
        :raises InvalidRequestException: in the unlikely event the provided
        list cannot be translated
        """
        exclude_users = users or []
        self._parameters.append(
            dict(
                name="popularity-exclude-user-config",
                value=dumps(exclude_users) if exclude_users else "[]",
            )
        )
        return self

    def popularity_window(self, days: int = 30) -> SnowflakeMiner:
        """
        Defines number of days to consider for calculating popularity.

        :param days: number of days to consider, defaults to 30
        :returns: miner, set to include popularity window
        """
        self._advanced_config = True
        self._parameters.append(dict(name="popularity-window-days", value=str(days)))
        return self

    def native_lineage(self, enabled: bool) -> SnowflakeMiner:
        """
        Whether to enable native lineage from Snowflake, using
        Snowflake's ACCESS_HISTORY.OBJECTS_MODIFIED Column.
        Note: this is only available only for Snowflake Enterprise customers.

        :param enabled: if True, native lineage from Snowflake will be used for crawling
        :returns: miner, set to include / exclude native lineage from Snowflake
        """
        self._advanced_config = True
        self._parameters.append(
            dict(name="native-lineage-active", value="true" if enabled else "false")
        )
        return self

    def custom_config(self, config: Dict) -> SnowflakeMiner:
        """
        Defines custom JSON configuration controlling
        experimental feature flags for the miner.

        :param config: custom configuration dict
        :returns: miner, set to include custom configuration
        """
        config and self._parameters.append(
            dict(name="control-config", value=dumps(config))
        )
        self._advanced_config = True
        return self

    def _set_required_metadata_params(self):
        self._parameters.append(
            dict(
                name="control-config-strategy",
                value="custom" if self._advanced_config else "default",
            )
        )
        self._parameters.append(dict(name="sigle-session", value="false"))

    def _get_metadata(self) -> WorkflowMetadata:
        self._set_required_metadata_params()
        return WorkflowMetadata(
            labels={
                "orchestration.atlan.com/certified": "true",
                "orchestration.atlan.com/source": self._NAME,
                "orchestration.atlan.com/sourceCategory": "warehouse",
                "orchestration.atlan.com/type": "miner",
                "orchestration.atlan.com/verified": "true",
                "package.argoproj.io/installer": "argopm",
                "package.argoproj.io/name": f"a-t-ratlans-l-a-s-h{self._NAME}-miner",
                "package.argoproj.io/registry": "httpsc-o-l-o-ns-l-a-s-hs-l-a-s-hpackages.atlan.com",
                "orchestration.atlan.com/atlan-ui": "true",
            },
            annotations={
                "orchestration.atlan.com/allowSchedule": "true",
                "orchestration.atlan.com/categories": "warehouse,miner",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/6482067592337",
                "orchestration.atlan.com/emoji": "\uD83D\uDE80",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": "Snowflake Miner",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": "Package to mine query history data from Snowflake and store it for further processing. The data mined will be used for generating lineage and usage metrics.",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": "[\"snowflake\",\"warehouse\",\"connector\",\"miner\"]",  # fmt: skip
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "git+https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"{self._PACKAGE_PREFIX}-{self._epoch}",
            },
            name=f"{self._PACKAGE_PREFIX}-{self._epoch}",
            namespace="default",
        )
