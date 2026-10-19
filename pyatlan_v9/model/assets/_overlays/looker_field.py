# INTERNAL_IMPORT: from pyatlan.model import looker_qn
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        explore_qualified_name: str | None = None,
        view_qualified_name: str | None = None,
        dashboard_qualified_name: str | None = None,
        look_qualified_name: str | None = None,
        tile_qualified_name: str | None = None,
        tile_id: str | int | None = None,
        refinement_file_path: str | None = None,
        refinement_line_number: str | None = None,
    ) -> "LookerField":
        """
        Create a new LookerField, keyed as atlan-looker-app keys it. Pass exactly one parent:

        - ``explore_qualified_name``: ``{model_qualified_name}/{explore}/{name}``
          (the explore segment has no ``{model}::`` prefix)
        - ``view_qualified_name``: ``{view_qualified_name}/{name}``; with
          ``refinement_file_path``, ``{connection}/{md5(path:line)}/{view path}/{name}``
        - ``dashboard_qualified_name`` and ``tile_id``:
          ``{dashboard_qualified_name}/{tile_id}/{name}``
        - ``look_qualified_name``: ``{look_qualified_name}/{name}``
        - ``tile_qualified_name``: ``{tile_qualified_name}/{name}``

        Args:
            name: Name of the field
            explore_qualified_name: Unique name of the explore, for an explore field
            view_qualified_name: Unique name of the view, for a view field
            dashboard_qualified_name: Unique name of the dashboard, for a dashboard field
            look_qualified_name: Unique name of the look, for a look field
            tile_qualified_name: Unique name of the tile, for a tile field
            tile_id: Looker id of the tile a dashboard field comes from (dashboard fields only)
            refinement_file_path: File that declares the refinement, for a refined explore
                or view field
            refinement_line_number: Line of that refinement in ``refinement_file_path``

        Returns:
            LookerField instance ready to be created
        """
        validate_required_fields(["name"], [name])
        field_name = looker_qn.looker_id(name, "name")
        parents = {
            "explore_qualified_name": explore_qualified_name,
            "view_qualified_name": view_qualified_name,
            "dashboard_qualified_name": dashboard_qualified_name,
            "look_qualified_name": look_qualified_name,
            "tile_qualified_name": tile_qualified_name,
        }
        given = [key for key, value in parents.items() if value is not None]
        if len(given) != 1:
            raise ValueError(
                "Exactly one of explore_qualified_name, view_qualified_name, "
                "dashboard_qualified_name, look_qualified_name or "
                f"tile_qualified_name is required, got {given or 'none'}"
            )
        parent_key = given[0]
        validate_required_fields([parent_key], [parents[parent_key]])
        if tile_id is not None and parent_key != "dashboard_qualified_name":
            raise ValueError("tile_id is only used with dashboard_qualified_name")
        refined = refinement_file_path is not None
        if refinement_line_number is not None and not refined:
            raise ValueError("refinement_line_number requires refinement_file_path")
        if refined:
            validate_required_fields(["refinement_file_path"], [refinement_file_path])
            if parent_key not in ("explore_qualified_name", "view_qualified_name"):
                raise ValueError(
                    "refinement_file_path is only used with explore_qualified_name "
                    "or view_qualified_name"
                )

        attributes: dict = {}
        if explore_qualified_name is not None:
            parent = looker_qn.parse_explore(explore_qualified_name)
            model_qn = (
                f"{parent.connection_qualified_name}/project/{parent.project_name}"
                f"/model/{parent.model_name}"
            )
            qualified_name = f"{model_qn}/{parent.explore_name}/{field_name}"
            attributes.update(
                model_name=parent.model_name,
                model=RelatedLookerModel(qualified_name=model_qn),
                looker_explore_qualified_name=explore_qualified_name,
                explore=RelatedLookerExplore(qualified_name=explore_qualified_name),
            )
        elif view_qualified_name is not None:
            parent = looker_qn.parse_view(view_qualified_name)
            if refined:
                prefix = looker_qn.refinement_hash(
                    refinement_file_path, refinement_line_number or ""
                )
                qualified_name = (
                    f"{parent.connection_qualified_name}/{prefix}"
                    f"/{parent.relative}/{field_name}"
                )
            else:
                qualified_name = f"{view_qualified_name}/{field_name}"
            attributes.update(
                looker_view_qualified_name=view_qualified_name,
                view=RelatedLookerView(qualified_name=view_qualified_name),
            )
        elif dashboard_qualified_name is not None:
            parent = looker_qn.parse_content("dashboard", dashboard_qualified_name)
            source_tile_id = looker_qn.looker_id(tile_id, "tile_id")
            qualified_name = f"{dashboard_qualified_name}/{source_tile_id}/{field_name}"
            attributes.update(
                looker_dashboard_qualified_name=dashboard_qualified_name,
                dashboard=RelatedLookerDashboard(
                    qualified_name=dashboard_qualified_name
                ),
            )
        elif look_qualified_name is not None:
            parent = looker_qn.parse_content("look", look_qualified_name)
            qualified_name = f"{look_qualified_name}/{field_name}"
            attributes.update(
                looker_look_qualified_name=look_qualified_name,
                look=RelatedLookerLook(qualified_name=look_qualified_name),
            )
        else:
            parent = looker_qn.parse_content("tile", tile_qualified_name)
            qualified_name = f"{tile_qualified_name}/{field_name}"
            attributes.update(
                looker_tile_qualified_name=tile_qualified_name,
                tile=RelatedLookerTile(qualified_name=tile_qualified_name),
            )

        if parent.project_name:
            attributes.update(
                project_name=parent.project_name,
                project=RelatedLookerProject(
                    qualified_name=f"{parent.connection_qualified_name}"
                    f"/project/{parent.project_name}"
                ),
            )
        if refined:
            attributes.update(
                looker_field_is_refined=True,
                looker_field_refinement_file_path=refinement_file_path,
                looker_field_refinement_line_number=refinement_line_number,
            )
        return cls(
            name=name,
            qualified_name=qualified_name,
            connection_qualified_name=parent.connection_qualified_name,
            connector_name=looker_qn.connector_name(parent.connection_qualified_name),
            **attributes,
        )

    @classmethod
    def create(cls, **kwargs) -> "LookerField":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "LookerField":
        return cls.updater(**kwargs)
