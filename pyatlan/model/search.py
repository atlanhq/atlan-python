# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/elastic/elasticsearch-dsl-py.git (under Apache-2.0 license)
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from itertools import chain
from typing import TYPE_CHECKING, Any, Literal, Optional, Union

from pydantic import (
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    validate_arguments,
    validator,
)

from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlanConnectorType, SortOrder

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass

import copy

SearchFieldType = Union[StrictStr, StrictInt, StrictFloat, StrictBool, datetime]


class Attributes(str, Enum):
    attribute_type: type

    def __new__(cls, value: str, attribute_type: type) -> "Attributes":
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.attribute_type = attribute_type
        return obj


class TermAttributes(Attributes):

    CONNECTOR_NAME = ("connectorName", AtlanConnectorType)
    CATEGORIES = ("__categories", StrictStr)
    CREATE_TIME_AS_TIMESTAMP = ("__timestamp", datetime)
    CREATED_BY = ("__createdBy", StrictStr)
    GLOSSARY = ("__glossary", StrictStr)
    GUID = ("__guid", StrictStr)
    HAS_LINEAGE = ("__hasLineage", StrictBool)
    MEANINGS = ("__meanings", StrictStr)
    MODIFIED_BY = ("__modifiedBy", StrictStr)
    NAME = ("name.keyword", StrictStr)
    OWNER_GROUPS = ("ownerGroups", StrictStr)
    OWNER_USERS = ("ownerUsers", StrictStr)
    PARENT_CATEGORY = ("__parentCategory", StrictStr)
    POPULARITY_SCORE = ("popularityScore", float)
    QUALIFIED_NAME = ("qualifiedName", StrictStr)
    STATE = ("__state", Literal["ACTIVE", "DELETED"])
    SUPER_TYPE_NAMES = ("__superTypeNames.keyword", StrictStr)
    TYPE_NAME = ("__typeName.keyword", StrictStr)
    UPDATE_TIME_AS_TIMESTAMP = ("__modificationTimestamp", datetime)


class TextAttributes(Attributes):
    CLASSIFICATION_NAMES = ("__classificationNames", StrictStr)
    CLASSIFICATIONS_TEXT = ("__classificationsText", StrictStr)
    CREATE_TIME_AS_DATE = ("__timestamp.date", StrictStr)
    DESCRIPTION = ("description", StrictStr)
    MEANINGS_TEXT = ("__meaningsText", StrictStr)
    NAME = ("name", StrictStr)
    QUALIFIED_NAME = ("qualifiedName.text", StrictStr)
    PROPAGATED_CLASSIFICATION_NAMES = ("__propagatedClassificationNames", StrictStr)
    PROPAGATED_TRAIT_NAMES = ("__propagatedTraitNames", StrictStr)
    SUPER_TYPE_NAMES = ("__superTypeNames", StrictStr)
    TRAIT_NAMES = ("__traitNames", StrictStr)
    UPDATE_TIME_AS_DATE = ("__modificationTimestamp.date", StrictStr)
    USER_DESCRIPTION = ("userDescription", StrictStr)


def get_with_string(attribute: TermAttributes):
    @validate_arguments()
    def with_string(cls, value: StrictStr):
        """This function returns a string"""
        return cls(field=attribute.value, value=value)

    return with_string


@dataclass
class Query(ABC):
    def __add__(self, other):
        # make sure we give queries that know how to combine themselves
        # preference
        if hasattr(other, "__radd__"):
            return other.__radd__(self)
        return Bool(must=[self, other])

    def __and__(self, other):
        # make sure we give queries that know how to combine themselves
        # preference
        if hasattr(other, "__rand__"):
            return other.__rand__(self)
        return Bool(must=[self, other])

    def __or__(self, other):
        # make sure we give queries that know how to combine themselves
        # preference
        if hasattr(other, "__ror__"):
            return other.__ror__(self)
        return Bool(should=[self, other])

    def __invert__(self):
        return Bool(must_not=[self])

    def _clone(self):
        return copy.deepcopy(self)

    @abstractmethod
    def to_dict(self) -> dict[Any, Any]:
        ...


@dataclass(config=ConfigDict(smart_union=True, extra="forbid"))  # type: ignore
class MatchAll(Query):
    type_name: Literal["match_all"] = "match_all"
    boost: Optional[float] = None

    def __add__(self, other):
        return other._clone()

    __and__ = __rand__ = __radd__ = __add__

    def __or__(self, other):
        return self

    __ror__ = __or__

    def __invert__(self):
        return MatchNone()

    def to_dict(self) -> dict[Any, Any]:
        value = {"boost": self.boost} if self.boost else {}
        return {self.type_name: value}


EMPTY_QUERY = MatchAll()


@dataclass(config=ConfigDict(smart_union=True, extra="forbid"))  # type: ignore
class MatchNone(Query):
    type_name: Literal["match_none"] = "match_none"

    def __add__(self, other):
        return self

    __and__ = __rand__ = __radd__ = __add__

    def __or__(self, other):
        return other._clone()

    __ror__ = __or__

    def __invert__(self):
        return MatchAll()

    def to_dict(self) -> dict[Any, Any]:
        return {"match_none": {}}


