# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def _create(cls, *, name: str) -> "AuthPolicy":
        validate_required_fields(["name"], [name])
        return cls(qualified_name=name, name=name, display_name="")
