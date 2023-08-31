# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField, RelationField

from .asset45 import Thoughtspot


class ThoughtspotLiveboard(Thoughtspot):
    """Description"""

    type_name: str = Field("ThoughtspotLiveboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotLiveboard":
            raise ValueError("must be ThoughtspotLiveboard")
        return v

    def __setattr__(self, name, value):
        if name in ThoughtspotLiveboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    THOUGHTSPOT_DASHLETS: ClassVar[RelationField] = RelationField("thoughtspotDashlets")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "thoughtspot_dashlets",
    ]

    @property
    def thoughtspot_dashlets(self) -> Optional[list[ThoughtspotDashlet]]:
        return None if self.attributes is None else self.attributes.thoughtspot_dashlets

    @thoughtspot_dashlets.setter
    def thoughtspot_dashlets(
        self, thoughtspot_dashlets: Optional[list[ThoughtspotDashlet]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_dashlets = thoughtspot_dashlets

    class Attributes(Thoughtspot.Attributes):
        thoughtspot_dashlets: Optional[list[ThoughtspotDashlet]] = Field(
            None, description="", alias="thoughtspotDashlets"
        )  # relationship

    attributes: "ThoughtspotLiveboard.Attributes" = Field(
        default_factory=lambda: ThoughtspotLiveboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ThoughtspotDashlet(Thoughtspot):
    """Description"""

    type_name: str = Field("ThoughtspotDashlet", allow_mutation=False)

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
    TBC
    """
    THOUGHTSPOT_LIVEBOARD_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "thoughtspotLiveboardQualifiedName",
        "thoughtspotLiveboardQualifiedName",
        "thoughtspotLiveboardQualifiedName.text",
    )
    """
    TBC
    """

    THOUGHTSPOT_LIVEBOARD: ClassVar[RelationField] = RelationField(
        "thoughtspotLiveboard"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
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
        thoughtspot_liveboard_name: Optional[str] = Field(
            None, description="", alias="thoughtspotLiveboardName"
        )
        thoughtspot_liveboard_qualified_name: Optional[str] = Field(
            None, description="", alias="thoughtspotLiveboardQualifiedName"
        )
        thoughtspot_liveboard: Optional[ThoughtspotLiveboard] = Field(
            None, description="", alias="thoughtspotLiveboard"
        )  # relationship

    attributes: "ThoughtspotDashlet.Attributes" = Field(
        default_factory=lambda: ThoughtspotDashlet.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


ThoughtspotLiveboard.Attributes.update_forward_refs()


ThoughtspotDashlet.Attributes.update_forward_refs()
