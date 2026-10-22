# STDLIB_IMPORT: import hashlib
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connector_id: str,
        destination_id: str,
        connection_qualified_name: str,
    ) -> "FivetranConnector":
        """
        Create a new FivetranConnector asset.

        The qualified name mirrors atlan-fivetran-app:
        ``{connection_qualified_name}/{sha1(connector_id + "-" + destination_id)}``.

        Args:
            name: Display name of the connector.
            connector_id: Fivetran connector (connection) ID.
            destination_id: Fivetran destination (group) ID.
            connection_qualified_name: Qualified name of the Fivetran connection.

        Returns:
            A new FivetranConnector instance.
        """
        validate_required_fields(
            ["name", "connector_id", "destination_id", "connection_qualified_name"],
            [name, connector_id, destination_id, connection_qualified_name],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        connector_hash = hashlib.sha1(  # noqa: S324
            f"{connector_id}-{destination_id}".encode("utf-8")
        ).hexdigest()
        connector_url = (
            f"https://fivetran.com/dashboard/connectors/{connector_id}"
            f"/status?groupId={destination_id}"
        )
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/{connector_hash}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            fivetran_connector_url=connector_url,
            fivetran_connector_destination_url=(
                f"https://fivetran.com/dashboard/warehouse?groupId={destination_id}"
            ),
            source_url=connector_url,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "FivetranConnector":
        """Create a FivetranConnector instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "FivetranConnector":
        """Return only fields required for update operations."""
        return FivetranConnector.updater(
            qualified_name=self.qualified_name, name=self.name
        )
