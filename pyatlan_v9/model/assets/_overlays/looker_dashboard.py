# INTERNAL_IMPORT: from pyatlan.model import looker_qn
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        dashboard_id: str | int,
        folder_qualified_name: str | None = None,
        folder_name: str | None = None,
    ) -> "LookerDashboard":
        """
        Create a new LookerDashboard, keyed as atlan-looker-app keys it:
        ``{connection_qualified_name}/dashboard/{dashboard_id}``.

        Args:
            name: Name of the dashboard
            connection_qualified_name: Unique name of the Looker connection
            dashboard_id: Looker id of the dashboard. A whole float (``11.0``) is written as ``11``.
            folder_qualified_name: Unique name of the folder that holds the dashboard, if any
            folder_name: Name of that folder

        Returns:
            LookerDashboard instance ready to be created
        """
        validate_required_fields(
            ["name", "connection_qualified_name", "dashboard_id"],
            [name, connection_qualified_name, dashboard_id],
        )
        connection_qn = looker_qn.connection(connection_qualified_name)
        source_id = looker_qn.looker_id(dashboard_id, "dashboard_id")
        dashboard = cls(
            name=name,
            qualified_name=f"{connection_qn}/dashboard/{source_id}",
            connection_qualified_name=connection_qn,
            connector_name=looker_qn.connector_name(connection_qn),
        )
        if folder_qualified_name is not None:
            looker_qn.parse_folder(folder_qualified_name, connection_qn)
            dashboard.folder = RelatedLookerFolder(qualified_name=folder_qualified_name)
            if folder_name is not None:
                dashboard.folder_name = folder_name
        elif folder_name is not None:
            raise ValueError("folder_name requires folder_qualified_name")
        return dashboard

    @classmethod
    def create(cls, **kwargs) -> "LookerDashboard":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "LookerDashboard":
        return cls.updater(**kwargs)
