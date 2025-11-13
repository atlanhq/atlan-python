# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .fabric import Fabric


class FabricPage(Fabric):
    """Description"""

    type_name: str = Field(default="FabricPage", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FabricPage":
            raise ValueError("must be FabricPage")
        return v

    def __setattr__(self, name, value):
        if name in FabricPage._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FABRIC_REPORT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "fabricReportQualifiedName", "fabricReportQualifiedName"
    )
    """
    Unique name of the Fabric report that contains this asset.
    """

    FABRIC_REPORT: ClassVar[RelationField] = RelationField("fabricReport")
    """
    TBC
    """
    FABRIC_VISUALS: ClassVar[RelationField] = RelationField("fabricVisuals")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "fabric_report_qualified_name",
        "fabric_report",
        "fabric_visuals",
    ]

    @property
    def fabric_report_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fabric_report_qualified_name
        )

    @fabric_report_qualified_name.setter
    def fabric_report_qualified_name(self, fabric_report_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_report_qualified_name = fabric_report_qualified_name

    @property
    def fabric_report(self) -> Optional[FabricReport]:
        return None if self.attributes is None else self.attributes.fabric_report

    @fabric_report.setter
    def fabric_report(self, fabric_report: Optional[FabricReport]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_report = fabric_report

    @property
    def fabric_visuals(self) -> Optional[List[FabricVisual]]:
        return None if self.attributes is None else self.attributes.fabric_visuals

    @fabric_visuals.setter
    def fabric_visuals(self, fabric_visuals: Optional[List[FabricVisual]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_visuals = fabric_visuals

    class Attributes(Fabric.Attributes):
        fabric_report_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        fabric_report: Optional[FabricReport] = Field(
            default=None, description=""
        )  # relationship
        fabric_visuals: Optional[List[FabricVisual]] = Field(
            default=None, description=""
        )  # relationship

    attributes: FabricPage.Attributes = Field(
        default_factory=lambda: FabricPage.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .fabric_report import FabricReport  # noqa: E402, F401
from .fabric_visual import FabricVisual  # noqa: E402, F401