@dataclass(config=ConfigDict(smart_union=True, extra="forbid"))  # type: ignore
class Exists(Query):
    field: str
    type_name: Literal["exists"] = "exists"

    @classmethod
    @validate_arguments()
    def with_categories(cls):
        return cls(field=TermAttributes.CATEGORIES.value)

    @classmethod
    @validate_arguments()
    def with_classification_names(cls):
        return cls(field=TextAttributes.CLASSIFICATION_NAMES.value)

    @classmethod
    @validate_arguments()
    def with_classifications_text(cls):
        return cls(field=TextAttributes.CLASSIFICATIONS_TEXT.value)

    @classmethod
    @validate_arguments()
    def with_connector_name(cls):
        return cls(field=TermAttributes.CONNECTOR_NAME.value)

    @classmethod
    @validate_arguments()
    def with_created_by(cls):
        return cls(field=TermAttributes.CREATED_BY.value)

    @classmethod
    @validate_arguments()
    def with_description(cls):
        return cls(field=TextAttributes.DESCRIPTION.value)

    @classmethod
    @validate_arguments()
    def with_glossary(cls):
        return cls(field=TermAttributes.GLOSSARY.value)

    @classmethod
    @validate_arguments()
    def with_guid(cls):
        # Use a GUID as a Query Term
        return cls(field=TermAttributes.GUID.value)

    @classmethod
    @validate_arguments()
    def with_has_lineage(cls):
        # Use a GUID as a Query Term
        return cls(field=TermAttributes.HAS_LINEAGE.value)

    @classmethod
    @validate_arguments()
    def with_meanings(cls):
        return cls(field=TermAttributes.MEANINGS.value)

    @classmethod
    @validate_arguments()
    def with_meanings_text(cls):
        return cls(field=TextAttributes.MEANINGS_TEXT.value)

    @classmethod
    @validate_arguments()
    def with_update_time_as_timestamp(cls):
        return cls(field=TermAttributes.UPDATE_TIME_AS_TIMESTAMP.value)

    @classmethod
    @validate_arguments()
    def with_modified_by(cls):
        return cls(field=TermAttributes.MODIFIED_BY.value)

    @classmethod
    @validate_arguments()
    def with_name(cls):
        return cls(field=TermAttributes.NAME.value)

    @classmethod
    @validate_arguments()
    def with_owner_users(cls):
        return cls(field=TermAttributes.OWNER_USERS.value)

    @classmethod
    @validate_arguments()
    def with_parent_category(cls):
        return cls(field=TermAttributes.PARENT_CATEGORY.value)

    @classmethod
    @validate_arguments()
    def with_popularity_score(cls):
        return cls(field=TermAttributes.POPULARITY_SCORE.value)

    @classmethod
    @validate_arguments()
    def with_propagated_classification_names(cls):
        return cls(field=TextAttributes.PROPAGATED_CLASSIFICATION_NAMES.value)

    @classmethod
    @validate_arguments()
    def with_propagated_trait_names(cls):
        return cls(field=TextAttributes.PROPAGATED_TRAIT_NAMES.value)

    @classmethod
    @validate_arguments()
    def with_qualified_name(cls):
        return cls(field=TermAttributes.QUALIFIED_NAME.value)

    @classmethod
    @validate_arguments()
    def with_super_type_names(cls):
        return cls(field=TermAttributes.SUPER_TYPE_NAMES.value)

    @classmethod
    @validate_arguments()
    def with_state(cls):
        return cls(field=TermAttributes.STATE.value)

    @classmethod
    @validate_arguments()
    def with_owner_groups(cls):
        return cls(field=TermAttributes.OWNER_GROUPS.value)

    @classmethod
    @validate_arguments()
    def with_create_time_as_timestamp(cls):
        return cls(field=TermAttributes.CREATE_TIME_AS_TIMESTAMP.value)

    @classmethod
    @validate_arguments()
    def with_trait_names(cls):
        return cls(field=TextAttributes.TRAIT_NAMES.value)

    @classmethod
    @validate_arguments()
    def with_type_name(cls):
        return cls(field=TermAttributes.TYPE_NAME.value)

    @classmethod
    @validate_arguments()
    def with_user_description(cls):
        return cls(field=TextAttributes.USER_DESCRIPTION.value)

    def to_dict(self):
        return {self.type_name: {"field": self.field}}


