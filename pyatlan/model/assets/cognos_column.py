# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .cognos import Cognos


class CognosColumn(Cognos):
    """Description"""

    type_name: str = Field(default="CognosColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CognosColumn":
            raise ValueError("must be CognosColumn")
        return v

    def __setattr__(self, name, value):
        if name in CognosColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COGNOS_COLUMN_DATATYPE: ClassVar[KeywordField] = KeywordField(
        "cognosColumnDatatype", "cognosColumnDatatype"
    )
    """
    Data type of the CognosColumn.
    """
    COGNOS_COLUMN_NULLABLE: ClassVar[KeywordField] = KeywordField(
        "cognosColumnNullable", "cognosColumnNullable"
    )
    """
    Whether the CognosColumn is nullable.
    """
    COGNOS_COLUMN_REGULAR_AGGREGATE: ClassVar[KeywordField] = KeywordField(
        "cognosColumnRegularAggregate", "cognosColumnRegularAggregate"
    )
    """
    How data should be summarized when aggregated across different dimensions or groupings.
    """

    COGNOS_MODULE: ClassVar[RelationField] = RelationField("cognosModule")
    """
    TBC
    """
    COGNOS_DATASET: ClassVar[RelationField] = RelationField("cognosDataset")
    """
    TBC
    """
    COGNOS_EXPLORATION: ClassVar[RelationField] = RelationField("cognosExploration")
    """
    TBC
    """
    COGNOS_DASHBOARD: ClassVar[RelationField] = RelationField("cognosDashboard")
    """
    TBC
    """
    COGNOS_FILE: ClassVar[RelationField] = RelationField("cognosFile")
    """
    TBC
    """
    COGNOS_PACKAGE: ClassVar[RelationField] = RelationField("cognosPackage")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cognos_column_datatype",
        "cognos_column_nullable",
        "cognos_column_regular_aggregate",
        "cognos_module",
        "cognos_dataset",
        "cognos_exploration",
        "cognos_dashboard",
        "cognos_file",
        "cognos_package",
    ]

    @property
    def cognos_column_datatype(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.cognos_column_datatype
        )

    @cognos_column_datatype.setter
    def cognos_column_datatype(self, cognos_column_datatype: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_column_datatype = cognos_column_datatype

    @property
    def cognos_column_nullable(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.cognos_column_nullable
        )

    @cognos_column_nullable.setter
    def cognos_column_nullable(self, cognos_column_nullable: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_column_nullable = cognos_column_nullable

    @property
    def cognos_column_regular_aggregate(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cognos_column_regular_aggregate
        )

    @cognos_column_regular_aggregate.setter
    def cognos_column_regular_aggregate(
        self, cognos_column_regular_aggregate: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_column_regular_aggregate = (
            cognos_column_regular_aggregate
        )

    @property
    def cognos_module(self) -> Optional[CognosModule]:
        return None if self.attributes is None else self.attributes.cognos_module

    @cognos_module.setter
    def cognos_module(self, cognos_module: Optional[CognosModule]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_module = cognos_module

    @property
    def cognos_dataset(self) -> Optional[CognosDataset]:
        return None if self.attributes is None else self.attributes.cognos_dataset

    @cognos_dataset.setter
    def cognos_dataset(self, cognos_dataset: Optional[CognosDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_dataset = cognos_dataset

    @property
    def cognos_exploration(self) -> Optional[CognosExploration]:
        return None if self.attributes is None else self.attributes.cognos_exploration

    @cognos_exploration.setter
    def cognos_exploration(self, cognos_exploration: Optional[CognosExploration]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_exploration = cognos_exploration

    @property
    def cognos_dashboard(self) -> Optional[CognosDashboard]:
        return None if self.attributes is None else self.attributes.cognos_dashboard

    @cognos_dashboard.setter
    def cognos_dashboard(self, cognos_dashboard: Optional[CognosDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_dashboard = cognos_dashboard

    @property
    def cognos_file(self) -> Optional[CognosFile]:
        return None if self.attributes is None else self.attributes.cognos_file

    @cognos_file.setter
    def cognos_file(self, cognos_file: Optional[CognosFile]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_file = cognos_file

    @property
    def cognos_package(self) -> Optional[CognosPackage]:
        return None if self.attributes is None else self.attributes.cognos_package

    @cognos_package.setter
    def cognos_package(self, cognos_package: Optional[CognosPackage]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_package = cognos_package

    class Attributes(Cognos.Attributes):
        cognos_column_datatype: Optional[str] = Field(default=None, description="")
        cognos_column_nullable: Optional[str] = Field(default=None, description="")
        cognos_column_regular_aggregate: Optional[str] = Field(
            default=None, description=""
        )
        cognos_module: Optional[CognosModule] = Field(
            default=None, description=""
        )  # relationship
        cognos_dataset: Optional[CognosDataset] = Field(
            default=None, description=""
        )  # relationship
        cognos_exploration: Optional[CognosExploration] = Field(
            default=None, description=""
        )  # relationship
        cognos_dashboard: Optional[CognosDashboard] = Field(
            default=None, description=""
        )  # relationship
        cognos_file: Optional[CognosFile] = Field(
            default=None, description=""
        )  # relationship
        cognos_package: Optional[CognosPackage] = Field(
            default=None, description=""
        )  # relationship

    attributes: CognosColumn.Attributes = Field(
        default_factory=lambda: CognosColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cognos_dashboard import CognosDashboard  # noqa: E402, F401
from .cognos_dataset import CognosDataset  # noqa: E402, F401
from .cognos_exploration import CognosExploration  # noqa: E402, F401
from .cognos_file import CognosFile  # noqa: E402, F401
from .cognos_module import CognosModule  # noqa: E402, F401
from .cognos_package import CognosPackage  # noqa: E402, F401

CognosColumn.Attributes.update_forward_refs()
