# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/elastic/elasticsearch-dsl-py.git (under Apache-2.0 license)
from __future__ import annotations

import copy
import json as json_lib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from itertools import chain
from typing import Any, Dict, List, Optional, Sequence, Union

import msgspec

from pyatlan.model.enums import (
    AtlanConnectorType,
    CertificateStatus,
    ChildScoreMode,
    SortOrder,
    UTMTags,
)
from pyatlan_v9.model.aggregation import Aggregation

SearchFieldType = Union[str, int, float, bool, datetime]


class Attributes(str, Enum):
    attribute_type: type

    def __new__(cls, value: str, attribute_type: type) -> "Attributes":
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.attribute_type = attribute_type
        return obj


class TermAttributes(Attributes):
    CONNECTOR_NAME = ("connectorName", AtlanConnectorType)
    CATEGORIES = ("__categories", str)
    CREATE_TIME_AS_TIMESTAMP = ("__timestamp", datetime)
    CREATED_BY = ("__createdBy", str)
    GLOSSARY = ("__glossary", str)
    GUID = ("__guid", str)
    HAS_LINEAGE = ("__hasLineage", bool)
    MEANINGS = ("__meanings", str)
    MODIFIED_BY = ("__modifiedBy", str)
    NAME = ("name.keyword", str)
    OWNER_GROUPS = ("ownerGroups", str)
    OWNER_USERS = ("ownerUsers", str)
    PARENT_CATEGORY = ("__parentCategory", str)
    POPULARITY_SCORE = ("popularityScore", float)
    QUALIFIED_NAME = ("qualifiedName", str)
    STATE = ("__state", str)
    SUPER_TYPE_NAMES = ("__superTypeNames.keyword", str)
    TYPE_NAME = ("__typeName.keyword", str)
    UPDATE_TIME_AS_TIMESTAMP = ("__modificationTimestamp", datetime)
    CERTIFICATE_STATUS = ("certificateStatus", CertificateStatus)


class TextAttributes(Attributes):
    CLASSIFICATION_NAMES = ("__classificationNames", str)
    CLASSIFICATIONS_TEXT = ("__classificationsText", str)
    CREATE_TIME_AS_DATE = ("__timestamp.date", str)
    DESCRIPTION = ("description", str)
    MEANINGS_TEXT = ("__meaningsText", str)
    NAME = ("name", str)
    QUALIFIED_NAME = ("qualifiedName.text", str)
    PROPAGATED_CLASSIFICATION_NAMES = ("__propagatedClassificationNames", str)
    PROPAGATED_TRAIT_NAMES = ("__propagatedTraitNames", str)
    SUPER_TYPE_NAMES = ("__superTypeNames", str)
    TRAIT_NAMES = ("__traitNames", str)
    UPDATE_TIME_AS_DATE = ("__modificationTimestamp.date", str)
    USER_DESCRIPTION = ("userDescription", str)


def get_with_string(attribute: TermAttributes):
    @classmethod  # type: ignore[misc]
    def with_string(cls, value: str):
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
        return Bool(filter=[self, other])

    def __and__(self, other):
        # make sure we give queries that know how to combine themselves
        # preference
        if hasattr(other, "__rand__"):
            return other.__rand__(self)
        return Bool(filter=[self, other])

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
    def to_dict(self) -> Dict[Any, Any]: ...


@dataclass
class MatchAll(Query):
    type_name: str = "match_all"
    boost: Optional[float] = None

    def __add__(self, other):
        return other._clone()

    __and__ = __rand__ = __radd__ = __add__

    def __or__(self, other):
        return self

    __ror__ = __or__

    def __invert__(self):
        return MatchNone()

    def to_dict(self) -> Dict[Any, Any]:
        value = {"boost": self.boost} if self.boost else {}
        return {self.type_name: value}


EMPTY_QUERY = MatchAll()


@dataclass
class MatchNone(Query):
    type_name: str = "match_none"

    def __add__(self, other):
        return self

    __and__ = __rand__ = __radd__ = __add__

    def __or__(self, other):
        return other._clone()

    __ror__ = __or__

    def __invert__(self):
        return MatchAll()

    def to_dict(self) -> Dict[Any, Any]:
        return {"match_none": {}}


