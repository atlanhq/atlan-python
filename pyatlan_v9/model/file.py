# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from enum import Enum

import msgspec


class PresignedURLRequest(msgspec.Struct, kw_only=True):
    """Request to generate a pre-signed URL for file upload/download."""

    class Method(str, Enum):
        GET = "GET"
        PUT = "PUT"

    key: str
    """Key (path) of the file."""

    expiry: str
    """Expiry duration for the URL."""

    method: PresignedURLRequest.Method
    """HTTP method for the pre-signed URL."""


class CloudStorageIdentifier(str, Enum):
    """Identifiers for cloud storage providers."""

    S3 = "amazonaws.com"
    GCS = "storage.googleapis.com"
    AZURE_BLOB = "blob.core.windows.net"
