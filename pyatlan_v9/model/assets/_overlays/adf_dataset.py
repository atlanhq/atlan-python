# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        adf_factory_name: str,
        connection_qualified_name: str,
        adf_linkedservice_name: Union[str, None] = None,
    ) -> "AdfDataset":
        """Create a new AdfDataset asset."""
        validate_required_fields(
            ["name", "adf_factory_name", "connection_qualified_name"],
            [name, adf_factory_name, connection_qualified_name],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        factory_qn = f"{connection_qualified_name}/factory/{adf_factory_name}"
        return cls(
            name=name,
            qualified_name=f"{factory_qn}/datasets/{name}",
            adf_factory_name=adf_factory_name,
            adf_dataset_linked_service=adf_linkedservice_name
            if adf_linkedservice_name
            else UNSET,
            adf_linkedservice=RelatedAdfLinkedservice(
                unique_attributes={
                    "qualifiedName": f"{factory_qn}/linkedservices/{adf_linkedservice_name}"
                }
            )
            if adf_linkedservice_name
            else UNSET,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "AdfDataset":
        """Create an AdfDataset instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "AdfDataset":
        """Return only fields required for update operations."""
        return AdfDataset.updater(qualified_name=self.qualified_name, name=self.name)
