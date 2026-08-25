# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .s_a_p_b_w import SAPBW


class SAPBWDataSource(SAPBW):
    """Description"""

    type_name: str = Field(default="SAPBWDataSource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SAPBWDataSource":
            raise ValueError("must be SAPBWDataSource")
        return v

    def __setattr__(self, name, value):
        if name in SAPBWDataSource._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_BW_LOGICAL_SYSTEM: ClassVar[KeywordField] = KeywordField(
        "sapBwLogicalSystem", "sapBwLogicalSystem"
    )
    """
    Source logical system this DataSource belongs to (RSDS.LOGSYS). Part of the composite primary key.
    """
    SAP_BW_SOURCE_TYPE: ClassVar[KeywordField] = KeywordField(
        "sapBwSourceType", "sapBwSourceType"
    )
    """
    Data type (RSDS.TYPE): M (master), T (text), D (transaction), or H (hierarchy).
    """
    SAP_BW_DELTA_METHOD: ClassVar[KeywordField] = KeywordField(
        "sapBwDeltaMethod", "sapBwDeltaMethod"
    )
    """
    Delta extraction method (RSDS.DELTA) such as AIMD or AIM. Empty means full-load only.
    """

    SAP_BW_DATA_SOURCE_FIELDS: ClassVar[RelationField] = RelationField(
        "sapBwDataSourceFields"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_bw_logical_system",
        "sap_bw_source_type",
        "sap_bw_delta_method",
        "sap_bw_data_source_fields",
    ]

    @property
    def sap_bw_logical_system(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sap_bw_logical_system
        )

    @sap_bw_logical_system.setter
    def sap_bw_logical_system(self, sap_bw_logical_system: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_logical_system = sap_bw_logical_system

    @property
    def sap_bw_source_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_bw_source_type

    @sap_bw_source_type.setter
    def sap_bw_source_type(self, sap_bw_source_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_source_type = sap_bw_source_type

    @property
    def sap_bw_delta_method(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_bw_delta_method

    @sap_bw_delta_method.setter
    def sap_bw_delta_method(self, sap_bw_delta_method: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_delta_method = sap_bw_delta_method

    @property
    def sap_bw_data_source_fields(self) -> Optional[List[SAPBWDataSourceField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_bw_data_source_fields
        )

    @sap_bw_data_source_fields.setter
    def sap_bw_data_source_fields(
        self, sap_bw_data_source_fields: Optional[List[SAPBWDataSourceField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_data_source_fields = sap_bw_data_source_fields

    class Attributes(SAPBW.Attributes):
        sap_bw_logical_system: Optional[str] = Field(default=None, description="")
        sap_bw_source_type: Optional[str] = Field(default=None, description="")
        sap_bw_delta_method: Optional[str] = Field(default=None, description="")
        sap_bw_data_source_fields: Optional[List[SAPBWDataSourceField]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SAPBWDataSource.Attributes = Field(
        default_factory=lambda: SAPBWDataSource.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_a_p_b_w_data_source_field import SAPBWDataSourceField  # noqa: E402, F401

SAPBWDataSource.Attributes.update_forward_refs()
