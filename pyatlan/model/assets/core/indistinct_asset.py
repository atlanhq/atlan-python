# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from pydantic.v1 import Field, validator

from .asset import Asset


class IndistinctAsset(Asset, type_name="IndistinctAsset"):
    """
    Instance of an asset where we cannot determine
    (have not yet modeled) its detailed information.
    In the meanwhile, this provides a catch-all case
    where at least the basic asset information is available.
    """

    type_name: str = Field(default="IndistinctAsset", allow_mutation=True)

    @validator("type_name")
    def validate_type_name(cls, v):
        return v
