# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
)

from .qlik import Qlik


class QlikApp(Qlik):
    """Description"""

    type_name: str = Field(default="QlikApp", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikApp":
            raise ValueError("must be QlikApp")
        return v

    def __setattr__(self, name, value):
        if name in QlikApp._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QLIK_HAS_SECTION_ACCESS: ClassVar[BooleanField] = BooleanField(
        "qlikHasSectionAccess", "qlikHasSectionAccess"
    )
    """
    Whether section access or data masking is enabled on the source (true) or not (false).
    """
    QLIK_ORIGIN_APP_ID: ClassVar[KeywordField] = KeywordField(
        "qlikOriginAppId", "qlikOriginAppId"
    )
    """
    Value of originAppId for this app.
    """
    QLIK_IS_ENCRYPTED: ClassVar[BooleanField] = BooleanField(
        "qlikIsEncrypted", "qlikIsEncrypted"
    )
    """
    Whether this app is encrypted (true) or not (false).
    """
    QLIK_IS_DIRECT_QUERY_MODE: ClassVar[BooleanField] = BooleanField(
        "qlikIsDirectQueryMode", "qlikIsDirectQueryMode"
    )
    """
    Whether this app is in direct query mode (true) or not (false).
    """
    QLIK_APP_STATIC_BYTE_SIZE: ClassVar[NumericField] = NumericField(
        "qlikAppStaticByteSize", "qlikAppStaticByteSize"
    )
    """
    Static space used by this app, in bytes.
    """

    QLIK_SPACE: ClassVar[RelationField] = RelationField("qlikSpace")
    """
    TBC
    """
    QLIK_SHEETS: ClassVar[RelationField] = RelationField("qlikSheets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "qlik_has_section_access",
        "qlik_origin_app_id",
        "qlik_is_encrypted",
        "qlik_is_direct_query_mode",
        "qlik_app_static_byte_size",
        "qlik_space",
        "qlik_sheets",
    ]

    @property
    def qlik_has_section_access(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.qlik_has_section_access
        )

    @qlik_has_section_access.setter
    def qlik_has_section_access(self, qlik_has_section_access: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_has_section_access = qlik_has_section_access

    @property
    def qlik_origin_app_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_origin_app_id

    @qlik_origin_app_id.setter
    def qlik_origin_app_id(self, qlik_origin_app_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_origin_app_id = qlik_origin_app_id

    @property
    def qlik_is_encrypted(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.qlik_is_encrypted

    @qlik_is_encrypted.setter
    def qlik_is_encrypted(self, qlik_is_encrypted: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_is_encrypted = qlik_is_encrypted

    @property
    def qlik_is_direct_query_mode(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.qlik_is_direct_query_mode
        )

    @qlik_is_direct_query_mode.setter
    def qlik_is_direct_query_mode(self, qlik_is_direct_query_mode: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_is_direct_query_mode = qlik_is_direct_query_mode

    @property
    def qlik_app_static_byte_size(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.qlik_app_static_byte_size
        )

    @qlik_app_static_byte_size.setter
    def qlik_app_static_byte_size(self, qlik_app_static_byte_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_app_static_byte_size = qlik_app_static_byte_size

    @property
    def qlik_space(self) -> Optional[QlikSpace]:
        return None if self.attributes is None else self.attributes.qlik_space

    @qlik_space.setter
    def qlik_space(self, qlik_space: Optional[QlikSpace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space = qlik_space

    @property
    def qlik_sheets(self) -> Optional[List[QlikSheet]]:
        return None if self.attributes is None else self.attributes.qlik_sheets

    @qlik_sheets.setter
    def qlik_sheets(self, qlik_sheets: Optional[List[QlikSheet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_sheets = qlik_sheets

    class Attributes(Qlik.Attributes):
        qlik_has_section_access: Optional[bool] = Field(default=None, description="")
        qlik_origin_app_id: Optional[str] = Field(default=None, description="")
        qlik_is_encrypted: Optional[bool] = Field(default=None, description="")
        qlik_is_direct_query_mode: Optional[bool] = Field(default=None, description="")
        qlik_app_static_byte_size: Optional[int] = Field(default=None, description="")
        qlik_space: Optional[QlikSpace] = Field(
            default=None, description=""
        )  # relationship
        qlik_sheets: Optional[List[QlikSheet]] = Field(
            default=None, description=""
        )  # relationship

    attributes: QlikApp.Attributes = Field(
        default_factory=lambda: QlikApp.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .qlik_sheet import QlikSheet  # noqa
from .qlik_space import QlikSpace  # noqa
