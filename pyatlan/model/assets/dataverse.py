# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField

from .saa_s import SaaS


class Dataverse(SaaS):
    """Description"""

    type_name: str = Field(default="Dataverse", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Dataverse":
            raise ValueError("must be Dataverse")
        return v

    def __setattr__(self, name, value):
        if name in Dataverse._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATAVERSE_IS_CUSTOM: ClassVar[BooleanField] = BooleanField(
        "dataverseIsCustom", "dataverseIsCustom"
    )
    """
    Indicator if DataverseEntity is custom built.
    """
    DATAVERSE_IS_CUSTOMIZABLE: ClassVar[BooleanField] = BooleanField(
        "dataverseIsCustomizable", "dataverseIsCustomizable"
    )
    """
    Indicator if DataverseEntity is customizable.
    """
    DATAVERSE_IS_AUDIT_ENABLED: ClassVar[BooleanField] = BooleanField(
        "dataverseIsAuditEnabled", "dataverseIsAuditEnabled"
    )
    """
    Indicator if DataverseEntity has auditing enabled.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dataverse_is_custom",
        "dataverse_is_customizable",
        "dataverse_is_audit_enabled",
    ]

    @property
    def dataverse_is_custom(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.dataverse_is_custom

    @dataverse_is_custom.setter
    def dataverse_is_custom(self, dataverse_is_custom: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataverse_is_custom = dataverse_is_custom

    @property
    def dataverse_is_customizable(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.dataverse_is_customizable
        )

    @dataverse_is_customizable.setter
    def dataverse_is_customizable(self, dataverse_is_customizable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataverse_is_customizable = dataverse_is_customizable

    @property
    def dataverse_is_audit_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.dataverse_is_audit_enabled
        )

    @dataverse_is_audit_enabled.setter
    def dataverse_is_audit_enabled(self, dataverse_is_audit_enabled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataverse_is_audit_enabled = dataverse_is_audit_enabled

    class Attributes(SaaS.Attributes):
        dataverse_is_custom: Optional[bool] = Field(default=None, description="")
        dataverse_is_customizable: Optional[bool] = Field(default=None, description="")
        dataverse_is_audit_enabled: Optional[bool] = Field(default=None, description="")

    attributes: Dataverse.Attributes = Field(
        default_factory=lambda: Dataverse.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Dataverse.Attributes.update_forward_refs()
