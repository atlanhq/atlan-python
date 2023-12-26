from json import dumps
from typing import Any, Dict, Optional

from pyatlan import utils

# from pyatlan.utils import get_epoch_timestamp
from pyatlan.cache.role_cache import RoleCache
from pyatlan.model.assets import Connection
from pyatlan.model.packages.package import AbstractPackage


class AbstractCrawler(AbstractPackage):
    """
    Abstract class for crawlers
    """

    def __init__(
        self,
        connection_name: str,
        connection_type: str,
        admin_roles: Optional[list[str]],
        admin_groups: Optional[list[str]],
        admin_users: Optional[list[str]],
        allow_query: bool = False,
        allow_query_preview: bool = False,
        row_limit: int = 0,
        source_logo: str = "",
    ):
        self._parameters: list = []
        self._credentials_body: dict = {}
        self._epoch = utils.get_epoch_timestamp()
        self._connection_name = connection_name
        self._connection_type = connection_type
        self._admin_roles = admin_roles
        self._admin_groups = admin_groups
        self._admin_users = admin_users
        self._allow_query = allow_query
        self._allow_query_preview = allow_query_preview
        self._row_limit = row_limit
        self._source_logo = source_logo

    def _get_connection(self) -> Connection:
        """
        Builds a connection using the provided parameters,
        which will be the target for the package to crawl assets.
        """
        if not self._admin_roles:
            role = RoleCache.get_id_for_name("$admin")
            if role:
                self._admin_roles = [role]
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
        to_include: Dict[str, Any] = {}
        if raw_filter:
            for db_name, schemas in raw_filter.items():
                exact_schemas = [f"^{schema}$" for schema in schemas]
                to_include[f"^{db_name}$"] = exact_schemas
        return dumps(to_include)

    @staticmethod
    def build_flat_filter(raw_filter: Optional[list]) -> str:
        to_include: Dict[str, Any] = {}
        if raw_filter:
            for entry in raw_filter:
                to_include[entry] = {}
        return dumps(to_include)

    @staticmethod
    def build_dbt_cloud_filter(raw_filter: Optional[dict]) -> str:
        to_include: Dict[str, Any] = {}
        if raw_filter:
            for account_id, projects in raw_filter.items():
                if account_id not in to_include:
                    to_include[account_id] = {}
                for project_id in projects:
                    to_include[account_id][project_id] = {}
        return dumps(to_include)
