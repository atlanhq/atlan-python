# STDLIB_IMPORT: import uuid
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    def can_be_archived(cls) -> bool:
        return False

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        anchor: "Asset | None" = None,
        glossary_qualified_name: str | None = None,
        glossary_guid: str | None = None,
        parent_category: "AtlasGlossaryCategory | None" = None,
    ) -> "AtlasGlossaryCategory":
        """
        Create a new AtlasGlossaryCategory asset.

        Args:
            name: Simple name of the category
            anchor: Glossary object in which this category is contained (mutually exclusive with glossary_qualified_name and glossary_guid)
            glossary_qualified_name: Qualified name of the glossary (mutually exclusive with anchor and glossary_guid)
            glossary_guid: GUID of the glossary (mutually exclusive with anchor and glossary_qualified_name)
            parent_category: Optional parent category for this category

        Returns:
            New AtlasGlossaryCategory instance

        Raises:
            ValueError: If required parameters are missing or if multiple glossary identifiers are provided
        """
        validate_required_fields(["name"], [name])

        provided_params = [
            p for p in [anchor, glossary_qualified_name, glossary_guid] if p is not None
        ]
        if len(provided_params) == 0:
            raise ValueError(
                "One of the following parameters are required: anchor, glossary_qualified_name, glossary_guid"
            )
        if len(provided_params) > 1:
            param_names = []
            if anchor is not None:
                param_names.append("anchor")
            if glossary_qualified_name is not None:
                param_names.append("glossary_qualified_name")
            if glossary_guid is not None:
                param_names.append("glossary_guid")
            raise ValueError(
                f"Only one of the following parameters are allowed: {', '.join(param_names)}"
            )

        import uuid

        qualified_name = f"{name}@{uuid.uuid4()}"

        from msgspec import UNSET as MSGSPEC_UNSET

        if anchor is not None:
            if hasattr(anchor, "trim_to_reference") and callable(
                anchor.trim_to_reference
            ):
                anchor_ref = anchor.trim_to_reference()
            else:
                anchor_ref = RelatedAtlasGlossary(
                    guid=anchor.guid
                    if hasattr(anchor, "guid") and anchor.guid is not MSGSPEC_UNSET
                    else None,
                    qualified_name=anchor.qualified_name
                    if hasattr(anchor, "qualified_name")
                    and anchor.qualified_name is not MSGSPEC_UNSET
                    else None,
                )
        elif glossary_qualified_name is not None:
            anchor_ref = RelatedAtlasGlossary(qualified_name=glossary_qualified_name)
        else:  # glossary_guid is not None
            anchor_ref = RelatedAtlasGlossary(guid=glossary_guid)

        parent_ref = None
        if parent_category is not None:
            if hasattr(parent_category, "trim_to_reference") and callable(
                parent_category.trim_to_reference
            ):
                parent_ref = parent_category.trim_to_reference()
            else:
                parent_ref = RelatedAtlasGlossaryCategory(
                    guid=parent_category.guid
                    if hasattr(parent_category, "guid")
                    and parent_category.guid is not MSGSPEC_UNSET
                    else None,
                    qualified_name=parent_category.qualified_name
                    if hasattr(parent_category, "qualified_name")
                    and parent_category.qualified_name is not MSGSPEC_UNSET
                    else None,
                )

        kwargs: dict = dict(
            name=name,
            qualified_name=qualified_name,
            anchor=anchor_ref,
        )
        if parent_ref is not None:
            kwargs["parent_category"] = parent_ref
        return cls(**kwargs)

    @classmethod
    def updater(
        cls, *, qualified_name: str, name: str, glossary_guid: str
    ) -> "AtlasGlossaryCategory":
        """
        Create an AtlasGlossaryCategory instance for updating an existing category.

        Args:
            qualified_name: Unique name of the category to update
            name: Simple name of the category
            glossary_guid: GUID of the glossary containing this category

        Returns:
            AtlasGlossaryCategory instance configured for updates

        Raises:
            ValueError: If required parameters are missing
        """
        validate_required_fields(
            ["qualified_name", "name", "glossary_guid"],
            [qualified_name, name, glossary_guid],
        )
        return cls(
            qualified_name=qualified_name,
            name=name,
            anchor=RelatedAtlasGlossary(guid=glossary_guid),
        )

    def trim_to_required(self) -> "AtlasGlossaryCategory":
        """
        Return an AtlasGlossaryCategory with only required fields for reference.

        Returns:
            AtlasGlossaryCategory instance with only required fields set

        Raises:
            ValueError: If anchor or anchor.guid is not available
        """
        if self.anchor is None or self.anchor is UNSET:
            raise ValueError("anchor.guid must be available")
        if (
            not hasattr(self.anchor, "guid")
            or self.anchor.guid is None
            or self.anchor.guid is UNSET
        ):
            raise ValueError("anchor.guid must be available")

        return AtlasGlossaryCategory(
            qualified_name=self.qualified_name,
            name=self.name,
            anchor=RelatedAtlasGlossary(guid=self.anchor.guid),
        )

    @classmethod
    def create(cls, **kwargs) -> "AtlasGlossaryCategory":
        """Backward compatibility alias for creator()."""
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "AtlasGlossaryCategory":
        """Backward compatibility alias for updater()."""
        return cls.updater(**kwargs)
