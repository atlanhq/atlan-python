# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .mode import Mode


class ModeWorkspace(Mode):
    """Description"""

    type_name: str = Field(default="ModeWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeWorkspace":
            raise ValueError("must be ModeWorkspace")
        return v

    def __setattr__(self, name, value):
        if name in ModeWorkspace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODE_COLLECTION_COUNT: ClassVar[NumericField] = NumericField(
        "modeCollectionCount", "modeCollectionCount"
    )
    """
    Number of collections in this workspace.
    """

    MODE_COLLECTIONS: ClassVar[RelationField] = RelationField("modeCollections")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "mode_collection_count",
        "mode_collections",
    ]

    @property
    def mode_collection_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.mode_collection_count
        )

    @mode_collection_count.setter
    def mode_collection_count(self, mode_collection_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_count = mode_collection_count

    @property
    def mode_collections(self) -> Optional[List[ModeCollection]]:
        return None if self.attributes is None else self.attributes.mode_collections

    @mode_collections.setter
    def mode_collections(self, mode_collections: Optional[List[ModeCollection]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collections = mode_collections

    class Attributes(Mode.Attributes):
        mode_collection_count: Optional[int] = Field(default=None, description="")
        mode_collections: Optional[List[ModeCollection]] = Field(
            default=None, description=""
        )  # relationship

    attributes: ModeWorkspace.Attributes = Field(
        default_factory=lambda: ModeWorkspace.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .mode_collection import ModeCollection  # noqa
