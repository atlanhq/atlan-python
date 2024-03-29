# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)

from .mode import Mode


class ModeReport(Mode):
    """Description"""

    type_name: str = Field(default="ModeReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeReport":
            raise ValueError("must be ModeReport")
        return v

    def __setattr__(self, name, value):
        if name in ModeReport._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODE_COLLECTION_TOKEN: ClassVar[KeywordField] = KeywordField(
        "modeCollectionToken", "modeCollectionToken"
    )
    """

    """
    MODE_REPORT_PUBLISHED_AT: ClassVar[NumericField] = NumericField(
        "modeReportPublishedAt", "modeReportPublishedAt"
    )
    """

    """
    MODE_QUERY_COUNT: ClassVar[NumericField] = NumericField(
        "modeQueryCount", "modeQueryCount"
    )
    """

    """
    MODE_CHART_COUNT: ClassVar[NumericField] = NumericField(
        "modeChartCount", "modeChartCount"
    )
    """

    """
    MODE_QUERY_PREVIEW: ClassVar[TextField] = TextField(
        "modeQueryPreview", "modeQueryPreview"
    )
    """

    """
    MODE_IS_PUBLIC: ClassVar[BooleanField] = BooleanField(
        "modeIsPublic", "modeIsPublic"
    )
    """

    """
    MODE_IS_SHARED: ClassVar[BooleanField] = BooleanField(
        "modeIsShared", "modeIsShared"
    )
    """

    """

    MODE_QUERIES: ClassVar[RelationField] = RelationField("modeQueries")
    """
    TBC
    """
    MODE_COLLECTIONS: ClassVar[RelationField] = RelationField("modeCollections")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "mode_collection_token",
        "mode_report_published_at",
        "mode_query_count",
        "mode_chart_count",
        "mode_query_preview",
        "mode_is_public",
        "mode_is_shared",
        "mode_queries",
        "mode_collections",
    ]

    @property
    def mode_collection_token(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.mode_collection_token
        )

    @mode_collection_token.setter
    def mode_collection_token(self, mode_collection_token: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_token = mode_collection_token

    @property
    def mode_report_published_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.mode_report_published_at
        )

    @mode_report_published_at.setter
    def mode_report_published_at(self, mode_report_published_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report_published_at = mode_report_published_at

    @property
    def mode_query_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.mode_query_count

    @mode_query_count.setter
    def mode_query_count(self, mode_query_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_count = mode_query_count

    @property
    def mode_chart_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.mode_chart_count

    @mode_chart_count.setter
    def mode_chart_count(self, mode_chart_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_chart_count = mode_chart_count

    @property
    def mode_query_preview(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_query_preview

    @mode_query_preview.setter
    def mode_query_preview(self, mode_query_preview: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_preview = mode_query_preview

    @property
    def mode_is_public(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.mode_is_public

    @mode_is_public.setter
    def mode_is_public(self, mode_is_public: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_is_public = mode_is_public

    @property
    def mode_is_shared(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.mode_is_shared

    @mode_is_shared.setter
    def mode_is_shared(self, mode_is_shared: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_is_shared = mode_is_shared

    @property
    def mode_queries(self) -> Optional[List[ModeQuery]]:
        return None if self.attributes is None else self.attributes.mode_queries

    @mode_queries.setter
    def mode_queries(self, mode_queries: Optional[List[ModeQuery]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_queries = mode_queries

    @property
    def mode_collections(self) -> Optional[List[ModeCollection]]:
        return None if self.attributes is None else self.attributes.mode_collections

    @mode_collections.setter
    def mode_collections(self, mode_collections: Optional[List[ModeCollection]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collections = mode_collections

    class Attributes(Mode.Attributes):
        mode_collection_token: Optional[str] = Field(default=None, description="")
        mode_report_published_at: Optional[datetime] = Field(
            default=None, description=""
        )
        mode_query_count: Optional[int] = Field(default=None, description="")
        mode_chart_count: Optional[int] = Field(default=None, description="")
        mode_query_preview: Optional[str] = Field(default=None, description="")
        mode_is_public: Optional[bool] = Field(default=None, description="")
        mode_is_shared: Optional[bool] = Field(default=None, description="")
        mode_queries: Optional[List[ModeQuery]] = Field(
            default=None, description=""
        )  # relationship
        mode_collections: Optional[List[ModeCollection]] = Field(
            default=None, description=""
        )  # relationship

    attributes: ModeReport.Attributes = Field(
        default_factory=lambda: ModeReport.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .mode_collection import ModeCollection  # noqa
from .mode_query import ModeQuery  # noqa
