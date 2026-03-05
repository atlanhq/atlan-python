# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        quick_sight_id: str,
        quick_sight_sheet_id: str,
        quick_sight_sheet_name: str,
        quick_sight_analysis_qualified_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "QuickSightAnalysisVisual":
        validate_required_fields(
            [
                "name",
                "quick_sight_id",
                "quick_sight_sheet_id",
                "quick_sight_sheet_name",
                "quick_sight_analysis_qualified_name",
            ],
            [
                name,
                quick_sight_id,
                quick_sight_sheet_id,
                quick_sight_sheet_name,
                quick_sight_analysis_qualified_name,
            ],
        )
        if connection_qualified_name:
            fields = connection_qualified_name.split("/")
            connector_name = fields[1] if len(fields) > 1 else None
        else:
            parts = quick_sight_analysis_qualified_name.split("/")
            connector_name = parts[1] if len(parts) > 1 else None
            connection_qualified_name = (
                "/".join(parts[:3])
                if len(parts) >= 3
                else quick_sight_analysis_qualified_name
            )
        qualified_name = f"{quick_sight_analysis_qualified_name}/{quick_sight_sheet_id}/{quick_sight_id}"
        return cls(
            name=name,
            quick_sight_id=quick_sight_id,
            quick_sight_sheet_id=quick_sight_sheet_id,
            quick_sight_sheet_name=quick_sight_sheet_name,
            quick_sight_analysis_qualified_name=quick_sight_analysis_qualified_name,
            qualified_name=qualified_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "QuickSightAnalysisVisual":
        """Create a QuickSightAnalysisVisual instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "QuickSightAnalysisVisual":
        """Return only fields required for update operations."""
        return QuickSightAnalysisVisual.updater(
            qualified_name=self.qualified_name, name=self.name
        )
