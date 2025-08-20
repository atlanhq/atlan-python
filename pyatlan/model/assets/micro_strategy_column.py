# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .micro_strategy import MicroStrategy


class MicroStrategyColumn(MicroStrategy):
    """Description"""

    type_name: str = Field(default="MicroStrategyColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyColumn":
            raise ValueError("must be MicroStrategyColumn")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MICRO_STRATEGY_COLUMN_ID: ClassVar[KeywordField] = KeywordField(
        "microStrategyColumnId", "microStrategyColumnId"
    )
    """
    Unique identifier of the column in MicroStrategy.
    """
    MICRO_STRATEGY_COLUMN_TYPE: ClassVar[KeywordField] = KeywordField(
        "microStrategyColumnType", "microStrategyColumnType"
    )
    """
    Type of the column (Eg attribute_column, fact_column, metric_column etc).
    """
    MICRO_STRATEGY_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "microStrategyDataType", "microStrategyDataType"
    )
    """
    Data type of the column.
    """
    MICRO_STRATEGY_COLUMN_ATTRIBUTE_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "microStrategyColumnAttributeQualifiedName",
            "microStrategyColumnAttributeQualifiedName.keyword",
            "microStrategyColumnAttributeQualifiedName",
        )
    )
    """
    Unique identifier of the Attribute in which this column exists.
    """
    MICRO_STRATEGY_COLUMN_FACT_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "microStrategyColumnFactQualifiedName",
            "microStrategyColumnFactQualifiedName.keyword",
            "microStrategyColumnFactQualifiedName",
        )
    )
    """
    Unique identifier of the Fact in which this column exists.
    """
    MICRO_STRATEGY_COLUMN_METRIC_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "microStrategyColumnMetricQualifiedName",
            "microStrategyColumnMetricQualifiedName.keyword",
            "microStrategyColumnMetricQualifiedName",
        )
    )
    """
    Unique identifier of the Metric in which this column exists.
    """
    MICRO_STRATEGY_COLUMN_CUBE_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "microStrategyColumnCubeQualifiedName",
            "microStrategyColumnCubeQualifiedName.keyword",
            "microStrategyColumnCubeQualifiedName",
        )
    )
    """
    Unique identifier of the Cube in which this column exists.
    """
    MICRO_STRATEGY_COLUMN_REPORT_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "microStrategyColumnReportQualifiedName",
            "microStrategyColumnReportQualifiedName.keyword",
            "microStrategyColumnReportQualifiedName",
        )
    )
    """
    Unique identifier of the Report in which this column exists.
    """
    MICRO_STRATEGY_COLUMN_DOSSIER_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "microStrategyColumnDossierQualifiedName",
            "microStrategyColumnDossierQualifiedName.keyword",
            "microStrategyColumnDossierQualifiedName",
        )
    )
    """
    Unique identifier of the Dossier in which this column exists.
    """
    MICRO_STRATEGY_COLUMN_DOCUMENT_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "microStrategyColumnDocumentQualifiedName",
            "microStrategyColumnDocumentQualifiedName.keyword",
            "microStrategyColumnDocumentQualifiedName",
        )
    )
    """
    Unique identifier of the Document in which this column exists.
    """
    MICRO_STRATEGY_PARENT_NAME: ClassVar[KeywordField] = KeywordField(
        "microStrategyParentName", "microStrategyParentName"
    )
    """
    Name of the parent asset.
    """
    MICRO_STRATEGY_COLUMN_EXPRESSION: ClassVar[KeywordField] = KeywordField(
        "microStrategyColumnExpression", "microStrategyColumnExpression"
    )
    """
    Expression or formula used to define this column.
    """

    MICRO_STRATEGY_DOSSIER: ClassVar[RelationField] = RelationField(
        "microStrategyDossier"
    )
    """
    TBC
    """
    MICRO_STRATEGY_DOCUMENT: ClassVar[RelationField] = RelationField(
        "microStrategyDocument"
    )
    """
    TBC
    """
    MICRO_STRATEGY_ATTRIBUTE: ClassVar[RelationField] = RelationField(
        "microStrategyAttribute"
    )
    """
    TBC
    """
    MICRO_STRATEGY_REPORT: ClassVar[RelationField] = RelationField(
        "microStrategyReport"
    )
    """
    TBC
    """
    MICRO_STRATEGY_METRIC: ClassVar[RelationField] = RelationField(
        "microStrategyMetric"
    )
    """
    TBC
    """
    MICRO_STRATEGY_CUBE: ClassVar[RelationField] = RelationField("microStrategyCube")
    """
    TBC
    """
    MICRO_STRATEGY_FACT: ClassVar[RelationField] = RelationField("microStrategyFact")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "micro_strategy_column_id",
        "micro_strategy_column_type",
        "micro_strategy_data_type",
        "micro_strategy_column_attribute_qualified_name",
        "micro_strategy_column_fact_qualified_name",
        "micro_strategy_column_metric_qualified_name",
        "micro_strategy_column_cube_qualified_name",
        "micro_strategy_column_report_qualified_name",
        "micro_strategy_column_dossier_qualified_name",
        "micro_strategy_column_document_qualified_name",
        "micro_strategy_parent_name",
        "micro_strategy_column_expression",
        "micro_strategy_dossier",
        "micro_strategy_document",
        "micro_strategy_attribute",
        "micro_strategy_report",
        "micro_strategy_metric",
        "micro_strategy_cube",
        "micro_strategy_fact",
    ]

    @property
    def micro_strategy_column_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_column_id
        )

    @micro_strategy_column_id.setter
    def micro_strategy_column_id(self, micro_strategy_column_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_column_id = micro_strategy_column_id

    @property
    def micro_strategy_column_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_column_type
        )

    @micro_strategy_column_type.setter
    def micro_strategy_column_type(self, micro_strategy_column_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_column_type = micro_strategy_column_type

    @property
    def micro_strategy_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_data_type
        )

    @micro_strategy_data_type.setter
    def micro_strategy_data_type(self, micro_strategy_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_data_type = micro_strategy_data_type

    @property
    def micro_strategy_column_attribute_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_column_attribute_qualified_name
        )

    @micro_strategy_column_attribute_qualified_name.setter
    def micro_strategy_column_attribute_qualified_name(
        self, micro_strategy_column_attribute_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_column_attribute_qualified_name = (
            micro_strategy_column_attribute_qualified_name
        )

    @property
    def micro_strategy_column_fact_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_column_fact_qualified_name
        )

    @micro_strategy_column_fact_qualified_name.setter
    def micro_strategy_column_fact_qualified_name(
        self, micro_strategy_column_fact_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_column_fact_qualified_name = (
            micro_strategy_column_fact_qualified_name
        )

    @property
    def micro_strategy_column_metric_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_column_metric_qualified_name
        )

    @micro_strategy_column_metric_qualified_name.setter
    def micro_strategy_column_metric_qualified_name(
        self, micro_strategy_column_metric_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_column_metric_qualified_name = (
            micro_strategy_column_metric_qualified_name
        )

    @property
    def micro_strategy_column_cube_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_column_cube_qualified_name
        )

    @micro_strategy_column_cube_qualified_name.setter
    def micro_strategy_column_cube_qualified_name(
        self, micro_strategy_column_cube_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_column_cube_qualified_name = (
            micro_strategy_column_cube_qualified_name
        )

    @property
    def micro_strategy_column_report_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_column_report_qualified_name
        )

    @micro_strategy_column_report_qualified_name.setter
    def micro_strategy_column_report_qualified_name(
        self, micro_strategy_column_report_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_column_report_qualified_name = (
            micro_strategy_column_report_qualified_name
        )

    @property
    def micro_strategy_column_dossier_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_column_dossier_qualified_name
        )

    @micro_strategy_column_dossier_qualified_name.setter
    def micro_strategy_column_dossier_qualified_name(
        self, micro_strategy_column_dossier_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_column_dossier_qualified_name = (
            micro_strategy_column_dossier_qualified_name
        )

    @property
    def micro_strategy_column_document_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_column_document_qualified_name
        )

    @micro_strategy_column_document_qualified_name.setter
    def micro_strategy_column_document_qualified_name(
        self, micro_strategy_column_document_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_column_document_qualified_name = (
            micro_strategy_column_document_qualified_name
        )

    @property
    def micro_strategy_parent_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_parent_name
        )

    @micro_strategy_parent_name.setter
    def micro_strategy_parent_name(self, micro_strategy_parent_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_parent_name = micro_strategy_parent_name

    @property
    def micro_strategy_column_expression(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_column_expression
        )

    @micro_strategy_column_expression.setter
    def micro_strategy_column_expression(
        self, micro_strategy_column_expression: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_column_expression = (
            micro_strategy_column_expression
        )

    @property
    def micro_strategy_dossier(self) -> Optional[MicroStrategyDossier]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_dossier
        )

    @micro_strategy_dossier.setter
    def micro_strategy_dossier(
        self, micro_strategy_dossier: Optional[MicroStrategyDossier]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_dossier = micro_strategy_dossier

    @property
    def micro_strategy_document(self) -> Optional[MicroStrategyDocument]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_document
        )

    @micro_strategy_document.setter
    def micro_strategy_document(
        self, micro_strategy_document: Optional[MicroStrategyDocument]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_document = micro_strategy_document

    @property
    def micro_strategy_attribute(self) -> Optional[MicroStrategyAttribute]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attribute
        )

    @micro_strategy_attribute.setter
    def micro_strategy_attribute(
        self, micro_strategy_attribute: Optional[MicroStrategyAttribute]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attribute = micro_strategy_attribute

    @property
    def micro_strategy_report(self) -> Optional[MicroStrategyReport]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_report
        )

    @micro_strategy_report.setter
    def micro_strategy_report(
        self, micro_strategy_report: Optional[MicroStrategyReport]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_report = micro_strategy_report

    @property
    def micro_strategy_metric(self) -> Optional[MicroStrategyMetric]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_metric
        )

    @micro_strategy_metric.setter
    def micro_strategy_metric(
        self, micro_strategy_metric: Optional[MicroStrategyMetric]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric = micro_strategy_metric

    @property
    def micro_strategy_cube(self) -> Optional[MicroStrategyCube]:
        return None if self.attributes is None else self.attributes.micro_strategy_cube

    @micro_strategy_cube.setter
    def micro_strategy_cube(self, micro_strategy_cube: Optional[MicroStrategyCube]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cube = micro_strategy_cube

    @property
    def micro_strategy_fact(self) -> Optional[MicroStrategyFact]:
        return None if self.attributes is None else self.attributes.micro_strategy_fact

    @micro_strategy_fact.setter
    def micro_strategy_fact(self, micro_strategy_fact: Optional[MicroStrategyFact]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_fact = micro_strategy_fact

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_column_id: Optional[str] = Field(default=None, description="")
        micro_strategy_column_type: Optional[str] = Field(default=None, description="")
        micro_strategy_data_type: Optional[str] = Field(default=None, description="")
        micro_strategy_column_attribute_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        micro_strategy_column_fact_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        micro_strategy_column_metric_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        micro_strategy_column_cube_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        micro_strategy_column_report_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        micro_strategy_column_dossier_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        micro_strategy_column_document_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        micro_strategy_parent_name: Optional[str] = Field(default=None, description="")
        micro_strategy_column_expression: Optional[str] = Field(
            default=None, description=""
        )
        micro_strategy_dossier: Optional[MicroStrategyDossier] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_document: Optional[MicroStrategyDocument] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_attribute: Optional[MicroStrategyAttribute] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_report: Optional[MicroStrategyReport] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_metric: Optional[MicroStrategyMetric] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_cube: Optional[MicroStrategyCube] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_fact: Optional[MicroStrategyFact] = Field(
            default=None, description=""
        )  # relationship

    attributes: MicroStrategyColumn.Attributes = Field(
        default_factory=lambda: MicroStrategyColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .micro_strategy_attribute import MicroStrategyAttribute  # noqa: E402, F401
from .micro_strategy_cube import MicroStrategyCube  # noqa: E402, F401
from .micro_strategy_document import MicroStrategyDocument  # noqa: E402, F401
from .micro_strategy_dossier import MicroStrategyDossier  # noqa: E402, F401
from .micro_strategy_fact import MicroStrategyFact  # noqa: E402, F401
from .micro_strategy_metric import MicroStrategyMetric  # noqa: E402, F401
from .micro_strategy_report import MicroStrategyReport  # noqa: E402, F401

MicroStrategyColumn.Attributes.update_forward_refs()
