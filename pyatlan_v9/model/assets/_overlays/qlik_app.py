# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        qlik_id: str,
        space_qualified_name: str,
    ) -> "QlikApp":
        """
        Build a Qlik app; qualifiedName is {connection}/app/{qlik_id}.

        space_qualified_name is the qualifiedName of the QlikSpace
        ({connection}/space/{id}) or QlikStream ({connection}/stream/{id})
        the app lives in. Its segment decides which type the qlik_space
        relationship points at.
        """
        validate_required_fields(
            ["name", "qlik_id", "space_qualified_name"],
            [name, qlik_id, space_qualified_name],
        )
        space_parts = space_qualified_name.rsplit("/", 2)
        if len(space_parts) != 3 or space_parts[1] not in ("space", "stream"):
            raise ValueError(
                "space_qualified_name must end in /space/<id> or /stream/<id>"
            )
        connection_qualified_name, space_kind, space_id = space_parts
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/app/{qlik_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            qlik_id=qlik_id,
            qlik_space_id=space_id,
            qlik_space_qualified_name=space_qualified_name,
            qlik_space=RelatedQlikSpace(
                type_name="QlikStream" if space_kind == "stream" else "QlikSpace",
                qualified_name=space_qualified_name,
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "QlikApp":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "QlikApp":
        return cls.updater(**kwargs)
