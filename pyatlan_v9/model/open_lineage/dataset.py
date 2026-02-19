# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Dict, Union

import msgspec


class OpenLineageDataset(msgspec.Struct, kw_only=True, omit_defaults=True):
    """
    Model for handling OpenLineage datasets.
    """

    name: Union[str, None] = None
    """Unique name for that dataset within that namespace."""

    namespace: Union[str, None] = None
    """Namespace containing that dataset."""

    facets: Union[Dict[str, Any], None] = msgspec.field(default_factory=dict)
    """Facets for this dataset."""

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/Job"
