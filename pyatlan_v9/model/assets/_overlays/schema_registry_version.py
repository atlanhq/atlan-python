# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        schema_registry_version_number: Union[int, str],
        schema_registry_subject_qualified_name: str,
        name: Union[str, None] = None,
        connection_qualified_name: Union[str, None] = None,
    ) -> "SchemaRegistryVersion":
        """Create a new SchemaRegistryVersion asset.

        ``name`` defaults to ``{subject}.v{version}``, as the Kafka app names it.
        """
        validate_required_fields(
            [
                "schema_registry_version_number",
                "schema_registry_subject_qualified_name",
            ],
            [schema_registry_version_number, schema_registry_subject_qualified_name],
        )
        version = str(schema_registry_version_number)
        # A subject qualifiedName is {connection_qn}/subject/{subject}.
        parts = schema_registry_subject_qualified_name.split("/")
        if len(parts) < 5 or parts[3] != "subject":
            raise ValueError("schema_registry_subject_qualified_name is invalid")
        if not name:
            name = f"{'/'.join(parts[4:])}.v{version}"
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:3])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{schema_registry_subject_qualified_name}/version/{version}",
            schema_registry_version_number=version,
            schema_registry_subject_qualified_name=schema_registry_subject_qualified_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            schema_registry_subject=RelatedSchemaRegistrySubject(
                unique_attributes={
                    "qualifiedName": schema_registry_subject_qualified_name
                }
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SchemaRegistryVersion":
        """Create a SchemaRegistryVersion instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SchemaRegistryVersion":
        """Return only fields required for update operations."""
        return SchemaRegistryVersion.updater(
            qualified_name=self.qualified_name, name=self.name
        )
