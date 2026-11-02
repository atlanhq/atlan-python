# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        owner_account: str,
        connection_qualified_name: str,
        kind: Union[str, None] = None,
        snowflake_listing_qualified_name: Union[str, None] = None,
    ) -> "SnowflakeShare":
        """Create a new SnowflakeShare asset."""
        validate_required_fields(
            ["name", "owner_account", "connection_qualified_name"],
            [name, owner_account, connection_qualified_name],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/share/{owner_account}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            snowflake_share_owner_account=owner_account,
            snowflake_share_kind=kind if kind is not None else UNSET,
            snowflake_listing=(
                RelatedSnowflakeListing(
                    unique_attributes={
                        "qualifiedName": snowflake_listing_qualified_name
                    }
                )
                if snowflake_listing_qualified_name
                else UNSET
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SnowflakeShare":
        """Create a SnowflakeShare instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SnowflakeShare":
        """Return only fields required for update operations."""
        return SnowflakeShare.updater(
            qualified_name=self.qualified_name, name=self.name
        )
