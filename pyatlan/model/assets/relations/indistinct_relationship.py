from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic.v1 import Field

from .relationship_attributes import RelationshipAttributes


class IndistinctRelationship(RelationshipAttributes):
    type_name: str = Field(
        default="IndistinctRelationship",
        description="Name of the relationship type that defines the relationship.",
    )
    attributes: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Map of attributes in the instance and their values",
    )
