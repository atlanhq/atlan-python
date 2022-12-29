from abc import ABC, abstractmethod
from typing import Any, Literal, Optional, Union

from pydantic import Field, validator
from pydantic.dataclasses import dataclass

from pyatlan.model.core import AtlanObject


class DSL(AtlanObject):
    from_: int = 0
    size: int = 100
    post_filter: dict = Field(default_factory=dict, alias="post_filter")
    query: dict = Field(default_factory=dict)


class IndexSearchRequest(AtlanObject):
    dsl: DSL = DSL()
    attributes: list = Field(default_factory=list)


@dataclass
class Query(ABC):
    ...

    @abstractmethod
    def to_dict(self) -> dict[Any, Any]:
        ...


@dataclass
class Term(Query):
    field: str
    value: str
    boost: Optional[float] = None
    case_insensitive: Optional[bool] = None
    _type_name: Literal["term"] = "term"

    def to_dict(self):
        parameters = {"value": self.value}
        if self.case_insensitive is not None:
            parameters["case_insensitive"] = self.case_insensitive
        if self.boost is not None:
            parameters["boost"] = self.boost
        return {self._type_name: {self.field: parameters}}


@dataclass
class Bool(Query):
    must: Optional[Union[Query, list[Query]]] = None
    should: Optional[Union[Query, list[Query]]] = None
    must_not: Optional[Union[Query, list[Query]]] = None
    filter: Optional[Union[Query, list[Query]]] = None
    _type_name: Literal["bool"] = "bool"

    @validator("filter")
    def has_clause(cls, v, values):
        if (
            v is None
            and values["must"] is None
            and values["should"] is None
            and values["must_not"] is None
        ):
            raise ValueError(
                "At least one of must, should, must_not or filter is required"
            )

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

        for name in ["must"]:
            add_clause(name)

        return {"bool": clauses}
