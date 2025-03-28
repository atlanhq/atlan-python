# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .power_b_i import PowerBI


class PowerBIDatasource(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBIDatasource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDatasource":
            raise ValueError("must be PowerBIDatasource")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDatasource._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CONNECTION_DETAILS: ClassVar[KeywordField] = KeywordField(
        "connectionDetails", "connectionDetails"
    )
    """
    Connection details of the datasource.
    """

    POWER_BI_DATAFLOWS: ClassVar[RelationField] = RelationField("powerBIDataflows")
    """
    TBC
    """
    DATASETS: ClassVar[RelationField] = RelationField("datasets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "connection_details",
        "power_b_i_dataflows",
        "datasets",
    ]

    @property
    def connection_details(self) -> Optional[Dict[str, str]]:
        return None if self.attributes is None else self.attributes.connection_details

    @connection_details.setter
    def connection_details(self, connection_details: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connection_details = connection_details

    @property
    def power_b_i_dataflows(self) -> Optional[List[PowerBIDataflow]]:
        return None if self.attributes is None else self.attributes.power_b_i_dataflows

    @power_b_i_dataflows.setter
    def power_b_i_dataflows(self, power_b_i_dataflows: Optional[List[PowerBIDataflow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_dataflows = power_b_i_dataflows

    @property
    def datasets(self) -> Optional[List[PowerBIDataset]]:
        return None if self.attributes is None else self.attributes.datasets

    @datasets.setter
    def datasets(self, datasets: Optional[List[PowerBIDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasets = datasets

    class Attributes(PowerBI.Attributes):
        connection_details: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        power_b_i_dataflows: Optional[List[PowerBIDataflow]] = Field(
            default=None, description=""
        )  # relationship
        datasets: Optional[List[PowerBIDataset]] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBIDatasource.Attributes = Field(
        default_factory=lambda: PowerBIDatasource.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_dataflow import PowerBIDataflow  # noqa: E402, F401
from .power_b_i_dataset import PowerBIDataset  # noqa: E402, F401
