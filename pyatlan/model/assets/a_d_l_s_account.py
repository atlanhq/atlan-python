# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import (
    ADLSAccessTier,
    ADLSAccountStatus,
    ADLSEncryptionTypes,
    ADLSPerformance,
    ADLSProvisionState,
    ADLSReplicationType,
    ADLSStorageKind,
    AtlanConnectorType,
)
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .a_d_l_s import ADLS


class ADLSAccount(ADLS):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> ADLSAccount:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = ADLSAccount.Attributes.create(
            name=name, connection_qualified_name=connection_qualified_name
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, connection_qualified_name: str) -> ADLSAccount:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )

    type_name: str = Field(default="ADLSAccount", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADLSAccount":
            raise ValueError("must be ADLSAccount")
        return v

    def __setattr__(self, name, value):
        if name in ADLSAccount._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ADLS_E_TAG: ClassVar[KeywordField] = KeywordField("adlsETag", "adlsETag")
    """
    Entity tag for the asset. An entity tag is a hash of the object and represents changes to the contents of an object only, not its metadata.
    """  # noqa: E501
    ADLS_ENCRYPTION_TYPE: ClassVar[KeywordField] = KeywordField(
        "adlsEncryptionType", "adlsEncryptionType"
    )
    """
    Type of encryption for this account.
    """
    ADLS_ACCOUNT_RESOURCE_GROUP: ClassVar[KeywordTextField] = KeywordTextField(
        "adlsAccountResourceGroup",
        "adlsAccountResourceGroup.keyword",
        "adlsAccountResourceGroup",
    )
    """
    Resource group for this account.
    """
    ADLS_ACCOUNT_SUBSCRIPTION: ClassVar[KeywordTextField] = KeywordTextField(
        "adlsAccountSubscription",
        "adlsAccountSubscription.keyword",
        "adlsAccountSubscription",
    )
    """
    Subscription for this account.
    """
    ADLS_ACCOUNT_PERFORMANCE: ClassVar[KeywordField] = KeywordField(
        "adlsAccountPerformance", "adlsAccountPerformance"
    )
    """
    Performance of this account.
    """
    ADLS_ACCOUNT_REPLICATION: ClassVar[KeywordField] = KeywordField(
        "adlsAccountReplication", "adlsAccountReplication"
    )
    """
    Replication of this account.
    """
    ADLS_ACCOUNT_KIND: ClassVar[KeywordField] = KeywordField(
        "adlsAccountKind", "adlsAccountKind"
    )
    """
    Kind of this account.
    """
    ADLS_PRIMARY_DISK_STATE: ClassVar[KeywordField] = KeywordField(
        "adlsPrimaryDiskState", "adlsPrimaryDiskState"
    )
    """
    Primary disk state of this account.
    """
    ADLS_ACCOUNT_PROVISION_STATE: ClassVar[KeywordField] = KeywordField(
        "adlsAccountProvisionState", "adlsAccountProvisionState"
    )
    """
    Provision state of this account.
    """
    ADLS_ACCOUNT_ACCESS_TIER: ClassVar[KeywordField] = KeywordField(
        "adlsAccountAccessTier", "adlsAccountAccessTier"
    )
    """
    Access tier of this account.
    """

    ADLS_CONTAINERS: ClassVar[RelationField] = RelationField("adlsContainers")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "adls_e_tag",
        "adls_encryption_type",
        "adls_account_resource_group",
        "adls_account_subscription",
        "adls_account_performance",
        "adls_account_replication",
        "adls_account_kind",
        "adls_primary_disk_state",
        "adls_account_provision_state",
        "adls_account_access_tier",
        "adls_containers",
    ]

    @property
    def adls_e_tag(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.adls_e_tag

    @adls_e_tag.setter
    def adls_e_tag(self, adls_e_tag: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_e_tag = adls_e_tag

    @property
    def adls_encryption_type(self) -> Optional[ADLSEncryptionTypes]:
        return None if self.attributes is None else self.attributes.adls_encryption_type

    @adls_encryption_type.setter
    def adls_encryption_type(self, adls_encryption_type: Optional[ADLSEncryptionTypes]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_encryption_type = adls_encryption_type

    @property
    def adls_account_resource_group(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_resource_group
        )

    @adls_account_resource_group.setter
    def adls_account_resource_group(self, adls_account_resource_group: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_resource_group = adls_account_resource_group

    @property
    def adls_account_subscription(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_subscription
        )

    @adls_account_subscription.setter
    def adls_account_subscription(self, adls_account_subscription: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_subscription = adls_account_subscription

    @property
    def adls_account_performance(self) -> Optional[ADLSPerformance]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_performance
        )

    @adls_account_performance.setter
    def adls_account_performance(
        self, adls_account_performance: Optional[ADLSPerformance]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_performance = adls_account_performance

    @property
    def adls_account_replication(self) -> Optional[ADLSReplicationType]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_replication
        )

    @adls_account_replication.setter
    def adls_account_replication(
        self, adls_account_replication: Optional[ADLSReplicationType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_replication = adls_account_replication

    @property
    def adls_account_kind(self) -> Optional[ADLSStorageKind]:
        return None if self.attributes is None else self.attributes.adls_account_kind

    @adls_account_kind.setter
    def adls_account_kind(self, adls_account_kind: Optional[ADLSStorageKind]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_kind = adls_account_kind

    @property
    def adls_primary_disk_state(self) -> Optional[ADLSAccountStatus]:
        return (
            None if self.attributes is None else self.attributes.adls_primary_disk_state
        )

    @adls_primary_disk_state.setter
    def adls_primary_disk_state(
        self, adls_primary_disk_state: Optional[ADLSAccountStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_primary_disk_state = adls_primary_disk_state

    @property
    def adls_account_provision_state(self) -> Optional[ADLSProvisionState]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_provision_state
        )

    @adls_account_provision_state.setter
    def adls_account_provision_state(
        self, adls_account_provision_state: Optional[ADLSProvisionState]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_provision_state = adls_account_provision_state

    @property
    def adls_account_access_tier(self) -> Optional[ADLSAccessTier]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_access_tier
        )

    @adls_account_access_tier.setter
    def adls_account_access_tier(
        self, adls_account_access_tier: Optional[ADLSAccessTier]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_access_tier = adls_account_access_tier

    @property
    def adls_containers(self) -> Optional[List[ADLSContainer]]:
        return None if self.attributes is None else self.attributes.adls_containers

    @adls_containers.setter
    def adls_containers(self, adls_containers: Optional[List[ADLSContainer]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_containers = adls_containers

    class Attributes(ADLS.Attributes):
        adls_e_tag: Optional[str] = Field(default=None, description="")
        adls_encryption_type: Optional[ADLSEncryptionTypes] = Field(
            default=None, description=""
        )
        adls_account_resource_group: Optional[str] = Field(default=None, description="")
        adls_account_subscription: Optional[str] = Field(default=None, description="")
        adls_account_performance: Optional[ADLSPerformance] = Field(
            default=None, description=""
        )
        adls_account_replication: Optional[ADLSReplicationType] = Field(
            default=None, description=""
        )
        adls_account_kind: Optional[ADLSStorageKind] = Field(
            default=None, description=""
        )
        adls_primary_disk_state: Optional[ADLSAccountStatus] = Field(
            default=None, description=""
        )
        adls_account_provision_state: Optional[ADLSProvisionState] = Field(
            default=None, description=""
        )
        adls_account_access_tier: Optional[ADLSAccessTier] = Field(
            default=None, description=""
        )
        adls_containers: Optional[List[ADLSContainer]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls, *, name: str, connection_qualified_name: str
        ) -> ADLSAccount.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return ADLSAccount.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: ADLSAccount.Attributes = Field(
        default_factory=lambda: ADLSAccount.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .a_d_l_s_container import ADLSContainer  # noqa
