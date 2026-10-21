# STDLIB_IMPORT: import re
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        parent_qualified_name: str,
        parent_name: Union[str, None] = None,
    ) -> "SapErpColumn":
        """
        Build a SAP ERP column under a table, view or CDS view.

        name is the raw SAP field name. As atlan-saperp-app does, the qualifiedName
        uses it cleaned (every non-word character replaced by "_"):
        {connection_qualified_name}/column/{cleaned parent name}/{cleaned name}.
        The parent type and its cleaned name are read from parent_qualified_name,
        which must end in /table/<name>, /view/<name> or /cdsview/<name>.
        parent_name is the parent's raw SAP name; it defaults to the cleaned one.
        """
        validate_required_fields(
            ["name", "parent_qualified_name"], [name, parent_qualified_name]
        )
        parts = parent_qualified_name.rsplit("/", 2)
        if (
            len(parts) != 3
            or not parts[0]
            or parts[1] not in ("table", "view", "cdsview")
            or not parts[2]
        ):
            raise ValueError("parent_qualified_name is invalid")
        connection_qualified_name, parent_kind, cleaned_parent_name = parts
        cleaned_name = re.sub(r"\W", "_", name.strip(), flags=re.ASCII)
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        parent_name = parent_name or cleaned_parent_name
        asset = cls(
            name=name,
            qualified_name=(
                f"{connection_qualified_name}/column/{cleaned_parent_name}/{cleaned_name}"
            ),
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )
        parent = {"qualifiedName": parent_qualified_name}
        if parent_kind == "table":
            asset.sap_erp_table = RelatedSapErpTable(unique_attributes=parent)
            asset.sap_erp_table_name = parent_name
            asset.sap_erp_table_qualified_name = parent_qualified_name
        elif parent_kind == "view":
            asset.sap_erp_view = RelatedSapErpView(unique_attributes=parent)
            asset.sap_erp_view_name = parent_name
            asset.sap_erp_view_qualified_name = parent_qualified_name
        else:
            asset.sap_erp_cds_view = RelatedSapErpCdsView(unique_attributes=parent)
            asset.sap_erp_cds_view_name = parent_name
            asset.sap_erp_cds_view_qualified_name = parent_qualified_name
        return asset

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SapErpColumn":
        """Create a SapErpColumn instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SapErpColumn":
        """Return only fields required for update operations."""
        return SapErpColumn.updater(qualified_name=self.qualified_name, name=self.name)
