# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        application_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "ApplicationField":
        """Create a new ApplicationField asset."""
        validate_required_fields(
            ["name", "application_qualified_name"], [name, application_qualified_name]
        )
        if connection_qualified_name:
            connector_name = (
                connection_qualified_name.split("/")[1]
                if len(connection_qualified_name.split("/")) > 1
                else ""
            )
        else:
            fields = application_qualified_name.split("/")
            if len(fields) < 3:
                raise ValueError("application_qualified_name is invalid")
            connection_qualified_name = "/".join(fields[:3])
            connector_name = fields[1]
        return cls(
            name=name,
            qualified_name=f"{application_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            application_parent_qualified_name=application_qualified_name,
            application_parent=RelatedApplication(
                unique_attributes={"qualifiedName": application_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "ApplicationField":
        """Create an ApplicationField instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "ApplicationField":
        """Return only fields required for update operations."""
        return ApplicationField.updater(
            qualified_name=self.qualified_name,
            name=self.name,
        )
