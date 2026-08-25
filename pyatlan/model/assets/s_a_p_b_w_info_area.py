# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .s_a_p_b_w import SAPBW


class SAPBWInfoArea(SAPBW):
    """Description"""

    type_name: str = Field(default="SAPBWInfoArea", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SAPBWInfoArea":
            raise ValueError("must be SAPBWInfoArea")
        return v

    def __setattr__(self, name, value):
        if name in SAPBWInfoArea._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_BW_CHILD_INFO_AREAS: ClassVar[RelationField] = RelationField(
        "sapBwChildInfoAreas"
    )
    """
    TBC
    """
    SAP_BW_COMPOSITE_PROVIDERS: ClassVar[RelationField] = RelationField(
        "sapBwCompositeProviders"
    )
    """
    TBC
    """
    SAP_BW_PARENT_INFO_AREA: ClassVar[RelationField] = RelationField(
        "sapBwParentInfoArea"
    )
    """
    TBC
    """
    SAP_BW_ADSOS: ClassVar[RelationField] = RelationField("sapBwAdsos")
    """
    TBC
    """
    SAP_BW_QUERIES: ClassVar[RelationField] = RelationField("sapBwQueries")
    """
    TBC
    """
    SAP_BW_INFO_OBJECTS: ClassVar[RelationField] = RelationField("sapBwInfoObjects")
    """
    TBC
    """
    SAP_BW_INFO_SOURCES: ClassVar[RelationField] = RelationField("sapBwInfoSources")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_bw_child_info_areas",
        "sap_bw_composite_providers",
        "sap_bw_parent_info_area",
        "sap_bw_adsos",
        "sap_bw_queries",
        "sap_bw_info_objects",
        "sap_bw_info_sources",
    ]

    @property
    def sap_bw_child_info_areas(self) -> Optional[List[SAPBWInfoArea]]:
        return (
            None if self.attributes is None else self.attributes.sap_bw_child_info_areas
        )

    @sap_bw_child_info_areas.setter
    def sap_bw_child_info_areas(
        self, sap_bw_child_info_areas: Optional[List[SAPBWInfoArea]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_child_info_areas = sap_bw_child_info_areas

    @property
    def sap_bw_composite_providers(self) -> Optional[List[SAPBWCompositeProvider]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_bw_composite_providers
        )

    @sap_bw_composite_providers.setter
    def sap_bw_composite_providers(
        self, sap_bw_composite_providers: Optional[List[SAPBWCompositeProvider]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_composite_providers = sap_bw_composite_providers

    @property
    def sap_bw_parent_info_area(self) -> Optional[SAPBWInfoArea]:
        return (
            None if self.attributes is None else self.attributes.sap_bw_parent_info_area
        )

    @sap_bw_parent_info_area.setter
    def sap_bw_parent_info_area(self, sap_bw_parent_info_area: Optional[SAPBWInfoArea]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_parent_info_area = sap_bw_parent_info_area

    @property
    def sap_bw_adsos(self) -> Optional[List[SAPBWADSO]]:
        return None if self.attributes is None else self.attributes.sap_bw_adsos

    @sap_bw_adsos.setter
    def sap_bw_adsos(self, sap_bw_adsos: Optional[List[SAPBWADSO]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_adsos = sap_bw_adsos

    @property
    def sap_bw_queries(self) -> Optional[List[SAPBWQuery]]:
        return None if self.attributes is None else self.attributes.sap_bw_queries

    @sap_bw_queries.setter
    def sap_bw_queries(self, sap_bw_queries: Optional[List[SAPBWQuery]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_queries = sap_bw_queries

    @property
    def sap_bw_info_objects(self) -> Optional[List[SAPBWInfoObject]]:
        return None if self.attributes is None else self.attributes.sap_bw_info_objects

    @sap_bw_info_objects.setter
    def sap_bw_info_objects(self, sap_bw_info_objects: Optional[List[SAPBWInfoObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_info_objects = sap_bw_info_objects

    @property
    def sap_bw_info_sources(self) -> Optional[List[SAPBWInfoSource]]:
        return None if self.attributes is None else self.attributes.sap_bw_info_sources

    @sap_bw_info_sources.setter
    def sap_bw_info_sources(self, sap_bw_info_sources: Optional[List[SAPBWInfoSource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_info_sources = sap_bw_info_sources

    class Attributes(SAPBW.Attributes):
        sap_bw_child_info_areas: Optional[List[SAPBWInfoArea]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_composite_providers: Optional[List[SAPBWCompositeProvider]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_parent_info_area: Optional[SAPBWInfoArea] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_adsos: Optional[List[SAPBWADSO]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_queries: Optional[List[SAPBWQuery]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_info_objects: Optional[List[SAPBWInfoObject]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_info_sources: Optional[List[SAPBWInfoSource]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SAPBWInfoArea.Attributes = Field(
        default_factory=lambda: SAPBWInfoArea.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_a_p_b_w_a_d_s_o import SAPBWADSO  # noqa: E402, F401
from .s_a_p_b_w_composite_provider import SAPBWCompositeProvider  # noqa: E402, F401
from .s_a_p_b_w_info_object import SAPBWInfoObject  # noqa: E402, F401
from .s_a_p_b_w_info_source import SAPBWInfoSource  # noqa: E402, F401
from .s_a_p_b_w_query import SAPBWQuery  # noqa: E402, F401

SAPBWInfoArea.Attributes.update_forward_refs()
