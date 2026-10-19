# INTERNAL_IMPORT: from pyatlan.model import looker_qn
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        dashboard_qualified_name: str,
        tile_id: str | int,
        look_qualified_name: str | None = None,
    ) -> "LookerTile":
        """
        Create a new LookerTile, keyed as atlan-looker-app keys it:
        ``{connection_qualified_name}/tile/{tile_id}``. The qualifiedName is not nested
        under the dashboard.

        Args:
            name: Name of the tile
            dashboard_qualified_name: Unique name of the dashboard that holds the tile
            tile_id: Looker id of the tile. A whole float (``11.0``) is written as ``11``.
            look_qualified_name: Unique name of the look the tile shows, for a look tile

        Returns:
            LookerTile instance ready to be created
        """
        validate_required_fields(
            ["name", "dashboard_qualified_name", "tile_id"],
            [name, dashboard_qualified_name, tile_id],
        )
        connection_qn = looker_qn.parse_content(
            "dashboard", dashboard_qualified_name
        ).connection_qualified_name
        source_id = looker_qn.looker_id(tile_id, "tile_id")
        tile = cls(
            name=name,
            qualified_name=f"{connection_qn}/tile/{source_id}",
            connection_qualified_name=connection_qn,
            connector_name=looker_qn.connector_name(connection_qn),
            dashboard=RelatedLookerDashboard(qualified_name=dashboard_qualified_name),
        )
        if look_qualified_name is not None:
            looker_qn.parse_content("look", look_qualified_name, connection_qn)
            tile.look = RelatedLookerLook(qualified_name=look_qualified_name)
        return tile

    @classmethod
    def create(cls, **kwargs) -> "LookerTile":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "LookerTile":
        return cls.updater(**kwargs)
