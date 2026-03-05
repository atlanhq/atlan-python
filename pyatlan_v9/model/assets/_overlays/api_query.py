# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        api_input_field_count: Union[int, None] = None,
        api_query_output_type: Union[str, None] = None,
        api_query_output_type_secondary: Union[str, None] = None,
        is_object_reference: bool = False,
        reference_api_object_qualified_name: Union[str, None] = None,
    ) -> "APIQuery":
        """Create a new APIQuery asset."""
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        if is_object_reference:
            if not reference_api_object_qualified_name or (
                isinstance(reference_api_object_qualified_name, str)
                and not reference_api_object_qualified_name.strip()
            ):
                raise ValueError(
                    "Set valid qualified name for reference_api_object_qualified_name when is_object_reference is true"
                )
        elif (
            reference_api_object_qualified_name
            and isinstance(reference_api_object_qualified_name, str)
            and reference_api_object_qualified_name.strip()
        ):
            raise ValueError(
                "Set is_object_reference to true to set reference_api_object_qualified_name"
            )

        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            api_input_field_count=api_input_field_count,
            api_query_output_type=api_query_output_type,
            api_query_output_type_secondary=api_query_output_type_secondary,
            api_is_object_reference=is_object_reference,
            api_object_qualified_name=(
                reference_api_object_qualified_name if is_object_reference else None
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "APIQuery":
        """Create an APIQuery instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "APIQuery":
        """Return only fields required for update operations."""
        return APIQuery.updater(qualified_name=self.qualified_name, name=self.name)
