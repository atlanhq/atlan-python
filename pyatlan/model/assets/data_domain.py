# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional
from warnings import warn

from pydantic.v1 import Field, StrictStr, validator

from pyatlan.model.fields.atlan_fields import RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .asset import SelfAsset
from .data_mesh import DataMesh


class DataDomain(DataMesh):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: StrictStr,
        parent_domain_qualified_name: Optional[StrictStr] = None,
    ) -> DataDomain:
        validate_required_fields(["name"], [name])
        attributes = DataDomain.Attributes.create(
            name=name,
            parent_domain_qualified_name=parent_domain_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(
        cls,
        *,
        name: StrictStr,
        parent_domain_qualified_name: Optional[StrictStr] = None,
    ) -> DataDomain:
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
            parent_domain_qualified_name=parent_domain_qualified_name,
        )

    @classmethod
    def updater(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = "",
    ) -> SelfAsset:
        validate_required_fields(["name", "qualified_name"], [name, qualified_name])
        fields = qualified_name.split("/")
        if len(fields) < 3:
            raise ValueError(f"Invalid data domain qualified_name: {qualified_name}")
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

    type_name: str = Field(default="DataDomain", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataDomain":
            raise ValueError("must be DataDomain")
        return v

    def __setattr__(self, name, value):
        if name in DataDomain._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_PRODUCTS: ClassVar[RelationField] = RelationField("dataProducts")
    """
    TBC
    """
    STAKEHOLDERS: ClassVar[RelationField] = RelationField("stakeholders")
    """
    TBC
    """
    PARENT_DOMAIN: ClassVar[RelationField] = RelationField("parentDomain")
    """
    TBC
    """
    SUB_DOMAINS: ClassVar[RelationField] = RelationField("subDomains")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "data_products",
        "stakeholders",
        "parent_domain",
        "sub_domains",
    ]

    @property
    def data_products(self) -> Optional[List[DataProduct]]:
        return None if self.attributes is None else self.attributes.data_products

    @data_products.setter
    def data_products(self, data_products: Optional[List[DataProduct]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_products = data_products

    @property
    def stakeholders(self) -> Optional[List[Stakeholder]]:
        return None if self.attributes is None else self.attributes.stakeholders

    @stakeholders.setter
    def stakeholders(self, stakeholders: Optional[List[Stakeholder]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.stakeholders = stakeholders

    @property
    def parent_domain(self) -> Optional[DataDomain]:
        return None if self.attributes is None else self.attributes.parent_domain

    @parent_domain.setter
    def parent_domain(self, parent_domain: Optional[DataDomain]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_domain = parent_domain

    @property
    def sub_domains(self) -> Optional[List[DataDomain]]:
        return None if self.attributes is None else self.attributes.sub_domains

    @sub_domains.setter
    def sub_domains(self, sub_domains: Optional[List[DataDomain]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sub_domains = sub_domains

    class Attributes(DataMesh.Attributes):
        data_products: Optional[List[DataProduct]] = Field(
            default=None, description=""
        )  # relationship
        stakeholders: Optional[List[Stakeholder]] = Field(
            default=None, description=""
        )  # relationship
        parent_domain: Optional[DataDomain] = Field(
            default=None, description=""
        )  # relationship
        sub_domains: Optional[List[DataDomain]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: StrictStr,
            parent_domain_qualified_name: Optional[StrictStr] = None,
        ) -> DataDomain.Attributes:
            validate_required_fields(["name"], [name])
            parent_domain = None
            super_domain_qualified_name = None

            # In case of sub-domain
            if parent_domain_qualified_name:
                parent_domain = DataDomain.ref_by_qualified_name(
                    parent_domain_qualified_name
                )
                super_domain_qualified_name = DataMesh.get_super_domain_qualified_name(
                    parent_domain_qualified_name
                )

            return DataDomain.Attributes(
                name=name,
                qualified_name=name,
                parent_domain=parent_domain,
                parent_domain_qualified_name=parent_domain_qualified_name,
                super_domain_qualified_name=super_domain_qualified_name,
            )

    attributes: DataDomain.Attributes = Field(
        default_factory=lambda: DataDomain.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .data_product import DataProduct  # noqa
from .stakeholder import Stakeholder  # noqa
