# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, field_validator

from .asset00 import Catalog


class API(Catalog):
    """Description"""

    type_name: str = Field("API", frozen=False)

    @field_validator("type_name")
    @classmethod
    def validate_type_name(cls, v):
        if v != "API":
            raise ValueError("must be API")
        return v

    def __setattr__(self, name, value):
        if name in API._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "api_spec_type",
        "api_spec_version",
        "api_spec_name",
        "api_spec_qualified_name",
        "api_external_docs",
        "api_is_auth_optional",
    ]

    @property
    def api_spec_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_spec_type

    @api_spec_type.setter
    def api_spec_type(self, api_spec_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_type = api_spec_type

    @property
    def api_spec_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_spec_version

    @api_spec_version.setter
    def api_spec_version(self, api_spec_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_version = api_spec_version

    @property
    def api_spec_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_spec_name

    @api_spec_name.setter
    def api_spec_name(self, api_spec_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_name = api_spec_name

    @property
    def api_spec_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.api_spec_qualified_name
        )

    @api_spec_qualified_name.setter
    def api_spec_qualified_name(self, api_spec_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_qualified_name = api_spec_qualified_name

    @property
    def api_external_docs(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.api_external_docs

    @api_external_docs.setter
    def api_external_docs(self, api_external_docs: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_external_docs = api_external_docs

    @property
    def api_is_auth_optional(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.api_is_auth_optional

    @api_is_auth_optional.setter
    def api_is_auth_optional(self, api_is_auth_optional: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_is_auth_optional = api_is_auth_optional

    class Attributes(Catalog.Attributes):
        api_spec_type: Optional[str] = Field(
            default=None, description="", alias="apiSpecType"
        )

        api_spec_version: Optional[str] = Field(
            default=None, description="", alias="apiSpecVersion"
        )

        api_spec_name: Optional[str] = Field(
            default=None, description="", alias="apiSpecName"
        )

        api_spec_qualified_name: Optional[str] = Field(
            default=None, description="", alias="apiSpecQualifiedName"
        )

        api_external_docs: Optional[dict[str, str]] = Field(
            default=None, description="", alias="apiExternalDocs"
        )

        api_is_auth_optional: Optional[bool] = Field(
            default=None, description="", alias="apiIsAuthOptional"
        )

    attributes: "API.Attributes" = Field(
        default_factory=lambda: API.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


API.Attributes.update_forward_refs()
