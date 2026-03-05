# IMPORT: from pyatlan.model.utils import construct_object_key
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        gcs_bucket_name: str,
        gcs_bucket_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "GCSObject":
        """
        Create a new GCSObject asset.

        Args:
            name: Name of the object
            gcs_bucket_name: Simple name of the bucket
            gcs_bucket_qualified_name: Unique name of the bucket
            connection_qualified_name: Unique name of the connection (optional,
                derived from gcs_bucket_qualified_name if not provided)

        Returns:
            GCSObject instance ready to be created

        Raises:
            ValueError: If required parameters are missing
        """
        validate_required_fields(
            ["name", "gcs_bucket_name", "gcs_bucket_qualified_name"],
            [name, gcs_bucket_name, gcs_bucket_qualified_name],
        )
        if connection_qualified_name:
            connector_name = connection_qualified_name.split("/")[1]
        else:
            # Derive connection_qualified_name from gcs_bucket_qualified_name
            # gcs_bucket_qualified_name format: "default/gcs/123456789/mybucket"
            parts = gcs_bucket_qualified_name.split("/")
            connection_qualified_name = "/".join(parts[:3])
            connector_name = parts[1]

        return cls(
            name=name,
            connection_qualified_name=connection_qualified_name,
            qualified_name=f"{gcs_bucket_qualified_name}/{name}",
            connector_name=connector_name,
            gcs_bucket_name=gcs_bucket_name,
            gcs_bucket_qualified_name=gcs_bucket_qualified_name,
        )

    @classmethod
    @init_guid
    def creator_with_prefix(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        gcs_bucket_name: str,
        gcs_bucket_qualified_name: str,
        prefix: str = "",
    ) -> "GCSObject":
        """
        Create a new GCSObject asset using a prefix-based object key.

        Args:
            name: Name of the object
            connection_qualified_name: Unique name of the connection
            gcs_bucket_name: Simple name of the bucket
            gcs_bucket_qualified_name: Unique name of the bucket
            prefix: Prefix (folder path) for the object

        Returns:
            GCSObject instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            [
                "name",
                "connection_qualified_name",
                "gcs_bucket_name",
                "gcs_bucket_qualified_name",
            ],
            [
                name,
                connection_qualified_name,
                gcs_bucket_name,
                gcs_bucket_qualified_name,
            ],
        )
        fields = connection_qualified_name.split("/")
        if len(fields) != 3:
            raise ValueError("Invalid connection_qualified_name")
        if fields[0].replace(" ", "") == "" or fields[2].replace(" ", "") == "":
            raise ValueError("Invalid connection_qualified_name")
        if fields[1].lower() != "gcs":
            raise ValueError("Invalid connection_qualified_name")

        connector_name = fields[1]
        object_key = construct_object_key(prefix, name)
        return cls(
            name=name,
            gcs_object_key=object_key,
            connection_qualified_name=connection_qualified_name,
            qualified_name=f"{gcs_bucket_qualified_name}/{object_key}",
            connector_name=connector_name,
            gcs_bucket_name=gcs_bucket_name,
            gcs_bucket_qualified_name=gcs_bucket_qualified_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "GCSObject":
        """
        Create a GCSObject instance for modification.

        Args:
            qualified_name: Unique name of the GCSObject to update
            name: Human-readable name of the GCSObject

        Returns:
            GCSObject instance ready for update

        Raises:
            ValueError: If required parameters are missing
        """
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "GCSObject":
        """
        Return a copy of this GCSObject with only the minimum required fields for update.

        Returns:
            GCSObject with only qualified_name and name set
        """
        return GCSObject.updater(qualified_name=self.qualified_name, name=self.name)
