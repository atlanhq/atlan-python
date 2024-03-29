# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
)

from .catalog import Catalog


class API(Catalog):
    """Description"""

    type_name: str = Field(default="API", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "API":
            raise ValueError("must be API")
        return v

    def __setattr__(self, name, value):
        if name in API._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    API_SPEC_TYPE: ClassVar[KeywordField] = KeywordField("apiSpecType", "apiSpecType")
    """
    Type of API, for example: OpenAPI, GraphQL, etc.
    """
    API_SPEC_VERSION: ClassVar[KeywordField] = KeywordField(
        "apiSpecVersion", "apiSpecVersion"
    )
    """
    Version of the API specification.
    """
    API_SPEC_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecName", "apiSpecName.keyword", "apiSpecName"
    )
    """
    Simple name of the API spec, if this asset is contained in an API spec.
    """
    API_SPEC_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecQualifiedName", "apiSpecQualifiedName", "apiSpecQualifiedName.text"
    )
    """
    Unique name of the API spec, if this asset is contained in an API spec.
    """
    API_EXTERNAL_DOCS: ClassVar[KeywordField] = KeywordField(
        "apiExternalDocs", "apiExternalDocs"
    )
    """
    External documentation of the API.
    """
    API_IS_AUTH_OPTIONAL: ClassVar[BooleanField] = BooleanField(
        "apiIsAuthOptional", "apiIsAuthOptional"
    )
    """
    Whether authentication is optional (true) or required (false).
    """

    _convenience_properties: ClassVar[List[str]] = [
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
    def api_external_docs(self) -> Optional[Dict[str, str]]:
        return None if self.attributes is None else self.attributes.api_external_docs

    @api_external_docs.setter
    def api_external_docs(self, api_external_docs: Optional[Dict[str, str]]):
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
        api_spec_type: Optional[str] = Field(default=None, description="")
        api_spec_version: Optional[str] = Field(default=None, description="")
        api_spec_name: Optional[str] = Field(default=None, description="")
        api_spec_qualified_name: Optional[str] = Field(default=None, description="")
        api_external_docs: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        api_is_auth_optional: Optional[bool] = Field(default=None, description="")

    attributes: API.Attributes = Field(
        default_factory=lambda: API.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
