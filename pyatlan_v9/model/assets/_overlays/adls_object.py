# IMPORT: from pyatlan.model.utils import construct_object_key
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        adls_container_name: str,
        adls_container_qualified_name: str,
        adls_account_qualified_name: str | None = None,
        connection_qualified_name: str | None = None,
    ) -> "ADLSObject":
        validate_required_fields(
            ["name", "adls_container_name", "adls_container_qualified_name"],
            [name, adls_container_name, adls_container_qualified_name],
        )
        if connection_qualified_name:
            fields = connection_qualified_name.split("/")
            connector_name = fields[1] if len(fields) > 1 else None
        else:
            fields = adls_container_qualified_name.split("/")
            connector_name = fields[1] if len(fields) > 1 else None
            connection_qualified_name = (
                "/".join(fields[:3])
                if len(fields) >= 3
                else adls_container_qualified_name
            )

        # Derive account qualified name from container qualified name
        if not adls_account_qualified_name:
            parts = adls_container_qualified_name.rsplit("/", 1)
            adls_account_qualified_name = (
                parts[0] if len(parts) > 1 else adls_container_qualified_name
            )

        qualified_name = f"{adls_container_qualified_name}/{name}"
        return cls(
            name=name,
            qualified_name=qualified_name,
            adls_container_qualified_name=adls_container_qualified_name,
            adls_container_name=adls_container_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qualified_name,
            adls_account_qualified_name=adls_account_qualified_name,
            adls_account_name=adls_account_qualified_name.rsplit("/", 1)[-1],
        )

    @classmethod
    @init_guid
    def creator_with_prefix(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        adls_container_name: str,
        adls_container_qualified_name: str,
        adls_account_qualified_name: str | None = None,
        prefix: str = "",
    ) -> "ADLSObject":
        validate_required_fields(
            [
                "name",
                "connection_qualified_name",
                "adls_container_name",
                "adls_container_qualified_name",
            ],
            [
                name,
                connection_qualified_name,
                adls_container_name,
                adls_container_qualified_name,
            ],
        )
        from pyatlan.model.utils import construct_object_key

        fields = connection_qualified_name.split("/")
        if len(fields) != 3:
            raise ValueError("Invalid connection_qualified_name")
        if fields[0].replace(" ", "") == "" or fields[2].replace(" ", "") == "":
            raise ValueError("Invalid connection_qualified_name")
        if fields[1].lower() != "adls":
            raise ValueError("Invalid connection_qualified_name")
        connector_name = fields[1]

        if not adls_account_qualified_name:
            parts = adls_container_qualified_name.rsplit("/", 1)
            adls_account_qualified_name = (
                parts[0] if len(parts) > 1 else adls_container_qualified_name
            )

        object_key = construct_object_key(prefix, name)
        qualified_name = f"{adls_container_qualified_name}/{object_key}"
        return cls(
            name=name,
            qualified_name=qualified_name,
            adls_object_key=object_key,
            adls_container_qualified_name=adls_container_qualified_name,
            adls_container_name=adls_container_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qualified_name,
            adls_account_qualified_name=adls_account_qualified_name,
            adls_account_name=adls_account_qualified_name.rsplit("/", 1)[-1],
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "ADLSObject":
        """Create an ADLSObject instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "ADLSObject":
        """Return only fields required for update operations."""
        return ADLSObject.updater(qualified_name=self.qualified_name, name=self.name)
