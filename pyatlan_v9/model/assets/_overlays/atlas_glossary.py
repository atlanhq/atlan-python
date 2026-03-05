# STDLIB_IMPORT: import uuid
# INTERNAL_IMPORT: from pyatlan.utils import init_guid

    @classmethod
    @init_guid
    def creator(cls, *, name: str) -> "AtlasGlossary":
        """
        Create a new AtlasGlossary asset.

        Args:
            name: Name of the glossary

        Returns:
            AtlasGlossary instance ready to be created

        Raises:
            ValueError: If name is not provided
        """
        if not name:
            raise ValueError("name is required")

        # Generate a unique qualified name using a simple ID generator
        import uuid

        qualified_name = str(uuid.uuid4().hex[:16])

        return AtlasGlossary(name=name, qualified_name=qualified_name)

    @classmethod
    def create(cls, *, name: str) -> "AtlasGlossary":
        """
        Create a new AtlasGlossary asset (deprecated - use creator instead).

        Args:
            name: Name of the glossary

        Returns:
            AtlasGlossary instance ready to be created
        """
        return cls.creator(name=name)
