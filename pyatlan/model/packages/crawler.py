from json import dumps
from typing import Any, Dict, List, Optional

from pyatlan.cache.role_cache import RoleCache
from pyatlan.model.assets import Connection
from pyatlan.model.packages.package import AbstractPackage


class AbstractCrawler(AbstractPackage):
    @staticmethod
    def get_connection(
        connection_name: str,
        connection_type,
        roles: List[str],
        groups: List[str],
        users: List[str],
        allow_query: bool,
        allow_query_preview: bool,
        row_limit: int = 10000,
        source_logo: str = None,
    ):
        """
        Builds a connection using the provided parameters,
        which will be the target for the package to crawl assets.
        """
        if not roles:
            roles = [RoleCache.get_id_for_name("$admin")]
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
        connection.source_logo = source_logo or (
            "https://docs.snowflake.com/en/_images/logo-snowflake-sans-text.png"
        )
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
    def build_flat_filter(raw_filter: Optional[dict]) -> str:
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
