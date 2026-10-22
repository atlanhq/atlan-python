from typing import Any, Dict, Optional

from pydantic.v1 import Extra, Field

from pyatlan.model.core import AtlanObject


class SSOMapperConfig(AtlanObject):
    sync_mode: Optional[str] = Field(default=None)
    attributes: Optional[str] = Field(default=None)
    group_name: Optional[str] = Field(default=None, alias="group")
    attribute_name: Optional[str] = Field(default=None, alias="attribute.name")
    attribute_value: Optional[str] = Field(default=None, alias="attribute.value")
    attribute_friendly_name: Optional[str] = Field(
        default=None, alias="attribute.friendly.name"
    )
    attribute_values_regex: Optional[str] = Field(
        default=None, alias="are.attribute.values.regex"
    )


class SSOMapper(AtlanObject):
    id: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    identity_provider_mapper: str
    identity_provider_alias: str
    config: SSOMapperConfig


class SSOProvider(AtlanObject):
    """
    A tenant's SSO identity provider configuration (Keycloak identity
    provider representation), as returned by `GET /api/service/idp`.

    The nested `config` is intentionally an untyped mapping: the backend
    treats updates as full replacements, so every key returned by the API
    must be sent back verbatim on update. Typing it would risk silently
    dropping (and therefore resetting) fields the SDK does not know about.
    """

    class Config(AtlanObject.Config):
        extra = Extra.allow

    alias: Optional[str] = Field(default=None)
    internal_id: Optional[str] = Field(default=None, alias="internalId")
    display_name: Optional[str] = Field(default=None, alias="displayName")
    provider_id: Optional[str] = Field(default=None, alias="providerId")
    enabled: Optional[bool] = Field(default=None)
    trust_email: Optional[bool] = Field(default=None, alias="trustEmail")
    store_token: Optional[bool] = Field(default=None, alias="storeToken")
    link_only: Optional[bool] = Field(default=None, alias="linkOnly")
    add_read_token_role_on_create: Optional[bool] = Field(
        default=None, alias="addReadTokenRoleOnCreate"
    )
    first_broker_login_flow_alias: Optional[str] = Field(
        default=None, alias="firstBrokerLoginFlowAlias"
    )
    config: Optional[Dict[str, Any]] = Field(default=None)
