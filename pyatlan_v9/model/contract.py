# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, ClassVar, Union

import msgspec
import yaml

from pyatlan.model.enums import CertificateStatus, DataContractStatus


class InitRequest(msgspec.Struct, kw_only=True):
    """Request to initialize a data contract."""

    asset_type: Union[str, None] = None
    asset_qualified_name: Union[str, None] = None


class DataContractOwners(msgspec.Struct, kw_only=True):
    """Owners of the dataset."""

    users: list[str] = msgspec.field(default_factory=list)
    """Individual users who own the dataset."""
    groups: list[str] = msgspec.field(default_factory=list)
    """Groups that own the dataset."""


class DataContractCertification(msgspec.Struct, kw_only=True):
    """Certification information for the dataset."""

    status: Union[CertificateStatus, str, None] = None
    """State of the certification."""
    message: Union[str, None] = None
    """Message to accompany the certification."""


class DataContractAnnouncement(msgspec.Struct, kw_only=True):
    """Announcement details for the dataset."""

    type: Union[CertificateStatus, str, None] = None
    """Type of announcement."""
    title: Union[str, None] = None
    """Title to use for the announcement."""
    description: Union[str, None] = None
    """Message to accompany the announcement."""


class DCTag(msgspec.Struct, kw_only=True):
    """Tagging details for the dataset."""

    name: Union[str, None] = None
    """Human-readable name of the Atlan tag."""
    propagate: Union[bool, str, None] = None
    """Whether to propagate the tag or not."""
    propagate_through_lineage: Union[bool, None] = msgspec.field(
        default=None, name="restrict_propagation_through_lineage"
    )
    """Whether to propagate the tag through lineage."""
    propagate_through_hierarchy: Union[bool, None] = msgspec.field(
        default=None, name="restrict_propagation_through_hierarchy"
    )
    """Whether to propagate the tag through asset's containment hierarchy."""


class DCColumn(msgspec.Struct, kw_only=True):
    """Details of individual columns in the dataset."""

    name: Union[str, None] = None
    """Name of the column as defined in the source system."""
    display_name: Union[str, None] = msgspec.field(default=None, name="business_name")
    """Alias for the column, to make its name more readable."""
    description: Union[str, None] = None
    """Description of this column."""
    is_primary: Union[bool, None] = None
    """When true, this column is the primary key for the table."""
    required: Union[bool, None] = None
    """When true, this column is required for the table."""
    data_type: Union[str, None] = None
    """Physical data type of values in this column."""
    local_type: Union[str, None] = None
    """Logical data type of values in this column."""
    invalid_type: Union[str, None] = None
    """Format of data to consider invalid."""
    invalid_format: Union[str, None] = None
    """Format of data to consider valid."""
    valid_regex: Union[str, None] = None
    """Regular expression to match valid values."""
    missing_regex: Union[str, None] = None
    """Regular expression to match missing values."""
    invalid_values: list[str] = msgspec.field(default_factory=list)
    """Enumeration of values that should be considered invalid."""
    valid_values: list[str] = msgspec.field(default_factory=list)
    """Enumeration of values that should be considered valid."""
    missing_values: list[str] = msgspec.field(default_factory=list)
    """Enumeration of values that should be considered missing."""
    not_null: Union[Any, None] = None
    """When true, this column cannot be empty."""
    valid_length: Union[int, None] = None
    """Fixed length for a string to be considered valid."""
    valid_min: Union[int, None] = None
    """Minimum numeric value considered valid."""
    valid_max: Union[int, None] = None
    """Maximum numeric value considered valid."""
    valid_min_length: Union[int, None] = None
    """Minimum length for a string to be considered valid."""
    unique: Union[Any, None] = None
    """When true, this column must have unique values."""


