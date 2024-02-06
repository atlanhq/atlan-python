# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.enums import (
    ADLSAccessTier,
    ADLSAccountStatus,
    ADLSEncryptionTypes,
    ADLSLeaseState,
    ADLSLeaseStatus,
    ADLSObjectArchiveStatus,
    ADLSObjectType,
    ADLSPerformance,
    ADLSProvisionState,
    ADLSReplicationType,
    ADLSStorageKind,
    AtlanConnectorType,
)
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.utils import get_parent_qualified_name, init_guid, validate_required_fields

from .asset36 import ADLS


class ADLSAccount(ADLS):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(cls, *, name: str, connection_qualified_name: str) -> ADLSAccount:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = ADLSAccount.Attributes.create(
            name=name, connection_qualified_name=connection_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field("ADLSAccount", allow_mutation=False)

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

    _convenience_properties: ClassVar[list[str]] = [
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
    def adls_containers(self) -> Optional[list[ADLSContainer]]:
        return None if self.attributes is None else self.attributes.adls_containers

    @adls_containers.setter
    def adls_containers(self, adls_containers: Optional[list[ADLSContainer]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_containers = adls_containers

    class Attributes(ADLS.Attributes):
        adls_e_tag: Optional[str] = Field(None, description="", alias="adlsETag")
        adls_encryption_type: Optional[ADLSEncryptionTypes] = Field(
            None, description="", alias="adlsEncryptionType"
        )
        adls_account_resource_group: Optional[str] = Field(
            None, description="", alias="adlsAccountResourceGroup"
        )
        adls_account_subscription: Optional[str] = Field(
            None, description="", alias="adlsAccountSubscription"
        )
        adls_account_performance: Optional[ADLSPerformance] = Field(
            None, description="", alias="adlsAccountPerformance"
        )
        adls_account_replication: Optional[ADLSReplicationType] = Field(
            None, description="", alias="adlsAccountReplication"
        )
        adls_account_kind: Optional[ADLSStorageKind] = Field(
            None, description="", alias="adlsAccountKind"
        )
        adls_primary_disk_state: Optional[ADLSAccountStatus] = Field(
            None, description="", alias="adlsPrimaryDiskState"
        )
        adls_account_provision_state: Optional[ADLSProvisionState] = Field(
            None, description="", alias="adlsAccountProvisionState"
        )
        adls_account_access_tier: Optional[ADLSAccessTier] = Field(
            None, description="", alias="adlsAccountAccessTier"
        )
        adls_containers: Optional[list[ADLSContainer]] = Field(
            None, description="", alias="adlsContainers"
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, *, name: str, connection_qualified_name: str
        ) -> ADLSAccount.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )

            # Split the connection_qualified_name to extract necessary information
            fields = connection_qualified_name.split("/")
            if len(fields) != 3:
                raise ValueError("Invalid connection_qualified_name")

            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid connection_qualified_name") from e

            return ADLSAccount.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=connector_type.value,
            )

    attributes: "ADLSAccount.Attributes" = Field(
        default_factory=lambda: ADLSAccount.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ADLSContainer(ADLS):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(cls, *, name: str, adls_account_qualified_name: str) -> ADLSContainer:
        validate_required_fields(
            ["name", "adls_account_qualified_name"], [name, adls_account_qualified_name]
        )
        attributes = ADLSContainer.Attributes.create(
            name=name, adls_account_qualified_name=adls_account_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field("ADLSContainer", allow_mutation=False)

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
    ADLS_CONTAINER_VERSION_LEVEL_IMMUTABILITY_SUPPORT: ClassVar[
        BooleanField
    ] = BooleanField(
        "adlsContainerVersionLevelImmutabilitySupport",
        "adlsContainerVersionLevelImmutabilitySupport",
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

    _convenience_properties: ClassVar[list[str]] = [
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
    def adls_objects(self) -> Optional[list[ADLSObject]]:
        return None if self.attributes is None else self.attributes.adls_objects

    @adls_objects.setter
    def adls_objects(self, adls_objects: Optional[list[ADLSObject]]):
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
        adls_container_url: Optional[str] = Field(
            None, description="", alias="adlsContainerUrl"
        )
        adls_container_lease_state: Optional[ADLSLeaseState] = Field(
            None, description="", alias="adlsContainerLeaseState"
        )
        adls_container_lease_status: Optional[ADLSLeaseStatus] = Field(
            None, description="", alias="adlsContainerLeaseStatus"
        )
        adls_container_encryption_scope: Optional[str] = Field(
            None, description="", alias="adlsContainerEncryptionScope"
        )
        adls_container_version_level_immutability_support: Optional[bool] = Field(
            None, description="", alias="adlsContainerVersionLevelImmutabilitySupport"
        )
        adls_object_count: Optional[int] = Field(
            None, description="", alias="adlsObjectCount"
        )
        adls_objects: Optional[list[ADLSObject]] = Field(
            None, description="", alias="adlsObjects"
        )  # relationship
        adls_account: Optional[ADLSAccount] = Field(
            None, description="", alias="adlsAccount"
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, *, name: str, adls_account_qualified_name: str
        ) -> ADLSContainer.Attributes:
            validate_required_fields(
                ["name", "adls_account_qualified_name"],
                [name, adls_account_qualified_name],
            )

            # Split the adls_account_qualified_name to extract necessary information
            fields = adls_account_qualified_name.split("/")
            if len(fields) != 4:
                raise ValueError("Invalid adls_account_qualified_name")

            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid adls_account_qualified_name") from e

            return ADLSContainer.Attributes(
                name=name,
                adls_account_qualified_name=adls_account_qualified_name,
                connection_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}",
                qualified_name=f"{adls_account_qualified_name}/{name}",
                connector_name=connector_type.value,
                adls_account=ADLSAccount.ref_by_qualified_name(
                    adls_account_qualified_name
                ),
            )

    attributes: "ADLSContainer.Attributes" = Field(
        default_factory=lambda: ADLSContainer.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ADLSObject(ADLS):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(
        cls,
        *,
        name: str,
        adls_container_qualified_name: str,
    ) -> ADLSObject:
        validate_required_fields(
            ["name", "adls_container_qualified_name"],
            [name, adls_container_qualified_name],
        )
        attributes = ADLSObject.Attributes.create(
            name=name, adls_container_qualified_name=adls_container_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field("ADLSObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADLSObject":
            raise ValueError("must be ADLSObject")
        return v

    def __setattr__(self, name, value):
        if name in ADLSObject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ADLS_OBJECT_URL: ClassVar[KeywordTextField] = KeywordTextField(
        "adlsObjectUrl", "adlsObjectUrl.keyword", "adlsObjectUrl"
    )
    """
    URL of this object.
    """
    ADLS_OBJECT_VERSION_ID: ClassVar[KeywordField] = KeywordField(
        "adlsObjectVersionId", "adlsObjectVersionId"
    )
    """
    Identifier of the version of this object, from ADLS.
    """
    ADLS_OBJECT_TYPE: ClassVar[KeywordField] = KeywordField(
        "adlsObjectType", "adlsObjectType"
    )
    """
    Type of this object.
    """
    ADLS_OBJECT_SIZE: ClassVar[NumericField] = NumericField(
        "adlsObjectSize", "adlsObjectSize"
    )
    """
    Size of this object.
    """
    ADLS_OBJECT_ACCESS_TIER: ClassVar[KeywordField] = KeywordField(
        "adlsObjectAccessTier", "adlsObjectAccessTier"
    )
    """
    Access tier of this object.
    """
    ADLS_OBJECT_ACCESS_TIER_LAST_MODIFIED_TIME: ClassVar[NumericField] = NumericField(
        "adlsObjectAccessTierLastModifiedTime", "adlsObjectAccessTierLastModifiedTime"
    )
    """
    Time (epoch) when the acccess tier for this object was last modified, in milliseconds.
    """
    ADLS_OBJECT_ARCHIVE_STATUS: ClassVar[KeywordField] = KeywordField(
        "adlsObjectArchiveStatus", "adlsObjectArchiveStatus"
    )
    """
    Archive status of this object.
    """
    ADLS_OBJECT_SERVER_ENCRYPTED: ClassVar[BooleanField] = BooleanField(
        "adlsObjectServerEncrypted", "adlsObjectServerEncrypted"
    )
    """
    Whether this object is server encrypted (true) or not (false).
    """
    ADLS_OBJECT_VERSION_LEVEL_IMMUTABILITY_SUPPORT: ClassVar[
        BooleanField
    ] = BooleanField(
        "adlsObjectVersionLevelImmutabilitySupport",
        "adlsObjectVersionLevelImmutabilitySupport",
    )
    """
    Whether this object supports version-level immutability (true) or not (false).
    """
    ADLS_OBJECT_CACHE_CONTROL: ClassVar[TextField] = TextField(
        "adlsObjectCacheControl", "adlsObjectCacheControl"
    )
    """
    Cache control of this object.
    """
    ADLS_OBJECT_CONTENT_TYPE: ClassVar[TextField] = TextField(
        "adlsObjectContentType", "adlsObjectContentType"
    )
    """
    Content type of this object.
    """
    ADLS_OBJECT_CONTENT_MD5HASH: ClassVar[KeywordField] = KeywordField(
        "adlsObjectContentMD5Hash", "adlsObjectContentMD5Hash"
    )
    """
    MD5 hash of this object's contents.
    """
    ADLS_OBJECT_CONTENT_LANGUAGE: ClassVar[KeywordTextField] = KeywordTextField(
        "adlsObjectContentLanguage",
        "adlsObjectContentLanguage.keyword",
        "adlsObjectContentLanguage",
    )
    """
    Language of this object's contents.
    """
    ADLS_OBJECT_LEASE_STATUS: ClassVar[KeywordField] = KeywordField(
        "adlsObjectLeaseStatus", "adlsObjectLeaseStatus"
    )
    """
    Status of this object's lease.
    """
    ADLS_OBJECT_LEASE_STATE: ClassVar[KeywordField] = KeywordField(
        "adlsObjectLeaseState", "adlsObjectLeaseState"
    )
    """
    State of this object's lease.
    """
    ADLS_OBJECT_METADATA: ClassVar[KeywordField] = KeywordField(
        "adlsObjectMetadata", "adlsObjectMetadata"
    )
    """
    Metadata associated with this object, from ADLS.
    """
    ADLS_CONTAINER_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "adlsContainerQualifiedName",
        "adlsContainerQualifiedName",
        "adlsContainerQualifiedName.text",
    )
    """
    Unique name of the container this object exists within.
    """

    ADLS_CONTAINER: ClassVar[RelationField] = RelationField("adlsContainer")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "adls_object_url",
        "adls_object_version_id",
        "adls_object_type",
        "adls_object_size",
        "adls_object_access_tier",
        "adls_object_access_tier_last_modified_time",
        "adls_object_archive_status",
        "adls_object_server_encrypted",
        "adls_object_version_level_immutability_support",
        "adls_object_cache_control",
        "adls_object_content_type",
        "adls_object_content_m_d5_hash",
        "adls_object_content_language",
        "adls_object_lease_status",
        "adls_object_lease_state",
        "adls_object_metadata",
        "adls_container_qualified_name",
        "adls_container",
    ]

    @property
    def adls_object_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.adls_object_url

    @adls_object_url.setter
    def adls_object_url(self, adls_object_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_url = adls_object_url

    @property
    def adls_object_version_id(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.adls_object_version_id
        )

    @adls_object_version_id.setter
    def adls_object_version_id(self, adls_object_version_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_version_id = adls_object_version_id

    @property
    def adls_object_type(self) -> Optional[ADLSObjectType]:
        return None if self.attributes is None else self.attributes.adls_object_type

    @adls_object_type.setter
    def adls_object_type(self, adls_object_type: Optional[ADLSObjectType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_type = adls_object_type

    @property
    def adls_object_size(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.adls_object_size

    @adls_object_size.setter
    def adls_object_size(self, adls_object_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_size = adls_object_size

    @property
    def adls_object_access_tier(self) -> Optional[ADLSAccessTier]:
        return (
            None if self.attributes is None else self.attributes.adls_object_access_tier
        )

    @adls_object_access_tier.setter
    def adls_object_access_tier(
        self, adls_object_access_tier: Optional[ADLSAccessTier]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_access_tier = adls_object_access_tier

    @property
    def adls_object_access_tier_last_modified_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_access_tier_last_modified_time
        )

    @adls_object_access_tier_last_modified_time.setter
    def adls_object_access_tier_last_modified_time(
        self, adls_object_access_tier_last_modified_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_access_tier_last_modified_time = (
            adls_object_access_tier_last_modified_time
        )

    @property
    def adls_object_archive_status(self) -> Optional[ADLSObjectArchiveStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_archive_status
        )

    @adls_object_archive_status.setter
    def adls_object_archive_status(
        self, adls_object_archive_status: Optional[ADLSObjectArchiveStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_archive_status = adls_object_archive_status

    @property
    def adls_object_server_encrypted(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_server_encrypted
        )

    @adls_object_server_encrypted.setter
    def adls_object_server_encrypted(
        self, adls_object_server_encrypted: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_server_encrypted = adls_object_server_encrypted

    @property
    def adls_object_version_level_immutability_support(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_version_level_immutability_support
        )

    @adls_object_version_level_immutability_support.setter
    def adls_object_version_level_immutability_support(
        self, adls_object_version_level_immutability_support: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_version_level_immutability_support = (
            adls_object_version_level_immutability_support
        )

    @property
    def adls_object_cache_control(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_cache_control
        )

    @adls_object_cache_control.setter
    def adls_object_cache_control(self, adls_object_cache_control: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_cache_control = adls_object_cache_control

    @property
    def adls_object_content_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_content_type
        )

    @adls_object_content_type.setter
    def adls_object_content_type(self, adls_object_content_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_content_type = adls_object_content_type

    @property
    def adls_object_content_m_d5_hash(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_content_m_d5_hash
        )

    @adls_object_content_m_d5_hash.setter
    def adls_object_content_m_d5_hash(
        self, adls_object_content_m_d5_hash: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_content_m_d5_hash = adls_object_content_m_d5_hash

    @property
    def adls_object_content_language(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_content_language
        )

    @adls_object_content_language.setter
    def adls_object_content_language(self, adls_object_content_language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_content_language = adls_object_content_language

    @property
    def adls_object_lease_status(self) -> Optional[ADLSLeaseStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_lease_status
        )

    @adls_object_lease_status.setter
    def adls_object_lease_status(
        self, adls_object_lease_status: Optional[ADLSLeaseStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_lease_status = adls_object_lease_status

    @property
    def adls_object_lease_state(self) -> Optional[ADLSLeaseState]:
        return (
            None if self.attributes is None else self.attributes.adls_object_lease_state
        )

    @adls_object_lease_state.setter
    def adls_object_lease_state(
        self, adls_object_lease_state: Optional[ADLSLeaseState]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_lease_state = adls_object_lease_state

    @property
    def adls_object_metadata(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.adls_object_metadata

    @adls_object_metadata.setter
    def adls_object_metadata(self, adls_object_metadata: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_metadata = adls_object_metadata

    @property
    def adls_container_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_container_qualified_name
        )

    @adls_container_qualified_name.setter
    def adls_container_qualified_name(
        self, adls_container_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_qualified_name = adls_container_qualified_name

    @property
    def adls_container(self) -> Optional[ADLSContainer]:
        return None if self.attributes is None else self.attributes.adls_container

    @adls_container.setter
    def adls_container(self, adls_container: Optional[ADLSContainer]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container = adls_container

    class Attributes(ADLS.Attributes):
        adls_object_url: Optional[str] = Field(
            None, description="", alias="adlsObjectUrl"
        )
        adls_object_version_id: Optional[str] = Field(
            None, description="", alias="adlsObjectVersionId"
        )
        adls_object_type: Optional[ADLSObjectType] = Field(
            None, description="", alias="adlsObjectType"
        )
        adls_object_size: Optional[int] = Field(
            None, description="", alias="adlsObjectSize"
        )
        adls_object_access_tier: Optional[ADLSAccessTier] = Field(
            None, description="", alias="adlsObjectAccessTier"
        )
        adls_object_access_tier_last_modified_time: Optional[datetime] = Field(
            None, description="", alias="adlsObjectAccessTierLastModifiedTime"
        )
        adls_object_archive_status: Optional[ADLSObjectArchiveStatus] = Field(
            None, description="", alias="adlsObjectArchiveStatus"
        )
        adls_object_server_encrypted: Optional[bool] = Field(
            None, description="", alias="adlsObjectServerEncrypted"
        )
        adls_object_version_level_immutability_support: Optional[bool] = Field(
            None, description="", alias="adlsObjectVersionLevelImmutabilitySupport"
        )
        adls_object_cache_control: Optional[str] = Field(
            None, description="", alias="adlsObjectCacheControl"
        )
        adls_object_content_type: Optional[str] = Field(
            None, description="", alias="adlsObjectContentType"
        )
        adls_object_content_m_d5_hash: Optional[str] = Field(
            None, description="", alias="adlsObjectContentMD5Hash"
        )
        adls_object_content_language: Optional[str] = Field(
            None, description="", alias="adlsObjectContentLanguage"
        )
        adls_object_lease_status: Optional[ADLSLeaseStatus] = Field(
            None, description="", alias="adlsObjectLeaseStatus"
        )
        adls_object_lease_state: Optional[ADLSLeaseState] = Field(
            None, description="", alias="adlsObjectLeaseState"
        )
        adls_object_metadata: Optional[dict[str, str]] = Field(
            None, description="", alias="adlsObjectMetadata"
        )
        adls_container_qualified_name: Optional[str] = Field(
            None, description="", alias="adlsContainerQualifiedName"
        )
        adls_container: Optional[ADLSContainer] = Field(
            None, description="", alias="adlsContainer"
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, *, name: str, adls_container_qualified_name: str
        ) -> ADLSObject.Attributes:
            validate_required_fields(
                ["name", "adls_container_qualified_name"],
                [name, adls_container_qualified_name],
            )

            # Split the qualified_name to extract necessary information
            fields = adls_container_qualified_name.split("/")
            if len(fields) != 5:
                raise ValueError("Invalid qualified_name")

            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid qualified_name") from e
            adls_account_qualified_name = get_parent_qualified_name(
                adls_container_qualified_name
            )

            return ADLSObject.Attributes(
                name=name,
                adls_container_qualified_name=adls_container_qualified_name,
                qualified_name=f"{adls_container_qualified_name}/{name}",
                connection_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}",
                connector_name=connector_type.value,
                adls_container=ADLSContainer.ref_by_qualified_name(
                    adls_container_qualified_name
                ),
                adls_account_qualified_name=adls_account_qualified_name,
            )

    attributes: "ADLSObject.Attributes" = Field(
        default_factory=lambda: ADLSObject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


ADLSAccount.Attributes.update_forward_refs()


ADLSContainer.Attributes.update_forward_refs()


ADLSObject.Attributes.update_forward_refs()
