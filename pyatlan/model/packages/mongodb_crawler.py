from __future__ import annotations

from typing import Dict, List, Optional

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.base.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class MongoDBCrawler(AbstractCrawler):
    """
    Base configuration for a new MongoDB crawler.

    :param client: connectivity to an Atlan tenant
    :param connection_name: name for the connection
    :param admin_roles: admin roles for the connection
    :param admin_groups: admin groups for the connection
    :param admin_users: admin users for the connection
    :param allow_query: allow data to be queried in the
    connection (True) or not (False), default: True
    :param allow_query_preview: allow sample data viewing for
    assets in the connection (True) or not (False), default: True
    :param row_limit: maximum number of rows
    that can be returned by a query, default: 10000

    Example:
        Basic MongoDB connection with SCRAM-SHA-256 authentication::

            from pyatlan.client.atlan import AtlanClient
            from pyatlan.model.packages import MongoDBCrawler

            client = AtlanClient()

            # Create MongoDB crawler with explicit authentication mechanism
            crawler = (
                MongoDBCrawler(
                    client=client,
                    connection_name="production-mongodb",
                    admin_roles=["admin-role-guid"],
                )
                .direct(hostname="mongodb.example.com", port=27017)
                .basic_auth(
                    username="admin_user",
                    password="secure_password",
                    native_host="mongodb.example.com:27017",
                    default_db="admin",
                    auth_db="admin",
                    is_ssl=True,
                    auth_mechanism="SCRAM-SHA-256",  # Explicitly specify auth mechanism
                )
                .include(assets=["production_db", "analytics_db"])
            )

            # Run the crawler workflow
            workflow = crawler.to_workflow()
            response = client.workflow.run(workflow)

    Note:
        - The `authSource` parameter (default: "admin") specifies the database
          where the user's credentials are stored.
        - Common authentication mechanisms include "SCRAM-SHA-1" and "SCRAM-SHA-256".
          If not specified, MongoDB will negotiate the best available mechanism.
        - For MongoDB Atlas clusters, ensure SSL is enabled (is_ssl=True).
        - Ensure the MongoDB user has the necessary roles such as `readAnyDatabase`
          and `clusterMonitor` for metadata extraction.
    """

    _NAME = "mongodb"
    _PACKAGE_NAME = "@atlan/mongodb"
    _PACKAGE_PREFIX = WorkflowPackage.MONGODB.value
    _CONNECTOR_TYPE = AtlanConnectorType.MONGODB
    _PACKAGE_ICON = "https://assets.atlan.com/assets/mongoDB.svg"
    _PACKAGE_LOGO = "https://assets.atlan.com/assets/mongoDB.svg"

    def __init__(
        self,
        client: AtlanClient,
        connection_name: str,
        admin_roles: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
        admin_users: Optional[List[str]] = None,
        allow_query: bool = True,
        allow_query_preview: bool = True,
        row_limit: int = 10000,
    ):
        super().__init__(
            client=client,
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

    def direct(self, hostname: str, port: int = 27017) -> MongoDBCrawler:
        """
        Set up the crawler to extract directly from the MongoDB Atlas.

        :param hostname: hostname of the Atlas SQL connection
        :param port: port number of the Atlas SQL connection. default: `27017`
        :returns: crawler, set up to extract directly from the Atlas SQL connection
        """
        local_creds = {
            "name": f"default-{self._NAME}-{self._epoch}-0",
            "host": hostname,
            "port": port,
            "connector_config_name": f"atlan-connectors-{self._NAME}",
        }
        self._credentials_body.update(local_creds)
        self._parameters.append(dict(name="extraction-method", value="direct"))
        return self

    def basic_auth(
        self,
        username: str,
        password: str,
        native_host: str,
        default_db: str,
        auth_db: str = "admin",
        is_ssl: bool = True,
        auth_mechanism: Optional[str] = None,
    ) -> MongoDBCrawler:
        """
        Set up the crawler to use basic authentication.

        :param username: through which to access MongoDB connection.
        :param password: through which to access MongoDB connection.
        :param native_host: native host address for the MongoDB connection
            (e.g., "mongodb.example.com:27017" or "localhost:27017").
        :param default_db: default database to connect to.
        :param auth_db: authentication database where user credentials are stored
            (default is `"admin"`). This should match the database where the
            MongoDB user was created.
        :param is_ssl: whether to use SSL/TLS for the connection (default is `True`).
            Set to `False` for local MongoDB instances or when SSL is not required.
        :param auth_mechanism: authentication mechanism to use. Common values:
            - `"SCRAM-SHA-1"`: Legacy SCRAM authentication
            - `"SCRAM-SHA-256"`: Modern SCRAM authentication (recommended)
            - `None`: Let MongoDB negotiate the best mechanism (default)
        :returns: crawler, set up to use basic authentication

        Note:
            Common authentication issues and solutions:

            - **Wrong authSource**: If authentication fails, verify the `auth_db`
              parameter matches the database where your user was created. For
              example, if you created a user in the "myapp" database, set
              `auth_db="myapp"`.

            - **Authentication mechanism mismatch**: Atlan requires SCRAM
              authentication for self-managed MongoDB. If you're using an older
              MongoDB version or a different auth mechanism, you may need to
              specify it explicitly with the `auth_mechanism` parameter.

            - **SSL/TLS certificate issues**: If you encounter SSL errors with
              self-signed certificates, ensure your MongoDB instance is properly
              configured for SSL, or set `is_ssl=False` for local development.

            - **Insufficient privileges**: The MongoDB user must have appropriate
              roles such as `readAnyDatabase` and `clusterMonitor` to extract
              metadata. Create the user with:

              .. code-block:: javascript

                  db.createUser({
                      user: "atlan_user",
                      pwd: "password",
                      roles: [
                          { role: "readAnyDatabase", db: "admin" },
                          { role: "clusterMonitor", db: "admin" }
                      ]
                  })

        Example:
            Basic authentication with explicit SCRAM-SHA-256::

                crawler.basic_auth(
                    username="my_user",
                    password="my_password",
                    native_host="mongodb.example.com:27017",
                    default_db="myapp",
                    auth_db="admin",
                    is_ssl=True,
                    auth_mechanism="SCRAM-SHA-256"
                )
        """
        extra_config = {
            "native-host": native_host,
            "default-database": default_db,
            "authSource": auth_db,
            "ssl": is_ssl,
        }

        # Add authentication mechanism if specified
        if auth_mechanism:
            extra_config["authMechanism"] = auth_mechanism

        local_creds = {
            "authType": "basic",
            "username": username,
            "password": password,
            "extra": extra_config,
        }
        self._credentials_body.update(local_creds)
        return self

    def include(self, assets: List[str]) -> MongoDBCrawler:
        """
        Defines the filter for assets to include when crawling.

        :param assets: list of databases names to include when crawling
        :returns: crawler, set to include only those assets specified
        :raises InvalidRequestException: In the unlikely
        event the provided filter cannot be translated
        """
        assets = assets or []
        include_assets: Dict[str, List[str]] = {asset: [] for asset in assets}
        to_include = self.build_hierarchical_filter(include_assets)
        self._parameters.append(
            dict(dict(name="include-filter", value=to_include or "{}"))
        )
        return self

    def exclude(self, assets: List[str]) -> MongoDBCrawler:
        """
        Defines the filter for assets to exclude when crawling.

        :param assets: list of databases names to exclude when crawling
        :returns: crawler, set to exclude only those assets specified
        :raises InvalidRequestException: In the unlikely
        event the provided filter cannot be translated
        """
        assets = assets or []
        exclude_assets: Dict[str, List[str]] = {asset: [] for asset in assets}
        to_exclude = self.build_hierarchical_filter(exclude_assets)
        self._parameters.append(dict(name="exclude-filter", value=to_exclude or "{}"))
        return self

    def exclude_regex(self, regex: str) -> MongoDBCrawler:
        """
        Defines the exclude regex for crawler
        ignore collections based on a naming convention.

        :param regex: exclude regex for the crawler
        :returns: crawler, set to exclude
        only those assets specified in the regex
        """
        self._parameters.append(dict(name="temp-table-regex", value=regex))
        return self

    def _set_required_metadata_params(self):
        self._parameters.append(
            {"name": "credentials-fetch-strategy", "value": "credential_guid"}
        )
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
                "orchestration.atlan.com/sourceCategory": "nosql",
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
                "orchestration.atlan.com/categories": "nosql,crawler",
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/7841931946639",  # noqa
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": "MongoDB Assets",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": f"Package to crawl MongoDB assets and publish to Atlan for discovery",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": '["mongodb","nosql","document-database","connector","crawler"]',  # fmt: skip # noqa
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "git+https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"{self._PACKAGE_PREFIX}-default-{self._NAME}-{self._epoch}",
            },
            name=f"{self._PACKAGE_PREFIX}-{self._epoch}",
            namespace="default",
        )
