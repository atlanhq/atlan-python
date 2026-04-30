# STDLIB_IMPORT: import re
# STDLIB_IMPORT: from json import loads, JSONDecodeError
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
        validate_required_fields(["asset_qualified_name"], [asset_qualified_name])
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
                contract_name = f"Data contract for {contract_spec.dataset or default_dataset}"
                contract_spec = contract_spec.to_yaml()
            else:
                is_dataset_found = re.search(r"dataset:\s*([^\s#]+)", contract_spec or default_dataset)
                dataset = is_dataset_found.group(1) if is_dataset_found else None
                contract_name = f"Data contract for {dataset or default_dataset}"
        return cls(
            name=contract_name,
            qualified_name=f"{asset_qualified_name}/contract",
            data_contract_json=contract_json,
            data_contract_spec=contract_spec,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "DataContract":
        """Create a DataContract instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "DataContract":
        """Return only required fields for update operations."""
        return DataContract.updater(qualified_name=self.qualified_name, name=self.name)
