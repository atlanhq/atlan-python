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

from .superset import Superset


class SupersetDataset(Superset):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        superset_dashboard_qualified_name: str,
    ) -> SupersetDataset: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        superset_dashboard_qualified_name: str,
        connection_qualified_name: str,
    ) -> SupersetDataset: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        superset_dashboard_qualified_name: str,
        connection_qualified_name: Optional[str] = None,
    ) -> SupersetDataset:
        validate_required_fields(
            ["name", "superset_dashboard_qualified_name"],
            [name, superset_dashboard_qualified_name],
        )
        attributes = SupersetDataset.Attributes.create(
            name=name,
            superset_dashboard_qualified_name=superset_dashboard_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(
        cls, *, name: str, superset_dashboard_qualified_name: str
    ) -> SupersetDataset:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name,
            superset_dashboard_qualified_name=superset_dashboard_qualified_name,
        )

    type_name: str = Field(default="SupersetDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SupersetDataset":
            raise ValueError("must be SupersetDataset")
        return v

    def __setattr__(self, name, value):
        if name in SupersetDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SUPERSET_DATASET_DATASOURCE_NAME: ClassVar[KeywordTextStemmedField] = (
        KeywordTextStemmedField(
            "supersetDatasetDatasourceName",
            "supersetDatasetDatasourceName.keyword",
            "supersetDatasetDatasourceName",
            "supersetDatasetDatasourceName.stemmed",
        )
    )
    """
    Name of the datasource for the dataset.
    """
    SUPERSET_DATASET_ID: ClassVar[NumericField] = NumericField(
        "supersetDatasetId", "supersetDatasetId"
    )
    """
    Id of the dataset in superset.
    """
    SUPERSET_DATASET_TYPE: ClassVar[KeywordField] = KeywordField(
        "supersetDatasetType", "supersetDatasetType"
    )
    """
    Type of the dataset in superset.
    """

    SUPERSET_DASHBOARD: ClassVar[RelationField] = RelationField("supersetDashboard")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "superset_dataset_datasource_name",
        "superset_dataset_id",
        "superset_dataset_type",
        "superset_dashboard",
    ]

    @property
    def superset_dataset_datasource_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_dataset_datasource_name
        )

    @superset_dataset_datasource_name.setter
    def superset_dataset_datasource_name(
        self, superset_dataset_datasource_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dataset_datasource_name = (
            superset_dataset_datasource_name
        )

    @property
    def superset_dataset_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.superset_dataset_id

    @superset_dataset_id.setter
    def superset_dataset_id(self, superset_dataset_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dataset_id = superset_dataset_id

    @property
    def superset_dataset_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.superset_dataset_type
        )

    @superset_dataset_type.setter
    def superset_dataset_type(self, superset_dataset_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dataset_type = superset_dataset_type

    @property
    def superset_dashboard(self) -> Optional[SupersetDashboard]:
        return None if self.attributes is None else self.attributes.superset_dashboard

    @superset_dashboard.setter
    def superset_dashboard(self, superset_dashboard: Optional[SupersetDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dashboard = superset_dashboard

    class Attributes(Superset.Attributes):
        superset_dataset_datasource_name: Optional[str] = Field(
            default=None, description=""
        )
        superset_dataset_id: Optional[int] = Field(default=None, description="")
        superset_dataset_type: Optional[str] = Field(default=None, description="")
        superset_dashboard: Optional[SupersetDashboard] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            superset_dashboard_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
        ) -> SupersetDataset.Attributes:
            validate_required_fields(
                ["name", "superset_dashboard_qualified_name"],
                [name, superset_dashboard_qualified_name],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    superset_dashboard_qualified_name,
                    "superset_dashboard_qualified_name",
                    4,
                )

            return SupersetDataset.Attributes(
                name=name,
                superset_dashboard_qualified_name=superset_dashboard_qualified_name,
                connection_qualified_name=connection_qualified_name or connection_qn,
                qualified_name=f"{superset_dashboard_qualified_name}/{name}",
                connector_name=connector_name,
                superset_dashboard=SupersetDashboard.ref_by_qualified_name(
                    superset_dashboard_qualified_name
                ),
            )

    attributes: SupersetDataset.Attributes = Field(
        default_factory=lambda: SupersetDataset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .superset_dashboard import SupersetDashboard  # noqa

SupersetDataset.Attributes.update_forward_refs()
