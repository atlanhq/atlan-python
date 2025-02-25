# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import RelationField, TextField
from pyatlan.utils import init_guid, validate_required_fields

from .s_q_l import SQL


class Procedure(SQL):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        schema_qualified_name: str,
        definition: str,
    ) -> Procedure: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        schema_qualified_name: str,
        schema_name: str,
        database_name: str,
        database_qualified_name: str,
        connection_qualified_name: str,
        definition: str,
    ) -> Procedure: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        definition: str,
        schema_qualified_name: str,
        schema_name: Optional[str] = None,
        database_name: Optional[str] = None,
        database_qualified_name: Optional[str] = None,
        connection_qualified_name: Optional[str] = None,
    ) -> Procedure:
        attributes = Procedure.Attributes.create(
            name=name,
            definition=definition,
            schema_qualified_name=schema_qualified_name,
            schema_name=schema_name,
            database_name=database_name,
            database_qualified_name=database_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def updater(cls, *, name: str, qualified_name: str, definition: str) -> Procedure:
        validate_required_fields(
            ["name", "qualified_name", "definition"],
            [name, qualified_name, definition],
        )
        procedure = Procedure(
            attributes=Procedure.Attributes(qualified_name=qualified_name, name=name)
        )
        procedure.definition = definition
        return procedure

    def trim_to_required(self: Procedure) -> Procedure:
        return self.updater(
            qualified_name=self.qualified_name or "",
            name=self.name or "",
            definition=self.definition or "",
        )

    type_name: str = Field(default="Procedure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Procedure":
            raise ValueError("must be Procedure")
        return v

    def __setattr__(self, name, value):
        if name in Procedure._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DEFINITION: ClassVar[TextField] = TextField("definition", "definition")
    """
    SQL definition of the procedure.
    """

    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "definition",
        "atlan_schema",
    ]

    @property
    def definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.definition

    @definition.setter
    def definition(self, definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.definition = definition

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    class Attributes(SQL.Attributes):
        definition: Optional[str] = Field(default=None, description="")
        atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            definition: str,
            schema_qualified_name: Optional[str] = None,
            schema_name: Optional[str] = None,
            database_name: Optional[str] = None,
            database_qualified_name: Optional[str] = None,
            connection_qualified_name: Optional[str] = None,
        ) -> Procedure.Attributes:
            validate_required_fields(
                ["name", "definition", "schema_qualified_name"],
                [name, definition, schema_qualified_name],
            )
            assert schema_qualified_name  # noqa: S101
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    schema_qualified_name, "schema_qualified_name", 5
                )

            fields = schema_qualified_name.split("/")
            qualified_name = f"{schema_qualified_name}/_procedures_/{name}"
            connection_qualified_name = connection_qualified_name or connection_qn
            database_name = database_name or fields[3]
            schema_name = schema_name or fields[4]
            database_qualified_name = (
                database_qualified_name
                or f"{connection_qualified_name}/{database_name}"
            )

            return Procedure.Attributes(
                name=name,
                definition=definition,
                qualified_name=qualified_name,
                database_name=database_name,
                database_qualified_name=database_qualified_name,
                schema_name=schema_name,
                schema_qualified_name=schema_qualified_name,
                atlan_schema=Schema.ref_by_qualified_name(schema_qualified_name),
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name,
            )

    attributes: Procedure.Attributes = Field(
        default_factory=lambda: Procedure.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .schema import Schema  # noqa: E402, F401
