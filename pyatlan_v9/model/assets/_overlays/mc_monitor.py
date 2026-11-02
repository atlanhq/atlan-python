# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        mc_monitor_id: str,
        connection_qualified_name: str,
        mc_monitor_namespace: Union[str, None] = None,
    ) -> "MCMonitor":
        """Create a new MCMonitor asset."""
        validate_required_fields(
            ["name", "mc_monitor_id", "connection_qualified_name"],
            [name, mc_monitor_id, connection_qualified_name],
        )
        # Monte Carlo places monitors created in its UI in the "ui" namespace.
        if not mc_monitor_namespace:
            mc_monitor_namespace = "ui"
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            mc_monitor_id=mc_monitor_id,
            mc_monitor_namespace=mc_monitor_namespace,
            qualified_name=f"{connection_qualified_name}/{mc_monitor_namespace}/{mc_monitor_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "MCMonitor":
        """Create a MCMonitor instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "MCMonitor":
        """Return only fields required for update operations."""
        return MCMonitor.updater(qualified_name=self.qualified_name, name=self.name)
