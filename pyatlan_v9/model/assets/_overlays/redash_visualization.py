# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        visualization_id: Union[str, int],
        redash_query_qualified_name: str,
        redash_query_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "RedashVisualization":
        """Create a new RedashVisualization asset."""
        validate_required_fields(
            [
                "name",
                "visualization_id",
                "redash_query_qualified_name",
                "redash_query_name",
            ],
            [name, visualization_id, redash_query_qualified_name, redash_query_name],
        )
        # A query qualifiedName is {connection_qn}/queries/{query_id}.
        parts = redash_query_qualified_name.split("/")
        if len(parts) < 5 or parts[-2] != "queries":
            raise ValueError("redash_query_qualified_name is invalid")
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:-2])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/visualizations/{visualization_id}",
            redash_query_qualified_name=redash_query_qualified_name,
            redash_query_name=redash_query_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            redash_query=RelatedRedashQuery(
                unique_attributes={"qualifiedName": redash_query_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "RedashVisualization":
        """Create a RedashVisualization instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "RedashVisualization":
        """Return only fields required for update operations."""
        return RedashVisualization.updater(
            qualified_name=self.qualified_name, name=self.name
        )
