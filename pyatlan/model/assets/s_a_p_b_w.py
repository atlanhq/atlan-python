# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField

from .core.s_a_p import SAP


class SAPBW(SAP):
    """Description"""

    type_name: str = Field(default="SAPBW", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SAPBW":
            raise ValueError("must be SAPBW")
        return v

    def __setattr__(self, name, value):
        if name in SAPBW._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_BW_OBJECT_STATUS: ClassVar[KeywordField] = KeywordField(
        "sapBwObjectStatus", "sapBwObjectStatus"
    )
    """
    Lifecycle status of the object in SAP BW such as active, inactive, or modified (e.g. RSDAREA.OBJSTAT, RSKSNEW.OBJSTAT).
    """  # noqa: E501
    SAP_BW_PARENT_NAME: ClassVar[KeywordField] = KeywordField(
        "sapBwParentName", "sapBwParentName"
    )
    """
    Simple name of the SAP BW parent asset in which this asset exists.
    """
    SAP_BW_PARENT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "sapBwParentQualifiedName", "sapBwParentQualifiedName"
    )
    """
    Unique name of the SAP BW parent asset in which this asset exists.
    """
    SAP_BW_INFO_OBJECT_NAME: ClassVar[KeywordField] = KeywordField(
        "sapBwInfoObjectName", "sapBwInfoObjectName"
    )
    """
    Simple name of the SAP BW InfoObject asset related to this asset.
    """
    SAP_BW_INFO_OBJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "sapBwInfoObjectQualifiedName", "sapBwInfoObjectQualifiedName"
    )
    """
    Unique name of the SAP BW InfoObject asset related to this asset.
    """
    SAP_BW_LENGTH: ClassVar[NumericField] = NumericField("sapBwLength", "sapBwLength")
    """
    Length of the field in characters or bytes (e.g. RSDSSEGFD.LENG, RSKSFIELDNEW.LENG).
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_bw_object_status",
        "sap_bw_parent_name",
        "sap_bw_parent_qualified_name",
        "sap_bw_info_object_name",
        "sap_bw_info_object_qualified_name",
        "sap_bw_length",
    ]

    @property
    def sap_bw_object_status(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_bw_object_status

    @sap_bw_object_status.setter
    def sap_bw_object_status(self, sap_bw_object_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_object_status = sap_bw_object_status

    @property
    def sap_bw_parent_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_bw_parent_name

    @sap_bw_parent_name.setter
    def sap_bw_parent_name(self, sap_bw_parent_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_parent_name = sap_bw_parent_name

    @property
    def sap_bw_parent_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_bw_parent_qualified_name
        )

    @sap_bw_parent_qualified_name.setter
    def sap_bw_parent_qualified_name(self, sap_bw_parent_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_parent_qualified_name = sap_bw_parent_qualified_name

    @property
    def sap_bw_info_object_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sap_bw_info_object_name
        )

    @sap_bw_info_object_name.setter
    def sap_bw_info_object_name(self, sap_bw_info_object_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_info_object_name = sap_bw_info_object_name

    @property
    def sap_bw_info_object_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_bw_info_object_qualified_name
        )

    @sap_bw_info_object_qualified_name.setter
    def sap_bw_info_object_qualified_name(
        self, sap_bw_info_object_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_info_object_qualified_name = (
            sap_bw_info_object_qualified_name
        )

    @property
    def sap_bw_length(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.sap_bw_length

    @sap_bw_length.setter
    def sap_bw_length(self, sap_bw_length: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_length = sap_bw_length

    class Attributes(SAP.Attributes):
        sap_bw_object_status: Optional[str] = Field(default=None, description="")
        sap_bw_parent_name: Optional[str] = Field(default=None, description="")
        sap_bw_parent_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sap_bw_info_object_name: Optional[str] = Field(default=None, description="")
        sap_bw_info_object_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sap_bw_length: Optional[int] = Field(default=None, description="")

    attributes: SAPBW.Attributes = Field(
        default_factory=lambda: SAPBW.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


SAPBW.Attributes.update_forward_refs()
