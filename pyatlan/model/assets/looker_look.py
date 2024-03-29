# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .looker import Looker


class LookerLook(Looker):
    """Description"""

    type_name: str = Field(default="LookerLook", allow_mutation=False)

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
    Name of the folder in which the Look is organized.
    """
    SOURCE_USER_ID: ClassVar[NumericField] = NumericField(
        "sourceUserId", "sourceUserId"
    )
    """
    Identifier of the user who created the Look, from Looker.
    """
    SOURCE_VIEW_COUNT: ClassVar[NumericField] = NumericField(
        "sourceViewCount", "sourceViewCount"
    )
    """
    Number of times the look has been viewed in the Looker web UI.
    """
    SOURCELAST_UPDATER_ID: ClassVar[NumericField] = NumericField(
        "sourcelastUpdaterId", "sourcelastUpdaterId"
    )
    """
    Identifier of the user that last updated the Look, from Looker.
    """
    SOURCE_LAST_ACCESSED_AT: ClassVar[NumericField] = NumericField(
        "sourceLastAccessedAt", "sourceLastAccessedAt"
    )
    """
    Time (epoch) when the Look was last accessed by a user, in milliseconds.
    """
    SOURCE_LAST_VIEWED_AT: ClassVar[NumericField] = NumericField(
        "sourceLastViewedAt", "sourceLastViewedAt"
    )
    """
    Time (epoch) when the Look was last viewed by a user, in milliseconds.
    """
    SOURCE_CONTENT_METADATA_ID: ClassVar[NumericField] = NumericField(
        "sourceContentMetadataId", "sourceContentMetadataId"
    )
    """
    Identifier of the Look's content metadata, from Looker.
    """
    SOURCE_QUERY_ID: ClassVar[NumericField] = NumericField(
        "sourceQueryId", "sourceQueryId"
    )
    """
    Identifier of the query for the Look, from Looker.
    """
    MODEL_NAME: ClassVar[KeywordField] = KeywordField("modelName", "modelName")
    """
    Name of the model in which this Look exists.
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

    _convenience_properties: ClassVar[List[str]] = [
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
        folder_name: Optional[str] = Field(default=None, description="")
        source_user_id: Optional[int] = Field(default=None, description="")
        source_view_count: Optional[int] = Field(default=None, description="")
        sourcelast_updater_id: Optional[int] = Field(default=None, description="")
        source_last_accessed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        source_last_viewed_at: Optional[datetime] = Field(default=None, description="")
        source_content_metadata_id: Optional[int] = Field(default=None, description="")
        source_query_id: Optional[int] = Field(default=None, description="")
        model_name: Optional[str] = Field(default=None, description="")
        query: Optional[LookerQuery] = Field(
            default=None, description=""
        )  # relationship
        folder: Optional[LookerFolder] = Field(
            default=None, description=""
        )  # relationship
        tile: Optional[LookerTile] = Field(default=None, description="")  # relationship
        model: Optional[LookerModel] = Field(
            default=None, description=""
        )  # relationship
        dashboard: Optional[LookerDashboard] = Field(
            default=None, description=""
        )  # relationship

    attributes: LookerLook.Attributes = Field(
        default_factory=lambda: LookerLook.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .looker_dashboard import LookerDashboard  # noqa
from .looker_folder import LookerFolder  # noqa
from .looker_model import LookerModel  # noqa
from .looker_query import LookerQuery  # noqa
from .looker_tile import LookerTile  # noqa
