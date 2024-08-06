# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .data_modeling import DataModeling


class DataModelVersion(DataModeling):
    """Description"""

    type_name: str = Field(default="DataModelVersion", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataModelVersion":
            raise ValueError("must be DataModelVersion")
        return v

    def __setattr__(self, name, value):
        if name in DataModelVersion._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_MODEL: ClassVar[RelationField] = RelationField("dataModel")
    """
    TBC
    """
    DATA_ENTITIES: ClassVar[RelationField] = RelationField("dataEntities")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "data_model",
        "data_entities",
    ]

    @property
    def data_model(self) -> Optional[DataModel]:
        return None if self.attributes is None else self.attributes.data_model

    @data_model.setter
    def data_model(self, data_model: Optional[DataModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model = data_model

    @property
    def data_entities(self) -> Optional[List[DataEntity]]:
        return None if self.attributes is None else self.attributes.data_entities

    @data_entities.setter
    def data_entities(self, data_entities: Optional[List[DataEntity]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_entities = data_entities

    class Attributes(DataModeling.Attributes):
        data_model: Optional[DataModel] = Field(
            default=None, description=""
        )  # relationship
        data_entities: Optional[List[DataEntity]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DataModelVersion.Attributes = Field(
        default_factory=lambda: DataModelVersion.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .data_entity import DataEntity  # noqa
from .data_model import DataModel  # noqa
