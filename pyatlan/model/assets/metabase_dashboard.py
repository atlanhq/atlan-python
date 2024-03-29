# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .metabase import Metabase


class MetabaseDashboard(Metabase):
    """Description"""

    type_name: str = Field(default="MetabaseDashboard", allow_mutation=False)

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

    """

    METABASE_QUESTIONS: ClassVar[RelationField] = RelationField("metabaseQuestions")
    """
    TBC
    """
    METABASE_COLLECTION: ClassVar[RelationField] = RelationField("metabaseCollection")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
    def metabase_questions(self) -> Optional[List[MetabaseQuestion]]:
        return None if self.attributes is None else self.attributes.metabase_questions

    @metabase_questions.setter
    def metabase_questions(self, metabase_questions: Optional[List[MetabaseQuestion]]):
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
        metabase_question_count: Optional[int] = Field(default=None, description="")
        metabase_questions: Optional[List[MetabaseQuestion]] = Field(
            default=None, description=""
        )  # relationship
        metabase_collection: Optional[MetabaseCollection] = Field(
            default=None, description=""
        )  # relationship

    attributes: MetabaseDashboard.Attributes = Field(
        default_factory=lambda: MetabaseDashboard.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .metabase_collection import MetabaseCollection  # noqa
from .metabase_question import MetabaseQuestion  # noqa
