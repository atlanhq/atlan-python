# IMPORT: from pyatlan.model.enums import AtlanConnectorType
# IMPORT: from pyatlan.utils import validate_required_fields
# INTERNAL_IMPORT: from pyatlan.model.assets import Collection
# INTERNAL_IMPORT: from pyatlan.model.assets import Folder

    @classmethod
    def creator(
        cls,
        *,
        name: str,
        collection_qualified_name: str | None = None,
        parent_folder_qualified_name: str | None = None,
    ) -> "Query":
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
            from pyatlan_v9.model.assets import Folder

            parent_ref = Folder.ref_by_qualified_name(parent_folder_qualified_name)

        return Query(
            name=name,
            qualified_name=qualified_name,
            collection_qualified_name=collection_qualified_name,
            parent=parent_ref,
            parent_qualified_name=parent_qn,
        )

    @classmethod
    def updater(
        cls,
        *,
        name: str,
        qualified_name: str,
        collection_qualified_name: str,
        parent_qualified_name: str,
    ) -> "Query":
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["name", "collection_qualified_name", "parent_qualified_name"],
            [name, collection_qualified_name, parent_qualified_name],
        )
        if collection_qualified_name == parent_qualified_name:
            from pyatlan_v9.model.assets import Collection

            parent = Collection.ref_by_qualified_name(collection_qualified_name)
        else:
            from pyatlan_v9.model.assets import Folder

            parent = Folder.ref_by_qualified_name(parent_qualified_name)

        return Query(
            qualified_name=qualified_name,
            name=name,
            parent=parent,
            collection_qualified_name=collection_qualified_name,
            parent_qualified_name=parent_qualified_name,
        )

    def with_raw_query(self, schema_qualified_name: str, query: str):
        from base64 import b64encode
        from json import dumps

        from pyatlan.model.enums import AtlanConnectorType

        _DEFAULT_VARIABLE_SCHEMA = dumps(
            {
                "customvariablesDateTimeFormat": {
                    "defaultDateFormat": "YYYY-MM-DD",
                    "defaultTimeFormat": "HH:mm",
                },
                "customVariables": [],
            }
        )
        connection_qn, connector_name = AtlanConnectorType.get_connector_name(
            schema_qualified_name, "schema_qualified_name", 5
        )
        tokens = schema_qualified_name.split("/")
        database_qn = f"{tokens[0]}/{tokens[1]}/{tokens[2]}/{tokens[3]}"
        self.connection_name = connector_name
        self.connection_qualified_name = connection_qn
        self.default_database_qualified_name = database_qn
        self.default_schema_qualified_name = schema_qualified_name
        self.is_visual_query = False
        self.raw_query_text = query
        self.variables_schema_base64 = b64encode(
            _DEFAULT_VARIABLE_SCHEMA.encode("utf-8")
        ).decode("utf-8")
