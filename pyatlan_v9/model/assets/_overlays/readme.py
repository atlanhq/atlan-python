# STDLIB_IMPORT: from urllib.parse import quote, unquote
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @property
    def description(self) -> Union[str, None, UnsetType]:
        """Decode URL-encoded description content for parity with legacy models."""
        if self.user_description is not UNSET:
            return (
                unquote(self.user_description)
                if self.user_description is not None
                else None
            )
        if self.asset_source_readme is not UNSET:
            return (
                unquote(self.asset_source_readme)
                if self.asset_source_readme is not None
                else None
            )
        return UNSET

    @description.setter
    def description(self, description: Union[str, None, UnsetType]) -> None:
        """Store README content in user_description with URL encoding."""
        if description is UNSET:
            self.user_description = UNSET
            return
        self.user_description = quote(description) if description is not None else None

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        asset: Asset,
        content: str,
        asset_name: Union[str, None] = None,
    ) -> "Readme":
        """Create a new Readme asset."""
        validate_required_fields(["asset", "content"], [asset, content])
        actual_asset_name = asset.name if asset.name is not UNSET else None
        if actual_asset_name:
            if asset_name:
                raise ValueError(
                    "asset_name can not be given when name is available from asset"
                )
            asset_name = actual_asset_name
        elif not asset_name:
            raise ValueError(
                "asset_name is required when name is not available from asset"
            )
        if asset.guid is UNSET or not asset.guid:
            raise ValueError(
                "asset guid must be present, use the client.asset.ref_by_guid() method to retrieve an asset by its GUID"
            )
        return cls(
            qualified_name=f"{asset.guid}/readme",
            name=f"{asset_name} Readme",
            asset=RelatedAsset(guid=asset.guid),
            user_description=quote(content),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "Readme":
        """Create a Readme instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "Readme":
        """Return only fields required for update operations."""
        return Readme.updater(qualified_name=self.qualified_name, name=self.name)
