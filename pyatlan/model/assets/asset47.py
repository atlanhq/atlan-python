# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Optional

from pydantic import Field, field_validator

from .asset18 import BI


class MicroStrategy(BI):
    """Description"""

    type_name: str = Field("MicroStrategy", frozen=False)

    @field_validator("type_name")
    @classmethod
    def validate_type_name(cls, v):
        if v != "MicroStrategy":
            raise ValueError("must be MicroStrategy")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategy._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "micro_strategy_project_qualified_name",
        "micro_strategy_project_name",
        "micro_strategy_cube_qualified_names",
        "micro_strategy_cube_names",
        "micro_strategy_report_qualified_names",
        "micro_strategy_report_names",
        "micro_strategy_is_certified",
        "micro_strategy_certified_by",
        "micro_strategy_certified_at",
        "micro_strategy_location",
    ]

    @property
    def micro_strategy_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_project_qualified_name
        )

    @micro_strategy_project_qualified_name.setter
    def micro_strategy_project_qualified_name(
        self, micro_strategy_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project_qualified_name = (
            micro_strategy_project_qualified_name
        )

    @property
    def micro_strategy_project_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_project_name
        )

    @micro_strategy_project_name.setter
    def micro_strategy_project_name(self, micro_strategy_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project_name = micro_strategy_project_name

    @property
    def micro_strategy_cube_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_cube_qualified_names
        )

    @micro_strategy_cube_qualified_names.setter
    def micro_strategy_cube_qualified_names(
        self, micro_strategy_cube_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cube_qualified_names = (
            micro_strategy_cube_qualified_names
        )

    @property
    def micro_strategy_cube_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_cube_names
        )

    @micro_strategy_cube_names.setter
    def micro_strategy_cube_names(self, micro_strategy_cube_names: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cube_names = micro_strategy_cube_names

    @property
    def micro_strategy_report_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_report_qualified_names
        )

    @micro_strategy_report_qualified_names.setter
    def micro_strategy_report_qualified_names(
        self, micro_strategy_report_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_report_qualified_names = (
            micro_strategy_report_qualified_names
        )

    @property
    def micro_strategy_report_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_report_names
        )

    @micro_strategy_report_names.setter
    def micro_strategy_report_names(
        self, micro_strategy_report_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_report_names = micro_strategy_report_names

    @property
    def micro_strategy_is_certified(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_is_certified
        )

    @micro_strategy_is_certified.setter
    def micro_strategy_is_certified(self, micro_strategy_is_certified: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_is_certified = micro_strategy_is_certified

    @property
    def micro_strategy_certified_by(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_certified_by
        )

    @micro_strategy_certified_by.setter
    def micro_strategy_certified_by(self, micro_strategy_certified_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_certified_by = micro_strategy_certified_by

    @property
    def micro_strategy_certified_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_certified_at
        )

    @micro_strategy_certified_at.setter
    def micro_strategy_certified_at(
        self, micro_strategy_certified_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_certified_at = micro_strategy_certified_at

    @property
    def micro_strategy_location(self) -> Optional[list[dict[str, str]]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_location
        )

    @micro_strategy_location.setter
    def micro_strategy_location(
        self, micro_strategy_location: Optional[list[dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_location = micro_strategy_location

    class Attributes(BI.Attributes):
        micro_strategy_project_qualified_name: Optional[str] = Field(
            default=None, description="", alias="microStrategyProjectQualifiedName"
        )

        micro_strategy_project_name: Optional[str] = Field(
            default=None, description="", alias="microStrategyProjectName"
        )

        micro_strategy_cube_qualified_names: Optional[set[str]] = Field(
            default=None, description="", alias="microStrategyCubeQualifiedNames"
        )

        micro_strategy_cube_names: Optional[set[str]] = Field(
            default=None, description="", alias="microStrategyCubeNames"
        )

        micro_strategy_report_qualified_names: Optional[set[str]] = Field(
            default=None, description="", alias="microStrategyReportQualifiedNames"
        )

        micro_strategy_report_names: Optional[set[str]] = Field(
            default=None, description="", alias="microStrategyReportNames"
        )

        micro_strategy_is_certified: Optional[bool] = Field(
            default=None, description="", alias="microStrategyIsCertified"
        )

        micro_strategy_certified_by: Optional[str] = Field(
            default=None, description="", alias="microStrategyCertifiedBy"
        )

        micro_strategy_certified_at: Optional[datetime] = Field(
            default=None, description="", alias="microStrategyCertifiedAt"
        )

        micro_strategy_location: Optional[list[dict[str, str]]] = Field(
            default=None, description="", alias="microStrategyLocation"
        )

    attributes: "MicroStrategy.Attributes" = Field(
        default_factory=lambda: MicroStrategy.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


MicroStrategy.Attributes.update_forward_refs()
