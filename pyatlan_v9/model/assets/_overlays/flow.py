# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        connection_qualified_name: str,
        folder_name: str,
        workflow_name: str,
        session_name: str,
        name: str | None = None,
    ) -> "Flow":
        """
        Create a new Flow asset for an orchestration unit (e.g. a PowerCenter session).

        The qualified name is
        ``{connection_qualified_name}/{folder_name}/{workflow_name}/{session_name}``,
        which is what atlan-powercenter-app's ``etl.jobRef`` resolves when a
        PowerCenter connection is configured for the repository.

        Args:
            connection_qualified_name: Unique name of the connection
            folder_name: Folder containing the workflow
            workflow_name: Workflow containing the session
            session_name: Session (orchestration unit) itself
            name: Name of the flow; defaults to
                ``{folder_name}/{workflow_name}/{session_name}``, which is what
                the app's ``etl.jobRef`` resolves by name when no connection is
                configured

        Returns:
            Flow instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            [
                "connection_qualified_name",
                "folder_name",
                "workflow_name",
                "session_name",
            ],
            [connection_qualified_name, folder_name, workflow_name, session_name],
        )
        fields = connection_qualified_name.split("/")
        if len(fields) != 3:
            raise ValueError("Invalid connection_qualified_name")
        if fields[0].replace(" ", "") == "" or fields[2].replace(" ", "") == "":
            raise ValueError("Invalid connection_qualified_name")
        if name is None:
            name = f"{folder_name}/{workflow_name}/{session_name}"
        validate_required_fields(["name"], [name])
        return cls(
            name=name,
            qualified_name=(
                f"{connection_qualified_name}/{folder_name}/"
                f"{workflow_name}/{session_name}"
            ),
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
            flow_folder_name=folder_name,
        )
