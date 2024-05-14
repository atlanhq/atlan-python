from __future__ import annotations

from typing import List, Optional

from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.base.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class ConfluentKafkaCrawler(AbstractCrawler):
    """
    Base configuration for a new Confluent Kafka crawler.

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

    _NAME = "confluent-kafka"
    _PACKAGE_NAME = "@atlan/kafka-confluent-cloud"
    _PACKAGE_PREFIX = WorkflowPackage.KAFKA_CONFLUENT_CLOUD.value
    _CONNECTOR_TYPE = AtlanConnectorType.CONFLUENT_KAFKA
    _PACKAGE_ICON = "https://cdn.confluent.io/wp-content/uploads/apache-kafka-icon-2021-e1638496305992.jpg"
    _PACKAGE_LOGO = "https://cdn.confluent.io/wp-content/uploads/apache-kafka-icon-2021-e1638496305992.jpg"

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

    def direct(self, bootstrap: str, encrypted: bool = True) -> ConfluentKafkaCrawler:
        """
        Set up the crawler to extract directly from Kafka.

        :param bootstrap: hostname and port number (host.example.com:9092) for the Kafka bootstrap server
        :param encrypted: whether to use an encrypted SSL connection (True), or plaintext (False), default: True
        :returns: crawler, set up to extract directly from Kafka
        """
        local_creds = {
            "name": f"default-{self._NAME}-{self._epoch}-0",
            "host": bootstrap,
            "port": 9092,
            "extra": {
                "security_protocol": "SASL_SSL" if encrypted else "SASL_PLAINTEXT"
            },
            "connector_config_name": "atlan-connectors-kafka-confluent-cloud",
        }
        self._credentials_body.update(local_creds)
        self._parameters.append(dict(name="extraction-method", value="direct"))
        return self

    def api_token(
        self,
        api_key: str,
        api_secret: str,
    ) -> ConfluentKafkaCrawler:
        """
        Set up the crawler to use API token-based authentication.

        :param api_key: through which to access Kafka
        :param api_secret: through which to access Kafka
        :returns: crawler, set up to use API token-based authentication
        """
        local_creds = {
            "auth_type": "basic",
            "username": api_key,
            "password": api_secret,
        }
        self._credentials_body.update(local_creds)
        return self

    def include(self, regex: str = "") -> ConfluentKafkaCrawler:
        """
        Defines the filter for topics to include when crawling.

        :param regex: any topic names that match this
        regular expression will be included in crawling
        :returns: crawler, set to include only those topics specified
        """
        if not regex:
            return self
        self._parameters.append(dict(name="include-filter", value=regex))
        return self

    def exclude(self, regex: str = "") -> ConfluentKafkaCrawler:
        """
        Defines a regular expression to use for excluding topics when crawling.

        :param regex: any topic names that match this
        regular expression will be excluded from crawling
        :returns: crawler, set to exclude any topics
        that match the provided regular expression
        """
        if not regex:
            return self
        self._parameters.append(dict(name="exclude-filter", value=regex))
        return self

    def skip_internal(self, enabled: bool = True) -> ConfluentKafkaCrawler:
        """
        Whether to skip internal topics when crawling (True) or include them.

        :param enabled: if True, internal topics
        will be skipped when crawling, default: True
        :returns: crawler, set to include or exclude internal topics
        """
        self._parameters.append(
            {
                "name": "skip-internal-topics",
                "value": "true" if enabled else "false",
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
        self._parameters.append(dict(name="publish-mode", value="production"))
        self._parameters.append(dict(name="atlas-auth-type", value="internal"))

    def _get_metadata(self) -> WorkflowMetadata:
        self._set_required_metadata_params()
        return WorkflowMetadata(
            labels={
                "orchestration.atlan.com/certified": "true",
                "orchestration.atlan.com/source": self._NAME,
                "orchestration.atlan.com/sourceCategory": "eventbus",
                "orchestration.atlan.com/type": "connector",
                "orchestration.atlan.com/verified": "true",
                "package.argoproj.io/installer": "argopm",
                "package.argoproj.io/name": "a-t-ratlans-l-a-s-hkafka-confluent-cloud",
                "package.argoproj.io/registry": "httpsc-o-l-o-ns-l-a-s-hs-l-a-s-hpackages.atlan.com",
                f"orchestration.atlan.com/default-{self._NAME}-{self._epoch}": "true",
                "orchestration.atlan.com/atlan-ui": "true",
            },
            annotations={
                "orchestration.atlan.com/allowSchedule": "true",
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/6778924963599",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,  # noqa
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": "Confluent Kafka Assets",
                "orchestration.atlan.com/usecase": "crawling,discovery",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": "Package to crawl Confluent Kafka assets and publish to Atlan for discovery.",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": '["kafka-confluent-cloud","confluent-kafka","eventbus","connector","kafka"]',  # fmt: skip # noqa
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
