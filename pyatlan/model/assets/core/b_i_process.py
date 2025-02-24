# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .process import Process


class BIProcess(Process):
    """Description"""

    type_name: str = Field(default="BIProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "BIProcess":
            raise ValueError("must be BIProcess")
        return v

    def __setattr__(self, name, value):
        if name in BIProcess._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    OUTPUTS: ClassVar[RelationField] = RelationField("outputs")
    """
    Assets that are outputs from this process.
    """
    INPUTS: ClassVar[RelationField] = RelationField("inputs")
    """
    Assets that are inputs to this process.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "outputs",
        "inputs",
    ]

    @property
    def outputs(self) -> Optional[List[Catalog]]:
        return None if self.attributes is None else self.attributes.outputs

    @outputs.setter
    def outputs(self, outputs: Optional[List[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.outputs = outputs

    @property
    def inputs(self) -> Optional[List[Catalog]]:
        return None if self.attributes is None else self.attributes.inputs

    @inputs.setter
    def inputs(self, inputs: Optional[List[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inputs = inputs

    class Attributes(Process.Attributes):
        outputs: Optional[List[Catalog]] = Field(
            default=None, description=""
        )  # relationship
        inputs: Optional[List[Catalog]] = Field(
            default=None, description=""
        )  # relationship

    attributes: BIProcess.Attributes = Field(
        default_factory=lambda: BIProcess.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .catalog import Catalog  # noqa
