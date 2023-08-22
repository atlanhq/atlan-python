# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .asset40 import Looker


class LookerLook(Looker):
    """Description"""

    type_name: str = Field("LookerLook", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerLook":
            raise ValueError("must be LookerLook")
        return v

    def __setattr__(self, name, value):
        if name in LookerLook._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FOLDER_NAME: ClassVar[KeywordField] = KeywordField("folderName", "folderName")
    """
    TBC
    """
    SOURCE_USER_ID: ClassVar[NumericField] = NumericField(
        "sourceUserId", "sourceUserId"
    )
    """
    TBC
    """
    SOURCE_VIEW_COUNT: ClassVar[NumericField] = NumericField(
        "sourceViewCount", "sourceViewCount"
    )
    """
    TBC
    """
    SOURCELAST_UPDATER_ID: ClassVar[NumericField] = NumericField(
        "sourcelastUpdaterId", "sourcelastUpdaterId"
    )
    """
    TBC
    """
    SOURCE_LAST_ACCESSED_AT: ClassVar[NumericField] = NumericField(
        "sourceLastAccessedAt", "sourceLastAccessedAt"
    )
    """
    TBC
    """
    SOURCE_LAST_VIEWED_AT: ClassVar[NumericField] = NumericField(
        "sourceLastViewedAt", "sourceLastViewedAt"
    )
    """
    TBC
    """
    SOURCE_CONTENT_METADATA_ID: ClassVar[NumericField] = NumericField(
        "sourceContentMetadataId", "sourceContentMetadataId"
    )
    """
    TBC
    """
    SOURCE_QUERY_ID: ClassVar[NumericField] = NumericField(
        "sourceQueryId", "sourceQueryId"
    )
    """
    TBC
    """
    MODEL_NAME: ClassVar[KeywordField] = KeywordField("modelName", "modelName")
    """
    TBC
    """

    QUERY: ClassVar[RelationField] = RelationField("query")
    """
    TBC
    """
    FOLDER: ClassVar[RelationField] = RelationField("folder")
    """
    TBC
    """
    TILE: ClassVar[RelationField] = RelationField("tile")
    """
    TBC
    """
    MODEL: ClassVar[RelationField] = RelationField("model")
    """
    TBC
    """
    DASHBOARD: ClassVar[RelationField] = RelationField("dashboard")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "folder_name",
        "source_user_id",
        "source_view_count",
        "sourcelast_updater_id",
        "source_last_accessed_at",
        "source_last_viewed_at",
        "source_content_metadata_id",
        "source_query_id",
        "model_name",
        "query",
        "folder",
        "tile",
        "model",
        "dashboard",
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
    def source_content_metadata_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_content_metadata_id
        )

    @source_content_metadata_id.setter
    def source_content_metadata_id(self, source_content_metadata_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_content_metadata_id = source_content_metadata_id

    @property
    def source_query_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_query_id

    @source_query_id.setter
    def source_query_id(self, source_query_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_query_id = source_query_id

    @property
    def model_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_name

    @model_name.setter
    def model_name(self, model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_name = model_name

    @property
    def query(self) -> Optional[LookerQuery]:
        return None if self.attributes is None else self.attributes.query

    @query.setter
    def query(self, query: Optional[LookerQuery]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query = query

    @property
    def folder(self) -> Optional[LookerFolder]:
        return None if self.attributes is None else self.attributes.folder

    @folder.setter
    def folder(self, folder: Optional[LookerFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.folder = folder

    @property
    def tile(self) -> Optional[LookerTile]:
        return None if self.attributes is None else self.attributes.tile

    @tile.setter
    def tile(self, tile: Optional[LookerTile]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tile = tile

    @property
    def model(self) -> Optional[LookerModel]:
        return None if self.attributes is None else self.attributes.model

    @model.setter
    def model(self, model: Optional[LookerModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model = model

    @property
    def dashboard(self) -> Optional[LookerDashboard]:
        return None if self.attributes is None else self.attributes.dashboard

    @dashboard.setter
    def dashboard(self, dashboard: Optional[LookerDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard = dashboard

    class Attributes(Looker.Attributes):
        folder_name: Optional[str] = Field(None, description="", alias="folderName")
        source_user_id: Optional[int] = Field(
            None, description="", alias="sourceUserId"
        )
        source_view_count: Optional[int] = Field(
            None, description="", alias="sourceViewCount"
        )
        sourcelast_updater_id: Optional[int] = Field(
            None, description="", alias="sourcelastUpdaterId"
        )
        source_last_accessed_at: Optional[datetime] = Field(
            None, description="", alias="sourceLastAccessedAt"
        )
        source_last_viewed_at: Optional[datetime] = Field(
            None, description="", alias="sourceLastViewedAt"
        )
        source_content_metadata_id: Optional[int] = Field(
            None, description="", alias="sourceContentMetadataId"
        )
        source_query_id: Optional[int] = Field(
            None, description="", alias="sourceQueryId"
        )
        model_name: Optional[str] = Field(None, description="", alias="modelName")
        query: Optional[LookerQuery] = Field(
            None, description="", alias="query"
        )  # relationship
        folder: Optional[LookerFolder] = Field(
            None, description="", alias="folder"
        )  # relationship
        tile: Optional[LookerTile] = Field(
            None, description="", alias="tile"
        )  # relationship
        model: Optional[LookerModel] = Field(
            None, description="", alias="model"
        )  # relationship
        dashboard: Optional[LookerDashboard] = Field(
            None, description="", alias="dashboard"
        )  # relationship

    attributes: "LookerLook.Attributes" = Field(
        default_factory=lambda: LookerLook.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerDashboard(Looker):
    """Description"""

    type_name: str = Field("LookerDashboard", allow_mutation=False)

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
    TBC
    """
    SOURCE_USER_ID: ClassVar[NumericField] = NumericField(
        "sourceUserId", "sourceUserId"
    )
    """
    TBC
    """
    SOURCE_VIEW_COUNT: ClassVar[NumericField] = NumericField(
        "sourceViewCount", "sourceViewCount"
    )
    """
    TBC
    """
    SOURCE_METADATA_ID: ClassVar[NumericField] = NumericField(
        "sourceMetadataId", "sourceMetadataId"
    )
    """
    TBC
    """
    SOURCELAST_UPDATER_ID: ClassVar[NumericField] = NumericField(
        "sourcelastUpdaterId", "sourcelastUpdaterId"
    )
    """
    TBC
    """
    SOURCE_LAST_ACCESSED_AT: ClassVar[NumericField] = NumericField(
        "sourceLastAccessedAt", "sourceLastAccessedAt"
    )
    """
    TBC
    """
    SOURCE_LAST_VIEWED_AT: ClassVar[NumericField] = NumericField(
        "sourceLastViewedAt", "sourceLastViewedAt"
    )
    """
    TBC
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

    _convenience_properties: ClassVar[list[str]] = [
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
    def tiles(self) -> Optional[list[LookerTile]]:
        return None if self.attributes is None else self.attributes.tiles

    @tiles.setter
    def tiles(self, tiles: Optional[list[LookerTile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tiles = tiles

    @property
    def looks(self) -> Optional[list[LookerLook]]:
        return None if self.attributes is None else self.attributes.looks

    @looks.setter
    def looks(self, looks: Optional[list[LookerLook]]):
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
        folder_name: Optional[str] = Field(None, description="", alias="folderName")
        source_user_id: Optional[int] = Field(
            None, description="", alias="sourceUserId"
        )
        source_view_count: Optional[int] = Field(
            None, description="", alias="sourceViewCount"
        )
        source_metadata_id: Optional[int] = Field(
            None, description="", alias="sourceMetadataId"
        )
        sourcelast_updater_id: Optional[int] = Field(
            None, description="", alias="sourcelastUpdaterId"
        )
        source_last_accessed_at: Optional[datetime] = Field(
            None, description="", alias="sourceLastAccessedAt"
        )
        source_last_viewed_at: Optional[datetime] = Field(
            None, description="", alias="sourceLastViewedAt"
        )
        tiles: Optional[list[LookerTile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        looks: Optional[list[LookerLook]] = Field(
            None, description="", alias="looks"
        )  # relationship
        folder: Optional[LookerFolder] = Field(
            None, description="", alias="folder"
        )  # relationship

    attributes: "LookerDashboard.Attributes" = Field(
        default_factory=lambda: LookerDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerFolder(Looker):
    """Description"""

    type_name: str = Field("LookerFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerFolder":
            raise ValueError("must be LookerFolder")
        return v

    def __setattr__(self, name, value):
        if name in LookerFolder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SOURCE_CONTENT_METADATA_ID: ClassVar[NumericField] = NumericField(
        "sourceContentMetadataId", "sourceContentMetadataId"
    )
    """
    TBC
    """
    SOURCE_CREATOR_ID: ClassVar[NumericField] = NumericField(
        "sourceCreatorId", "sourceCreatorId"
    )
    """
    TBC
    """
    SOURCE_CHILD_COUNT: ClassVar[NumericField] = NumericField(
        "sourceChildCount", "sourceChildCount"
    )
    """
    TBC
    """
    SOURCE_PARENT_ID: ClassVar[NumericField] = NumericField(
        "sourceParentID", "sourceParentID"
    )
    """
    TBC
    """

    DASHBOARDS: ClassVar[RelationField] = RelationField("dashboards")
    """
    TBC
    """
    LOOKS: ClassVar[RelationField] = RelationField("looks")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "source_content_metadata_id",
        "source_creator_id",
        "source_child_count",
        "source_parent_i_d",
        "dashboards",
        "looks",
    ]

    @property
    def source_content_metadata_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_content_metadata_id
        )

    @source_content_metadata_id.setter
    def source_content_metadata_id(self, source_content_metadata_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_content_metadata_id = source_content_metadata_id

    @property
    def source_creator_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_creator_id

    @source_creator_id.setter
    def source_creator_id(self, source_creator_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_creator_id = source_creator_id

    @property
    def source_child_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_child_count

    @source_child_count.setter
    def source_child_count(self, source_child_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_child_count = source_child_count

    @property
    def source_parent_i_d(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_parent_i_d

    @source_parent_i_d.setter
    def source_parent_i_d(self, source_parent_i_d: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_parent_i_d = source_parent_i_d

    @property
    def dashboards(self) -> Optional[list[LookerDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[list[LookerDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    @property
    def looks(self) -> Optional[list[LookerLook]]:
        return None if self.attributes is None else self.attributes.looks

    @looks.setter
    def looks(self, looks: Optional[list[LookerLook]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looks = looks

    class Attributes(Looker.Attributes):
        source_content_metadata_id: Optional[int] = Field(
            None, description="", alias="sourceContentMetadataId"
        )
        source_creator_id: Optional[int] = Field(
            None, description="", alias="sourceCreatorId"
        )
        source_child_count: Optional[int] = Field(
            None, description="", alias="sourceChildCount"
        )
        source_parent_i_d: Optional[int] = Field(
            None, description="", alias="sourceParentID"
        )
        dashboards: Optional[list[LookerDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship
        looks: Optional[list[LookerLook]] = Field(
            None, description="", alias="looks"
        )  # relationship

    attributes: "LookerFolder.Attributes" = Field(
        default_factory=lambda: LookerFolder.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerTile(Looker):
    """Description"""

    type_name: str = Field("LookerTile", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerTile":
            raise ValueError("must be LookerTile")
        return v

    def __setattr__(self, name, value):
        if name in LookerTile._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    LOOKML_LINK_ID: ClassVar[KeywordField] = KeywordField(
        "lookmlLinkId", "lookmlLinkId"
    )
    """
    TBC
    """
    MERGE_RESULT_ID: ClassVar[KeywordField] = KeywordField(
        "mergeResultId", "mergeResultId"
    )
    """
    TBC
    """
    NOTE_TEXT: ClassVar[KeywordField] = KeywordField("noteText", "noteText")
    """
    TBC
    """
    QUERY_ID: ClassVar[NumericField] = NumericField("queryID", "queryID")
    """
    TBC
    """
    RESULT_MAKER_ID: ClassVar[NumericField] = NumericField(
        "resultMakerID", "resultMakerID"
    )
    """
    TBC
    """
    SUBTITLE_TEXT: ClassVar[KeywordField] = KeywordField("subtitleText", "subtitleText")
    """
    TBC
    """
    LOOK_ID: ClassVar[NumericField] = NumericField("lookId", "lookId")
    """
    TBC
    """

    QUERY: ClassVar[RelationField] = RelationField("query")
    """
    TBC
    """
    LOOK: ClassVar[RelationField] = RelationField("look")
    """
    TBC
    """
    DASHBOARD: ClassVar[RelationField] = RelationField("dashboard")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "lookml_link_id",
        "merge_result_id",
        "note_text",
        "query_i_d",
        "result_maker_i_d",
        "subtitle_text",
        "look_id",
        "query",
        "look",
        "dashboard",
    ]

    @property
    def lookml_link_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.lookml_link_id

    @lookml_link_id.setter
    def lookml_link_id(self, lookml_link_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.lookml_link_id = lookml_link_id

    @property
    def merge_result_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.merge_result_id

    @merge_result_id.setter
    def merge_result_id(self, merge_result_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.merge_result_id = merge_result_id

    @property
    def note_text(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.note_text

    @note_text.setter
    def note_text(self, note_text: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.note_text = note_text

    @property
    def query_i_d(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_i_d

    @query_i_d.setter
    def query_i_d(self, query_i_d: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_i_d = query_i_d

    @property
    def result_maker_i_d(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.result_maker_i_d

    @result_maker_i_d.setter
    def result_maker_i_d(self, result_maker_i_d: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.result_maker_i_d = result_maker_i_d

    @property
    def subtitle_text(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.subtitle_text

    @subtitle_text.setter
    def subtitle_text(self, subtitle_text: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.subtitle_text = subtitle_text

    @property
    def look_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.look_id

    @look_id.setter
    def look_id(self, look_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.look_id = look_id

    @property
    def query(self) -> Optional[LookerQuery]:
        return None if self.attributes is None else self.attributes.query

    @query.setter
    def query(self, query: Optional[LookerQuery]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query = query

    @property
    def look(self) -> Optional[LookerLook]:
        return None if self.attributes is None else self.attributes.look

    @look.setter
    def look(self, look: Optional[LookerLook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.look = look

    @property
    def dashboard(self) -> Optional[LookerDashboard]:
        return None if self.attributes is None else self.attributes.dashboard

    @dashboard.setter
    def dashboard(self, dashboard: Optional[LookerDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard = dashboard

    class Attributes(Looker.Attributes):
        lookml_link_id: Optional[str] = Field(
            None, description="", alias="lookmlLinkId"
        )
        merge_result_id: Optional[str] = Field(
            None, description="", alias="mergeResultId"
        )
        note_text: Optional[str] = Field(None, description="", alias="noteText")
        query_i_d: Optional[int] = Field(None, description="", alias="queryID")
        result_maker_i_d: Optional[int] = Field(
            None, description="", alias="resultMakerID"
        )
        subtitle_text: Optional[str] = Field(None, description="", alias="subtitleText")
        look_id: Optional[int] = Field(None, description="", alias="lookId")
        query: Optional[LookerQuery] = Field(
            None, description="", alias="query"
        )  # relationship
        look: Optional[LookerLook] = Field(
            None, description="", alias="look"
        )  # relationship
        dashboard: Optional[LookerDashboard] = Field(
            None, description="", alias="dashboard"
        )  # relationship

    attributes: "LookerTile.Attributes" = Field(
        default_factory=lambda: LookerTile.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerModel(Looker):
    """Description"""

    type_name: str = Field("LookerModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerModel":
            raise ValueError("must be LookerModel")
        return v

    def __setattr__(self, name, value):
        if name in LookerModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PROJECT_NAME: ClassVar[KeywordField] = KeywordField("projectName", "projectName")
    """
    TBC
    """

    EXPLORES: ClassVar[RelationField] = RelationField("explores")
    """
    TBC
    """
    PROJECT: ClassVar[RelationField] = RelationField("project")
    """
    TBC
    """
    LOOK: ClassVar[RelationField] = RelationField("look")
    """
    TBC
    """
    QUERIES: ClassVar[RelationField] = RelationField("queries")
    """
    TBC
    """
    FIELDS: ClassVar[RelationField] = RelationField("fields")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "project_name",
        "explores",
        "project",
        "look",
        "queries",
        "fields",
    ]

    @property
    def project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.project_name

    @project_name.setter
    def project_name(self, project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_name = project_name

    @property
    def explores(self) -> Optional[list[LookerExplore]]:
        return None if self.attributes is None else self.attributes.explores

    @explores.setter
    def explores(self, explores: Optional[list[LookerExplore]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.explores = explores

    @property
    def project(self) -> Optional[LookerProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[LookerProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def look(self) -> Optional[LookerLook]:
        return None if self.attributes is None else self.attributes.look

    @look.setter
    def look(self, look: Optional[LookerLook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.look = look

    @property
    def queries(self) -> Optional[list[LookerQuery]]:
        return None if self.attributes is None else self.attributes.queries

    @queries.setter
    def queries(self, queries: Optional[list[LookerQuery]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.queries = queries

    @property
    def fields(self) -> Optional[list[LookerField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[list[LookerField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    class Attributes(Looker.Attributes):
        project_name: Optional[str] = Field(None, description="", alias="projectName")
        explores: Optional[list[LookerExplore]] = Field(
            None, description="", alias="explores"
        )  # relationship
        project: Optional[LookerProject] = Field(
            None, description="", alias="project"
        )  # relationship
        look: Optional[LookerLook] = Field(
            None, description="", alias="look"
        )  # relationship
        queries: Optional[list[LookerQuery]] = Field(
            None, description="", alias="queries"
        )  # relationship
        fields: Optional[list[LookerField]] = Field(
            None, description="", alias="fields"
        )  # relationship

    attributes: "LookerModel.Attributes" = Field(
        default_factory=lambda: LookerModel.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerExplore(Looker):
    """Description"""

    type_name: str = Field("LookerExplore", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerExplore":
            raise ValueError("must be LookerExplore")
        return v

    def __setattr__(self, name, value):
        if name in LookerExplore._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PROJECT_NAME: ClassVar[KeywordField] = KeywordField("projectName", "projectName")
    """
    TBC
    """
    MODEL_NAME: ClassVar[KeywordField] = KeywordField("modelName", "modelName")
    """
    TBC
    """
    SOURCE_CONNECTION_NAME: ClassVar[KeywordField] = KeywordField(
        "sourceConnectionName", "sourceConnectionName"
    )
    """
    TBC
    """
    VIEW_NAME: ClassVar[KeywordField] = KeywordField("viewName", "viewName")
    """
    TBC
    """
    SQL_TABLE_NAME: ClassVar[KeywordField] = KeywordField(
        "sqlTableName", "sqlTableName"
    )
    """
    TBC
    """

    PROJECT: ClassVar[RelationField] = RelationField("project")
    """
    TBC
    """
    MODEL: ClassVar[RelationField] = RelationField("model")
    """
    TBC
    """
    FIELDS: ClassVar[RelationField] = RelationField("fields")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "project_name",
        "model_name",
        "source_connection_name",
        "view_name",
        "sql_table_name",
        "project",
        "model",
        "fields",
    ]

    @property
    def project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.project_name

    @project_name.setter
    def project_name(self, project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_name = project_name

    @property
    def model_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_name

    @model_name.setter
    def model_name(self, model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_name = model_name

    @property
    def source_connection_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.source_connection_name
        )

    @source_connection_name.setter
    def source_connection_name(self, source_connection_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_connection_name = source_connection_name

    @property
    def view_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.view_name

    @view_name.setter
    def view_name(self, view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_name = view_name

    @property
    def sql_table_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sql_table_name

    @sql_table_name.setter
    def sql_table_name(self, sql_table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_table_name = sql_table_name

    @property
    def project(self) -> Optional[LookerProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[LookerProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def model(self) -> Optional[LookerModel]:
        return None if self.attributes is None else self.attributes.model

    @model.setter
    def model(self, model: Optional[LookerModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model = model

    @property
    def fields(self) -> Optional[list[LookerField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[list[LookerField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    class Attributes(Looker.Attributes):
        project_name: Optional[str] = Field(None, description="", alias="projectName")
        model_name: Optional[str] = Field(None, description="", alias="modelName")
        source_connection_name: Optional[str] = Field(
            None, description="", alias="sourceConnectionName"
        )
        view_name: Optional[str] = Field(None, description="", alias="viewName")
        sql_table_name: Optional[str] = Field(
            None, description="", alias="sqlTableName"
        )
        project: Optional[LookerProject] = Field(
            None, description="", alias="project"
        )  # relationship
        model: Optional[LookerModel] = Field(
            None, description="", alias="model"
        )  # relationship
        fields: Optional[list[LookerField]] = Field(
            None, description="", alias="fields"
        )  # relationship

    attributes: "LookerExplore.Attributes" = Field(
        default_factory=lambda: LookerExplore.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerProject(Looker):
    """Description"""

    type_name: str = Field("LookerProject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerProject":
            raise ValueError("must be LookerProject")
        return v

    def __setattr__(self, name, value):
        if name in LookerProject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODELS: ClassVar[RelationField] = RelationField("models")
    """
    TBC
    """
    EXPLORES: ClassVar[RelationField] = RelationField("explores")
    """
    TBC
    """
    FIELDS: ClassVar[RelationField] = RelationField("fields")
    """
    TBC
    """
    VIEWS: ClassVar[RelationField] = RelationField("views")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "models",
        "explores",
        "fields",
        "views",
    ]

    @property
    def models(self) -> Optional[list[LookerModel]]:
        return None if self.attributes is None else self.attributes.models

    @models.setter
    def models(self, models: Optional[list[LookerModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.models = models

    @property
    def explores(self) -> Optional[list[LookerExplore]]:
        return None if self.attributes is None else self.attributes.explores

    @explores.setter
    def explores(self, explores: Optional[list[LookerExplore]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.explores = explores

    @property
    def fields(self) -> Optional[list[LookerField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[list[LookerField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    @property
    def views(self) -> Optional[list[LookerView]]:
        return None if self.attributes is None else self.attributes.views

    @views.setter
    def views(self, views: Optional[list[LookerView]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.views = views

    class Attributes(Looker.Attributes):
        models: Optional[list[LookerModel]] = Field(
            None, description="", alias="models"
        )  # relationship
        explores: Optional[list[LookerExplore]] = Field(
            None, description="", alias="explores"
        )  # relationship
        fields: Optional[list[LookerField]] = Field(
            None, description="", alias="fields"
        )  # relationship
        views: Optional[list[LookerView]] = Field(
            None, description="", alias="views"
        )  # relationship

    attributes: "LookerProject.Attributes" = Field(
        default_factory=lambda: LookerProject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerQuery(Looker):
    """Description"""

    type_name: str = Field("LookerQuery", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerQuery":
            raise ValueError("must be LookerQuery")
        return v

    def __setattr__(self, name, value):
        if name in LookerQuery._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SOURCE_DEFINITION: ClassVar[KeywordField] = KeywordField(
        "sourceDefinition", "sourceDefinition"
    )
    """
    TBC
    """
    SOURCE_DEFINITION_DATABASE: ClassVar[KeywordField] = KeywordField(
        "sourceDefinitionDatabase", "sourceDefinitionDatabase"
    )
    """
    TBC
    """
    SOURCE_DEFINITION_SCHEMA: ClassVar[KeywordField] = KeywordField(
        "sourceDefinitionSchema", "sourceDefinitionSchema"
    )
    """
    TBC
    """
    FIELDS: ClassVar[KeywordField] = KeywordField("fields", "fields")
    """
    TBC
    """

    TILES: ClassVar[RelationField] = RelationField("tiles")
    """
    TBC
    """
    LOOKS: ClassVar[RelationField] = RelationField("looks")
    """
    TBC
    """
    MODEL: ClassVar[RelationField] = RelationField("model")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "source_definition",
        "source_definition_database",
        "source_definition_schema",
        "fields",
        "tiles",
        "looks",
        "model",
    ]

    @property
    def source_definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_definition

    @source_definition.setter
    def source_definition(self, source_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_definition = source_definition

    @property
    def source_definition_database(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_definition_database
        )

    @source_definition_database.setter
    def source_definition_database(self, source_definition_database: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_definition_database = source_definition_database

    @property
    def source_definition_schema(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_definition_schema
        )

    @source_definition_schema.setter
    def source_definition_schema(self, source_definition_schema: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_definition_schema = source_definition_schema

    @property
    def fields(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    @property
    def tiles(self) -> Optional[list[LookerTile]]:
        return None if self.attributes is None else self.attributes.tiles

    @tiles.setter
    def tiles(self, tiles: Optional[list[LookerTile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tiles = tiles

    @property
    def looks(self) -> Optional[list[LookerLook]]:
        return None if self.attributes is None else self.attributes.looks

    @looks.setter
    def looks(self, looks: Optional[list[LookerLook]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looks = looks

    @property
    def model(self) -> Optional[LookerModel]:
        return None if self.attributes is None else self.attributes.model

    @model.setter
    def model(self, model: Optional[LookerModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model = model

    class Attributes(Looker.Attributes):
        source_definition: Optional[str] = Field(
            None, description="", alias="sourceDefinition"
        )
        source_definition_database: Optional[str] = Field(
            None, description="", alias="sourceDefinitionDatabase"
        )
        source_definition_schema: Optional[str] = Field(
            None, description="", alias="sourceDefinitionSchema"
        )
        fields: Optional[set[str]] = Field(None, description="", alias="fields")
        tiles: Optional[list[LookerTile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        looks: Optional[list[LookerLook]] = Field(
            None, description="", alias="looks"
        )  # relationship
        model: Optional[LookerModel] = Field(
            None, description="", alias="model"
        )  # relationship

    attributes: "LookerQuery.Attributes" = Field(
        default_factory=lambda: LookerQuery.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerField(Looker):
    """Description"""

    type_name: str = Field("LookerField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerField":
            raise ValueError("must be LookerField")
        return v

    def __setattr__(self, name, value):
        if name in LookerField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PROJECT_NAME: ClassVar[KeywordField] = KeywordField("projectName", "projectName")
    """
    TBC
    """
    LOOKER_EXPLORE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "lookerExploreQualifiedName",
        "lookerExploreQualifiedName",
        "lookerExploreQualifiedName.text",
    )
    """
    TBC
    """
    LOOKER_VIEW_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "lookerViewQualifiedName",
        "lookerViewQualifiedName",
        "lookerViewQualifiedName.text",
    )
    """
    TBC
    """
    MODEL_NAME: ClassVar[KeywordField] = KeywordField("modelName", "modelName")
    """
    TBC
    """
    SOURCE_DEFINITION: ClassVar[KeywordField] = KeywordField(
        "sourceDefinition", "sourceDefinition"
    )
    """
    TBC
    """
    LOOKER_FIELD_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "lookerFieldDataType", "lookerFieldDataType"
    )
    """
    TBC
    """
    LOOKER_TIMES_USED: ClassVar[NumericField] = NumericField(
        "lookerTimesUsed", "lookerTimesUsed"
    )
    """
    TBC
    """

    EXPLORE: ClassVar[RelationField] = RelationField("explore")
    """
    TBC
    """
    PROJECT: ClassVar[RelationField] = RelationField("project")
    """
    TBC
    """
    VIEW: ClassVar[RelationField] = RelationField("view")
    """
    TBC
    """
    MODEL: ClassVar[RelationField] = RelationField("model")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "project_name",
        "looker_explore_qualified_name",
        "looker_view_qualified_name",
        "model_name",
        "source_definition",
        "looker_field_data_type",
        "looker_times_used",
        "explore",
        "project",
        "view",
        "model",
    ]

    @property
    def project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.project_name

    @project_name.setter
    def project_name(self, project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_name = project_name

    @property
    def looker_explore_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.looker_explore_qualified_name
        )

    @looker_explore_qualified_name.setter
    def looker_explore_qualified_name(
        self, looker_explore_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_explore_qualified_name = looker_explore_qualified_name

    @property
    def looker_view_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.looker_view_qualified_name
        )

    @looker_view_qualified_name.setter
    def looker_view_qualified_name(self, looker_view_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_view_qualified_name = looker_view_qualified_name

    @property
    def model_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_name

    @model_name.setter
    def model_name(self, model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_name = model_name

    @property
    def source_definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_definition

    @source_definition.setter
    def source_definition(self, source_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_definition = source_definition

    @property
    def looker_field_data_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.looker_field_data_type
        )

    @looker_field_data_type.setter
    def looker_field_data_type(self, looker_field_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_field_data_type = looker_field_data_type

    @property
    def looker_times_used(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.looker_times_used

    @looker_times_used.setter
    def looker_times_used(self, looker_times_used: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_times_used = looker_times_used

    @property
    def explore(self) -> Optional[LookerExplore]:
        return None if self.attributes is None else self.attributes.explore

    @explore.setter
    def explore(self, explore: Optional[LookerExplore]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.explore = explore

    @property
    def project(self) -> Optional[LookerProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[LookerProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def view(self) -> Optional[LookerView]:
        return None if self.attributes is None else self.attributes.view

    @view.setter
    def view(self, view: Optional[LookerView]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view = view

    @property
    def model(self) -> Optional[LookerModel]:
        return None if self.attributes is None else self.attributes.model

    @model.setter
    def model(self, model: Optional[LookerModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model = model

    class Attributes(Looker.Attributes):
        project_name: Optional[str] = Field(None, description="", alias="projectName")
        looker_explore_qualified_name: Optional[str] = Field(
            None, description="", alias="lookerExploreQualifiedName"
        )
        looker_view_qualified_name: Optional[str] = Field(
            None, description="", alias="lookerViewQualifiedName"
        )
        model_name: Optional[str] = Field(None, description="", alias="modelName")
        source_definition: Optional[str] = Field(
            None, description="", alias="sourceDefinition"
        )
        looker_field_data_type: Optional[str] = Field(
            None, description="", alias="lookerFieldDataType"
        )
        looker_times_used: Optional[int] = Field(
            None, description="", alias="lookerTimesUsed"
        )
        explore: Optional[LookerExplore] = Field(
            None, description="", alias="explore"
        )  # relationship
        project: Optional[LookerProject] = Field(
            None, description="", alias="project"
        )  # relationship
        view: Optional[LookerView] = Field(
            None, description="", alias="view"
        )  # relationship
        model: Optional[LookerModel] = Field(
            None, description="", alias="model"
        )  # relationship

    attributes: "LookerField.Attributes" = Field(
        default_factory=lambda: LookerField.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class LookerView(Looker):
    """Description"""

    type_name: str = Field("LookerView", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerView":
            raise ValueError("must be LookerView")
        return v

    def __setattr__(self, name, value):
        if name in LookerView._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PROJECT_NAME: ClassVar[KeywordField] = KeywordField("projectName", "projectName")
    """
    TBC
    """
    LOOKER_VIEW_FILE_PATH: ClassVar[KeywordField] = KeywordField(
        "lookerViewFilePath", "lookerViewFilePath"
    )
    """
    File path of the looker view in the project
    """
    LOOKER_VIEW_FILE_NAME: ClassVar[KeywordField] = KeywordField(
        "lookerViewFileName", "lookerViewFileName"
    )
    """
    File name of the looker view in the project
    """

    PROJECT: ClassVar[RelationField] = RelationField("project")
    """
    TBC
    """
    FIELDS: ClassVar[RelationField] = RelationField("fields")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "project_name",
        "looker_view_file_path",
        "looker_view_file_name",
        "project",
        "fields",
    ]

    @property
    def project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.project_name

    @project_name.setter
    def project_name(self, project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_name = project_name

    @property
    def looker_view_file_path(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.looker_view_file_path
        )

    @looker_view_file_path.setter
    def looker_view_file_path(self, looker_view_file_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_view_file_path = looker_view_file_path

    @property
    def looker_view_file_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.looker_view_file_name
        )

    @looker_view_file_name.setter
    def looker_view_file_name(self, looker_view_file_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_view_file_name = looker_view_file_name

    @property
    def project(self) -> Optional[LookerProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[LookerProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def fields(self) -> Optional[list[LookerField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[list[LookerField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    class Attributes(Looker.Attributes):
        project_name: Optional[str] = Field(None, description="", alias="projectName")
        looker_view_file_path: Optional[str] = Field(
            None, description="", alias="lookerViewFilePath"
        )
        looker_view_file_name: Optional[str] = Field(
            None, description="", alias="lookerViewFileName"
        )
        project: Optional[LookerProject] = Field(
            None, description="", alias="project"
        )  # relationship
        fields: Optional[list[LookerField]] = Field(
            None, description="", alias="fields"
        )  # relationship

    attributes: "LookerView.Attributes" = Field(
        default_factory=lambda: LookerView.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


LookerLook.Attributes.update_forward_refs()


LookerDashboard.Attributes.update_forward_refs()


LookerFolder.Attributes.update_forward_refs()


LookerTile.Attributes.update_forward_refs()


LookerModel.Attributes.update_forward_refs()


LookerExplore.Attributes.update_forward_refs()


LookerProject.Attributes.update_forward_refs()


LookerQuery.Attributes.update_forward_refs()


LookerField.Attributes.update_forward_refs()


LookerView.Attributes.update_forward_refs()
