# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .s_a_p_b_w import SAPBW


class SAPBWInfoObject(SAPBW):
    """Description"""

    type_name: str = Field(default="SAPBWInfoObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SAPBWInfoObject":
            raise ValueError("must be SAPBWInfoObject")
        return v

    def __setattr__(self, name, value):
        if name in SAPBWInfoObject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_BW_FIELD_NAME: ClassVar[KeywordField] = KeywordField(
        "sapBwFieldName", "sapBwFieldName"
    )
    """
    Associated ABAP field name (RSDIOBJ.FIELDNM).
    """

    SAP_BW_MAPPED_COMPOSITE_PROVIDER_FIELDS: ClassVar[RelationField] = RelationField(
        "sapBwMappedCompositeProviderFields"
    )
    """
    TBC
    """
    SAP_BW_MAPPED_ADSO_FIELDS: ClassVar[RelationField] = RelationField(
        "sapBwMappedAdsoFields"
    )
    """
    TBC
    """
    SAP_BW_RELATED_INFO_OBJECTS: ClassVar[RelationField] = RelationField(
        "sapBwRelatedInfoObjects"
    )
    """
    TBC
    """
    SAP_BW_MAPPED_QUERY_ELEMENTS: ClassVar[RelationField] = RelationField(
        "sapBwMappedQueryElements"
    )
    """
    TBC
    """
    SAP_BW_INFO_OBJECTS: ClassVar[RelationField] = RelationField("sapBwInfoObjects")
    """
    TBC
    """
    SAP_BW_INFO_AREA: ClassVar[RelationField] = RelationField("sapBwInfoArea")
    """
    TBC
    """
    SAP_BW_MAPPED_DATA_SOURCE_FIELDS: ClassVar[RelationField] = RelationField(
        "sapBwMappedDataSourceFields"
    )
    """
    TBC
    """
    SAP_BW_MAPPED_INFO_SOURCE_FIELDS: ClassVar[RelationField] = RelationField(
        "sapBwMappedInfoSourceFields"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_bw_field_name",
        "sap_bw_mapped_composite_provider_fields",
        "sap_bw_mapped_adso_fields",
        "sap_bw_related_info_objects",
        "sap_bw_mapped_query_elements",
        "sap_bw_info_objects",
        "sap_bw_info_area",
        "sap_bw_mapped_data_source_fields",
        "sap_bw_mapped_info_source_fields",
    ]

    @property
    def sap_bw_field_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_bw_field_name

    @sap_bw_field_name.setter
    def sap_bw_field_name(self, sap_bw_field_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_field_name = sap_bw_field_name

    @property
    def sap_bw_mapped_composite_provider_fields(
        self,
    ) -> Optional[List[SAPBWCompositeProviderField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_bw_mapped_composite_provider_fields
        )

    @sap_bw_mapped_composite_provider_fields.setter
    def sap_bw_mapped_composite_provider_fields(
        self,
        sap_bw_mapped_composite_provider_fields: Optional[
            List[SAPBWCompositeProviderField]
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_mapped_composite_provider_fields = (
            sap_bw_mapped_composite_provider_fields
        )

    @property
    def sap_bw_mapped_adso_fields(self) -> Optional[List[SAPBWADSOField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_bw_mapped_adso_fields
        )

    @sap_bw_mapped_adso_fields.setter
    def sap_bw_mapped_adso_fields(
        self, sap_bw_mapped_adso_fields: Optional[List[SAPBWADSOField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_mapped_adso_fields = sap_bw_mapped_adso_fields

    @property
    def sap_bw_related_info_objects(self) -> Optional[List[SAPBWInfoObject]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_bw_related_info_objects
        )

    @sap_bw_related_info_objects.setter
    def sap_bw_related_info_objects(
        self, sap_bw_related_info_objects: Optional[List[SAPBWInfoObject]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_related_info_objects = sap_bw_related_info_objects

    @property
    def sap_bw_mapped_query_elements(self) -> Optional[List[SAPBWQueryElement]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_bw_mapped_query_elements
        )

    @sap_bw_mapped_query_elements.setter
    def sap_bw_mapped_query_elements(
        self, sap_bw_mapped_query_elements: Optional[List[SAPBWQueryElement]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_mapped_query_elements = sap_bw_mapped_query_elements

    @property
    def sap_bw_info_objects(self) -> Optional[List[SAPBWInfoObject]]:
        return None if self.attributes is None else self.attributes.sap_bw_info_objects

    @sap_bw_info_objects.setter
    def sap_bw_info_objects(self, sap_bw_info_objects: Optional[List[SAPBWInfoObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_info_objects = sap_bw_info_objects

    @property
    def sap_bw_info_area(self) -> Optional[SAPBWInfoArea]:
        return None if self.attributes is None else self.attributes.sap_bw_info_area

    @sap_bw_info_area.setter
    def sap_bw_info_area(self, sap_bw_info_area: Optional[SAPBWInfoArea]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_info_area = sap_bw_info_area

    @property
    def sap_bw_mapped_data_source_fields(self) -> Optional[List[SAPBWDataSourceField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_bw_mapped_data_source_fields
        )

    @sap_bw_mapped_data_source_fields.setter
    def sap_bw_mapped_data_source_fields(
        self, sap_bw_mapped_data_source_fields: Optional[List[SAPBWDataSourceField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_mapped_data_source_fields = (
            sap_bw_mapped_data_source_fields
        )

    @property
    def sap_bw_mapped_info_source_fields(self) -> Optional[List[SAPBWInfoSourceField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_bw_mapped_info_source_fields
        )

    @sap_bw_mapped_info_source_fields.setter
    def sap_bw_mapped_info_source_fields(
        self, sap_bw_mapped_info_source_fields: Optional[List[SAPBWInfoSourceField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_mapped_info_source_fields = (
            sap_bw_mapped_info_source_fields
        )

    class Attributes(SAPBW.Attributes):
        sap_bw_field_name: Optional[str] = Field(default=None, description="")
        sap_bw_mapped_composite_provider_fields: Optional[
            List[SAPBWCompositeProviderField]
        ] = Field(default=None, description="")  # relationship
        sap_bw_mapped_adso_fields: Optional[List[SAPBWADSOField]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_related_info_objects: Optional[List[SAPBWInfoObject]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_mapped_query_elements: Optional[List[SAPBWQueryElement]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_info_objects: Optional[List[SAPBWInfoObject]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_info_area: Optional[SAPBWInfoArea] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_mapped_data_source_fields: Optional[List[SAPBWDataSourceField]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_mapped_info_source_fields: Optional[List[SAPBWInfoSourceField]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SAPBWInfoObject.Attributes = Field(
        default_factory=lambda: SAPBWInfoObject.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_a_p_b_w_a_d_s_o_field import SAPBWADSOField  # noqa: E402, F401
from .s_a_p_b_w_composite_provider_field import (
    SAPBWCompositeProviderField,  # noqa: E402, F401
)
from .s_a_p_b_w_data_source_field import SAPBWDataSourceField  # noqa: E402, F401
from .s_a_p_b_w_info_area import SAPBWInfoArea  # noqa: E402, F401
from .s_a_p_b_w_info_source_field import SAPBWInfoSourceField  # noqa: E402, F401
from .s_a_p_b_w_query_element import SAPBWQueryElement  # noqa: E402, F401

SAPBWInfoObject.Attributes.update_forward_refs()
