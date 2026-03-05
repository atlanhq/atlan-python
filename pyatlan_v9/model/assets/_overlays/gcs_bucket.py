# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> "GCSBucket":
        """
        Create a new GCSBucket asset.

        Args:
            name: Name of the bucket
            connection_qualified_name: Unique name of the connection

        Returns:
            GCSBucket instance ready to be created

        Raises:
            ValueError: If required parameters are missing
        """
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        # Extract connector name from the connection_qualified_name
        connector_name = connection_qualified_name.split("/")[1]
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "GCSBucket":
        """
        Create a GCSBucket instance for modification.

        Args:
            qualified_name: Unique name of the GCSBucket to update
            name: Human-readable name of the GCSBucket

        Returns:
            GCSBucket instance ready for update

        Raises:
            ValueError: If required parameters are missing
        """
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "GCSBucket":
        """
        Return a copy of this GCSBucket with only the minimum required fields for update.

        Returns:
            GCSBucket with only qualified_name and name set
        """
        return GCSBucket.updater(qualified_name=self.qualified_name, name=self.name)
