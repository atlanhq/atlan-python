# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .power_b_i import PowerBI


class PowerBIPage(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBIPage", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIPage":
            raise ValueError("must be PowerBIPage")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIPage._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    Unique name of the workspace in which this page exists.
    """
    REPORT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "reportQualifiedName", "reportQualifiedName"
    )
    """
    Unique name of the report in which this page exists.
    """

    REPORT: ClassVar[RelationField] = RelationField("report")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "workspace_qualified_name",
        "report_qualified_name",
        "report",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def report_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.report_qualified_name
        )

    @report_qualified_name.setter
    def report_qualified_name(self, report_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_qualified_name = report_qualified_name

    @property
    def report(self) -> Optional[PowerBIReport]:
        return None if self.attributes is None else self.attributes.report

    @report.setter
    def report(self, report: Optional[PowerBIReport]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report = report

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(default=None, description="")
        report_qualified_name: Optional[str] = Field(default=None, description="")
        report: Optional[PowerBIReport] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBIPage.Attributes = Field(
        default_factory=lambda: PowerBIPage.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_report import PowerBIReport  # noqa
