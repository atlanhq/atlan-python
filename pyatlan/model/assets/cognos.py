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


class Cognos(BI):
    """Description"""

    type_name: str = Field(default="Cognos", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Cognos":
            raise ValueError("must be Cognos")
        return v

    def __setattr__(self, name, value):
        if name in Cognos._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COGNOS_ID: ClassVar[KeywordField] = KeywordField("cognosId", "cognosId")
    """
    ID of the asset in Cognos
    """
    COGNOS_PATH: ClassVar[KeywordField] = KeywordField("cognosPath", "cognosPath")
    """
    Path of the asset in Cognos. E.g. /content/folder[@name='Folder Name']
    """
    COGNOS_PARENT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "cognosParentName", "cognosParentName.keyword", "cognosParentName"
    )
    """
    Name of the parent asset in Cognos
    """
    COGNOS_PARENT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "cognosParentQualifiedName", "cognosParentQualifiedName"
    )
    """
    Qualified name of the parent asset in Cognos
    """
    COGNOS_VERSION: ClassVar[KeywordField] = KeywordField(
        "cognosVersion", "cognosVersion"
    )
    """
    Version of the Cognos asset
    """
    COGNOS_TYPE: ClassVar[KeywordField] = KeywordField("cognosType", "cognosType")
    """
    Cognos type of the Cognos asset. E.g. report, dashboard, package, etc.
    """
    COGNOS_IS_HIDDEN: ClassVar[BooleanField] = BooleanField(
        "cognosIsHidden", "cognosIsHidden"
    )
    """
    Whether the Cognos asset is hidden from the ui
    """
    COGNOS_IS_DISABLED: ClassVar[BooleanField] = BooleanField(
        "cognosIsDisabled", "cognosIsDisabled"
    )
    """
    Whether the Cognos asset is diabled
    """
    COGNOS_DEFAULT_SCREEN_TIP: ClassVar[KeywordField] = KeywordField(
        "cognosDefaultScreenTip", "cognosDefaultScreenTip"
    )
    """
    Tooltip text present for the Cognos asset
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cognos_id",
        "cognos_path",
        "cognos_parent_name",
        "cognos_parent_qualified_name",
        "cognos_version",
        "cognos_type",
        "cognos_is_hidden",
        "cognos_is_disabled",
        "cognos_default_screen_tip",
    ]

    @property
    def cognos_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cognos_id

    @cognos_id.setter
    def cognos_id(self, cognos_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_id = cognos_id

    @property
    def cognos_path(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cognos_path

    @cognos_path.setter
    def cognos_path(self, cognos_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_path = cognos_path

    @property
    def cognos_parent_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cognos_parent_name

    @cognos_parent_name.setter
    def cognos_parent_name(self, cognos_parent_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_parent_name = cognos_parent_name

    @property
    def cognos_parent_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cognos_parent_qualified_name
        )

    @cognos_parent_qualified_name.setter
    def cognos_parent_qualified_name(self, cognos_parent_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_parent_qualified_name = cognos_parent_qualified_name

    @property
    def cognos_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cognos_version

    @cognos_version.setter
    def cognos_version(self, cognos_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_version = cognos_version

    @property
    def cognos_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cognos_type

    @cognos_type.setter
    def cognos_type(self, cognos_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_type = cognos_type

    @property
    def cognos_is_hidden(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.cognos_is_hidden

    @cognos_is_hidden.setter
    def cognos_is_hidden(self, cognos_is_hidden: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_is_hidden = cognos_is_hidden

    @property
    def cognos_is_disabled(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.cognos_is_disabled

    @cognos_is_disabled.setter
    def cognos_is_disabled(self, cognos_is_disabled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_is_disabled = cognos_is_disabled

    @property
    def cognos_default_screen_tip(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cognos_default_screen_tip
        )

    @cognos_default_screen_tip.setter
    def cognos_default_screen_tip(self, cognos_default_screen_tip: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_default_screen_tip = cognos_default_screen_tip

    class Attributes(BI.Attributes):
        cognos_id: Optional[str] = Field(default=None, description="")
        cognos_path: Optional[str] = Field(default=None, description="")
        cognos_parent_name: Optional[str] = Field(default=None, description="")
        cognos_parent_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        cognos_version: Optional[str] = Field(default=None, description="")
        cognos_type: Optional[str] = Field(default=None, description="")
        cognos_is_hidden: Optional[bool] = Field(default=None, description="")
        cognos_is_disabled: Optional[bool] = Field(default=None, description="")
        cognos_default_screen_tip: Optional[str] = Field(default=None, description="")

    attributes: Cognos.Attributes = Field(
        default_factory=lambda: Cognos.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
