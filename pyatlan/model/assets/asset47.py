# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField

from .asset18 import BI


class QuickSight(BI):
    """Description"""

    type_name: str = Field("QuickSight", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSight":
            raise ValueError("must be QuickSight")
        return v

    def __setattr__(self, name, value):
        if name in QuickSight._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_ID: ClassVar[KeywordField] = KeywordField(
        "quickSightId", "quickSightId"
    )
    """
    TBC
    """
    QUICK_SIGHT_SHEET_ID: ClassVar[KeywordField] = KeywordField(
        "quickSightSheetId", "quickSightSheetId"
    )
    """
    TBC
    """
    QUICK_SIGHT_SHEET_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "quickSightSheetName", "quickSightSheetName.keyword", "quickSightSheetName"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "quick_sight_id",
        "quick_sight_sheet_id",
        "quick_sight_sheet_name",
    ]

    @property
    def quick_sight_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.quick_sight_id

    @quick_sight_id.setter
    def quick_sight_id(self, quick_sight_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_id = quick_sight_id

    @property
    def quick_sight_sheet_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.quick_sight_sheet_id

    @quick_sight_sheet_id.setter
    def quick_sight_sheet_id(self, quick_sight_sheet_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_sheet_id = quick_sight_sheet_id

    @property
    def quick_sight_sheet_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.quick_sight_sheet_name
        )

    @quick_sight_sheet_name.setter
    def quick_sight_sheet_name(self, quick_sight_sheet_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_sheet_name = quick_sight_sheet_name

    class Attributes(BI.Attributes):
        quick_sight_id: Optional[str] = Field(
            None, description="", alias="quickSightId"
        )
        quick_sight_sheet_id: Optional[str] = Field(
            None, description="", alias="quickSightSheetId"
        )
        quick_sight_sheet_name: Optional[str] = Field(
            None, description="", alias="quickSightSheetName"
        )

    attributes: "QuickSight.Attributes" = Field(
        default_factory=lambda: QuickSight.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


QuickSight.Attributes.update_forward_refs()
