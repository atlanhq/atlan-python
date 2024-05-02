# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import QuickSightAnalysisStatus
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .quick_sight import QuickSight


class QuickSightAnalysis(QuickSight):
    """Description"""

    type_name: str = Field(default="QuickSightAnalysis", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightAnalysis":
            raise ValueError("must be QuickSightAnalysis")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightAnalysis._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_ANALYSIS_STATUS: ClassVar[KeywordField] = KeywordField(
        "quickSightAnalysisStatus", "quickSightAnalysisStatus"
    )
    """
    Status of this analysis, for example: CREATION_IN_PROGRESS, UPDATE_SUCCESSFUL, etc.
    """
    QUICK_SIGHT_ANALYSIS_CALCULATED_FIELDS: ClassVar[KeywordField] = KeywordField(
        "quickSightAnalysisCalculatedFields", "quickSightAnalysisCalculatedFields"
    )
    """
    List of field names calculated by this analysis.
    """
    QUICK_SIGHT_ANALYSIS_PARAMETER_DECLARATIONS: ClassVar[KeywordField] = KeywordField(
        "quickSightAnalysisParameterDeclarations",
        "quickSightAnalysisParameterDeclarations",
    )
    """
    List of parameters used for this analysis.
    """
    QUICK_SIGHT_ANALYSIS_FILTER_GROUPS: ClassVar[KeywordField] = KeywordField(
        "quickSightAnalysisFilterGroups", "quickSightAnalysisFilterGroups"
    )
    """
    List of filter groups used for this analysis.
    """

    QUICK_SIGHT_ANALYSIS_VISUALS: ClassVar[RelationField] = RelationField(
        "quickSightAnalysisVisuals"
    )
    """
    TBC
    """
    QUICK_SIGHT_ANALYSIS_FOLDERS: ClassVar[RelationField] = RelationField(
        "quickSightAnalysisFolders"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "quick_sight_analysis_status",
        "quick_sight_analysis_calculated_fields",
        "quick_sight_analysis_parameter_declarations",
        "quick_sight_analysis_filter_groups",
        "quick_sight_analysis_visuals",
        "quick_sight_analysis_folders",
    ]

    @property
    def quick_sight_analysis_status(self) -> Optional[QuickSightAnalysisStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_status
        )

    @quick_sight_analysis_status.setter
    def quick_sight_analysis_status(
        self, quick_sight_analysis_status: Optional[QuickSightAnalysisStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_status = quick_sight_analysis_status

    @property
    def quick_sight_analysis_calculated_fields(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_calculated_fields
        )

    @quick_sight_analysis_calculated_fields.setter
    def quick_sight_analysis_calculated_fields(
        self, quick_sight_analysis_calculated_fields: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_calculated_fields = (
            quick_sight_analysis_calculated_fields
        )

    @property
    def quick_sight_analysis_parameter_declarations(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_parameter_declarations
        )

    @quick_sight_analysis_parameter_declarations.setter
    def quick_sight_analysis_parameter_declarations(
        self, quick_sight_analysis_parameter_declarations: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_parameter_declarations = (
            quick_sight_analysis_parameter_declarations
        )

    @property
    def quick_sight_analysis_filter_groups(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_filter_groups
        )

    @quick_sight_analysis_filter_groups.setter
    def quick_sight_analysis_filter_groups(
        self, quick_sight_analysis_filter_groups: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_filter_groups = (
            quick_sight_analysis_filter_groups
        )

    @property
    def quick_sight_analysis_visuals(self) -> Optional[List[QuickSightAnalysisVisual]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_visuals
        )

    @quick_sight_analysis_visuals.setter
    def quick_sight_analysis_visuals(
        self, quick_sight_analysis_visuals: Optional[List[QuickSightAnalysisVisual]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_visuals = quick_sight_analysis_visuals

    @property
    def quick_sight_analysis_folders(self) -> Optional[List[QuickSightFolder]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_folders
        )

    @quick_sight_analysis_folders.setter
    def quick_sight_analysis_folders(
        self, quick_sight_analysis_folders: Optional[List[QuickSightFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_folders = quick_sight_analysis_folders

    class Attributes(QuickSight.Attributes):
        quick_sight_analysis_status: Optional[QuickSightAnalysisStatus] = Field(
            default=None, description=""
        )
        quick_sight_analysis_calculated_fields: Optional[Set[str]] = Field(
            default=None, description=""
        )
        quick_sight_analysis_parameter_declarations: Optional[Set[str]] = Field(
            default=None, description=""
        )
        quick_sight_analysis_filter_groups: Optional[Set[str]] = Field(
            default=None, description=""
        )
        quick_sight_analysis_visuals: Optional[List[QuickSightAnalysisVisual]] = Field(
            default=None, description=""
        )  # relationship
        quick_sight_analysis_folders: Optional[List[QuickSightFolder]] = Field(
            default=None, description=""
        )  # relationship

    attributes: QuickSightAnalysis.Attributes = Field(
        default_factory=lambda: QuickSightAnalysis.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .quick_sight_analysis_visual import QuickSightAnalysisVisual  # noqa
from .quick_sight_folder import QuickSightFolder  # noqa
