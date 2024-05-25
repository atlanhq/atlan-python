# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .asset import Asset


class StakeholderTitle(Asset, type_name="StakeholderTitle"):
    """Description"""

    type_name: str = Field(default="StakeholderTitle", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "StakeholderTitle":
            raise ValueError("must be StakeholderTitle")
        return v

    def __setattr__(self, name, value):
        if name in StakeholderTitle._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    STAKEHOLDER_TITLE_DOMAIN_QUALIFIED_NAMES: ClassVar[KeywordField] = KeywordField(
        "stakeholderTitleDomainQualifiedNames", "stakeholderTitleDomainQualifiedNames"
    )
    """
    qualified name array representing the Domains for which this StakeholderTitle is applicable
    """

    STAKEHOLDERS: ClassVar[RelationField] = RelationField("stakeholders")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "stakeholder_title_domain_qualified_names",
        "stakeholders",
    ]

    @property
    def stakeholder_title_domain_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.stakeholder_title_domain_qualified_names
        )

    @stakeholder_title_domain_qualified_names.setter
    def stakeholder_title_domain_qualified_names(
        self, stakeholder_title_domain_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.stakeholder_title_domain_qualified_names = (
            stakeholder_title_domain_qualified_names
        )

    @property
    def stakeholders(self) -> Optional[List[Stakeholder]]:
        return None if self.attributes is None else self.attributes.stakeholders

    @stakeholders.setter
    def stakeholders(self, stakeholders: Optional[List[Stakeholder]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.stakeholders = stakeholders

    class Attributes(Asset.Attributes):
        stakeholder_title_domain_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        stakeholders: Optional[List[Stakeholder]] = Field(
            default=None, description=""
        )  # relationship

    attributes: StakeholderTitle.Attributes = Field(
        default_factory=lambda: StakeholderTitle.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .stakeholder import Stakeholder  # noqa
