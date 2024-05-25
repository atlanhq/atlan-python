# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .cognos import Cognos


class CognosFile(Cognos):
    """Description"""

    type_name: str = Field(default="CognosFile", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CognosFile":
            raise ValueError("must be CognosFile")
        return v

    def __setattr__(self, name, value):
        if name in CognosFile._convenience_properties:
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

    attributes: CognosFile.Attributes = Field(
        default_factory=lambda: CognosFile.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cognos_folder import CognosFolder  # noqa
