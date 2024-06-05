# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextStemmedField,
    NumericField,
    RelationField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .preset import Preset


class PresetDataset(Preset):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        preset_dashboard_qualified_name: str,
    ) -> PresetDataset: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        preset_dashboard_qualified_name: str,
        connection_qualified_name: str,
    ) -> PresetDataset: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        preset_dashboard_qualified_name: str,
        connection_qualified_name: Optional[str] = None,
    ) -> PresetDataset:
        validate_required_fields(
            ["name", "preset_dashboard_qualified_name"],
            [name, preset_dashboard_qualified_name],
        )
        attributes = PresetDataset.Attributes.create(
            name=name,
            preset_dashboard_qualified_name=preset_dashboard_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(
        cls, *, name: str, preset_dashboard_qualified_name: str
    ) -> PresetDataset:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name, preset_dashboard_qualified_name=preset_dashboard_qualified_name
        )

    type_name: str = Field(default="PresetDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetDataset":
            raise ValueError("must be PresetDataset")
        return v

    def __setattr__(self, name, value):
        if name in PresetDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PRESET_DATASET_DATASOURCE_NAME: ClassVar[KeywordTextStemmedField] = (
        KeywordTextStemmedField(
            "presetDatasetDatasourceName",
            "presetDatasetDatasourceName.keyword",
            "presetDatasetDatasourceName",
            "presetDatasetDatasourceName.stemmed",
        )
    )
    """

    """
    PRESET_DATASET_ID: ClassVar[NumericField] = NumericField(
        "presetDatasetId", "presetDatasetId"
    )
    """

    """
    PRESET_DATASET_TYPE: ClassVar[KeywordField] = KeywordField(
        "presetDatasetType", "presetDatasetType"
    )
    """

    """

    PRESET_DASHBOARD: ClassVar[RelationField] = RelationField("presetDashboard")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "preset_dataset_datasource_name",
        "preset_dataset_id",
        "preset_dataset_type",
        "preset_dashboard",
    ]

    @property
    def preset_dataset_datasource_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dataset_datasource_name
        )

    @preset_dataset_datasource_name.setter
    def preset_dataset_datasource_name(
        self, preset_dataset_datasource_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dataset_datasource_name = preset_dataset_datasource_name

    @property
    def preset_dataset_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.preset_dataset_id

    @preset_dataset_id.setter
    def preset_dataset_id(self, preset_dataset_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dataset_id = preset_dataset_id

    @property
    def preset_dataset_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.preset_dataset_type

    @preset_dataset_type.setter
    def preset_dataset_type(self, preset_dataset_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dataset_type = preset_dataset_type

    @property
    def preset_dashboard(self) -> Optional[PresetDashboard]:
        return None if self.attributes is None else self.attributes.preset_dashboard

    @preset_dashboard.setter
    def preset_dashboard(self, preset_dashboard: Optional[PresetDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard = preset_dashboard

    class Attributes(Preset.Attributes):
        preset_dataset_datasource_name: Optional[str] = Field(
            default=None, description=""
        )
        preset_dataset_id: Optional[int] = Field(default=None, description="")
        preset_dataset_type: Optional[str] = Field(default=None, description="")
        preset_dashboard: Optional[PresetDashboard] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            preset_dashboard_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
        ) -> PresetDataset.Attributes:
            validate_required_fields(
                ["name", "preset_dashboard_qualified_name"],
                [name, preset_dashboard_qualified_name],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    preset_dashboard_qualified_name,
                    "preset_dashboard_qualified_name",
                    5,
                )

            return PresetDataset.Attributes(
                name=name,
                preset_dashboard_qualified_name=preset_dashboard_qualified_name,
                connection_qualified_name=connection_qualified_name or connection_qn,
                qualified_name=f"{preset_dashboard_qualified_name}/{name}",
                connector_name=connector_name,
                preset_dashboard=PresetDashboard.ref_by_qualified_name(
                    preset_dashboard_qualified_name
                ),
            )

    attributes: PresetDataset.Attributes = Field(
        default_factory=lambda: PresetDataset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .preset_dashboard import PresetDashboard  # noqa
