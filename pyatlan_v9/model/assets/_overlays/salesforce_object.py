# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        api_name: str,
        organization_qualified_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "SalesforceObject":
        validate_required_fields(
            ["name", "api_name", "organization_qualified_name"],
            [name, api_name, organization_qualified_name],
        )
        fields = organization_qualified_name.split("/")
        if len(fields) < 4:
            raise ValueError("organization_qualified_name is invalid")
        if not connection_qualified_name:
            connection_qualified_name = "/".join(fields[:3])
        return cls(
            name=name,
            qualified_name=f"{organization_qualified_name}/{api_name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
            api_name=api_name,
            organization_qualified_name=organization_qualified_name,
            organization=RelatedSalesforceOrganization(
                qualified_name=organization_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "SalesforceObject":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "SalesforceObject":
        return cls.updater(**kwargs)
