# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, field_validator

from .asset18 import BI


class Qlik(BI):
    """Description"""

    type_name: str = Field("Qlik", frozen=False)

    @field_validator("type_name")
    @classmethod
    def validate_type_name(cls, v):
        if v != "Qlik":
            raise ValueError("must be Qlik")
        return v

    def __setattr__(self, name, value):
        if name in Qlik._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
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
        qlik_id: Optional[str] = Field(default=None, description="", alias="qlikId")

        qlik_q_r_i: Optional[str] = Field(default=None, description="", alias="qlikQRI")

        qlik_space_id: Optional[str] = Field(
            default=None, description="", alias="qlikSpaceId"
        )

        qlik_space_qualified_name: Optional[str] = Field(
            default=None, description="", alias="qlikSpaceQualifiedName"
        )

        qlik_app_id: Optional[str] = Field(
            default=None, description="", alias="qlikAppId"
        )

        qlik_app_qualified_name: Optional[str] = Field(
            default=None, description="", alias="qlikAppQualifiedName"
        )

        qlik_owner_id: Optional[str] = Field(
            default=None, description="", alias="qlikOwnerId"
        )

        qlik_is_published: Optional[bool] = Field(
            default=None, description="", alias="qlikIsPublished"
        )

    attributes: "Qlik.Attributes" = Field(
        default_factory=lambda: Qlik.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


Qlik.Attributes.update_forward_refs()
