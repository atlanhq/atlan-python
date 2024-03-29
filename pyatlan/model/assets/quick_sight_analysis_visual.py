# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField, RelationField

from .quick_sight import QuickSight


class QuickSightAnalysisVisual(QuickSight):
    """Description"""

    type_name: str = Field(default="QuickSightAnalysisVisual", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightAnalysisVisual":
            raise ValueError("must be QuickSightAnalysisVisual")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightAnalysisVisual._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_ANALYSIS_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "quickSightAnalysisQualifiedName",
        "quickSightAnalysisQualifiedName",
        "quickSightAnalysisQualifiedName.text",
    )
    """
    Unique name of the QuickSight analysis in which this visual exists.
    """

    QUICK_SIGHT_ANALYSIS: ClassVar[RelationField] = RelationField("quickSightAnalysis")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "quick_sight_analysis_qualified_name",
        "quick_sight_analysis",
    ]

    @property
    def quick_sight_analysis_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_qualified_name
        )

    @quick_sight_analysis_qualified_name.setter
    def quick_sight_analysis_qualified_name(
        self, quick_sight_analysis_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_qualified_name = (
            quick_sight_analysis_qualified_name
        )

    @property
    def quick_sight_analysis(self) -> Optional[QuickSightAnalysis]:
        return None if self.attributes is None else self.attributes.quick_sight_analysis

    @quick_sight_analysis.setter
    def quick_sight_analysis(self, quick_sight_analysis: Optional[QuickSightAnalysis]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis = quick_sight_analysis

    class Attributes(QuickSight.Attributes):
        quick_sight_analysis_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        quick_sight_analysis: Optional[QuickSightAnalysis] = Field(
            default=None, description=""
        )  # relationship

    attributes: QuickSightAnalysisVisual.Attributes = Field(
        default_factory=lambda: QuickSightAnalysisVisual.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .quick_sight_analysis import QuickSightAnalysis  # noqa
