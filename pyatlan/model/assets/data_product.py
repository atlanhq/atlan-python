# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic.v1 import Field, StrictStr, validator

from pyatlan.model.enums import (
    AtlanIcon,
    DataProductCriticality,
    DataProductSensitivity,
    DataProductStatus,
)
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.model.search import IndexSearchRequest
from pyatlan.utils import (
    init_guid,
    to_camel_case,
    validate_required_fields,
    validate_single_required_field,
)

from .asset import SelfAsset
from .data_mesh import DataMesh


class DataProduct(DataMesh):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(
        cls,
        *,
        name: StrictStr,
        assets: IndexSearchRequest,
        icon: Optional[AtlanIcon] = None,
        domain: Optional[DataDomain] = None,
        domain_qualified_name: Optional[StrictStr] = None,
    ) -> DataProduct:
        validate_required_fields(["name", "assets"], [name, assets])
        assets_dsl = assets.get_dsl_str()
        attributes = DataProduct.Attributes.create(
            name=name,
            assets_dsl=assets_dsl,
            icon=icon,
            domain=domain,
            domain_qualified_name=domain_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    def create_for_modification(
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
        if len(fields) != 3:
            raise ValueError(f"Invalid data product qualified_name: {qualified_name}")
        return cls(
            attributes=cls.Attributes(
                qualified_name=qualified_name,
                name=name,
            )
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
    DATA_PRODUCT_CRITICALITY: ClassVar[KeywordField] = KeywordField(
        "dataProductCriticality", "dataProductCriticality"
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

    DATA_DOMAIN: ClassVar[RelationField] = RelationField("dataDomain")
    """
    TBC
    """
    OUTPUT_PORTS: ClassVar[RelationField] = RelationField("outputPorts")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "data_product_status",
        "data_product_criticality",
        "data_product_sensitivity",
        "data_product_assets_d_s_l",
        "data_product_assets_playbook_filter",
        "data_domain",
        "output_ports",
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
    def data_domain(self) -> Optional[DataDomain]:
        return None if self.attributes is None else self.attributes.data_domain

    @data_domain.setter
    def data_domain(self, data_domain: Optional[DataDomain]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_domain = data_domain

    @property
    def output_ports(self) -> Optional[list[Asset]]:
        return None if self.attributes is None else self.attributes.output_ports

    @output_ports.setter
    def output_ports(self, output_ports: Optional[list[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_ports = output_ports

    class Attributes(DataMesh.Attributes):
        data_product_status: Optional[DataProductStatus] = Field(
            default=None, description=""
        )
        data_product_criticality: Optional[DataProductCriticality] = Field(
            default=None, description=""
        )
        data_product_sensitivity: Optional[DataProductSensitivity] = Field(
            default=None, description=""
        )
        data_product_assets_d_s_l: Optional[str] = Field(default=None, description="")
        data_product_assets_playbook_filter: Optional[str] = Field(
            default=None, description=""
        )
        data_domain: Optional[DataDomain] = Field(
            default=None, description=""
        )  # relationship
        output_ports: Optional[list[Asset]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: StrictStr,
            assets_dsl: StrictStr,
            icon: Optional[AtlanIcon] = None,
            domain: Optional[DataDomain] = None,
            domain_qualified_name: Optional[StrictStr] = None,
        ) -> DataProduct.Attributes:
            validate_required_fields(["name"], [name])
            validate_single_required_field(
                ["domain", "domain_qualified_name"],
                [domain, domain_qualified_name],
            )
            if domain_qualified_name:
                domain = DataDomain()
                domain.unique_attributes = {"qualifiedName": domain_qualified_name}
            icon_str = icon.value if icon is not None else None
            camel_case_name = to_camel_case(name)
            return DataProduct.Attributes(
                name=name,
                data_product_assets_d_s_l=assets_dsl,
                data_domain=domain,
                qualified_name=f"default/product/{camel_case_name}",
                asset_icon=icon_str,
            )

    attributes: "DataProduct.Attributes" = Field(
        default_factory=lambda: DataProduct.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


from .asset import Asset  # noqa
from .data_domain import DataDomain  # noqa
