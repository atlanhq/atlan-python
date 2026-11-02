# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        version: str,
        model_group_qualified_name: str,
        name: Union[str, None] = None,
        connection_qualified_name: Union[str, None] = None,
    ) -> "SageMakerModel":
        """Create a new SageMakerModel (a versioned model package) asset."""
        validate_required_fields(
            ["version", "model_group_qualified_name"],
            [version, model_group_qualified_name],
        )
        # A model group qualifiedName is {connection_qn}/{aws_region}/{group_name}.
        parts = model_group_qualified_name.split("/")
        if len(parts) < 5:
            raise ValueError("model_group_qualified_name is invalid")
        model_group_name = parts[-1]
        aws_region = parts[-2]
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:-2])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name or f"{model_group_name}/{version}",
            qualified_name=f"{model_group_qualified_name}/{version}",
            sage_maker_model_version=version,
            sage_maker_model_model_group_name=model_group_name,
            sage_maker_model_model_group_qualified_name=model_group_qualified_name,
            aws_region=aws_region,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            sage_maker_model_group=RelatedSageMakerModelGroup(
                unique_attributes={"qualifiedName": model_group_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SageMakerModel":
        """Create a SageMakerModel instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SageMakerModel":
        """Return only fields required for update operations."""
        return SageMakerModel.updater(qualified_name=self.qualified_name, name=self.name)
