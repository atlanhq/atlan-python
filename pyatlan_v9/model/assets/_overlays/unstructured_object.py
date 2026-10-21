# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        unstructured_container_qualified_name: str,
        unstructured_parent_folder_qualified_name: Union[str, None] = None,
        connection_qualified_name: Union[str, None] = None,
    ) -> "UnstructuredObject":
        """Create a new UnstructuredObject asset, at the container root or under a parent folder."""
        validate_required_fields(
            ["name", "unstructured_container_qualified_name"],
            [name, unstructured_container_qualified_name],
        )
        # A container qualifiedName is {connection_qn}/{container_name}.
        container_qn = unstructured_container_qualified_name
        if not connection_qualified_name:
            connection_qualified_name = "/".join(container_qn.split("/")[:3])
        if not container_qn.startswith(f"{connection_qualified_name}/"):
            raise ValueError("unstructured_container_qualified_name is invalid")
        container_name = container_qn[len(connection_qualified_name) + 1 :]
        if not container_name:
            raise ValueError("unstructured_container_qualified_name is invalid")
        parent_path = ""
        if unstructured_parent_folder_qualified_name:
            # A folder qualifiedName is {container_qn}/[{ancestor_path}/]{folder_name}.
            if not unstructured_parent_folder_qualified_name.startswith(
                f"{container_qn}/"
            ):
                raise ValueError("unstructured_parent_folder_qualified_name is invalid")
            parent_path = unstructured_parent_folder_qualified_name[
                len(container_qn) + 1 :
            ]
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        object_key = f"{parent_path}/{name}" if parent_path else name
        asset = cls(
            name=name,
            qualified_name=f"{container_qn}/{parent_path}/{name}"
            if parent_path
            else f"{container_qn}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            unstructured_container_name=container_name,
            unstructured_container_qualified_name=container_qn,
            unstructured_container=RelatedUnstructuredContainer(
                unique_attributes={"qualifiedName": container_qn}
            ),
            unstructured_object_key=object_key,
        )
        if parent_path:
            # Ancestor folders, nearest first, as atlan-bridge-app emits them.
            segments = parent_path.split("/")
            asset.unstructured_parent_folder_qualified_name = (
                unstructured_parent_folder_qualified_name
            )
            asset.unstructured_parent_folder = RelatedUnstructuredFolder(
                unique_attributes={
                    "qualifiedName": unstructured_parent_folder_qualified_name
                }
            )
            asset.unstructured_folder_hierarchy = [
                {
                    "qualifiedName": f"{container_qn}/{'/'.join(segments[:end])}",
                    "name": segments[end - 1],
                }
                for end in range(len(segments), 0, -1)
            ]
        return asset

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "UnstructuredObject":
        """Create an UnstructuredObject instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "UnstructuredObject":
        """Return only fields required for update operations."""
        return UnstructuredObject.updater(
            qualified_name=self.qualified_name, name=self.name
        )
