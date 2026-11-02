# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        feature_group_qualified_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "SageMakerFeature":
        """Create a new SageMakerFeature asset."""
        validate_required_fields(
            ["name", "feature_group_qualified_name"],
            [name, feature_group_qualified_name],
        )
        # A feature group qualifiedName is {connection_qn}/{aws_region}/{group_name}.
        parts = feature_group_qualified_name.split("/")
        if len(parts) < 5:
            raise ValueError("feature_group_qualified_name is invalid")
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:-2])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{feature_group_qualified_name}/{name}",
            sage_maker_feature_group_name=parts[-1],
            sage_maker_feature_group_qualified_name=feature_group_qualified_name,
            aws_region=parts[-2],
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            sage_maker_feature_group=RelatedSageMakerFeatureGroup(
                unique_attributes={"qualifiedName": feature_group_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SageMakerFeature":
        """Create a SageMakerFeature instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SageMakerFeature":
        """Return only fields required for update operations."""
        return SageMakerFeature.updater(
            qualified_name=self.qualified_name, name=self.name
        )
