# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .qlik import Qlik


class QlikColumn(Qlik):
    """Description"""

    type_name: str = Field(default="QlikColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikColumn":
            raise ValueError("must be QlikColumn")
        return v

    def __setattr__(self, name, value):
        if name in QlikColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QLIK_COLUMN_NAME: ClassVar[KeywordField] = KeywordField(
        "qlikColumnName", "qlikColumnName"
    )
    """
    Qlik Column name.
    """
    QLIK_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "qlikDataType", "qlikDataType"
    )
    """
    Data type of the Qlik Column.
    """
    QLIK_COLUMN_TYPE: ClassVar[KeywordField] = KeywordField(
        "qlikColumnType", "qlikColumnType"
    )
    """
    Column type can be: Dimension, Measure or Normal.
    """
    QLIK_PARENT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "qlikParentQualifiedName", "qlikParentQualifiedName"
    )
    """
    Parent Qualified name of column.
    """

    QLIK_SHEET: ClassVar[RelationField] = RelationField("qlikSheet")
    """
    TBC
    """
    QLIK_DATASET: ClassVar[RelationField] = RelationField("qlikDataset")
    """
    TBC
    """
    QLIK_CHART: ClassVar[RelationField] = RelationField("qlikChart")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "qlik_column_name",
        "qlik_data_type",
        "qlik_column_type",
        "qlik_parent_qualified_name",
        "qlik_sheet",
        "qlik_dataset",
        "qlik_chart",
    ]

    @property
    def qlik_column_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_column_name

    @qlik_column_name.setter
    def qlik_column_name(self, qlik_column_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_column_name = qlik_column_name

    @property
    def qlik_data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_data_type

    @qlik_data_type.setter
    def qlik_data_type(self, qlik_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_data_type = qlik_data_type

    @property
    def qlik_column_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_column_type

    @qlik_column_type.setter
    def qlik_column_type(self, qlik_column_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_column_type = qlik_column_type

    @property
    def qlik_parent_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.qlik_parent_qualified_name
        )

    @qlik_parent_qualified_name.setter
    def qlik_parent_qualified_name(self, qlik_parent_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_parent_qualified_name = qlik_parent_qualified_name

    @property
    def qlik_sheet(self) -> Optional[QlikSheet]:
        return None if self.attributes is None else self.attributes.qlik_sheet

    @qlik_sheet.setter
    def qlik_sheet(self, qlik_sheet: Optional[QlikSheet]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_sheet = qlik_sheet

    @property
    def qlik_dataset(self) -> Optional[QlikDataset]:
        return None if self.attributes is None else self.attributes.qlik_dataset

    @qlik_dataset.setter
    def qlik_dataset(self, qlik_dataset: Optional[QlikDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset = qlik_dataset

    @property
    def qlik_chart(self) -> Optional[QlikChart]:
        return None if self.attributes is None else self.attributes.qlik_chart

    @qlik_chart.setter
    def qlik_chart(self, qlik_chart: Optional[QlikChart]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_chart = qlik_chart

    class Attributes(Qlik.Attributes):
        qlik_column_name: Optional[str] = Field(default=None, description="")
        qlik_data_type: Optional[str] = Field(default=None, description="")
        qlik_column_type: Optional[str] = Field(default=None, description="")
        qlik_parent_qualified_name: Optional[str] = Field(default=None, description="")
        qlik_sheet: Optional[QlikSheet] = Field(
            default=None, description=""
        )  # relationship
        qlik_dataset: Optional[QlikDataset] = Field(
            default=None, description=""
        )  # relationship
        qlik_chart: Optional[QlikChart] = Field(
            default=None, description=""
        )  # relationship

    attributes: QlikColumn.Attributes = Field(
        default_factory=lambda: QlikColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .qlik_chart import QlikChart  # noqa: E402, F401
from .qlik_dataset import QlikDataset  # noqa: E402, F401
from .qlik_sheet import QlikSheet  # noqa: E402, F401

QlikColumn.Attributes.update_forward_refs()
