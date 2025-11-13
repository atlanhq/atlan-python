# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .fabric import Fabric


class FabricActivity(Fabric):
    """Description"""

    type_name: str = Field(default="FabricActivity", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FabricActivity":
            raise ValueError("must be FabricActivity")
        return v

    def __setattr__(self, name, value):
        if name in FabricActivity._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FABRIC_DATA_PIPELINE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "fabricDataPipelineQualifiedName", "fabricDataPipelineQualifiedName"
    )
    """
    Unique name of the Fabric data pipeline that contains this asset.
    """
    FABRIC_ACTIVITY_TYPE: ClassVar[KeywordField] = KeywordField(
        "fabricActivityType", "fabricActivityType"
    )
    """
    Type of activity.
    """

    FABRIC_DATA_PIPELINE: ClassVar[RelationField] = RelationField("fabricDataPipeline")
    """
    TBC
    """
    FABRIC_PROCESS: ClassVar[RelationField] = RelationField("fabricProcess")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "fabric_data_pipeline_qualified_name",
        "fabric_activity_type",
        "fabric_data_pipeline",
        "fabric_process",
    ]

    @property
    def fabric_data_pipeline_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fabric_data_pipeline_qualified_name
        )

    @fabric_data_pipeline_qualified_name.setter
    def fabric_data_pipeline_qualified_name(
        self, fabric_data_pipeline_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_data_pipeline_qualified_name = (
            fabric_data_pipeline_qualified_name
        )

    @property
    def fabric_activity_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.fabric_activity_type

    @fabric_activity_type.setter
    def fabric_activity_type(self, fabric_activity_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_activity_type = fabric_activity_type

    @property
    def fabric_data_pipeline(self) -> Optional[FabricDataPipeline]:
        return None if self.attributes is None else self.attributes.fabric_data_pipeline

    @fabric_data_pipeline.setter
    def fabric_data_pipeline(self, fabric_data_pipeline: Optional[FabricDataPipeline]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_data_pipeline = fabric_data_pipeline

    @property
    def fabric_process(self) -> Optional[Process]:
        return None if self.attributes is None else self.attributes.fabric_process

    @fabric_process.setter
    def fabric_process(self, fabric_process: Optional[Process]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_process = fabric_process

    class Attributes(Fabric.Attributes):
        fabric_data_pipeline_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        fabric_activity_type: Optional[str] = Field(default=None, description="")
        fabric_data_pipeline: Optional[FabricDataPipeline] = Field(
            default=None, description=""
        )  # relationship
        fabric_process: Optional[Process] = Field(
            default=None, description=""
        )  # relationship

    attributes: FabricActivity.Attributes = Field(
        default_factory=lambda: FabricActivity.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .fabric_data_pipeline import FabricDataPipeline  # noqa: E402, F401
from .process import Process  # noqa: E402, F401
