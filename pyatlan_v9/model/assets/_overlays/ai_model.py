# STDLIB_IMPORT: from typing import Dict, List
# IMPORT: from pyatlan.model.enums import AIDatasetType, AtlanConnectorType
# IMPORT: from pyatlan.utils import to_camel_case
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields
# INTERNAL_IMPORT: from pyatlan.model.transform import get_type
# INTERNAL_IMPORT: from pyatlan.model.assets.process import Process

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        ai_model_status: str,
        owner_groups: Union[set[str], None] = None,
        owner_users: Union[set[str], None] = None,
        ai_model_version: Union[str, None] = None,
    ) -> "AIModel":
        """Create a new AIModel asset."""
        validate_required_fields(["name", "ai_model_status"], [name, ai_model_status])
        name_camel_case = to_camel_case(name)
        return cls(
            name=name,
            qualified_name=f"default/ai/aiapplication/{name_camel_case}",
            connector_name=AtlanConnectorType.AI.value,
            ai_model_status=ai_model_status,
            ai_model_version=ai_model_version
            if ai_model_version is not None
            else UNSET,
            owner_groups=owner_groups if owner_groups is not None else UNSET,
            owner_users=owner_users if owner_users is not None else UNSET,
        )

    @classmethod
    def processes_creator(
        cls,
        ai_model: "AIModel",
        dataset_dict: Dict[AIDatasetType, list],
    ) -> List[Process]:
        """
        Create Process assets representing AI model lineage with dataset assets.
        """
        if not ai_model.guid or not ai_model.name:
            raise ValueError("AI model must have both guid and name attributes")

        process_list: List[Process] = []
        for dataset_type, assets in dataset_dict.items():
            for asset in assets:
                asset_cls = get_type(getattr(asset, "type_name", "Asset"))
                asset_guid = getattr(asset, "guid", None)
                asset_name = getattr(asset, "name", None)
                if not asset_guid or not asset_name:
                    continue

                if dataset_type == AIDatasetType.OUTPUT:
                    process_name = f"{ai_model.name} -> {asset_name}"
                    process_created = Process.creator(
                        name=process_name,
                        connection_qualified_name="default/ai/dataset",
                        inputs=[AIModel.ref_by_guid(guid=ai_model.guid)],
                        outputs=[asset_cls.ref_by_guid(guid=asset_guid)],
                        extra_hash_params={dataset_type.value},
                    )
                else:
                    process_name = f"{asset_name} -> {ai_model.name}"
                    process_created = Process.creator(
                        name=process_name,
                        connection_qualified_name="default/ai/dataset",
                        inputs=[asset_cls.ref_by_guid(guid=asset_guid)],
                        outputs=[AIModel.ref_by_guid(guid=ai_model.guid)],
                        extra_hash_params={dataset_type.value},
                    )

                process_created.ai_dataset_type = dataset_type
                process_list.append(process_created)

        return process_list

    @classmethod
    def processes_batch_save(
        cls, client: Any, process_list: List[Process]
    ) -> List[Any]:
        """
        Save Process assets in batches to reduce API payload size.
        """
        batch_size = 20
        responses: List[Any] = []
        for i in range(0, len(process_list), batch_size):
            responses.append(client.asset.save(process_list[i : i + batch_size]))
        return responses

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "AIModel":
        """Create an AIModel instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "AIModel":
        """Return only fields required for update operations."""
        return AIModel.updater(qualified_name=self.qualified_name, name=self.name)
