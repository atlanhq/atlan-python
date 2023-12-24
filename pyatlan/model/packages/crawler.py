from json import dumps
from time import time
from typing import Any, Dict, Optional

from pyatlan.cache.role_cache import RoleCache
from pyatlan.model.assets import Connection
from pyatlan.model.packages.package import AbstractPackage


class AbstractCrawler(AbstractPackage):
    """
    Abstract class for crawlers
    """

    @staticmethod
    def get_epoch() -> str:
        return str(int(time()))

    @staticmethod
    def get_connection(
        connection_name: str,
        connection_type: str,
        roles: Optional[list[str]],
        groups: Optional[list[str]],
        users: Optional[list[str]],
        allow_query: bool,
        allow_query_preview: bool,
        row_limit: int,
        source_logo: str,
    ) -> Connection:
        """
        Builds a connection using the provided parameters,
        which will be the target for the package to crawl assets.
        """
        admin_role = RoleCache.get_id_for_name("$admin")
        if not roles and admin_role:
            roles = [admin_role]
        connection = Connection.create(
            name=connection_name,
            connector_type=connection_type,
            admin_roles=roles,
            admin_groups=groups,
            admin_users=users,
        )
        connection.allow_query = allow_query
        connection.allow_query_preview = allow_query_preview
        connection.row_limit = row_limit
        connection.default_credential_guid = "{{credentialGuid}}"
        connection.source_logo = source_logo
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