@dataclass
class Exists(Query):
    field: str
    type_name: str = "exists"

    @classmethod
    def with_custom_metadata(cls, client: Any, set_name: str, attr_name: str):
        if attr_id := client.custom_metadata_cache.get_attr_id_for_name(
            set_name=set_name, attr_name=attr_name
        ):
            return cls(field=attr_id)
        else:
            raise ValueError(
                f"No custom metadata with the name {set_name} or property {attr_name} exists"
            )

    @classmethod
    def with_categories(cls):
        return cls(field=TermAttributes.CATEGORIES.value)

    @classmethod
    def with_classification_names(cls):
        return cls(field=TextAttributes.CLASSIFICATION_NAMES.value)

    @classmethod
    def with_classifications_text(cls):
        return cls(field=TextAttributes.CLASSIFICATIONS_TEXT.value)

    @classmethod
    def with_connector_name(cls):
        return cls(field=TermAttributes.CONNECTOR_NAME.value)

    @classmethod
    def with_created_by(cls):
        return cls(field=TermAttributes.CREATED_BY.value)

    @classmethod
    def with_description(cls):
        return cls(field=TextAttributes.DESCRIPTION.value)

    @classmethod
    def with_glossary(cls):
        return cls(field=TermAttributes.GLOSSARY.value)

    @classmethod
    def with_guid(cls):
        return cls(field=TermAttributes.GUID.value)

    @classmethod
    def with_has_lineage(cls):
        return cls(field=TermAttributes.HAS_LINEAGE.value)

    @classmethod
    def with_meanings(cls):
        return cls(field=TermAttributes.MEANINGS.value)

    @classmethod
    def with_meanings_text(cls):
        return cls(field=TextAttributes.MEANINGS_TEXT.value)

    @classmethod
    def with_update_time_as_timestamp(cls):
        return cls(field=TermAttributes.UPDATE_TIME_AS_TIMESTAMP.value)

    @classmethod
    def with_modified_by(cls):
        return cls(field=TermAttributes.MODIFIED_BY.value)

    @classmethod
    def with_name(cls):
        return cls(field=TermAttributes.NAME.value)

    @classmethod
    def with_owner_users(cls):
        return cls(field=TermAttributes.OWNER_USERS.value)

    @classmethod
    def with_parent_category(cls):
        return cls(field=TermAttributes.PARENT_CATEGORY.value)

    @classmethod
    def with_popularity_score(cls):
        return cls(field=TermAttributes.POPULARITY_SCORE.value)

    @classmethod
    def with_propagated_classification_names(cls):
        return cls(field=TextAttributes.PROPAGATED_CLASSIFICATION_NAMES.value)

    @classmethod
    def with_propagated_trait_names(cls):
        return cls(field=TextAttributes.PROPAGATED_TRAIT_NAMES.value)

    @classmethod
    def with_qualified_name(cls):
        return cls(field=TermAttributes.QUALIFIED_NAME.value)

    @classmethod
    def with_super_type_names(cls):
        return cls(field=TermAttributes.SUPER_TYPE_NAMES.value)

    @classmethod
    def with_state(cls):
        return cls(field=TermAttributes.STATE.value)

    @classmethod
    def with_owner_groups(cls):
        return cls(field=TermAttributes.OWNER_GROUPS.value)

    @classmethod
    def with_create_time_as_timestamp(cls):
        return cls(field=TermAttributes.CREATE_TIME_AS_TIMESTAMP.value)

    @classmethod
    def with_trait_names(cls):
        return cls(field=TextAttributes.TRAIT_NAMES.value)

    @classmethod
    def with_type_name(cls):
        return cls(field=TermAttributes.TYPE_NAME.value)

    @classmethod
    def with_user_description(cls):
        return cls(field=TextAttributes.USER_DESCRIPTION.value)

    @classmethod
    def with_certificate_status(cls):
        return cls(field=TermAttributes.CERTIFICATE_STATUS.value)

    def to_dict(self):
        return {self.type_name: {"field": self.field}}


@dataclass
class NestedQuery(Query):
    path: str
    query: Query
    score_mode: Optional[ChildScoreMode] = None
    ignore_unmapped: Optional[bool] = None
    type_name: str = "nested"

    def to_dict(self):
        parameters: Dict[str, Any] = {"path": self.path, "query": self.query.to_dict()}
        if self.score_mode:
            parameters["score_more"] = str(self.score_mode)
        if self.ignore_unmapped is not None:
            parameters["ignore_unmapped"] = self.ignore_unmapped
        return {self.type_name: parameters}


