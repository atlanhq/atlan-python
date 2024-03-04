# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .catalog import Catalog


class AlteryxWorkflow(Catalog):
    """Description"""

    type_name: str = Field(default="AlteryxWorkflow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AlteryxWorkflow":
            raise ValueError("must be AlteryxWorkflow")
        return v

    def __setattr__(self, name, value):
        if name in AlteryxWorkflow._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ALTERYX_TRANSFORMATIONS: ClassVar[RelationField] = RelationField(
        "alteryxTransformations"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "alteryx_transformations",
    ]

    @property
    def alteryx_transformations(self) -> Optional[List[Process]]:
        return (
            None if self.attributes is None else self.attributes.alteryx_transformations
        )

    @alteryx_transformations.setter
    def alteryx_transformations(self, alteryx_transformations: Optional[List[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alteryx_transformations = alteryx_transformations

    class Attributes(Catalog.Attributes):
        alteryx_transformations: Optional[List[Process]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "AlteryxWorkflow.Attributes" = Field(
        default_factory=lambda: AlteryxWorkflow.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


from .process import Process  # noqa
