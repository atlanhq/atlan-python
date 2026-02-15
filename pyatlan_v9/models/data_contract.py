# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""DataContract asset model for pyatlan_v9."""

from __future__ import annotations

import re
from json import JSONDecodeError, loads
from typing import Union

from msgspec import UNSET, UnsetType

from pyatlan.errors import ErrorCode
from pyatlan.model.contract import DataContractSpec
from pyatlan_v9.conversion_utils import (
    build_attributes_kwargs,
    build_flat_kwargs,
    categorize_relationships,
    merge_relationships,
)
from pyatlan_v9.serde import Serde, get_serde
from pyatlan_v9.transform import register_asset
from pyatlan_v9.utils import init_guid, validate_required_fields

from .asset_related import RelatedAsset
from .catalog import (
    Catalog,
    CatalogAttributes,
    CatalogNested,
    CatalogRelationshipAttributes,
)
from .catalog_related import RelatedCatalog


@register_asset
class DataContract(Catalog):
    """Instance of a data contract in Atlan."""

    type_name: Union[str, UnsetType] = "DataContract"

    data_contract_json: Union[str, None, UnsetType] = UNSET
    """Deprecated JSON representation of the data contract."""

    data_contract_spec: Union[str, None, UnsetType] = UNSET
    """YAML representation of the data contract."""

    data_contract_version: Union[int, None, UnsetType] = UNSET
    """Version number of the data contract."""

    data_contract_asset_guid: Union[str, None, UnsetType] = UNSET
    """GUID of the governed asset."""

    data_contract_asset_certified: Union[RelatedAsset, None, UnsetType] = UNSET
    """Certified target asset for this contract."""

    data_contract_next_version: Union[RelatedCatalog, None, UnsetType] = UNSET
    """Next version in this contract chain."""

    data_contract_asset_latest: Union[RelatedAsset, None, UnsetType] = UNSET
    """Latest version of this contract."""

    data_contract_previous_version: Union[RelatedCatalog, None, UnsetType] = UNSET
    """Previous version in this contract chain."""

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        asset_qualified_name: str,
        contract_json: Union[str, None] = None,
        contract_spec: Union[DataContractSpec, str, None] = None,
    ) -> "DataContract":
        """Create a new DataContract asset."""
        attrs = DataContract.Attributes.creator(
            asset_qualified_name=asset_qualified_name,
            contract_json=contract_json,
            contract_spec=contract_spec,
        )
        return cls(
            name=attrs.name,
            qualified_name=attrs.qualified_name,
            data_contract_json=attrs.data_contract_json,
            data_contract_spec=attrs.data_contract_spec,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "DataContract":
        """Create a DataContract instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "DataContract":
        """Return only required fields for update operations."""
        return DataContract.updater(qualified_name=self.qualified_name, name=self.name)

    def to_json(self, nested: bool = True, serde: Serde | None = None) -> str:
        """Convert to JSON string."""
        if serde is None:
            serde = get_serde()
        if nested:
            return _data_contract_to_nested_bytes(self, serde).decode("utf-8")
        return serde.encode(self).decode("utf-8")

    @staticmethod
    def from_json(
        json_data: Union[str, bytes], serde: Serde | None = None
    ) -> "DataContract":
        """Create from JSON string or bytes."""
        if isinstance(json_data, str):
            json_data = json_data.encode("utf-8")
        if serde is None:
            serde = get_serde()
        return _data_contract_from_nested_bytes(json_data, serde)


class DataContractAttributes(CatalogAttributes):
    """DataContract-specific attributes for nested API format."""

    data_contract_json: Union[str, None, UnsetType] = UNSET
    data_contract_spec: Union[str, None, UnsetType] = UNSET
    data_contract_version: Union[int, None, UnsetType] = UNSET
    data_contract_asset_guid: Union[str, None, UnsetType] = UNSET

    @classmethod
    def creator(
        cls,
        *,
        asset_qualified_name: str,
        contract_json: Union[str, None] = None,
        contract_spec: Union[DataContractSpec, str, None] = None,
    ) -> "DataContractAttributes":
        """Create DataContract attributes from JSON or YAML contract content."""
        validate_required_fields(["asset_qualified_name"], [asset_qualified_name])
        if not (contract_json or contract_spec):
            raise ValueError(
                "At least one of `contract_json` or `contract_spec` must be provided to create a contract."
            )
        if contract_json and contract_spec:
            raise ValueError(
                "Both `contract_json` and `contract_spec` cannot be provided simultaneously to create a contract."
            )

        default_dataset = asset_qualified_name[asset_qualified_name.rfind("/") + 1 :]
        contract_name: str
        contract_spec_value: Union[str, None] = None

        if contract_json:
            try:
                payload = loads(contract_json)
                dataset = payload.get("dataset")
                if not dataset:
                    raise KeyError("dataset")
                contract_name = f"Data contract for {dataset}"
            except (JSONDecodeError, KeyError):
                raise ErrorCode.INVALID_CONTRACT_JSON.exception_with_parameters()
        else:
            if isinstance(contract_spec, DataContractSpec):
                contract_name = (
                    f"Data contract for {contract_spec.dataset or default_dataset}"
                )
                contract_spec_value = contract_spec.to_yaml()
            else:
                spec_str = contract_spec or ""
                match = re.search(r"dataset:\s*([^\s#]+)", spec_str)
                dataset = match.group(1) if match else default_dataset
                contract_name = f"Data contract for {dataset}"
                contract_spec_value = spec_str

        return cls(
            name=contract_name,
            qualified_name=f"{asset_qualified_name}/contract",
            data_contract_json=contract_json,
            data_contract_spec=contract_spec_value,
        )


DataContract.Attributes = DataContractAttributes  # type: ignore[attr-defined]


class DataContractRelationshipAttributes(CatalogRelationshipAttributes):
    """DataContract-specific relationship attributes for nested API format."""

    data_contract_asset_certified: Union[RelatedAsset, None, UnsetType] = UNSET
    data_contract_next_version: Union[RelatedCatalog, None, UnsetType] = UNSET
    data_contract_asset_latest: Union[RelatedAsset, None, UnsetType] = UNSET
    data_contract_previous_version: Union[RelatedCatalog, None, UnsetType] = UNSET


class DataContractNested(CatalogNested):
    """DataContract in nested API format for high-performance serialization."""

    attributes: Union[DataContractAttributes, UnsetType] = UNSET
    relationship_attributes: Union[DataContractRelationshipAttributes, UnsetType] = (
        UNSET
    )
    append_relationship_attributes: Union[
        DataContractRelationshipAttributes, UnsetType
    ] = UNSET
    remove_relationship_attributes: Union[
        DataContractRelationshipAttributes, UnsetType
    ] = UNSET


def _data_contract_to_nested(data_contract: DataContract) -> DataContractNested:
    """Convert flat DataContract to nested format."""
    attrs_kwargs = build_attributes_kwargs(data_contract, DataContractAttributes)
    attrs = DataContractAttributes(**attrs_kwargs)
    rel_fields: list[str] = [
        "data_contract_asset_certified",
        "data_contract_next_version",
        "data_contract_asset_latest",
        "data_contract_previous_version",
    ]
    replace_rels, append_rels, remove_rels = categorize_relationships(
        data_contract, rel_fields, DataContractRelationshipAttributes
    )
    return DataContractNested(
        guid=data_contract.guid,
        type_name=data_contract.type_name,
        status=data_contract.status,
        version=data_contract.version,
        create_time=data_contract.create_time,
        update_time=data_contract.update_time,
        created_by=data_contract.created_by,
        updated_by=data_contract.updated_by,
        classifications=data_contract.classifications,
        classification_names=data_contract.classification_names,
        meanings=data_contract.meanings,
        labels=data_contract.labels,
        business_attributes=data_contract.business_attributes,
        custom_attributes=data_contract.custom_attributes,
        pending_tasks=data_contract.pending_tasks,
        proxy=data_contract.proxy,
        is_incomplete=data_contract.is_incomplete,
        provenance_type=data_contract.provenance_type,
        home_id=data_contract.home_id,
        attributes=attrs,
        relationship_attributes=replace_rels,
        append_relationship_attributes=append_rels,
        remove_relationship_attributes=remove_rels,
    )


def _data_contract_from_nested(nested: DataContractNested) -> DataContract:
    """Convert nested format to flat DataContract."""
    attrs = (
        nested.attributes
        if nested.attributes is not UNSET
        else DataContractAttributes()
    )
    rel_fields: list[str] = [
        "data_contract_asset_certified",
        "data_contract_next_version",
        "data_contract_asset_latest",
        "data_contract_previous_version",
    ]
    merged_rels = merge_relationships(
        nested.relationship_attributes,
        nested.append_relationship_attributes,
        nested.remove_relationship_attributes,
        rel_fields,
        DataContractRelationshipAttributes,
    )
    kwargs = build_flat_kwargs(
        nested, attrs, merged_rels, CatalogNested, DataContractAttributes
    )
    return DataContract(**kwargs)


def _data_contract_to_nested_bytes(data_contract: DataContract, serde: Serde) -> bytes:
    """Convert flat DataContract to nested JSON bytes."""
    return serde.encode(_data_contract_to_nested(data_contract))


def _data_contract_from_nested_bytes(data: bytes, serde: Serde) -> DataContract:
    """Convert nested JSON bytes to flat DataContract."""
    nested = serde.decode(data, DataContractNested)
    return _data_contract_from_nested(nested)
