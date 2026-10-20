# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        cosmos_mongo_db_account_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "CosmosMongoDBDatabase":
        validate_required_fields(
            ["name", "cosmos_mongo_db_account_qualified_name"],
            [name, cosmos_mongo_db_account_qualified_name],
        )
        if not connection_qualified_name:
            fields = cosmos_mongo_db_account_qualified_name.split("/")
            if len(fields) < 5:
                raise ValueError("cosmos_mongo_db_account_qualified_name is invalid")
            connection_qualified_name = "/".join(fields[:3])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{cosmos_mongo_db_account_qualified_name}/databases/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            cosmos_mongo_db_account_qualified_name=cosmos_mongo_db_account_qualified_name,
            cosmos_mongo_db_account=RelatedCosmosMongoDBAccount(
                unique_attributes={
                    "qualifiedName": cosmos_mongo_db_account_qualified_name
                }
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "CosmosMongoDBDatabase":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "CosmosMongoDBDatabase":
        return cls.updater(**kwargs)
