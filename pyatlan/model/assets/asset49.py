# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField

from .asset19 import SaaS


class Salesforce(SaaS):
    """Description"""

    type_name: str = Field("Salesforce", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Salesforce":
            raise ValueError("must be Salesforce")
        return v

    def __setattr__(self, name, value):
        if name in Salesforce._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ORGANIZATION_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "organizationQualifiedName", "organizationQualifiedName"
    )
    """
    TBC
    """
    API_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "apiName", "apiName.keyword", "apiName"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "organization_qualified_name",
        "api_name",
    ]

    @property
    def organization_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.organization_qualified_name
        )

    @organization_qualified_name.setter
    def organization_qualified_name(self, organization_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.organization_qualified_name = organization_qualified_name

    @property
    def api_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_name

    @api_name.setter
    def api_name(self, api_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_name = api_name

    class Attributes(SaaS.Attributes):
        organization_qualified_name: Optional[str] = Field(
            None, description="", alias="organizationQualifiedName"
        )
        api_name: Optional[str] = Field(None, description="", alias="apiName")

    attributes: "Salesforce.Attributes" = Field(
        default_factory=lambda: Salesforce.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


Salesforce.Attributes.update_forward_refs()
