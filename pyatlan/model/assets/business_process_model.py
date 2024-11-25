# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .core.catalog import Catalog


class BusinessProcessModel(Catalog):
    """Description"""

    type_name: str = Field(default="BusinessProcessModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "BusinessProcessModel":
            raise ValueError("must be BusinessProcessModel")
        return v

    def __setattr__(self, name, value):
        if name in BusinessProcessModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    BUSINESS_PROCESS_MODEL_TYPE: ClassVar[KeywordField] = KeywordField(
        "businessProcessModelType", "businessProcessModelType"
    )
    """
    Type attribute for the BusinessProcessModel asset to help distinguish the entity type.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "business_process_model_type",
    ]

    @property
    def business_process_model_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_process_model_type
        )

    @business_process_model_type.setter
    def business_process_model_type(self, business_process_model_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_process_model_type = business_process_model_type

    class Attributes(Catalog.Attributes):
        business_process_model_type: Optional[str] = Field(default=None, description="")

    attributes: BusinessProcessModel.Attributes = Field(
        default_factory=lambda: BusinessProcessModel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


BusinessProcessModel.Attributes.update_forward_refs()
