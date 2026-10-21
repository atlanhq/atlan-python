# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        mc_incident_id: str,
        connection_qualified_name: str,
        mc_monitor_qualified_name: Union[str, None] = None,
    ) -> "MCIncident":
        """Create a new MCIncident asset."""
        validate_required_fields(
            ["name", "mc_incident_id", "connection_qualified_name"],
            [name, mc_incident_id, connection_qualified_name],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        mc_monitor: Union[RelatedMCMonitor, UnsetType] = UNSET
        if mc_monitor_qualified_name:
            # A monitor qualifiedName is {connection_qn}/{namespace}/{monitor_id}.
            prefix = f"{connection_qualified_name}/"
            parts = mc_monitor_qualified_name.split("/")
            if not mc_monitor_qualified_name.startswith(prefix):
                raise ValueError("mc_monitor_qualified_name is invalid")
            if len(parts) != len(fields) + 2:
                raise ValueError("mc_monitor_qualified_name is invalid")
            mc_monitor = RelatedMCMonitor(
                unique_attributes={"qualifiedName": mc_monitor_qualified_name}
            )
        return cls(
            name=name,
            mc_incident_id=mc_incident_id,
            qualified_name=f"{connection_qualified_name}/{mc_incident_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            mc_monitor=mc_monitor,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "MCIncident":
        """Create a MCIncident instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "MCIncident":
        """Return only fields required for update operations."""
        return MCIncident.updater(qualified_name=self.qualified_name, name=self.name)
