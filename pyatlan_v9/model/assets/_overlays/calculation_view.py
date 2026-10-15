# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields
# IMPORT: from .sql_related import RelatedSchema

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        package_id: str,
        schema_qualified_name: str,
    ) -> "CalculationView":
        """
        Create a new CalculationView asset.

        Args:
            name: Name of the calculation view
            package_id: Repository package that contains the calculation view (for example ``sales.reporting``)
            schema_qualified_name: Unique name of the schema in which this calculation view exists

        Returns:
            CalculationView instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            ["name", "package_id", "schema_qualified_name"],
            [name, package_id, schema_qualified_name],
        )
        if "/" in package_id:
            raise ValueError(
                f"Invalid package_id: {package_id}. "
                "Package segments are separated by '.'"
            )
        fields = schema_qualified_name.split("/")
        if len(fields) != 5:
            raise ValueError(
                f"Invalid schema_qualified_name: {schema_qualified_name}. "
                "Expected format: default/connector/connection_id/database/schema"
            )
        connection_qualified_name = "/".join(fields[:3])
        return cls(
            name=name,
            qualified_name=f"{schema_qualified_name}/{package_id}/{name}",
            calculation_view_package_id=package_id,
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
            database_name=fields[3],
            database_qualified_name=f"{connection_qualified_name}/{fields[3]}",
            schema_name=fields[4],
            schema_qualified_name=schema_qualified_name,
            atlan_schema=RelatedSchema(qualified_name=schema_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "CalculationView":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "CalculationView":
        return cls.updater(**kwargs)
