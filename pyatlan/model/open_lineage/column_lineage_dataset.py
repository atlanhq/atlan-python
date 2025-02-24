from typing import List, Optional

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject


class OpenLineageTransformation(AtlanObject):
    type: Optional[str] = Field(
        default=None,
        description="Type of the transformation. Allowed values are: DIRECT, INDIRECT",
    )
    subtype: Optional[str] = Field(
        default=None, description="Subtype of the transformation"
    )
    description: Optional[str] = Field(
        default=None, description="String representation of the transformation applied"
    )
    masking: Optional[bool] = Field(
        default=None, description="Is the transformation masking the data or not"
    )


class OpenLineageInputField(AtlanObject):
    namespace: Optional[str] = Field(
        default=None, description="Input dataset namespace"
    )
    name: Optional[str] = Field(default=None, description="Input dataset name")
    field: Optional[str] = Field(default=None, description="Input field")
    transformations: Optional[List[OpenLineageTransformation]] = Field(
        default_factory=list, description="List of transformations"
    )
