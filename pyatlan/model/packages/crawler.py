from json import dumps
from typing import Any, Dict, Optional


class AbstractCrawler:
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
