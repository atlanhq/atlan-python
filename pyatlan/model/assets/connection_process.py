# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from .core.asset import Asset


class ConnectionProcess(Asset, type_name="ConnectionProcess"):
    """Description"""

    type_name: str = Field(default="ConnectionProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ConnectionProcess":
            raise ValueError("must be ConnectionProcess")
        return v

    def __setattr__(self, name, value):
        if name in ConnectionProcess._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[List[str]] = [
        "inputs",
        "outputs",
    ]

    @property
    def inputs(self) -> Optional[List[Connection]]:
        return None if self.attributes is None else self.attributes.inputs

    @inputs.setter
    def inputs(self, inputs: Optional[List[Connection]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inputs = inputs

    @property
    def outputs(self) -> Optional[List[Connection]]:
        return None if self.attributes is None else self.attributes.outputs

    @outputs.setter
    def outputs(self, outputs: Optional[List[Connection]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.outputs = outputs

    class Attributes(Asset.Attributes):
        inputs: Optional[List[Connection]] = Field(default=None, description="")
        outputs: Optional[List[Connection]] = Field(default=None, description="")

    attributes: ConnectionProcess.Attributes = Field(
        default_factory=lambda: ConnectionProcess.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .connection import Connection  # noqa: E402, F401

ConnectionProcess.Attributes.update_forward_refs()
