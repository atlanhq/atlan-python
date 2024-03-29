# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
)

from .b_i import BI


class Qlik(BI):
    """Description"""

    type_name: str = Field(default="Qlik", allow_mutation=False)

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
    Identifier of this asset, from Qlik.
    """
    QLIK_QRI: ClassVar[KeywordTextField] = KeywordTextField(
        "qlikQRI", "qlikQRI", "qlikQRI.text"
    )
    """
    Unique QRI of this asset, from Qlik.
    """
    QLIK_SPACE_ID: ClassVar[KeywordField] = KeywordField("qlikSpaceId", "qlikSpaceId")
    """
    Identifier of the space in which this asset exists, from Qlik.
    """
    QLIK_SPACE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "qlikSpaceQualifiedName",
        "qlikSpaceQualifiedName",
        "qlikSpaceQualifiedName.text",
    )
    """
    Unique name of the space in which this asset exists.
    """
    QLIK_APP_ID: ClassVar[KeywordField] = KeywordField("qlikAppId", "qlikAppId")
    """
    Identifier of the app in which this asset belongs, from Qlik.
    """
    QLIK_APP_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "qlikAppQualifiedName", "qlikAppQualifiedName", "qlikAppQualifiedName.text"
    )
    """
    Unique name of the app where this asset belongs.
    """
    QLIK_OWNER_ID: ClassVar[KeywordField] = KeywordField("qlikOwnerId", "qlikOwnerId")
    """
    Identifier of the owner of this asset, in Qlik.
    """
    QLIK_IS_PUBLISHED: ClassVar[BooleanField] = BooleanField(
        "qlikIsPublished", "qlikIsPublished"
    )
    """
    Whether this asset is published in Qlik (true) or not (false).
    """

    _convenience_properties: ClassVar[List[str]] = [
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
        qlik_id: Optional[str] = Field(default=None, description="")
        qlik_q_r_i: Optional[str] = Field(default=None, description="")
        qlik_space_id: Optional[str] = Field(default=None, description="")
        qlik_space_qualified_name: Optional[str] = Field(default=None, description="")
        qlik_app_id: Optional[str] = Field(default=None, description="")
        qlik_app_qualified_name: Optional[str] = Field(default=None, description="")
        qlik_owner_id: Optional[str] = Field(default=None, description="")
        qlik_is_published: Optional[bool] = Field(default=None, description="")

    attributes: Qlik.Attributes = Field(
        default_factory=lambda: Qlik.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
