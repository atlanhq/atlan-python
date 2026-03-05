# STDLIB_IMPORT: import re
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    def _get_super_domain_qualified_name(
        cls, domain_qualified_name: str
    ) -> Union[str, None]:
        """Extract the top-most ancestor domain qualified name."""
        domain_qn_prefix = re.compile(r"(default/domain/[a-zA-Z0-9-]+/super)/.*")
        if domain_qualified_name:
            match = domain_qn_prefix.match(domain_qualified_name)
            if match and match.group(1):
                return match.group(1)
            if domain_qualified_name.startswith("default/domain/"):
                return domain_qualified_name
        return None

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        parent_domain_qualified_name: Union[str, None] = None,
    ) -> "DataDomain":
        """Create a new DataDomain asset."""
        validate_required_fields(["name"], [name])
        parent_domain = (
            RelatedDataDomain(
                unique_attributes={"qualifiedName": parent_domain_qualified_name}
            )
            if parent_domain_qualified_name
            else None
        )
        super_domain_qualified_name = (
            cls._get_super_domain_qualified_name(parent_domain_qualified_name)
            if parent_domain_qualified_name
            else None
        )
        return cls(
            name=name,
            qualified_name=name,
            parent_domain=parent_domain,
            parent_domain_qualified_name=parent_domain_qualified_name,
            super_domain_qualified_name=super_domain_qualified_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "DataDomain":
        """Create a DataDomain instance for update operations."""
        validate_required_fields(["name", "qualified_name"], [name, qualified_name])
        fields = qualified_name.split("/")
        if len(fields) < 3:
            raise ValueError(f"Invalid data domain qualified_name: {qualified_name}")
        return cls(
            qualified_name=qualified_name,
            name=name,
            parent_domain_qualified_name=None,
        )

    def trim_to_required(self) -> "DataDomain":
        """Return only the required fields for updates."""
        return DataDomain.updater(qualified_name=self.qualified_name, name=self.name)
