# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields
# IMPORT: from .iceberg_related import RelatedIcebergCatalog

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        parent_qualified_name: str,
    ) -> "IcebergNamespace":
        """
        Create a new IcebergNamespace asset.

        Namespaces nest to any depth, so the namespace is named by its parent:
        the catalog for a top-level namespace, or the enclosing namespace for a
        nested one. Namespace ``a.b`` in catalog ``cat`` has qualifiedName
        ``{connection}/cat/a/b``.

        Args:
            name: Name of this namespace level (the last segment, e.g. ``b`` for ``a.b``)
            parent_qualified_name: Unique name of the parent catalog or namespace

        Returns:
            IcebergNamespace instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            ["name", "parent_qualified_name"], [name, parent_qualified_name]
        )
        fields = parent_qualified_name.split("/")
        if len(fields) < 4:
            raise ValueError(
                f"Invalid parent_qualified_name: {parent_qualified_name}. "
                "Expected format: default/connector/connection_id/catalog[/namespace...]"
            )
        connection_qualified_name = "/".join(fields[:3])
        catalog_name = fields[3]
        catalog_qualified_name = f"{connection_qualified_name}/{catalog_name}"
        qualified_name = f"{parent_qualified_name}/{name}"
        path = fields[4:] + [name]
        return cls(
            name=name,
            qualified_name=qualified_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
            database_name=catalog_name,
            database_qualified_name=catalog_qualified_name,
            database=RelatedIcebergCatalog(
                unique_attributes={"qualifiedName": catalog_qualified_name}
            ),
            # Matches atlan-iceberg-app: the first namespace segment, not the
            # immediate parent, for any nested namespace.
            iceberg_parent_namespace_qualified_name=(
                f"{catalog_qualified_name}/{path[0]}" if len(path) > 1 else None
            ),
            iceberg_namespace_hierarchy=[
                {
                    "qualifiedName": "/".join([catalog_qualified_name, *path[:i]]),
                    "name": path[i - 1],
                }
                for i in range(1, len(path) + 1)
            ],
        )

    @classmethod
    def create(cls, **kwargs) -> "IcebergNamespace":
        return cls.creator(**kwargs)

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "IcebergNamespace":
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "IcebergNamespace":
        return cls.updater(**kwargs)

    def trim_to_required(self) -> "IcebergNamespace":
        return IcebergNamespace.updater(qualified_name=self.qualified_name, name=self.name)
