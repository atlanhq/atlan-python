# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .agentic import Agentic


class Context(Agentic):
    """Description"""

    type_name: str = Field(default="Context", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Context":
            raise ValueError("must be Context")
        return v

    def __setattr__(self, name, value):
        if name in Context._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CONTEXT_REPOSITORY_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "contextRepositoryQualifiedName", "contextRepositoryQualifiedName"
    )
    """
    Qualified name of the context repository to which this asset belongs.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "context_repository_qualified_name",
    ]

    @property
    def context_repository_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_repository_qualified_name
        )

    @context_repository_qualified_name.setter
    def context_repository_qualified_name(
        self, context_repository_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_repository_qualified_name = (
            context_repository_qualified_name
        )

    class Attributes(Agentic.Attributes):
        context_repository_qualified_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: Context.Attributes = Field(
        default_factory=lambda: Context.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
