# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, NumericField

from .asset import Asset


class AuthService(Asset, type_name="AuthService"):
    """Description"""

    type_name: str = Field(default="AuthService", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AuthService":
            raise ValueError("must be AuthService")
        return v

    def __setattr__(self, name, value):
        if name in AuthService._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AUTH_SERVICE_TYPE: ClassVar[KeywordField] = KeywordField(
        "authServiceType", "authServiceType"
    )
    """
    TBC
    """
    TAG_SERVICE: ClassVar[KeywordField] = KeywordField("tagService", "tagService")
    """
    TBC
    """
    AUTH_SERVICE_IS_ENABLED: ClassVar[BooleanField] = BooleanField(
        "authServiceIsEnabled", "authServiceIsEnabled"
    )
    """
    TBC
    """
    AUTH_SERVICE_CONFIG: ClassVar[KeywordField] = KeywordField(
        "authServiceConfig", "authServiceConfig"
    )
    """
    TBC
    """
    AUTH_SERVICE_POLICY_LAST_SYNC: ClassVar[NumericField] = NumericField(
        "authServicePolicyLastSync", "authServicePolicyLastSync"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "auth_service_type",
        "tag_service",
        "auth_service_is_enabled",
        "auth_service_config",
        "auth_service_policy_last_sync",
    ]

    @property
    def auth_service_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.auth_service_type

    @auth_service_type.setter
    def auth_service_type(self, auth_service_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.auth_service_type = auth_service_type

    @property
    def tag_service(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.tag_service

    @tag_service.setter
    def tag_service(self, tag_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tag_service = tag_service

    @property
    def auth_service_is_enabled(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.auth_service_is_enabled
        )

    @auth_service_is_enabled.setter
    def auth_service_is_enabled(self, auth_service_is_enabled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.auth_service_is_enabled = auth_service_is_enabled

    @property
    def auth_service_config(self) -> Optional[Dict[str, str]]:
        return None if self.attributes is None else self.attributes.auth_service_config

    @auth_service_config.setter
    def auth_service_config(self, auth_service_config: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.auth_service_config = auth_service_config

    @property
    def auth_service_policy_last_sync(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.auth_service_policy_last_sync
        )

    @auth_service_policy_last_sync.setter
    def auth_service_policy_last_sync(
        self, auth_service_policy_last_sync: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.auth_service_policy_last_sync = auth_service_policy_last_sync

    class Attributes(Asset.Attributes):
        auth_service_type: Optional[str] = Field(default=None, description="")
        tag_service: Optional[str] = Field(default=None, description="")
        auth_service_is_enabled: Optional[bool] = Field(default=None, description="")
        auth_service_config: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        auth_service_policy_last_sync: Optional[int] = Field(
            default=None, description=""
        )

    attributes: AuthService.Attributes = Field(
        default_factory=lambda: AuthService.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
