# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        ssrs_report_qualified_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "SSRSDataSet":
        """Create a new SSRSDataSet asset within a report."""
        validate_required_fields(
            ["name", "ssrs_report_qualified_name"], [name, ssrs_report_qualified_name]
        )
        # A report qualifiedName is {connection_qn}[/{folder}...]/{report}.
        parts = ssrs_report_qualified_name.split("/")
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:3])
        connection_depth = len(connection_qualified_name.split("/"))
        if len(parts) <= connection_depth or not ssrs_report_qualified_name.startswith(
            f"{connection_qualified_name}/"
        ):
            raise ValueError("ssrs_report_qualified_name is invalid")
        folder_parts = parts[:-1]
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        # atlan-ssrs-app strips spaces from each qualifiedName segment.
        return cls(
            name=name,
            qualified_name=f"{ssrs_report_qualified_name}/{name.replace(' ', '')}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            ssrs_report_qualified_name=ssrs_report_qualified_name,
            ssrs_report_name=parts[-1],
            ssrs_parent_folder_qualified_name="/".join(folder_parts)
            if len(folder_parts) > connection_depth
            else UNSET,
            ssrs_report=RelatedSSRSReport(
                unique_attributes={"qualifiedName": ssrs_report_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SSRSDataSet":
        """Create an SSRSDataSet instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SSRSDataSet":
        """Return only fields required for update operations."""
        return SSRSDataSet.updater(qualified_name=self.qualified_name, name=self.name)
