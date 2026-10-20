# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        qlik_id: str,
        sheet_qualified_name: str,
        space_qualified_name: Union[str, None] = None,
    ) -> "QlikChart":
        """
        Build a Qlik chart; qualifiedName is {app_qualified_name}/chart/{qlik_id}.

        The chart's qualifiedName hangs off the app, not the sheet: the app is
        taken from sheet_qualified_name ({app_qualified_name}/sheet/{id}).
        space_qualified_name is optional and only fills the denormalised
        qlik_space_id / qlik_space_qualified_name of the app's space or stream.
        """
        validate_required_fields(
            ["name", "qlik_id", "sheet_qualified_name"],
            [name, qlik_id, sheet_qualified_name],
        )
        sheet_parts = sheet_qualified_name.rsplit("/", 4)
        if len(sheet_parts) != 5 or sheet_parts[1] != "app" or sheet_parts[3] != "sheet":
            raise ValueError("sheet_qualified_name must end in /app/<id>/sheet/<id>")
        connection_qualified_name, _, app_id, _, _ = sheet_parts
        app_qualified_name = f"{connection_qualified_name}/app/{app_id}"
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        asset = cls(
            name=name,
            qualified_name=f"{app_qualified_name}/chart/{qlik_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            qlik_id=qlik_id,
            qlik_app_id=app_id,
            qlik_app_qualified_name=app_qualified_name,
            qlik_sheet=RelatedQlikSheet(qualified_name=sheet_qualified_name),
        )
        if space_qualified_name:
            space_parts = space_qualified_name.rsplit("/", 2)
            if len(space_parts) != 3 or space_parts[1] not in ("space", "stream"):
                raise ValueError(
                    "space_qualified_name must end in /space/<id> or /stream/<id>"
                )
            asset.qlik_space_id = space_parts[2]
            asset.qlik_space_qualified_name = space_qualified_name
        return asset

    @classmethod
    def create(cls, **kwargs) -> "QlikChart":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "QlikChart":
        return cls.updater(**kwargs)
