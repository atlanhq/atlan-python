# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .s_q_l import SQL


class Database(SQL):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> Database:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = Database.Attributes(
            name=name,
            connection_qualified_name=connection_qualified_name,
            qualified_name=f"{connection_qualified_name}/{name}",
            connector_name=AtlanConnectorType.get_connector_name(
                connection_qualified_name
            ),
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, connection_qualified_name: str) -> Database:
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

    type_name: str = Field(default="Database", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Database":
            raise ValueError("must be Database")
        return v

    def __setattr__(self, name, value):
        if name in Database._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SCHEMA_COUNT: ClassVar[NumericField] = NumericField("schemaCount", "schemaCount")
    """
    Number of schemas in this database.
    """
    SQL_IS_IMPORTED_VIA_DATA_SHARE: ClassVar[BooleanField] = BooleanField(
        "sqlIsImportedViaDataShare", "sqlIsImportedViaDataShare"
    )
    """
    Whether this database was imported via a data share (true) or not (false).
    """
    SQL_ORIGIN_ACCOUNT_GUID: ClassVar[KeywordField] = KeywordField(
        "sqlOriginAccountGuid", "sqlOriginAccountGuid"
    )
    """
    Source-system identifier of the account that produced this imported database.
    """

    FABRIC_WORKSPACE: ClassVar[RelationField] = RelationField("fabricWorkspace")
    """
    TBC
    """
    SQL_SCHEMAS: ClassVar[RelationField] = RelationField("sqlSchemas")
    """
    TBC
    """
    SCHEMAS: ClassVar[RelationField] = RelationField("schemas")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "schema_count",
        "sql_is_imported_via_data_share",
        "sql_origin_account_guid",
        "fabric_workspace",
        "sql_schemas",
        "schemas",
    ]

    @property
    def schema_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.schema_count

    @schema_count.setter
    def schema_count(self, schema_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_count = schema_count

    @property
    def sql_is_imported_via_data_share(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_is_imported_via_data_share
        )

    @sql_is_imported_via_data_share.setter
    def sql_is_imported_via_data_share(
        self, sql_is_imported_via_data_share: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_is_imported_via_data_share = sql_is_imported_via_data_share

    @property
    def sql_origin_account_guid(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sql_origin_account_guid
        )

    @sql_origin_account_guid.setter
    def sql_origin_account_guid(self, sql_origin_account_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_origin_account_guid = sql_origin_account_guid

    @property
    def fabric_workspace(self) -> Optional[FabricWorkspace]:
        return None if self.attributes is None else self.attributes.fabric_workspace

    @fabric_workspace.setter
    def fabric_workspace(self, fabric_workspace: Optional[FabricWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_workspace = fabric_workspace

    @property
    def sql_schemas(self) -> Optional[List[Schema]]:
        return None if self.attributes is None else self.attributes.sql_schemas

    @sql_schemas.setter
    def sql_schemas(self, sql_schemas: Optional[List[Schema]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_schemas = sql_schemas

    @property
    def schemas(self) -> Optional[List[Schema]]:
        return None if self.attributes is None else self.attributes.schemas

    @schemas.setter
    def schemas(self, schemas: Optional[List[Schema]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schemas = schemas

    class Attributes(SQL.Attributes):
        schema_count: Optional[int] = Field(default=None, description="")
        sql_is_imported_via_data_share: Optional[bool] = Field(
            default=None, description=""
        )
        sql_origin_account_guid: Optional[str] = Field(default=None, description="")
        fabric_workspace: Optional[FabricWorkspace] = Field(
            default=None, description=""
        )  # relationship
        sql_schemas: Optional[List[Schema]] = Field(
            default=None, description=""
        )  # relationship
        schemas: Optional[List[Schema]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls, name: str, connection_qualified_name: str
        ) -> Database.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return Database.Attributes(
                name=name,
                connection_qualified_name=connection_qualified_name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: Database.Attributes = Field(
        default_factory=lambda: Database.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .fabric_workspace import FabricWorkspace  # noqa: E402, F401
from .schema import Schema  # noqa: E402, F401
