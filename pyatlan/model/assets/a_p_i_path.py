# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    RelationField,
    TextField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .a_p_i import API


class APIPath(API):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(cls, *, path_raw_uri: str, spec_qualified_name: str) -> APIPath:
        validate_required_fields(
            ["path_raw_uri", "spec_qualified_name"], [path_raw_uri, spec_qualified_name]
        )
        attributes = APIPath.Attributes.create(
            path_raw_uri=path_raw_uri, spec_qualified_name=spec_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="APIPath", allow_mutation=False)

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
    Descriptive summary intended to apply to all operations in this path.
    """
    API_PATH_RAW_URI: ClassVar[KeywordTextField] = KeywordTextField(
        "apiPathRawURI", "apiPathRawURI", "apiPathRawURI.text"
    )
    """
    Absolute path to an individual endpoint.
    """
    API_PATH_IS_TEMPLATED: ClassVar[BooleanField] = BooleanField(
        "apiPathIsTemplated", "apiPathIsTemplated"
    )
    """
    Whether the endpoint's path contains replaceable parameters (true) or not (false).
    """
    API_PATH_AVAILABLE_OPERATIONS: ClassVar[KeywordField] = KeywordField(
        "apiPathAvailableOperations", "apiPathAvailableOperations"
    )
    """
    List of the operations available on the endpoint.
    """
    API_PATH_AVAILABLE_RESPONSE_CODES: ClassVar[KeywordField] = KeywordField(
        "apiPathAvailableResponseCodes", "apiPathAvailableResponseCodes"
    )
    """
    Response codes available on the path across all operations.
    """
    API_PATH_IS_INGRESS_EXPOSED: ClassVar[BooleanField] = BooleanField(
        "apiPathIsIngressExposed", "apiPathIsIngressExposed"
    )
    """
    Whether the path is exposed as an ingress (true) or not (false).
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
        api_path_summary: Optional[str] = Field(default=None, description="")
        api_path_raw_u_r_i: Optional[str] = Field(default=None, description="")
        api_path_is_templated: Optional[bool] = Field(default=None, description="")
        api_path_available_operations: Optional[set[str]] = Field(
            default=None, description=""
        )
        api_path_available_response_codes: Optional[dict[str, str]] = Field(
            default=None, description=""
        )
        api_path_is_ingress_exposed: Optional[bool] = Field(
            default=None, description=""
        )
        api_spec: Optional[APISpec] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, *, path_raw_uri: str, spec_qualified_name: str
        ) -> APIPath.Attributes:
            validate_required_fields(
                ["path_raw_uri", "spec_qualified_name"],
                [path_raw_uri, spec_qualified_name],
            )

            # Split the spec_qualified_name to extract necessary information
            fields = spec_qualified_name.split("/")
            if len(fields) != 4:
                raise ValueError("Invalid spec_qualified_name")

            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid spec_qualified_name") from e

            return APIPath.Attributes(
                api_path_raw_u_r_i=path_raw_uri,
                name=path_raw_uri,
                api_spec_qualified_name=spec_qualified_name,
                connection_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}",
                qualified_name=f"{spec_qualified_name}{path_raw_uri}",
                connector_name=connector_type.value,
                api_spec=APISpec.ref_by_qualified_name(spec_qualified_name),
            )

    attributes: "APIPath.Attributes" = Field(
        default_factory=lambda: APIPath.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


from .a_p_i_spec import APISpec  # noqa: E402