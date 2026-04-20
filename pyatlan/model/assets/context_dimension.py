# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .context_studio import ContextStudio


class ContextDimension(ContextStudio):
    """Description"""

    type_name: str = Field(default="ContextDimension", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ContextDimension":
            raise ValueError("must be ContextDimension")
        return v

    def __setattr__(self, name, value):
        if name in ContextDimension._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CONTEXT_DIMENSION_SAMPLE_VALUES: ClassVar[KeywordField] = KeywordField(
        "contextDimensionSampleValues", "contextDimensionSampleValues"
    )
    """
    Representative sample values observed in the underlying data for this dimension, used to help the LLM understand value distribution and generate accurate filters.
    """  # noqa: E501
    CONTEXT_DIMENSION_ALLOWED_VALUES: ClassVar[KeywordField] = KeywordField(
        "contextDimensionAllowedValues", "contextDimensionAllowedValues"
    )
    """
    Exhaustive set of allowed values for this dimension, used to constrain the LLM to only generate filters with valid entries.
    """  # noqa: E501

    _convenience_properties: ClassVar[List[str]] = [
        "context_dimension_sample_values",
        "context_dimension_allowed_values",
    ]

    @property
    def context_dimension_sample_values(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_dimension_sample_values
        )

    @context_dimension_sample_values.setter
    def context_dimension_sample_values(
        self, context_dimension_sample_values: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_dimension_sample_values = (
            context_dimension_sample_values
        )

    @property
    def context_dimension_allowed_values(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_dimension_allowed_values
        )

    @context_dimension_allowed_values.setter
    def context_dimension_allowed_values(
        self, context_dimension_allowed_values: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_dimension_allowed_values = (
            context_dimension_allowed_values
        )

    class Attributes(ContextStudio.Attributes):
        context_dimension_sample_values: Optional[Set[str]] = Field(
            default=None, description=""
        )
        context_dimension_allowed_values: Optional[Set[str]] = Field(
            default=None, description=""
        )

    attributes: ContextDimension.Attributes = Field(
        default_factory=lambda: ContextDimension.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


ContextDimension.Attributes.update_forward_refs()
