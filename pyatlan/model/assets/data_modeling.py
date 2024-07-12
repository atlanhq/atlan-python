# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField

from .catalog import Catalog


class DataModeling(Catalog):
    """Description"""

    type_name: str = Field(default="DataModeling", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataModeling":
            raise ValueError("must be DataModeling")
        return v

    def __setattr__(self, name, value):
        if name in DataModeling._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_MODEL_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dataModelName", "dataModelName.keyword", "dataModelName"
    )
    """
    Simple name of the data model in which this asset exists, or empty if it is itself a data model.
    """
    DATA_MODEL_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dataModelQualifiedName", "dataModelQualifiedName"
    )
    """

    """
    DATA_MODEL_VERSION_QUALIFIED_NAMES: ClassVar[KeywordField] = KeywordField(
        "dataModelVersionQualifiedNames", "dataModelVersionQualifiedNames"
    )
    """

    """
    DATA_MODEL_ENVIRONMENT: ClassVar[KeywordField] = KeywordField(
        "dataModelEnvironment", "dataModelEnvironment"
    )
    """

    """
    DATA_MODEL_DOMAIN: ClassVar[KeywordField] = KeywordField(
        "dataModelDomain", "dataModelDomain"
    )
    """

    """
    DATA_MODEL_NAMESPACE: ClassVar[KeywordField] = KeywordField(
        "dataModelNamespace", "dataModelNamespace"
    )
    """

    """
    DATA_MODEL_ID: ClassVar[KeywordField] = KeywordField("dataModelId", "dataModelId")
    """

    """
    DATA_ENTITY_ID: ClassVar[KeywordField] = KeywordField(
        "dataEntityId", "dataEntityId"
    )
    """

    """

    _convenience_properties: ClassVar[List[str]] = [
        "data_model_name",
        "data_model_qualified_name",
        "data_model_version_qualified_names",
        "data_model_environment",
        "data_model_domain",
        "data_model_namespace",
        "data_model_id",
        "data_entity_id",
    ]

    @property
    def data_model_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_model_name

    @data_model_name.setter
    def data_model_name(self, data_model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_name = data_model_name

    @property
    def data_model_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_model_qualified_name
        )

    @data_model_qualified_name.setter
    def data_model_qualified_name(self, data_model_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_qualified_name = data_model_qualified_name

    @property
    def data_model_version_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_model_version_qualified_names
        )

    @data_model_version_qualified_names.setter
    def data_model_version_qualified_names(
        self, data_model_version_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_version_qualified_names = (
            data_model_version_qualified_names
        )

    @property
    def data_model_environment(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.data_model_environment
        )

    @data_model_environment.setter
    def data_model_environment(self, data_model_environment: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_environment = data_model_environment

    @property
    def data_model_domain(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_model_domain

    @data_model_domain.setter
    def data_model_domain(self, data_model_domain: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_domain = data_model_domain

    @property
    def data_model_namespace(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_model_namespace

    @data_model_namespace.setter
    def data_model_namespace(self, data_model_namespace: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_namespace = data_model_namespace

    @property
    def data_model_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_model_id

    @data_model_id.setter
    def data_model_id(self, data_model_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_id = data_model_id

    @property
    def data_entity_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_entity_id

    @data_entity_id.setter
    def data_entity_id(self, data_entity_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_entity_id = data_entity_id

    class Attributes(Catalog.Attributes):
        data_model_name: Optional[str] = Field(default=None, description="")
        data_model_qualified_name: Optional[str] = Field(default=None, description="")
        data_model_version_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        data_model_environment: Optional[str] = Field(default=None, description="")
        data_model_domain: Optional[str] = Field(default=None, description="")
        data_model_namespace: Optional[str] = Field(default=None, description="")
        data_model_id: Optional[str] = Field(default=None, description="")
        data_entity_id: Optional[str] = Field(default=None, description="")

    attributes: DataModeling.Attributes = Field(
        default_factory=lambda: DataModeling.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
