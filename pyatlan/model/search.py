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
)

from pyatlan.model.core import AtlanObject

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

    CREATED_BY = ("__createdBy", StrictStr)
    GUID = ("__guid", StrictStr)
    MEANINGS_TEXT = ("__meaningsText", StrictStr)
    MODIFICATION_TIMESTAMP = ("__modificationTimestamp", datetime)
    MODIFIED_BY = ("__modifiedBy", StrictStr)
    QUALIFIED_NAME = ("qualifiedName", StrictStr)
    NAME = ("name.keyword", StrictStr)
    STATE = ("__state", Literal["ACTIVE", "DELETED"])
    TIMESTAMP = ("__timestamp", datetime)
    TYPE_NAME = ("__typeName", StrictStr)


def get_with_string(attribute: Attributes):
    @validate_arguments()
    def with_string(cls, value: StrictStr):
        """This function returns a string"""
        return cls(field=attribute.value, value=value)

    return with_string


# def add_with_methods(cls):
#     setattr(cls, "with_guid", classmethod(get_with_string(Attributes.GUID)))
#     return cls


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
    def with_created_by(cls):
        return cls(field=Attributes.CREATED_BY.value)

    @classmethod
    @validate_arguments()
    def with_guid(cls):
        # Use a GUID as a Query Term
        return cls(field=Attributes.GUID.value)

    @classmethod
    @validate_arguments()
    def with_meanings_text(cls):
        return cls(field=Attributes.MEANINGS_TEXT.value)

    @classmethod
    @validate_arguments()
    def with_modification_timestamp(cls):
        return cls(field=Attributes.MODIFICATION_TIMESTAMP.value)

    @classmethod
    @validate_arguments()
    def with_modified_by(cls):
        return cls(field=Attributes.MODIFIED_BY.value)

    @classmethod
    @validate_arguments()
    def with_qualified_name(cls):
        return cls(field=Attributes.QUALIFIED_NAME.value)

    @classmethod
    @validate_arguments()
    def with_name(cls):
        return cls(field=Attributes.NAME.value)

    @classmethod
    @validate_arguments()
    def with_state(cls):
        return cls(field=Attributes.STATE.value)

    @classmethod
    @validate_arguments()
    def with_timestamp(cls):
        return cls(field=Attributes.TIMESTAMP.value)

    @classmethod
    @validate_arguments()
    def with_type_name(cls):
        return cls(field=Attributes.TYPE_NAME.value)

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
    def with_created_by(cls, value: StrictStr):
        return cls(field=Attributes.CREATED_BY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_guid(cls, value: StrictStr):
        # Use a GUID as a Query Term
        return cls(field=Attributes.GUID.value, value=value)

    @classmethod
    @validate_arguments()
    def with_meanings_text(cls, value: StrictStr):
        return cls(field=Attributes.MEANINGS_TEXT.value, value=value)

    @classmethod
    @validate_arguments()
    def with_modification_timestamp(cls, value: datetime):
        return cls(field=Attributes.MODIFICATION_TIMESTAMP.value, value=value)

    @classmethod
    @validate_arguments()
    def with_modified_by(cls, value: StrictStr):
        return cls(field=Attributes.MODIFIED_BY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_qualified_name(cls, value: StrictStr):
        return cls(field=Attributes.QUALIFIED_NAME.value, value=value)

    @classmethod
    @validate_arguments()
    def with_name(cls, value: StrictStr):
        return cls(field=Attributes.NAME.value, value=value)

    @classmethod
    @validate_arguments()
    def with_state(cls, value: Literal["ACTIVE", "DELETE"]):
        return cls(field=Attributes.STATE.value, value=value)

    @classmethod
    @validate_arguments()
    def with_timestamp(cls, value: datetime):
        return cls(field=Attributes.TIMESTAMP.value, value=value)

    @classmethod
    @validate_arguments()
    def with_type_name(cls, value: StrictStr):
        return cls(field=Attributes.TYPE_NAME.value, value=value)

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
    def with_created_by(cls, value: StrictStr):
        return cls(field=Attributes.CREATED_BY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_guid(cls, value: StrictStr):
        # Use a GUID as a Query Term
        return cls(field=Attributes.GUID.value, value=value)

    @classmethod
    @validate_arguments()
    def with_meanings_text(cls, value: StrictStr):
        return cls(field=Attributes.MEANINGS_TEXT.value, value=value)

    @classmethod
    @validate_arguments()
    def with_modification_timestamp(cls, value: datetime):
        return cls(field=Attributes.MODIFICATION_TIMESTAMP.value, value=value)

    @classmethod
    @validate_arguments()
    def with_modified_by(cls, value: StrictStr):
        return cls(field=Attributes.MODIFIED_BY.value, value=value)

    @classmethod
    @validate_arguments()
    def with_qualified_name(cls, value: StrictStr):
        return cls(field=Attributes.QUALIFIED_NAME.value, value=value)

    @classmethod
    @validate_arguments()
    def with_name(cls, value: StrictStr):
        return cls(field=Attributes.NAME.value, value=value)

    @classmethod
    @validate_arguments()
    def with_state(cls, value: Literal["ACTIVE", "DELETE"]):
        return cls(field=Attributes.STATE.value, value=value)

    @classmethod
    @validate_arguments()
    def with_timestamp(cls, value: datetime):
        return cls(field=Attributes.TIMESTAMP.value, value=value)

    @classmethod
    @validate_arguments()
    def with_type_name(cls, value: StrictStr):
        return cls(field=Attributes.TYPE_NAME.value, value=value)

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
    gt: Optional[SearchFieldType]
    gte: Optional[SearchFieldType]
    lt: Optional[SearchFieldType]
    lte: Optional[SearchFieldType]
    boost: Optional[float] = None
    format: Optional[StrictStr] = None
    relation: Optional[Literal["INTERSECTS", "CONTAINS", "WITHIN"]] = None
    time_zone: Optional[StrictStr] = None
    type_name: Literal["range"] = "range"

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


class DSL(AtlanObject):
    from_: int = Field(0, alias="from")
    size: int = 100
    post_filter: Optional[Query] = Field(alias="post_filter")
    query: Optional[Query]
    sort: Optional[list[dict[Any, Any]]]

    class Config:
        json_encoders = {Query: lambda v: v.to_dict()}


class IndexSearchRequest(AtlanObject):
    dsl: DSL
    attributes: list = Field(default_factory=list)

    class Config:
        json_encoders = {Query: lambda v: v.to_dict()}
