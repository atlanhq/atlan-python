# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

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
    Name of the SageMaker Unified Studio domain.
    """
    SMUS_DOMAIN_ID: ClassVar[KeywordField] = KeywordField(
        "smusDomainId", "smusDomainId"
    )
    """
    Unique identifier of the SageMaker Unified Studio domain.
    """
    SMUS_DOMAIN_UNIT_NAME: ClassVar[KeywordField] = KeywordField(
        "smusDomainUnitName", "smusDomainUnitName"
    )
    """
    Name of the SageMaker Unified Studio domain unit.
    """
    SMUS_DOMAIN_UNIT_ID: ClassVar[KeywordField] = KeywordField(
        "smusDomainUnitId", "smusDomainUnitId"
    )
    """
    Unique identifier of the SageMaker Unified Studio domain unit.
    """
    SMUS_PROJECT_ID: ClassVar[KeywordField] = KeywordField(
        "smusProjectId", "smusProjectId"
    )
    """
    Unique identifier of the SageMaker Unified Studio project.
    """
    SMUS_OWNING_PROJECT_ID: ClassVar[KeywordField] = KeywordField(
        "smusOwningProjectId", "smusOwningProjectId"
    )
    """
    Unique identifier of the SageMaker Unified Studio project which owns the asset.
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


SageMakerUnifiedStudio.Attributes.update_forward_refs()
