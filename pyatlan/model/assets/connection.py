# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Set
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType, QueryUsernameStrategy
from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, NumericField
from pyatlan.utils import init_guid, validate_required_fields

from .asset import Asset


class Connection(Asset, type_name="Connection"):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connector_type: AtlanConnectorType,
        admin_users: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
        admin_roles: Optional[List[str]] = None,
    ) -> Connection:
        validate_required_fields(["name", "connector_type"], [name, connector_type])
        if not admin_users and not admin_groups and not admin_roles:
            raise ValueError(
                "One of admin_user, admin_groups or admin_roles is required"
            )
        attr = cls.Attributes(
            name=name,
            qualified_name=connector_type.to_qualified_name(),
            connector_name=connector_type.value,
            category=connector_type.category.value,
        )
        attr.admin_users = set() if admin_users is None else set(admin_users)
        attr.admin_groups = set() if admin_groups is None else set(admin_groups)
        attr.admin_roles = set() if admin_roles is None else set(admin_roles)
        return cls(attributes=attr)

    @classmethod
    @init_guid
    def create(
        cls,
        *,
        name: str,
        connector_type: AtlanConnectorType,
        admin_users: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
        admin_roles: Optional[List[str]] = None,
    ) -> Connection:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name,
            connector_type=connector_type,
            admin_users=admin_users,
            admin_groups=admin_groups,
            admin_roles=admin_roles,
        )

    type_name: str = Field(default="Connection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Connection":
            raise ValueError("must be Connection")
        return v

    def __setattr__(self, name, value):
        if name in Connection._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CATEGORY: ClassVar[KeywordField] = KeywordField("category", "category")
    """
    Type of connection, for example WAREHOUSE, RDBMS, etc.
    """
    SUB_CATEGORY: ClassVar[KeywordField] = KeywordField("subCategory", "subCategory")
    """
    Subcategory of this connection.
    """
    HOST: ClassVar[KeywordField] = KeywordField("host", "host")
    """
    Host name of this connection's source.
    """
    PORT: ClassVar[NumericField] = NumericField("port", "port")
    """
    Port number to this connection's source.
    """
    ALLOW_QUERY: ClassVar[BooleanField] = BooleanField("allowQuery", "allowQuery")
    """
    Whether using this connection to run queries on the source is allowed (true) or not (false).
    """
    ALLOW_QUERY_PREVIEW: ClassVar[BooleanField] = BooleanField(
        "allowQueryPreview", "allowQueryPreview"
    )
    """
    Whether using this connection to run preview queries on the source is allowed (true) or not (false).
    """
    QUERY_PREVIEW_CONFIG: ClassVar[KeywordField] = KeywordField(
        "queryPreviewConfig", "queryPreviewConfig"
    )
    """
    Configuration for preview queries.
    """
    QUERY_CONFIG: ClassVar[KeywordField] = KeywordField("queryConfig", "queryConfig")
    """
    Query config for this connection.
    """
    CREDENTIAL_STRATEGY: ClassVar[KeywordField] = KeywordField(
        "credentialStrategy", "credentialStrategy"
    )
    """
    Credential strategy to use for this connection for queries.
    """
    PREVIEW_CREDENTIAL_STRATEGY: ClassVar[KeywordField] = KeywordField(
        "previewCredentialStrategy", "previewCredentialStrategy"
    )
    """
    Credential strategy to use for this connection for preview queries.
    """
    POLICY_STRATEGY: ClassVar[KeywordField] = KeywordField(
        "policyStrategy", "policyStrategy"
    )
    """
    Policy strategy is a configuration that determines whether the Atlan policy will be applied to the results of insight queries and whether the query will be rewritten, applicable for stream api call made from insight screen
    """  # noqa: E501
    POLICY_STRATEGY_FOR_SAMPLE_PREVIEW: ClassVar[KeywordField] = KeywordField(
        "policyStrategyForSamplePreview", "policyStrategyForSamplePreview"
    )
    """
    Policy strategy is a configuration that determines whether the Atlan policy will be applied to the results of insight queries and whether the query will be rewritten. policyStrategyForSamplePreview config is applicable for sample preview call from assets screen
    """  # noqa: E501
    QUERY_USERNAME_STRATEGY: ClassVar[KeywordField] = KeywordField(
        "queryUsernameStrategy", "queryUsernameStrategy"
    )
    """
    Username strategy to use for this connection for queries.
    """
    ROW_LIMIT: ClassVar[NumericField] = NumericField("rowLimit", "rowLimit")
    """
    Maximum number of rows that can be returned for the source.
    """
    QUERY_TIMEOUT: ClassVar[NumericField] = NumericField("queryTimeout", "queryTimeout")
    """
    Maximum time a query should be allowed to run before timing out.
    """
    DEFAULT_CREDENTIAL_GUID: ClassVar[KeywordField] = KeywordField(
        "defaultCredentialGuid", "defaultCredentialGuid"
    )
    """
    Unique identifier (GUID) for the default credentials to use for this connection.
    """
    CONNECTOR_ICON: ClassVar[KeywordField] = KeywordField(
        "connectorIcon", "connectorIcon"
    )
    """
    Unused. Only the value of connectorType impacts icons.
    """
    CONNECTOR_IMAGE: ClassVar[KeywordField] = KeywordField(
        "connectorImage", "connectorImage"
    )
    """
    Unused. Only the value of connectorType impacts icons.
    """
    SOURCE_LOGO: ClassVar[KeywordField] = KeywordField("sourceLogo", "sourceLogo")
    """
    Unused. Only the value of connectorType impacts icons.
    """
    IS_SAMPLE_DATA_PREVIEW_ENABLED: ClassVar[BooleanField] = BooleanField(
        "isSampleDataPreviewEnabled", "isSampleDataPreviewEnabled"
    )
    """
    Whether sample data can be previewed for this connection (true) or not (false).
    """
    POPULARITY_INSIGHTS_TIMEFRAME: ClassVar[NumericField] = NumericField(
        "popularityInsightsTimeframe", "popularityInsightsTimeframe"
    )
    """
    Number of days over which popularity is calculated, for example 30 days.
    """
    HAS_POPULARITY_INSIGHTS: ClassVar[BooleanField] = BooleanField(
        "hasPopularityInsights", "hasPopularityInsights"
    )
    """
    Whether this connection has popularity insights (true) or not (false).
    """
    CONNECTION_DBT_ENVIRONMENTS: ClassVar[KeywordField] = KeywordField(
        "connectionDbtEnvironments", "connectionDbtEnvironments"
    )
    """

    """
    CONNECTION_SSO_CREDENTIAL_GUID: ClassVar[KeywordField] = KeywordField(
        "connectionSSOCredentialGuid", "connectionSSOCredentialGuid"
    )
    """
    Unique identifier (GUID) for the SSO credentials to use for this connection.
    """
    USE_OBJECT_STORAGE: ClassVar[BooleanField] = BooleanField(
        "useObjectStorage", "useObjectStorage"
    )
    """
    Whether to upload to S3, GCP, or another storage location (true) or not (false).
    """
    OBJECT_STORAGE_UPLOAD_THRESHOLD: ClassVar[NumericField] = NumericField(
        "objectStorageUploadThreshold", "objectStorageUploadThreshold"
    )
    """
    Number of rows after which results should be uploaded to storage.
    """
    VECTOR_EMBEDDINGS_ENABLED: ClassVar[BooleanField] = BooleanField(
        "vectorEmbeddingsEnabled", "vectorEmbeddingsEnabled"
    )
    """

    """
    VECTOR_EMBEDDINGS_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "vectorEmbeddingsUpdatedAt", "vectorEmbeddingsUpdatedAt"
    )
    """

    """

    _convenience_properties: ClassVar[List[str]] = [
        "category",
        "sub_category",
        "host",
        "port",
        "allow_query",
        "allow_query_preview",
        "query_preview_config",
        "query_config",
        "credential_strategy",
        "preview_credential_strategy",
        "policy_strategy",
        "policy_strategy_for_sample_preview",
        "query_username_strategy",
        "row_limit",
        "query_timeout",
        "default_credential_guid",
        "connector_icon",
        "connector_image",
        "source_logo",
        "is_sample_data_preview_enabled",
        "popularity_insights_timeframe",
        "has_popularity_insights",
        "connection_dbt_environments",
        "connection_s_s_o_credential_guid",
        "use_object_storage",
        "object_storage_upload_threshold",
        "vector_embeddings_enabled",
        "vector_embeddings_updated_at",
    ]

    @property
    def category(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.category

    @category.setter
    def category(self, category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.category = category

    @property
    def sub_category(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sub_category

    @sub_category.setter
    def sub_category(self, sub_category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sub_category = sub_category

    @property
    def host(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.host

    @host.setter
    def host(self, host: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.host = host

    @property
    def port(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.port

    @port.setter
    def port(self, port: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.port = port

    @property
    def allow_query(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.allow_query

    @allow_query.setter
    def allow_query(self, allow_query: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.allow_query = allow_query

    @property
    def allow_query_preview(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.allow_query_preview

    @allow_query_preview.setter
    def allow_query_preview(self, allow_query_preview: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.allow_query_preview = allow_query_preview

    @property
    def query_preview_config(self) -> Optional[Dict[str, str]]:
        return None if self.attributes is None else self.attributes.query_preview_config

    @query_preview_config.setter
    def query_preview_config(self, query_preview_config: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_preview_config = query_preview_config

    @property
    def query_config(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.query_config

    @query_config.setter
    def query_config(self, query_config: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_config = query_config

    @property
    def credential_strategy(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.credential_strategy

    @credential_strategy.setter
    def credential_strategy(self, credential_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.credential_strategy = credential_strategy

    @property
    def preview_credential_strategy(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preview_credential_strategy
        )

    @preview_credential_strategy.setter
    def preview_credential_strategy(self, preview_credential_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preview_credential_strategy = preview_credential_strategy

    @property
    def policy_strategy(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.policy_strategy

    @policy_strategy.setter
    def policy_strategy(self, policy_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_strategy = policy_strategy

    @property
    def policy_strategy_for_sample_preview(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.policy_strategy_for_sample_preview
        )

    @policy_strategy_for_sample_preview.setter
    def policy_strategy_for_sample_preview(
        self, policy_strategy_for_sample_preview: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_strategy_for_sample_preview = (
            policy_strategy_for_sample_preview
        )

    @property
    def query_username_strategy(self) -> Optional[QueryUsernameStrategy]:
        return (
            None if self.attributes is None else self.attributes.query_username_strategy
        )

    @query_username_strategy.setter
    def query_username_strategy(
        self, query_username_strategy: Optional[QueryUsernameStrategy]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_username_strategy = query_username_strategy

    @property
    def row_limit(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.row_limit

    @row_limit.setter
    def row_limit(self, row_limit: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.row_limit = row_limit

    @property
    def query_timeout(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_timeout

    @query_timeout.setter
    def query_timeout(self, query_timeout: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_timeout = query_timeout

    @property
    def default_credential_guid(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.default_credential_guid
        )

    @default_credential_guid.setter
    def default_credential_guid(self, default_credential_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.default_credential_guid = default_credential_guid

    @property
    def connector_icon(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.connector_icon

    @connector_icon.setter
    def connector_icon(self, connector_icon: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connector_icon = connector_icon

    @property
    def connector_image(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.connector_image

    @connector_image.setter
    def connector_image(self, connector_image: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connector_image = connector_image

    @property
    def source_logo(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_logo

    @source_logo.setter
    def source_logo(self, source_logo: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_logo = source_logo

    @property
    def is_sample_data_preview_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.is_sample_data_preview_enabled
        )

    @is_sample_data_preview_enabled.setter
    def is_sample_data_preview_enabled(
        self, is_sample_data_preview_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_sample_data_preview_enabled = is_sample_data_preview_enabled

    @property
    def popularity_insights_timeframe(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.popularity_insights_timeframe
        )

    @popularity_insights_timeframe.setter
    def popularity_insights_timeframe(
        self, popularity_insights_timeframe: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.popularity_insights_timeframe = popularity_insights_timeframe

    @property
    def has_popularity_insights(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.has_popularity_insights
        )

    @has_popularity_insights.setter
    def has_popularity_insights(self, has_popularity_insights: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.has_popularity_insights = has_popularity_insights

    @property
    def connection_dbt_environments(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.connection_dbt_environments
        )

    @connection_dbt_environments.setter
    def connection_dbt_environments(
        self, connection_dbt_environments: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connection_dbt_environments = connection_dbt_environments

    @property
    def connection_s_s_o_credential_guid(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.connection_s_s_o_credential_guid
        )

    @connection_s_s_o_credential_guid.setter
    def connection_s_s_o_credential_guid(
        self, connection_s_s_o_credential_guid: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connection_s_s_o_credential_guid = (
            connection_s_s_o_credential_guid
        )

    @property
    def use_object_storage(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.use_object_storage

    @use_object_storage.setter
    def use_object_storage(self, use_object_storage: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.use_object_storage = use_object_storage

    @property
    def object_storage_upload_threshold(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.object_storage_upload_threshold
        )

    @object_storage_upload_threshold.setter
    def object_storage_upload_threshold(
        self, object_storage_upload_threshold: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.object_storage_upload_threshold = (
            object_storage_upload_threshold
        )

    @property
    def vector_embeddings_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.vector_embeddings_enabled
        )

    @vector_embeddings_enabled.setter
    def vector_embeddings_enabled(self, vector_embeddings_enabled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.vector_embeddings_enabled = vector_embeddings_enabled

    @property
    def vector_embeddings_updated_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.vector_embeddings_updated_at
        )

    @vector_embeddings_updated_at.setter
    def vector_embeddings_updated_at(
        self, vector_embeddings_updated_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.vector_embeddings_updated_at = vector_embeddings_updated_at

    class Attributes(Asset.Attributes):
        category: Optional[str] = Field(default=None, description="")
        sub_category: Optional[str] = Field(default=None, description="")
        host: Optional[str] = Field(default=None, description="")
        port: Optional[int] = Field(default=None, description="")
        allow_query: Optional[bool] = Field(default=None, description="")
        allow_query_preview: Optional[bool] = Field(default=None, description="")
        query_preview_config: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        query_config: Optional[str] = Field(default=None, description="")
        credential_strategy: Optional[str] = Field(default=None, description="")
        preview_credential_strategy: Optional[str] = Field(default=None, description="")
        policy_strategy: Optional[str] = Field(default=None, description="")
        policy_strategy_for_sample_preview: Optional[str] = Field(
            default=None, description=""
        )
        query_username_strategy: Optional[QueryUsernameStrategy] = Field(
            default=None, description=""
        )
        row_limit: Optional[int] = Field(default=None, description="")
        query_timeout: Optional[int] = Field(default=None, description="")
        default_credential_guid: Optional[str] = Field(default=None, description="")
        connector_icon: Optional[str] = Field(default=None, description="")
        connector_image: Optional[str] = Field(default=None, description="")
        source_logo: Optional[str] = Field(default=None, description="")
        is_sample_data_preview_enabled: Optional[bool] = Field(
            default=None, description=""
        )
        popularity_insights_timeframe: Optional[int] = Field(
            default=None, description=""
        )
        has_popularity_insights: Optional[bool] = Field(default=None, description="")
        connection_dbt_environments: Optional[Set[str]] = Field(
            default=None, description=""
        )
        connection_s_s_o_credential_guid: Optional[str] = Field(
            default=None, description=""
        )
        use_object_storage: Optional[bool] = Field(default=None, description="")
        object_storage_upload_threshold: Optional[int] = Field(
            default=None, description=""
        )
        vector_embeddings_enabled: Optional[bool] = Field(default=None, description="")
        vector_embeddings_updated_at: Optional[datetime] = Field(
            default=None, description=""
        )

        is_loaded: bool = Field(default=True)

        @validator("admin_users")
        def admin_users_valid(cls, admin_users, values):
            from pyatlan.cache.user_cache import UserCache

            if values.get("is_loaded", False):
                UserCache.validate_names(names=admin_users)
            return admin_users

        @validator("admin_roles")
        def admin_roles_valid(cls, admin_roles, values):
            from pyatlan.cache.role_cache import RoleCache

            if values.get("is_loaded", False):
                RoleCache.validate_idstrs(idstrs=admin_roles)
            return admin_roles

        @validator("admin_groups")
        def admin_groups_valid(cls, admin_groups, values):
            from pyatlan.cache.group_cache import GroupCache

            if values.get("is_loaded", False):
                GroupCache.validate_aliases(aliases=admin_groups)
                return admin_groups

    attributes: Connection.Attributes = Field(
        default_factory=lambda: Connection.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
