# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .micro_strategy import MicroStrategy


class MicroStrategyDocument(MicroStrategy):
    """Description"""

    type_name: str = Field(default="MicroStrategyDocument", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyDocument":
            raise ValueError("must be MicroStrategyDocument")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyDocument._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MICRO_STRATEGY_PROJECT: ClassVar[RelationField] = RelationField(
        "microStrategyProject"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "micro_strategy_project",
    ]

    @property
    def micro_strategy_project(self) -> Optional[MicroStrategyProject]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_project
        )

    @micro_strategy_project.setter
    def micro_strategy_project(
        self, micro_strategy_project: Optional[MicroStrategyProject]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project = micro_strategy_project

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            default=None, description=""
        )  # relationship

    attributes: MicroStrategyDocument.Attributes = Field(
        default_factory=lambda: MicroStrategyDocument.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .micro_strategy_project import MicroStrategyProject  # noqa
