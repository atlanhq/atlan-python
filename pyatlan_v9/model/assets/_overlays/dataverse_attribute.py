# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        dataverse_entity_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "DataverseAttribute":
        """Create a new DataverseAttribute asset."""
        validate_required_fields(
            ["name", "dataverse_entity_qualified_name"],
            [name, dataverse_entity_qualified_name],
        )
        if connection_qualified_name:
            connector_name = (
                connection_qualified_name.split("/")[1]
                if len(connection_qualified_name.split("/")) > 1
                else ""
            )
        else:
            fields = dataverse_entity_qualified_name.split("/")
            if len(fields) < 3:
                raise ValueError("dataverse_entity_qualified_name is invalid")
            connection_qualified_name = "/".join(fields[:3])
            connector_name = fields[1]
        return cls(
            name=name,
            qualified_name=f"{dataverse_entity_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            dataverse_entity_qualified_name=dataverse_entity_qualified_name,
            dataverse_entity=RelatedDataverseEntity(
                unique_attributes={"qualifiedName": dataverse_entity_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "DataverseAttribute":
        """Create a DataverseAttribute instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "DataverseAttribute":
        """Return only fields required for update operations."""
        return DataverseAttribute.updater(
            qualified_name=self.qualified_name,
            name=self.name,
        )
