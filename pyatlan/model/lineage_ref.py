# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
from __future__ import annotations

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject


class LineageRef(AtlanObject):
    qualified_name: str = Field(
        default=None, description="Unique name of the asset being referenced."
    )
    name: str = Field(
        default=None, description="Simple name of the asset being referenced."
    )
    guid: str = Field(default=None, description="UUID of the asset being referenced.")
