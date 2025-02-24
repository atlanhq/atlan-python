# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .persona import Persona


class Stakeholder(Persona):
    """Description"""

    type_name: str = Field(default="Stakeholder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Stakeholder":
            raise ValueError("must be Stakeholder")
        return v

    def __setattr__(self, name, value):
        if name in Stakeholder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    STAKEHOLDER_DOMAIN_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "stakeholderDomainQualifiedName", "stakeholderDomainQualifiedName"
    )
    """
    TBC
    """
    STAKEHOLDER_TITLE_GUID: ClassVar[KeywordField] = KeywordField(
        "stakeholderTitleGuid", "stakeholderTitleGuid"
    )
    """
    TBC
    """

    STAKEHOLDER_TITLE: ClassVar[RelationField] = RelationField("stakeholderTitle")
    """
    TBC
    """
    STAKEHOLDER_DATA_DOMAIN: ClassVar[RelationField] = RelationField(
        "stakeholderDataDomain"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "stakeholder_domain_qualified_name",
        "stakeholder_title_guid",
        "stakeholder_title",
        "stakeholder_data_domain",
    ]

    @property
    def stakeholder_domain_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.stakeholder_domain_qualified_name
        )

    @stakeholder_domain_qualified_name.setter
    def stakeholder_domain_qualified_name(
        self, stakeholder_domain_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.stakeholder_domain_qualified_name = (
            stakeholder_domain_qualified_name
        )

    @property
    def stakeholder_title_guid(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.stakeholder_title_guid
        )

    @stakeholder_title_guid.setter
    def stakeholder_title_guid(self, stakeholder_title_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.stakeholder_title_guid = stakeholder_title_guid

    @property
    def stakeholder_title(self) -> Optional[StakeholderTitle]:
        return None if self.attributes is None else self.attributes.stakeholder_title

    @stakeholder_title.setter
    def stakeholder_title(self, stakeholder_title: Optional[StakeholderTitle]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.stakeholder_title = stakeholder_title

    @property
    def stakeholder_data_domain(self) -> Optional[DataDomain]:
        return (
            None if self.attributes is None else self.attributes.stakeholder_data_domain
        )

    @stakeholder_data_domain.setter
    def stakeholder_data_domain(self, stakeholder_data_domain: Optional[DataDomain]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.stakeholder_data_domain = stakeholder_data_domain

    class Attributes(Persona.Attributes):
        stakeholder_domain_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        stakeholder_title_guid: Optional[str] = Field(default=None, description="")
        stakeholder_title: Optional[StakeholderTitle] = Field(
            default=None, description=""
        )  # relationship
        stakeholder_data_domain: Optional[DataDomain] = Field(
            default=None, description=""
        )  # relationship

    attributes: Stakeholder.Attributes = Field(
        default_factory=lambda: Stakeholder.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .data_domain import DataDomain  # noqa
from .stakeholder_title import StakeholderTitle  # noqa
