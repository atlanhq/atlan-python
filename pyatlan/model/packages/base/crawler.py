from json import dumps
from typing import Any, Dict, List, Optional

from pyatlan import utils
from pyatlan.errors import ErrorCode
from pyatlan.model.assets import Connection
from pyatlan.model.packages.base.package import AbstractPackage


class AbstractCrawler(AbstractPackage):
    """
    Abstract class for crawlers

    :param connection_name: name for the connection
    :param connection_type: type of connector for the connection
    :param admin_roles: admin roles for the connection
    :param admin_groups: admin groups for the connection
    :param admin_users: admin users for the connection
    :param allow_query: allow data to be queried in the connection (True) or not (False)
    :param allow_query_preview: allow sample data viewing for assets in the connection (True) or not (False)
    :param row_limit: maximum number of rows that can be returned by a query
    :param source_logo: logo to use for the source

    :raises AtlanError: if there is not at least one role,
    group, or user defined as an admin (or any of them are invalid)
    """

    def __init__(
        self,
        connection_name: str,
        connection_type: str,
        admin_roles: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
        admin_users: Optional[List[str]] = None,
        allow_query: bool = False,
        allow_query_preview: bool = False,
        row_limit: int = 0,
        source_logo: str = "",
    ):
        super().__init__()
        self._connection_name = connection_name
        self._connection_type = connection_type
        self._admin_roles = admin_roles
        self._admin_groups = admin_groups
        self._admin_users = admin_users
        self._allow_query = allow_query
        self._allow_query_preview = allow_query_preview
        self._row_limit = row_limit
        self._source_logo = source_logo
        self._epoch = int(utils.get_epoch_timestamp())

    def _get_connection(self) -> Connection:
        """
        Builds a connection using the provided parameters,
        which will be the target for the package to crawl assets.
        """
        connection = Connection.create(
            name=self._connection_name,
            connector_type=self._connection_type,
            admin_roles=self._admin_roles,
            admin_groups=self._admin_groups,
            admin_users=self._admin_users,
        )
        connection.allow_query = self._allow_query
        connection.allow_query_preview = self._allow_query_preview
        connection.row_limit = self._row_limit
        connection.default_credential_guid = "{{credentialGuid}}"
        connection.source_logo = self._source_logo
        connection.is_discoverable = True
        connection.is_editable = False
        return connection

    @staticmethod
    def build_hierarchical_filter(raw_filter: Optional[dict]) -> str:
        """
        Build an exact match filter from the provided map of databases and schemas.

        :param raw_filter: map keyed by database name with each value being a list of schemas
        :returns: an exact-match filter map string, usable in crawlers include / exclude filters
        :raises InvalidRequestException: In the unlikely event the provided filter cannot be translated
        """
        to_include: Dict[str, Any] = {}
        if not raw_filter:
            return ""
        try:
            for db_name, schemas in raw_filter.items():
                exact_schemas = [f"^{schema}$" for schema in schemas]
                to_include[f"^{db_name}$"] = exact_schemas
            return dumps(to_include)
        except (AttributeError, TypeError):
            raise ErrorCode.UNABLE_TO_TRANSLATE_FILTERS.exception_with_parameters()

    @staticmethod
    def build_flat_filter(raw_filter: Optional[list]) -> str:
        """
        Build a filter from the provided list of object names / IDs.

        :param raw_filter: list of objects for the filter
        :returns: a filter map string, usable in crawlers include / exclude filters
        :raises InvalidRequestException: In the unlikely event the provided filter cannot be translated
        """
        to_include: Dict[str, Any] = {}
        if not raw_filter:
            return ""
        try:
            for entry in raw_filter:
                to_include[entry] = {}
            return dumps(to_include)
        except (AttributeError, TypeError):
            raise ErrorCode.UNABLE_TO_TRANSLATE_FILTERS.exception_with_parameters()
