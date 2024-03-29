# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .cognite import Cognite


class CogniteAsset(Cognite):
    """Description"""

    type_name: str = Field(default="CogniteAsset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CogniteAsset":
            raise ValueError("must be CogniteAsset")
        return v

    def __setattr__(self, name, value):
        if name in CogniteAsset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COGNITE_EVENTS: ClassVar[RelationField] = RelationField("cogniteEvents")
    """
    TBC
    """
    COGNITE_FILES: ClassVar[RelationField] = RelationField("cogniteFiles")
    """
    TBC
    """
    COGNITE_TIMESERIES: ClassVar[RelationField] = RelationField("cogniteTimeseries")
    """
    TBC
    """
    COGNITE_SEQUENCES: ClassVar[RelationField] = RelationField("cogniteSequences")
    """
    TBC
    """
    COGNITE3DMODELS: ClassVar[RelationField] = RelationField("cognite3dmodels")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cognite_events",
        "cognite_files",
        "cognite_timeseries",
        "cognite_sequences",
        "cognite3dmodels",
    ]

    @property
    def cognite_events(self) -> Optional[List[CogniteEvent]]:
        return None if self.attributes is None else self.attributes.cognite_events

    @cognite_events.setter
    def cognite_events(self, cognite_events: Optional[List[CogniteEvent]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_events = cognite_events

    @property
    def cognite_files(self) -> Optional[List[CogniteFile]]:
        return None if self.attributes is None else self.attributes.cognite_files

    @cognite_files.setter
    def cognite_files(self, cognite_files: Optional[List[CogniteFile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_files = cognite_files

    @property
    def cognite_timeseries(self) -> Optional[List[CogniteTimeSeries]]:
        return None if self.attributes is None else self.attributes.cognite_timeseries

    @cognite_timeseries.setter
    def cognite_timeseries(self, cognite_timeseries: Optional[List[CogniteTimeSeries]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_timeseries = cognite_timeseries

    @property
    def cognite_sequences(self) -> Optional[List[CogniteSequence]]:
        return None if self.attributes is None else self.attributes.cognite_sequences

    @cognite_sequences.setter
    def cognite_sequences(self, cognite_sequences: Optional[List[CogniteSequence]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_sequences = cognite_sequences

    @property
    def cognite3dmodels(self) -> Optional[List[Cognite3DModel]]:
        return None if self.attributes is None else self.attributes.cognite3dmodels

    @cognite3dmodels.setter
    def cognite3dmodels(self, cognite3dmodels: Optional[List[Cognite3DModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite3dmodels = cognite3dmodels

    class Attributes(Cognite.Attributes):
        cognite_events: Optional[List[CogniteEvent]] = Field(
            default=None, description=""
        )  # relationship
        cognite_files: Optional[List[CogniteFile]] = Field(
            default=None, description=""
        )  # relationship
        cognite_timeseries: Optional[List[CogniteTimeSeries]] = Field(
            default=None, description=""
        )  # relationship
        cognite_sequences: Optional[List[CogniteSequence]] = Field(
            default=None, description=""
        )  # relationship
        cognite3dmodels: Optional[List[Cognite3DModel]] = Field(
            default=None, description=""
        )  # relationship

    attributes: CogniteAsset.Attributes = Field(
        default_factory=lambda: CogniteAsset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cognite3_d_model import Cognite3DModel  # noqa
from .cognite_event import CogniteEvent  # noqa
from .cognite_file import CogniteFile  # noqa
from .cognite_sequence import CogniteSequence  # noqa
from .cognite_time_series import CogniteTimeSeries  # noqa
