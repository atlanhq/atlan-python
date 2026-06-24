# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's /v1/apps/{app}/inputs contract — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_app_inputs
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.app_inputs._base import AppInput


class KafkaApacheInputs(AppInput):
    """Typed inputs for the `Kafka-apache` / `apache` app (generated from its input contract)."""

    _APP_ID: ClassVar[str] = "Kafka-apache"
    _ENTRYPOINT: ClassVar[Optional[str]] = "apache"

    credential_guid: str = ""
    """Credential Guid"""
    extraction_method: str = "direct"
    """Extraction Method"""
    agent_json: Any = None
    connection: Any = None
    connection_qualified_name: str = ""
    """Connection Qualified Name"""
    connection_name: str = ""
    """Connection Name"""
    connection_id: str = ""
    """Connection Id"""
    include_filter: str = ""
    """Include Filter"""
    exclude_filter: str = ""
    """Exclude Filter"""
    skip_internal_topics: bool = True
    """Skip Internal Topics"""


__all__ = ["KafkaApacheInputs"]
