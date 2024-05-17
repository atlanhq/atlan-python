# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .a_p_i import API


class APISpec(API):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> APISpec:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = APISpec.Attributes.create(
            name=name, connection_qualified_name=connection_qualified_name
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, connection_qualified_name: str) -> APISpec:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )

    type_name: str = Field(default="APISpec", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "APISpec":
            raise ValueError("must be APISpec")
        return v

    def __setattr__(self, name, value):
        if name in APISpec._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    API_SPEC_TERMS_OF_SERVICE_URL: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecTermsOfServiceURL",
        "apiSpecTermsOfServiceURL",
        "apiSpecTermsOfServiceURL.text",
    )
    """
    URL to the terms of service for the API specification.
    """
    API_SPEC_CONTACT_EMAIL: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecContactEmail", "apiSpecContactEmail", "apiSpecContactEmail.text"
    )
    """
    Email address for a contact responsible for the API specification.
    """
    API_SPEC_CONTACT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecContactName", "apiSpecContactName.keyword", "apiSpecContactName"
    )
    """
    Name of the contact responsible for the API specification.
    """
    API_SPEC_CONTACT_URL: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecContactURL", "apiSpecContactURL", "apiSpecContactURL.text"
    )
    """
    URL pointing to the contact information.
    """
    API_SPEC_LICENSE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecLicenseName", "apiSpecLicenseName.keyword", "apiSpecLicenseName"
    )
    """
    Name of the license under which the API specification is available.
    """
    API_SPEC_LICENSE_URL: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecLicenseURL", "apiSpecLicenseURL", "apiSpecLicenseURL.text"
    )
    """
    URL to the license under which the API specification is available.
    """
    API_SPEC_CONTRACT_VERSION: ClassVar[KeywordField] = KeywordField(
        "apiSpecContractVersion", "apiSpecContractVersion"
    )
    """
    Version of the contract for the API specification.
    """
    API_SPEC_SERVICE_ALIAS: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecServiceAlias", "apiSpecServiceAlias", "apiSpecServiceAlias.text"
    )
    """
    Service alias for the API specification.
    """

    API_PATHS: ClassVar[RelationField] = RelationField("apiPaths")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "api_spec_terms_of_service_url",
        "api_spec_contact_email",
        "api_spec_contact_name",
        "api_spec_contact_url",
        "api_spec_license_name",
        "api_spec_license_url",
        "api_spec_contract_version",
        "api_spec_service_alias",
        "api_paths",
    ]

    @property
    def api_spec_terms_of_service_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.api_spec_terms_of_service_url
        )

    @api_spec_terms_of_service_url.setter
    def api_spec_terms_of_service_url(
        self, api_spec_terms_of_service_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_terms_of_service_url = api_spec_terms_of_service_url

    @property
    def api_spec_contact_email(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.api_spec_contact_email
        )

    @api_spec_contact_email.setter
    def api_spec_contact_email(self, api_spec_contact_email: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_contact_email = api_spec_contact_email

    @property
    def api_spec_contact_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.api_spec_contact_name
        )

    @api_spec_contact_name.setter
    def api_spec_contact_name(self, api_spec_contact_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_contact_name = api_spec_contact_name

    @property
    def api_spec_contact_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_spec_contact_url

    @api_spec_contact_url.setter
    def api_spec_contact_url(self, api_spec_contact_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_contact_url = api_spec_contact_url

    @property
    def api_spec_license_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.api_spec_license_name
        )

    @api_spec_license_name.setter
    def api_spec_license_name(self, api_spec_license_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_license_name = api_spec_license_name

    @property
    def api_spec_license_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_spec_license_url

    @api_spec_license_url.setter
    def api_spec_license_url(self, api_spec_license_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_license_url = api_spec_license_url

    @property
    def api_spec_contract_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.api_spec_contract_version
        )

    @api_spec_contract_version.setter
    def api_spec_contract_version(self, api_spec_contract_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_contract_version = api_spec_contract_version

    @property
    def api_spec_service_alias(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.api_spec_service_alias
        )

    @api_spec_service_alias.setter
    def api_spec_service_alias(self, api_spec_service_alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec_service_alias = api_spec_service_alias

    @property
    def api_paths(self) -> Optional[List[APIPath]]:
        return None if self.attributes is None else self.attributes.api_paths

    @api_paths.setter
    def api_paths(self, api_paths: Optional[List[APIPath]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_paths = api_paths

    class Attributes(API.Attributes):
        api_spec_terms_of_service_url: Optional[str] = Field(
            default=None, description=""
        )
        api_spec_contact_email: Optional[str] = Field(default=None, description="")
        api_spec_contact_name: Optional[str] = Field(default=None, description="")
        api_spec_contact_url: Optional[str] = Field(default=None, description="")
        api_spec_license_name: Optional[str] = Field(default=None, description="")
        api_spec_license_url: Optional[str] = Field(default=None, description="")
        api_spec_contract_version: Optional[str] = Field(default=None, description="")
        api_spec_service_alias: Optional[str] = Field(default=None, description="")
        api_paths: Optional[List[APIPath]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls, *, name: str, connection_qualified_name: str
        ) -> APISpec.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return APISpec.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: APISpec.Attributes = Field(
        default_factory=lambda: APISpec.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .a_p_i_path import APIPath  # noqa
