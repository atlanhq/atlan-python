# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)

from .cosmos_mongo_d_b import CosmosMongoDB


class CosmosMongoDBAccount(CosmosMongoDB):
    """Description"""

    type_name: str = Field(default="CosmosMongoDBAccount", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CosmosMongoDBAccount":
            raise ValueError("must be CosmosMongoDBAccount")
        return v

    def __setattr__(self, name, value):
        if name in CosmosMongoDBAccount._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COSMOS_MONGO_DB_ACCOUNT_INSTANCE_ID: ClassVar[KeywordField] = KeywordField(
        "cosmosMongoDBAccountInstanceId", "cosmosMongoDBAccountInstanceId"
    )
    """
    The unique identifier for the Cosmos MongoDB account.
    """
    COSMOS_MONGO_DB_DATABASE_COUNT: ClassVar[NumericField] = NumericField(
        "cosmosMongoDBDatabaseCount", "cosmosMongoDBDatabaseCount"
    )
    """
    Number of databases in this Cosmos MongoDB account.
    """
    COSMOS_MONGO_DB_ACCOUNT_TYPE: ClassVar[KeywordField] = KeywordField(
        "cosmosMongoDBAccountType", "cosmosMongoDBAccountType"
    )
    """
    The type of the Cosmos MongoDB account, such as RU or VCORE.
    """
    COSMOS_MONGO_DB_ACCOUNT_SUBSCRIPTION_ID: ClassVar[KeywordField] = KeywordField(
        "cosmosMongoDBAccountSubscriptionId", "cosmosMongoDBAccountSubscriptionId"
    )
    """
    The ID of the subscription to which the Cosmos MongoDB account belongs.
    """
    COSMOS_MONGO_DB_ACCOUNT_RESOURCE_GROUP: ClassVar[KeywordField] = KeywordField(
        "cosmosMongoDBAccountResourceGroup", "cosmosMongoDBAccountResourceGroup"
    )
    """
    The resource group that contains the Cosmos MongoDB account.
    """
    COSMOS_MONGO_DB_ACCOUNT_DOCUMENT_ENDPOINT: ClassVar[TextField] = TextField(
        "cosmosMongoDBAccountDocumentEndpoint", "cosmosMongoDBAccountDocumentEndpoint"
    )
    """
    The Document Endpoint URL for the Cosmos MongoDB account.
    """
    COSMOS_MONGO_DB_ACCOUNT_MONGO_ENDPOINT: ClassVar[TextField] = TextField(
        "cosmosMongoDBAccountMongoEndpoint", "cosmosMongoDBAccountMongoEndpoint"
    )
    """
    The MongoDB connection endpoint for the Cosmos MongoDB account.
    """
    COSMOS_MONGO_DB_ACCOUNT_PUBLIC_NETWORK_ACCESS: ClassVar[TextField] = TextField(
        "cosmosMongoDBAccountPublicNetworkAccess",
        "cosmosMongoDBAccountPublicNetworkAccess",
    )
    """
    The status of public network access for the Cosmos MongoDB account.
    """
    COSMOS_MONGO_DB_ACCOUNT_ENABLE_AUTOMATIC_FAILOVER: ClassVar[BooleanField] = (
        BooleanField(
            "cosmosMongoDBAccountEnableAutomaticFailover",
            "cosmosMongoDBAccountEnableAutomaticFailover",
        )
    )
    """
    Indicates whether automatic failover is enabled for the Cosmos MongoDB account.
    """
    COSMOS_MONGO_DB_ACCOUNT_ENABLE_MULTIPLE_WRITE_LOCATIONS: ClassVar[BooleanField] = (
        BooleanField(
            "cosmosMongoDBAccountEnableMultipleWriteLocations",
            "cosmosMongoDBAccountEnableMultipleWriteLocations",
        )
    )
    """
    Indicates whether multiple write locations are enabled for the Cosmos MongoDB account.
    """
    COSMOS_MONGO_DB_ACCOUNT_ENABLE_PARTITION_KEY_MONITOR: ClassVar[BooleanField] = (
        BooleanField(
            "cosmosMongoDBAccountEnablePartitionKeyMonitor",
            "cosmosMongoDBAccountEnablePartitionKeyMonitor",
        )
    )
    """
    Indicates whether partition key monitoring is enabled for the Cosmos MongoDB account.
    """
    COSMOS_MONGO_DB_ACCOUNT_IS_VIRTUAL_NETWORK_FILTER_ENABLED: ClassVar[
        BooleanField
    ] = BooleanField(
        "cosmosMongoDBAccountIsVirtualNetworkFilterEnabled",
        "cosmosMongoDBAccountIsVirtualNetworkFilterEnabled",
    )
    """
    Indicates whether the virtual network filter is enabled for the Cosmos MongoDB account.
    """
    COSMOS_MONGO_DB_ACCOUNT_CONSISTENCY_POLICY: ClassVar[TextField] = TextField(
        "cosmosMongoDBAccountConsistencyPolicy", "cosmosMongoDBAccountConsistencyPolicy"
    )
    """
    The consistency policy configured for the Cosmos MongoDB account.
    """
    COSMOS_MONGO_DB_ACCOUNT_LOCATIONS: ClassVar[TextField] = TextField(
        "cosmosMongoDBAccountLocations", "cosmosMongoDBAccountLocations"
    )
    """
    The locations where the Cosmos MongoDB account is available.
    """
    COSMOS_MONGO_DB_ACCOUNT_READ_LOCATIONS: ClassVar[TextField] = TextField(
        "cosmosMongoDBAccountReadLocations", "cosmosMongoDBAccountReadLocations"
    )
    """
    The read locations configured for the Cosmos MongoDB account.
    """
    COSMOS_MONGO_DB_ACCOUNT_WRITE_LOCATIONS: ClassVar[TextField] = TextField(
        "cosmosMongoDBAccountWriteLocations", "cosmosMongoDBAccountWriteLocations"
    )
    """
    The write locations configured for the Cosmos MongoDB account.
    """

    COSMOS_MONGO_DB_DATABASES: ClassVar[RelationField] = RelationField(
        "cosmosMongoDBDatabases"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cosmos_mongo_d_b_account_instance_id",
        "cosmos_mongo_d_b_database_count",
        "cosmos_mongo_d_b_account_type",
        "cosmos_mongo_d_b_account_subscription_id",
        "cosmos_mongo_d_b_account_resource_group",
        "cosmos_mongo_d_b_account_document_endpoint",
        "cosmos_mongo_d_b_account_mongo_endpoint",
        "cosmos_mongo_d_b_account_public_network_access",
        "cosmos_mongo_d_b_account_enable_automatic_failover",
        "cosmos_mongo_d_b_account_enable_multiple_write_locations",
        "cosmos_mongo_d_b_account_enable_partition_key_monitor",
        "cosmos_mongo_d_b_account_is_virtual_network_filter_enabled",
        "cosmos_mongo_d_b_account_consistency_policy",
        "cosmos_mongo_d_b_account_locations",
        "cosmos_mongo_d_b_account_read_locations",
        "cosmos_mongo_d_b_account_write_locations",
        "cosmos_mongo_d_b_databases",
    ]

    @property
    def cosmos_mongo_d_b_account_instance_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_instance_id
        )

    @cosmos_mongo_d_b_account_instance_id.setter
    def cosmos_mongo_d_b_account_instance_id(
        self, cosmos_mongo_d_b_account_instance_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_instance_id = (
            cosmos_mongo_d_b_account_instance_id
        )

    @property
    def cosmos_mongo_d_b_database_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_database_count
        )

    @cosmos_mongo_d_b_database_count.setter
    def cosmos_mongo_d_b_database_count(
        self, cosmos_mongo_d_b_database_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_database_count = (
            cosmos_mongo_d_b_database_count
        )

    @property
    def cosmos_mongo_d_b_account_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_type
        )

    @cosmos_mongo_d_b_account_type.setter
    def cosmos_mongo_d_b_account_type(
        self, cosmos_mongo_d_b_account_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_type = cosmos_mongo_d_b_account_type

    @property
    def cosmos_mongo_d_b_account_subscription_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_subscription_id
        )

    @cosmos_mongo_d_b_account_subscription_id.setter
    def cosmos_mongo_d_b_account_subscription_id(
        self, cosmos_mongo_d_b_account_subscription_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_subscription_id = (
            cosmos_mongo_d_b_account_subscription_id
        )

    @property
    def cosmos_mongo_d_b_account_resource_group(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_resource_group
        )

    @cosmos_mongo_d_b_account_resource_group.setter
    def cosmos_mongo_d_b_account_resource_group(
        self, cosmos_mongo_d_b_account_resource_group: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_resource_group = (
            cosmos_mongo_d_b_account_resource_group
        )

    @property
    def cosmos_mongo_d_b_account_document_endpoint(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_document_endpoint
        )

    @cosmos_mongo_d_b_account_document_endpoint.setter
    def cosmos_mongo_d_b_account_document_endpoint(
        self, cosmos_mongo_d_b_account_document_endpoint: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_document_endpoint = (
            cosmos_mongo_d_b_account_document_endpoint
        )

    @property
    def cosmos_mongo_d_b_account_mongo_endpoint(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_mongo_endpoint
        )

    @cosmos_mongo_d_b_account_mongo_endpoint.setter
    def cosmos_mongo_d_b_account_mongo_endpoint(
        self, cosmos_mongo_d_b_account_mongo_endpoint: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_mongo_endpoint = (
            cosmos_mongo_d_b_account_mongo_endpoint
        )

    @property
    def cosmos_mongo_d_b_account_public_network_access(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_public_network_access
        )

    @cosmos_mongo_d_b_account_public_network_access.setter
    def cosmos_mongo_d_b_account_public_network_access(
        self, cosmos_mongo_d_b_account_public_network_access: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_public_network_access = (
            cosmos_mongo_d_b_account_public_network_access
        )

    @property
    def cosmos_mongo_d_b_account_enable_automatic_failover(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_enable_automatic_failover
        )

    @cosmos_mongo_d_b_account_enable_automatic_failover.setter
    def cosmos_mongo_d_b_account_enable_automatic_failover(
        self, cosmos_mongo_d_b_account_enable_automatic_failover: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_enable_automatic_failover = (
            cosmos_mongo_d_b_account_enable_automatic_failover
        )

    @property
    def cosmos_mongo_d_b_account_enable_multiple_write_locations(
        self,
    ) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_enable_multiple_write_locations
        )

    @cosmos_mongo_d_b_account_enable_multiple_write_locations.setter
    def cosmos_mongo_d_b_account_enable_multiple_write_locations(
        self, cosmos_mongo_d_b_account_enable_multiple_write_locations: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_enable_multiple_write_locations = (
            cosmos_mongo_d_b_account_enable_multiple_write_locations
        )

    @property
    def cosmos_mongo_d_b_account_enable_partition_key_monitor(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_enable_partition_key_monitor
        )

    @cosmos_mongo_d_b_account_enable_partition_key_monitor.setter
    def cosmos_mongo_d_b_account_enable_partition_key_monitor(
        self, cosmos_mongo_d_b_account_enable_partition_key_monitor: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_enable_partition_key_monitor = (
            cosmos_mongo_d_b_account_enable_partition_key_monitor
        )

    @property
    def cosmos_mongo_d_b_account_is_virtual_network_filter_enabled(
        self,
    ) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_is_virtual_network_filter_enabled
        )

    @cosmos_mongo_d_b_account_is_virtual_network_filter_enabled.setter
    def cosmos_mongo_d_b_account_is_virtual_network_filter_enabled(
        self, cosmos_mongo_d_b_account_is_virtual_network_filter_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_is_virtual_network_filter_enabled = (
            cosmos_mongo_d_b_account_is_virtual_network_filter_enabled
        )

    @property
    def cosmos_mongo_d_b_account_consistency_policy(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_consistency_policy
        )

    @cosmos_mongo_d_b_account_consistency_policy.setter
    def cosmos_mongo_d_b_account_consistency_policy(
        self, cosmos_mongo_d_b_account_consistency_policy: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_consistency_policy = (
            cosmos_mongo_d_b_account_consistency_policy
        )

    @property
    def cosmos_mongo_d_b_account_locations(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_locations
        )

    @cosmos_mongo_d_b_account_locations.setter
    def cosmos_mongo_d_b_account_locations(
        self, cosmos_mongo_d_b_account_locations: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_locations = (
            cosmos_mongo_d_b_account_locations
        )

    @property
    def cosmos_mongo_d_b_account_read_locations(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_read_locations
        )

    @cosmos_mongo_d_b_account_read_locations.setter
    def cosmos_mongo_d_b_account_read_locations(
        self, cosmos_mongo_d_b_account_read_locations: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_read_locations = (
            cosmos_mongo_d_b_account_read_locations
        )

    @property
    def cosmos_mongo_d_b_account_write_locations(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_account_write_locations
        )

    @cosmos_mongo_d_b_account_write_locations.setter
    def cosmos_mongo_d_b_account_write_locations(
        self, cosmos_mongo_d_b_account_write_locations: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_account_write_locations = (
            cosmos_mongo_d_b_account_write_locations
        )

    @property
    def cosmos_mongo_d_b_databases(self) -> Optional[List[CosmosMongoDBDatabase]]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_databases
        )

    @cosmos_mongo_d_b_databases.setter
    def cosmos_mongo_d_b_databases(
        self, cosmos_mongo_d_b_databases: Optional[List[CosmosMongoDBDatabase]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_databases = cosmos_mongo_d_b_databases

    class Attributes(CosmosMongoDB.Attributes):
        cosmos_mongo_d_b_account_instance_id: Optional[str] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_database_count: Optional[int] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_account_type: Optional[str] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_account_subscription_id: Optional[str] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_account_resource_group: Optional[str] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_account_document_endpoint: Optional[str] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_account_mongo_endpoint: Optional[str] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_account_public_network_access: Optional[str] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_account_enable_automatic_failover: Optional[bool] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_account_enable_multiple_write_locations: Optional[bool] = (
            Field(default=None, description="")
        )
        cosmos_mongo_d_b_account_enable_partition_key_monitor: Optional[bool] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_account_is_virtual_network_filter_enabled: Optional[bool] = (
            Field(default=None, description="")
        )
        cosmos_mongo_d_b_account_consistency_policy: Optional[str] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_account_locations: Optional[Set[str]] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_account_read_locations: Optional[Set[str]] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_account_write_locations: Optional[Set[str]] = Field(
            default=None, description=""
        )
        cosmos_mongo_d_b_databases: Optional[List[CosmosMongoDBDatabase]] = Field(
            default=None, description=""
        )  # relationship

    attributes: CosmosMongoDBAccount.Attributes = Field(
        default_factory=lambda: CosmosMongoDBAccount.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cosmos_mongo_d_b_database import CosmosMongoDBDatabase  # noqa

CosmosMongoDBAccount.Attributes.update_forward_refs()
