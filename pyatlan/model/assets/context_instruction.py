# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .context_studio import ContextStudio


class ContextInstruction(ContextStudio):
    """Description"""

    type_name: str = Field(default="ContextInstruction", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ContextInstruction":
            raise ValueError("must be ContextInstruction")
        return v

    def __setattr__(self, name, value):
        if name in ContextInstruction._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CONTEXT_INSTRUCTION_PAYLOAD: ClassVar[KeywordField] = KeywordField(
        "contextInstructionPayload", "contextInstructionPayload"
    )
    """
    The instruction content as plain text or structured JSON, containing the actual guidance or rule the LLM should follow during query generation.
    """  # noqa: E501

    _convenience_properties: ClassVar[List[str]] = [
        "context_instruction_payload",
    ]

    @property
    def context_instruction_payload(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_instruction_payload
        )

    @context_instruction_payload.setter
    def context_instruction_payload(self, context_instruction_payload: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_instruction_payload = context_instruction_payload

    class Attributes(ContextStudio.Attributes):
        context_instruction_payload: Optional[str] = Field(default=None, description="")

    attributes: ContextInstruction.Attributes = Field(
        default_factory=lambda: ContextInstruction.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


ContextInstruction.Attributes.update_forward_refs()
