# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .dataverse import Dataverse


class DataverseAttribute(Dataverse):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        dataverse_entity_qualified_name: str,
    ) -> DataverseAttribute: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        dataverse_entity_qualified_name: str,
        connection_qualified_name: str,
    ) -> DataverseAttribute: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        dataverse_entity_qualified_name: str,
        connection_qualified_name: Optional[str] = None,
    ) -> DataverseAttribute:
        validate_required_fields(
            ["name", "dataverse_entity_qualified_name"],
            [name, dataverse_entity_qualified_name],
        )
        attributes = DataverseAttribute.Attributes.creator(
            name=name,
            dataverse_entity_qualified_name=dataverse_entity_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="DataverseAttribute", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataverseAttribute":
            raise ValueError("must be DataverseAttribute")
        return v

    def __setattr__(self, name, value):
        if name in DataverseAttribute._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATAVERSE_ENTITY_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dataverseEntityQualifiedName", "dataverseEntityQualifiedName"
    )
    """
    Entity Qualified Name of the DataverseAttribute.
    """
    DATAVERSE_ATTRIBUTE_SCHEMA_NAME: ClassVar[KeywordField] = KeywordField(
        "dataverseAttributeSchemaName", "dataverseAttributeSchemaName"
    )
    """
    Schema Name of the DataverseAttribute.
    """
    DATAVERSE_ATTRIBUTE_TYPE: ClassVar[KeywordField] = KeywordField(
        "dataverseAttributeType", "dataverseAttributeType"
    )
    """
    Type of the DataverseAttribute.
    """
    DATAVERSE_ATTRIBUTE_IS_PRIMARY_ID: ClassVar[BooleanField] = BooleanField(
        "dataverseAttributeIsPrimaryId", "dataverseAttributeIsPrimaryId"
    )
    """
    Indicator if DataverseAttribute is the primary key.
    """
    DATAVERSE_ATTRIBUTE_IS_SEARCHABLE: ClassVar[BooleanField] = BooleanField(
        "dataverseAttributeIsSearchable", "dataverseAttributeIsSearchable"
    )
    """
    Indicator if DataverseAttribute is searchable.
    """

    DATAVERSE_ENTITY: ClassVar[RelationField] = RelationField("dataverseEntity")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dataverse_entity_qualified_name",
        "dataverse_attribute_schema_name",
        "dataverse_attribute_type",
        "dataverse_attribute_is_primary_id",
        "dataverse_attribute_is_searchable",
        "dataverse_entity",
    ]

    @property
    def dataverse_entity_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dataverse_entity_qualified_name
        )

    @dataverse_entity_qualified_name.setter
    def dataverse_entity_qualified_name(
        self, dataverse_entity_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataverse_entity_qualified_name = (
            dataverse_entity_qualified_name
        )

    @property
    def dataverse_attribute_schema_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dataverse_attribute_schema_name
        )

    @dataverse_attribute_schema_name.setter
    def dataverse_attribute_schema_name(
        self, dataverse_attribute_schema_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataverse_attribute_schema_name = (
            dataverse_attribute_schema_name
        )

    @property
    def dataverse_attribute_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dataverse_attribute_type
        )

    @dataverse_attribute_type.setter
    def dataverse_attribute_type(self, dataverse_attribute_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataverse_attribute_type = dataverse_attribute_type

    @property
    def dataverse_attribute_is_primary_id(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.dataverse_attribute_is_primary_id
        )

    @dataverse_attribute_is_primary_id.setter
    def dataverse_attribute_is_primary_id(
        self, dataverse_attribute_is_primary_id: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataverse_attribute_is_primary_id = (
            dataverse_attribute_is_primary_id
        )

    @property
    def dataverse_attribute_is_searchable(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.dataverse_attribute_is_searchable
        )

    @dataverse_attribute_is_searchable.setter
    def dataverse_attribute_is_searchable(
        self, dataverse_attribute_is_searchable: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataverse_attribute_is_searchable = (
            dataverse_attribute_is_searchable
        )

    @property
    def dataverse_entity(self) -> Optional[DataverseEntity]:
        return None if self.attributes is None else self.attributes.dataverse_entity

    @dataverse_entity.setter
    def dataverse_entity(self, dataverse_entity: Optional[DataverseEntity]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataverse_entity = dataverse_entity

    class Attributes(Dataverse.Attributes):
        dataverse_entity_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        dataverse_attribute_schema_name: Optional[str] = Field(
            default=None, description=""
        )
        dataverse_attribute_type: Optional[str] = Field(default=None, description="")
        dataverse_attribute_is_primary_id: Optional[bool] = Field(
            default=None, description=""
        )
        dataverse_attribute_is_searchable: Optional[bool] = Field(
            default=None, description=""
        )
        dataverse_entity: Optional[DataverseEntity] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            dataverse_entity_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
        ) -> DataverseAttribute.Attributes:
            validate_required_fields(
                ["name", "dataverse_entity_qualified_name"],
                [name, dataverse_entity_qualified_name],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    dataverse_entity_qualified_name,
                    "dataverse_entity_qualified_name",
                    4,
                )

            return DataverseAttribute.Attributes(
                name=name,
                dataverse_entity_qualified_name=dataverse_entity_qualified_name,
                connection_qualified_name=connection_qualified_name or connection_qn,
                qualified_name=f"{dataverse_entity_qualified_name}/{name}",
                connector_name=connector_name,
                dataverse_entity=DataverseEntity.ref_by_qualified_name(
                    dataverse_entity_qualified_name
                ),
            )

    attributes: DataverseAttribute.Attributes = Field(
        default_factory=lambda: DataverseAttribute.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .dataverse_entity import DataverseEntity  # noqa: E402, F401

DataverseAttribute.Attributes.update_forward_refs()
