# STDLIB_IMPORT: import uuid
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        anchor: "Asset | None" = None,
        glossary_qualified_name: str | None = None,
        glossary_guid: str | None = None,
        categories: list["RelatedAtlasGlossaryCategory"] | None = None,
    ) -> "AtlasGlossaryTerm":
        """
        Create a new AtlasGlossaryTerm asset.

        Args:
            name: Simple name of the term
            anchor: Glossary object in which this term is contained (mutually exclusive with glossary_qualified_name and glossary_guid)
            glossary_qualified_name: Qualified name of the glossary (mutually exclusive with anchor and glossary_guid)
            glossary_guid: GUID of the glossary (mutually exclusive with anchor and glossary_qualified_name)
            categories: Optional list of categories to which this term belongs

        Returns:
            New AtlasGlossaryTerm instance

        Raises:
            ValueError: If required parameters are missing or if multiple glossary identifiers are provided
        """
        validate_required_fields(["name"], [name])

        # Validate exactly one glossary identifier is provided
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

        # Generate qualified name
        import uuid

        qualified_name = f"{name}@{uuid.uuid4()}"

        # Create anchor reference based on which parameter was provided
        if anchor is not None:
            # Use provided anchor object
            from msgspec import UNSET as MSGSPEC_UNSET

            if hasattr(anchor, "trim_to_reference") and callable(
                anchor.trim_to_reference
            ):
                anchor_ref = anchor.trim_to_reference()
            else:
                # Fallback: create RelatedAtlasGlossary from anchor attributes
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

        return cls(
            name=name,
            qualified_name=qualified_name,
            anchor=anchor_ref,
            categories=categories,
        )

    @classmethod
    def updater(
        cls, *, qualified_name: str, name: str, glossary_guid: str
    ) -> "AtlasGlossaryTerm":
        """
        Create an AtlasGlossaryTerm instance for updating an existing term.

        Args:
            qualified_name: Unique name of the term to update
            name: Simple name of the term
            glossary_guid: GUID of the glossary containing this term

        Returns:
            AtlasGlossaryTerm instance configured for updates

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

    def trim_to_required(self) -> "AtlasGlossaryTerm":
        """
        Return an AtlasGlossaryTerm with only required fields for reference.

        Returns:
            AtlasGlossaryTerm instance with only required fields set

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

        return AtlasGlossaryTerm(
            qualified_name=self.qualified_name,
            name=self.name,
            anchor=RelatedAtlasGlossary(guid=self.anchor.guid),
        )

    @classmethod
    def create(cls, **kwargs) -> "AtlasGlossaryTerm":
        """Backward compatibility alias for creator()."""
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "AtlasGlossaryTerm":
        """Backward compatibility alias for updater()."""
        return cls.updater(**kwargs)
