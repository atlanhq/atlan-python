# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        quick_sight_id: str,
        quick_sight_analysis_visual_qualified_name: str,
        quick_sight_analysis_qualified_name: Union[str, None] = None,
        quick_sight_analysis_field_expression: Union[str, None] = None,
        quick_sight_analysis_field_data_set_identifier: Union[str, None] = None,
        connection_qualified_name: Union[str, None] = None,
    ) -> "QuickSightAnalysisField":
        """Create a new QuickSightAnalysisField asset."""
        validate_required_fields(
            ["name", "quick_sight_id", "quick_sight_analysis_visual_qualified_name"],
            [name, quick_sight_id, quick_sight_analysis_visual_qualified_name],
        )
        # A visual qualifiedName is {connection_qn}/{analysis_id}/{sheet_id}/{visual_id}.
        parts = quick_sight_analysis_visual_qualified_name.split("/")
        if len(parts) < 6:
            raise ValueError("quick_sight_analysis_visual_qualified_name is invalid")
        if not quick_sight_analysis_qualified_name:
            quick_sight_analysis_qualified_name = "/".join(parts[:-2])
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:3])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            quick_sight_id=quick_sight_id,
            qualified_name=f"{quick_sight_analysis_visual_qualified_name}/{quick_sight_id}",
            quick_sight_analysis_visual_qualified_name=quick_sight_analysis_visual_qualified_name,
            quick_sight_analysis_qualified_name=quick_sight_analysis_qualified_name,
            quick_sight_analysis_field_expression=quick_sight_analysis_field_expression
            if quick_sight_analysis_field_expression is not None
            else UNSET,
            quick_sight_analysis_field_data_set_identifier=quick_sight_analysis_field_data_set_identifier
            if quick_sight_analysis_field_data_set_identifier is not None
            else UNSET,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            quick_sight_analysis_visual=RelatedQuickSightAnalysisVisual(
                unique_attributes={
                    "qualifiedName": quick_sight_analysis_visual_qualified_name
                }
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "QuickSightAnalysisField":
        """Create a QuickSightAnalysisField instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "QuickSightAnalysisField":
        """Return only fields required for update operations."""
        return QuickSightAnalysisField.updater(
            qualified_name=self.qualified_name, name=self.name
        )
