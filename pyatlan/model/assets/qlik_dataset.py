# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .qlik import Qlik


class QlikDataset(Qlik):
    """Description"""

    type_name: str = Field(default="QlikDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikDataset":
            raise ValueError("must be QlikDataset")
        return v

    def __setattr__(self, name, value):
        if name in QlikDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QLIK_DATASET_TECHNICAL_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "qlikDatasetTechnicalName",
        "qlikDatasetTechnicalName.keyword",
        "qlikDatasetTechnicalName",
    )
    """
    Technical name of this asset.
    """
    QLIK_DATASET_TYPE: ClassVar[KeywordField] = KeywordField(
        "qlikDatasetType", "qlikDatasetType"
    )
    """
    Type of this data asset, for example: qix-df, snowflake, etc.
    """
    QLIK_DATASET_URI: ClassVar[KeywordTextField] = KeywordTextField(
        "qlikDatasetUri", "qlikDatasetUri", "qlikDatasetUri.text"
    )
    """
    URI of this dataset.
    """
    QLIK_DATASET_SUBTYPE: ClassVar[KeywordField] = KeywordField(
        "qlikDatasetSubtype", "qlikDatasetSubtype"
    )
    """
    Subtype this dataset asset.
    """

    QLIK_SPACE: ClassVar[RelationField] = RelationField("qlikSpace")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "qlik_dataset_technical_name",
        "qlik_dataset_type",
        "qlik_dataset_uri",
        "qlik_dataset_subtype",
        "qlik_space",
    ]

    @property
    def qlik_dataset_technical_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.qlik_dataset_technical_name
        )

    @qlik_dataset_technical_name.setter
    def qlik_dataset_technical_name(self, qlik_dataset_technical_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_technical_name = qlik_dataset_technical_name

    @property
    def qlik_dataset_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_dataset_type

    @qlik_dataset_type.setter
    def qlik_dataset_type(self, qlik_dataset_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_type = qlik_dataset_type

    @property
    def qlik_dataset_uri(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_dataset_uri

    @qlik_dataset_uri.setter
    def qlik_dataset_uri(self, qlik_dataset_uri: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_uri = qlik_dataset_uri

    @property
    def qlik_dataset_subtype(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_dataset_subtype

    @qlik_dataset_subtype.setter
    def qlik_dataset_subtype(self, qlik_dataset_subtype: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_subtype = qlik_dataset_subtype

    @property
    def qlik_space(self) -> Optional[QlikSpace]:
        return None if self.attributes is None else self.attributes.qlik_space

    @qlik_space.setter
    def qlik_space(self, qlik_space: Optional[QlikSpace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space = qlik_space

    class Attributes(Qlik.Attributes):
        qlik_dataset_technical_name: Optional[str] = Field(default=None, description="")
        qlik_dataset_type: Optional[str] = Field(default=None, description="")
        qlik_dataset_uri: Optional[str] = Field(default=None, description="")
        qlik_dataset_subtype: Optional[str] = Field(default=None, description="")
        qlik_space: Optional[QlikSpace] = Field(
            default=None, description=""
        )  # relationship

    attributes: QlikDataset.Attributes = Field(
        default_factory=lambda: QlikDataset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .qlik_space import QlikSpace  # noqa
