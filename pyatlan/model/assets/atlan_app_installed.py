# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField

from .atlan_app import AtlanApp


class AtlanAppInstalled(AtlanApp):
    """Description"""

    type_name: str = Field(default="AtlanAppInstalled", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlanAppInstalled":
            raise ValueError("must be AtlanAppInstalled")
        return v

    def __setattr__(self, name, value):
        if name in AtlanAppInstalled._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ATLAN_APP_CURRENT_VERSION_ID: ClassVar[NumericField] = NumericField(
        "atlanAppCurrentVersionId", "atlanAppCurrentVersionId"
    )
    """
    Current version identifier for the atlan application.
    """
    ATLAN_APP_DEPLOYMENT_CONFIG: ClassVar[KeywordField] = KeywordField(
        "atlanAppDeploymentConfig", "atlanAppDeploymentConfig"
    )
    """
    Configuration settings used by the atlan application.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "atlan_app_current_version_id",
        "atlan_app_deployment_config",
    ]

    @property
    def atlan_app_current_version_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.atlan_app_current_version_id
        )

    @atlan_app_current_version_id.setter
    def atlan_app_current_version_id(self, atlan_app_current_version_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_current_version_id = atlan_app_current_version_id

    @property
    def atlan_app_deployment_config(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.atlan_app_deployment_config
        )

    @atlan_app_deployment_config.setter
    def atlan_app_deployment_config(self, atlan_app_deployment_config: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_deployment_config = atlan_app_deployment_config

    class Attributes(AtlanApp.Attributes):
        atlan_app_current_version_id: Optional[int] = Field(
            default=None, description=""
        )
        atlan_app_deployment_config: Optional[str] = Field(default=None, description="")

    attributes: AtlanAppInstalled.Attributes = Field(
        default_factory=lambda: AtlanAppInstalled.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


AtlanAppInstalled.Attributes.update_forward_refs()
