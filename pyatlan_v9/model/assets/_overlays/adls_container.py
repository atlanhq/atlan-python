# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        adls_account_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "ADLSContainer":
        validate_required_fields(
            ["name", "adls_account_qualified_name"],
            [name, adls_account_qualified_name],
        )
        if connection_qualified_name:
            fields = connection_qualified_name.split("/")
            connector_name = fields[1] if len(fields) > 1 else None
        else:
            fields = adls_account_qualified_name.split("/")
            connector_name = fields[1] if len(fields) > 1 else None
            connection_qualified_name = (
                "/".join(fields[:3])
                if len(fields) >= 3
                else adls_account_qualified_name
            )

        adls_account_name = adls_account_qualified_name.rsplit("/", 1)[-1]
        qualified_name = f"{adls_account_qualified_name}/{name}"
        return cls(
            name=name,
            qualified_name=qualified_name,
            adls_account_qualified_name=adls_account_qualified_name,
            adls_account_name=adls_account_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qualified_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "ADLSContainer":
        """Create an ADLSContainer instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "ADLSContainer":
        """Return only fields required for update operations."""
        return ADLSContainer.updater(qualified_name=self.qualified_name, name=self.name)
