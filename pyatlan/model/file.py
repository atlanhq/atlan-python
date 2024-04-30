# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
from __future__ import annotations

from enum import Enum

from pyatlan.model.core import AtlanObject


class PresignedURLRequest(AtlanObject):
    key: str
    expiry: str
    method: PresignedURLRequest.Method

    class Method(str, Enum):
        GET = "GET"
        PUT = "PUT"


class CloudStorageIdentifier(str, Enum):
    S3 = "amazonaws.com"
    GCS = "storage.googleapis.com"
    AZURE_BLOB = "blob.core.windows.net"
