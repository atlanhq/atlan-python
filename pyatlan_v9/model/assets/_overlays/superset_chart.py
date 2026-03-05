# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        superset_dashboard_qualified_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "SupersetChart":
        """Create a new SupersetChart asset."""
        validate_required_fields(
            ["name", "superset_dashboard_qualified_name"],
            [name, superset_dashboard_qualified_name],
        )
        if connection_qualified_name:
            fields = connection_qualified_name.split("/")
            connector_name = fields[1] if len(fields) > 1 else None
        else:
            fields = superset_dashboard_qualified_name.split("/")
            connector_name = fields[1] if len(fields) > 1 else None
            connection_qualified_name = (
                "/".join(fields[:3])
                if len(fields) >= 3
                else superset_dashboard_qualified_name
            )
        return cls(
            name=name,
            superset_dashboard_qualified_name=superset_dashboard_qualified_name,
            connection_qualified_name=connection_qualified_name,
            qualified_name=f"{superset_dashboard_qualified_name}/{name}",
            connector_name=connector_name,
            superset_dashboard=RelatedSupersetDashboard(
                unique_attributes={"qualifiedName": superset_dashboard_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SupersetChart":
        """Create a SupersetChart instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SupersetChart":
        """Return only fields required for update operations."""
        return SupersetChart.updater(qualified_name=self.qualified_name, name=self.name)
