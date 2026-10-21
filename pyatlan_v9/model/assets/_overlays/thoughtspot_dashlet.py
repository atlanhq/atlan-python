# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        thoughtspot_id: str,
        thoughtspot_liveboard_qualified_name: str,
        thoughtspot_liveboard_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "ThoughtspotDashlet":
        """Create a new ThoughtspotDashlet asset."""
        validate_required_fields(
            [
                "name",
                "thoughtspot_id",
                "thoughtspot_liveboard_qualified_name",
                "thoughtspot_liveboard_name",
            ],
            [
                name,
                thoughtspot_id,
                thoughtspot_liveboard_qualified_name,
                thoughtspot_liveboard_name,
            ],
        )
        # A liveboard qualifiedName is {connection_qn}/liveboards/{liveboard_id}.
        parts = thoughtspot_liveboard_qualified_name.split("/")
        if len(parts) < 5:
            raise ValueError("thoughtspot_liveboard_qualified_name is invalid")
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:3])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/dashlets/{thoughtspot_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            thoughtspot_liveboard_name=thoughtspot_liveboard_name,
            thoughtspot_liveboard_qualified_name=thoughtspot_liveboard_qualified_name,
            thoughtspot_liveboard=RelatedThoughtspotLiveboard(
                unique_attributes={"qualifiedName": thoughtspot_liveboard_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "ThoughtspotDashlet":
        """Create a ThoughtspotDashlet instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "ThoughtspotDashlet":
        """Return only fields required for update operations."""
        return ThoughtspotDashlet.updater(
            qualified_name=self.qualified_name, name=self.name
        )
