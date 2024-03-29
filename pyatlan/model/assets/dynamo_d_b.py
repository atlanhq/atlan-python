# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import DynamoDBStatus
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField

from .no_s_q_l import NoSQL


class DynamoDB(NoSQL):
    """Description"""

    type_name: str = Field(default="DynamoDB", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DynamoDB":
            raise ValueError("must be DynamoDB")
        return v

    def __setattr__(self, name, value):
        if name in DynamoDB._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DYNAMO_DB_STATUS: ClassVar[KeywordField] = KeywordField(
        "dynamoDBStatus", "dynamoDBStatus"
    )
    """
    Status of the DynamoDB Asset
    """
    DYNAMO_DB_PARTITION_KEY: ClassVar[KeywordField] = KeywordField(
        "dynamoDBPartitionKey", "dynamoDBPartitionKey"
    )
    """
    Specifies the partition key of the DynamoDB Table/Index
    """
    DYNAMO_DB_SORT_KEY: ClassVar[KeywordField] = KeywordField(
        "dynamoDBSortKey", "dynamoDBSortKey"
    )
    """
    Specifies the sort key of the DynamoDB Table/Index
    """
    DYNAMO_DB_READ_CAPACITY_UNITS: ClassVar[NumericField] = NumericField(
        "dynamoDBReadCapacityUnits", "dynamoDBReadCapacityUnits"
    )
    """
    The maximum number of strongly consistent reads consumed per second before DynamoDB returns a ThrottlingException
    """
    DYNAMO_DB_WRITE_CAPACITY_UNITS: ClassVar[NumericField] = NumericField(
        "dynamoDBWriteCapacityUnits", "dynamoDBWriteCapacityUnits"
    )
    """
    The maximum number of writes consumed per second before DynamoDB returns a ThrottlingException
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dynamo_d_b_status",
        "dynamo_d_b_partition_key",
        "dynamo_d_b_sort_key",
        "dynamo_d_b_read_capacity_units",
        "dynamo_d_b_write_capacity_units",
    ]

    @property
    def dynamo_d_b_status(self) -> Optional[DynamoDBStatus]:
        return None if self.attributes is None else self.attributes.dynamo_d_b_status

    @dynamo_d_b_status.setter
    def dynamo_d_b_status(self, dynamo_d_b_status: Optional[DynamoDBStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_d_b_status = dynamo_d_b_status

    @property
    def dynamo_d_b_partition_key(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dynamo_d_b_partition_key
        )

    @dynamo_d_b_partition_key.setter
    def dynamo_d_b_partition_key(self, dynamo_d_b_partition_key: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_d_b_partition_key = dynamo_d_b_partition_key

    @property
    def dynamo_d_b_sort_key(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dynamo_d_b_sort_key

    @dynamo_d_b_sort_key.setter
    def dynamo_d_b_sort_key(self, dynamo_d_b_sort_key: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_d_b_sort_key = dynamo_d_b_sort_key

    @property
    def dynamo_d_b_read_capacity_units(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.dynamo_d_b_read_capacity_units
        )

    @dynamo_d_b_read_capacity_units.setter
    def dynamo_d_b_read_capacity_units(
        self, dynamo_d_b_read_capacity_units: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_d_b_read_capacity_units = dynamo_d_b_read_capacity_units

    @property
    def dynamo_d_b_write_capacity_units(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.dynamo_d_b_write_capacity_units
        )

    @dynamo_d_b_write_capacity_units.setter
    def dynamo_d_b_write_capacity_units(
        self, dynamo_d_b_write_capacity_units: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_d_b_write_capacity_units = (
            dynamo_d_b_write_capacity_units
        )

    class Attributes(NoSQL.Attributes):
        dynamo_d_b_status: Optional[DynamoDBStatus] = Field(
            default=None, description=""
        )
        dynamo_d_b_partition_key: Optional[str] = Field(default=None, description="")
        dynamo_d_b_sort_key: Optional[str] = Field(default=None, description="")
        dynamo_d_b_read_capacity_units: Optional[int] = Field(
            default=None, description=""
        )
        dynamo_d_b_write_capacity_units: Optional[int] = Field(
            default=None, description=""
        )

    attributes: DynamoDB.Attributes = Field(
        default_factory=lambda: DynamoDB.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
