# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
)

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

    DM_DATA_MODEL_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dmDataModelName", "dmDataModelName.keyword", "dmDataModelName"
    )
    """
    Simple name of the model in which this asset exists, or empty if it is itself a data model.
    """
    DM_DATA_MODEL_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dmDataModelQualifiedName", "dmDataModelQualifiedName"
    )
    """
    Unique name of the model in which this asset exists, or empty if it is itself a data model.
    """
    DM_DATA_MODEL_DOMAIN: ClassVar[KeywordTextField] = KeywordTextField(
        "dmDataModelDomain", "dmDataModelDomain.keyword", "dmDataModelDomain"
    )
    """
    A domain of the data model in which this asset exists.
    """
    DM_DATA_MODEL_NAMESPACE: ClassVar[KeywordTextField] = KeywordTextField(
        "dmDataModelNamespace", "dmDataModelNamespace.keyword", "dmDataModelNamespace"
    )
    """
    A namespace of the data model in which this asset exists.
    """
    DM_VERSION_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dmVersionName", "dmVersionName.keyword", "dmVersionName"
    )
    """
    Simple name of the version in which this asset exists, or empty if it is itself a data model version.
    """
    DM_VERSION_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dmVersionQualifiedName", "dmVersionQualifiedName"
    )
    """
    Unique name of the version in which this asset exists, or empty if it is itself a data model version.
    """
    DM_ENTITY_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dmEntityName", "dmEntityName.keyword", "dmEntityName"
    )
    """
    Simple name of the entity in which this asset exists, or empty if it is itself a data model entity.
    """
    DM_ENTITY_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dmEntityQualifiedName", "dmEntityQualifiedName"
    )
    """
    Unique name of the entity in which this asset exists, or empty if it is itself a data model entity.
    """
    DM_SYSTEM_DATE: ClassVar[NumericField] = NumericField(
        "dmSystemDate", "dmSystemDate"
    )
    """
    System date for the asset.
    """
    DM_BUSINESS_DATE: ClassVar[NumericField] = NumericField(
        "dmBusinessDate", "dmBusinessDate"
    )
    """
    Business date for the asset.
    """
    DM_EXPIRED_AT_SYSTEM_DATE: ClassVar[NumericField] = NumericField(
        "dmExpiredAtSystemDate", "dmExpiredAtSystemDate"
    )
    """
    System expiration date for the asset.
    """
    DM_EXPIRED_AT_BUSINESS_DATE: ClassVar[NumericField] = NumericField(
        "dmExpiredAtBusinessDate", "dmExpiredAtBusinessDate"
    )
    """
    Business expiration date for the asset.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dm_data_model_name",
        "dm_data_model_qualified_name",
        "dm_data_model_domain",
        "dm_data_model_namespace",
        "dm_version_name",
        "dm_version_qualified_name",
        "dm_entity_name",
        "dm_entity_qualified_name",
        "dm_system_date",
        "dm_business_date",
        "dm_expired_at_system_date",
        "dm_expired_at_business_date",
    ]

    @property
    def dm_data_model_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dm_data_model_name

    @dm_data_model_name.setter
    def dm_data_model_name(self, dm_data_model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_data_model_name = dm_data_model_name

    @property
    def dm_data_model_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dm_data_model_qualified_name
        )

    @dm_data_model_qualified_name.setter
    def dm_data_model_qualified_name(self, dm_data_model_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_data_model_qualified_name = dm_data_model_qualified_name

    @property
    def dm_data_model_domain(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dm_data_model_domain

    @dm_data_model_domain.setter
    def dm_data_model_domain(self, dm_data_model_domain: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_data_model_domain = dm_data_model_domain

    @property
    def dm_data_model_namespace(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dm_data_model_namespace
        )

    @dm_data_model_namespace.setter
    def dm_data_model_namespace(self, dm_data_model_namespace: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_data_model_namespace = dm_data_model_namespace

    @property
    def dm_version_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dm_version_name

    @dm_version_name.setter
    def dm_version_name(self, dm_version_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_version_name = dm_version_name

    @property
    def dm_version_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dm_version_qualified_name
        )

    @dm_version_qualified_name.setter
    def dm_version_qualified_name(self, dm_version_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_version_qualified_name = dm_version_qualified_name

    @property
    def dm_entity_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dm_entity_name

    @dm_entity_name.setter
    def dm_entity_name(self, dm_entity_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_entity_name = dm_entity_name

    @property
    def dm_entity_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dm_entity_qualified_name
        )

    @dm_entity_qualified_name.setter
    def dm_entity_qualified_name(self, dm_entity_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_entity_qualified_name = dm_entity_qualified_name

    @property
    def dm_system_date(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.dm_system_date

    @dm_system_date.setter
    def dm_system_date(self, dm_system_date: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_system_date = dm_system_date

    @property
    def dm_business_date(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.dm_business_date

    @dm_business_date.setter
    def dm_business_date(self, dm_business_date: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_business_date = dm_business_date

    @property
    def dm_expired_at_system_date(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dm_expired_at_system_date
        )

    @dm_expired_at_system_date.setter
    def dm_expired_at_system_date(self, dm_expired_at_system_date: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_expired_at_system_date = dm_expired_at_system_date

    @property
    def dm_expired_at_business_date(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dm_expired_at_business_date
        )

    @dm_expired_at_business_date.setter
    def dm_expired_at_business_date(
        self, dm_expired_at_business_date: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_expired_at_business_date = dm_expired_at_business_date

    class Attributes(Catalog.Attributes):
        dm_data_model_name: Optional[str] = Field(default=None, description="")
        dm_data_model_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        dm_data_model_domain: Optional[str] = Field(default=None, description="")
        dm_data_model_namespace: Optional[str] = Field(default=None, description="")
        dm_version_name: Optional[str] = Field(default=None, description="")
        dm_version_qualified_name: Optional[str] = Field(default=None, description="")
        dm_entity_name: Optional[str] = Field(default=None, description="")
        dm_entity_qualified_name: Optional[str] = Field(default=None, description="")
        dm_system_date: Optional[datetime] = Field(default=None, description="")
        dm_business_date: Optional[datetime] = Field(default=None, description="")
        dm_expired_at_system_date: Optional[datetime] = Field(
            default=None, description=""
        )
        dm_expired_at_business_date: Optional[datetime] = Field(
            default=None, description=""
        )

    attributes: DM.Attributes = Field(
        default_factory=lambda: DM.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


DM.Attributes.update_forward_refs()
