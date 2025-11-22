# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField

from .saa_s import SaaS


class SageMakerUnifiedStudio(SaaS):
    """Description"""

    type_name: str = Field(default="SageMakerUnifiedStudio", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SageMakerUnifiedStudio":
            raise ValueError("must be SageMakerUnifiedStudio")
        return v

    def __setattr__(self, name, value):
        if name in SageMakerUnifiedStudio._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SMUS_DOMAIN_NAME: ClassVar[KeywordField] = KeywordField(
        "smusDomainName", "smusDomainName"
    )
    """
    AWS SMUS Domain Name
    """
    SMUS_DOMAIN_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "smusDomainId", "smusDomainId.keyword", "smusDomainId"
    )
    """
    AWS SMUS Domain ID
    """
    SMUS_DOMAIN_UNIT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "smusDomainUnitName", "smusDomainUnitName.keyword", "smusDomainUnitName"
    )
    """
    AWS SMUS Domain Unit Name
    """
    SMUS_DOMAIN_UNIT_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "smusDomainUnitId", "smusDomainUnitId.keyword", "smusDomainUnitId"
    )
    """
    AWS SMUS Domain Unit ID
    """
    SMUS_PROJECT_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "smusProjectId", "smusProjectId.keyword", "smusProjectId"
    )
    """
    Unique ID of the AWS SMUS Project
    """
    SMUS_OWNING_PROJECT_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "smusOwningProjectId", "smusOwningProjectId.keyword", "smusOwningProjectId"
    )
    """
    Unique ID of the AWS SMUS Project which owns an Asset
    """

    _convenience_properties: ClassVar[List[str]] = [
        "smus_domain_name",
        "smus_domain_id",
        "smus_domain_unit_name",
        "smus_domain_unit_id",
        "smus_project_id",
        "smus_owning_project_id",
    ]

    @property
    def smus_domain_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.smus_domain_name

    @smus_domain_name.setter
    def smus_domain_name(self, smus_domain_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_domain_name = smus_domain_name

    @property
    def smus_domain_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.smus_domain_id

    @smus_domain_id.setter
    def smus_domain_id(self, smus_domain_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_domain_id = smus_domain_id

    @property
    def smus_domain_unit_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.smus_domain_unit_name
        )

    @smus_domain_unit_name.setter
    def smus_domain_unit_name(self, smus_domain_unit_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_domain_unit_name = smus_domain_unit_name

    @property
    def smus_domain_unit_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.smus_domain_unit_id

    @smus_domain_unit_id.setter
    def smus_domain_unit_id(self, smus_domain_unit_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_domain_unit_id = smus_domain_unit_id

    @property
    def smus_project_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.smus_project_id

    @smus_project_id.setter
    def smus_project_id(self, smus_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_project_id = smus_project_id

    @property
    def smus_owning_project_id(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.smus_owning_project_id
        )

    @smus_owning_project_id.setter
    def smus_owning_project_id(self, smus_owning_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_owning_project_id = smus_owning_project_id

    class Attributes(SaaS.Attributes):
        smus_domain_name: Optional[str] = Field(default=None, description="")
        smus_domain_id: Optional[str] = Field(default=None, description="")
        smus_domain_unit_name: Optional[str] = Field(default=None, description="")
        smus_domain_unit_id: Optional[str] = Field(default=None, description="")
        smus_project_id: Optional[str] = Field(default=None, description="")
        smus_owning_project_id: Optional[str] = Field(default=None, description="")

    attributes: SageMakerUnifiedStudio.Attributes = Field(
        default_factory=lambda: SageMakerUnifiedStudio.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
