# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        matillion_component_id: str,
        matillion_job_qualified_name: str,
        matillion_job_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "MatillionComponent":
        """Create a new MatillionComponent asset."""
        validate_required_fields(
            [
                "name",
                "matillion_component_id",
                "matillion_job_qualified_name",
                "matillion_job_name",
            ],
            [
                name,
                matillion_component_id,
                matillion_job_qualified_name,
                matillion_job_name,
            ],
        )
        # A job qualifiedName is {connection_qn}/job/{job_id}.
        parts = matillion_job_qualified_name.split("/")
        if len(parts) < 5:
            raise ValueError("matillion_job_qualified_name is invalid")
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:3])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        # Components are keyed flat under the connection, not under their job.
        return cls(
            name=name,
            matillion_component_id=matillion_component_id,
            qualified_name=f"{connection_qualified_name}/component/{matillion_component_id}",
            matillion_job_qualified_name=matillion_job_qualified_name,
            matillion_job_name=matillion_job_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            matillion_job=RelatedMatillionJob(
                unique_attributes={"qualifiedName": matillion_job_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "MatillionComponent":
        """Create a MatillionComponent instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "MatillionComponent":
        """Return only fields required for update operations."""
        return MatillionComponent.updater(
            qualified_name=self.qualified_name, name=self.name
        )
