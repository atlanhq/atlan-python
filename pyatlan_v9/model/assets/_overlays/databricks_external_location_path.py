# STDLIB_IMPORT: import hashlib
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        path: str,
        external_location_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "DatabricksExternalLocationPath":
        validate_required_fields(
            ["path", "external_location_qualified_name"],
            [path, external_location_qualified_name],
        )
        fields = external_location_qualified_name.split("/")
        if len(fields) < 4:
            raise ValueError(
                "Invalid external_location_qualified_name: "
                f"{external_location_qualified_name}. "
                "Expected format: default/connector/connection_id/location_name"
            )
        # The path segment is the md5 of the raw path, as atlan-databricks-app emits it.
        path_hash = hashlib.md5(path.encode("utf-8"), usedforsecurity=False).hexdigest()
        return cls(
            name=path,
            qualified_name=f"{external_location_qualified_name}/{path_hash}",
            connector_name=fields[1],
            connection_qualified_name=connection_qualified_name
            or "/".join(fields[:3]),
            databricks_path=path,
            databricks_parent_name="/".join(fields[3:]),
            databricks_parent_qualified_name=external_location_qualified_name,
            databricks_external_location=RelatedDatabricksExternalLocation(
                qualified_name=external_location_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "DatabricksExternalLocationPath":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "DatabricksExternalLocationPath":
        return cls.updater(**kwargs)
