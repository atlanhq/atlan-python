# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField
from pyatlan.model.structs import ResponseValue

from .core.asset import Asset


class Response(Asset, type_name="Response"):
    """Description"""

    type_name: str = Field(default="Response", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Response":
            raise ValueError("must be Response")
        return v

    def __setattr__(self, name, value):
        if name in Response._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FORM_GUID: ClassVar[KeywordField] = KeywordField("formGuid", "formGuid")
    """
    Unique identifier of the form.
    """
    RESPONSE_VALUES: ClassVar[KeywordField] = KeywordField(
        "responseValues", "responseValues"
    )
    """
    Fields in a form.
    """
    RESPONSE_OPTIONS: ClassVar[KeywordField] = KeywordField(
        "responseOptions", "responseOptions"
    )
    """
    Options of the response to a form.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "form_guid",
        "response_values",
        "response_options",
    ]

    @property
    def form_guid(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.form_guid

    @form_guid.setter
    def form_guid(self, form_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.form_guid = form_guid

    @property
    def response_values(self) -> Optional[List[ResponseValue]]:
        return None if self.attributes is None else self.attributes.response_values

    @response_values.setter
    def response_values(self, response_values: Optional[List[ResponseValue]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.response_values = response_values

    @property
    def response_options(self) -> Optional[Dict[str, str]]:
        return None if self.attributes is None else self.attributes.response_options

    @response_options.setter
    def response_options(self, response_options: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.response_options = response_options

    class Attributes(Asset.Attributes):
        form_guid: Optional[str] = Field(default=None, description="")
        response_values: Optional[List[ResponseValue]] = Field(
            default=None, description=""
        )
        response_options: Optional[Dict[str, str]] = Field(default=None, description="")

    attributes: Response.Attributes = Field(
        default_factory=lambda: Response.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Response.Attributes.update_forward_refs()
