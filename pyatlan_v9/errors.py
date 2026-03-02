# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""Re-export all error classes from the legacy pyatlan.errors module."""

from pyatlan.errors import *  # noqa: F401,F403
from pyatlan.errors import (  # noqa: F401 — explicit re-exports for type checkers
    ApiError,
    AtlanError,
    AuthenticationError,
    ConflictError,
    ErrorCode,
    InvalidRequestError,
    LogicError,
    NotFoundError,
    PermissionError,
)
