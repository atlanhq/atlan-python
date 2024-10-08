# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject, AtlanYamlModel
from pyatlan.model.enums import CertificateStatus, DataContractStatus


class InitRequest(AtlanObject):
    asset_type: Optional[str]
    asset_qualified_name: Optional[str]


class DataContractSpec(AtlanYamlModel):
    """
    Capture the detailed specification of a data contract for an asset.
    """

    kind: str = Field(
        default="DataContract",
        description="Controls the specification as one for a data contract.",
    )
    status: Union[DataContractStatus, str] = Field(description="State of the contract.")
    template_version: str = Field(
        default="0.0.2", description="Version of the template for the data contract."
    )
    type: str = Field(description="Type of the dataset in Atlan.")
    dataset: str = Field(description="Name of the asset as it exists inside Atlan.")
    data_source: Optional[str] = Field(
        default=None,
        description="Name that must match a data source defined in your config file.",
    )
    description: Optional[str] = Field(
        default=None, description="Description of this dataset."
    )
    owners: Optional[DataContractSpec.Owners] = Field(
        default=None,
        description=(
            "Owners of the dataset, which can include users (by username) and/or groups (by internal Atlan alias)."
        ),
    )
    certification: Optional[DataContractSpec.Certification] = Field(
        default=None, description="Certification to apply to the dataset."
    )
    announcement: Optional[DataContractSpec.Announcement] = Field(
        default=None, description="Announcement to apply to the dataset."
    )
    terms: Optional[List[str]] = Field(
        default_factory=list, description="Glossary terms to assign to the dataset."
    )
    tags: Optional[List[DataContractSpec.DCTag]] = Field(
        default_factory=list, description="Atlan tags for the dataset."
    )
    custom_metadata_sets: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        alias="custom_metadata",
        description="Custom metadata for the dataset.",
    )
    columns: Optional[List[DataContractSpec.DCColumn]] = Field(
        default_factory=list,
        description="Details of each column in the dataset to be governed.",
    )
    checks: Optional[List[str]] = Field(
        default_factory=list,
        description="List of checks to run to verify data quality of the dataset.",
    )
    extra_properties: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Any extra properties provided in the specification (but unknown to this version of the template).",
    )

    class Owners(AtlanYamlModel):
        """
        Owners of the dataset.
        """

        users: Optional[List[str]] = Field(
            default_factory=list, description="Individual users who own the dataset."
        )
        groups: Optional[List[str]] = Field(
            default_factory=list, description="Groups that own the dataset."
        )

    class Certification(AtlanYamlModel):
        """
        Certification information for the dataset.
        """

        status: Optional[Union[CertificateStatus, str]] = Field(
            default=None, description="State of the certification."
        )
        message: Optional[str] = Field(
            default=None, description="Message to accompany the certification."
        )

    class Announcement(AtlanYamlModel):
        """
        Announcement details for the dataset.
        """

        type: Optional[Union[CertificateStatus, str]] = Field(
            default=None, description="Type of announcement."
        )
        title: Optional[str] = Field(
            default=None, description="Title to use for the announcement."
        )
        description: Optional[str] = Field(
            default=None, description="Message to accompany the announcement."
        )

    class DCTag(AtlanYamlModel):
        """
        Tagging details for the dataset.
        """

        name: Optional[str] = Field(
            default=None, description="Human-readable name of the Atlan tag."
        )
        propagate: Optional[str] = Field(
            default=None, description="Whether to propagate the tag or not."
        )
        propagate_through_lineage: Optional[bool] = Field(
            default=None,
            alias="restrict_propagation_through_lineage",
            description="Whether to propagate the tag through lineage.",
        )
        propagate_through_hierarchy: Optional[bool] = Field(
            default=None,
            alias="restrict_propagation_through_hierarchy",
            description="Whether to propagate the tag through asset's containment hierarchy.",
        )

    class DCColumn(AtlanYamlModel):
        """
        Details of individual columns in the dataset.
        """

        name: Optional[str] = Field(
            default=None,
            description="Name of the column as it is defined in the source system (often technical).",
        )
        display_name: Optional[str] = Field(
            default=None,
            alias="business_name",
            description="Alias for the column, to make its name more readable.",
        )
        description: Optional[str] = Field(
            default=None,
            description="Description of this column, for documentation purposes.",
        )
        is_primary: Optional[bool] = Field(
            default=None,
            description="When true, this column is the primary key for the table.",
        )
        data_type: Optional[str] = Field(
            default=None,
            description="Physical data type of values in this column (e.g. varchar(20)).",
        )
        local_type: Optional[str] = Field(
            default=None,
            description="Logical data type of values in this column (e.g. string).",
        )
        invalid_type: Optional[str] = Field(
            default=None, description="Format of data to consider invalid."
        )
        invalid_format: Optional[str] = Field(
            default=None, description="Format of data to consider valid."
        )
        valid_regex: Optional[str] = Field(
            default=None, description="Regular expression to match valid values."
        )
        missing_regex: Optional[str] = Field(
            default=None, description="Regular expression to match missing values."
        )
        invalid_values: Optional[List[str]] = Field(
            default_factory=list,
            description="Enumeration of values that should be considered invalid.",
        )
        valid_values: Optional[List[str]] = Field(
            default_factory=list,
            description="Enumeration of values that should be considered valid.",
        )
        missing_values: Optional[List[str]] = Field(
            default_factory=list,
            description="Enumeration of values that should be considered missing.",
        )
        not_null: Optional[bool] = Field(
            default=None, description="When true, this column cannot be empty."
        )
        valid_length: Optional[int] = Field(
            default=None,
            description="Fixed length for a string to be considered valid.",
        )
        valid_min: Optional[int] = Field(
            default=None, description="Minimum numeric value considered valid."
        )
        valid_max: Optional[int] = Field(
            default=None, description="Maximum numeric value considered valid."
        )
        valid_min_length: Optional[int] = Field(
            default=None,
            description="Minimum length for a string to be considered valid.",
        )
        unique: Optional[bool] = Field(
            default=None, description="When true, this column must have unique values."
        )
