# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Purpose asset model for pyatlan_v9."""

from __future__ import annotations

from typing import Union

import msgspec
from msgspec import UNSET, UnsetType

from pyatlan_v9.model.conversion_utils import (
    build_attributes_kwargs,
    build_flat_kwargs,
    merge_relationships,
)
from pyatlan_v9.model.core import AtlanTagName
from pyatlan_v9.model.serde import Serde, get_serde
from pyatlan_v9.model.structs import SourceTagAttachment
from pyatlan_v9.model.transform import register_asset
from pyatlan_v9.utils import init_guid, validate_required_fields

from .asset import Asset, AssetAttributes, AssetNested


class PurposeClassification(msgspec.Struct, kw_only=True, rename="camel"):
    """Classification view used by Purpose to retain source-tag attachments."""

    type_name: Union[str, None] = None
    source_tag_attachments: list[SourceTagAttachment] = msgspec.field(
        default_factory=list
    )
    entity_status: Union[str, None] = None


@register_asset
class Purpose(Asset):
    """Purpose asset in Atlan."""

    type_name: Union[str, UnsetType] = "Purpose"
    purpose_classifications: Union[list[str], None, UnsetType] = UNSET
    classifications: Union[list[PurposeClassification], None, UnsetType] = UNSET

    @property
    def purpose_atlan_tags(self) -> Union[list[AtlanTagName], None]:
        """Expose purpose classifications as AtlanTagName objects for parity."""
        if self.purpose_classifications in (UNSET, None):
            return None
        return [AtlanTagName(tag) for tag in self.purpose_classifications]

    @purpose_atlan_tags.setter
    def purpose_atlan_tags(self, value: Union[list[AtlanTagName], None]) -> None:
        if value is None:
            self.purpose_classifications = None
        else:
            self.purpose_classifications = [str(tag) for tag in value]

    @classmethod
    @init_guid
    def creator(cls, *, name: str, atlan_tags: list[AtlanTagName]) -> "Purpose":
        """Create a new Purpose asset."""
        validate_required_fields(["name", "atlan_tags"], [name, atlan_tags])
        return cls(
            name=name,
            qualified_name=name,
            display_name=name,
            description="",
            purpose_classifications=[str(tag) for tag in atlan_tags],
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "Purpose":
        """Create a Purpose asset for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "Purpose":
        """Return only required fields for updates."""
        return Purpose.updater(qualified_name=self.qualified_name, name=self.name)

    def to_json(self, nested: bool = True, serde: Serde | None = None) -> str:
        """Serialize the Purpose to JSON."""
        if serde is None:
            serde = get_serde()
        if nested:
            return _purpose_to_nested_bytes(self, serde).decode("utf-8")
        return serde.encode(self).decode("utf-8")

    @staticmethod
    def from_json(
        json_data: Union[str, bytes], serde: Serde | None = None
    ) -> "Purpose":
        """Deserialize a Purpose from nested API JSON."""
        if isinstance(json_data, str):
            json_data = json_data.encode("utf-8")
        if serde is None:
            serde = get_serde()
        return _purpose_from_nested_bytes(json_data, serde)


class PurposeAttributes(AssetAttributes):
    """Purpose-specific nested attributes."""

    purpose_classifications: Union[list[str], None, UnsetType] = UNSET


class PurposeNested(AssetNested):
    """Purpose entity in nested API format."""

    attributes: Union[PurposeAttributes, UnsetType] = UNSET


def _purpose_to_nested(purpose: Purpose) -> PurposeNested:
    attrs_kwargs = build_attributes_kwargs(purpose, PurposeAttributes)
    attrs = PurposeAttributes(**attrs_kwargs)
    return PurposeNested(
        guid=purpose.guid,
        type_name=purpose.type_name,
        status=purpose.status,
        version=purpose.version,
        create_time=purpose.create_time,
        update_time=purpose.update_time,
        created_by=purpose.created_by,
        updated_by=purpose.updated_by,
        classifications=purpose.classifications,
        classification_names=purpose.classification_names,
        meanings=purpose.meanings,
        labels=purpose.labels,
        business_attributes=purpose.business_attributes,
        custom_attributes=purpose.custom_attributes,
        pending_tasks=purpose.pending_tasks,
        proxy=purpose.proxy,
        is_incomplete=purpose.is_incomplete,
        provenance_type=purpose.provenance_type,
        home_id=purpose.home_id,
        attributes=attrs,
    )


def _purpose_from_nested(nested: PurposeNested) -> Purpose:
    attrs = nested.attributes if nested.attributes is not UNSET else PurposeAttributes()
    merged_rels = merge_relationships(
        nested.relationship_attributes,
        nested.append_relationship_attributes,
        nested.remove_relationship_attributes,
        [],
        object,
    )
    kwargs = build_flat_kwargs(
        nested, attrs, merged_rels, AssetNested, PurposeAttributes
    )
    purpose = Purpose(**kwargs)
    if (
        purpose.classifications is not UNSET
        and purpose.classifications is not None
        and purpose.classifications
        and isinstance(purpose.classifications[0], dict)
    ):
        purpose.classifications = [
            msgspec.convert(classification, type=PurposeClassification)
            for classification in purpose.classifications
        ]
    return purpose


def _purpose_to_nested_bytes(purpose: Purpose, serde: Serde) -> bytes:
    return serde.encode(_purpose_to_nested(purpose))


def _purpose_from_nested_bytes(data: bytes, serde: Serde) -> Purpose:
    nested = serde.decode(data, PurposeNested)
    return _purpose_from_nested(nested)
