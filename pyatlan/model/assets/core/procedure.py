# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
    TextField,
)
from pyatlan.model.structs import SQLProcedureArgument, SQLProcedureReturn
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
    SQL_LANGUAGE: ClassVar[KeywordTextField] = KeywordTextField(
        "sqlLanguage", "sqlLanguage.keyword", "sqlLanguage"
    )
    """
    Programming language used for the procedure (e.g., SQL, JavaScript, Python, Scala).
    """
    SQL_RUNTIME_VERSION: ClassVar[KeywordTextField] = KeywordTextField(
        "sqlRuntimeVersion", "sqlRuntimeVersion.keyword", "sqlRuntimeVersion"
    )
    """
    Version of the language runtime used by the procedure.
    """
    SQL_OWNER_ROLE_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "sqlOwnerRoleType", "sqlOwnerRoleType.keyword", "sqlOwnerRoleType"
    )
    """
    Type of role that owns the procedure.
    """
    SQL_ARGUMENTS: ClassVar[KeywordField] = KeywordField("sqlArguments", "sqlArguments")
    """
    List of procedure arguments with name and type information.
    """
    SQL_PROCEDURE_RETURN: ClassVar[KeywordField] = KeywordField(
        "sqlProcedureReturn", "sqlProcedureReturn"
    )
    """
    Detailed information about the procedure's return type.
    """
    SQL_EXTERNAL_ACCESS_INTEGRATIONS: ClassVar[KeywordField] = KeywordField(
        "sqlExternalAccessIntegrations", "sqlExternalAccessIntegrations"
    )
    """
    Names of external access integrations used by the procedure.
    """
    SQL_SECRETS: ClassVar[KeywordField] = KeywordField("sqlSecrets", "sqlSecrets")
    """
    Secret variables used by the procedure.
    """
    SQL_PACKAGES: ClassVar[KeywordField] = KeywordField("sqlPackages", "sqlPackages")
    """
    Packages requested by the procedure.
    """
    SQL_INSTALLED_PACKAGES: ClassVar[KeywordField] = KeywordField(
        "sqlInstalledPackages", "sqlInstalledPackages"
    )
    """
    Packages actually installed for the procedure.
    """
    SQL_SCHEMA_ID: ClassVar[KeywordField] = KeywordField("sqlSchemaId", "sqlSchemaId")
    """
    Internal ID for the schema containing the procedure.
    """
    SQL_CATALOG_ID: ClassVar[KeywordField] = KeywordField(
        "sqlCatalogId", "sqlCatalogId"
    )
    """
    Internal ID for the database containing the procedure.
    """

    SQL_PROCESSES: ClassVar[RelationField] = RelationField("sqlProcesses")
    """
    TBC
    """
    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "definition",
        "sql_language",
        "sql_runtime_version",
        "sql_owner_role_type",
        "sql_arguments",
        "sql_procedure_return",
        "sql_external_access_integrations",
        "sql_secrets",
        "sql_packages",
        "sql_installed_packages",
        "sql_schema_id",
        "sql_catalog_id",
        "sql_processes",
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
    def sql_language(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sql_language

    @sql_language.setter
    def sql_language(self, sql_language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_language = sql_language

    @property
    def sql_runtime_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sql_runtime_version

    @sql_runtime_version.setter
    def sql_runtime_version(self, sql_runtime_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_runtime_version = sql_runtime_version

    @property
    def sql_owner_role_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sql_owner_role_type

    @sql_owner_role_type.setter
    def sql_owner_role_type(self, sql_owner_role_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_owner_role_type = sql_owner_role_type

    @property
    def sql_arguments(self) -> Optional[List[SQLProcedureArgument]]:
        return None if self.attributes is None else self.attributes.sql_arguments

    @sql_arguments.setter
    def sql_arguments(self, sql_arguments: Optional[List[SQLProcedureArgument]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_arguments = sql_arguments

    @property
    def sql_procedure_return(self) -> Optional[SQLProcedureReturn]:
        return None if self.attributes is None else self.attributes.sql_procedure_return

    @sql_procedure_return.setter
    def sql_procedure_return(self, sql_procedure_return: Optional[SQLProcedureReturn]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_procedure_return = sql_procedure_return

    @property
    def sql_external_access_integrations(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_external_access_integrations
        )

    @sql_external_access_integrations.setter
    def sql_external_access_integrations(
        self, sql_external_access_integrations: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_external_access_integrations = (
            sql_external_access_integrations
        )

    @property
    def sql_secrets(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sql_secrets

    @sql_secrets.setter
    def sql_secrets(self, sql_secrets: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_secrets = sql_secrets

    @property
    def sql_packages(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sql_packages

    @sql_packages.setter
    def sql_packages(self, sql_packages: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_packages = sql_packages

    @property
    def sql_installed_packages(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sql_installed_packages
        )

    @sql_installed_packages.setter
    def sql_installed_packages(self, sql_installed_packages: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_installed_packages = sql_installed_packages

    @property
    def sql_schema_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sql_schema_id

    @sql_schema_id.setter
    def sql_schema_id(self, sql_schema_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_schema_id = sql_schema_id

    @property
    def sql_catalog_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sql_catalog_id

    @sql_catalog_id.setter
    def sql_catalog_id(self, sql_catalog_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_catalog_id = sql_catalog_id

    @property
    def sql_processes(self) -> Optional[List[Process]]:
        return None if self.attributes is None else self.attributes.sql_processes

    @sql_processes.setter
    def sql_processes(self, sql_processes: Optional[List[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_processes = sql_processes

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
        sql_language: Optional[str] = Field(default=None, description="")
        sql_runtime_version: Optional[str] = Field(default=None, description="")
        sql_owner_role_type: Optional[str] = Field(default=None, description="")
        sql_arguments: Optional[List[SQLProcedureArgument]] = Field(
            default=None, description=""
        )
        sql_procedure_return: Optional[SQLProcedureReturn] = Field(
            default=None, description=""
        )
        sql_external_access_integrations: Optional[str] = Field(
            default=None, description=""
        )
        sql_secrets: Optional[str] = Field(default=None, description="")
        sql_packages: Optional[str] = Field(default=None, description="")
        sql_installed_packages: Optional[str] = Field(default=None, description="")
        sql_schema_id: Optional[str] = Field(default=None, description="")
        sql_catalog_id: Optional[str] = Field(default=None, description="")
        sql_processes: Optional[List[Process]] = Field(
            default=None, description=""
        )  # relationship
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


from .process import Process  # noqa: E402, F401
from .schema import Schema  # noqa: E402, F401
