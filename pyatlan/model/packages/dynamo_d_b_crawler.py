from __future__ import annotations

from typing import List, Optional

from pyatlan.model.enums import AtlanConnectorType, WorkflowPackage
from pyatlan.model.packages.base.crawler import AbstractCrawler
from pyatlan.model.workflow import WorkflowMetadata


class DynamoDBCrawler(AbstractCrawler):
    """
    Base configuration for a new Amazon DynamoDB crawler.

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
    """

    _NAME = "dynamodb"
    _PACKAGE_NAME = "@atlan/dynamodb"
    _PACKAGE_PREFIX = WorkflowPackage.DYNAMODB.value
    _CONNECTOR_TYPE = AtlanConnectorType.DYNAMODB
    _PACKAGE_ICON = "http://assets.atlan.com/assets/aws-dynamodb.svg"
    _PACKAGE_LOGO = "http://assets.atlan.com/assets/aws-dynamodb.svg"

    def __init__(
        self,
        connection_name: str,
        admin_roles: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
        admin_users: Optional[List[str]] = None,
        allow_query: bool = True,
        allow_query_preview: bool = True,
        row_limit: int = 10000,
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
        region: str,
    ) -> DynamoDBCrawler:
        """
        Set up the crawler to extract directly from the DynamoDB.

        :param region: AWS region where database is set up
        :returns: crawler, set up to extract directly from DynamoDB
        """
        local_creds = {
            "name": f"default-{self._NAME}-{self._epoch}-0",
            "extra": {"region": region},
            "connector_config_name": f"atlan-connectors-{self._NAME}",
        }
        self._credentials_body.update(local_creds)
        self._parameters.append(dict(name="extraction-method", value="direct"))
        return self

    def iam_user_auth(self, access_key: str, secret_key: str) -> DynamoDBCrawler:
        """
        Set up the crawler to use IAM user-based authentication.

        :param access_key: through which to access DynamoDB
        :param secret_key: through which to access DynamoDB
        :returns: crawler, set up to use IAM user-based authentication
        """
        local_creds = {
            "auth_type": "iam",
            "username": access_key,
            "password": secret_key,
        }
        self._credentials_body.update(local_creds)
        return self

    def iam_role_auth(self, arn: str, external_id: str) -> DynamoDBCrawler:
        """
        Set up the crawler to use IAM role-based authentication.

        :param arn: ARN of the AWS role
        :param external_id: AWS external ID
        :returns: crawler, set up to use IAM user role-based authentication
        """
        local_creds = {
            "auth_type": "role",
            "connector_type": "sdk",
        }
        self._credentials_body["extra"].update(
            {"aws_role_arn": arn, "aws_external_id": external_id}
        )
        self._credentials_body.update(local_creds)
        return self

    def include_regex(self, regex: str) -> DynamoDBCrawler:
        """
        Defines the regex of tables to include.
        By default, everything will be included.

        :param regex: exclude regex for the crawler
        :returns: crawler, set to include
        only those assets specified in the regex
        """
        self._parameters.append(dict(name="include-filter", value=regex))
        return self

    def exclude_regex(self, regex: str) -> DynamoDBCrawler:
        """
        Defines the regex of tables to ignore.
        By default, nothing will be excluded.
        This takes priority over include regex.

        :param regex: exclude regex for the crawler
        :returns: crawler, set to exclude
        only those assets specified in the regex
        """
        self._parameters.append(dict(name="exclude-filter", value=regex))
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
                "orchestration.atlan.com/docsUrl": "https://ask.atlan.com/hc/en-us/articles/8362826839823",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,
                "orchestration.atlan.com/marketplaceLink": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",  # noqa
                "orchestration.atlan.com/name": "Amazon DynamoDB Assets",
                "package.argoproj.io/author": "Atlan",
                "package.argoproj.io/description": "Package to crawl Amazon DynamoDB assets and publish to Atlan for discovery",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": '["dynamodb","nosql","document-database","connector","crawler"]',  # fmt: skip  # noqa
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"{self._PACKAGE_PREFIX}-default-{self._NAME}-{self._epoch}",
            },
            name=f"{self._PACKAGE_PREFIX}-{self._epoch}",
            namespace="default",
        )
