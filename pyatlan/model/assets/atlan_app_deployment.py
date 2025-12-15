# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanAppDeploymentOperation, AtlanAppDeploymentStatus
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField

from .atlan_app import AtlanApp


class AtlanAppDeployment(AtlanApp):
    """Description"""

    type_name: str = Field(default="AtlanAppDeployment", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlanAppDeployment":
            raise ValueError("must be AtlanAppDeployment")
        return v

    def __setattr__(self, name, value):
        if name in AtlanAppDeployment._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ATLAN_APP_VERSION_ID: ClassVar[NumericField] = NumericField(
        "atlanAppVersionId", "atlanAppVersionId"
    )
    """
    Version identifier for deployment.
    """
    ATLAN_APP_STATUS: ClassVar[KeywordField] = KeywordField(
        "atlanAppStatus", "atlanAppStatus"
    )
    """
    Status of deployment.
    """
    ATLAN_APP_OPERATION: ClassVar[KeywordField] = KeywordField(
        "atlanAppOperation", "atlanAppOperation"
    )
    """
    Type of operation requested.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "atlan_app_version_id",
        "atlan_app_status",
        "atlan_app_operation",
    ]

    @property
    def atlan_app_version_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.atlan_app_version_id

    @atlan_app_version_id.setter
    def atlan_app_version_id(self, atlan_app_version_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_version_id = atlan_app_version_id

    @property
    def atlan_app_status(self) -> Optional[AtlanAppDeploymentStatus]:
        return None if self.attributes is None else self.attributes.atlan_app_status

    @atlan_app_status.setter
    def atlan_app_status(self, atlan_app_status: Optional[AtlanAppDeploymentStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_status = atlan_app_status

    @property
    def atlan_app_operation(self) -> Optional[AtlanAppDeploymentOperation]:
        return None if self.attributes is None else self.attributes.atlan_app_operation

    @atlan_app_operation.setter
    def atlan_app_operation(
        self, atlan_app_operation: Optional[AtlanAppDeploymentOperation]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_operation = atlan_app_operation

    class Attributes(AtlanApp.Attributes):
        atlan_app_version_id: Optional[int] = Field(default=None, description="")
        atlan_app_status: Optional[AtlanAppDeploymentStatus] = Field(
            default=None, description=""
        )
        atlan_app_operation: Optional[AtlanAppDeploymentOperation] = Field(
            default=None, description=""
        )

    attributes: AtlanAppDeployment.Attributes = Field(
        default_factory=lambda: AtlanAppDeployment.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


AtlanAppDeployment.Attributes.update_forward_refs()
