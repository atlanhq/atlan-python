# STDLIB_IMPORT: import hashlib
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        parent_qualified_name: str,
    ) -> "QlikColumn":
        """
        Build a Qlik column under a sheet, chart or dataset.

        qualifiedName is {parent_qualified_name}/column/{md5}, where md5 is taken
        over "{parent path}/column/{name}" and the parent path is the parent's
        qualifiedName without the connection (app/<id>/sheet/<id>,
        app/<id>/chart/<id> or dataset/<id>), exactly as atlan-qlik-sense-app
        builds it. The parent type is read from parent_qualified_name.
        """
        validate_required_fields(
            ["name", "parent_qualified_name"], [name, parent_qualified_name]
        )
        dataset_parts = parent_qualified_name.rsplit("/", 2)
        app_parts = parent_qualified_name.rsplit("/", 4)
        if len(dataset_parts) == 3 and dataset_parts[1] == "dataset":
            connection_qualified_name, parent_kind = dataset_parts[0], "dataset"
        elif (
            len(app_parts) == 5
            and app_parts[1] == "app"
            and app_parts[3] in ("sheet", "chart")
        ):
            connection_qualified_name, parent_kind = app_parts[0], app_parts[3]
        else:
            raise ValueError(
                "parent_qualified_name must end in /app/<id>/sheet/<id>, "
                "/app/<id>/chart/<id> or /dataset/<id>"
            )
        parent_path = parent_qualified_name[len(connection_qualified_name) + 1 :]
        # deepcode ignore InsecureHash/test: an identifier, not a security key
        column_hash = hashlib.md5(  # noqa: S324
            f"{parent_path}/column/{name}".encode("utf-8")
        ).hexdigest()
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        asset = cls(
            name=name,
            qualified_name=f"{parent_qualified_name}/column/{column_hash}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            qlik_column_name=name,
            qlik_parent_qualified_name=parent_qualified_name,
        )
        if parent_kind == "sheet":
            asset.qlik_sheet = RelatedQlikSheet(qualified_name=parent_qualified_name)
        elif parent_kind == "chart":
            asset.qlik_chart = RelatedQlikChart(qualified_name=parent_qualified_name)
        else:
            asset.qlik_dataset = RelatedQlikDataset(
                qualified_name=parent_qualified_name
            )
        return asset

    @classmethod
    def create(cls, **kwargs) -> "QlikColumn":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "QlikColumn":
        return cls.updater(**kwargs)
