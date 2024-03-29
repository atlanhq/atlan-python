# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordTextField,
    NumericField,
    RelationField,
)

from .metabase import Metabase


class MetabaseQuestion(Metabase):
    """Description"""

    type_name: str = Field(default="MetabaseQuestion", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MetabaseQuestion":
            raise ValueError("must be MetabaseQuestion")
        return v

    def __setattr__(self, name, value):
        if name in MetabaseQuestion._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    METABASE_DASHBOARD_COUNT: ClassVar[NumericField] = NumericField(
        "metabaseDashboardCount", "metabaseDashboardCount"
    )
    """

    """
    METABASE_QUERY_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "metabaseQueryType", "metabaseQueryType", "metabaseQueryType.text"
    )
    """

    """
    METABASE_QUERY: ClassVar[KeywordTextField] = KeywordTextField(
        "metabaseQuery", "metabaseQuery.keyword", "metabaseQuery"
    )
    """

    """

    METABASE_DASHBOARDS: ClassVar[RelationField] = RelationField("metabaseDashboards")
    """
    TBC
    """
    METABASE_COLLECTION: ClassVar[RelationField] = RelationField("metabaseCollection")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "metabase_dashboard_count",
        "metabase_query_type",
        "metabase_query",
        "metabase_dashboards",
        "metabase_collection",
    ]

    @property
    def metabase_dashboard_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.metabase_dashboard_count
        )

    @metabase_dashboard_count.setter
    def metabase_dashboard_count(self, metabase_dashboard_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_dashboard_count = metabase_dashboard_count

    @property
    def metabase_query_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_query_type

    @metabase_query_type.setter
    def metabase_query_type(self, metabase_query_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_query_type = metabase_query_type

    @property
    def metabase_query(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_query

    @metabase_query.setter
    def metabase_query(self, metabase_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_query = metabase_query

    @property
    def metabase_dashboards(self) -> Optional[List[MetabaseDashboard]]:
        return None if self.attributes is None else self.attributes.metabase_dashboards

    @metabase_dashboards.setter
    def metabase_dashboards(
        self, metabase_dashboards: Optional[List[MetabaseDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_dashboards = metabase_dashboards

    @property
    def metabase_collection(self) -> Optional[MetabaseCollection]:
        return None if self.attributes is None else self.attributes.metabase_collection

    @metabase_collection.setter
    def metabase_collection(self, metabase_collection: Optional[MetabaseCollection]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_collection = metabase_collection

    class Attributes(Metabase.Attributes):
        metabase_dashboard_count: Optional[int] = Field(default=None, description="")
        metabase_query_type: Optional[str] = Field(default=None, description="")
        metabase_query: Optional[str] = Field(default=None, description="")
        metabase_dashboards: Optional[List[MetabaseDashboard]] = Field(
            default=None, description=""
        )  # relationship
        metabase_collection: Optional[MetabaseCollection] = Field(
            default=None, description=""
        )  # relationship

    attributes: MetabaseQuestion.Attributes = Field(
        default_factory=lambda: MetabaseQuestion.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .metabase_collection import MetabaseCollection  # noqa
from .metabase_dashboard import MetabaseDashboard  # noqa
