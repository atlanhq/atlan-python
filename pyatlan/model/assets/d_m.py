# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField

from .core.catalog import Catalog


class DM(Catalog):
    """Description"""

    type_name: str = Field(default="DM", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DM":
            raise ValueError("must be DM")
        return v

    def __setattr__(self, name, value):
        if name in DM._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    D_M_DATA_MODEL_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dMDataModelName", "dMDataModelName.keyword", "dMDataModelName"
    )
    """
    Simple name of the model in which this asset exists, or empty if it is itself a data model.
    """
    D_M_DATA_MODEL_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dMDataModelQualifiedName", "dMDataModelQualifiedName"
    )
    """
    Unique name of the model in which this asset exists, or empty if it is itself a data model.
    """
    D_M_DATA_MODEL_DOMAIN: ClassVar[KeywordTextField] = KeywordTextField(
        "dMDataModelDomain", "dMDataModelDomain.keyword", "dMDataModelDomain"
    )
    """
    A domain of the datam model in which this asset exists.
    """
    D_M_DATA_MODEL_NAMESPACE: ClassVar[KeywordTextField] = KeywordTextField(
        "dMDataModelNamespace", "dMDataModelNamespace.keyword", "dMDataModelNamespace"
    )
    """
    A namespace of the data model in which this asset exists.
    """
    D_M_VERSION_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dMVersionName", "dMVersionName.keyword", "dMVersionName"
    )
    """
    Simple name of the version in which this asset exists, or empty if it is itself a data model version.
    """
    D_M_VERSION_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dMVersionQualifiedName", "dMVersionQualifiedName"
    )
    """
    Unique name of the version in which this asset exists, or empty if it is itself a data model version.
    """
    D_M_ENTITY_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dMEntityName", "dMEntityName.keyword", "dMEntityName"
    )
    """
    Simple name of the entity in which this asset exists, or empty if it is itself a data model entity.
    """
    D_M_ENTITY_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dMEntityQualifiedName", "dMEntityQualifiedName"
    )
    """
    Unique name of the entity in which this asset exists, or empty if it is itself a data model entity.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "d_m_data_model_name",
        "d_m_data_model_qualified_name",
        "d_m_data_model_domain",
        "d_m_data_model_namespace",
        "d_m_version_name",
        "d_m_version_qualified_name",
        "d_m_entity_name",
        "d_m_entity_qualified_name",
    ]

    @property
    def d_m_data_model_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.d_m_data_model_name

    @d_m_data_model_name.setter
    def d_m_data_model_name(self, d_m_data_model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_data_model_name = d_m_data_model_name

    @property
    def d_m_data_model_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.d_m_data_model_qualified_name
        )

    @d_m_data_model_qualified_name.setter
    def d_m_data_model_qualified_name(
        self, d_m_data_model_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_data_model_qualified_name = d_m_data_model_qualified_name

    @property
    def d_m_data_model_domain(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.d_m_data_model_domain
        )

    @d_m_data_model_domain.setter
    def d_m_data_model_domain(self, d_m_data_model_domain: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_data_model_domain = d_m_data_model_domain

    @property
    def d_m_data_model_namespace(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.d_m_data_model_namespace
        )

    @d_m_data_model_namespace.setter
    def d_m_data_model_namespace(self, d_m_data_model_namespace: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_data_model_namespace = d_m_data_model_namespace

    @property
    def d_m_version_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.d_m_version_name

    @d_m_version_name.setter
    def d_m_version_name(self, d_m_version_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_version_name = d_m_version_name

    @property
    def d_m_version_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.d_m_version_qualified_name
        )

    @d_m_version_qualified_name.setter
    def d_m_version_qualified_name(self, d_m_version_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_version_qualified_name = d_m_version_qualified_name

    @property
    def d_m_entity_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.d_m_entity_name

    @d_m_entity_name.setter
    def d_m_entity_name(self, d_m_entity_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_entity_name = d_m_entity_name

    @property
    def d_m_entity_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.d_m_entity_qualified_name
        )

    @d_m_entity_qualified_name.setter
    def d_m_entity_qualified_name(self, d_m_entity_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_entity_qualified_name = d_m_entity_qualified_name

    class Attributes(Catalog.Attributes):
        d_m_data_model_name: Optional[str] = Field(default=None, description="")
        d_m_data_model_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        d_m_data_model_domain: Optional[str] = Field(default=None, description="")
        d_m_data_model_namespace: Optional[str] = Field(default=None, description="")
        d_m_version_name: Optional[str] = Field(default=None, description="")
        d_m_version_qualified_name: Optional[str] = Field(default=None, description="")
        d_m_entity_name: Optional[str] = Field(default=None, description="")
        d_m_entity_qualified_name: Optional[str] = Field(default=None, description="")

    attributes: DM.Attributes = Field(
        default_factory=lambda: DM.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


DM.Attributes.update_forward_refs()
