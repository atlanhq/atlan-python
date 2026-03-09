# INTERNAL_IMPORT: from pyatlan.model.assets.related_entity import SaveSemantic
# INTERNAL_IMPORT: from pyatlan.model.core import Announcement
# INTERNAL_IMPORT: from pyatlan.model.enums import AnnouncementType

    @classmethod
    def ref_by_guid(
        cls, guid: str, semantic: "SaveSemantic | str" = SaveSemantic.REPLACE
    ) -> "Asset":
        """
        Create a minimal reference to this asset type by its GUID.

        Args:
            guid: Globally unique identifier of the asset
            semantic: Save semantic (REPLACE, APPEND, REMOVE)

        Returns:
            Asset reference instance
        """
        if isinstance(semantic, str):
            semantic = SaveSemantic(semantic)
        return cls(guid=guid, type_name=cls.__name__, semantic=semantic)

    @classmethod
    def ref_by_qualified_name(
        cls, qualified_name: str, semantic: "SaveSemantic | str" = SaveSemantic.REPLACE
    ) -> "Asset":
        """
        Create a minimal reference to this asset type by its qualifiedName.

        Args:
            qualified_name: Unique fully-qualified name of the asset
            semantic: Save semantic (REPLACE, APPEND, REMOVE)

        Returns:
            Asset reference instance
        """
        if isinstance(semantic, str):
            semantic = SaveSemantic(semantic)
        return cls(
            qualified_name=qualified_name, type_name=cls.__name__, semantic=semantic
        )

    def set_announcement(self, announcement) -> None:
        """
        Set an announcement on this asset.

        Args:
            announcement: Announcement object with type, title, and message
        """
        self.announcement_type = announcement.announcement_type.value
        self.announcement_title = announcement.announcement_title
        self.announcement_message = announcement.announcement_message

    def remove_announcement(self) -> "Asset":
        """
        Remove the announcement from this asset.

        Returns:
            Self for fluent chaining
        """
        self.announcement_type = None
        self.announcement_title = None
        self.announcement_message = None
        return self

    def get_announcment(self):
        """Return an Announcement object for this asset, or None if no announcement is set."""
        from pyatlan_v9.model.core import Announcement
        from pyatlan_v9.model.enums import AnnouncementType

        ann_type = self.announcement_type
        ann_title = self.announcement_title
        if ann_type and ann_title and ann_type is not UNSET and ann_title is not UNSET:
            return Announcement(
                announcement_type=AnnouncementType[str(ann_type).upper()],
                announcement_title=ann_title,
                announcement_message=self.announcement_message
                if self.announcement_message is not UNSET
                else None,
            )
        return None

    def remove_certificate(self) -> "Asset":
        """
        Remove the certificate from this asset.

        Returns:
            Self for fluent chaining
        """
        self.certificate_status = None
        self.certificate_status_message = None
        return self

    def remove_description(self) -> "Asset":
        """
        Remove the description from this asset.

        Returns:
            Self for fluent chaining
        """
        self.description = None
        return self

    def remove_user_description(self) -> "Asset":
        """
        Remove the user description from this asset.

        Returns:
            Self for fluent chaining
        """
        self.user_description = None
        return self

    def remove_owners(self) -> "Asset":
        """
        Remove the owners from this asset.

        Returns:
            Self for fluent chaining
        """
        self.owner_groups = None
        self.owner_users = None
        return self

    def validate_required(self) -> None:
        """Validate required fields before save (no-op in v9 msgspec models)."""
        pass

    def flush_custom_metadata(self, client=None) -> None:
        """
        Flush (clear) all custom metadata on this asset.

        Args:
            client: AtlanClient instance (for compatibility with legacy API)
        """
        self.business_attributes = {}

    async def get_custom_metadata_async(self, client, name: str):
        """Async: get custom metadata by name."""
        from pyatlan_v9.model.aio.custom_metadata import AsyncCustomMetadataProxy

        proxy = AsyncCustomMetadataProxy(
            business_attributes=self.business_attributes, client=client
        )
        return await proxy.get_custom_metadata(name=name)

    async def set_custom_metadata_async(self, client, custom_metadata) -> None:
        """Async: set custom metadata and immediately update business_attributes."""
        from pyatlan_v9.model.aio.custom_metadata import AsyncCustomMetadataProxy

        proxy = AsyncCustomMetadataProxy(
            business_attributes=self.business_attributes, client=client
        )
        await proxy.set_custom_metadata(custom_metadata=custom_metadata)
        self.business_attributes = await proxy.business_attributes()

    async def flush_custom_metadata_async(self, client=None) -> None:
        """Flush custom metadata to business_attributes (no-op since set writes immediately)."""
        pass

    @classmethod
    def updater(cls, qualified_name: str = "", name: str = "") -> "Asset":
        """
        Create an asset for modification (update operations).

        Args:
            qualified_name: Unique name of the asset
            name: Name of the asset

        Returns:
            Asset instance configured for update operations

        Raises:
            ValueError: If required parameters are missing
        """
        if not qualified_name:
            raise ValueError("qualified_name is required")
        if not name:
            raise ValueError("name is required")

        return cls(qualified_name=qualified_name, name=name)

    @classmethod
    def create_for_modification(
        cls, qualified_name: str = "", name: str = ""
    ) -> "Asset":
        """
        Create an asset for modification (deprecated - use updater instead).

        Args:
            qualified_name: Unique name of the asset
            name: Name of the asset

        Returns:
            Asset instance configured for update operations
        """
        return cls.updater(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "Asset":
        """
        Trim this asset to only the required fields for an update.

        Returns:
            Asset with only qualified_name and name set
        """
        return self.__class__.updater(
            qualified_name=self.qualified_name
            if self.qualified_name is not UNSET
            else "",
            name=self.name if self.name is not UNSET else "",
        )
