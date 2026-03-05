# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        file_type: str,
    ) -> "File":
        """
        Create a new File asset.

        Args:
            name: Simple name of the file
            connection_qualified_name: Unique name of the connection in which this file exists
            file_type: Type of the file (e.g., PDF, CSV)

        Returns:
            New File instance with all fields populated

        Raises:
            ValueError: If required parameters are missing or blank
        """
        if isinstance(name, str) and name.strip() == "":
            raise ValueError("name cannot be blank")
        if (
            isinstance(connection_qualified_name, str)
            and connection_qualified_name.strip() == ""
        ):
            raise ValueError("connection_qualified_name cannot be blank")
        if isinstance(file_type, str) and file_type.strip() == "":
            raise ValueError("file_type cannot be blank")
        validate_required_fields(
            ["name", "connection_qualified_name", "file_type"],
            [name, connection_qualified_name, file_type],
        )

        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        qualified_name = f"{connection_qualified_name}/{name}"

        return cls(
            name=name,
            qualified_name=qualified_name,
            file_type=file_type,
            connector_name=connector_name,
            connection_qualified_name=connection_qualified_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "File":
        """
        Create a File instance for updating an existing asset.

        Args:
            qualified_name: Unique name of the file to update
            name: Simple name of the file

        Returns:
            File instance configured for updates

        Raises:
            ValueError: If required parameters are missing
        """
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "File":
        """
        Return a File with only required fields for reference.

        Returns:
            File instance with only qualified_name and name set
        """
        return File(qualified_name=self.qualified_name, name=self.name)

    @classmethod
    def create(cls, **kwargs) -> "File":
        """Backward compatibility alias for creator()."""
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "File":
        """Backward compatibility alias for updater()."""
        return cls.updater(**kwargs)
