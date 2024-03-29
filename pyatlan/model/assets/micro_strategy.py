# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
)

from .b_i import BI


class MicroStrategy(BI):
    """Description"""

    type_name: str = Field(default="MicroStrategy", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategy":
            raise ValueError("must be MicroStrategy")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategy._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MICRO_STRATEGY_PROJECT_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "microStrategyProjectQualifiedName",
            "microStrategyProjectQualifiedName",
            "microStrategyProjectQualifiedName.text",
        )
    )
    """
    Unique name of the project in which this asset exists.
    """
    MICRO_STRATEGY_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyProjectName",
        "microStrategyProjectName.keyword",
        "microStrategyProjectName",
    )
    """
    Simple name of the project in which this asset exists.
    """
    MICRO_STRATEGY_CUBE_QUALIFIED_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyCubeQualifiedNames",
        "microStrategyCubeQualifiedNames",
        "microStrategyCubeQualifiedNames.text",
    )
    """
    Unique names of the cubes related to this asset.
    """
    MICRO_STRATEGY_CUBE_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyCubeNames",
        "microStrategyCubeNames.keyword",
        "microStrategyCubeNames",
    )
    """
    Simple names of the cubes related to this asset.
    """
    MICRO_STRATEGY_REPORT_QUALIFIED_NAMES: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "microStrategyReportQualifiedNames",
            "microStrategyReportQualifiedNames",
            "microStrategyReportQualifiedNames.text",
        )
    )
    """
    Unique names of the reports related to this asset.
    """
    MICRO_STRATEGY_REPORT_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyReportNames",
        "microStrategyReportNames.keyword",
        "microStrategyReportNames",
    )
    """
    Simple names of the reports related to this asset.
    """
    MICRO_STRATEGY_IS_CERTIFIED: ClassVar[BooleanField] = BooleanField(
        "microStrategyIsCertified", "microStrategyIsCertified"
    )
    """
    Whether the asset is certified in MicroStrategy (true) or not (false).
    """
    MICRO_STRATEGY_CERTIFIED_BY: ClassVar[KeywordField] = KeywordField(
        "microStrategyCertifiedBy", "microStrategyCertifiedBy"
    )
    """
    User who certified this asset, in MicroStrategy.
    """
    MICRO_STRATEGY_CERTIFIED_AT: ClassVar[NumericField] = NumericField(
        "microStrategyCertifiedAt", "microStrategyCertifiedAt"
    )
    """
    Time (epoch) this asset was certified in MicroStrategy, in milliseconds.
    """
    MICRO_STRATEGY_LOCATION: ClassVar[KeywordField] = KeywordField(
        "microStrategyLocation", "microStrategyLocation"
    )
    """
    Location of this asset in MicroStrategy.
    """

    _convenience_properties: ClassVar[List[str]] = [
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
    def micro_strategy_cube_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_cube_qualified_names
        )

    @micro_strategy_cube_qualified_names.setter
    def micro_strategy_cube_qualified_names(
        self, micro_strategy_cube_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cube_qualified_names = (
            micro_strategy_cube_qualified_names
        )

    @property
    def micro_strategy_cube_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_cube_names
        )

    @micro_strategy_cube_names.setter
    def micro_strategy_cube_names(self, micro_strategy_cube_names: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cube_names = micro_strategy_cube_names

    @property
    def micro_strategy_report_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_report_qualified_names
        )

    @micro_strategy_report_qualified_names.setter
    def micro_strategy_report_qualified_names(
        self, micro_strategy_report_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_report_qualified_names = (
            micro_strategy_report_qualified_names
        )

    @property
    def micro_strategy_report_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_report_names
        )

    @micro_strategy_report_names.setter
    def micro_strategy_report_names(
        self, micro_strategy_report_names: Optional[Set[str]]
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
    def micro_strategy_location(self) -> Optional[List[Dict[str, str]]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_location
        )

    @micro_strategy_location.setter
    def micro_strategy_location(
        self, micro_strategy_location: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_location = micro_strategy_location

    class Attributes(BI.Attributes):
        micro_strategy_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        micro_strategy_project_name: Optional[str] = Field(default=None, description="")
        micro_strategy_cube_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        micro_strategy_cube_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        micro_strategy_report_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        micro_strategy_report_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        micro_strategy_is_certified: Optional[bool] = Field(
            default=None, description=""
        )
        micro_strategy_certified_by: Optional[str] = Field(default=None, description="")
        micro_strategy_certified_at: Optional[datetime] = Field(
            default=None, description=""
        )
        micro_strategy_location: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )

    attributes: MicroStrategy.Attributes = Field(
        default_factory=lambda: MicroStrategy.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
