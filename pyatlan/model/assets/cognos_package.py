# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .cognos import Cognos


class CognosPackage(Cognos):
    """Description"""

    type_name: str = Field(default="CognosPackage", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CognosPackage":
            raise ValueError("must be CognosPackage")
        return v

    def __setattr__(self, name, value):
        if name in CognosPackage._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COGNOS_FOLDER: ClassVar[RelationField] = RelationField("cognosFolder")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cognos_folder",
    ]

    @property
    def cognos_folder(self) -> Optional[CognosFolder]:
        return None if self.attributes is None else self.attributes.cognos_folder

    @cognos_folder.setter
    def cognos_folder(self, cognos_folder: Optional[CognosFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_folder = cognos_folder

    class Attributes(Cognos.Attributes):
        cognos_folder: Optional[CognosFolder] = Field(
            default=None, description=""
        )  # relationship

    attributes: CognosPackage.Attributes = Field(
        default_factory=lambda: CognosPackage.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cognos_folder import CognosFolder  # noqa: E402, F401

CognosPackage.Attributes.update_forward_refs()
