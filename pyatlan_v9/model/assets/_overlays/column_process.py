# STDLIB_IMPORT: import hashlib
# STDLIB_IMPORT: from io import StringIO
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @staticmethod
    def _extract_guid(relationship: Any) -> Union[str, None]:
        """Extract guid from a relationship-like object."""
        if relationship is None:
            return None
        guid = getattr(relationship, "guid", UNSET)
        if guid is UNSET or not guid:
            return None
        return guid

    @staticmethod
    def _to_related_catalog(value: Any) -> RelatedCatalog:
        """Convert any relationship-like value to a RelatedCatalog reference."""
        if isinstance(value, RelatedCatalog):
            return value
        guid = getattr(value, "guid", UNSET)
        type_name = getattr(value, "type_name", UNSET)
        if guid is not UNSET and guid:
            kwargs: dict[str, Any] = {"guid": guid}
            if type_name is not UNSET and type_name:
                kwargs["type_name"] = type_name
            return RelatedCatalog(**kwargs)
        qualified_name = getattr(value, "qualified_name", UNSET)
        if qualified_name is not UNSET and qualified_name:
            kwargs = {"unique_attributes": {"qualifiedName": qualified_name}}
            if type_name is not UNSET and type_name:
                kwargs["type_name"] = type_name
            return RelatedCatalog(**kwargs)
        return RelatedCatalog()

    @staticmethod
    def _to_related_process(value: Any) -> RelatedProcess:
        """Convert any relationship-like value to a RelatedProcess reference."""
        if isinstance(value, RelatedProcess):
            return value
        guid = getattr(value, "guid", UNSET)
        type_name = getattr(value, "type_name", UNSET)
        if guid is not UNSET and guid:
            kwargs: dict[str, Any] = {"guid": guid}
            if type_name is not UNSET and type_name:
                kwargs["type_name"] = type_name
            return RelatedProcess(**kwargs)
        qualified_name = getattr(value, "qualified_name", UNSET)
        if qualified_name is not UNSET and qualified_name:
            kwargs = {"unique_attributes": {"qualifiedName": qualified_name}}
            if type_name is not UNSET and type_name:
                kwargs["type_name"] = type_name
            return RelatedProcess(**kwargs)
        return RelatedProcess()

    @staticmethod
    def generate_qualified_name(
        *,
        name: str,
        connection_qualified_name: str,
        inputs: list[Any],
        outputs: list[Any],
        parent: Any,
        process_id: Union[str, None] = None,
    ) -> str:
        """Generate column process qualified name using explicit process_id or deterministic hash."""
        validate_required_fields(
            ["name", "connection_qualified_name", "inputs", "outputs", "parent"],
            [name, connection_qualified_name, inputs, outputs, parent],
        )
        if process_id and process_id.strip():
            return f"{connection_qualified_name}/{process_id}"
        buffer = StringIO()
        buffer.write(name)
        buffer.write(connection_qualified_name)
        parent_guid = ColumnProcess._extract_guid(parent)
        if parent_guid:
            buffer.write(parent_guid)
        for relationship in inputs:
            guid = ColumnProcess._extract_guid(relationship)
            if guid:
                buffer.write(guid)
        for relationship in outputs:
            guid = ColumnProcess._extract_guid(relationship)
            if guid:
                buffer.write(guid)
        hash_seed = buffer.getvalue()
        buffer.close()
        # deepcode ignore InsecureHash/test: this is not used for generating security keys
        return (
            f"{connection_qualified_name}/{hashlib.md5(hash_seed.encode()).hexdigest()}"  # noqa: S324
        )

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        inputs: list[Any],
        outputs: list[Any],
        parent: Any,
        process_id: Union[str, None] = None,
    ) -> "ColumnProcess":
        """Create a new ColumnProcess asset."""
        qualified_name = cls.generate_qualified_name(
            name=name,
            connection_qualified_name=connection_qualified_name,
            inputs=inputs,
            outputs=outputs,
            parent=parent,
            process_id=process_id,
        )
        connector_name = (
            connection_qualified_name.split("/")[1]
            if len(connection_qualified_name.split("/")) > 1
            else ""
        )
        return cls(
            name=name,
            qualified_name=qualified_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qualified_name,
            inputs=[cls._to_related_catalog(item) for item in inputs],
            outputs=[cls._to_related_catalog(item) for item in outputs],
            process=cls._to_related_process(parent),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "ColumnProcess":
        """Create a ColumnProcess instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "ColumnProcess":
        """Return only fields required for update operations."""
        return ColumnProcess.updater(qualified_name=self.qualified_name, name=self.name)
