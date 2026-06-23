# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's /v1/apps/{app}/inputs contract — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_app_inputs
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.app_inputs._base import AppInput


class PostgresCrawlerInputs(AppInput):
    """Typed inputs for the `postgres-crawler` / `crawler` app (generated from its input contract)."""

    _APP_ID: ClassVar[str] = "postgres-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"

    connection: Optional[Any] = None
    credential_guid: str = ""
    """Credential Guid"""
    credential_ref: Any = None
    extraction_method: str = ""
    """Extraction Method"""
    agent_json: Any = None
    output_prefix: str = ""
    """Output Prefix"""
    output_path: str = ""
    """Output Path"""
    exclude_filter: Union[Dict[str, Any], str] = ""
    """Exclude Filter"""
    include_filter: Union[Dict[str, Any], str] = ""
    """Include Filter"""
    temp_table_regex: str = ""
    """Temp Table Regex"""
    source_tag_prefix: str = ""
    """Source Tag Prefix"""
    advanced_config: str = "default"
    """Advanced Config"""
    use_source_schema_filtering: str = "false"
    """Use Source Schema Filtering"""
    use_jdbc_internal_methods: str = "true"
    """Use Jdbc Internal Methods"""
    control_config_strategy: str = "default"
    """Control Config Strategy"""
    control_config: str = "{}"
    """Control Config"""
    preflight_check: str = ""
    """Preflight Check"""
    postgres_crawler_credential: Any = None
    output_dir: str = ""
    """Output Dir"""
    checkpoint_dir: str = ""
    """Checkpoint Dir"""
    load_to_atlan: bool = True
    """Load To Atlan"""
    publish_dry_run: bool = False
    """Publish Dry Run"""


__all__ = ["PostgresCrawlerInputs"]
