# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import ADLSLeaseState, ADLSLeaseStatus, AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .a_d_l_s import ADLS


class ADLSContainer(ADLS):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        adls_account_qualified_name: str,
    ) -> ADLSContainer: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        adls_account_qualified_name: str,
        connection_qualified_name: str,
    ) -> ADLSContainer: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        adls_account_qualified_name: str,
        connection_qualified_name: Optional[str] = None,
    ) -> ADLSContainer:
        validate_required_fields(
            ["name", "adls_account_qualified_name"], [name, adls_account_qualified_name]
        )
        attributes = ADLSContainer.Attributes.create(
            name=name,
            adls_account_qualified_name=adls_account_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, adls_account_qualified_name: str) -> ADLSContainer:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name, adls_account_qualified_name=adls_account_qualified_name
        )

    type_name: str = Field(default="ADLSContainer", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADLSContainer":
            raise ValueError("must be ADLSContainer")
        return v

    def __setattr__(self, name, value):
        if name in ADLSContainer._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ADLS_CONTAINER_URL: ClassVar[KeywordTextField] = KeywordTextField(
        "adlsContainerUrl", "adlsContainerUrl.keyword", "adlsContainerUrl"
    )
    """
    URL of this container.
    """
    ADLS_CONTAINER_LEASE_STATE: ClassVar[KeywordField] = KeywordField(
        "adlsContainerLeaseState", "adlsContainerLeaseState"
    )
    """
    Lease state of this container.
    """
    ADLS_CONTAINER_LEASE_STATUS: ClassVar[KeywordField] = KeywordField(
        "adlsContainerLeaseStatus", "adlsContainerLeaseStatus"
    )
    """
    Lease status of this container.
    """
    ADLS_CONTAINER_ENCRYPTION_SCOPE: ClassVar[KeywordField] = KeywordField(
        "adlsContainerEncryptionScope", "adlsContainerEncryptionScope"
    )
    """
    Encryption scope of this container.
    """
    ADLS_CONTAINER_VERSION_LEVEL_IMMUTABILITY_SUPPORT: ClassVar[BooleanField] = (
        BooleanField(
            "adlsContainerVersionLevelImmutabilitySupport",
            "adlsContainerVersionLevelImmutabilitySupport",
        )
    )
    """
    Whether this container supports version-level immutability (true) or not (false).
    """
    ADLS_OBJECT_COUNT: ClassVar[NumericField] = NumericField(
        "adlsObjectCount", "adlsObjectCount"
    )
    """
    Number of objects that exist within this container.
    """

    ADLS_OBJECTS: ClassVar[RelationField] = RelationField("adlsObjects")
    """
    TBC
    """
    ADLS_ACCOUNT: ClassVar[RelationField] = RelationField("adlsAccount")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "adls_container_url",
        "adls_container_lease_state",
        "adls_container_lease_status",
        "adls_container_encryption_scope",
        "adls_container_version_level_immutability_support",
        "adls_object_count",
        "adls_objects",
        "adls_account",
    ]

    @property
    def adls_container_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.adls_container_url

    @adls_container_url.setter
    def adls_container_url(self, adls_container_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_url = adls_container_url

    @property
    def adls_container_lease_state(self) -> Optional[ADLSLeaseState]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_container_lease_state
        )

    @adls_container_lease_state.setter
    def adls_container_lease_state(
        self, adls_container_lease_state: Optional[ADLSLeaseState]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_lease_state = adls_container_lease_state

    @property
    def adls_container_lease_status(self) -> Optional[ADLSLeaseStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_container_lease_status
        )

    @adls_container_lease_status.setter
    def adls_container_lease_status(
        self, adls_container_lease_status: Optional[ADLSLeaseStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_lease_status = adls_container_lease_status

    @property
    def adls_container_encryption_scope(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_container_encryption_scope
        )

    @adls_container_encryption_scope.setter
    def adls_container_encryption_scope(
        self, adls_container_encryption_scope: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_encryption_scope = (
            adls_container_encryption_scope
        )

    @property
    def adls_container_version_level_immutability_support(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_container_version_level_immutability_support
        )

    @adls_container_version_level_immutability_support.setter
    def adls_container_version_level_immutability_support(
        self, adls_container_version_level_immutability_support: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_version_level_immutability_support = (
            adls_container_version_level_immutability_support
        )

    @property
    def adls_object_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.adls_object_count

    @adls_object_count.setter
    def adls_object_count(self, adls_object_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_count = adls_object_count

    @property
    def adls_objects(self) -> Optional[List[ADLSObject]]:
        return None if self.attributes is None else self.attributes.adls_objects

    @adls_objects.setter
    def adls_objects(self, adls_objects: Optional[List[ADLSObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_objects = adls_objects

    @property
    def adls_account(self) -> Optional[ADLSAccount]:
        return None if self.attributes is None else self.attributes.adls_account

    @adls_account.setter
    def adls_account(self, adls_account: Optional[ADLSAccount]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account = adls_account

    class Attributes(ADLS.Attributes):
        adls_container_url: Optional[str] = Field(default=None, description="")
        adls_container_lease_state: Optional[ADLSLeaseState] = Field(
            default=None, description=""
        )
        adls_container_lease_status: Optional[ADLSLeaseStatus] = Field(
            default=None, description=""
        )
        adls_container_encryption_scope: Optional[str] = Field(
            default=None, description=""
        )
        adls_container_version_level_immutability_support: Optional[bool] = Field(
            default=None, description=""
        )
        adls_object_count: Optional[int] = Field(default=None, description="")
        adls_objects: Optional[List[ADLSObject]] = Field(
            default=None, description=""
        )  # relationship
        adls_account: Optional[ADLSAccount] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            adls_account_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
        ) -> ADLSContainer.Attributes:
            validate_required_fields(
                ["name", "adls_account_qualified_name"],
                [name, adls_account_qualified_name],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    adls_account_qualified_name, "adls_account_qualified_name", 4
                )

            return ADLSContainer.Attributes(
                name=name,
                qualified_name=f"{adls_account_qualified_name}/{name}",
                adls_account=ADLSAccount.ref_by_qualified_name(
                    adls_account_qualified_name
                ),
                adls_account_qualified_name=adls_account_qualified_name,
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name or connection_qn,
            )

    attributes: ADLSContainer.Attributes = Field(
        default_factory=lambda: ADLSContainer.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .a_d_l_s_account import ADLSAccount  # noqa
from .a_d_l_s_object import ADLSObject  # noqa
