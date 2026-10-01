# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    RelationField,
    TextField,
)

from .fabric import Fabric


class FabricSemanticModelMeasure(Fabric):
    """Description"""

    type_name: str = Field(default="FabricSemanticModelMeasure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FabricSemanticModelMeasure":
            raise ValueError("must be FabricSemanticModelMeasure")
        return v

    def __setattr__(self, name, value):
        if name in FabricSemanticModelMeasure._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FABRIC_SEMANTIC_MODEL_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "fabricSemanticModelQualifiedName", "fabricSemanticModelQualifiedName"
    )
    """
    Unique name of the Fabric semantic model that contains this asset.
    """
    FABRIC_SEMANTIC_MODEL_TABLE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "fabricSemanticModelTableQualifiedName", "fabricSemanticModelTableQualifiedName"
    )
    """
    Unique name of the Fabric semantic model table that contains this asset.
    """
    FABRIC_SEMANTIC_MODEL_TABLE_NAME: ClassVar[KeywordField] = KeywordField(
        "fabricSemanticModelTableName", "fabricSemanticModelTableName"
    )
    """
    Name of the Fabric semantic model table that contains this asset.
    """
    FABRIC_MEASURE_EXPRESSION: ClassVar[TextField] = TextField(
        "fabricMeasureExpression", "fabricMeasureExpression"
    )
    """
    DAX expression for this measure.
    """
    FABRIC_FORMAT_STRING: ClassVar[KeywordField] = KeywordField(
        "fabricFormatString", "fabricFormatString"
    )
    """
    Format string applied to the values of this measure.
    """
    FABRIC_DISPLAY_FOLDER: ClassVar[KeywordField] = KeywordField(
        "fabricDisplayFolder", "fabricDisplayFolder"
    )
    """
    Display folder in which this measure is grouped within its table.
    """
    FABRIC_IS_HIDDEN: ClassVar[BooleanField] = BooleanField(
        "fabricIsHidden", "fabricIsHidden"
    )
    """
    Whether this measure is hidden in the semantic model (true) or visible (false).
    """
    FABRIC_IS_EXTERNAL_MEASURE: ClassVar[BooleanField] = BooleanField(
        "fabricIsExternalMeasure", "fabricIsExternalMeasure"
    )
    """
    Whether this measure is an external measure (true) or defined within the semantic model (false).
    """

    FABRIC_SEMANTIC_MODEL_TABLE_COLUMNS: ClassVar[RelationField] = RelationField(
        "fabricSemanticModelTableColumns"
    )
    """
    TBC
    """
    FABRIC_SEMANTIC_MODEL_TABLE: ClassVar[RelationField] = RelationField(
        "fabricSemanticModelTable"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "fabric_semantic_model_qualified_name",
        "fabric_semantic_model_table_qualified_name",
        "fabric_semantic_model_table_name",
        "fabric_measure_expression",
        "fabric_format_string",
        "fabric_display_folder",
        "fabric_is_hidden",
        "fabric_is_external_measure",
        "fabric_semantic_model_table_columns",
        "fabric_semantic_model_table",
    ]

    @property
    def fabric_semantic_model_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fabric_semantic_model_qualified_name
        )

    @fabric_semantic_model_qualified_name.setter
    def fabric_semantic_model_qualified_name(
        self, fabric_semantic_model_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_semantic_model_qualified_name = (
            fabric_semantic_model_qualified_name
        )

    @property
    def fabric_semantic_model_table_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fabric_semantic_model_table_qualified_name
        )

    @fabric_semantic_model_table_qualified_name.setter
    def fabric_semantic_model_table_qualified_name(
        self, fabric_semantic_model_table_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_semantic_model_table_qualified_name = (
            fabric_semantic_model_table_qualified_name
        )

    @property
    def fabric_semantic_model_table_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fabric_semantic_model_table_name
        )

    @fabric_semantic_model_table_name.setter
    def fabric_semantic_model_table_name(
        self, fabric_semantic_model_table_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_semantic_model_table_name = (
            fabric_semantic_model_table_name
        )

    @property
    def fabric_measure_expression(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fabric_measure_expression
        )

    @fabric_measure_expression.setter
    def fabric_measure_expression(self, fabric_measure_expression: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_measure_expression = fabric_measure_expression

    @property
    def fabric_format_string(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.fabric_format_string

    @fabric_format_string.setter
    def fabric_format_string(self, fabric_format_string: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_format_string = fabric_format_string

    @property
    def fabric_display_folder(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.fabric_display_folder
        )

    @fabric_display_folder.setter
    def fabric_display_folder(self, fabric_display_folder: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_display_folder = fabric_display_folder

    @property
    def fabric_is_hidden(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.fabric_is_hidden

    @fabric_is_hidden.setter
    def fabric_is_hidden(self, fabric_is_hidden: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_is_hidden = fabric_is_hidden

    @property
    def fabric_is_external_measure(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.fabric_is_external_measure
        )

    @fabric_is_external_measure.setter
    def fabric_is_external_measure(self, fabric_is_external_measure: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_is_external_measure = fabric_is_external_measure

    @property
    def fabric_semantic_model_table_columns(
        self,
    ) -> Optional[List[FabricSemanticModelTableColumn]]:
        return (
            None
            if self.attributes is None
            else self.attributes.fabric_semantic_model_table_columns
        )

    @fabric_semantic_model_table_columns.setter
    def fabric_semantic_model_table_columns(
        self,
        fabric_semantic_model_table_columns: Optional[
            List[FabricSemanticModelTableColumn]
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_semantic_model_table_columns = (
            fabric_semantic_model_table_columns
        )

    @property
    def fabric_semantic_model_table(self) -> Optional[FabricSemanticModelTable]:
        return (
            None
            if self.attributes is None
            else self.attributes.fabric_semantic_model_table
        )

    @fabric_semantic_model_table.setter
    def fabric_semantic_model_table(
        self, fabric_semantic_model_table: Optional[FabricSemanticModelTable]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_semantic_model_table = fabric_semantic_model_table

    class Attributes(Fabric.Attributes):
        fabric_semantic_model_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        fabric_semantic_model_table_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        fabric_semantic_model_table_name: Optional[str] = Field(
            default=None, description=""
        )
        fabric_measure_expression: Optional[str] = Field(default=None, description="")
        fabric_format_string: Optional[str] = Field(default=None, description="")
        fabric_display_folder: Optional[str] = Field(default=None, description="")
        fabric_is_hidden: Optional[bool] = Field(default=None, description="")
        fabric_is_external_measure: Optional[bool] = Field(default=None, description="")
        fabric_semantic_model_table_columns: Optional[
            List[FabricSemanticModelTableColumn]
        ] = Field(default=None, description="")  # relationship
        fabric_semantic_model_table: Optional[FabricSemanticModelTable] = Field(
            default=None, description=""
        )  # relationship

    attributes: FabricSemanticModelMeasure.Attributes = Field(
        default_factory=lambda: FabricSemanticModelMeasure.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .fabric_semantic_model_table import FabricSemanticModelTable  # noqa: E402, F401
from .fabric_semantic_model_table_column import (
    FabricSemanticModelTableColumn,  # noqa: E402, F401
)
