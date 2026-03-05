# STDLIB_IMPORT: import re
# IMPORT: from pyatlan.errors import ErrorCode
# INTERNAL_IMPORT: from pyatlan.model.contract import DataContractSpec
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        asset_qualified_name: str,
        contract_json: Union[str, None] = None,
        contract_spec: Union[DataContractSpec, str, None] = None,
    ) -> "DataContract":
        """Create a new DataContract asset."""
        attrs = DataContract.Attributes.creator(
            asset_qualified_name=asset_qualified_name,
            contract_json=contract_json,
            contract_spec=contract_spec,
        )
        return cls(
            name=attrs.name,
            qualified_name=attrs.qualified_name,
            data_contract_json=attrs.data_contract_json,
            data_contract_spec=attrs.data_contract_spec,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "DataContract":
        """Create a DataContract instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "DataContract":
        """Return only required fields for update operations."""
        return DataContract.updater(qualified_name=self.qualified_name, name=self.name)
