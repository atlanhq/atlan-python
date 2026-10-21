# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        aws_region: str,
        connection_qualified_name: str,
    ) -> "SageMakerModelDeployment":
        """Create a new SageMakerModelDeployment asset."""
        validate_required_fields(
            ["name", "aws_region", "connection_qualified_name"],
            [name, aws_region, connection_qualified_name],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/{aws_region}/{name}",
            aws_region=aws_region,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SageMakerModelDeployment":
        """Create a SageMakerModelDeployment instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SageMakerModelDeployment":
        """Return only fields required for update operations."""
        return SageMakerModelDeployment.updater(qualified_name=self.qualified_name, name=self.name)
