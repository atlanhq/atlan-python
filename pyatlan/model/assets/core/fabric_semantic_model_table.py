# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .fabric import Fabric


class FabricSemanticModelTable(Fabric):
    """Description"""

    type_name: str = Field(default="FabricSemanticModelTable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FabricSemanticModelTable":
            raise ValueError("must be FabricSemanticModelTable")
        return v

    def __setattr__(self, name, value):
        if name in FabricSemanticModelTable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FABRIC_SEMANTIC_MODEL_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "fabricSemanticModelQualifiedName", "fabricSemanticModelQualifiedName"
    )
    """
    Unique name of the Fabric semantic model that contains this asset.
    """

    FABRIC_SEMANTIC_MODEL_TABLE_COLUMNS: ClassVar[RelationField] = RelationField(
        "fabricSemanticModelTableColumns"
    )
    """
    TBC
    """
    FABRIC_SEMANTIC_MODEL: ClassVar[RelationField] = RelationField(
        "fabricSemanticModel"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "fabric_semantic_model_qualified_name",
        "fabric_semantic_model_table_columns",
        "fabric_semantic_model",
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
    def fabric_semantic_model(self) -> Optional[FabricSemanticModel]:
        return (
            None if self.attributes is None else self.attributes.fabric_semantic_model
        )

    @fabric_semantic_model.setter
    def fabric_semantic_model(
        self, fabric_semantic_model: Optional[FabricSemanticModel]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_semantic_model = fabric_semantic_model

    class Attributes(Fabric.Attributes):
        fabric_semantic_model_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        fabric_semantic_model_table_columns: Optional[
            List[FabricSemanticModelTableColumn]
        ] = Field(default=None, description="")  # relationship
        fabric_semantic_model: Optional[FabricSemanticModel] = Field(
            default=None, description=""
        )  # relationship

    attributes: FabricSemanticModelTable.Attributes = Field(
        default_factory=lambda: FabricSemanticModelTable.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .fabric_semantic_model import FabricSemanticModel  # noqa: E402, F401
from .fabric_semantic_model_table_column import (
    FabricSemanticModelTableColumn,  # noqa: E402, F401
)
