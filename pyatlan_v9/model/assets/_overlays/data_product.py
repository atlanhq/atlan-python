# STDLIB_IMPORT: import re
# IMPORT: from pyatlan.errors import ErrorCode
# IMPORT: from pyatlan.model.enums import DataProductStatus
# INTERNAL_IMPORT: from pyatlan.model.data_mesh import DataProductsAssetsDSL
# INTERNAL_IMPORT: from pyatlan.model.search import IndexSearchRequest
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    def _get_super_domain_qualified_name(
        cls, domain_qualified_name: str
    ) -> Union[str, None]:
        """Extract the top-most ancestor domain qualified name."""
        domain_qn_prefix = re.compile(r"(default/domain/[a-zA-Z0-9-]+/super)/.*")
        if domain_qualified_name:
            match = domain_qn_prefix.match(domain_qualified_name)
            if match and match.group(1):
                return match.group(1)
            if domain_qualified_name.startswith("default/domain/"):
                return domain_qualified_name
        return None

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        domain_qualified_name: str,
        asset_selection: IndexSearchRequest,
    ) -> "DataProduct":
        """Create a new DataProduct asset."""
        validate_required_fields(
            ["name", "domain_qualified_name", "asset_selection"],
            [name, domain_qualified_name, asset_selection],
        )
        assets_playbook_filter = '{"condition":"AND","isGroupLocked":false,"rules":[]}'
        return cls(
            name=name,
            data_product_assets_dsl=DataProductsAssetsDSL.get_asset_selection(
                asset_selection
            ),
            data_domain=RelatedDataDomain(
                unique_attributes={"qualifiedName": domain_qualified_name}
            ),
            qualified_name=f"{domain_qualified_name}/product/{name}",
            data_product_assets_playbook_filter=assets_playbook_filter,
            parent_domain_qualified_name=domain_qualified_name,
            super_domain_qualified_name=cls._get_super_domain_qualified_name(
                domain_qualified_name
            ),
            daap_status=DataProductStatus.ACTIVE,
        )

    @classmethod
    @init_guid
    def updater(
        cls,
        *,
        qualified_name: str,
        name: str,
        asset_selection: Union[IndexSearchRequest, None] = None,
    ) -> "DataProduct":
        """Create a DataProduct instance for update operations."""
        validate_required_fields(["name", "qualified_name"], [name, qualified_name])
        fields = qualified_name.split("/")
        if len(fields) < 5:
            raise ValueError(f"Invalid data product qualified_name: {qualified_name}")
        product = cls(qualified_name=qualified_name, name=name)
        if asset_selection:
            product.data_product_assets_dsl = DataProductsAssetsDSL.get_asset_selection(
                asset_selection
            )
        return product

    def trim_to_required(self) -> "DataProduct":
        """Return only the required fields for updates."""
        return DataProduct.updater(qualified_name=self.qualified_name, name=self.name)

    def get_assets(self, client: "AtlanClient"):
        """Retrieve assets linked to this data product."""
        dp_dsl = self.data_product_assets_dsl
        if not dp_dsl:
            raise ErrorCode.MISSING_DATA_PRODUCT_ASSET_DSL.exception_with_parameters()
        query_data = msgspec.json.decode(dp_dsl).get("query", {})
        request = msgspec.convert(query_data, IndexSearchRequest, strict=False)
        return client.asset.search(request)
