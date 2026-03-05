# IMPORT: from pyatlan.model.enums import AtlanConnectorType
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        client: AtlanClient,
        name: str,
        connector_type: AtlanConnectorType,
        admin_users: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
        admin_roles: Optional[List[str]] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
    ) -> "Connection":
        """
        Create a new Connection asset.

        Args:
            client: AtlanClient for cache validation
            name: Simple name of the connection
            connector_type: Type of connector for the connection
            admin_users: List of admin usernames
            admin_groups: List of admin group names
            admin_roles: List of admin role GUIDs
            host: Optional hostname for the connection
            port: Optional port number for the connection

        Returns:
            New Connection instance with all fields populated

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            ["client", "name", "connector_type"], [client, name, connector_type]
        )
        if not admin_users and not admin_groups and not admin_roles:
            raise ValueError(
                "One of admin_user, admin_groups or admin_roles is required"
            )
        client.user_cache.validate_names(names=admin_users or [])
        client.role_cache.validate_idstrs(idstrs=admin_roles or [])
        client.group_cache.validate_aliases(aliases=admin_groups or [])

        kwargs: dict = dict(
            name=name,
            qualified_name=connector_type.to_qualified_name(),
            connector_name=connector_type.value,
            category=connector_type.category.value,
            admin_users=set() if admin_users is None else set(admin_users),
            admin_groups=set() if admin_groups is None else set(admin_groups),
            admin_roles=set() if admin_roles is None else set(admin_roles),
        )
        if host is not None:
            kwargs["host"] = host
        if port is not None:
            kwargs["port"] = port
        return cls(**kwargs)

    @classmethod
    @init_guid
    async def creator_async(
        cls,
        *,
        client: Any,
        name: str,
        connector_type: AtlanConnectorType,
        admin_users: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
        admin_roles: Optional[List[str]] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
    ) -> "Connection":
        """
        Async version of creator() for creating a new Connection asset.

        :param client: async Atlan client for cache validation
        :param name: name for the connection
        :param connector_type: type of connector
        :param admin_users: list of admin usernames
        :param admin_groups: list of admin group names
        :param admin_roles: list of admin role GUIDs
        :param host: optional hostname
        :param port: optional port number
        :returns: the new connection object
        :raises ValueError: if required parameters are missing or invalid
        """
        validate_required_fields(
            ["client", "name", "connector_type"], [client, name, connector_type]
        )
        if not admin_users and not admin_groups and not admin_roles:
            raise ValueError(
                "One of admin_user, admin_groups or admin_roles is required"
            )
        await client.user_cache.validate_names(names=admin_users or [])
        await client.role_cache.validate_idstrs(idstrs=admin_roles or [])
        await client.group_cache.validate_aliases(aliases=admin_groups or [])

        kwargs: dict = dict(
            name=name,
            qualified_name=connector_type.to_qualified_name(),
            connector_name=connector_type.value,
            category=connector_type.category.value,
            admin_users=set() if admin_users is None else set(admin_users),
            admin_groups=set() if admin_groups is None else set(admin_groups),
            admin_roles=set() if admin_roles is None else set(admin_roles),
        )
        if host is not None:
            kwargs["host"] = host
        if port is not None:
            kwargs["port"] = port
        return cls(**kwargs)

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "Connection":
        """
        Create a Connection instance for updating an existing asset.

        Args:
            qualified_name: Unique name of the connection to update
            name: Simple name of the connection

        Returns:
            Connection instance configured for updates

        Raises:
            ValueError: If required parameters are missing
        """
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "Connection":
        """
        Return a Connection with only required fields for reference.

        Returns:
            Connection instance with only qualified_name and name set
        """
        return Connection(qualified_name=self.qualified_name, name=self.name)

    @classmethod
    def create(cls, **kwargs) -> "Connection":
        """Backward compatibility alias for creator()."""
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "Connection":
        """Backward compatibility alias for updater()."""
        return cls.updater(**kwargs)
