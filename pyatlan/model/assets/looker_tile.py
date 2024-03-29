# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .looker import Looker


class LookerTile(Looker):
    """Description"""

    type_name: str = Field(default="LookerTile", allow_mutation=False)

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
    Identifier for the LoomML link.
    """
    MERGE_RESULT_ID: ClassVar[KeywordField] = KeywordField(
        "mergeResultId", "mergeResultId"
    )
    """
    Identifier for the merge result.
    """
    NOTE_TEXT: ClassVar[KeywordField] = KeywordField("noteText", "noteText")
    """
    Text of notes added to the tile.
    """
    QUERY_ID: ClassVar[NumericField] = NumericField("queryID", "queryID")
    """
    Identifier for the query used to build this tile, from Looker.
    """
    RESULT_MAKER_ID: ClassVar[NumericField] = NumericField(
        "resultMakerID", "resultMakerID"
    )
    """
    Identifier of the ResultMarkerLookup entry, from Looker.
    """
    SUBTITLE_TEXT: ClassVar[KeywordField] = KeywordField("subtitleText", "subtitleText")
    """
    Text for the subtitle for text tiles.
    """
    LOOK_ID: ClassVar[NumericField] = NumericField("lookId", "lookId")
    """
    Identifier of the Look used to create this tile, from Looker.
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

    _convenience_properties: ClassVar[List[str]] = [
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
        lookml_link_id: Optional[str] = Field(default=None, description="")
        merge_result_id: Optional[str] = Field(default=None, description="")
        note_text: Optional[str] = Field(default=None, description="")
        query_i_d: Optional[int] = Field(default=None, description="")
        result_maker_i_d: Optional[int] = Field(default=None, description="")
        subtitle_text: Optional[str] = Field(default=None, description="")
        look_id: Optional[int] = Field(default=None, description="")
        query: Optional[LookerQuery] = Field(
            default=None, description=""
        )  # relationship
        look: Optional[LookerLook] = Field(default=None, description="")  # relationship
        dashboard: Optional[LookerDashboard] = Field(
            default=None, description=""
        )  # relationship

    attributes: LookerTile.Attributes = Field(
        default_factory=lambda: LookerTile.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .looker_dashboard import LookerDashboard  # noqa
from .looker_look import LookerLook  # noqa
from .looker_query import LookerQuery  # noqa
