# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @property
    def api_path_raw_u_r_i(self) -> Union[str, None, UnsetType]:
        return self.api_path_raw_uri

    @api_path_raw_u_r_i.setter
    def api_path_raw_u_r_i(self, value: Union[str, None, UnsetType]) -> None:
        self.api_path_raw_uri = value

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        path_raw_uri: str,
        spec_qualified_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "APIPath":
        """Create a new APIPath asset."""
        validate_required_fields(
            ["path_raw_uri", "spec_qualified_name"], [path_raw_uri, spec_qualified_name]
        )
        if connection_qualified_name:
            connection_qn = connection_qualified_name
        else:
            spec_parts = spec_qualified_name.split("/")
            connection_qn = (
                "/".join(spec_parts[:3])
                if len(spec_parts) >= 3
                else spec_qualified_name
            )
        conn_parts = connection_qn.split("/")
        connector_name = conn_parts[1] if len(conn_parts) > 1 else None
        return cls(
            name=path_raw_uri,
            qualified_name=f"{spec_qualified_name}{path_raw_uri}",
            api_path_raw_uri=path_raw_uri,
            api_spec_qualified_name=spec_qualified_name,
            connection_qualified_name=connection_qn,
            connector_name=connector_name,
            api_spec=RelatedAPISpec(
                unique_attributes={"qualifiedName": spec_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "APIPath":
        """Create an APIPath instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "APIPath":
        """Return only fields required for update operations."""
        return APIPath.updater(qualified_name=self.qualified_name, name=self.name)
