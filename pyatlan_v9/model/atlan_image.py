# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Union

import msgspec


class AtlanImage(msgspec.Struct, kw_only=True):
    """Details of an uploaded image in Atlan."""

    id: Union[str, None] = None
    """Unique identifier (GUID) of the image."""

    version: Union[str, None] = None

    created_at: Union[int, None] = None
    """Time at which the image was uploaded (epoch), in milliseconds."""

    updated_at: Union[int, None] = None
    """Time at which the image was last modified (epoch), in milliseconds."""

    file_name: Union[str, None] = None
    """Generated name of the image that was uploaded."""

    raw_name: Union[str, None] = None
    """Generated name of the image that was uploaded."""

    key: Union[str, None] = None
    """Generated name of the image that was uploaded."""

    extension: Union[str, None] = None
    """Filename extension for the image that was uploaded."""

    content_type: Union[str, None] = None
    """MIME type for the image that was uploaded."""

    file_size: Union[str, None] = None
    """Size of the image that was uploaded, in bytes."""

    is_encrypted: Union[bool, None] = None
    """Whether the image is encrypted (true) or not (false)."""

    redirect_url: Union[str, None] = None

    is_uploaded: Union[bool, None] = None

    uploaded_at: Union[str, None] = None

    is_archived: Union[bool, None] = None
    """Whether the image has been archived (true) or is still actively available (false)."""
