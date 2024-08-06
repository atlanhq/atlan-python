# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional
from urllib.parse import quote, unquote
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .resource import Resource


class Readme(Resource):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls, *, asset: Asset, content: str, asset_name: Optional[str] = None
    ) -> Readme:
        return Readme(
            attributes=Readme.Attributes.create(
                asset=asset, content=content, asset_name=asset_name
            )
        )

    @classmethod
    @init_guid
    def create(
        cls, *, asset: Asset, content: str, asset_name: Optional[str] = None
    ) -> Readme:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(asset=asset, content=content, asset_name=asset_name)

    @property
    def description(self) -> Optional[str]:
        ret_value = self.attributes.description
        return unquote(ret_value) if ret_value is not None else ret_value

    @description.setter
    def description(self, description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.description = (
            quote(description) if description is not None else description
        )

    type_name: str = Field(default="Readme", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Readme":
            raise ValueError("must be Readme")
        return v

    def __setattr__(self, name, value):
        if name in Readme._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SEE_ALSO: ClassVar[RelationField] = RelationField("seeAlso")
    """
    TBC
    """
    ASSET: ClassVar[RelationField] = RelationField("asset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "see_also",
        "asset",
    ]

    @property
    def see_also(self) -> Optional[List[Readme]]:
        return None if self.attributes is None else self.attributes.see_also

    @see_also.setter
    def see_also(self, see_also: Optional[List[Readme]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.see_also = see_also

    @property
    def asset(self) -> Optional[Asset]:
        return None if self.attributes is None else self.attributes.asset

    @asset.setter
    def asset(self, asset: Optional[Asset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset = asset

    class Attributes(Resource.Attributes):
        see_also: Optional[List[Readme]] = Field(
            default=None, description=""
        )  # relationship
        asset: Optional[Asset] = Field(default=None, description="")  # relationship

        @classmethod
        @init_guid
        def create(
            cls, *, asset: Asset, content: str, asset_name: Optional[str] = None
        ) -> Readme.Attributes:
            validate_required_fields(["asset", "content"], [asset, content])
            if not asset.name or len(asset.name) < 1:
                if not asset_name:
                    raise ValueError(
                        "asset_name is required when name is not available from asset"
                    )
            elif asset_name:
                raise ValueError(
                    "asset_name can not be given when name is available from asset"
                )
            else:
                asset_name = asset.name
            return Readme.Attributes(
                qualified_name=f"{asset.guid}/readme",
                name=f"{asset_name} Readme",
                asset=asset,
                description=quote(content),
            )

    attributes: Readme.Attributes = Field(
        default_factory=lambda: Readme.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa
