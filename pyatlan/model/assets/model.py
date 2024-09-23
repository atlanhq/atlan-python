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


class Model(Catalog):
    """Description"""

    type_name: str = Field(default="Model", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Model":
            raise ValueError("must be Model")
        return v

    def __setattr__(self, name, value):
        if name in Model._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODEL_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modelName", "modelName.keyword", "modelName"
    )
    """
    Simple name of the model in which this asset exists, or empty if it is itself a data model.
    """
    MODEL_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "modelQualifiedName", "modelQualifiedName"
    )
    """
    Unique name of the model in which this asset exists, or empty if it is itself a data model.
    """
    MODEL_DOMAIN: ClassVar[KeywordTextField] = KeywordTextField(
        "modelDomain", "modelDomain.keyword", "modelDomain"
    )
    """
    Model domain in which this asset exists.
    """
    MODEL_NAMESPACE: ClassVar[KeywordTextField] = KeywordTextField(
        "modelNamespace", "modelNamespace.keyword", "modelNamespace"
    )
    """
    Model namespace in which this asset exists.
    """
    MODEL_VERSION_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modelVersionName", "modelVersionName.keyword", "modelVersionName"
    )
    """
    Simple name of the version in which this asset exists, or empty if it is itself a data model version.
    """
    MODEL_VERSION_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "modelVersionQualifiedName", "modelVersionQualifiedName"
    )
    """
    Unique name of the version in which this asset exists, or empty if it is itself a data model version.
    """
    MODEL_ENTITY_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modelEntityName", "modelEntityName.keyword", "modelEntityName"
    )
    """
    Simple name of the entity in which this asset exists, or empty if it is itself a data model entity.
    """
    MODEL_ENTITY_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "modelEntityQualifiedName", "modelEntityQualifiedName"
    )
    """
    Unique name of the entity in which this asset exists, or empty if it is itself a data model entity.
    """
    MODEL_TYPE: ClassVar[KeywordField] = KeywordField("modelType", "modelType")
    """
    Type of the model asset (conceptual, logical, physical).
    """
    MODEL_SYSTEM_DATE: ClassVar[NumericField] = NumericField(
        "modelSystemDate", "modelSystemDate"
    )
    """
    System date for the asset.
    """
    MODEL_BUSINESS_DATE: ClassVar[NumericField] = NumericField(
        "modelBusinessDate", "modelBusinessDate"
    )
    """
    Business date for the asset.
    """
    MODEL_EXPIRED_AT_SYSTEM_DATE: ClassVar[NumericField] = NumericField(
        "modelExpiredAtSystemDate", "modelExpiredAtSystemDate"
    )
    """
    System expiration date for the asset.
    """
    MODEL_EXPIRED_AT_BUSINESS_DATE: ClassVar[NumericField] = NumericField(
        "modelExpiredAtBusinessDate", "modelExpiredAtBusinessDate"
    )
    """
    Business expiration date for the asset.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "model_name",
        "model_qualified_name",
        "model_domain",
        "model_namespace",
        "model_version_name",
        "model_version_qualified_name",
        "model_entity_name",
        "model_entity_qualified_name",
        "model_type",
        "model_system_date",
        "model_business_date",
        "model_expired_at_system_date",
        "model_expired_at_business_date",
    ]

    @property
    def model_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_name

    @model_name.setter
    def model_name(self, model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_name = model_name

    @property
    def model_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_qualified_name

    @model_qualified_name.setter
    def model_qualified_name(self, model_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_qualified_name = model_qualified_name

    @property
    def model_domain(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_domain

    @model_domain.setter
    def model_domain(self, model_domain: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_domain = model_domain

    @property
    def model_namespace(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_namespace

    @model_namespace.setter
    def model_namespace(self, model_namespace: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_namespace = model_namespace

    @property
    def model_version_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_version_name

    @model_version_name.setter
    def model_version_name(self, model_version_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_version_name = model_version_name

    @property
    def model_version_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_version_qualified_name
        )

    @model_version_qualified_name.setter
    def model_version_qualified_name(self, model_version_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_version_qualified_name = model_version_qualified_name

    @property
    def model_entity_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_entity_name

    @model_entity_name.setter
    def model_entity_name(self, model_entity_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_name = model_entity_name

    @property
    def model_entity_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_entity_qualified_name
        )

    @model_entity_qualified_name.setter
    def model_entity_qualified_name(self, model_entity_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_qualified_name = model_entity_qualified_name

    @property
    def model_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_type

    @model_type.setter
    def model_type(self, model_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_type = model_type

    @property
    def model_system_date(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.model_system_date

    @model_system_date.setter
    def model_system_date(self, model_system_date: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_system_date = model_system_date

    @property
    def model_business_date(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.model_business_date

    @model_business_date.setter
    def model_business_date(self, model_business_date: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_business_date = model_business_date

    @property
    def model_expired_at_system_date(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_expired_at_system_date
        )

    @model_expired_at_system_date.setter
    def model_expired_at_system_date(
        self, model_expired_at_system_date: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_expired_at_system_date = model_expired_at_system_date

    @property
    def model_expired_at_business_date(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_expired_at_business_date
        )

    @model_expired_at_business_date.setter
    def model_expired_at_business_date(
        self, model_expired_at_business_date: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_expired_at_business_date = model_expired_at_business_date

    class Attributes(Catalog.Attributes):
        model_name: Optional[str] = Field(default=None, description="")
        model_qualified_name: Optional[str] = Field(default=None, description="")
        model_domain: Optional[str] = Field(default=None, description="")
        model_namespace: Optional[str] = Field(default=None, description="")
        model_version_name: Optional[str] = Field(default=None, description="")
        model_version_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        model_entity_name: Optional[str] = Field(default=None, description="")
        model_entity_qualified_name: Optional[str] = Field(default=None, description="")
        model_type: Optional[str] = Field(default=None, description="")
        model_system_date: Optional[datetime] = Field(default=None, description="")
        model_business_date: Optional[datetime] = Field(default=None, description="")
        model_expired_at_system_date: Optional[datetime] = Field(
            default=None, description=""
        )
        model_expired_at_business_date: Optional[datetime] = Field(
            default=None, description=""
        )

    attributes: Model.Attributes = Field(
        default_factory=lambda: Model.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Model.Attributes.update_forward_refs()