class DataContractSpec(msgspec.Struct, kw_only=True):
    """Capture the detailed specification of a data contract for an asset."""

    kind: str = "DataContract"
    """Controls the specification as one for a data contract."""
    status: Union[DataContractStatus, str] = ""
    """State of the contract."""
    template_version: str = "0.0.2"
    """Version of the template for the data contract."""
    type: str = ""
    """Type of the dataset in Atlan."""
    dataset: str = ""
    """Name of the asset as it exists inside Atlan."""
    data_source: Union[str, None] = None
    """Name that must match a data source defined in your config file."""
    description: Union[str, None] = None
    """Description of this dataset."""
    owners: Union[DataContractOwners, None] = None
    """Owners of the dataset."""
    certification: Union[DataContractCertification, None] = None
    """Certification to apply to the dataset."""
    announcement: Union[DataContractAnnouncement, None] = None
    """Announcement to apply to the dataset."""
    terms: list[str] = msgspec.field(default_factory=list)
    """Glossary terms to assign to the dataset."""
    tags: list[DCTag] = msgspec.field(default_factory=list)
    """Atlan tags for the dataset."""
    custom_metadata_sets: Union[dict[str, Any], None] = msgspec.field(
        default_factory=dict, name="custom_metadata"
    )
    """Custom metadata for the dataset."""
    columns: list[DCColumn] = msgspec.field(default_factory=list)
    """Details of each column in the dataset to be governed."""
    checks: list[str] = msgspec.field(default_factory=list)
    """List of checks to run to verify data quality of the dataset."""
    extra_properties: dict[str, Any] = msgspec.field(default_factory=dict)
    """Extra properties provided in the specification."""

    # -- Alias mappings: YAML key → Python field name ----------------------
    _ALIAS_TO_FIELD: ClassVar[dict[str, str]] = {
        "custom_metadata": "custom_metadata_sets",
    }
    _COLUMN_ALIAS_TO_FIELD: ClassVar[dict[str, str]] = {
        "business_name": "display_name",
    }
    _TAG_ALIAS_TO_FIELD: ClassVar[dict[str, str]] = {
        "restrict_propagation_through_lineage": "propagate_through_lineage",
        "restrict_propagation_through_hierarchy": "propagate_through_hierarchy",
    }

    @classmethod
    def _remap_keys(cls, data: dict, mapping: dict[str, str]) -> dict:
        """Remap aliased YAML keys to Python field names."""
        return {mapping.get(k, k): v for k, v in data.items()}

    @classmethod
    def from_yaml(cls, yaml_str: str) -> DataContractSpec:
        """
        Create an instance of DataContractSpec from a YAML string.

        :param yaml_str: YAML string to parse.
        :returns: a DataContractSpec with attributes populated from the YAML data.
        """
        data: dict = yaml.safe_load(yaml_str)
        data = cls._remap_keys(data, cls._ALIAS_TO_FIELD)

        # Convert nested dicts to struct types
        if "owners" in data and isinstance(data["owners"], dict):
            data["owners"] = DataContractOwners(**data["owners"])
        if "certification" in data and isinstance(data["certification"], dict):
            data["certification"] = DataContractCertification(**data["certification"])
        if "announcement" in data and isinstance(data["announcement"], dict):
            data["announcement"] = DataContractAnnouncement(**data["announcement"])
        if "tags" in data and isinstance(data["tags"], list):
            data["tags"] = [
                DCTag(**cls._remap_keys(t, cls._TAG_ALIAS_TO_FIELD))
                if isinstance(t, dict)
                else t
                for t in data["tags"]
            ]
        if "columns" in data and isinstance(data["columns"], list):
            data["columns"] = [
                DCColumn(**cls._remap_keys(c, cls._COLUMN_ALIAS_TO_FIELD))
                if isinstance(c, dict)
                else c
                for c in data["columns"]
            ]

        # Collect any extra keys not defined on the struct
        known_fields = {fi.name for fi in msgspec.structs.fields(cls)}
        extra = {k: data.pop(k) for k in list(data) if k not in known_fields}
        spec = cls(**data)
        if extra:
            spec.extra_properties = extra
        return spec

    def to_yaml(self, sort_keys: bool = False) -> str:
        """
        Serialize the DataContractSpec to a YAML string.

        :param sort_keys: whether to sort keys in the YAML output.
        :returns: a YAML string representation of this DataContractSpec.
        """
        raw = msgspec.to_builtins(self)
        return yaml.dump(raw, sort_keys=sort_keys)
