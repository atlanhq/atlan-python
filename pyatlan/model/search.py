from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Literal, Optional

from pydantic import Field, validator

from pyatlan.model.core import AtlanObject

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass
import copy


@dataclass
class Query(ABC):
    ...

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
        return copy.copy(self)

    @abstractmethod
    def to_dict(self) -> dict[Any, Any]:
        ...


@dataclass
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
        if self.boost:
            value = {"boost": self.boost}
        else:
            value = {}
        return {self.type_name: value}


EMPTY_QUERY = MatchAll()


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


@dataclass
class Term(Query):
    field: str
    value: str
    boost: Optional[float] = None
    case_insensitive: Optional[bool] = None
    type_name: Literal["term"] = "term"

    def to_dict(self):
        parameters = {"value": self.value}
        if self.case_insensitive is not None:
            parameters["case_insensitive"] = self.case_insensitive
        if self.boost is not None:
            parameters["boost"] = self.boost
        return {self.type_name: {self.field: parameters}}


@dataclass
class Bool(Query):
    must: list[Query] = Field(default_factory=list)
    should: list[Query] = Field(default_factory=list)
    must_not: list[Query] = Field(default_factory=list)
    filter: list[Query] = Field(default_factory=list)
    type_name: Literal["bool"] = "bool"
    boost: Optional[float] = None
    minimum_should_match: Optional[int] = None

    @validator("filter", always=True)
    def has_clause(cls, v, values):
        if (
            len(v) < 1
            and len(values["must"]) < 1
            and len(values["should"]) < 1
            and len(values["must_not"]) < 1
        ):
            raise ValueError(
                "At least one of must, should, must_not or filter is required"
            )
        return v

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

    def to_dict(self) -> dict[Any, Any]:
        clauses = {}

        def add_clause(name):
            if hasattr(self, name):
                clause = self.__getattribute__(name)
                if clause:
                    if isinstance(clause, list):
                        clauses[name] = [c.to_dict() for c in clause]
                    else:
                        clauses[name] = clause.to_dict()

        for name in ["must", "should", "must_not", "filter"]:
            add_clause(name)
        if self.boost is not None:
            clauses["boost"] = self.boost
        if self.minimum_should_match is not None:
            clauses["minimum_should_match"] = self.minimum_should_match
        return {"bool": clauses}


class DSL(AtlanObject):
    from_: int = Field(0, alias="from")
    size: int = 100
    post_filter: Optional[Query] = Field(alias="post_filter")
    query: Optional[Query]

    class Config:
        json_encoders = {Query: lambda v: v.to_dict()}


class IndexSearchRequest(AtlanObject):
    dsl: DSL
    attributes: list = Field(default_factory=list)

    class Config:
        json_encoders = {Query: lambda v: v.to_dict()}
