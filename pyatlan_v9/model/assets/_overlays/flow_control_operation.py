# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        source_id: str,
        scope: str | None = None,
        parent_qualified_name: str | None = None,
        flow_id: str | None = None,
    ) -> "FlowControlOperation":
        """
        Create a new FlowControlOperation asset.

        Exactly one of ``scope`` or ``parent_qualified_name`` must be given:

        - top-level operation: ``{connection_qualified_name}/{scope}/{source_id}``
          (e.g. scope = Fabric workspace ID, or SageMaker region)
        - child operation: ``{parent_qualified_name}/jobs/{source_id}``, linked to
          its parent through ``flow_controlled_by``

        Args:
            name: Name of the operation
            connection_qualified_name: Unique name of the connection
            source_id: Identifier of the operation in the source system; the last
                segment of the qualified name
            scope: Source-system container of a top-level operation
            parent_qualified_name: Unique name of the controlling operation
            flow_id: Value for ``flow_id`` (e.g. an ARN); not part of the
                qualified name

        Returns:
            FlowControlOperation instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            ["name", "connection_qualified_name", "source_id"],
            [name, connection_qualified_name, source_id],
        )
        fields = connection_qualified_name.split("/")
        if len(fields) != 3:
            raise ValueError("Invalid connection_qualified_name")
        if fields[0].replace(" ", "") == "" or fields[2].replace(" ", "") == "":
            raise ValueError("Invalid connection_qualified_name")
        if (scope is None) == (parent_qualified_name is None):
            raise ValueError(
                "Exactly one of scope or parent_qualified_name must be provided"
            )

        flow_controlled_by: RelatedFlowControlOperation | UnsetType = UNSET
        if parent_qualified_name is not None:
            validate_required_fields(["parent_qualified_name"], [parent_qualified_name])
            if not parent_qualified_name.startswith(f"{connection_qualified_name}/"):
                raise ValueError(
                    "parent_qualified_name must belong to connection_qualified_name"
                )
            qualified_name = f"{parent_qualified_name}/jobs/{source_id}"
            flow_controlled_by = RelatedFlowControlOperation(
                qualified_name=parent_qualified_name
            )
        else:
            validate_required_fields(["scope"], [scope])
            qualified_name = f"{connection_qualified_name}/{scope}/{source_id}"

        return cls(
            name=name,
            qualified_name=qualified_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
            flow_id=flow_id if flow_id is not None else UNSET,
            flow_controlled_by=flow_controlled_by,
        )
