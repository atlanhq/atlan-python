# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .g_c_p_dataplex import GCPDataplex


class GCPDataplexAspectType(GCPDataplex):
    """Description"""

    type_name: str = Field(default="GCPDataplexAspectType", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "GCPDataplexAspectType":
            raise ValueError("must be GCPDataplexAspectType")
        return v

    def __setattr__(self, name, value):
        if name in GCPDataplexAspectType._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    GCP_DATAPLEX_ASPECT_TYPE_RESOURCE_NAME: ClassVar[KeywordField] = KeywordField(
        "gcpDataplexAspectTypeResourceName", "gcpDataplexAspectTypeResourceName"
    )
    """
    Full GCP resource name of this Aspect Type (e.g. projects/{project}/locations/{location}/aspectTypes/{id}). Used to match against assetGCPDataplexAspectType on BigQuery entry assets.
    """  # noqa: E501
    GCP_DATAPLEX_ASPECT_TYPE_PROJECT: ClassVar[KeywordField] = KeywordField(
        "gcpDataplexAspectTypeProject", "gcpDataplexAspectTypeProject"
    )
    """
    GCP project in which this Aspect Type is defined.
    """
    GCP_DATAPLEX_ASPECT_TYPE_LOCATION: ClassVar[KeywordField] = KeywordField(
        "gcpDataplexAspectTypeLocation", "gcpDataplexAspectTypeLocation"
    )
    """
    GCP location (region or global) in which this Aspect Type is defined.
    """
    GCP_DATAPLEX_ASPECT_TYPE_METADATA_TEMPLATE: ClassVar[KeywordField] = KeywordField(
        "gcpDataplexAspectTypeMetadataTemplate", "gcpDataplexAspectTypeMetadataTemplate"
    )
    """
    Full Dataplex metadataTemplate JSON schema, stored as a stringified JSON blob.
    """
    GCP_DATAPLEX_ASPECT_TYPE_LABELS: ClassVar[KeywordField] = KeywordField(
        "gcpDataplexAspectTypeLabels", "gcpDataplexAspectTypeLabels"
    )
    """
    GCP labels attached to this Aspect Type resource.
    """

    GCP_DATAPLEX_ASPECT_TYPE_ENTRIES: ClassVar[RelationField] = RelationField(
        "gcpDataplexAspectTypeEntries"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "gcp_dataplex_aspect_type_resource_name",
        "gcp_dataplex_aspect_type_project",
        "gcp_dataplex_aspect_type_location",
        "gcp_dataplex_aspect_type_metadata_template",
        "gcp_dataplex_aspect_type_labels",
        "gcp_dataplex_aspect_type_entries",
    ]

    @property
    def gcp_dataplex_aspect_type_resource_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcp_dataplex_aspect_type_resource_name
        )

    @gcp_dataplex_aspect_type_resource_name.setter
    def gcp_dataplex_aspect_type_resource_name(
        self, gcp_dataplex_aspect_type_resource_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcp_dataplex_aspect_type_resource_name = (
            gcp_dataplex_aspect_type_resource_name
        )

    @property
    def gcp_dataplex_aspect_type_project(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcp_dataplex_aspect_type_project
        )

    @gcp_dataplex_aspect_type_project.setter
    def gcp_dataplex_aspect_type_project(
        self, gcp_dataplex_aspect_type_project: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcp_dataplex_aspect_type_project = (
            gcp_dataplex_aspect_type_project
        )

    @property
    def gcp_dataplex_aspect_type_location(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcp_dataplex_aspect_type_location
        )

    @gcp_dataplex_aspect_type_location.setter
    def gcp_dataplex_aspect_type_location(
        self, gcp_dataplex_aspect_type_location: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcp_dataplex_aspect_type_location = (
            gcp_dataplex_aspect_type_location
        )

    @property
    def gcp_dataplex_aspect_type_metadata_template(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcp_dataplex_aspect_type_metadata_template
        )

    @gcp_dataplex_aspect_type_metadata_template.setter
    def gcp_dataplex_aspect_type_metadata_template(
        self, gcp_dataplex_aspect_type_metadata_template: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcp_dataplex_aspect_type_metadata_template = (
            gcp_dataplex_aspect_type_metadata_template
        )

    @property
    def gcp_dataplex_aspect_type_labels(self) -> Optional[Dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcp_dataplex_aspect_type_labels
        )

    @gcp_dataplex_aspect_type_labels.setter
    def gcp_dataplex_aspect_type_labels(
        self, gcp_dataplex_aspect_type_labels: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcp_dataplex_aspect_type_labels = (
            gcp_dataplex_aspect_type_labels
        )

    @property
    def gcp_dataplex_aspect_type_entries(self) -> Optional[List[Asset]]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcp_dataplex_aspect_type_entries
        )

    @gcp_dataplex_aspect_type_entries.setter
    def gcp_dataplex_aspect_type_entries(
        self, gcp_dataplex_aspect_type_entries: Optional[List[Asset]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcp_dataplex_aspect_type_entries = (
            gcp_dataplex_aspect_type_entries
        )

    class Attributes(GCPDataplex.Attributes):
        gcp_dataplex_aspect_type_resource_name: Optional[str] = Field(
            default=None, description=""
        )
        gcp_dataplex_aspect_type_project: Optional[str] = Field(
            default=None, description=""
        )
        gcp_dataplex_aspect_type_location: Optional[str] = Field(
            default=None, description=""
        )
        gcp_dataplex_aspect_type_metadata_template: Optional[str] = Field(
            default=None, description=""
        )
        gcp_dataplex_aspect_type_labels: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        gcp_dataplex_aspect_type_entries: Optional[List[Asset]] = Field(
            default=None, description=""
        )  # relationship

    attributes: GCPDataplexAspectType.Attributes = Field(
        default_factory=lambda: GCPDataplexAspectType.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa: E402, F401
