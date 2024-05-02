# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .mode import Mode


class ModeCollection(Mode):
    """Description"""

    type_name: str = Field(default="ModeCollection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeCollection":
            raise ValueError("must be ModeCollection")
        return v

    def __setattr__(self, name, value):
        if name in ModeCollection._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODE_COLLECTION_TYPE: ClassVar[KeywordField] = KeywordField(
        "modeCollectionType", "modeCollectionType"
    )
    """
    Type of this collection.
    """
    MODE_COLLECTION_STATE: ClassVar[KeywordField] = KeywordField(
        "modeCollectionState", "modeCollectionState"
    )
    """
    State of this collection.
    """

    MODE_WORKSPACE: ClassVar[RelationField] = RelationField("modeWorkspace")
    """
    TBC
    """
    MODE_REPORTS: ClassVar[RelationField] = RelationField("modeReports")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "mode_collection_type",
        "mode_collection_state",
        "mode_workspace",
        "mode_reports",
    ]

    @property
    def mode_collection_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_collection_type

    @mode_collection_type.setter
    def mode_collection_type(self, mode_collection_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_type = mode_collection_type

    @property
    def mode_collection_state(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.mode_collection_state
        )

    @mode_collection_state.setter
    def mode_collection_state(self, mode_collection_state: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_state = mode_collection_state

    @property
    def mode_workspace(self) -> Optional[ModeWorkspace]:
        return None if self.attributes is None else self.attributes.mode_workspace

    @mode_workspace.setter
    def mode_workspace(self, mode_workspace: Optional[ModeWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_workspace = mode_workspace

    @property
    def mode_reports(self) -> Optional[List[ModeReport]]:
        return None if self.attributes is None else self.attributes.mode_reports

    @mode_reports.setter
    def mode_reports(self, mode_reports: Optional[List[ModeReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_reports = mode_reports

    class Attributes(Mode.Attributes):
        mode_collection_type: Optional[str] = Field(default=None, description="")
        mode_collection_state: Optional[str] = Field(default=None, description="")
        mode_workspace: Optional[ModeWorkspace] = Field(
            default=None, description=""
        )  # relationship
        mode_reports: Optional[List[ModeReport]] = Field(
            default=None, description=""
        )  # relationship

    attributes: ModeCollection.Attributes = Field(
        default_factory=lambda: ModeCollection.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .mode_report import ModeReport  # noqa
from .mode_workspace import ModeWorkspace  # noqa
