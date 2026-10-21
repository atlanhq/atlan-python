# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        api_name: str,
        object_qualified_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "SalesforceField":
        validate_required_fields(
            ["name", "api_name", "object_qualified_name"],
            [name, api_name, object_qualified_name],
        )
        fields = object_qualified_name.split("/")
        if len(fields) < 5:
            raise ValueError("object_qualified_name is invalid")
        if not connection_qualified_name:
            connection_qualified_name = "/".join(fields[:3])
        return cls(
            name=name,
            qualified_name=f"{object_qualified_name}/{api_name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
            api_name=api_name,
            object_qualified_name=object_qualified_name,
            organization_qualified_name="/".join(fields[:-1]),
            object=RelatedSalesforceObject(qualified_name=object_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "SalesforceField":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "SalesforceField":
        return cls.updater(**kwargs)