@dataclass
class Term(Query):
    field: str
    value: SearchFieldType
    boost: Optional[float] = None
    case_insensitive: Optional[bool] = None
    type_name: str = "term"

    @classmethod
    def with_custom_metadata(
        cls,
        client: Any,
        set_name: str,
        attr_name: str,
        value: SearchFieldType,
    ):
        if attr_id := client.custom_metadata_cache.get_attr_id_for_name(
            set_name=set_name, attr_name=attr_name
        ):
            return cls(field=attr_id, value=value)
        else:
            raise ValueError(
                f"No custom metadata with the name {set_name} or property {attr_name} exists"
            )

    @classmethod
    def with_categories(cls, value: str):
        return cls(field=TermAttributes.CATEGORIES.value, value=value)

    @classmethod
    def with_connector_name(cls, value: AtlanConnectorType):
        return cls(field=TermAttributes.CONNECTOR_NAME.value, value=value.value)

    @classmethod
    def with_created_by(cls, value: str):
        return cls(field=TermAttributes.CREATED_BY.value, value=value)

    @classmethod
    def with_glossary(cls, qualified_name: str):
        return cls(field=TermAttributes.GLOSSARY.value, value=qualified_name)

    @classmethod
    def with_guid(cls, value: str):
        return cls(field=TermAttributes.GUID.value, value=value)

    @classmethod
    def with_has_lineage(cls, value: bool):
        return cls(field=TermAttributes.HAS_LINEAGE.value, value=value)

    @classmethod
    def with_meanings(cls, value: str):
        return cls(field=TermAttributes.MEANINGS.value, value=value)

    @classmethod
    def with_update_time_as_timestamp(cls, value: datetime):
        return cls(field=TermAttributes.UPDATE_TIME_AS_TIMESTAMP.value, value=value)

    @classmethod
    def with_modified_by(cls, value: str):
        return cls(field=TermAttributes.MODIFIED_BY.value, value=value)

    @classmethod
    def with_name(cls, value: str):
        return cls(field=TermAttributes.NAME.value, value=value)

    @classmethod
    def with_owner_groups(cls, value: str):
        return cls(field=TermAttributes.OWNER_GROUPS.value, value=value)

    @classmethod
    def with_owner_users(cls, value: str):
        return cls(field=TermAttributes.OWNER_USERS.value, value=value)

    @classmethod
    def with_parent_category(cls, value: str):
        return cls(field=TermAttributes.PARENT_CATEGORY.value, value=value)

    @classmethod
    def with_qualified_name(cls, value: str):
        return cls(field=TermAttributes.QUALIFIED_NAME.value, value=value)

    @classmethod
    def with_super_type_names(cls, value: str):
        return cls(field=TermAttributes.SUPER_TYPE_NAMES.value, value=value)

    @classmethod
    def with_state(cls, value: str):
        return cls(field=TermAttributes.STATE.value, value=value)

    @classmethod
    def with_create_time_as_timestamp(cls, value: datetime):
        return cls(field=TermAttributes.CREATE_TIME_AS_TIMESTAMP.value, value=value)

    @classmethod
    def with_type_name(cls, value: str):
        return cls(field=TermAttributes.TYPE_NAME.value, value=value)

    @classmethod
    def with_certificate_status(cls, value: CertificateStatus):
        return cls(field=TermAttributes.CERTIFICATE_STATUS.value, value=value.value)

    def to_dict(self):
        if isinstance(self.value, datetime):
            parameters: Dict[str, Any] = {"value": int(self.value.timestamp() * 1000)}
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
    values: List[str]
    boost: Optional[float] = None
    type_name: str = "terms"

    @classmethod
    def with_type_name(cls, values: List[str]):
        return cls(field=TermAttributes.TYPE_NAME.value, values=values)

    def to_dict(self):
        terms: Dict[str, Any] = {self.field: self.values}
        if self.boost is not None:
            terms["boost"] = self.boost
        return {self.type_name: terms}


@dataclass
class SpanWithin(Query):
    little: Optional[Query] = None
    big: Optional[Query] = None
    boost: Optional[float] = None
    type_name: str = "span_within"

    def to_dict(self):
        span_within: Dict[str, Any] = {}
        if self.little is not None:
            span_within["little"] = self.little
        if self.big is not None:
            span_within["big"] = self.big
        if self.boost is not None:
            span_within["boost"] = self.boost
        return {self.type_name: span_within}


@dataclass
class SpanTerm(Query):
    field: str
    value: SearchFieldType
    boost: Optional[float] = None
    type_name: str = "span_term"

    def to_dict(self):
        span_term: Dict[str, Any] = {self.field: self.value}
        if self.boost is not None:
            span_term["boost"] = self.boost
        return {self.type_name: span_term}


@dataclass
class SpanNear(Query):
    clauses: Optional[Sequence[Query]] = None
    in_order: Optional[bool] = None
    slop: Optional[int] = None
    type_name: str = "span_near"

    def to_dict(self):
        span_near: Dict[str, Any] = {}
        if self.clauses is not None:
            span_near["clauses"] = self.clauses
        if self.in_order is not None:
            span_near["in_order"] = self.in_order
        if self.slop is not None:
            span_near["slop"] = self.slop
        return {self.type_name: span_near}


@dataclass
class SpanOr(Query):
    clauses: Optional[Sequence[Query]] = None
    type_name: str = "span_or"

    def to_dict(self):
        span_or: Dict[str, Any] = {}
        if self.clauses is not None:
            span_or["clauses"] = self.clauses
        return {self.type_name: span_or}


@dataclass
class Span(Query):
    span_within: Optional[Query] = None
    span_near: Optional[Query] = None
    type_name: str = "span"

    def to_dict(self):
        span: Dict[str, Any] = {}
        if self.span_within is not None:
            span["span_within"] = self.span_within
        if self.span_near is not None:
            span["span_near"] = self.span_near
        return {self.type_name: span}


