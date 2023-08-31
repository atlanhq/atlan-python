# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    RelationField,
    TextField,
)

from .asset24 import API


class APISpec(API):
    """Description"""

    type_name: str = Field("APISpec", allow_mutation=False)

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
    TBC
    """
    API_SPEC_CONTACT_EMAIL: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecContactEmail", "apiSpecContactEmail", "apiSpecContactEmail.text"
    )
    """
    TBC
    """
    API_SPEC_CONTACT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecContactName", "apiSpecContactName.keyword", "apiSpecContactName"
    )
    """
    TBC
    """
    API_SPEC_CONTACT_URL: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecContactURL", "apiSpecContactURL", "apiSpecContactURL.text"
    )
    """
    TBC
    """
    API_SPEC_LICENSE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecLicenseName", "apiSpecLicenseName.keyword", "apiSpecLicenseName"
    )
    """
    TBC
    """
    API_SPEC_LICENSE_URL: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecLicenseURL", "apiSpecLicenseURL", "apiSpecLicenseURL.text"
    )
    """
    TBC
    """
    API_SPEC_CONTRACT_VERSION: ClassVar[KeywordField] = KeywordField(
        "apiSpecContractVersion", "apiSpecContractVersion"
    )
    """
    TBC
    """
    API_SPEC_SERVICE_ALIAS: ClassVar[KeywordTextField] = KeywordTextField(
        "apiSpecServiceAlias", "apiSpecServiceAlias", "apiSpecServiceAlias.text"
    )
    """
    TBC
    """

    API_PATHS: ClassVar[RelationField] = RelationField("apiPaths")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
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
    def api_paths(self) -> Optional[list[APIPath]]:
        return None if self.attributes is None else self.attributes.api_paths

    @api_paths.setter
    def api_paths(self, api_paths: Optional[list[APIPath]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_paths = api_paths

    class Attributes(API.Attributes):
        api_spec_terms_of_service_url: Optional[str] = Field(
            None, description="", alias="apiSpecTermsOfServiceURL"
        )
        api_spec_contact_email: Optional[str] = Field(
            None, description="", alias="apiSpecContactEmail"
        )
        api_spec_contact_name: Optional[str] = Field(
            None, description="", alias="apiSpecContactName"
        )
        api_spec_contact_url: Optional[str] = Field(
            None, description="", alias="apiSpecContactURL"
        )
        api_spec_license_name: Optional[str] = Field(
            None, description="", alias="apiSpecLicenseName"
        )
        api_spec_license_url: Optional[str] = Field(
            None, description="", alias="apiSpecLicenseURL"
        )
        api_spec_contract_version: Optional[str] = Field(
            None, description="", alias="apiSpecContractVersion"
        )
        api_spec_service_alias: Optional[str] = Field(
            None, description="", alias="apiSpecServiceAlias"
        )
        api_paths: Optional[list[APIPath]] = Field(
            None, description="", alias="apiPaths"
        )  # relationship

    attributes: "APISpec.Attributes" = Field(
        default_factory=lambda: APISpec.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class APIPath(API):
    """Description"""

    type_name: str = Field("APIPath", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "APIPath":
            raise ValueError("must be APIPath")
        return v

    def __setattr__(self, name, value):
        if name in APIPath._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    API_PATH_SUMMARY: ClassVar[TextField] = TextField(
        "apiPathSummary", "apiPathSummary"
    )
    """
    TBC
    """
    API_PATH_RAW_URI: ClassVar[KeywordTextField] = KeywordTextField(
        "apiPathRawURI", "apiPathRawURI", "apiPathRawURI.text"
    )
    """
    TBC
    """
    API_PATH_IS_TEMPLATED: ClassVar[BooleanField] = BooleanField(
        "apiPathIsTemplated", "apiPathIsTemplated"
    )
    """
    TBC
    """
    API_PATH_AVAILABLE_OPERATIONS: ClassVar[KeywordField] = KeywordField(
        "apiPathAvailableOperations", "apiPathAvailableOperations"
    )
    """
    TBC
    """
    API_PATH_AVAILABLE_RESPONSE_CODES: ClassVar[KeywordField] = KeywordField(
        "apiPathAvailableResponseCodes", "apiPathAvailableResponseCodes"
    )
    """
    TBC
    """
    API_PATH_IS_INGRESS_EXPOSED: ClassVar[BooleanField] = BooleanField(
        "apiPathIsIngressExposed", "apiPathIsIngressExposed"
    )
    """
    TBC
    """

    API_SPEC: ClassVar[RelationField] = RelationField("apiSpec")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "api_path_summary",
        "api_path_raw_u_r_i",
        "api_path_is_templated",
        "api_path_available_operations",
        "api_path_available_response_codes",
        "api_path_is_ingress_exposed",
        "api_spec",
    ]

    @property
    def api_path_summary(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_path_summary

    @api_path_summary.setter
    def api_path_summary(self, api_path_summary: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_summary = api_path_summary

    @property
    def api_path_raw_u_r_i(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_path_raw_u_r_i

    @api_path_raw_u_r_i.setter
    def api_path_raw_u_r_i(self, api_path_raw_u_r_i: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_raw_u_r_i = api_path_raw_u_r_i

    @property
    def api_path_is_templated(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.api_path_is_templated
        )

    @api_path_is_templated.setter
    def api_path_is_templated(self, api_path_is_templated: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_is_templated = api_path_is_templated

    @property
    def api_path_available_operations(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.api_path_available_operations
        )

    @api_path_available_operations.setter
    def api_path_available_operations(
        self, api_path_available_operations: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_available_operations = api_path_available_operations

    @property
    def api_path_available_response_codes(self) -> Optional[dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.api_path_available_response_codes
        )

    @api_path_available_response_codes.setter
    def api_path_available_response_codes(
        self, api_path_available_response_codes: Optional[dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_available_response_codes = (
            api_path_available_response_codes
        )

    @property
    def api_path_is_ingress_exposed(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.api_path_is_ingress_exposed
        )

    @api_path_is_ingress_exposed.setter
    def api_path_is_ingress_exposed(self, api_path_is_ingress_exposed: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_path_is_ingress_exposed = api_path_is_ingress_exposed

    @property
    def api_spec(self) -> Optional[APISpec]:
        return None if self.attributes is None else self.attributes.api_spec

    @api_spec.setter
    def api_spec(self, api_spec: Optional[APISpec]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_spec = api_spec

    class Attributes(API.Attributes):
        api_path_summary: Optional[str] = Field(
            None, description="", alias="apiPathSummary"
        )
        api_path_raw_u_r_i: Optional[str] = Field(
            None, description="", alias="apiPathRawURI"
        )
        api_path_is_templated: Optional[bool] = Field(
            None, description="", alias="apiPathIsTemplated"
        )
        api_path_available_operations: Optional[set[str]] = Field(
            None, description="", alias="apiPathAvailableOperations"
        )
        api_path_available_response_codes: Optional[dict[str, str]] = Field(
            None, description="", alias="apiPathAvailableResponseCodes"
        )
        api_path_is_ingress_exposed: Optional[bool] = Field(
            None, description="", alias="apiPathIsIngressExposed"
        )
        api_spec: Optional[APISpec] = Field(
            None, description="", alias="apiSpec"
        )  # relationship

    attributes: "APIPath.Attributes" = Field(
        default_factory=lambda: APIPath.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


APISpec.Attributes.update_forward_refs()


APIPath.Attributes.update_forward_refs()
