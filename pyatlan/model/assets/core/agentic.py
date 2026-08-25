# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AgenticSource
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField

from .catalog import Catalog


class Agentic(Catalog):
    """Description"""

    type_name: str = Field(default="Agentic", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Agentic":
            raise ValueError("must be Agentic")
        return v

    def __setattr__(self, name, value):
        if name in Agentic._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AGENTIC_VERSION: ClassVar[NumericField] = NumericField(
        "agenticVersion", "agenticVersion"
    )
    """
    Version of this agentic asset as an epoch-millisecond timestamp. One Atlan entity per (slug, version) tuple.
    """
    AGENTIC_SOURCE: ClassVar[KeywordField] = KeywordField(
        "agenticSource", "agenticSource"
    )
    """
    Product surface this agentic asset was created from, so agents and skills can be attributed to their originating surface without slug pattern matching (AUT-1074). Mirrors AtlanAppWorkflow.source, which does the same for workflows (AUT-1028).
    """  # noqa: E501

    _convenience_properties: ClassVar[List[str]] = [
        "agentic_version",
        "agentic_source",
    ]

    @property
    def agentic_version(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.agentic_version

    @agentic_version.setter
    def agentic_version(self, agentic_version: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agentic_version = agentic_version

    @property
    def agentic_source(self) -> Optional[AgenticSource]:
        return None if self.attributes is None else self.attributes.agentic_source

    @agentic_source.setter
    def agentic_source(self, agentic_source: Optional[AgenticSource]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agentic_source = agentic_source

    class Attributes(Catalog.Attributes):
        agentic_version: Optional[int] = Field(default=None, description="")
        agentic_source: Optional[AgenticSource] = Field(default=None, description="")

    attributes: Agentic.Attributes = Field(
        default_factory=lambda: Agentic.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
