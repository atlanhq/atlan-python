# IMPORT: from pyatlan.utils import validate_required_fields
# INTERNAL_IMPORT: from pyatlan.model.assets import Collection

    @classmethod
    def creator(
        cls,
        *,
        name: str,
        collection_qualified_name: str | None = None,
        parent_folder_qualified_name: str | None = None,
    ) -> "Folder":
        from pyatlan.utils import validate_required_fields

        validate_required_fields(["name"], [name])
        if not (parent_folder_qualified_name or collection_qualified_name):
            raise ValueError(
                "Either 'collection_qualified_name' or 'parent_folder_qualified_name' must be specified."
            )

        if not parent_folder_qualified_name:
            qualified_name = f"{collection_qualified_name}/{name}"
            parent_qn = collection_qualified_name
            from pyatlan_v9.model.assets import Collection

            parent_ref = Collection.ref_by_qualified_name(
                collection_qualified_name or ""
            )
        else:
            tokens = parent_folder_qualified_name.split("/")
            if len(tokens) < 4:
                raise ValueError("Invalid parent_folder_qualified_name")
            collection_qualified_name = (
                f"{tokens[0]}/{tokens[1]}/{tokens[2]}/{tokens[3]}"
            )
            qualified_name = f"{parent_folder_qualified_name}/{name}"
            parent_qn = parent_folder_qualified_name
            parent_ref = Folder.ref_by_qualified_name(parent_folder_qualified_name)

        return Folder(
            name=name,
            qualified_name=qualified_name,
            collection_qualified_name=collection_qualified_name,
            parent=parent_ref,
            parent_qualified_name=parent_qn,
        )
