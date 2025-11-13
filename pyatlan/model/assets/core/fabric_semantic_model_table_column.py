# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .fabric import Fabric


class FabricSemanticModelTableColumn(Fabric):
    """Description"""

    type_name: str = Field(
        default="FabricSemanticModelTableColumn", allow_mutation=False
    )

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FabricSemanticModelTableColumn":
            raise ValueError("must be FabricSemanticModelTableColumn")
        return v

    def __setattr__(self, name, value):
        if name in FabricSemanticModelTableColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

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

    FABRIC_SEMANTIC_MODEL_TABLE: ClassVar[RelationField] = RelationField(
        "fabricSemanticModelTable"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "fabric_semantic_model_table_qualified_name",
        "fabric_semantic_model_table_name",
        "fabric_semantic_model_table",
    ]

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
        fabric_semantic_model_table_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        fabric_semantic_model_table_name: Optional[str] = Field(
            default=None, description=""
        )
        fabric_semantic_model_table: Optional[FabricSemanticModelTable] = Field(
            default=None, description=""
        )  # relationship

    attributes: FabricSemanticModelTableColumn.Attributes = Field(
        default_factory=lambda: FabricSemanticModelTableColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .fabric_semantic_model_table import FabricSemanticModelTable  # noqa: E402, F401
