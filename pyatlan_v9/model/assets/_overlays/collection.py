# IMPORT: from pyatlan.errors import AtlanError
# IMPORT: from pyatlan.errors import ErrorCode
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(cls, *, client: "AtlanClient", name: str) -> "Collection":
        validate_required_fields(["client", "name"], [client, name])
        return cls(
            name=name,
            qualified_name=cls._generate_qualified_name(client),
        )

    @classmethod
    def _generate_qualified_name(cls, client: "AtlanClient") -> str:
        from pyatlan.errors import AtlanError

        try:
            username = client.user.get_current().username
            return f"default/collection/{username}/{uuid4()}"
        except AtlanError as e:
            raise ErrorCode.UNABLE_TO_GENERATE_QN.exception_with_parameters(
                cls.__name__, e
            ) from e
