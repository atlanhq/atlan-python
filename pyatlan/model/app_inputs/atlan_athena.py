# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's /v1/apps/{app}/inputs contract — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_app_inputs
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.app_inputs._base import AppInput


class AtlanAthenaInputs(AppInput):
    """Typed inputs for the `atlan-athena` app (generated from its input contract)."""

    _APP_ID: ClassVar[str] = "atlan-athena"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    credential_guid: str = ""
    """Credential Guid"""
    credentials: Dict[str, Any] = {}
    """Credentials"""
    connection: Dict[str, Any] = {}
    """Connection"""
    metadata: Dict[str, Any] = {}
    """Metadata"""


__all__ = ["AtlanAthenaInputs"]
