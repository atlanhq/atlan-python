# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .metabase import Metabase


class MetabaseCollection(Metabase):
    """Description"""

    type_name: str = Field(default="MetabaseCollection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MetabaseCollection":
            raise ValueError("must be MetabaseCollection")
        return v

    def __setattr__(self, name, value):
        if name in MetabaseCollection._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    METABASE_SLUG: ClassVar[KeywordTextField] = KeywordTextField(
        "metabaseSlug", "metabaseSlug", "metabaseSlug.text"
    )
    """

    """
    METABASE_COLOR: ClassVar[KeywordField] = KeywordField(
        "metabaseColor", "metabaseColor"
    )
    """

    """
    METABASE_NAMESPACE: ClassVar[KeywordTextField] = KeywordTextField(
        "metabaseNamespace", "metabaseNamespace", "metabaseNamespace.text"
    )
    """

    """
    METABASE_IS_PERSONAL_COLLECTION: ClassVar[BooleanField] = BooleanField(
        "metabaseIsPersonalCollection", "metabaseIsPersonalCollection"
    )
    """

    """

    METABASE_DASHBOARDS: ClassVar[RelationField] = RelationField("metabaseDashboards")
    """
    TBC
    """
    METABASE_QUESTIONS: ClassVar[RelationField] = RelationField("metabaseQuestions")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "metabase_slug",
        "metabase_color",
        "metabase_namespace",
        "metabase_is_personal_collection",
        "metabase_dashboards",
        "metabase_questions",
    ]

    @property
    def metabase_slug(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_slug

    @metabase_slug.setter
    def metabase_slug(self, metabase_slug: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_slug = metabase_slug

    @property
    def metabase_color(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_color

    @metabase_color.setter
    def metabase_color(self, metabase_color: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_color = metabase_color

    @property
    def metabase_namespace(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_namespace

    @metabase_namespace.setter
    def metabase_namespace(self, metabase_namespace: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_namespace = metabase_namespace

    @property
    def metabase_is_personal_collection(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.metabase_is_personal_collection
        )

    @metabase_is_personal_collection.setter
    def metabase_is_personal_collection(
        self, metabase_is_personal_collection: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_is_personal_collection = (
            metabase_is_personal_collection
        )

    @property
    def metabase_dashboards(self) -> Optional[List[MetabaseDashboard]]:
        return None if self.attributes is None else self.attributes.metabase_dashboards

    @metabase_dashboards.setter
    def metabase_dashboards(
        self, metabase_dashboards: Optional[List[MetabaseDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_dashboards = metabase_dashboards

    @property
    def metabase_questions(self) -> Optional[List[MetabaseQuestion]]:
        return None if self.attributes is None else self.attributes.metabase_questions

    @metabase_questions.setter
    def metabase_questions(self, metabase_questions: Optional[List[MetabaseQuestion]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_questions = metabase_questions

    class Attributes(Metabase.Attributes):
        metabase_slug: Optional[str] = Field(default=None, description="")
        metabase_color: Optional[str] = Field(default=None, description="")
        metabase_namespace: Optional[str] = Field(default=None, description="")
        metabase_is_personal_collection: Optional[bool] = Field(
            default=None, description=""
        )
        metabase_dashboards: Optional[List[MetabaseDashboard]] = Field(
            default=None, description=""
        )  # relationship
        metabase_questions: Optional[List[MetabaseQuestion]] = Field(
            default=None, description=""
        )  # relationship

    attributes: MetabaseCollection.Attributes = Field(
        default_factory=lambda: MetabaseCollection.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .metabase_dashboard import MetabaseDashboard  # noqa
from .metabase_question import MetabaseQuestion  # noqa
