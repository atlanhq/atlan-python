# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .fabric import Fabric


class FabricDataflowEntityColumn(Fabric):
    """Description"""

    type_name: str = Field(default="FabricDataflowEntityColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FabricDataflowEntityColumn":
            raise ValueError("must be FabricDataflowEntityColumn")
        return v

    def __setattr__(self, name, value):
        if name in FabricDataflowEntityColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FABRIC_DATAFLOW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "fabricDataflowQualifiedName", "fabricDataflowQualifiedName"
    )
    """
    Unique name of the Fabric dataflow that contains this asset.
    """
    FABRIC_DATAFLOW_NAME: ClassVar[KeywordField] = KeywordField(
        "fabricDataflowName", "fabricDataflowName"
    )
    """
    Name of the Fabric dataflow that contains this asset.
    """

    FABRIC_DATAFLOW: ClassVar[RelationField] = RelationField("fabricDataflow")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "fabric_dataflow_qualified_name",
        "fabric_dataflow_name",
        "fabric_dataflow",
    ]

    @property
    def fabric_dataflow_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fabric_dataflow_qualified_name
        )

    @fabric_dataflow_qualified_name.setter
    def fabric_dataflow_qualified_name(
        self, fabric_dataflow_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_dataflow_qualified_name = fabric_dataflow_qualified_name

    @property
    def fabric_dataflow_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.fabric_dataflow_name

    @fabric_dataflow_name.setter
    def fabric_dataflow_name(self, fabric_dataflow_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_dataflow_name = fabric_dataflow_name

    @property
    def fabric_dataflow(self) -> Optional[FabricDataflow]:
        return None if self.attributes is None else self.attributes.fabric_dataflow

    @fabric_dataflow.setter
    def fabric_dataflow(self, fabric_dataflow: Optional[FabricDataflow]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_dataflow = fabric_dataflow

    class Attributes(Fabric.Attributes):
        fabric_dataflow_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        fabric_dataflow_name: Optional[str] = Field(default=None, description="")
        fabric_dataflow: Optional[FabricDataflow] = Field(
            default=None, description=""
        )  # relationship

    attributes: FabricDataflowEntityColumn.Attributes = Field(
        default_factory=lambda: FabricDataflowEntityColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .fabric_dataflow import FabricDataflow  # noqa: E402, F401
