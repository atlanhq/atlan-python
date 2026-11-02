# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        warehouse_id: Union[int, str],
        table_id: str,
        check_id: str,
        linked_asset_qualified_name: Union[str, None] = None,
        linked_asset_type_name: str = "Table",
    ) -> "AnomaloCheck":
        """
        Create a new AnomaloCheck asset.

        :param name: name of the check
        :param connection_qualified_name: unique name of the Anomalo connection
        :param warehouse_id: Anomalo id of the warehouse the checked table is in
        :param table_id: Anomalo id of the checked table
        :param check_id: Anomalo (static) id of the check
        :param linked_asset_qualified_name: (optional) unique name of the asset in Atlan the check runs on
        :param linked_asset_type_name: type of the linked asset (default: Table)
        :returns: AnomaloCheck asset with the provided details
        """
        validate_required_fields(
            [
                "name",
                "connection_qualified_name",
                "warehouse_id",
                "table_id",
                "check_id",
            ],
            [name, connection_qualified_name, warehouse_id, table_id, check_id],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        check = cls(
            name=name,
            qualified_name=(
                f"{connection_qualified_name}/{warehouse_id}/{table_id}"
                f"/check/{check_id}"
            ),
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )
        if linked_asset_qualified_name:
            check.anomalo_check_linked_asset_qualified_name = (
                linked_asset_qualified_name
            )
            check.anomalo_check_asset = RelatedAsset(
                type_name=linked_asset_type_name,
                unique_attributes={"qualifiedName": linked_asset_qualified_name},
            )
        return check

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "AnomaloCheck":
        """Create an AnomaloCheck instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "AnomaloCheck":
        """Return only fields required for update operations."""
        return AnomaloCheck.updater(qualified_name=self.qualified_name, name=self.name)
