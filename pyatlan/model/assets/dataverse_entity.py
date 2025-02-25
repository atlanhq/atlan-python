# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .dataverse import Dataverse


class DataverseEntity(Dataverse):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> DataverseEntity:
        validate_required_fields(
            ["name", "connection_qualified_name"],
            [name, connection_qualified_name],
        )
        attributes = DataverseEntity.Attributes.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="DataverseEntity", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataverseEntity":
            raise ValueError("must be DataverseEntity")
        return v

    def __setattr__(self, name, value):
        if name in DataverseEntity._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATAVERSE_ENTITY_SCHEMA_NAME: ClassVar[KeywordField] = KeywordField(
        "dataverseEntitySchemaName", "dataverseEntitySchemaName"
    )
    """
    Schema Name of the DataverseEntity.
    """
    DATAVERSE_ENTITY_TABLE_TYPE: ClassVar[KeywordField] = KeywordField(
        "dataverseEntityTableType", "dataverseEntityTableType"
    )
    """
    Table Type of the DataverseEntity.
    """

    DATAVERSE_ATTRIBUTES: ClassVar[RelationField] = RelationField("dataverseAttributes")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dataverse_entity_schema_name",
        "dataverse_entity_table_type",
        "dataverse_attributes",
    ]

    @property
    def dataverse_entity_schema_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dataverse_entity_schema_name
        )

    @dataverse_entity_schema_name.setter
    def dataverse_entity_schema_name(self, dataverse_entity_schema_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataverse_entity_schema_name = dataverse_entity_schema_name

    @property
    def dataverse_entity_table_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dataverse_entity_table_type
        )

    @dataverse_entity_table_type.setter
    def dataverse_entity_table_type(self, dataverse_entity_table_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataverse_entity_table_type = dataverse_entity_table_type

    @property
    def dataverse_attributes(self) -> Optional[List[DataverseAttribute]]:
        return None if self.attributes is None else self.attributes.dataverse_attributes

    @dataverse_attributes.setter
    def dataverse_attributes(
        self, dataverse_attributes: Optional[List[DataverseAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataverse_attributes = dataverse_attributes

    class Attributes(Dataverse.Attributes):
        dataverse_entity_schema_name: Optional[str] = Field(
            default=None, description=""
        )
        dataverse_entity_table_type: Optional[str] = Field(default=None, description="")
        dataverse_attributes: Optional[List[DataverseAttribute]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls, *, name: str, connection_qualified_name: str
        ) -> DataverseEntity.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"],
                [name, connection_qualified_name],
            )
            return DataverseEntity.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: DataverseEntity.Attributes = Field(
        default_factory=lambda: DataverseEntity.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .dataverse_attribute import DataverseAttribute  # noqa: E402, F401

DataverseEntity.Attributes.update_forward_refs()
