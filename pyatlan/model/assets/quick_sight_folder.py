# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType, QuickSightFolderType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .quick_sight import QuickSight


class QuickSightFolder(QuickSight):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        quick_sight_id: str,
    ) -> QuickSightFolder: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        quick_sight_id: str,
        quick_sight_folder_type: QuickSightFolderType,
    ) -> QuickSightFolder: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        quick_sight_id: str,
        quick_sight_folder_type: Optional[QuickSightFolderType] = None,
    ) -> QuickSightFolder:
        validate_required_fields(
            ["name", "connection_qualified_name", "quick_sight_id"],
            [name, connection_qualified_name, quick_sight_id],
        )
        attributes = QuickSightFolder.Attributes.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            quick_sight_id=quick_sight_id,
            quick_sight_folder_type=quick_sight_folder_type,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="QuickSightFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightFolder":
            raise ValueError("must be QuickSightFolder")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightFolder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_FOLDER_TYPE: ClassVar[KeywordField] = KeywordField(
        "quickSightFolderType", "quickSightFolderType"
    )
    """
    Type of this folder, for example: SHARED.
    """
    QUICK_SIGHT_FOLDER_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "quickSightFolderHierarchy", "quickSightFolderHierarchy"
    )
    """
    Detailed path of this folder.
    """

    QUICK_SIGHT_ANALYSES: ClassVar[RelationField] = RelationField("quickSightAnalyses")
    """
    TBC
    """
    QUICK_SIGHT_DASHBOARDS: ClassVar[RelationField] = RelationField(
        "quickSightDashboards"
    )
    """
    TBC
    """
    QUICK_SIGHT_DATASETS: ClassVar[RelationField] = RelationField("quickSightDatasets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "quick_sight_folder_type",
        "quick_sight_folder_hierarchy",
        "quick_sight_analyses",
        "quick_sight_dashboards",
        "quick_sight_datasets",
    ]

    @property
    def quick_sight_folder_type(self) -> Optional[QuickSightFolderType]:
        return (
            None if self.attributes is None else self.attributes.quick_sight_folder_type
        )

    @quick_sight_folder_type.setter
    def quick_sight_folder_type(
        self, quick_sight_folder_type: Optional[QuickSightFolderType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_folder_type = quick_sight_folder_type

    @property
    def quick_sight_folder_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_folder_hierarchy
        )

    @quick_sight_folder_hierarchy.setter
    def quick_sight_folder_hierarchy(
        self, quick_sight_folder_hierarchy: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_folder_hierarchy = quick_sight_folder_hierarchy

    @property
    def quick_sight_analyses(self) -> Optional[List[QuickSightAnalysis]]:
        return None if self.attributes is None else self.attributes.quick_sight_analyses

    @quick_sight_analyses.setter
    def quick_sight_analyses(
        self, quick_sight_analyses: Optional[List[QuickSightAnalysis]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analyses = quick_sight_analyses

    @property
    def quick_sight_dashboards(self) -> Optional[List[QuickSightDashboard]]:
        return (
            None if self.attributes is None else self.attributes.quick_sight_dashboards
        )

    @quick_sight_dashboards.setter
    def quick_sight_dashboards(
        self, quick_sight_dashboards: Optional[List[QuickSightDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboards = quick_sight_dashboards

    @property
    def quick_sight_datasets(self) -> Optional[List[QuickSightDataset]]:
        return None if self.attributes is None else self.attributes.quick_sight_datasets

    @quick_sight_datasets.setter
    def quick_sight_datasets(
        self, quick_sight_datasets: Optional[List[QuickSightDataset]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_datasets = quick_sight_datasets

    class Attributes(QuickSight.Attributes):
        quick_sight_folder_type: Optional[QuickSightFolderType] = Field(
            default=None, description=""
        )
        quick_sight_folder_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        quick_sight_analyses: Optional[List[QuickSightAnalysis]] = Field(
            default=None, description=""
        )  # relationship
        quick_sight_dashboards: Optional[List[QuickSightDashboard]] = Field(
            default=None, description=""
        )  # relationship
        quick_sight_datasets: Optional[List[QuickSightDataset]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            connection_qualified_name: str,
            quick_sight_id: str,
            quick_sight_folder_type: Optional[QuickSightFolderType] = None,
        ) -> QuickSightFolder.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name", "quick_sight_id"],
                [name, connection_qualified_name, quick_sight_id],
            )
            return QuickSightFolder.Attributes(
                name=name,
                quick_sight_id=quick_sight_id,
                qualified_name=f"{connection_qualified_name}/{quick_sight_id}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
                quick_sight_folder_type=quick_sight_folder_type,
            )

    attributes: QuickSightFolder.Attributes = Field(
        default_factory=lambda: QuickSightFolder.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .quick_sight_analysis import QuickSightAnalysis  # noqa: E402, F401
from .quick_sight_dashboard import QuickSightDashboard  # noqa: E402, F401
from .quick_sight_dataset import QuickSightDataset  # noqa: E402, F401

QuickSightFolder.Attributes.update_forward_refs()
