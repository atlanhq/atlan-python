# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .s_a_p_b_w import SAPBW


class SAPBWDTP(SAPBW):
    """Description"""

    type_name: str = Field(default="SAPBWDTP", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SAPBWDTP":
            raise ValueError("must be SAPBWDTP")
        return v

    def __setattr__(self, name, value):
        if name in SAPBWDTP._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_BW_PROCESSES: ClassVar[RelationField] = RelationField("sapBwProcesses")
    """
    TBC
    """
    SAP_BW_TRANSFORMATIONS: ClassVar[RelationField] = RelationField(
        "sapBwTransformations"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_bw_processes",
        "sap_bw_transformations",
    ]

    @property
    def sap_bw_processes(self) -> Optional[List[SAPProcess]]:
        return None if self.attributes is None else self.attributes.sap_bw_processes

    @sap_bw_processes.setter
    def sap_bw_processes(self, sap_bw_processes: Optional[List[SAPProcess]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_processes = sap_bw_processes

    @property
    def sap_bw_transformations(self) -> Optional[List[SAPBWTransformation]]:
        return (
            None if self.attributes is None else self.attributes.sap_bw_transformations
        )

    @sap_bw_transformations.setter
    def sap_bw_transformations(
        self, sap_bw_transformations: Optional[List[SAPBWTransformation]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_transformations = sap_bw_transformations

    class Attributes(SAPBW.Attributes):
        sap_bw_processes: Optional[List[SAPProcess]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_transformations: Optional[List[SAPBWTransformation]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SAPBWDTP.Attributes = Field(
        default_factory=lambda: SAPBWDTP.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_a_p_b_w_transformation import SAPBWTransformation  # noqa: E402, F401
from .s_a_p_process import SAPProcess  # noqa: E402, F401

SAPBWDTP.Attributes.update_forward_refs()
