# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, RelationField

from .qlik import Qlik


class QlikSheet(Qlik):
    """Description"""

    type_name: str = Field(default="QlikSheet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikSheet":
            raise ValueError("must be QlikSheet")
        return v

    def __setattr__(self, name, value):
        if name in QlikSheet._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QLIK_SHEET_IS_APPROVED: ClassVar[BooleanField] = BooleanField(
        "qlikSheetIsApproved", "qlikSheetIsApproved"
    )
    """
    Whether this is approved (true) or not (false).
    """

    QLIK_APP: ClassVar[RelationField] = RelationField("qlikApp")
    """
    TBC
    """
    QLIK_CHARTS: ClassVar[RelationField] = RelationField("qlikCharts")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "qlik_sheet_is_approved",
        "qlik_app",
        "qlik_charts",
    ]

    @property
    def qlik_sheet_is_approved(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.qlik_sheet_is_approved
        )

    @qlik_sheet_is_approved.setter
    def qlik_sheet_is_approved(self, qlik_sheet_is_approved: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_sheet_is_approved = qlik_sheet_is_approved

    @property
    def qlik_app(self) -> Optional[QlikApp]:
        return None if self.attributes is None else self.attributes.qlik_app

    @qlik_app.setter
    def qlik_app(self, qlik_app: Optional[QlikApp]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_app = qlik_app

    @property
    def qlik_charts(self) -> Optional[List[QlikChart]]:
        return None if self.attributes is None else self.attributes.qlik_charts

    @qlik_charts.setter
    def qlik_charts(self, qlik_charts: Optional[List[QlikChart]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_charts = qlik_charts

    class Attributes(Qlik.Attributes):
        qlik_sheet_is_approved: Optional[bool] = Field(default=None, description="")
        qlik_app: Optional[QlikApp] = Field(
            default=None, description=""
        )  # relationship
        qlik_charts: Optional[List[QlikChart]] = Field(
            default=None, description=""
        )  # relationship

    attributes: QlikSheet.Attributes = Field(
        default_factory=lambda: QlikSheet.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .qlik_app import QlikApp  # noqa
from .qlik_chart import QlikChart  # noqa
