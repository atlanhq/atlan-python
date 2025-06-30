# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .flow import Flow


class FlowControlOperation(Flow):
    """Description"""

    type_name: str = Field(default="FlowControlOperation", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FlowControlOperation":
            raise ValueError("must be FlowControlOperation")
        return v

    def __setattr__(self, name, value):
        if name in FlowControlOperation._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FLOW_DATA_RESULTS: ClassVar[RelationField] = RelationField("flowDataResults")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "flow_data_results",
    ]

    @property
    def flow_data_results(self) -> Optional[List[Process]]:
        return None if self.attributes is None else self.attributes.flow_data_results

    @flow_data_results.setter
    def flow_data_results(self, flow_data_results: Optional[List[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_data_results = flow_data_results

    class Attributes(Flow.Attributes):
        flow_data_results: Optional[List[Process]] = Field(
            default=None, description=""
        )  # relationship

    attributes: FlowControlOperation.Attributes = Field(
        default_factory=lambda: FlowControlOperation.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .process import Process  # noqa: E402, F401
