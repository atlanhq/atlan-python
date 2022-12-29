from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Literal, Optional, Union

from pydantic import Field, validator

from pyatlan.model.core import AtlanObject

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass


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
    must: Optional[Union[Query, list[Query]]] = None
    should: Optional[Union[Query, list[Query]]] = None
    must_not: Optional[Union[Query, list[Query]]] = None
    filter: Optional[Union[Query, list[Query]]] = None
    type_name: Literal["bool"] = "bool"

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
