# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional, Set, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AIDatasetType, AIModelStatus, AtlanConnectorType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField
from pyatlan.utils import init_guid, to_camel_case, validate_required_fields

from .a_i import AI
from .asset import Asset
from .process import Process


class AIModel(AI):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        ai_model_status: AIModelStatus,
    ) -> AIModel: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        ai_model_status: AIModelStatus,
        owner_groups: Set[str],
        owner_users: Set[str],
        ai_model_version: str,
    ) -> AIModel: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        ai_model_status: AIModelStatus,
        owner_groups: Optional[Set[str]] = None,
        owner_users: Optional[Set[str]] = None,
        ai_model_version: Optional[str] = None,
    ) -> AIModel:
        validate_required_fields(
            ["name", "ai_model_status"],
            [name, ai_model_status],
        )
        attributes = AIModel.Attributes.creator(
            name=name,
            ai_model_status=ai_model_status,
            owner_groups=owner_groups,
            owner_users=owner_users,
            ai_model_version=ai_model_version,
        )
        return cls(attributes=attributes)

    @classmethod
    def processes_creator(
        cls,
        ai_model: AIModel,
        dataset_dict: Dict[AIDatasetType, list],
    ) -> List[Process]:
        """
        Creates a list of Process objects representing the relationships between an AI model and its datasets.

        :param ai_model: the AI model for which to create processes
        :param dataset_dict: dictionary mapping AI dataset types to lists of assets
        :returns: list of Process objects representing the AI model's data lineage
        :raises ValueError: when the AI model is missing required attributes (guid or name)
        """
        if not ai_model.guid or not ai_model.name:
            raise ValueError("AI model must have both guid and name attributes")
        process_list = []
        for key, value_list in dataset_dict.items():
            for value in value_list:
                asset_type = Asset._convert_to_real_type_(value)
                if key == AIDatasetType.OUTPUT:
                    process_name = f"{ai_model.name} -> {value.name}"
                    process_created = Process.creator(
                        name=process_name,
                        connection_qualified_name="default/ai/dataset",
                        inputs=[AIModel.ref_by_guid(guid=ai_model.guid)],
                        outputs=[asset_type.ref_by_guid(guid=value.guid)],  # type: ignore
                        extra_hash_params={key.value},
                    )
                    process_created.ai_dataset_type = key
                else:
                    process_name = f"{value.name} -> {ai_model.name}"
                    process_created = Process.creator(
                        name=process_name,
                        connection_qualified_name="default/ai/dataset",
                        inputs=[asset_type.ref_by_guid(guid=value.guid)],  # type: ignore
                        outputs=[AIModel.ref_by_guid(guid=ai_model.guid)],
                        extra_hash_params={key.value},
                    )
                    process_created.ai_dataset_type = key
                process_list.append(process_created)

        return process_list

    @classmethod
    def processes_batch_save(cls, client, process_list: List[Process]) -> List:
        """
        Saves a list of Process objects to Atlan in batches to optimize performance.
        We save the processes in batches of 20.

        :param client: Atlan client instance for making API calls
        :param process_list: list of Process objects to save
        :returns: list of API responses from each batch save operation
        """
        batch_size = 20
        total_processes = len(process_list)
        responses = []

        for i in range(0, total_processes, batch_size):
            batch = process_list[i : i + batch_size]
            response = client.asset.save(batch)
            responses.append(response)

        return responses

    type_name: str = Field(default="AIModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AIModel":
            raise ValueError("must be AIModel")
        return v

    def __setattr__(self, name, value):
        if name in AIModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AI_MODEL_DATASETS_DSL: ClassVar[TextField] = TextField(
        "aiModelDatasetsDSL", "aiModelDatasetsDSL"
    )
    """
    Search DSL used to define which assets/datasets are part of the AI model.
    """
    AI_MODEL_STATUS: ClassVar[KeywordField] = KeywordField(
        "aiModelStatus", "aiModelStatus"
    )
    """
    Status of the AI model.
    """
    AI_MODEL_VERSION: ClassVar[KeywordField] = KeywordField(
        "aiModelVersion", "aiModelVersion"
    )
    """
    Version of the AI model.
    """

    AI_MODEL_VERSIONS: ClassVar[RelationField] = RelationField("aiModelVersions")
    """
    TBC
    """
    APPLICATIONS: ClassVar[RelationField] = RelationField("applications")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "ai_model_datasets_d_s_l",
        "ai_model_status",
        "ai_model_version",
        "ai_model_versions",
        "applications",
    ]

    @property
    def ai_model_datasets_d_s_l(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.ai_model_datasets_d_s_l
        )

    @ai_model_datasets_d_s_l.setter
    def ai_model_datasets_d_s_l(self, ai_model_datasets_d_s_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model_datasets_d_s_l = ai_model_datasets_d_s_l

    @property
    def ai_model_status(self) -> Optional[AIModelStatus]:
        return None if self.attributes is None else self.attributes.ai_model_status

    @ai_model_status.setter
    def ai_model_status(self, ai_model_status: Optional[AIModelStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model_status = ai_model_status

    @property
    def ai_model_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ai_model_version

    @ai_model_version.setter
    def ai_model_version(self, ai_model_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model_version = ai_model_version

    @property
    def ai_model_versions(self) -> Optional[List[AIModelVersion]]:
        return None if self.attributes is None else self.attributes.ai_model_versions

    @ai_model_versions.setter
    def ai_model_versions(self, ai_model_versions: Optional[List[AIModelVersion]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model_versions = ai_model_versions

    @property
    def applications(self) -> Optional[List[AIApplication]]:
        return None if self.attributes is None else self.attributes.applications

    @applications.setter
    def applications(self, applications: Optional[List[AIApplication]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.applications = applications

    class Attributes(AI.Attributes):
        ai_model_datasets_d_s_l: Optional[str] = Field(default=None, description="")
        ai_model_status: Optional[AIModelStatus] = Field(default=None, description="")
        ai_model_version: Optional[str] = Field(default=None, description="")
        ai_model_versions: Optional[List[AIModelVersion]] = Field(
            default=None, description=""
        )  # relationship
        applications: Optional[List[AIApplication]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            ai_model_status: AIModelStatus,
            owner_groups: Optional[Set[str]] = None,
            owner_users: Optional[Set[str]] = None,
            ai_model_version: Optional[str] = None,
        ) -> AIModel.Attributes:
            validate_required_fields(
                ["name", "ai_model_status"],
                [name, ai_model_status],
            )
            owner_groups = owner_groups or set()
            owner_users = owner_users or set()
            name_camel_case = to_camel_case(name)
            return AIModel.Attributes(
                name=name,
                qualified_name=f"default/ai/aiapplication/{name_camel_case}",
                connector_name=AtlanConnectorType.AI.value,
                ai_model_status=ai_model_status,
                ai_model_version=ai_model_version,
                owner_groups=owner_groups,
                owner_users=owner_users,
                asset_cover_image="/assets/default-product-cover-DeQonY47.webp",
            )

    attributes: AIModel.Attributes = Field(
        default_factory=lambda: AIModel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .a_i_application import AIApplication  # noqa: E402, F401
from .a_i_model_version import AIModelVersion  # noqa: E402, F401
