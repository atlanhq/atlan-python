# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from json import JSONDecodeError, loads
from typing import TYPE_CHECKING, ClassVar, List, Optional, Tuple, Type, Union

from pydantic.v1 import Field, validator

from pyatlan.errors import ErrorCode
from pyatlan.model.contract import DataContractSpec
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .catalog import Catalog

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.response import AssetMutationResponse


class DataContract(Catalog):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        asset_qualified_name: str,
        asset_type: Type[Asset],
        contract_json: Optional[str] = None,
        contract_spec: Optional[Union[DataContractSpec, str]] = None,
    ) -> DataContract:
        validate_required_fields(
            ["asset_qualified_name"],
            [asset_qualified_name],
        )
        attributes = DataContract.Attributes.creator(
            asset_qualified_name=asset_qualified_name,
            asset_type=asset_type,
            contract_json=contract_json,
            contract_spec=contract_spec,
        )
        return cls(attributes=attributes)

    @staticmethod
    def save(
        client: "AtlanClient",
        contract: "DataContract",
    ) -> "AssetMutationResponse":
        """Save a DataContract.

        The contract's ``data_contract_asset_latest`` relationship (set by
        ``creator()``) links the contract to the governed asset automatically.

        :param client: connectivity to an Atlan tenant
        :param contract: DataContract to save (from ``DataContract.creator()``)
        :returns: the result of the save
        """
        return client.asset.save(contract)

    @staticmethod
    def delete(
        client: "AtlanClient",
        contract_guid: str,
        linked_asset_guid: str,
    ) -> "Tuple[AssetMutationResponse, AssetMutationResponse]":
        """Delete (purge) a DataContract and clean up the linked asset.

        Uses hard-delete to avoid qualified-name conflicts on re-creation,
        and clears ``hasContract``, ``dataContractLatest``, and
        ``dataContractLatestCertified`` on the linked asset.

        :param client: connectivity to an Atlan tenant
        :param contract_guid: GUID of the DataContract to delete
        :param linked_asset_guid: GUID of the asset the contract was linked to
        :returns: tuple of (contract delete response, asset update response)
        """
        from pyatlan.model.assets.core.indistinct_asset import IndistinctAsset

        delete_response = client.asset.purge_by_guid(contract_guid)

        asset_update = IndistinctAsset()
        asset_update.guid = linked_asset_guid
        asset_update.has_contract = False
        asset_update.data_contract_latest = None  # type: ignore[assignment]
        asset_update.data_contract_latest_certified = None  # type: ignore[assignment]
        asset_response = client.asset.save(asset_update)
        return delete_response, asset_response

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

    DATA_CONTRACT_JSON: ClassVar[TextField] = TextField(
        "dataContractJson", "dataContractJson"
    )
    """
    (Deprecated) Replaced by dataContractSpec attribute.
    """
    DATA_CONTRACT_SPEC: ClassVar[TextField] = TextField(
        "dataContractSpec", "dataContractSpec"
    )
    """
    Actual content of the contract in YAML string format. Any changes to this string should create a new instance (with new sequential version number).
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

    DATA_CONTRACT_ASSET_CERTIFIED: ClassVar[RelationField] = RelationField(
        "dataContractAssetCertified"
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
    DATA_CONTRACT_ASSET_LATEST: ClassVar[RelationField] = RelationField(
        "dataContractAssetLatest"
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

    _convenience_properties: ClassVar[List[str]] = [
        "data_contract_json",
        "data_contract_spec",
        "data_contract_version",
        "data_contract_asset_guid",
        "data_contract_asset_certified",
        "data_contract_next_version",
        "data_contract_asset_latest",
        "data_contract_previous_version",
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
    def data_contract_spec(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_contract_spec

    @data_contract_spec.setter
    def data_contract_spec(self, data_contract_spec: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_contract_spec = data_contract_spec

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

    class Attributes(Catalog.Attributes):
        data_contract_json: Optional[str] = Field(default=None, description="")
        data_contract_spec: Optional[str] = Field(default=None, description="")
        data_contract_version: Optional[int] = Field(default=None, description="")
        data_contract_asset_guid: Optional[str] = Field(default=None, description="")
        data_contract_asset_certified: Optional[Asset] = Field(
            default=None, description=""
        )  # relationship
        data_contract_next_version: Optional[DataContract] = Field(
            default=None, description=""
        )  # relationship
        data_contract_asset_latest: Optional[Asset] = Field(
            default=None, description=""
        )  # relationship
        data_contract_previous_version: Optional[DataContract] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            asset_qualified_name: str,
            asset_type: Type[Asset],
            contract_json: Optional[str] = None,
            contract_spec: Optional[Union[DataContractSpec, str]] = None,
        ) -> DataContract.Attributes:
            from re import search

            validate_required_fields(
                ["asset_qualified_name"],
                [asset_qualified_name],
            )
            if not (contract_json or contract_spec):
                raise ValueError(
                    "At least one of `contract_json` or `contract_spec` "
                    "must be provided to create a contract."
                )
            if contract_json and contract_spec:
                raise ValueError(
                    "Both `contract_json` and `contract_spec` cannot be "
                    "provided simultaneously to create a contract."
                )
            last_slash_index = asset_qualified_name.rfind("/")
            default_dataset = asset_qualified_name[last_slash_index + 1 :]  # noqa

            if contract_json:
                try:
                    contract_name = f"Data contract for {loads(contract_json)['dataset'] or default_dataset}"
                except (JSONDecodeError, KeyError):
                    raise ErrorCode.INVALID_CONTRACT_JSON.exception_with_parameters()
            else:
                if isinstance(contract_spec, DataContractSpec):
                    contract_name = (
                        "Data contract for "
                        f"{contract_spec.dataset or default_dataset}"  # type: ignore[union-attr, attr-defined]
                    )
                    contract_spec = contract_spec.to_yaml()
                else:
                    is_dataset_found = search(
                        r"dataset:\s*([^\s#]+)", contract_spec or default_dataset
                    )
                    dataset = None
                    if is_dataset_found:
                        dataset = is_dataset_found.group(1)
                    contract_name = f"Data contract for {dataset or default_dataset}"

            return DataContract.Attributes(
                name=contract_name,
                qualified_name=f"{asset_qualified_name}/contract",
                data_contract_json=contract_json,
                data_contract_spec=contract_spec,  # type: ignore[arg-type]
                data_contract_asset_latest=asset_type.ref_by_qualified_name(
                    asset_qualified_name
                ),
            )

    attributes: DataContract.Attributes = Field(
        default_factory=lambda: DataContract.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa: E402, F401
