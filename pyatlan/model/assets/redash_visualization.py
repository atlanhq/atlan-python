# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .redash import Redash


class RedashVisualization(Redash):
    """Description"""

    type_name: str = Field(default="RedashVisualization", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "RedashVisualization":
            raise ValueError("must be RedashVisualization")
        return v

    def __setattr__(self, name, value):
        if name in RedashVisualization._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    REDASH_VISUALIZATION_TYPE: ClassVar[KeywordField] = KeywordField(
        "redashVisualizationType", "redashVisualizationType"
    )
    """
    Type of this visualization.
    """
    REDASH_QUERY_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "redashQueryName", "redashQueryName.keyword", "redashQueryName"
    )
    """
    Simple name of the query from which this visualization is created.
    """
    REDASH_QUERY_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "redashQueryQualifiedName",
        "redashQueryQualifiedName",
        "redashQueryQualifiedName.text",
    )
    """
    Unique name of the query from which this visualization is created.
    """

    REDASH_QUERY: ClassVar[RelationField] = RelationField("redashQuery")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "redash_visualization_type",
        "redash_query_name",
        "redash_query_qualified_name",
        "redash_query",
    ]

    @property
    def redash_visualization_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.redash_visualization_type
        )

    @redash_visualization_type.setter
    def redash_visualization_type(self, redash_visualization_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_visualization_type = redash_visualization_type

    @property
    def redash_query_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.redash_query_name

    @redash_query_name.setter
    def redash_query_name(self, redash_query_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_name = redash_query_name

    @property
    def redash_query_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.redash_query_qualified_name
        )

    @redash_query_qualified_name.setter
    def redash_query_qualified_name(self, redash_query_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_qualified_name = redash_query_qualified_name

    @property
    def redash_query(self) -> Optional[RedashQuery]:
        return None if self.attributes is None else self.attributes.redash_query

    @redash_query.setter
    def redash_query(self, redash_query: Optional[RedashQuery]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query = redash_query

    class Attributes(Redash.Attributes):
        redash_visualization_type: Optional[str] = Field(default=None, description="")
        redash_query_name: Optional[str] = Field(default=None, description="")
        redash_query_qualified_name: Optional[str] = Field(default=None, description="")
        redash_query: Optional[RedashQuery] = Field(
            default=None, description=""
        )  # relationship

    attributes: RedashVisualization.Attributes = Field(
        default_factory=lambda: RedashVisualization.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .redash_query import RedashQuery  # noqa
