# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .asset57 import Cognite


class CogniteEvent(Cognite):
    """Description"""

    type_name: str = Field("CogniteEvent", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CogniteEvent":
            raise ValueError("must be CogniteEvent")
        return v

    def __setattr__(self, name, value):
        if name in CogniteEvent._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COGNITE_ASSET: ClassVar[RelationField] = RelationField("cogniteAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "cognite_asset",
    ]

    @property
    def cognite_asset(self) -> Optional[CogniteAsset]:
        return None if self.attributes is None else self.attributes.cognite_asset

    @cognite_asset.setter
    def cognite_asset(self, cognite_asset: Optional[CogniteAsset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_asset = cognite_asset

    class Attributes(Cognite.Attributes):
        cognite_asset: Optional[CogniteAsset] = Field(
            None, description="", alias="cogniteAsset"
        )  # relationship

    attributes: "CogniteEvent.Attributes" = Field(
        default_factory=lambda: CogniteEvent.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class CogniteAsset(Cognite):
    """Description"""

    type_name: str = Field("CogniteAsset", allow_mutation=False)

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

    _convenience_properties: ClassVar[list[str]] = [
        "cognite_events",
        "cognite_files",
        "cognite_timeseries",
        "cognite_sequences",
        "cognite3dmodels",
    ]

    @property
    def cognite_events(self) -> Optional[list[CogniteEvent]]:
        return None if self.attributes is None else self.attributes.cognite_events

    @cognite_events.setter
    def cognite_events(self, cognite_events: Optional[list[CogniteEvent]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_events = cognite_events

    @property
    def cognite_files(self) -> Optional[list[CogniteFile]]:
        return None if self.attributes is None else self.attributes.cognite_files

    @cognite_files.setter
    def cognite_files(self, cognite_files: Optional[list[CogniteFile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_files = cognite_files

    @property
    def cognite_timeseries(self) -> Optional[list[CogniteTimeSeries]]:
        return None if self.attributes is None else self.attributes.cognite_timeseries

    @cognite_timeseries.setter
    def cognite_timeseries(self, cognite_timeseries: Optional[list[CogniteTimeSeries]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_timeseries = cognite_timeseries

    @property
    def cognite_sequences(self) -> Optional[list[CogniteSequence]]:
        return None if self.attributes is None else self.attributes.cognite_sequences

    @cognite_sequences.setter
    def cognite_sequences(self, cognite_sequences: Optional[list[CogniteSequence]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_sequences = cognite_sequences

    @property
    def cognite3dmodels(self) -> Optional[list[Cognite3DModel]]:
        return None if self.attributes is None else self.attributes.cognite3dmodels

    @cognite3dmodels.setter
    def cognite3dmodels(self, cognite3dmodels: Optional[list[Cognite3DModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite3dmodels = cognite3dmodels

    class Attributes(Cognite.Attributes):
        cognite_events: Optional[list[CogniteEvent]] = Field(
            None, description="", alias="cogniteEvents"
        )  # relationship
        cognite_files: Optional[list[CogniteFile]] = Field(
            None, description="", alias="cogniteFiles"
        )  # relationship
        cognite_timeseries: Optional[list[CogniteTimeSeries]] = Field(
            None, description="", alias="cogniteTimeseries"
        )  # relationship
        cognite_sequences: Optional[list[CogniteSequence]] = Field(
            None, description="", alias="cogniteSequences"
        )  # relationship
        cognite3dmodels: Optional[list[Cognite3DModel]] = Field(
            None, description="", alias="cognite3dmodels"
        )  # relationship

    attributes: "CogniteAsset.Attributes" = Field(
        default_factory=lambda: CogniteAsset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class CogniteSequence(Cognite):
    """Description"""

    type_name: str = Field("CogniteSequence", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CogniteSequence":
            raise ValueError("must be CogniteSequence")
        return v

    def __setattr__(self, name, value):
        if name in CogniteSequence._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COGNITE_ASSET: ClassVar[RelationField] = RelationField("cogniteAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "cognite_asset",
    ]

    @property
    def cognite_asset(self) -> Optional[CogniteAsset]:
        return None if self.attributes is None else self.attributes.cognite_asset

    @cognite_asset.setter
    def cognite_asset(self, cognite_asset: Optional[CogniteAsset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_asset = cognite_asset

    class Attributes(Cognite.Attributes):
        cognite_asset: Optional[CogniteAsset] = Field(
            None, description="", alias="cogniteAsset"
        )  # relationship

    attributes: "CogniteSequence.Attributes" = Field(
        default_factory=lambda: CogniteSequence.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class Cognite3DModel(Cognite):
    """Description"""

    type_name: str = Field("Cognite3DModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Cognite3DModel":
            raise ValueError("must be Cognite3DModel")
        return v

    def __setattr__(self, name, value):
        if name in Cognite3DModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COGNITE_ASSET: ClassVar[RelationField] = RelationField("cogniteAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "cognite_asset",
    ]

    @property
    def cognite_asset(self) -> Optional[CogniteAsset]:
        return None if self.attributes is None else self.attributes.cognite_asset

    @cognite_asset.setter
    def cognite_asset(self, cognite_asset: Optional[CogniteAsset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_asset = cognite_asset

    class Attributes(Cognite.Attributes):
        cognite_asset: Optional[CogniteAsset] = Field(
            None, description="", alias="cogniteAsset"
        )  # relationship

    attributes: "Cognite3DModel.Attributes" = Field(
        default_factory=lambda: Cognite3DModel.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class CogniteTimeSeries(Cognite):
    """Description"""

    type_name: str = Field("CogniteTimeSeries", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CogniteTimeSeries":
            raise ValueError("must be CogniteTimeSeries")
        return v

    def __setattr__(self, name, value):
        if name in CogniteTimeSeries._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COGNITE_ASSET: ClassVar[RelationField] = RelationField("cogniteAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "cognite_asset",
    ]

    @property
    def cognite_asset(self) -> Optional[CogniteAsset]:
        return None if self.attributes is None else self.attributes.cognite_asset

    @cognite_asset.setter
    def cognite_asset(self, cognite_asset: Optional[CogniteAsset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_asset = cognite_asset

    class Attributes(Cognite.Attributes):
        cognite_asset: Optional[CogniteAsset] = Field(
            None, description="", alias="cogniteAsset"
        )  # relationship

    attributes: "CogniteTimeSeries.Attributes" = Field(
        default_factory=lambda: CogniteTimeSeries.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class CogniteFile(Cognite):
    """Description"""

    type_name: str = Field("CogniteFile", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CogniteFile":
            raise ValueError("must be CogniteFile")
        return v

    def __setattr__(self, name, value):
        if name in CogniteFile._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COGNITE_ASSET: ClassVar[RelationField] = RelationField("cogniteAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "cognite_asset",
    ]

    @property
    def cognite_asset(self) -> Optional[CogniteAsset]:
        return None if self.attributes is None else self.attributes.cognite_asset

    @cognite_asset.setter
    def cognite_asset(self, cognite_asset: Optional[CogniteAsset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_asset = cognite_asset

    class Attributes(Cognite.Attributes):
        cognite_asset: Optional[CogniteAsset] = Field(
            None, description="", alias="cogniteAsset"
        )  # relationship

    attributes: "CogniteFile.Attributes" = Field(
        default_factory=lambda: CogniteFile.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


CogniteEvent.Attributes.update_forward_refs()


CogniteAsset.Attributes.update_forward_refs()


CogniteSequence.Attributes.update_forward_refs()


Cognite3DModel.Attributes.update_forward_refs()


CogniteTimeSeries.Attributes.update_forward_refs()


CogniteFile.Attributes.update_forward_refs()