@dataclass
class Bool(Query):
    must: List[Query] = field(default_factory=list)
    should: List[Query] = field(default_factory=list)
    must_not: List[Query] = field(default_factory=list)
    filter: List[Query] = field(default_factory=list)
    type_name: str = "bool"
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
            q.filter.append(other)
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
            if not q.must and not q.filter and q.should:
                q.minimum_should_match = 1
            q.must.append(other)
        return q

    __rand__ = __and__

    def to_dict(self) -> Dict[Any, Any]:
        clauses: Dict[str, Any] = {}

        def add_clause(name):
            if hasattr(self, name):
                clause = getattr(self, name)
                if clause and isinstance(clause, list) and len(clause) > 0:
                    clauses[name] = [c.to_dict() for c in clause]

        for name in ["must", "should", "must_not", "filter"]:
            add_clause(name)
        if self.boost is not None:
            clauses["boost"] = self.boost
        if self.minimum_should_match is not None:
            clauses["minimum_should_match"] = self.minimum_should_match
        return {"bool": clauses}


@dataclass
class Prefix(Query):
    field: str
    value: SearchFieldType
    boost: Optional[float] = None
    case_insensitive: Optional[bool] = None
    type_name: str = "prefix"

    @classmethod
    def with_categories(cls, value: str):
        return cls(field=TermAttributes.CATEGORIES.value, value=value)

    @classmethod
    def with_created_by(cls, value: str):
        return cls(field=TermAttributes.CREATED_BY.value, value=value)

    @classmethod
    def with_glossary(cls, value: str):
        return cls(field=TermAttributes.GLOSSARY.value, value=value)

    @classmethod
    def with_guid(cls, value: str):
        return cls(field=TermAttributes.GUID.value, value=value)

    @classmethod
    def with_meanings(cls, value: str):
        return cls(field=TermAttributes.MEANINGS.value, value=value)

    @classmethod
    def with_modified_by(cls, value: str):
        return cls(field=TermAttributes.MODIFIED_BY.value, value=value)

    @classmethod
    def with_name(cls, value: str):
        return cls(field=TermAttributes.NAME.value, value=value)

    @classmethod
    def with_owner_groups(cls, value: str):
        return cls(field=TermAttributes.OWNER_GROUPS.value, value=value)

    @classmethod
    def with_owner_users(cls, value: str):
        return cls(field=TermAttributes.OWNER_USERS.value, value=value)

    @classmethod
    def with_parent_category(cls, value: str):
        return cls(field=TermAttributes.PARENT_CATEGORY.value, value=value)

    @classmethod
    def with_qualified_name(cls, value: str):
        return cls(field=TermAttributes.QUALIFIED_NAME.value, value=value)

    @classmethod
    def with_state(cls, value: str):
        return cls(field=TermAttributes.STATE.value, value=value)

    @classmethod
    def with_super_type_names(cls, value: str):
        return cls(field=TermAttributes.SUPER_TYPE_NAMES.value, value=value)

    @classmethod
    def with_type_name(cls, value: str):
        return cls(field=TermAttributes.TYPE_NAME.value, value=value)

    def to_dict(self) -> Dict[Any, Any]:
        parameters: Dict[str, Any] = {
            "value": (
                int(self.value.timestamp() * 1000)
                if isinstance(self.value, datetime)
                else self.value
            )
        }

        if self.case_insensitive is not None:
            parameters["case_insensitive"] = self.case_insensitive
        if self.boost is not None:
            parameters["boost"] = self.boost
        return {self.type_name: {self.field: parameters}}


