# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        path: str,
        volume_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "DatabricksVolumePath":
        validate_required_fields(
            ["path", "volume_qualified_name"], [path, volume_qualified_name]
        )
        fields = volume_qualified_name.split("/")
        if len(fields) != 6:
            raise ValueError(
                f"Invalid volume_qualified_name: {volume_qualified_name}. "
                "Expected format: default/connector/connection_id/catalog/schema/volume"
            )
        if "/Volumes/" not in path:
            raise ValueError(
                f"Invalid path: {path}. Expected a Unity Catalog volume path, "
                "e.g. /Volumes/catalog/schema/volume/dir/file.csv"
            )
        parts = path.split("/Volumes", 1)[1].strip("/").split("/")
        if len(parts) < 3 or not all(parts[:3]):
            raise ValueError(
                f"Invalid path: {path}. Expected /Volumes/catalog/schema/volume[/...]"
            )
        file_path = "/".join(parts[3:])
        connection_qn = connection_qualified_name or "/".join(fields[:3])
        return cls(
            name=path,
            # The volume root keeps a trailing slash: "{volume_qn}/".
            qualified_name=f"{volume_qualified_name}/{file_path}",
            database_name=fields[3],
            database_qualified_name=f"{connection_qn}/{fields[3]}",
            schema_name=fields[4],
            schema_qualified_name="/".join(fields[:5]),
            connector_name=fields[1],
            connection_qualified_name=connection_qn,
            databricks_volume_path_path=path if file_path else "/",
            databricks_volume_path_volume_name=fields[5],
            databricks_volume_path_volume_qualified_name=volume_qualified_name,
            databricks_volume=RelatedDatabricksVolume(
                qualified_name=volume_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "DatabricksVolumePath":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "DatabricksVolumePath":
        return cls.updater(**kwargs)
