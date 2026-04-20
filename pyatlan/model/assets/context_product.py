# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import ContextLifecycleStatus
from pyatlan.model.fields.atlan_fields import KeywordField

from .context_studio import ContextStudio


class ContextProduct(ContextStudio):
    """Description"""

    type_name: str = Field(default="ContextProduct", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ContextProduct":
            raise ValueError("must be ContextProduct")
        return v

    def __setattr__(self, name, value):
        if name in ContextProduct._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CONTEXT_PRODUCT_LIFECYCLE_STATUS: ClassVar[KeywordField] = KeywordField(
        "contextProductLifecycleStatus", "contextProductLifecycleStatus"
    )
    """
    Lifecycle status of this context product.
    """
    CONTEXT_PRODUCT_AGENT_INSTRUCTIONS: ClassVar[KeywordField] = KeywordField(
        "contextProductAgentInstructions", "contextProductAgentInstructions"
    )
    """
    Free-form instructions provided to the LLM agent when generating SQL from this context product, such as scope constraints, tables to prefer or avoid, or domain-specific guidance.
    """  # noqa: E501

    _convenience_properties: ClassVar[List[str]] = [
        "context_product_lifecycle_status",
        "context_product_agent_instructions",
    ]

    @property
    def context_product_lifecycle_status(self) -> Optional[ContextLifecycleStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_product_lifecycle_status
        )

    @context_product_lifecycle_status.setter
    def context_product_lifecycle_status(
        self, context_product_lifecycle_status: Optional[ContextLifecycleStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_product_lifecycle_status = (
            context_product_lifecycle_status
        )

    @property
    def context_product_agent_instructions(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_product_agent_instructions
        )

    @context_product_agent_instructions.setter
    def context_product_agent_instructions(
        self, context_product_agent_instructions: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_product_agent_instructions = (
            context_product_agent_instructions
        )

    class Attributes(ContextStudio.Attributes):
        context_product_lifecycle_status: Optional[ContextLifecycleStatus] = Field(
            default=None, description=""
        )
        context_product_agent_instructions: Optional[str] = Field(
            default=None, description=""
        )

    attributes: ContextProduct.Attributes = Field(
        default_factory=lambda: ContextProduct.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


ContextProduct.Attributes.update_forward_refs()
