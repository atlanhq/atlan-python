# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        workbook_id: str,
    ) -> "SigmaWorkbook":
        validate_required_fields(
            ["name", "connection_qualified_name", "workbook_id"],
            [name, connection_qualified_name, workbook_id],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/{workbook_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def create(cls, **kwargs) -> "SigmaWorkbook":
        return cls.creator(**kwargs)

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SigmaWorkbook":
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "SigmaWorkbook":
        return cls.updater(**kwargs)

    def trim_to_required(self) -> "SigmaWorkbook":
        return SigmaWorkbook.updater(qualified_name=self.qualified_name, name=self.name)
