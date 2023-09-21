# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, StrictStr, validator

from pyatlan.model.enums import EntityStatus
from pyatlan.model.fields.atlan_fields import KeywordField
from pyatlan.model.structs import BadgeCondition
from pyatlan.utils import validate_required_fields

from .asset00 import Asset


class Badge(Asset, type_name="Badge"):
    """Description"""

    @classmethod
    # @validate_arguments()
    def create(
        cls,
        *,
        name: StrictStr,
        cm_name: str,
        cm_attribute: str,
        badge_conditions: list[BadgeCondition],
    ) -> Badge:
        return cls(
            status=EntityStatus.ACTIVE,
            attributes=Badge.Attributes.create(
                name=name,
                cm_name=cm_name,
                cm_attribute=cm_attribute,
                badge_conditions=badge_conditions,
            ),
        )

    type_name: str = Field("Badge", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Badge":
            raise ValueError("must be Badge")
        return v

    def __setattr__(self, name, value):
        if name in Badge._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    BADGE_CONDITIONS: ClassVar[KeywordField] = KeywordField(
        "badgeConditions", "badgeConditions"
    )
    """
    TBC
    """
    BADGE_METADATA_ATTRIBUTE: ClassVar[KeywordField] = KeywordField(
        "badgeMetadataAttribute", "badgeMetadataAttribute"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "badge_conditions",
        "badge_metadata_attribute",
    ]

    @property
    def badge_conditions(self) -> Optional[list[BadgeCondition]]:
        return None if self.attributes is None else self.attributes.badge_conditions

    @badge_conditions.setter
    def badge_conditions(self, badge_conditions: Optional[list[BadgeCondition]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.badge_conditions = badge_conditions

    @property
    def badge_metadata_attribute(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.badge_metadata_attribute
        )

    @badge_metadata_attribute.setter
    def badge_metadata_attribute(self, badge_metadata_attribute: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.badge_metadata_attribute = badge_metadata_attribute

    class Attributes(Asset.Attributes):
        badge_conditions: Optional[list[BadgeCondition]] = Field(
            None, description="", alias="badgeConditions"
        )
        badge_metadata_attribute: Optional[str] = Field(
            None, description="", alias="badgeMetadataAttribute"
        )

        @classmethod
        # @validate_arguments()
        def create(
            cls,
            *,
            name: StrictStr,
            cm_name: str,
            cm_attribute: str,
            badge_conditions: list[BadgeCondition],
        ) -> Badge.Attributes:
            validate_required_fields(
                ["name", "cm_name", "cm_attribute", "badge_conditions"],
                [name, cm_name, cm_attribute, badge_conditions],
            )
            from pyatlan.cache.custom_metadata_cache import CustomMetadataCache

            cm_id = CustomMetadataCache.get_id_for_name(cm_name)
            cm_attr_id = CustomMetadataCache.get_attr_id_for_name(
                set_name=cm_name, attr_name=cm_attribute
            )
            return Badge.Attributes(
                name=name,
                qualified_name=f"badges/global/{cm_id}.{cm_attr_id}",
                badge_metadata_attribute=f"{cm_id}.{cm_attr_id}",
                badge_conditions=badge_conditions,
            )

    attributes: "Badge.Attributes" = Field(
        default_factory=lambda: Badge.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


Badge.Attributes.update_forward_refs()
