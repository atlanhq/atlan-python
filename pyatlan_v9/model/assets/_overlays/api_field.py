# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        parent_api_object_qualified_name: Union[str, None] = None,
        parent_api_query_qualified_name: Union[str, None] = None,
        connection_qualified_name: Union[str, None] = None,
        api_field_type: Union[str, None] = None,
        api_field_type_secondary: Union[str, None] = None,
        is_api_object_reference: bool = False,
        reference_api_object_qualified_name: Union[str, None] = None,
        api_query_param_type: Union[str, None] = None,
    ) -> "APIField":
        """Create a new APIField asset."""
        validate_required_fields(["name"], [name])
        if parent_api_object_qualified_name is None or (
            isinstance(parent_api_object_qualified_name, str)
            and not parent_api_object_qualified_name.strip()
        ):
            if parent_api_query_qualified_name is None or (
                isinstance(parent_api_query_qualified_name, str)
                and not parent_api_query_qualified_name.strip()
            ):
                raise ValueError(
                    "Either parent_api_object_qualified_name or parent_api_query_qualified_name requires a valid value"
                )
        elif (
            isinstance(parent_api_query_qualified_name, str)
            and parent_api_query_qualified_name.strip()
        ):
            raise ValueError(
                "Both parent_api_object_qualified_name and parent_api_query_qualified_name cannot be valid"
            )

        if is_api_object_reference:
            if not reference_api_object_qualified_name or (
                isinstance(reference_api_object_qualified_name, str)
                and not reference_api_object_qualified_name.strip()
            ):
                raise ValueError(
                    "Set valid qualified name for reference_api_object_qualified_name"
                )
        elif (
            reference_api_object_qualified_name
            and isinstance(reference_api_object_qualified_name, str)
            and reference_api_object_qualified_name.strip()
        ):
            raise ValueError(
                "Set is_api_object_reference to true to set reference_api_object_qualified_name"
            )

        if connection_qualified_name:
            connection_qn = connection_qualified_name
        elif parent_api_object_qualified_name:
            parts = parent_api_object_qualified_name.split("/")
            connection_qn = (
                "/".join(parts[:3])
                if len(parts) >= 3
                else parent_api_object_qualified_name
            )
        else:
            parts = (parent_api_query_qualified_name or "").split("/")
            connection_qn = (
                "/".join(parts[:3])
                if len(parts) >= 3
                else parent_api_query_qualified_name
            )

        conn_parts = (connection_qn or "").split("/")
        connector_name = conn_parts[1] if len(conn_parts) > 1 else None

        if parent_api_object_qualified_name:
            return cls(
                name=name,
                qualified_name=f"{parent_api_object_qualified_name}/{name}",
                connection_qualified_name=connection_qn,
                connector_name=connector_name,
                api_field_type=api_field_type,
                api_field_type_secondary=api_field_type_secondary,
                api_is_object_reference=is_api_object_reference,
                api_object_qualified_name=(
                    reference_api_object_qualified_name
                    if is_api_object_reference
                    else None
                ),
                api_object=RelatedAPIObject(
                    qualified_name=parent_api_object_qualified_name,
                    unique_attributes={
                        "qualifiedName": parent_api_object_qualified_name
                    },
                ),
                api_query_param_type=api_query_param_type,
            )
        return cls(
            name=name,
            qualified_name=f"{parent_api_query_qualified_name}/{name}",
            connection_qualified_name=connection_qn,
            connector_name=connector_name,
            api_field_type=api_field_type,
            api_field_type_secondary=api_field_type_secondary,
            api_is_object_reference=is_api_object_reference,
            api_object_qualified_name=(
                reference_api_object_qualified_name if is_api_object_reference else None
            ),
            api_query=RelatedAPIQuery(
                qualified_name=parent_api_query_qualified_name,
                unique_attributes={"qualifiedName": parent_api_query_qualified_name},
            ),
            api_query_param_type=api_query_param_type,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "APIField":
        """Create an APIField instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "APIField":
        """Return only fields required for update operations."""
        return APIField.updater(qualified_name=self.qualified_name, name=self.name)
