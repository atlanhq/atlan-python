# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .core.asset import Asset


class Cloud(Asset, type_name="Cloud"):
    """Description"""

    type_name: str = Field(default="Cloud", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Cloud":
            raise ValueError("must be Cloud")
        return v

    def __setattr__(self, name, value):
        if name in Cloud._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CLOUD_UNIFORM_RESOURCE_NAME: ClassVar[KeywordField] = KeywordField(
        "cloudUniformResourceName", "cloudUniformResourceName"
    )
    """
    Uniform resource name (URN) for the asset: AWS ARN, Google Cloud URI, Azure resource ID, Oracle OCID, and so on.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cloud_uniform_resource_name",
    ]

    @property
    def cloud_uniform_resource_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cloud_uniform_resource_name
        )

    @cloud_uniform_resource_name.setter
    def cloud_uniform_resource_name(self, cloud_uniform_resource_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cloud_uniform_resource_name = cloud_uniform_resource_name

    class Attributes(Asset.Attributes):
        cloud_uniform_resource_name: Optional[str] = Field(default=None, description="")

    attributes: Cloud.Attributes = Field(
        default_factory=lambda: Cloud.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Cloud.Attributes.update_forward_refs()
