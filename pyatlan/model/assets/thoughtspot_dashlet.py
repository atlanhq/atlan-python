# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField, RelationField

from .thoughtspot import Thoughtspot


class ThoughtspotDashlet(Thoughtspot):
    """Description"""

    type_name: str = Field(default="ThoughtspotDashlet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotDashlet":
            raise ValueError("must be ThoughtspotDashlet")
        return v

    def __setattr__(self, name, value):
        if name in ThoughtspotDashlet._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    THOUGHTSPOT_LIVEBOARD_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "thoughtspotLiveboardName",
        "thoughtspotLiveboardName.keyword",
        "thoughtspotLiveboardName",
    )
    """
    Simple name of the liveboard in which this dashlet exists.
    """
    THOUGHTSPOT_LIVEBOARD_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "thoughtspotLiveboardQualifiedName",
        "thoughtspotLiveboardQualifiedName",
        "thoughtspotLiveboardQualifiedName.text",
    )
    """
    Unique name of the liveboard in which this dashlet exists.
    """

    THOUGHTSPOT_LIVEBOARD: ClassVar[RelationField] = RelationField(
        "thoughtspotLiveboard"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "thoughtspot_liveboard_name",
        "thoughtspot_liveboard_qualified_name",
        "thoughtspot_liveboard",
    ]

    @property
    def thoughtspot_liveboard_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.thoughtspot_liveboard_name
        )

    @thoughtspot_liveboard_name.setter
    def thoughtspot_liveboard_name(self, thoughtspot_liveboard_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_liveboard_name = thoughtspot_liveboard_name

    @property
    def thoughtspot_liveboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.thoughtspot_liveboard_qualified_name
        )

    @thoughtspot_liveboard_qualified_name.setter
    def thoughtspot_liveboard_qualified_name(
        self, thoughtspot_liveboard_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_liveboard_qualified_name = (
            thoughtspot_liveboard_qualified_name
        )

    @property
    def thoughtspot_liveboard(self) -> Optional[ThoughtspotLiveboard]:
        return (
            None if self.attributes is None else self.attributes.thoughtspot_liveboard
        )

    @thoughtspot_liveboard.setter
    def thoughtspot_liveboard(
        self, thoughtspot_liveboard: Optional[ThoughtspotLiveboard]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_liveboard = thoughtspot_liveboard

    class Attributes(Thoughtspot.Attributes):
        thoughtspot_liveboard_name: Optional[str] = Field(default=None, description="")
        thoughtspot_liveboard_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        thoughtspot_liveboard: Optional[ThoughtspotLiveboard] = Field(
            default=None, description=""
        )  # relationship

    attributes: ThoughtspotDashlet.Attributes = Field(
        default_factory=lambda: ThoughtspotDashlet.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .thoughtspot_liveboard import ThoughtspotLiveboard  # noqa
