# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        adf_pipeline_qualified_name: str,
        adf_factory_name: Union[str, None] = None,
        connection_qualified_name: Union[str, None] = None,
    ) -> "AdfActivity":
        """Create a new AdfActivity asset."""
        validate_required_fields(
            ["name", "adf_pipeline_qualified_name"],
            [name, adf_pipeline_qualified_name],
        )
        # A pipeline qualifiedName is {connection_qn}/factory/{factory}/pipeline/{pipeline}.
        parts = adf_pipeline_qualified_name.split("/")
        if len(parts) != 7 or parts[3] != "factory" or parts[5] != "pipeline":
            raise ValueError("adf_pipeline_qualified_name is invalid")
        if not adf_factory_name:
            adf_factory_name = parts[4]
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:3])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{adf_pipeline_qualified_name}/activities/{name}",
            adf_pipeline_qualified_name=adf_pipeline_qualified_name,
            adf_factory_name=adf_factory_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            adf_pipeline=RelatedAdfPipeline(
                unique_attributes={"qualifiedName": adf_pipeline_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "AdfActivity":
        """Create an AdfActivity instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "AdfActivity":
        """Return only fields required for update operations."""
        return AdfActivity.updater(qualified_name=self.qualified_name, name=self.name)
