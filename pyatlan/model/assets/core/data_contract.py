# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from json import loads
from json.decoder import JSONDecodeError
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.errors import ErrorCode
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .catalog import Catalog


class DataContract(Catalog):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, asset_qualified_name: str, contract_json: str) -> DataContract:
        validate_required_fields(
            ["asset_qualified_name", "contract_json"],
            [asset_qualified_name, contract_json],
        )
        attributes = DataContract.Attributes.creator(
            asset_qualified_name=asset_qualified_name,
            contract_json=contract_json,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="DataContract", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataContract":
            raise ValueError("must be DataContract")
        return v

    def __setattr__(self, name, value):
        if name in DataContract._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_CONTRACT_JSON: ClassVar[KeywordField] = KeywordField(
        "dataContractJson", "dataContractJson"
    )
    """
    Actual content of the contract in JSON string format. Any changes to this string should create a new instance (with new sequential version number).
    """  # noqa: E501
    DATA_CONTRACT_VERSION: ClassVar[NumericField] = NumericField(
        "dataContractVersion", "dataContractVersion"
    )
    """
    Version of the contract.
    """
    DATA_CONTRACT_ASSET_GUID: ClassVar[KeywordField] = KeywordField(
        "dataContractAssetGuid", "dataContractAssetGuid"
    )
    """
    Unique identifier of the asset associated with this data contract.
    """

    DATA_CONTRACT_ASSET_LATEST: ClassVar[RelationField] = RelationField(
        "dataContractAssetLatest"
    )
    """
    TBC
    """
    DATA_CONTRACT_ASSET_CERTIFIED: ClassVar[RelationField] = RelationField(
        "dataContractAssetCertified"
    )
    """
    TBC
    """
    DATA_CONTRACT_PREVIOUS_VERSION: ClassVar[RelationField] = RelationField(
        "dataContractPreviousVersion"
    )
    """
    TBC
    """
    DATA_CONTRACT_NEXT_VERSION: ClassVar[RelationField] = RelationField(
        "dataContractNextVersion"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "data_contract_json",
        "data_contract_version",
        "data_contract_asset_guid",
        "data_contract_asset_latest",
        "data_contract_asset_certified",
        "data_contract_previous_version",
        "data_contract_next_version",
    ]

    @property
    def data_contract_json(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_contract_json

    @data_contract_json.setter
    def data_contract_json(self, data_contract_json: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_contract_json = data_contract_json

    @property
    def data_contract_version(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.data_contract_version
        )

    @data_contract_version.setter
    def data_contract_version(self, data_contract_version: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_contract_version = data_contract_version

    @property
    def data_contract_asset_guid(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_contract_asset_guid
        )

    @data_contract_asset_guid.setter
    def data_contract_asset_guid(self, data_contract_asset_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_contract_asset_guid = data_contract_asset_guid

    @property
    def data_contract_asset_latest(self) -> Optional[Asset]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_contract_asset_latest
        )

    @data_contract_asset_latest.setter
    def data_contract_asset_latest(self, data_contract_asset_latest: Optional[Asset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_contract_asset_latest = data_contract_asset_latest

    @property
    def data_contract_asset_certified(self) -> Optional[Asset]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_contract_asset_certified
        )

    @data_contract_asset_certified.setter
    def data_contract_asset_certified(
        self, data_contract_asset_certified: Optional[Asset]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_contract_asset_certified = data_contract_asset_certified

    @property
    def data_contract_previous_version(self) -> Optional[DataContract]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_contract_previous_version
        )

    @data_contract_previous_version.setter
    def data_contract_previous_version(
        self, data_contract_previous_version: Optional[DataContract]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_contract_previous_version = data_contract_previous_version

    @property
    def data_contract_next_version(self) -> Optional[DataContract]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_contract_next_version
        )

    @data_contract_next_version.setter
    def data_contract_next_version(
        self, data_contract_next_version: Optional[DataContract]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_contract_next_version = data_contract_next_version

    class Attributes(Catalog.Attributes):
        data_contract_json: Optional[str] = Field(default=None, description="")
        data_contract_version: Optional[int] = Field(default=None, description="")
        data_contract_asset_guid: Optional[str] = Field(default=None, description="")
        data_contract_asset_latest: Optional[Asset] = Field(
            default=None, description=""
        )  # relationship
        data_contract_asset_certified: Optional[Asset] = Field(
            default=None, description=""
        )  # relationship
        data_contract_previous_version: Optional[DataContract] = Field(
            default=None, description=""
        )  # relationship
        data_contract_next_version: Optional[DataContract] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls, *, asset_qualified_name: str, contract_json: str
        ) -> DataContract.Attributes:
            validate_required_fields(
                ["asset_qualified_name", "contract_json"],
                [asset_qualified_name, contract_json],
            )
            try:
                contract_name = f"Data contract for {loads(contract_json)['dataset']}"
            except (JSONDecodeError, KeyError):
                raise ErrorCode.INVALID_CONTRACT_JSON.exception_with_parameters()

            return DataContract.Attributes(
                name=contract_name,
                qualified_name=f"{asset_qualified_name}/contract",
                data_contract_json=contract_json,
            )

    attributes: DataContract.Attributes = Field(
        default_factory=lambda: DataContract.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa
