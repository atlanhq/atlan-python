# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType, DynamoDBStatus
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .core.column import Column


class DynamoDBAttribute(Column):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        parent_qualified_name: str,
        order: int,
        parent_name: Optional[str] = None,
        connection_qualified_name: Optional[str] = None,
    ) -> DynamoDBAttribute:
        """
        Builds the minimal object necessary to create a DynamoDBAttribute.

        :param name: name of the DynamoDBAttribute
        :param parent_qualified_name: unique name of the DynamoDBTable
        in which this attribute exists
        :param order: the order the attribute appears within its parent
        :param parent_name: simple name of the DynamoDBTable
        in which the attribute is contained
        :param connection_qualified_name: unique name of the connection
        in which the attribute should be created
        :returns: the minimal request necessary to create the DynamoDBAttribute
        """
        return DynamoDBAttribute(
            attributes=DynamoDBAttribute.Attributes.create(
                name=name,
                parent_qualified_name=parent_qualified_name,
                order=order,
                parent_name=parent_name,
                connection_qualified_name=connection_qualified_name,
            )
        )

    type_name: str = Field(default="DynamoDBAttribute", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DynamoDBAttribute":
            raise ValueError("must be DynamoDBAttribute")
        return v

    def __setattr__(self, name, value):
        if name in DynamoDBAttribute._convenience_properties:
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
    NO_SQL_SCHEMA_DEFINITION: ClassVar[TextField] = TextField(
        "noSQLSchemaDefinition", "noSQLSchemaDefinition"
    )
    """
    Represents attributes for describing the key schema for the table and indexes.
    """

    DYNAMO_DB_TABLE: ClassVar[RelationField] = RelationField("dynamoDBTable")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dynamo_d_b_status",
        "dynamo_d_b_partition_key",
        "dynamo_d_b_sort_key",
        "dynamo_d_b_read_capacity_units",
        "dynamo_d_b_write_capacity_units",
        "no_s_q_l_schema_definition",
        "dynamo_dbtable",
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

    @property
    def no_s_q_l_schema_definition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.no_s_q_l_schema_definition
        )

    @no_s_q_l_schema_definition.setter
    def no_s_q_l_schema_definition(self, no_s_q_l_schema_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.no_s_q_l_schema_definition = no_s_q_l_schema_definition

    @property
    def dynamo_dbtable(self) -> Optional[DynamoDBTable]:
        return None if self.attributes is None else self.attributes.dynamo_dbtable

    @dynamo_dbtable.setter
    def dynamo_dbtable(self, dynamo_dbtable: Optional[DynamoDBTable]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_dbtable = dynamo_dbtable

    class Attributes(Column.Attributes):
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
        no_s_q_l_schema_definition: Optional[str] = Field(default=None, description="")
        dynamo_dbtable: Optional[DynamoDBTable] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            parent_qualified_name: str,
            order: int,
            parent_name: Optional[str] = None,
            connection_qualified_name: Optional[str] = None,
        ) -> DynamoDBAttribute.Attributes:
            """
            Builds the minimal object necessary to create a DynamoDBAttribute.

            :param name: name of the DynamoDBAttribute
            :param parent_qualified_name: unique name of the DynamoDBTable
            in which this attribute exists
            :param order: the order the attribute appears within its parent
            :param parent_name: simple name of the DynamoDBTable
            in which the attribute is contained
            :param connection_qualified_name: unique name of the connection
            in which the attribute should be created
            :returns: the minimal request necessary to create the DynamoDBAttribute
            """
            validate_required_fields(
                ["name", "parent_qualified_name", "order"],
                [name, parent_qualified_name, order],
            )
            fields = parent_qualified_name.split("/")
            if len(fields) != 4:
                raise ValueError("Invalid parent_qualified_name")
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    parent_qualified_name, "parent_qualified_name", 4
                )
            if order < 0:
                raise ValueError("Order must be be a positive integer")

            qualified_name = f"{parent_qualified_name}/{name}"
            connection_qualified_name = connection_qualified_name or connection_qn
            parent_name = parent_name or fields[3]

            return DynamoDBAttribute.Attributes(
                name=name,
                order=order,
                qualified_name=qualified_name,
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name,
                table_name=parent_name,
                table_qualified_name=parent_qualified_name,
                dynamo_dbtable=DynamoDBTable.ref_by_qualified_name(
                    parent_qualified_name
                ),
            )

    attributes: DynamoDBAttribute.Attributes = Field(
        default_factory=lambda: DynamoDBAttribute.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .dynamo_dbtable import DynamoDBTable  # noqa: E402, F401

DynamoDBAttribute.Attributes.update_forward_refs()
