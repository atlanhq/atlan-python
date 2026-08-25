# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField
from pyatlan.model.structs import TableauReadCountWindow

from .core.b_i import BI


class Tableau(BI):
    """Description"""

    type_name: str = Field(default="Tableau", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Tableau":
            raise ValueError("must be Tableau")
        return v

    def __setattr__(self, name, value):
        if name in Tableau._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    TABLEAU_PROJECT_HIERARCHY_QUALIFIED_NAMES: ClassVar[KeywordField] = KeywordField(
        "tableauProjectHierarchyQualifiedNames", "tableauProjectHierarchyQualifiedNames"
    )
    """
    Array of qualified names representing the project hierarchy for this Tableau asset.
    """
    TABLEAU_SOURCE_READ_COUNTS: ClassVar[KeywordField] = KeywordField(
        "tableauSourceReadCounts", "tableauSourceReadCounts"
    )
    """
    Read/view counts on this asset bucketed by time window, as reported by Tableau's Content Exploration API.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "tableau_project_hierarchy_qualified_names",
        "tableau_source_read_counts",
    ]

    @property
    def tableau_project_hierarchy_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_project_hierarchy_qualified_names
        )

    @tableau_project_hierarchy_qualified_names.setter
    def tableau_project_hierarchy_qualified_names(
        self, tableau_project_hierarchy_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_project_hierarchy_qualified_names = (
            tableau_project_hierarchy_qualified_names
        )

    @property
    def tableau_source_read_counts(self) -> Optional[List[TableauReadCountWindow]]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_source_read_counts
        )

    @tableau_source_read_counts.setter
    def tableau_source_read_counts(
        self, tableau_source_read_counts: Optional[List[TableauReadCountWindow]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_source_read_counts = tableau_source_read_counts

    class Attributes(BI.Attributes):
        tableau_project_hierarchy_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        tableau_source_read_counts: Optional[List[TableauReadCountWindow]] = Field(
            default=None, description=""
        )

    attributes: Tableau.Attributes = Field(
        default_factory=lambda: Tableau.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Tableau.Attributes.update_forward_refs()
