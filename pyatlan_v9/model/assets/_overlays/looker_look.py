# INTERNAL_IMPORT: from pyatlan.model import looker_qn
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        look_id: str | int,
        folder_qualified_name: str | None = None,
        folder_name: str | None = None,
    ) -> "LookerLook":
        """
        Create a new LookerLook, keyed as atlan-looker-app keys it:
        ``{connection_qualified_name}/look/{look_id}``.

        Args:
            name: Name of the look
            connection_qualified_name: Unique name of the Looker connection
            look_id: Looker id of the look. A whole float (``11.0``) is written as ``11``.
            Leading zeros are dropped from a numeric id, as the app does.
            folder_qualified_name: Unique name of the folder that holds the look, if any
            folder_name: Name of that folder

        Returns:
            LookerLook instance ready to be created
        """
        validate_required_fields(
            ["name", "connection_qualified_name", "look_id"],
            [name, connection_qualified_name, look_id],
        )
        connection_qn = looker_qn.connection(connection_qualified_name)
        source_id = looker_qn.looker_id(look_id, "look_id", numeric=True)
        look = cls(
            name=name,
            qualified_name=f"{connection_qn}/look/{source_id}",
            connection_qualified_name=connection_qn,
            connector_name=looker_qn.connector_name(connection_qn),
        )
        if folder_qualified_name is not None:
            looker_qn.parse_folder(folder_qualified_name, connection_qn)
            look.folder = RelatedLookerFolder(qualified_name=folder_qualified_name)
            if folder_name is not None:
                look.folder_name = folder_name
        elif folder_name is not None:
            raise ValueError("folder_name requires folder_qualified_name")
        return look

    @classmethod
    def create(cls, **kwargs) -> "LookerLook":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "LookerLook":
        return cls.updater(**kwargs)
