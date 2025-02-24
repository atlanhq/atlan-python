from typing import Optional

from pydantic.v1 import Field

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