@dataclass
class Range(Query):
    field: str
    gt: Optional[SearchFieldType] = None
    gte: Optional[SearchFieldType] = None
    lt: Optional[SearchFieldType] = None
    lte: Optional[SearchFieldType] = None
    boost: Optional[float] = None
    format: Optional[str] = None
    relation: Optional[str] = None
    time_zone: Optional[str] = None
    type_name: str = "range"

    @classmethod
    def with_popularity_score(
        cls,
        gt: Optional[SearchFieldType] = None,
        gte: Optional[SearchFieldType] = None,
        lt: Optional[SearchFieldType] = None,
        lte: Optional[SearchFieldType] = None,
        boost: Optional[float] = None,
        format: Optional[str] = None,
        relation: Optional[str] = None,
        time_zone: Optional[str] = None,
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
    def with_create_time_as_timestamp(
        cls,
        gt: Optional[SearchFieldType] = None,
        gte: Optional[SearchFieldType] = None,
        lt: Optional[SearchFieldType] = None,
        lte: Optional[SearchFieldType] = None,
        boost: Optional[float] = None,
        format: Optional[str] = None,
        relation: Optional[str] = None,
        time_zone: Optional[str] = None,
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
    def with_create_time_as_date(
        cls,
        gt: Optional[SearchFieldType] = None,
        gte: Optional[SearchFieldType] = None,
        lt: Optional[SearchFieldType] = None,
        lte: Optional[SearchFieldType] = None,
        boost: Optional[float] = None,
        format: Optional[str] = None,
        relation: Optional[str] = None,
        time_zone: Optional[str] = None,
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
    def with_update_time_as_timestamp(
        cls,
        gt: Optional[SearchFieldType] = None,
        gte: Optional[SearchFieldType] = None,
        lt: Optional[SearchFieldType] = None,
        lte: Optional[SearchFieldType] = None,
        boost: Optional[float] = None,
        format: Optional[str] = None,
        relation: Optional[str] = None,
        time_zone: Optional[str] = None,
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
    def with_update_time_as_date(
        cls,
        gt: Optional[SearchFieldType] = None,
        gte: Optional[SearchFieldType] = None,
        lt: Optional[SearchFieldType] = None,
        lte: Optional[SearchFieldType] = None,
        boost: Optional[float] = None,
        format: Optional[str] = None,
        relation: Optional[str] = None,
        time_zone: Optional[str] = None,
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

    def to_dict(self) -> Dict[Any, Any]:
        def get_value(attribute_name):
            if hasattr(self, attribute_name):
                attribute_value = getattr(self, attribute_name)
                if isinstance(attribute_value, datetime):
                    attribute_value = int(attribute_value.timestamp() * 1000)
            else:
                attribute_value = None
            return attribute_value

        parameters: Dict[str, Any] = {}
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
            if value is not None:
                parameters[name] = value
        return {self.type_name: {self.field: parameters}}


@dataclass
class Wildcard(Query):
    field: str
    value: str
    boost: Optional[float] = None
    case_insensitive: Optional[bool] = None
    type_name: str = "wildcard"

    @classmethod
    def with_categories(cls, value: str):
        return cls(field=TermAttributes.CATEGORIES.value, value=value)

    @classmethod
    def with_created_by(cls, value: str):
        return cls(field=TermAttributes.CREATED_BY.value, value=value)

    @classmethod
    def with_glossary(cls, value: str):
        return cls(field=TermAttributes.GLOSSARY.value, value=value)

    @classmethod
    def with_guid(cls, value: str):
        return cls(field=TermAttributes.GUID.value, value=value)

    @classmethod
    def with_meanings(cls, value: str):
        return cls(field=TermAttributes.MEANINGS.value, value=value)

    @classmethod
    def with_modified_by(cls, value: str):
        return cls(field=TermAttributes.MODIFIED_BY.value, value=value)

    @classmethod
    def with_name(cls, value: str):
        return cls(field=TermAttributes.NAME.value, value=value)

    @classmethod
    def with_owner_groups(cls, value: str):
        return cls(field=TermAttributes.OWNER_GROUPS.value, value=value)

    @classmethod
    def with_owner_users(cls, value: str):
        return cls(field=TermAttributes.OWNER_USERS.value, value=value)

    @classmethod
    def with_parent_category(cls, value: str):
        return cls(field=TermAttributes.PARENT_CATEGORY.value, value=value)

    @classmethod
    def with_qualified_name(cls, value: str):
        return cls(field=TermAttributes.QUALIFIED_NAME.value, value=value)

    @classmethod
    def with_super_type_names(cls, value: str):
        return cls(field=TermAttributes.SUPER_TYPE_NAMES.value, value=value)

    @classmethod
    def with_state(cls, value: str):
        return cls(field=TermAttributes.STATE.value, value=value)

    @classmethod
    def with_type_name(cls, value: str):
        return cls(field=TermAttributes.TYPE_NAME.value, value=value)

    def to_dict(self):
        if isinstance(self.value, datetime):
            parameters: Dict[str, Any] = {"value": int(self.value.timestamp() * 1000)}
        else:
            parameters = {"value": self.value}
        if self.case_insensitive is not None:
            parameters["case_insensitive"] = self.case_insensitive
        if self.boost is not None:
            parameters["boost"] = self.boost
        return {self.type_name: {self.field: parameters}}


@dataclass
class Regexp(Query):
    field: str
    value: str
    boost: Optional[float] = None
    case_insensitive: Optional[bool] = None
    max_determinized_states: Optional[int] = None
    type_name: str = "regexp"

    @classmethod
    def with_categories(cls, value: str):
        return cls(field=TermAttributes.CATEGORIES.value, value=value)

    @classmethod
    def with_created_by(cls, value: str):
        return cls(field=TermAttributes.CREATED_BY.value, value=value)

    @classmethod
    def with_glossary(cls, value: str):
        return cls(field=TermAttributes.GLOSSARY.value, value=value)

    @classmethod
    def with_guid(cls, value: str):
        return cls(field=TermAttributes.GUID.value, value=value)

    @classmethod
    def with_meanings(cls, value: str):
        return cls(field=TermAttributes.MEANINGS.value, value=value)

    @classmethod
    def with_modified_by(cls, value: str):
        return cls(field=TermAttributes.MODIFIED_BY.value, value=value)

    @classmethod
    def with_name(cls, value: str):
        return cls(field=TermAttributes.NAME.value, value=value)

    @classmethod
    def with_owner_groups(cls, value: str):
        return cls(field=TermAttributes.OWNER_GROUPS.value, value=value)

    @classmethod
    def with_owner_users(cls, value: str):
        return cls(field=TermAttributes.OWNER_USERS.value, value=value)

    @classmethod
    def with_parent_category(cls, value: str):
        return cls(field=TermAttributes.PARENT_CATEGORY.value, value=value)

    @classmethod
    def with_qualified_name(cls, value: str):
        return cls(field=TermAttributes.QUALIFIED_NAME.value, value=value)

    @classmethod
    def with_super_type_names(cls, value: str):
        return cls(field=TermAttributes.SUPER_TYPE_NAMES.value, value=value)

    @classmethod
    def with_state(cls, value: str):
        return cls(field=TermAttributes.STATE.value, value=value)

    @classmethod
    def with_type_name(cls, value: str):
        return cls(field=TermAttributes.TYPE_NAME.value, value=value)

    def to_dict(self):
        if isinstance(self.value, datetime):
            parameters: Dict[str, Any] = {"value": int(self.value.timestamp() * 1000)}
        else:
            parameters = {"value": self.value}
        if self.case_insensitive is not None:
            parameters["case_insensitive"] = self.case_insensitive
        if self.boost is not None:
            parameters["boost"] = self.boost
        if self.max_determinized_states:
            parameters["max_determinized_states"] = self.max_determinized_states
        return {self.type_name: {self.field: parameters}}


@dataclass
class Fuzzy(Query):
    field: str
    value: str
    fuzziness: Optional[str] = None
    max_expansions: Optional[int] = None
    prefix_length: Optional[int] = None
    transpositions: Optional[bool] = None
    rewrite: Optional[str] = None
    type_name: str = "fuzzy"

    @classmethod
    def with_categories(
        cls,
        value: str,
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
    def with_created_by(
        cls,
        value: str,
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
    def with_glossary(
        cls,
        value: str,
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
    def with_guid(
        cls,
        value: str,
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
    def with_meanings(
        cls,
        value: str,
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
    def with_modified_by(
        cls,
        value: str,
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
    def with_name(
        cls,
        value: str,
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
    def with_owner_groups(
        cls,
        value: str,
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
    def with_owner_users(
        cls,
        value: str,
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
    def with_parent_category(
        cls,
        value: str,
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
    def with_qualified_name(
        cls,
        value: str,
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
    def with_super_type_names(
        cls,
        value: str,
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
    def with_state(
        cls,
        value: str,
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
    def with_type_name(
        cls,
        value: str,
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
        parameters: Dict[str, Any] = {"value": self.value}
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


@dataclass
class Match(Query):
    field: str
    query: str
    analyzer: Optional[str] = None
    auto_generate_synonyms_phrase_query: Optional[bool] = None
    fuzziness: Optional[str] = None
    fuzzy_transpositions: Optional[bool] = None
    fuzzy_rewrite: Optional[str] = None
    lenient: Optional[bool] = None
    operator: Optional[str] = None
    minimum_should_match: Optional[int] = None
    zero_terms_query: Optional[str] = None
    max_expansions: Optional[int] = None
    prefix_length: Optional[int] = None
    type_name: str = "match"

    @classmethod
    def with_classification_names(
        cls,
        query: str,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[str] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[str] = None,
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
    def with_classifications_text(
        cls,
        query: str,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[str] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[str] = None,
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
    def with_name(
        cls,
        query: str,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[str] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[str] = None,
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
    def with_propagated_classification_names(
        cls,
        query: str,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[str] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[str] = None,
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
    def with_description(
        cls,
        query: str,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[str] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[str] = None,
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
    def with_propagated_trait_names(
        cls,
        query: str,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[str] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[str] = None,
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
    def with_qualified_name(
        cls,
        query: str,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[str] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[str] = None,
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
    def with_super_type_names(
        cls,
        query: str,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[str] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[str] = None,
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
    def with_trait_names(
        cls,
        query: str,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[str] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[str] = None,
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
    def with_user_description(
        cls,
        query: str,
        analyzer: Optional[str] = None,
        auto_generate_synonyms_phrase_query: Optional[bool] = None,
        fuzziness: Optional[str] = None,
        fuzzy_transpositions: Optional[bool] = None,
        fuzzy_rewrite: Optional[str] = None,
        lenient: Optional[bool] = None,
        operator: Optional[str] = None,
        minimum_should_match: Optional[int] = None,
        zero_terms_query: Optional[str] = None,
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
        parameters: Dict[str, Any] = {"query": self.query}
        if self.analyzer is not None:
            parameters["analyzer"] = self.analyzer
        if self.auto_generate_synonyms_phrase_query is not None:
            parameters["auto_generate_synonyms_phrase_query"] = (
                self.auto_generate_synonyms_phrase_query
            )
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


@dataclass
class MatchPhrase(Query):
    field: str
    query: str
    analyzer: Optional[str] = None
    slop: Optional[int] = None
    zero_terms_query: Optional[str] = None
    boost: Optional[float] = None
    type_name: str = "match_phrase"

    def to_dict(self):
        parameters: Dict[str, Any] = {"query": self.query}
        if self.analyzer is not None:
            parameters["analyzer"] = self.analyzer
        if self.slop is not None:
            parameters["slop"] = self.slop
        if self.zero_terms_query is not None:
            parameters["zero_terms_query"] = self.zero_terms_query
        if self.boost is not None:
            parameters["boost"] = self.boost
        return {self.type_name: {self.field: parameters}}


@dataclass
class SortItem:
    field: str
    order: Optional[SortOrder] = None
    nested_path: Optional[str] = None

    def __post_init__(self):
        if self.order is None:
            self.order = SortOrder.ASCENDING

    def to_dict(self):
        parameters: Dict[str, Any] = {"order": self.order.value}
        if self.nested_path is not None:
            parameters["nested"] = {"path": self.nested_path}
        return {self.field: parameters}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "SortItem":
        field_name, params = list(d.items())[0]
        order_val = params.get("order", SortOrder.ASCENDING)
        if isinstance(order_val, str):
            order_val = SortOrder(order_val)
        nested_path = params.get("nested", {}).get("path", None)
        return cls(field=field_name, order=order_val, nested_path=nested_path)


def _serialize_value(v: Any) -> Any:
    """Recursively serialize a value to JSON-compatible types."""
    if v is None:
        return None
    if hasattr(v, "to_dict") and callable(v.to_dict):
        return v.to_dict()
    if isinstance(v, dict):
        return {k: _serialize_value(val) for k, val in v.items()}
    if isinstance(v, list):
        return [_serialize_value(item) for item in v]
    if isinstance(v, Enum):
        return v.value
    return v


class DSL(msgspec.Struct, kw_only=True):
    from_: int = msgspec.field(default=0, name="from")
    size: int = 300
    aggregations: Dict[str, Aggregation] = msgspec.field(default_factory=dict)
    track_total_hits: Optional[bool] = True
    post_filter: Optional[Union[Dict[str, Any], Query]] = None
    query: Optional[Union[Dict[str, Any], Query]] = None
    req_class_name: Optional[str] = None
    sort: List[SortItem] = msgspec.field(default_factory=list)

    def __post_init__(self):
        # Validate that either query or post_filter is provided
        if not self.query and not self.post_filter:
            raise ValueError("Either query or post_filter is required")

        # Convert dict entries to SortItem instances
        if self.sort and all(isinstance(item, dict) for item in self.sort):
            self.sort = [SortItem.from_dict(item) for item in self.sort]  # type: ignore[arg-type]

        # Ensure sort includes GUID sort
        missing_guid_sort = True
        sort_by_guid = "__guid"
        auditsearch_sort_by_guid = "entityId"
        searchlog_sort_by_guid = "entityGuidsAll"
        for option in self.sort:
            if option.field and option.field in (
                sort_by_guid,
                auditsearch_sort_by_guid,
                searchlog_sort_by_guid,
            ):
                missing_guid_sort = False
                break
        if missing_guid_sort:
            if self.req_class_name == "SearchLogRequest":
                self.sort.append(SortItem(searchlog_sort_by_guid))
            elif self.req_class_name == "AuditSearchRequest":
                self.sort.append(SortItem(auditsearch_sort_by_guid))
            elif self.req_class_name == "IndexSearchRequest":
                self.sort.append(SortItem(sort_by_guid))

    def json(
        self,
        by_alias: bool = False,
        exclude_none: bool = False,
        exclude_unset: bool = False,
    ) -> str:
        """Serialize DSL to JSON string, matching legacy Pydantic output format."""
        d: Dict[str, Any] = {}
        d["from" if by_alias else "from_"] = self.from_
        d["size"] = self.size
        d["aggregations"] = _serialize_value(self.aggregations)
        d["track_total_hits"] = self.track_total_hits
        d["post_filter"] = _serialize_value(self.post_filter)
        d["query"] = _serialize_value(self.query)
        d["sort"] = _serialize_value(self.sort)
        if exclude_none:
            d = {k: v for k, v in d.items() if v is not None}
        return json_lib.dumps(d)


class IndexSearchRequestMetadata(msgspec.Struct, kw_only=True):
    save_search_log: bool = False
    utm_tags: List[str] = msgspec.field(default_factory=list)

    def to_dict(self, by_alias: bool = True) -> Dict[str, Any]:
        """Convert to dict with camelCase keys when by_alias=True."""
        if by_alias:
            return {
                "saveSearchLog": self.save_search_log,
                "utmTags": self.utm_tags,
            }
        return {
            "save_search_log": self.save_search_log,
            "utm_tags": self.utm_tags,
        }


class IndexSearchRequest(msgspec.Struct, kw_only=True):
    dsl: DSL
    attributes: Optional[List[str]] = msgspec.field(default_factory=list)
    relation_attributes: Optional[List[str]] = msgspec.field(
        default_factory=list, name="relationAttributes"
    )
    suppress_logs: Optional[bool] = msgspec.field(default=None, name="suppressLogs")
    show_search_score: Optional[bool] = msgspec.field(
        default=None, name="showSearchScore"
    )
    exclude_meanings: Optional[bool] = msgspec.field(
        default=None, name="excludeMeanings"
    )
    exclude_atlan_tags: Optional[bool] = msgspec.field(
        default=None, name="excludeClassifications"
    )
    allow_deleted_relations: Optional[bool] = msgspec.field(
        default=None, name="allowDeletedRelations"
    )
    include_atlan_tag_names: Optional[bool] = msgspec.field(
        default=None, name="includeClassificationNames"
    )
    persona: Optional[str] = None
    purpose: Optional[str] = None
    include_relationship_attributes: Optional[bool] = False
    enable_full_restriction: Optional[bool] = msgspec.field(
        default=None, name="enableFullRestriction"
    )
    request_metadata: Optional[IndexSearchRequestMetadata] = None

    def __post_init__(self):
        # Ensure DSL has the correct req_class_name
        class_name = self.__class__.__name__
        if self.dsl and isinstance(self.dsl, DSL) and not self.dsl.req_class_name:
            self.dsl = DSL(
                req_class_name=class_name,
                from_=self.dsl.from_,
                size=self.dsl.size,
                aggregations=self.dsl.aggregations,
                track_total_hits=self.dsl.track_total_hits,
                post_filter=self.dsl.post_filter,
                query=self.dsl.query,
                sort=self.dsl.sort,
            )

        # Set default request_metadata
        if self.request_metadata is None:
            self.request_metadata = IndexSearchRequestMetadata(
                save_search_log=False,
                utm_tags=[UTMTags.PROJECT_SDK_PYTHON],
            )

    def json(
        self,
        by_alias: bool = False,
        exclude_none: bool = False,
        exclude_unset: bool = False,
    ) -> str:
        """Serialize IndexSearchRequest to JSON string, matching legacy Pydantic output format."""
        # Build dict in field-declaration order with alias mapping
        _ALIAS_MAP = {
            "attributes": "attributes",
            "dsl": "dsl",
            "relation_attributes": "relationAttributes",
            "suppress_logs": "suppressLogs",
            "show_search_score": "showSearchScore",
            "exclude_meanings": "excludeMeanings",
            "exclude_atlan_tags": "excludeClassifications",
            "allow_deleted_relations": "allowDeletedRelations",
            "include_atlan_tag_names": "includeClassificationNames",
            "persona": "persona",
            "purpose": "purpose",
            "include_relationship_attributes": "includeRelationshipAttributes",
            "enable_full_restriction": "enableFullRestriction",
            "request_metadata": "requestMetadata",
        }
        d: Dict[str, Any] = {}
        for field_name, alias in _ALIAS_MAP.items():
            val = getattr(self, field_name, None)
            key = alias if by_alias else field_name
            if field_name == "dsl" and val is not None:
                val = json_lib.loads(
                    val.json(by_alias=by_alias, exclude_none=exclude_none)
                )
            elif field_name == "request_metadata" and val is not None:
                val = val.to_dict(by_alias=by_alias)
            else:
                val = _serialize_value(val)
            d[key] = val
        if exclude_none:
            d = {k: v for k, v in d.items() if v is not None}
        return json_lib.dumps(d)


def _validate_name(name: str) -> None:
    """Validate that name is a non-None, non-blank string."""
    if name is None:
        raise ValueError("name must not be None")
    if not name.strip():
        raise ValueError("name must have at least 1 non-whitespace character")


def _validate_glossary_qualified_name(qualified_name: str) -> None:
    """Validate that glossary qualified_name is a non-None, non-blank string."""
    if qualified_name is None:
        raise ValueError("glossary_qualified_name must not be None")
    if not qualified_name.strip():
        raise ValueError(
            "glossary_qualified_name must have at least 1 non-whitespace character"
        )


def with_active_glossary(name: str) -> Bool:
    """Return a Bool query matching an active glossary by name."""
    _validate_name(name)
    return (
        Term.with_state("ACTIVE")
        + Term.with_type_name("AtlasGlossary")
        + Term.with_name(name)
    )


def with_active_category(name: str, glossary_qualified_name: str) -> Bool:
    """Return a Bool query matching an active glossary category by name and glossary."""
    _validate_name(name)
    _validate_glossary_qualified_name(glossary_qualified_name)
    return (
        Term.with_state("ACTIVE")
        + Term.with_type_name("AtlasGlossaryCategory")
        + Term.with_name(name)
        + Term.with_glossary(glossary_qualified_name)
    )


def with_active_term(name: str, glossary_qualified_name: str) -> Bool:
    """Return a Bool query matching an active glossary term by name and glossary."""
    _validate_name(name)
    _validate_glossary_qualified_name(glossary_qualified_name)
    return (
        Term.with_state("ACTIVE")
        + Term.with_type_name("AtlasGlossaryTerm")
        + Term.with_name(name)
        + Term.with_glossary(glossary_qualified_name)
    )
