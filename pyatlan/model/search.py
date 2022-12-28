from pydantic import Field

from pyatlan.model.core import AtlanObject


class DSL(AtlanObject):
    from_: int = 0
    size: int = 100
    post_filter: dict = Field(default_factory=dict, alias="post_filter")
    query: dict = Field(default_factory=dict)


class IndexSearchRequest(AtlanObject):
    dsl: DSL = DSL()
    attributes: list = Field(default_factory=list)
