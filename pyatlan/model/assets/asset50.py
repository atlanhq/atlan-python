# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
)

from .asset18 import BI


class Qlik(BI):
    """Description"""

    type_name: str = Field("Qlik", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Qlik":
            raise ValueError("must be Qlik")
        return v

    def __setattr__(self, name, value):
        if name in Qlik._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QLIK_ID: ClassVar[KeywordField] = KeywordField("qlikId", "qlikId")
    """
    qID/guid of the qlik object
    """
    QLIK_QRI: ClassVar[KeywordTextField] = KeywordTextField(
        "qlikQRI", "qlikQRI", "qlikQRI.text"
    )
    """
    QRI of the qlik object, kind of like qualifiedName on Atlan
    """
    QLIK_SPACE_ID: ClassVar[KeywordField] = KeywordField("qlikSpaceId", "qlikSpaceId")
    """
    qID of a space where the qlik object belongs to
    """
    QLIK_SPACE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "qlikSpaceQualifiedName",
        "qlikSpaceQualifiedName",
        "qlikSpaceQualifiedName.text",
    )
    """
    qualifiedName of a space where the qlik object belongs to
    """
    QLIK_APP_ID: ClassVar[KeywordField] = KeywordField("qlikAppId", "qlikAppId")
    """
    qID of a app where the qlik object belongs
    """
    QLIK_APP_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "qlikAppQualifiedName", "qlikAppQualifiedName", "qlikAppQualifiedName.text"
    )
    """
    qualifiedName of an app where the qlik object belongs to
    """
    QLIK_OWNER_ID: ClassVar[KeywordField] = KeywordField("qlikOwnerId", "qlikOwnerId")
    """
    Owner's guid of the qlik object
    """
    QLIK_IS_PUBLISHED: ClassVar[BooleanField] = BooleanField(
        "qlikIsPublished", "qlikIsPublished"
    )
    """
    If the qlik object is published
    """

    _convenience_properties: ClassVar[list[str]] = [
        "qlik_id",
        "qlik_q_r_i",
        "qlik_space_id",
        "qlik_space_qualified_name",
        "qlik_app_id",
        "qlik_app_qualified_name",
        "qlik_owner_id",
        "qlik_is_published",
    ]

    @property
    def qlik_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_id

    @qlik_id.setter
    def qlik_id(self, qlik_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_id = qlik_id

    @property
    def qlik_q_r_i(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_q_r_i

    @qlik_q_r_i.setter
    def qlik_q_r_i(self, qlik_q_r_i: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_q_r_i = qlik_q_r_i

    @property
    def qlik_space_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_space_id

    @qlik_space_id.setter
    def qlik_space_id(self, qlik_space_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space_id = qlik_space_id

    @property
    def qlik_space_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.qlik_space_qualified_name
        )

    @qlik_space_qualified_name.setter
    def qlik_space_qualified_name(self, qlik_space_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space_qualified_name = qlik_space_qualified_name

    @property
    def qlik_app_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_app_id

    @qlik_app_id.setter
    def qlik_app_id(self, qlik_app_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_app_id = qlik_app_id

    @property
    def qlik_app_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.qlik_app_qualified_name
        )

    @qlik_app_qualified_name.setter
    def qlik_app_qualified_name(self, qlik_app_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_app_qualified_name = qlik_app_qualified_name

    @property
    def qlik_owner_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_owner_id

    @qlik_owner_id.setter
    def qlik_owner_id(self, qlik_owner_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_owner_id = qlik_owner_id

    @property
    def qlik_is_published(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.qlik_is_published

    @qlik_is_published.setter
    def qlik_is_published(self, qlik_is_published: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_is_published = qlik_is_published

    class Attributes(BI.Attributes):
        qlik_id: Optional[str] = Field(None, description="", alias="qlikId")
        qlik_q_r_i: Optional[str] = Field(None, description="", alias="qlikQRI")
        qlik_space_id: Optional[str] = Field(None, description="", alias="qlikSpaceId")
        qlik_space_qualified_name: Optional[str] = Field(
            None, description="", alias="qlikSpaceQualifiedName"
        )
        qlik_app_id: Optional[str] = Field(None, description="", alias="qlikAppId")
        qlik_app_qualified_name: Optional[str] = Field(
            None, description="", alias="qlikAppQualifiedName"
        )
        qlik_owner_id: Optional[str] = Field(None, description="", alias="qlikOwnerId")
        qlik_is_published: Optional[bool] = Field(
            None, description="", alias="qlikIsPublished"
        )

    attributes: "Qlik.Attributes" = Field(
        default_factory=lambda: Qlik.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


Qlik.Attributes.update_forward_refs()
