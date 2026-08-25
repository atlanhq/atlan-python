# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .s_a_p_b_w import SAPBW


class SAPBWTransformation(SAPBW):
    """Description"""

    type_name: str = Field(default="SAPBWTransformation", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SAPBWTransformation":
            raise ValueError("must be SAPBWTransformation")
        return v

    def __setattr__(self, name, value):
        if name in SAPBWTransformation._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_BW_RULES: ClassVar[KeywordField] = KeywordField("sapBwRules", "sapBwRules")
    """
    Rules defined within this transformation as key-value pairs (rule_id mapped to rule_type, sourced from RSTRANRULE). Mirrors the SAP ERP sapErpFunctionModuleImportParams shape.
    """  # noqa: E501

    SAP_BW_COLUMN_PROCESSES: ClassVar[RelationField] = RelationField(
        "sapBwColumnProcesses"
    )
    """
    TBC
    """
    SAP_BW_DTPS: ClassVar[RelationField] = RelationField("sapBwDtps")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_bw_rules",
        "sap_bw_column_processes",
        "sap_bw_dtps",
    ]

    @property
    def sap_bw_rules(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.sap_bw_rules

    @sap_bw_rules.setter
    def sap_bw_rules(self, sap_bw_rules: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_rules = sap_bw_rules

    @property
    def sap_bw_column_processes(self) -> Optional[List[SAPColumnProcess]]:
        return (
            None if self.attributes is None else self.attributes.sap_bw_column_processes
        )

    @sap_bw_column_processes.setter
    def sap_bw_column_processes(
        self, sap_bw_column_processes: Optional[List[SAPColumnProcess]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_column_processes = sap_bw_column_processes

    @property
    def sap_bw_dtps(self) -> Optional[List[SAPBWDTP]]:
        return None if self.attributes is None else self.attributes.sap_bw_dtps

    @sap_bw_dtps.setter
    def sap_bw_dtps(self, sap_bw_dtps: Optional[List[SAPBWDTP]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_dtps = sap_bw_dtps

    class Attributes(SAPBW.Attributes):
        sap_bw_rules: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        sap_bw_column_processes: Optional[List[SAPColumnProcess]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_dtps: Optional[List[SAPBWDTP]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SAPBWTransformation.Attributes = Field(
        default_factory=lambda: SAPBWTransformation.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_a_p_b_w_d_t_p import SAPBWDTP  # noqa: E402, F401
from .s_a_p_column_process import SAPColumnProcess  # noqa: E402, F401

SAPBWTransformation.Attributes.update_forward_refs()
