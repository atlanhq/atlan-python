# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        qlik_id: str,
        app_qualified_name: str,
        space_qualified_name: Union[str, None] = None,
    ) -> "QlikSheet":
        """
        Build a Qlik sheet; qualifiedName is {app_qualified_name}/sheet/{qlik_id}.

        space_qualified_name is optional and only fills the denormalised
        qlik_space_id / qlik_space_qualified_name of the app's space or stream.
        """
        validate_required_fields(
            ["name", "qlik_id", "app_qualified_name"],
            [name, qlik_id, app_qualified_name],
        )
        app_parts = app_qualified_name.rsplit("/", 2)
        if len(app_parts) != 3 or app_parts[1] != "app":
            raise ValueError("app_qualified_name must end in /app/<id>")
        connection_qualified_name, _, app_id = app_parts
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        asset = cls(
            name=name,
            qualified_name=f"{app_qualified_name}/sheet/{qlik_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            qlik_id=qlik_id,
            qlik_app_id=app_id,
            qlik_app_qualified_name=app_qualified_name,
            qlik_app=RelatedQlikApp(qualified_name=app_qualified_name),
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
    def create(cls, **kwargs) -> "QlikSheet":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "QlikSheet":
        return cls.updater(**kwargs)
