# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .asset43 import Metabase


class MetabaseQuestion(Metabase):
    """Description"""

    type_name: str = Field("MetabaseQuestion", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MetabaseQuestion":
            raise ValueError("must be MetabaseQuestion")
        return v

    def __setattr__(self, name, value):
        if name in MetabaseQuestion._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    METABASE_DASHBOARD_COUNT: ClassVar[NumericField] = NumericField(
        "metabaseDashboardCount", "metabaseDashboardCount"
    )
    """
    TBC
    """
    METABASE_QUERY_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "metabaseQueryType", "metabaseQueryType", "metabaseQueryType.text"
    )
    """
    TBC
    """
    METABASE_QUERY: ClassVar[KeywordTextField] = KeywordTextField(
        "metabaseQuery", "metabaseQuery.keyword", "metabaseQuery"
    )
    """
    TBC
    """

    METABASE_DASHBOARDS: ClassVar[RelationField] = RelationField("metabaseDashboards")
    """
    TBC
    """
    METABASE_COLLECTION: ClassVar[RelationField] = RelationField("metabaseCollection")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "metabase_dashboard_count",
        "metabase_query_type",
        "metabase_query",
        "metabase_dashboards",
        "metabase_collection",
    ]

    @property
    def metabase_dashboard_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.metabase_dashboard_count
        )

    @metabase_dashboard_count.setter
    def metabase_dashboard_count(self, metabase_dashboard_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_dashboard_count = metabase_dashboard_count

    @property
    def metabase_query_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_query_type

    @metabase_query_type.setter
    def metabase_query_type(self, metabase_query_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_query_type = metabase_query_type

    @property
    def metabase_query(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metabase_query

    @metabase_query.setter
    def metabase_query(self, metabase_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_query = metabase_query

    @property
    def metabase_dashboards(self) -> Optional[list[MetabaseDashboard]]:
        return None if self.attributes is None else self.attributes.metabase_dashboards

    @metabase_dashboards.setter
    def metabase_dashboards(
        self, metabase_dashboards: Optional[list[MetabaseDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_dashboards = metabase_dashboards

    @property
    def metabase_collection(self) -> Optional[MetabaseCollection]:
        return None if self.attributes is None else self.attributes.metabase_collection

    @metabase_collection.setter
    def metabase_collection(self, metabase_collection: Optional[MetabaseCollection]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_collection = metabase_collection

    class Attributes(Metabase.Attributes):
        metabase_dashboard_count: Optional[int] = Field(
            None, description="", alias="metabaseDashboardCount"
        )
        metabase_query_type: Optional[str] = Field(
            None, description="", alias="metabaseQueryType"
        )
        metabase_query: Optional[str] = Field(
            None, description="", alias="metabaseQuery"
        )
        metabase_dashboards: Optional[list[MetabaseDashboard]] = Field(
            None, description="", alias="metabaseDashboards"
        )  # relationship
        metabase_collection: Optional[MetabaseCollection] = Field(
            None, description="", alias="metabaseCollection"
        )  # relationship

    attributes: "MetabaseQuestion.Attributes" = Field(
        default_factory=lambda: MetabaseQuestion.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MetabaseCollection(Metabase):
    """Description"""

    type_name: str = Field("MetabaseCollection", allow_mutation=False)

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
    TBC
    """
    METABASE_COLOR: ClassVar[KeywordField] = KeywordField(
        "metabaseColor", "metabaseColor"
    )
    """
    TBC
    """
    METABASE_NAMESPACE: ClassVar[KeywordTextField] = KeywordTextField(
        "metabaseNamespace", "metabaseNamespace", "metabaseNamespace.text"
    )
    """
    TBC
    """
    METABASE_IS_PERSONAL_COLLECTION: ClassVar[BooleanField] = BooleanField(
        "metabaseIsPersonalCollection", "metabaseIsPersonalCollection"
    )
    """
    TBC
    """

    METABASE_DASHBOARDS: ClassVar[RelationField] = RelationField("metabaseDashboards")
    """
    TBC
    """
    METABASE_QUESTIONS: ClassVar[RelationField] = RelationField("metabaseQuestions")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
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
    def metabase_dashboards(self) -> Optional[list[MetabaseDashboard]]:
        return None if self.attributes is None else self.attributes.metabase_dashboards

    @metabase_dashboards.setter
    def metabase_dashboards(
        self, metabase_dashboards: Optional[list[MetabaseDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_dashboards = metabase_dashboards

    @property
    def metabase_questions(self) -> Optional[list[MetabaseQuestion]]:
        return None if self.attributes is None else self.attributes.metabase_questions

    @metabase_questions.setter
    def metabase_questions(self, metabase_questions: Optional[list[MetabaseQuestion]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_questions = metabase_questions

    class Attributes(Metabase.Attributes):
        metabase_slug: Optional[str] = Field(None, description="", alias="metabaseSlug")
        metabase_color: Optional[str] = Field(
            None, description="", alias="metabaseColor"
        )
        metabase_namespace: Optional[str] = Field(
            None, description="", alias="metabaseNamespace"
        )
        metabase_is_personal_collection: Optional[bool] = Field(
            None, description="", alias="metabaseIsPersonalCollection"
        )
        metabase_dashboards: Optional[list[MetabaseDashboard]] = Field(
            None, description="", alias="metabaseDashboards"
        )  # relationship
        metabase_questions: Optional[list[MetabaseQuestion]] = Field(
            None, description="", alias="metabaseQuestions"
        )  # relationship

    attributes: "MetabaseCollection.Attributes" = Field(
        default_factory=lambda: MetabaseCollection.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MetabaseDashboard(Metabase):
    """Description"""

    type_name: str = Field("MetabaseDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MetabaseDashboard":
            raise ValueError("must be MetabaseDashboard")
        return v

    def __setattr__(self, name, value):
        if name in MetabaseDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    METABASE_QUESTION_COUNT: ClassVar[NumericField] = NumericField(
        "metabaseQuestionCount", "metabaseQuestionCount"
    )
    """
    TBC
    """

    METABASE_QUESTIONS: ClassVar[RelationField] = RelationField("metabaseQuestions")
    """
    TBC
    """
    METABASE_COLLECTION: ClassVar[RelationField] = RelationField("metabaseCollection")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "metabase_question_count",
        "metabase_questions",
        "metabase_collection",
    ]

    @property
    def metabase_question_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.metabase_question_count
        )

    @metabase_question_count.setter
    def metabase_question_count(self, metabase_question_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_question_count = metabase_question_count

    @property
    def metabase_questions(self) -> Optional[list[MetabaseQuestion]]:
        return None if self.attributes is None else self.attributes.metabase_questions

    @metabase_questions.setter
    def metabase_questions(self, metabase_questions: Optional[list[MetabaseQuestion]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_questions = metabase_questions

    @property
    def metabase_collection(self) -> Optional[MetabaseCollection]:
        return None if self.attributes is None else self.attributes.metabase_collection

    @metabase_collection.setter
    def metabase_collection(self, metabase_collection: Optional[MetabaseCollection]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_collection = metabase_collection

    class Attributes(Metabase.Attributes):
        metabase_question_count: Optional[int] = Field(
            None, description="", alias="metabaseQuestionCount"
        )
        metabase_questions: Optional[list[MetabaseQuestion]] = Field(
            None, description="", alias="metabaseQuestions"
        )  # relationship
        metabase_collection: Optional[MetabaseCollection] = Field(
            None, description="", alias="metabaseCollection"
        )  # relationship

    attributes: "MetabaseDashboard.Attributes" = Field(
        default_factory=lambda: MetabaseDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


MetabaseQuestion.Attributes.update_forward_refs()


MetabaseCollection.Attributes.update_forward_refs()


MetabaseDashboard.Attributes.update_forward_refs()
