# INTERNAL_IMPORT: from pyatlan.model import looker_qn
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        folder_id: str | int,
        parent_folder_qualified_name: str | None = None,
    ) -> "LookerFolder":
        """
        Create a new LookerFolder, keyed as atlan-looker-app keys it:
        ``{connection_qualified_name}/folder/{folder_id}``.

        Args:
            name: Name of the folder
            connection_qualified_name: Unique name of the Looker connection
            folder_id: Looker id of the folder. A whole float (``11.0``) is written as ``11``.
            parent_folder_qualified_name: Unique name of the parent folder, for a subfolder

        Returns:
            LookerFolder instance ready to be created
        """
        validate_required_fields(
            ["name", "connection_qualified_name", "folder_id"],
            [name, connection_qualified_name, folder_id],
        )
        connection_qn = looker_qn.connection(connection_qualified_name)
        source_id = looker_qn.looker_id(folder_id, "folder_id")
        folder = cls(
            name=name,
            qualified_name=f"{connection_qn}/folder/{source_id}",
            connection_qualified_name=connection_qn,
            connector_name=looker_qn.connector_name(connection_qn),
        )
        if parent_folder_qualified_name is not None:
            looker_qn.parse_folder(
                parent_folder_qualified_name,
                connection_qn,
                "parent_folder_qualified_name",
            )
            folder.looker_parent_folder = RelatedLookerFolder(
                qualified_name=parent_folder_qualified_name
            )
        return folder

    @classmethod
    def create(cls, **kwargs) -> "LookerFolder":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "LookerFolder":
        return cls.updater(**kwargs)
