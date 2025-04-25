# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField
from pyatlan.model.structs import FormField

from .core.asset import Asset


class Form(Asset, type_name="Form"):
    """Description"""

    type_name: str = Field(default="Form", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Form":
            raise ValueError("must be Form")
        return v

    def __setattr__(self, name, value):
        if name in Form._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FORM_FIELDS: ClassVar[KeywordField] = KeywordField("formFields", "formFields")
    """
    Fields in a form.
    """
    FORM_OPTIONS: ClassVar[KeywordField] = KeywordField("formOptions", "formOptions")
    """
    Options of the form.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "form_fields",
        "form_options",
    ]

    @property
    def form_fields(self) -> Optional[List[FormField]]:
        return None if self.attributes is None else self.attributes.form_fields

    @form_fields.setter
    def form_fields(self, form_fields: Optional[List[FormField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.form_fields = form_fields

    @property
    def form_options(self) -> Optional[Dict[str, str]]:
        return None if self.attributes is None else self.attributes.form_options

    @form_options.setter
    def form_options(self, form_options: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.form_options = form_options

    class Attributes(Asset.Attributes):
        form_fields: Optional[List[FormField]] = Field(default=None, description="")
        form_options: Optional[Dict[str, str]] = Field(default=None, description="")

    attributes: Form.Attributes = Field(
        default_factory=lambda: Form.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Form.Attributes.update_forward_refs()
