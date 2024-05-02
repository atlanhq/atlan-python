# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .looker import Looker


class LookerDashboard(Looker):
    """Description"""

    type_name: str = Field(default="LookerDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerDashboard":
            raise ValueError("must be LookerDashboard")
        return v

    def __setattr__(self, name, value):
        if name in LookerDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FOLDER_NAME: ClassVar[KeywordField] = KeywordField("folderName", "folderName")
    """
    Name of the parent folder in Looker that contains this dashboard.
    """
    SOURCE_USER_ID: ClassVar[NumericField] = NumericField(
        "sourceUserId", "sourceUserId"
    )
    """
    Identifier of the user who created this dashboard, from Looker.
    """
    SOURCE_VIEW_COUNT: ClassVar[NumericField] = NumericField(
        "sourceViewCount", "sourceViewCount"
    )
    """
    Number of times the dashboard has been viewed through the Looker web UI.
    """
    SOURCE_METADATA_ID: ClassVar[NumericField] = NumericField(
        "sourceMetadataId", "sourceMetadataId"
    )
    """
    Identifier of the dashboard's content metadata, from Looker.
    """
    SOURCELAST_UPDATER_ID: ClassVar[NumericField] = NumericField(
        "sourcelastUpdaterId", "sourcelastUpdaterId"
    )
    """
    Identifier of the user who last updated the dashboard, from Looker.
    """
    SOURCE_LAST_ACCESSED_AT: ClassVar[NumericField] = NumericField(
        "sourceLastAccessedAt", "sourceLastAccessedAt"
    )
    """
    Timestamp (epoch) when the dashboard was last accessed by a user, in milliseconds.
    """
    SOURCE_LAST_VIEWED_AT: ClassVar[NumericField] = NumericField(
        "sourceLastViewedAt", "sourceLastViewedAt"
    )
    """
    Timestamp (epoch) when the dashboard was last viewed by a user.
    """

    TILES: ClassVar[RelationField] = RelationField("tiles")
    """
    TBC
    """
    LOOKS: ClassVar[RelationField] = RelationField("looks")
    """
    TBC
    """
    FOLDER: ClassVar[RelationField] = RelationField("folder")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "folder_name",
        "source_user_id",
        "source_view_count",
        "source_metadata_id",
        "sourcelast_updater_id",
        "source_last_accessed_at",
        "source_last_viewed_at",
        "tiles",
        "looks",
        "folder",
    ]

    @property
    def folder_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.folder_name

    @folder_name.setter
    def folder_name(self, folder_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.folder_name = folder_name

    @property
    def source_user_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_user_id

    @source_user_id.setter
    def source_user_id(self, source_user_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_user_id = source_user_id

    @property
    def source_view_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_view_count

    @source_view_count.setter
    def source_view_count(self, source_view_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_view_count = source_view_count

    @property
    def source_metadata_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_metadata_id

    @source_metadata_id.setter
    def source_metadata_id(self, source_metadata_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_metadata_id = source_metadata_id

    @property
    def sourcelast_updater_id(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.sourcelast_updater_id
        )

    @sourcelast_updater_id.setter
    def sourcelast_updater_id(self, sourcelast_updater_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sourcelast_updater_id = sourcelast_updater_id

    @property
    def source_last_accessed_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.source_last_accessed_at
        )

    @source_last_accessed_at.setter
    def source_last_accessed_at(self, source_last_accessed_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_last_accessed_at = source_last_accessed_at

    @property
    def source_last_viewed_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.source_last_viewed_at
        )

    @source_last_viewed_at.setter
    def source_last_viewed_at(self, source_last_viewed_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_last_viewed_at = source_last_viewed_at

    @property
    def tiles(self) -> Optional[List[LookerTile]]:
        return None if self.attributes is None else self.attributes.tiles

    @tiles.setter
    def tiles(self, tiles: Optional[List[LookerTile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tiles = tiles

    @property
    def looks(self) -> Optional[List[LookerLook]]:
        return None if self.attributes is None else self.attributes.looks

    @looks.setter
    def looks(self, looks: Optional[List[LookerLook]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looks = looks

    @property
    def folder(self) -> Optional[LookerFolder]:
        return None if self.attributes is None else self.attributes.folder

    @folder.setter
    def folder(self, folder: Optional[LookerFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.folder = folder

    class Attributes(Looker.Attributes):
        folder_name: Optional[str] = Field(default=None, description="")
        source_user_id: Optional[int] = Field(default=None, description="")
        source_view_count: Optional[int] = Field(default=None, description="")
        source_metadata_id: Optional[int] = Field(default=None, description="")
        sourcelast_updater_id: Optional[int] = Field(default=None, description="")
        source_last_accessed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        source_last_viewed_at: Optional[datetime] = Field(default=None, description="")
        tiles: Optional[List[LookerTile]] = Field(
            default=None, description=""
        )  # relationship
        looks: Optional[List[LookerLook]] = Field(
            default=None, description=""
        )  # relationship
        folder: Optional[LookerFolder] = Field(
            default=None, description=""
        )  # relationship

    attributes: LookerDashboard.Attributes = Field(
        default_factory=lambda: LookerDashboard.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .looker_folder import LookerFolder  # noqa
from .looker_look import LookerLook  # noqa
from .looker_tile import LookerTile  # noqa
