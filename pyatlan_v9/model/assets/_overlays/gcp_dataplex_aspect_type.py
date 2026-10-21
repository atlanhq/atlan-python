# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        resource_name: str,
        connection_qualified_name: str,
    ) -> "GCPDataplexAspectType":
        """
        Builds the minimal object necessary to create a GCPDataplexAspectType.

        ``resource_name`` is the full GCP resource name,
        ``projects/{project}/locations/{location}/aspectTypes/{id}``. The qualifiedName
        is ``{connection_qualified_name}/aspect-type/{resource_name}`` and the name is
        the aspect type id, as atlan-dataplex-app emits them.
        """
        validate_required_fields(
            ["resource_name", "connection_qualified_name"],
            [resource_name, connection_qualified_name],
        )
        parts = resource_name.split("/")
        if (
            len(parts) != 6
            or parts[0] != "projects"
            or parts[2] != "locations"
            or parts[4] != "aspectTypes"
            or not all(part.strip() for part in parts)
        ):
            raise ValueError(
                f"Invalid resource_name: {resource_name}. "
                "Expected format: projects/{project}/locations/{location}/aspectTypes/{id}"
            )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=parts[5],
            qualified_name=f"{connection_qualified_name}/aspect-type/{resource_name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            gcp_dataplex_aspect_type_resource_name=resource_name,
            gcp_dataplex_aspect_type_project=parts[1],
            gcp_dataplex_aspect_type_location=parts[3],
        )

    @classmethod
    def create(cls, **kwargs) -> "GCPDataplexAspectType":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "GCPDataplexAspectType":
        return cls.updater(**kwargs)
