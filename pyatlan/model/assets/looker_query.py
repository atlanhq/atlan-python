# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .looker import Looker


class LookerQuery(Looker):
    """Description"""

    type_name: str = Field(default="LookerQuery", allow_mutation=False)

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
    Deprecated.
    """
    SOURCE_DEFINITION_DATABASE: ClassVar[KeywordField] = KeywordField(
        "sourceDefinitionDatabase", "sourceDefinitionDatabase"
    )
    """
    Deprecated.
    """
    SOURCE_DEFINITION_SCHEMA: ClassVar[KeywordField] = KeywordField(
        "sourceDefinitionSchema", "sourceDefinitionSchema"
    )
    """
    Deprecated.
    """
    FIELDS: ClassVar[KeywordField] = KeywordField("fields", "fields")
    """
    Deprecated.
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

    _convenience_properties: ClassVar[List[str]] = [
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
    def fields(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

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
    def model(self) -> Optional[LookerModel]:
        return None if self.attributes is None else self.attributes.model

    @model.setter
    def model(self, model: Optional[LookerModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model = model

    class Attributes(Looker.Attributes):
        source_definition: Optional[str] = Field(default=None, description="")
        source_definition_database: Optional[str] = Field(default=None, description="")
        source_definition_schema: Optional[str] = Field(default=None, description="")
        fields: Optional[Set[str]] = Field(default=None, description="")
        tiles: Optional[List[LookerTile]] = Field(
            default=None, description=""
        )  # relationship
        looks: Optional[List[LookerLook]] = Field(
            default=None, description=""
        )  # relationship
        model: Optional[LookerModel] = Field(
            default=None, description=""
        )  # relationship

    attributes: LookerQuery.Attributes = Field(
        default_factory=lambda: LookerQuery.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .looker_look import LookerLook  # noqa
from .looker_model import LookerModel  # noqa
from .looker_tile import LookerTile  # noqa