@dataclass(config=ConfigDict(smart_union=True, extra="forbid"))  # type: ignore
class Term(Query):
    field: str
    value: SearchFieldType
    boost: Optional[float] = None
    case_insensitive: Optional[bool] = None
    type_name: Literal["term"] = "term"

    @classmethod
    @validate_arguments()
    def with_categories(cls, value: StrictStr):
        return cls(field=TermAttributes.CATEGORIES.value, value=value)

    @classmethod
    @validate_arguments()
    def with_connector_name(cls, value: AtlanConnectorType):
        return cls(field=TermAttributes.CONNECTOR_NAME.value, value=value.value)

    @classmethod
    @validate_arguments()
    def with_created_by(cls, value: StrictStr):
        return cls(field=TermAttributes.CREATED_BY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_glossary(cls, value: StrictStr):
        return cls(field=TermAttributes.GLOSSARY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_guid(cls, value: StrictStr):
        # Use a GUID as a Query Term
        return cls(field=TermAttributes.GUID.value, value=value)

    @classmethod
    @validate_arguments()
    def with_has_lineage(cls, value: StrictBool):
        # Use a GUID as a Query Term
        return cls(field=TermAttributes.HAS_LINEAGE.value, value=value)

    @classmethod
    @validate_arguments()
    def with_meanings(cls, value: StrictStr):
        return cls(field=TermAttributes.MEANINGS.value, value=value)

    @classmethod
    @validate_arguments()
    def with_update_time_as_timestamp(cls, value: datetime):
        return cls(field=TermAttributes.UPDATE_TIME_AS_TIMESTAMP.value, value=value)

    @classmethod
    @validate_arguments()
    def with_modified_by(cls, value: StrictStr):
        return cls(field=TermAttributes.MODIFIED_BY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_name(cls, value: StrictStr):
        return cls(field=TermAttributes.NAME.value, value=value)

    @classmethod
    @validate_arguments()
    def with_owner_groups(cls, value: StrictStr):
        return cls(field=TermAttributes.OWNER_GROUPS.value, value=value)

    @classmethod
    @validate_arguments()
    def with_owner_users(cls, value: StrictStr):
        return cls(field=TermAttributes.OWNER_USERS.value, value=value)

    @classmethod
    @validate_arguments()
    def with_parent_category(cls, value: StrictStr):
        return cls(field=TermAttributes.PARENT_CATEGORY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_qualified_name(cls, value: StrictStr):
        return cls(field=TermAttributes.QUALIFIED_NAME.value, value=value)

    @classmethod
    @validate_arguments()
    def with_super_type_names(cls, value: StrictStr):
        return cls(field=TermAttributes.SUPER_TYPE_NAMES.value, value=value)

    @classmethod
    @validate_arguments()
    def with_state(cls, value: Literal["ACTIVE", "DELETE"]):
        return cls(field=TermAttributes.STATE.value, value=value)

    @classmethod
    @validate_arguments()
    def with_create_time_as_timestamp(cls, value: datetime):
        return cls(field=TermAttributes.CREATE_TIME_AS_TIMESTAMP.value, value=value)

    @classmethod
    @validate_arguments()
    def with_type_name(cls, value: StrictStr):
        return cls(field=TermAttributes.TYPE_NAME.value, value=value)

    def to_dict(self):
        if isinstance(self.value, datetime):
            parameters = {"value": int(self.value.timestamp() * 1000)}
        else:
            parameters = {"value": self.value}
        if self.case_insensitive is not None:
            parameters["case_insensitive"] = self.case_insensitive
        if self.boost is not None:
            parameters["boost"] = self.boost
        return {self.type_name: {self.field: parameters}}


@dataclass
class Terms(Query):
    field: str
    values: list[str]
    boost: Optional[float] = None
    type_name: Literal["terms"] = "terms"

    def to_dict(self):
        terms = {self.field: self.values}
        if self.boost is not None:
            terms["boost"] = self.boost
        return {self.type_name: terms}


@dataclass(config=ConfigDict(smart_union=True, extra="forbid"))  # type: ignore
class Bool(Query):
    must: list[Query] = Field(default_factory=list)
    should: list[Query] = Field(default_factory=list)
    must_not: list[Query] = Field(default_factory=list)
    filter: list[Query] = Field(default_factory=list)
    type_name: Literal["bool"] = "bool"
    boost: Optional[float] = None
    minimum_should_match: Optional[int] = None

    def __add__(self, other):
        q = self._clone()
        if isinstance(other, Bool):
            if other.must:
                q.must += other.must
            if other.should:
                q.should += other.should
            if other.must_not:
                q.must_not += other.must_not
            if other.filter:
                q.filter += other.filter
        else:
            q.must.append(other)
        return q

    __radd__ = __add__

    def __or__(self, other):
        for q in (self, other):
            if isinstance(q, Bool) and not any(
                (q.must, q.must_not, q.filter, getattr(q, "minimum_should_match", None))
            ):
                other = self if q is other else other
                q = q._clone()
                if isinstance(other, Bool) and not any(
                    (
                        other.must,
                        other.must_not,
                        other.filter,
                        getattr(other, "minimum_should_match", None),
                    )
                ):
                    q.should.extend(other.should)
                else:
                    q.should.append(other)
                return q

        return Bool(should=[self, other])

    __ror__ = __or__

    @property
    def _min_should_match(self):
        if not self.minimum_should_match:
            return 0 if not self.should or (self.must or self.filter) else 1
        else:
            return self.minimum_should_match

    def __invert__(self):
        # Because an empty Bool query is treated like
        # MatchAll the inverse should be MatchNone
        if not any(chain(self.must, self.filter, self.should, self.must_not)):
            return MatchNone()

        negations = [~q for q in chain(self.must, self.filter)]
        negations.extend(iter(self.must_not))
        if self.should and self._min_should_match:
            negations.append(Bool(must_not=self.should[:]))

        return negations[0] if len(negations) == 1 else Bool(should=negations)

    def __and__(self, other):
        q = self._clone()
        if isinstance(other, Bool):
            q.must += other.must
            q.must_not += other.must_not
            q.filter += other.filter
            q.should = []

            # reset minimum_should_match as it will get calculated below
            if q.minimum_should_match:
                q.minimum_should_match = None

            for qx in (self, other):
                # TODO: percentages will fail here
                min_should_match = qx._min_should_match
                # all subqueries are required
                if len(qx.should) <= min_should_match:
                    q.must.extend(qx.should)
                # not all of them are required, use it and remember min_should_match
                elif not q.should:
                    q.minimum_should_match = min_should_match
                    q.should = qx.should
                # all queries are optional, just extend should
                elif q._min_should_match == 0 and min_should_match == 0:
                    q.should.extend(qx.should)
                # not all are required, add a should list to the must with proper min_should_match
                else:
                    q.must.append(
                        Bool(should=qx.should, minimum_should_match=min_should_match)
                    )
        else:
            if not (q.must or q.filter) and q.should:
                q.minimum_should_match = 1
            q.must.append(other)
        return q

    __rand__ = __and__

    def to_dict(self) -> dict[Any, Any]:
        clauses = {}

        def add_clause(name):
            if hasattr(self, name):
                clause = self.__getattribute__(name)
                if clause and isinstance(clause, list) and len(clause) > 0:
                    clauses[name] = [c.to_dict() for c in clause]

        for name in ["must", "should", "must_not", "filter"]:
            add_clause(name)
        if self.boost is not None:
            clauses["boost"] = self.boost
        if self.minimum_should_match is not None:
            clauses["minimum_should_match"] = self.minimum_should_match
        return {"bool": clauses}


@dataclass(config=ConfigDict(smart_union=True, extra="forbid"))  # type: ignore
class Prefix(Query):
    field: str
    value: SearchFieldType
    boost: Optional[float] = None
    case_insensitive: Optional[bool] = None
    type_name: Literal["prefix"] = "prefix"

    @classmethod
    @validate_arguments()
    def with_categories(cls, value: StrictStr):
        return cls(field=TermAttributes.CATEGORIES.value, value=value)

    @classmethod
    @validate_arguments()
    def with_created_by(cls, value: StrictStr):
        return cls(field=TermAttributes.CREATED_BY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_glossary(cls, value: StrictStr):
        return cls(field=TermAttributes.GLOSSARY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_guid(cls, value: StrictStr):
        # Use a GUID as a Query Term
        return cls(field=TermAttributes.GUID.value, value=value)

    @classmethod
    @validate_arguments()
    def with_meanings(cls, value: StrictStr):
        return cls(field=TermAttributes.MEANINGS.value, value=value)

    @classmethod
    @validate_arguments()
    def with_modified_by(cls, value: StrictStr):
        return cls(field=TermAttributes.MODIFIED_BY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_name(cls, value: StrictStr):
        return cls(field=TermAttributes.NAME.value, value=value)

    @classmethod
    @validate_arguments()
    def with_owner_groups(cls, value: StrictStr):
        return cls(field=TermAttributes.OWNER_GROUPS.value, value=value)

    @classmethod
    @validate_arguments()
    def with_owner_users(cls, value: StrictStr):
        return cls(field=TermAttributes.OWNER_USERS.value, value=value)

    @classmethod
    @validate_arguments()
    def with_parent_category(cls, value: StrictStr):
        return cls(field=TermAttributes.PARENT_CATEGORY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_qualified_name(cls, value: StrictStr):
        return cls(field=TermAttributes.QUALIFIED_NAME.value, value=value)

    @classmethod
    @validate_arguments()
    def with_state(cls, value: Literal["ACTIVE", "DELETE"]):
        return cls(field=TermAttributes.STATE.value, value=value)

    @classmethod
    @validate_arguments()
    def with_super_type_names(cls, value: StrictStr):
        return cls(field=TermAttributes.SUPER_TYPE_NAMES.value, value=value)

    @classmethod
    @validate_arguments()
    def with_type_name(cls, value: StrictStr):
        return cls(field=TermAttributes.TYPE_NAME.value, value=value)

    def to_dict(self) -> dict[Any, Any]:
        parameters: dict[str, Any] = {
            "value": int(self.value.timestamp() * 1000)
            if isinstance(self.value, datetime)
            else self.value
        }

        if self.case_insensitive is not None:
            parameters["case_insensitive"] = self.case_insensitive
        if self.boost is not None:
            parameters["boost"] = self.boost
        return {self.type_name: {self.field: parameters}}


@dataclass(config=ConfigDict(smart_union=True, extra="forbid"))  # type: ignore
class Range(Query):
    field: str
    gt: Optional[SearchFieldType] = None
    gte: Optional[SearchFieldType] = None
    lt: Optional[SearchFieldType] = None
    lte: Optional[SearchFieldType] = None
    boost: Optional[float] = None
    format: Optional[StrictStr] = None
    relation: Optional[Literal["INTERSECTS", "CONTAINS", "WITHIN"]] = None
    time_zone: Optional[StrictStr] = None
    type_name: Literal["range"] = "range"

    @classmethod
    @validate_arguments()
    def with_popularity_score(
        cls,
        gt: Optional[SearchFieldType] = None,
        gte: Optional[SearchFieldType] = None,
        lt: Optional[SearchFieldType] = None,
        lte: Optional[SearchFieldType] = None,
        boost: Optional[float] = None,
        format: Optional[StrictStr] = None,
        relation: Optional[Literal["INTERSECTS", "CONTAINS", "WITHIN"]] = None,
        time_zone: Optional[StrictStr] = None,
    ):
        return cls(
            field=TermAttributes.POPULARITY_SCORE.value,
            gt=gt,
            gte=gte,
            lt=lt,
            lte=lte,
            boost=boost,
            format=format,
            relation=relation,
            time_zone=time_zone,
        )

    @classmethod
    @validate_arguments()
    def with_create_time_as_timestamp(
        cls,
        gt: Optional[SearchFieldType] = None,
        gte: Optional[SearchFieldType] = None,
        lt: Optional[SearchFieldType] = None,
        lte: Optional[SearchFieldType] = None,
        boost: Optional[float] = None,
        format: Optional[StrictStr] = None,
        relation: Optional[Literal["INTERSECTS", "CONTAINS", "WITHIN"]] = None,
        time_zone: Optional[StrictStr] = None,
    ):
        return cls(
            field=TermAttributes.CREATE_TIME_AS_TIMESTAMP.value,
            gt=gt,
            gte=gte,
            lt=lt,
            lte=lte,
            boost=boost,
            format=format,
            relation=relation,
            time_zone=time_zone,
        )

    @classmethod
    @validate_arguments()
    def with_create_time_as_date(
        cls,
        gt: Optional[SearchFieldType] = None,
        gte: Optional[SearchFieldType] = None,
        lt: Optional[SearchFieldType] = None,
        lte: Optional[SearchFieldType] = None,
        boost: Optional[float] = None,
        format: Optional[StrictStr] = None,
        relation: Optional[Literal["INTERSECTS", "CONTAINS", "WITHIN"]] = None,
        time_zone: Optional[StrictStr] = None,
    ):
        return cls(
            field=TextAttributes.CREATE_TIME_AS_DATE.value,
            gt=gt,
            gte=gte,
            lt=lt,
            lte=lte,
            boost=boost,
            format=format,
            relation=relation,
            time_zone=time_zone,
        )

    @classmethod
    @validate_arguments()
    def with_update_time_as_timestamp(
        cls,
        gt: Optional[SearchFieldType] = None,
        gte: Optional[SearchFieldType] = None,
        lt: Optional[SearchFieldType] = None,
        lte: Optional[SearchFieldType] = None,
        boost: Optional[float] = None,
        format: Optional[StrictStr] = None,
        relation: Optional[Literal["INTERSECTS", "CONTAINS", "WITHIN"]] = None,
        time_zone: Optional[StrictStr] = None,
    ):
        return cls(
            field=TermAttributes.UPDATE_TIME_AS_TIMESTAMP.value,
            gt=gt,
            gte=gte,
            lt=lt,
            lte=lte,
            boost=boost,
            format=format,
            relation=relation,
            time_zone=time_zone,
        )

    @classmethod
    @validate_arguments()
    def with_update_time_as_date(
        cls,
        gt: Optional[SearchFieldType] = None,
        gte: Optional[SearchFieldType] = None,
        lt: Optional[SearchFieldType] = None,
        lte: Optional[SearchFieldType] = None,
        boost: Optional[float] = None,
        format: Optional[StrictStr] = None,
        relation: Optional[Literal["INTERSECTS", "CONTAINS", "WITHIN"]] = None,
        time_zone: Optional[StrictStr] = None,
    ):
        return cls(
            field=TextAttributes.UPDATE_TIME_AS_DATE.value,
            gt=gt,
            gte=gte,
            lt=lt,
            lte=lte,
            boost=boost,
            format=format,
            relation=relation,
            time_zone=time_zone,
        )

    def to_dict(self) -> dict[Any, Any]:
        def get_value(attribute_name):
            if hasattr(self, attribute_name):
                attribute_value = getattr(self, attribute_name)
                if isinstance(attribute_value, datetime):
                    attribute_value = int(self.value.timestamp() * 1000)
            else:
                attribute_value = None
            return attribute_value

        parameters = {}
        for name in [
            "gt",
            "gte",
            "lt",
            "lte",
            "boost",
            "format",
            "relation",
            "time_zone",
        ]:
            value = get_value(name)
            if value:
                parameters[name] = value
        return {self.type_name: {self.field: parameters}}


@dataclass(config=ConfigDict(smart_union=True, extra="forbid"))  # type: ignore
class Wildcard(Query):
    field: str
    value: StrictStr
    boost: Optional[float] = None
    case_insensitive: Optional[bool] = None
    type_name: Literal["wildcard"] = "wildcard"

    @classmethod
    @validate_arguments()
    def with_categories(cls, value: StrictStr):
        return cls(field=TermAttributes.CATEGORIES.value, value=value)

    @classmethod
    @validate_arguments()
    def with_created_by(cls, value: StrictStr):
        return cls(field=TermAttributes.CREATED_BY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_glossary(cls, value: StrictStr):
        return cls(field=TermAttributes.GLOSSARY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_guid(cls, value: StrictStr):
        # Use a GUID as a Query Term
        return cls(field=TermAttributes.GUID.value, value=value)

    @classmethod
    @validate_arguments()
    def with_meanings(cls, value: StrictStr):
        return cls(field=TermAttributes.MEANINGS.value, value=value)

    @classmethod
    @validate_arguments()
    def with_modified_by(cls, value: StrictStr):
        return cls(field=TermAttributes.MODIFIED_BY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_name(cls, value: StrictStr):
        return cls(field=TermAttributes.NAME.value, value=value)

    @classmethod
    @validate_arguments()
    def with_owner_groups(cls, value: StrictStr):
        return cls(field=TermAttributes.OWNER_GROUPS.value, value=value)

    @classmethod
    @validate_arguments()
    def with_owner_users(cls, value: StrictStr):
        return cls(field=TermAttributes.OWNER_USERS.value, value=value)

    @classmethod
    @validate_arguments()
    def with_parent_category(cls, value: StrictStr):
        return cls(field=TermAttributes.PARENT_CATEGORY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_qualified_name(cls, value: StrictStr):
        return cls(field=TermAttributes.QUALIFIED_NAME.value, value=value)

    @classmethod
    @validate_arguments()
    def with_super_type_names(cls, value: StrictStr):
        return cls(field=TermAttributes.SUPER_TYPE_NAMES.value, value=value)

    @classmethod
    @validate_arguments()
    def with_state(cls, value: Literal["ACTIVE", "DELETE"]):
        return cls(field=TermAttributes.STATE.value, value=value)

    @classmethod
    @validate_arguments()
    def with_type_name(cls, value: StrictStr):
        return cls(field=TermAttributes.TYPE_NAME.value, value=value)

    def to_dict(self):
        if isinstance(self.value, datetime):
            parameters = {"value": int(self.value.timestamp() * 1000)}
        else:
            parameters = {"value": self.value}
        if self.case_insensitive is not None:
            parameters["case_insensitive"] = self.case_insensitive
        if self.boost is not None:
            parameters["boost"] = self.boost
        return {self.type_name: {self.field: parameters}}


@dataclass(config=ConfigDict(smart_union=True, extra="forbid"))  # type: ignore
class Regexp(Query):
    field: str
    value: StrictStr
    boost: Optional[float] = None
    case_insensitive: Optional[bool] = None
    max_determinized_states: Optional[int] = None
    type_name: Literal["regexp"] = "regexp"

    @classmethod
    @validate_arguments()
    def with_categories(cls, value: StrictStr):
        return cls(field=TermAttributes.CATEGORIES.value, value=value)

    @classmethod
    @validate_arguments()
    def with_created_by(cls, value: StrictStr):
        return cls(field=TermAttributes.CREATED_BY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_glossary(cls, value: StrictStr):
        return cls(field=TermAttributes.GLOSSARY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_guid(cls, value: StrictStr):
        # Use a GUID as a Query Term
        return cls(field=TermAttributes.GUID.value, value=value)

    @classmethod
    @validate_arguments()
    def with_meanings(cls, value: StrictStr):
        return cls(field=TermAttributes.MEANINGS.value, value=value)

    @classmethod
    @validate_arguments()
    def with_modified_by(cls, value: StrictStr):
        return cls(field=TermAttributes.MODIFIED_BY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_name(cls, value: StrictStr):
        return cls(field=TermAttributes.NAME.value, value=value)

    @classmethod
    @validate_arguments()
    def with_owner_groups(cls, value: StrictStr):
        return cls(field=TermAttributes.OWNER_GROUPS.value, value=value)

    @classmethod
    @validate_arguments()
    def with_owner_users(cls, value: StrictStr):
        return cls(field=TermAttributes.OWNER_USERS.value, value=value)

    @classmethod
    @validate_arguments()
    def with_parent_category(cls, value: StrictStr):
        return cls(field=TermAttributes.PARENT_CATEGORY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_qualified_name(cls, value: StrictStr):
        return cls(field=TermAttributes.QUALIFIED_NAME.value, value=value)

    @classmethod
    @validate_arguments()
    def with_super_type_names(cls, value: StrictStr):
        return cls(field=TermAttributes.SUPER_TYPE_NAMES.value, value=value)

    @classmethod
    @validate_arguments()
    def with_state(cls, value: Literal["ACTIVE", "DELETE"]):
        return cls(field=TermAttributes.STATE.value, value=value)

    @classmethod
    @validate_arguments()
    def with_type_name(cls, value: StrictStr):
        return cls(field=TermAttributes.TYPE_NAME.value, value=value)

    def to_dict(self):
        if isinstance(self.value, datetime):
            parameters = {"value": int(self.value.timestamp() * 1000)}
        else:
            parameters = {"value": self.value}
        if self.case_insensitive is not None:
            parameters["case_insensitive"] = self.case_insensitive
        if self.boost is not None:
            parameters["boost"] = self.boost
        if self.max_determinized_states:
            parameters["max_determinized_states"] = self.max_determinized_states
        return {self.type_name: {self.field: parameters}}


@dataclass(config=ConfigDict(smart_union=True, extra="forbid"))  # type: ignore
class Fuzzy(Query):
    field: str
    value: StrictStr
    fuzziness: Optional[str] = None
    max_expansions: Optional[int] = None
    prefix_length: Optional[int] = None
    transpositions: Optional[bool] = None
    rewrite: Optional[str] = None
    type_name: Literal["fuzzy"] = "fuzzy"

    @classmethod
    @validate_arguments()
    def with_categories(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.CATEGORIES.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    @classmethod
    @validate_arguments()
    def with_created_by(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.CREATED_BY.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    @classmethod
    @validate_arguments()
    def with_glossary(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.GLOSSARY.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    @classmethod
    @validate_arguments()
    def with_guid(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.GUID.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    @classmethod
    @validate_arguments()
    def with_meanings(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.MEANINGS.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    @classmethod
    @validate_arguments()
    def with_modified_by(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.MODIFIED_BY.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    @classmethod
    @validate_arguments()
    def with_name(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.NAME.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    @classmethod
    @validate_arguments()
    def with_owner_groups(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.OWNER_GROUPS.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    @classmethod
    @validate_arguments()
    def with_owner_users(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.OWNER_USERS.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    @classmethod
    @validate_arguments()
    def with_parent_category(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.PARENT_CATEGORY.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    @classmethod
    @validate_arguments()
    def with_qualified_name(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.QUALIFIED_NAME.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    @classmethod
    @validate_arguments()
    def with_super_type_names(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.SUPER_TYPE_NAMES.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    @classmethod
    @validate_arguments()
    def with_state(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.STATE.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    @classmethod
    @validate_arguments()
    def with_type_name(
        cls,
        value: StrictStr,
        fuzziness: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        transpositions: Optional[bool] = None,
        rewrite: Optional[str] = None,
    ):
        return cls(
            field=TermAttributes.TYPE_NAME.value,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )

    def to_dict(self):
        parameters = {"value": self.value}
        if self.fuzziness is not None:
            parameters["fuzziness"] = self.fuzziness
        if self.max_expansions is not None:
            parameters["max_expansions"] = self.max_expansions
        if self.prefix_length is not None:
            parameters["prefix_length"] = self.prefix_length
        if self.transpositions is not None:
            parameters["transpositions"] = self.transpositions
        if self.rewrite is not None:
            parameters["rewrite"] = self.rewrite
        return {self.type_name: {self.field: parameters}}


@dataclass(config=ConfigDict(smart_union=True, extra="forbid"))  # type: ignore
class Match(Query):
    field: str
    query: StrictStr
    analyzer: Optional[str] = None
    auto_generate_synonyms_phrase_query: Optional[bool] = None
    fuzziness: Optional[str] = None
    fuzzy_transpositions: Optional[bool] = None
    fuzzy_rewrite: Optional[str] = None
    lenient: Optional[bool] = None
    operator: Optional[Literal["OR", "AND"]] = None
    minimum_should_match: Optional[int] = None
    zero_terms_query: Optional[Literal["none", "all"]] = None
    max_expansions: Optional[int] = None
    prefix_length: Optional[int] = None
    type_name: Literal["match"] = "match"

    @classmethod
    @validate_arguments()
    def with_classification_names(
        cls,
        query: StrictStr,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[Literal["OR", "AND"]] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[Literal["none", "all"]] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
    ):
        return cls(
            field=TextAttributes.CLASSIFICATION_NAMES.value,
            query=query,
            analyzer=analyzer,
            auto_generate_synonyms_phrase_query=auto_generate_synonyms_phrase_query,
            fuzziness=fuzziness,
            fuzzy_transpositions=fuzzy_transpositions,
            fuzzy_rewrite=fuzzy_rewrite,
            lenient=lenient,
            operator=operator,
            minimum_should_match=minimum_should_match,
            zero_terms_query=zero_terms_query,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
        )

    @classmethod
    @validate_arguments()
    def with_classifications_text(
        cls,
        query: StrictStr,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[Literal["OR", "AND"]] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[Literal["none", "all"]] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
    ):
        return cls(
            field=TextAttributes.CLASSIFICATIONS_TEXT.value,
            query=query,
            analyzer=analyzer,
            auto_generate_synonyms_phrase_query=auto_generate_synonyms_phrase_query,
            fuzziness=fuzziness,
            fuzzy_transpositions=fuzzy_transpositions,
            fuzzy_rewrite=fuzzy_rewrite,
            lenient=lenient,
            operator=operator,
            minimum_should_match=minimum_should_match,
            zero_terms_query=zero_terms_query,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
        )

    @classmethod
    @validate_arguments()
    def with_name(
        cls,
        query: StrictStr,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[Literal["OR", "AND"]] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[Literal["none", "all"]] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
    ):
        return cls(
            field=TextAttributes.NAME.value,
            query=query,
            analyzer=analyzer,
            auto_generate_synonyms_phrase_query=auto_generate_synonyms_phrase_query,
            fuzziness=fuzziness,
            fuzzy_transpositions=fuzzy_transpositions,
            fuzzy_rewrite=fuzzy_rewrite,
            lenient=lenient,
            operator=operator,
            minimum_should_match=minimum_should_match,
            zero_terms_query=zero_terms_query,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
        )

    @classmethod
    @validate_arguments()
    def with_propagated_classification_names(
        cls,
        query: StrictStr,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[Literal["OR", "AND"]] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[Literal["none", "all"]] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
    ):
        return cls(
            field=TextAttributes.PROPAGATED_CLASSIFICATION_NAMES.value,
            query=query,
            analyzer=analyzer,
            auto_generate_synonyms_phrase_query=auto_generate_synonyms_phrase_query,
            fuzziness=fuzziness,
            fuzzy_transpositions=fuzzy_transpositions,
            fuzzy_rewrite=fuzzy_rewrite,
            lenient=lenient,
            operator=operator,
            minimum_should_match=minimum_should_match,
            zero_terms_query=zero_terms_query,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
        )

    @classmethod
    @validate_arguments()
    def with_description(
        cls,
        query: StrictStr,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[Literal["OR", "AND"]] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[Literal["none", "all"]] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
    ):
        return cls(
            field=TextAttributes.DESCRIPTION.value,
            query=query,
            analyzer=analyzer,
            auto_generate_synonyms_phrase_query=auto_generate_synonyms_phrase_query,
            fuzziness=fuzziness,
            fuzzy_transpositions=fuzzy_transpositions,
            fuzzy_rewrite=fuzzy_rewrite,
            lenient=lenient,
            operator=operator,
            minimum_should_match=minimum_should_match,
            zero_terms_query=zero_terms_query,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
        )

    @classmethod
    @validate_arguments()
    def with_propagated_trait_names(
        cls,
        query: StrictStr,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[Literal["OR", "AND"]] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[Literal["none", "all"]] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
    ):
        return cls(
            field=TextAttributes.PROPAGATED_TRAIT_NAMES.value,
            query=query,
            analyzer=analyzer,
            auto_generate_synonyms_phrase_query=auto_generate_synonyms_phrase_query,
            fuzziness=fuzziness,
            fuzzy_transpositions=fuzzy_transpositions,
            fuzzy_rewrite=fuzzy_rewrite,
            lenient=lenient,
            operator=operator,
            minimum_should_match=minimum_should_match,
            zero_terms_query=zero_terms_query,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
        )

    @classmethod
    @validate_arguments()
    def with_qualified_name(
        cls,
        query: StrictStr,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[Literal["OR", "AND"]] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[Literal["none", "all"]] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
    ):
        return cls(
            field=TextAttributes.QUALIFIED_NAME.value,
            query=query,
            analyzer=analyzer,
            auto_generate_synonyms_phrase_query=auto_generate_synonyms_phrase_query,
            fuzziness=fuzziness,
            fuzzy_transpositions=fuzzy_transpositions,
            fuzzy_rewrite=fuzzy_rewrite,
            lenient=lenient,
            operator=operator,
            minimum_should_match=minimum_should_match,
            zero_terms_query=zero_terms_query,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
        )

    @classmethod
    @validate_arguments()
    def with_super_type_names(
        cls,
        query: StrictStr,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[Literal["OR", "AND"]] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[Literal["none", "all"]] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
    ):
        return cls(
            field=TextAttributes.SUPER_TYPE_NAMES.value,
            query=query,
            analyzer=analyzer,
            auto_generate_synonyms_phrase_query=auto_generate_synonyms_phrase_query,
            fuzziness=fuzziness,
            fuzzy_transpositions=fuzzy_transpositions,
            fuzzy_rewrite=fuzzy_rewrite,
            lenient=lenient,
            operator=operator,
            minimum_should_match=minimum_should_match,
            zero_terms_query=zero_terms_query,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
        )

    @classmethod
    @validate_arguments()
    def with_trait_names(
        cls,
        query: StrictStr,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[Literal["OR", "AND"]] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[Literal["none", "all"]] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
    ):
        return cls(
            field=TextAttributes.TRAIT_NAMES.value,
            query=query,
            analyzer=analyzer,
            auto_generate_synonyms_phrase_query=auto_generate_synonyms_phrase_query,
            fuzziness=fuzziness,
            fuzzy_transpositions=fuzzy_transpositions,
            fuzzy_rewrite=fuzzy_rewrite,
            lenient=lenient,
            operator=operator,
            minimum_should_match=minimum_should_match,
            zero_terms_query=zero_terms_query,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
        )

    @classmethod
    @validate_arguments()
    def with_user_description(
        cls,
        query: StrictStr,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[Literal["OR", "AND"]] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[Literal["none", "all"]] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
    ):
        return cls(
            field=TextAttributes.USER_DESCRIPTION.value,
            query=query,
            analyzer=analyzer,
            auto_generate_synonyms_phrase_query=auto_generate_synonyms_phrase_query,
            fuzziness=fuzziness,
            fuzzy_transpositions=fuzzy_transpositions,
            fuzzy_rewrite=fuzzy_rewrite,
            lenient=lenient,
            operator=operator,
            minimum_should_match=minimum_should_match,
            zero_terms_query=zero_terms_query,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
        )

    def to_dict(self):
        parameters = {"query": self.query}
        if self.analyzer is not None:
            parameters["analyzer"] = self.analyzer
        if self.auto_generate_synonyms_phrase_query is not None:
            parameters[
                "auto_generate_synonyms_phrase_query"
            ] = self.auto_generate_synonyms_phrase_query
        if self.fuzziness is not None:
            parameters["fuzziness"] = self.fuzziness
        if self.fuzzy_transpositions is not None:
            parameters["fuzzy_transpositions"] = self.fuzzy_transpositions
        if self.fuzzy_rewrite is not None:
            parameters["fuzzy_rewrite"] = self.fuzzy_rewrite
        if self.lenient is not None:
            parameters["lenient"] = self.lenient
        if self.operator is not None:
            parameters["operator"] = self.operator
        if self.minimum_should_match is not None:
            parameters["minimum_should_match"] = self.minimum_should_match
        if self.zero_terms_query is not None:
            parameters["zero_terms_query"] = self.zero_terms_query
        if self.max_expansions is not None:
            parameters["max_expansions"] = self.max_expansions
        if self.prefix_length is not None:
            parameters["prefix_length"] = self.prefix_length
        return {self.type_name: {self.field: parameters}}


@dataclass(config=ConfigDict(smart_union=True, extra="forbid"))  # type: ignore
class SortItem:
    field: StrictStr
    order: Optional[SortOrder] = None

    def to_dict(self):
        return {self.field: {"order": self.order.value}}

    @validator("order", always=True)
    def validate_order(cls, v, values):
        if not v:
            if "field" in values:
                v = SortOrder.ASCENDING
        return v


class DSL(AtlanObject):
    from_: int = Field(0, alias="from")
    size: int = 100
    track_total_hits: bool = Field(True, alias="track_total_hits")
    post_filter: Optional[Query] = Field(alias="post_filter")
    query: Optional[Query]
    sort: Optional[list[SortItem]] = Field(alias="sort")

    class Config:
        json_encoders = {Query: lambda v: v.to_dict(), SortItem: lambda v: v.to_dict()}

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["from_", "size", "track_total_hits"])

    @validator("query", always=True)
    def validate_query(cls, v, values):
        if not v and ("post_filter" not in values or not values["post_filter"]):
            raise ValueError("Either query or post_filter is required")
        return v


class IndexSearchRequest(AtlanObject):
    dsl: DSL
    attributes: list[str] = Field(default_factory=list)
    relation_attributes: list[str] = Field(
        default_factory=list, alias="relationAttributes"
    )

    class Config:
        json_encoders = {Query: lambda v: v.to_dict(), SortItem: lambda v: v.to_dict()}
