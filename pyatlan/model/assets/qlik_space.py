# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .qlik import Qlik


class QlikSpace(Qlik):
    """Description"""

    type_name: str = Field(default="QlikSpace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikSpace":
            raise ValueError("must be QlikSpace")
        return v

    def __setattr__(self, name, value):
        if name in QlikSpace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QLIK_SPACE_TYPE: ClassVar[KeywordField] = KeywordField(
        "qlikSpaceType", "qlikSpaceType"
    )
    """
    Type of this space, for exmaple: Private, Shared, etc.
    """

    QLIK_DATASETS: ClassVar[RelationField] = RelationField("qlikDatasets")
    """
    TBC
    """
    QLIK_APPS: ClassVar[RelationField] = RelationField("qlikApps")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "qlik_space_type",
        "qlik_datasets",
        "qlik_apps",
    ]

    @property
    def qlik_space_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_space_type

    @qlik_space_type.setter
    def qlik_space_type(self, qlik_space_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space_type = qlik_space_type

    @property
    def qlik_datasets(self) -> Optional[List[QlikDataset]]:
        return None if self.attributes is None else self.attributes.qlik_datasets

    @qlik_datasets.setter
    def qlik_datasets(self, qlik_datasets: Optional[List[QlikDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_datasets = qlik_datasets

    @property
    def qlik_apps(self) -> Optional[List[QlikApp]]:
        return None if self.attributes is None else self.attributes.qlik_apps

    @qlik_apps.setter
    def qlik_apps(self, qlik_apps: Optional[List[QlikApp]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_apps = qlik_apps

    class Attributes(Qlik.Attributes):
        qlik_space_type: Optional[str] = Field(default=None, description="")
        qlik_datasets: Optional[List[QlikDataset]] = Field(
            default=None, description=""
        )  # relationship
        qlik_apps: Optional[List[QlikApp]] = Field(
            default=None, description=""
        )  # relationship

    attributes: QlikSpace.Attributes = Field(
        default_factory=lambda: QlikSpace.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .qlik_app import QlikApp  # noqa
from .qlik_dataset import QlikDataset  # noqa
