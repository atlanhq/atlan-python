# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's /v1/apps/{app}/inputs contract — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_app_inputs
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.app_inputs._base import AppInput


class OracleMinerInputs(AppInput):
    """Typed inputs for the `oracle-miner` app (generated from its input contract)."""

    _APP_ID: ClassVar[str] = "oracle-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    connection: Optional[Any] = None
    credential_guid: str = ""
    """Credential Guid"""
    credential_ref: Any = None
    extraction_method: str = ""
    """Extraction Method"""
    agent_json: Any = None
    exclude_filter: Union[Dict[str, Any], str] = ""
    """Exclude Filter"""
    include_filter: Union[Dict[str, Any], str] = ""
    """Include Filter"""
    temp_table_regex: str = ""
    """Temp Table Regex"""
    source_tag_prefix: str = ""
    """Source Tag Prefix"""
    incremental_extraction: bool = False
    """Incremental Extraction"""
    column_batch_size: int = 25000
    """Column Batch Size"""
    column_chunk_size: int = 100000
    """Column Chunk Size"""
    copy_workers: int = 3
    """Copy Workers"""
    prepone_marker_timestamp: bool = True
    """Prepone Marker Timestamp"""
    prepone_marker_hours: int = 3
    """Prepone Marker Hours"""


__all__ = ["OracleMinerInputs"]
