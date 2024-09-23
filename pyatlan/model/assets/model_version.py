# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .model import Model


class ModelVersion(Model):
    """Description"""

    type_name: str = Field(default="ModelVersion", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModelVersion":
            raise ValueError("must be ModelVersion")
        return v

    def __setattr__(self, name, value):
        if name in ModelVersion._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODEL_VERSION_ENTITY_COUNT: ClassVar[NumericField] = NumericField(
        "modelVersionEntityCount", "modelVersionEntityCount"
    )
    """
    Number of entities in the version.
    """

    MODEL_DATA_MODEL: ClassVar[RelationField] = RelationField("modelDataModel")
    """
    TBC
    """
    MODEL_VERSION_ENTITIES: ClassVar[RelationField] = RelationField(
        "modelVersionEntities"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "model_version_entity_count",
        "model_data_model",
        "model_version_entities",
    ]

    @property
    def model_version_entity_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_version_entity_count
        )

    @model_version_entity_count.setter
    def model_version_entity_count(self, model_version_entity_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_version_entity_count = model_version_entity_count

    @property
    def model_data_model(self) -> Optional[ModelDataModel]:
        return None if self.attributes is None else self.attributes.model_data_model

    @model_data_model.setter
    def model_data_model(self, model_data_model: Optional[ModelDataModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_data_model = model_data_model

    @property
    def model_version_entities(self) -> Optional[List[ModelEntity]]:
        return (
            None if self.attributes is None else self.attributes.model_version_entities
        )

    @model_version_entities.setter
    def model_version_entities(
        self, model_version_entities: Optional[List[ModelEntity]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_version_entities = model_version_entities

    class Attributes(Model.Attributes):
        model_version_entity_count: Optional[int] = Field(default=None, description="")
        model_data_model: Optional[ModelDataModel] = Field(
            default=None, description=""
        )  # relationship
        model_version_entities: Optional[List[ModelEntity]] = Field(
            default=None, description=""
        )  # relationship

    attributes: ModelVersion.Attributes = Field(
        default_factory=lambda: ModelVersion.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .model_data_model import ModelDataModel  # noqa
from .model_entity import ModelEntity  # noqa

ModelVersion.Attributes.update_forward_refs()
