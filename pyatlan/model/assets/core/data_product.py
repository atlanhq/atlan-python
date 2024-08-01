# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional, Set
from warnings import warn

from pydantic.v1 import Field, StrictStr, validator

from pyatlan.model.data_mesh import DataProductsAssetsDSL
from pyatlan.model.enums import (
    DataProductCriticality,
    DataProductSensitivity,
    DataProductStatus,
    DataProductVisibility,
)
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField
from pyatlan.model.search import IndexSearchRequest
from pyatlan.utils import init_guid, validate_required_fields

from .asset import SelfAsset
from .data_mesh import DataMesh


class DataProduct(DataMesh):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: StrictStr,
        domain_qualified_name: StrictStr,
        asset_selection: IndexSearchRequest,
    ) -> DataProduct:
        attributes = DataProduct.Attributes.create(
            name=name,
            domain_qualified_name=domain_qualified_name,
            asset_selection=asset_selection,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(
        cls,
        *,
        name: StrictStr,
        domain_qualified_name: StrictStr,
        asset_selection: IndexSearchRequest,
    ) -> DataProduct:
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
            domain_qualified_name=domain_qualified_name,
            asset_selection=asset_selection,
        )

    @classmethod
    def updater(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = "",
    ) -> SelfAsset:
        validate_required_fields(
            ["name", "qualified_name"],
            [name, qualified_name],
        )
        # Split the data product qualified_name to extract data mesh info
        fields = qualified_name.split("/")
        if len(fields) < 5:
            raise ValueError(f"Invalid data product qualified_name: {qualified_name}")
        return cls(
            attributes=cls.Attributes(
                qualified_name=qualified_name,
                name=name,
            )
        )

    @classmethod
    def create_for_modification(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = "",
    ) -> SelfAsset:
        warn(
            (
                "This method is deprecated, please use 'updater' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.updater(
            qualified_name=qualified_name,
            name=name,
        )

    type_name: str = Field(default="DataProduct", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataProduct":
            raise ValueError("must be DataProduct")
        return v

    def __setattr__(self, name, value):
        if name in DataProduct._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_PRODUCT_STATUS: ClassVar[KeywordField] = KeywordField(
        "dataProductStatus", "dataProductStatus"
    )
    """
    Status of this data product.
    """
    DAAP_STATUS: ClassVar[KeywordField] = KeywordField("daapStatus", "daapStatus")
    """
    Status of this data product.
    """
    DATA_PRODUCT_CRITICALITY: ClassVar[KeywordField] = KeywordField(
        "dataProductCriticality", "dataProductCriticality"
    )
    """
    Criticality of this data product.
    """
    DAAP_CRITICALITY: ClassVar[KeywordField] = KeywordField(
        "daapCriticality", "daapCriticality"
    )
    """
    Criticality of this data product.
    """
    DATA_PRODUCT_SENSITIVITY: ClassVar[KeywordField] = KeywordField(
        "dataProductSensitivity", "dataProductSensitivity"
    )
    """
    Information sensitivity of this data product.
    """
    DAAP_SENSITIVITY: ClassVar[KeywordField] = KeywordField(
        "daapSensitivity", "daapSensitivity"
    )
    """
    Information sensitivity of this data product.
    """
    DATA_PRODUCT_VISIBILITY: ClassVar[KeywordField] = KeywordField(
        "dataProductVisibility", "dataProductVisibility"
    )
    """
    Visibility of a data product.
    """
    DAAP_VISIBILITY: ClassVar[KeywordField] = KeywordField(
        "daapVisibility", "daapVisibility"
    )
    """
    Visibility of a data product.
    """
    DATA_PRODUCT_ASSETS_DSL: ClassVar[KeywordField] = KeywordField(
        "dataProductAssetsDSL", "dataProductAssetsDSL"
    )
    """
    Search DSL used to define which assets are part of this data product.
    """
    DATA_PRODUCT_ASSETS_PLAYBOOK_FILTER: ClassVar[KeywordField] = KeywordField(
        "dataProductAssetsPlaybookFilter", "dataProductAssetsPlaybookFilter"
    )
    """
    Playbook filter to define which assets are part of this data product.
    """
    DATA_PRODUCT_SCORE_VALUE: ClassVar[NumericField] = NumericField(
        "dataProductScoreValue", "dataProductScoreValue"
    )
    """
    Score of this data product.
    """
    DATA_PRODUCT_SCORE_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "dataProductScoreUpdatedAt", "dataProductScoreUpdatedAt"
    )
    """
    Timestamp when the score of this data product was last updated.
    """
    DAAP_VISIBILITY_USERS: ClassVar[KeywordField] = KeywordField(
        "daapVisibilityUsers", "daapVisibilityUsers"
    )
    """
    list of users for product visibility control
    """
    DAAP_VISIBILITY_GROUPS: ClassVar[KeywordField] = KeywordField(
        "daapVisibilityGroups", "daapVisibilityGroups"
    )
    """
    list of groups for product visibility control
    """

    DATA_DOMAIN: ClassVar[RelationField] = RelationField("dataDomain")
    """
    TBC
    """
    OUTPUT_PORTS: ClassVar[RelationField] = RelationField("outputPorts")
    """
    TBC
    """
    INPUT_PORTS: ClassVar[RelationField] = RelationField("inputPorts")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "data_product_status",
        "daap_status",
        "data_product_criticality",
        "daap_criticality",
        "data_product_sensitivity",
        "daap_sensitivity",
        "data_product_visibility",
        "daap_visibility",
        "data_product_assets_d_s_l",
        "data_product_assets_playbook_filter",
        "data_product_score_value",
        "data_product_score_updated_at",
        "daap_visibility_users",
        "daap_visibility_groups",
        "data_domain",
        "output_ports",
        "input_ports",
    ]

    @property
    def data_product_status(self) -> Optional[DataProductStatus]:
        return None if self.attributes is None else self.attributes.data_product_status

    @data_product_status.setter
    def data_product_status(self, data_product_status: Optional[DataProductStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_product_status = data_product_status

    @property
    def daap_status(self) -> Optional[DataProductStatus]:
        return None if self.attributes is None else self.attributes.daap_status

    @daap_status.setter
    def daap_status(self, daap_status: Optional[DataProductStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.daap_status = daap_status

    @property
    def data_product_criticality(self) -> Optional[DataProductCriticality]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_product_criticality
        )

    @data_product_criticality.setter
    def data_product_criticality(
        self, data_product_criticality: Optional[DataProductCriticality]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_product_criticality = data_product_criticality

    @property
    def daap_criticality(self) -> Optional[DataProductCriticality]:
        return None if self.attributes is None else self.attributes.daap_criticality

    @daap_criticality.setter
    def daap_criticality(self, daap_criticality: Optional[DataProductCriticality]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.daap_criticality = daap_criticality

    @property
    def data_product_sensitivity(self) -> Optional[DataProductSensitivity]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_product_sensitivity
        )

    @data_product_sensitivity.setter
    def data_product_sensitivity(
        self, data_product_sensitivity: Optional[DataProductSensitivity]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_product_sensitivity = data_product_sensitivity

    @property
    def daap_sensitivity(self) -> Optional[DataProductSensitivity]:
        return None if self.attributes is None else self.attributes.daap_sensitivity

    @daap_sensitivity.setter
    def daap_sensitivity(self, daap_sensitivity: Optional[DataProductSensitivity]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.daap_sensitivity = daap_sensitivity

    @property
    def data_product_visibility(self) -> Optional[DataProductVisibility]:
        return (
            None if self.attributes is None else self.attributes.data_product_visibility
        )

    @data_product_visibility.setter
    def data_product_visibility(
        self, data_product_visibility: Optional[DataProductVisibility]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_product_visibility = data_product_visibility

    @property
    def daap_visibility(self) -> Optional[DataProductVisibility]:
        return None if self.attributes is None else self.attributes.daap_visibility

    @daap_visibility.setter
    def daap_visibility(self, daap_visibility: Optional[DataProductVisibility]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.daap_visibility = daap_visibility

    @property
    def data_product_assets_d_s_l(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_product_assets_d_s_l
        )

    @data_product_assets_d_s_l.setter
    def data_product_assets_d_s_l(self, data_product_assets_d_s_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_product_assets_d_s_l = data_product_assets_d_s_l

    @property
    def data_product_assets_playbook_filter(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_product_assets_playbook_filter
        )

    @data_product_assets_playbook_filter.setter
    def data_product_assets_playbook_filter(
        self, data_product_assets_playbook_filter: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_product_assets_playbook_filter = (
            data_product_assets_playbook_filter
        )

    @property
    def data_product_score_value(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_product_score_value
        )

    @data_product_score_value.setter
    def data_product_score_value(self, data_product_score_value: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_product_score_value = data_product_score_value

    @property
    def data_product_score_updated_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_product_score_updated_at
        )

    @data_product_score_updated_at.setter
    def data_product_score_updated_at(
        self, data_product_score_updated_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_product_score_updated_at = data_product_score_updated_at

    @property
    def daap_visibility_users(self) -> Optional[Set[str]]:
        return (
            None if self.attributes is None else self.attributes.daap_visibility_users
        )

    @daap_visibility_users.setter
    def daap_visibility_users(self, daap_visibility_users: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.daap_visibility_users = daap_visibility_users

    @property
    def daap_visibility_groups(self) -> Optional[Set[str]]:
        return (
            None if self.attributes is None else self.attributes.daap_visibility_groups
        )

    @daap_visibility_groups.setter
    def daap_visibility_groups(self, daap_visibility_groups: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.daap_visibility_groups = daap_visibility_groups

    @property
    def data_domain(self) -> Optional[DataDomain]:
        return None if self.attributes is None else self.attributes.data_domain

    @data_domain.setter
    def data_domain(self, data_domain: Optional[DataDomain]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_domain = data_domain

    @property
    def output_ports(self) -> Optional[List[Asset]]:
        return None if self.attributes is None else self.attributes.output_ports

    @output_ports.setter
    def output_ports(self, output_ports: Optional[List[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_ports = output_ports

    @property
    def input_ports(self) -> Optional[List[Asset]]:
        return None if self.attributes is None else self.attributes.input_ports

    @input_ports.setter
    def input_ports(self, input_ports: Optional[List[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_ports = input_ports

    class Attributes(DataMesh.Attributes):
        data_product_status: Optional[DataProductStatus] = Field(
            default=None, description=""
        )
        daap_status: Optional[DataProductStatus] = Field(default=None, description="")
        data_product_criticality: Optional[DataProductCriticality] = Field(
            default=None, description=""
        )
        daap_criticality: Optional[DataProductCriticality] = Field(
            default=None, description=""
        )
        data_product_sensitivity: Optional[DataProductSensitivity] = Field(
            default=None, description=""
        )
        daap_sensitivity: Optional[DataProductSensitivity] = Field(
            default=None, description=""
        )
        data_product_visibility: Optional[DataProductVisibility] = Field(
            default=None, description=""
        )
        daap_visibility: Optional[DataProductVisibility] = Field(
            default=None, description=""
        )
        data_product_assets_d_s_l: Optional[str] = Field(default=None, description="")
        data_product_assets_playbook_filter: Optional[str] = Field(
            default=None, description=""
        )
        data_product_score_value: Optional[float] = Field(default=None, description="")
        data_product_score_updated_at: Optional[datetime] = Field(
            default=None, description=""
        )
        daap_visibility_users: Optional[Set[str]] = Field(default=None, description="")
        daap_visibility_groups: Optional[Set[str]] = Field(default=None, description="")
        data_domain: Optional[DataDomain] = Field(
            default=None, description=""
        )  # relationship
        output_ports: Optional[List[Asset]] = Field(
            default=None, description=""
        )  # relationship
        input_ports: Optional[List[Asset]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: StrictStr,
            domain_qualified_name: StrictStr,
            asset_selection: IndexSearchRequest,
        ) -> DataProduct.Attributes:
            validate_required_fields(
                ["name", "domain_qualified_name", "asset_selection"],
                [name, domain_qualified_name, asset_selection],
            )
            ASSETS_PLAYBOOK_FILTER = (
                '{"condition":"AND","isGroupLocked":false,"rules":[]}'
            )
            return DataProduct.Attributes(
                name=name,
                data_product_assets_d_s_l=DataProductsAssetsDSL(
                    query=asset_selection
                ).to_string(),
                data_domain=DataDomain.ref_by_qualified_name(domain_qualified_name),
                qualified_name=f"{domain_qualified_name}/product/{name}",
                data_product_assets_playbook_filter=ASSETS_PLAYBOOK_FILTER,
                parent_domain_qualified_name=domain_qualified_name,
                super_domain_qualified_name=DataMesh.get_super_domain_qualified_name(
                    domain_qualified_name
                ),
                daap_status=DataProductStatus.ACTIVE,
            )

    attributes: DataProduct.Attributes = Field(
        default_factory=lambda: DataProduct.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa
from .data_domain import DataDomain  # noqa
