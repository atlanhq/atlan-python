# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    # atlan-sapdatasphere-app's norm(): every char outside [A-Za-z0-9_] becomes "_".
    # Applied only to qualifiedName segments; name and space name keep raw values.
    _QN_UNSAFE: ClassVar[re.Pattern] = re.compile(r"[^A-Za-z0-9_]")

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        space_name: str,
        connection_qualified_name: str,
        space_qualified_name: Union[str, None] = None,
    ) -> "SapDatasphereReplicationFlow":
        """
        Create a new SapDatasphereReplicationFlow asset.

        :param name: name of the replication flow, as it appears in Datasphere
        :param space_name: name of the Datasphere space the flow runs in
        :param connection_qualified_name: unique name of the SAP Datasphere connection
        :param space_qualified_name: unique name of the space's SQL Schema; derived
            as ``{connection_qualified_name}/DEFAULT/{space}`` when not given
        :returns: the minimal object needed to create the replication flow
        """
        validate_required_fields(
            ["name", "space_name", "connection_qualified_name"],
            [name, space_name, connection_qualified_name],
        )
        safe_space = cls._QN_UNSAFE.sub("_", space_name)
        safe_name = cls._QN_UNSAFE.sub("_", name)
        if not space_qualified_name:
            space_qualified_name = f"{connection_qualified_name}/DEFAULT/{safe_space}"
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/flow/{safe_space}/{safe_name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            sap_datasphere_replication_flow_space_name=space_name,
            sap_datasphere_replication_flow_space_qualified_name=space_qualified_name,
            sap_datasphere_schema=RelatedSchema(
                unique_attributes={"qualifiedName": space_qualified_name}
            ),
        )

    @classmethod
    def updater(
        cls, *, qualified_name: str, name: str
    ) -> "SapDatasphereReplicationFlow":
        """Create a SapDatasphereReplicationFlow instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SapDatasphereReplicationFlow":
        """Return only fields required for update operations."""
        return SapDatasphereReplicationFlow.updater(
            qualified_name=self.qualified_name, name=self.name
        )
