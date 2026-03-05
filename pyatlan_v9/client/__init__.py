# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""
PyAtlan V9 Client - HTTP client for Atlan's Atlas API.

This module provides the AtlanClient class (plain Python, no Pydantic BaseSettings)
that manages HTTP sessions, proxy/SSL configuration, and sub-client access.
"""

from pyatlan_v9.client.atlan import AtlanClient, client_connection

__all__ = [
    "AtlanClient",
    "client_connection",
]
