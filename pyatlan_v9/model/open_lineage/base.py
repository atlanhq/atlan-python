# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Union
from urllib.parse import urlparse

import msgspec
from dateutil import parser  # type:ignore[import-untyped]


class OpenLineageBaseEvent(
    msgspec.Struct, kw_only=True, omit_defaults=True, rename="camel"
):
    """
    Base model for OpenLineage events.
    """

    event_time: Union[str, None] = None
    """Time the event occurred at."""

    producer: Union[str, None] = None
    """Producer of the event."""

    schema_url: Union[str, None] = msgspec.field(
        default=None, name="schemaURL"
    )
    """Schema URL for the event."""

    def __post_init__(self) -> None:
        if self.schema_url is None:
            self.schema_url = self._get_schema()
        if self.event_time is not None:
            self._validate_event_time(self.event_time)
        if self.producer is not None:
            urlparse(self.producer)

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/BaseEvent"

    @staticmethod
    def _validate_event_time(value: str) -> str:
        # Parse and validate the ISO format
        parser.isoparse(value)
        if "t" not in value.lower():
            raise ValueError(f"Parsed date-time has to contain time: {value}")
        return value


class OpenLineageBaseFacet(
    msgspec.Struct, kw_only=True, omit_defaults=True
):
    """
    Base model for OpenLineage facets.
    """

    producer: Union[str, None] = msgspec.field(default=None, name="_producer")
    schema_url: Union[str, None] = msgspec.field(default=None, name="_schemaURL")

    def __post_init__(self) -> None:
        if self.schema_url is None:
            self.schema_url = self._get_schema()

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/BaseFacet"
