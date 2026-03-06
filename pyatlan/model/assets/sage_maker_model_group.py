# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import (
    AIModelStatus,
    EthicalAIAccountabilityConfig,
    EthicalAIBiasMitigationConfig,
    EthicalAIEnvironmentalConsciousnessConfig,
    EthicalAIFairnessConfig,
    EthicalAIPrivacyConfig,
    EthicalAIReliabilityAndSafetyConfig,
    EthicalAITransparencyConfig,
)
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
    TextField,
)
from pyatlan.model.structs import AwsTag

from .sage_maker import SageMaker


class SageMakerModelGroup(SageMaker):
    """Description"""

    type_name: str = Field(default="SageMakerModelGroup", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SageMakerModelGroup":
            raise ValueError("must be SageMakerModelGroup")
        return v

    def __setattr__(self, name, value):
        if name in SageMakerModelGroup._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAGE_MAKER_MODEL_GROUP_STATUS: ClassVar[KeywordField] = KeywordField(
        "sageMakerModelGroupStatus", "sageMakerModelGroupStatus"
    )
    """
    Current status of the Model Package Group.
    """
    SAGE_MAKER_S3URI: ClassVar[KeywordField] = KeywordField(
        "sageMakerS3Uri", "sageMakerS3Uri"
    )
    """
    Primary S3 URI associated with this SageMaker asset.
    """
    ETHICAL_AI_PRIVACY_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIPrivacyConfig", "ethicalAIPrivacyConfig"
    )
    """
    Privacy configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_FAIRNESS_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIFairnessConfig", "ethicalAIFairnessConfig"
    )
    """
    Fairness configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_BIAS_MITIGATION_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIBiasMitigationConfig", "ethicalAIBiasMitigationConfig"
    )
    """
    Bias mitigation configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_RELIABILITY_AND_SAFETY_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIReliabilityAndSafetyConfig", "ethicalAIReliabilityAndSafetyConfig"
    )
    """
    Reliability and safety configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_TRANSPARENCY_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAITransparencyConfig", "ethicalAITransparencyConfig"
    )
    """
    Transparency configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_ACCOUNTABILITY_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIAccountabilityConfig", "ethicalAIAccountabilityConfig"
    )
    """
    Accountability configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_ENVIRONMENTAL_CONSCIOUSNESS_CONFIG: ClassVar[KeywordField] = (
        KeywordField(
            "ethicalAIEnvironmentalConsciousnessConfig",
            "ethicalAIEnvironmentalConsciousnessConfig",
        )
    )
    """
    Environmental consciousness configuration for ensuring the ethical use of an AI asset
    """
    AWS_ARN: ClassVar[KeywordTextField] = KeywordTextField(
        "awsArn", "awsArn", "awsArn.text"
    )
    """
    DEPRECATED: This legacy attribute must be unique across all AWS asset instances. This can create non-obvious edge cases for creating / updating assets, and we therefore recommended NOT using it. See and use cloudResourceName instead.
    """  # noqa: E501
    AWS_PARTITION: ClassVar[KeywordField] = KeywordField("awsPartition", "awsPartition")
    """
    Group of AWS region and service objects.
    """
    AWS_SERVICE: ClassVar[KeywordField] = KeywordField("awsService", "awsService")
    """
    Type of service in which the asset exists.
    """
    AWS_REGION: ClassVar[KeywordField] = KeywordField("awsRegion", "awsRegion")
    """
    Physical region where the data center in which the asset exists is clustered.
    """
    AWS_ACCOUNT_ID: ClassVar[KeywordField] = KeywordField(
        "awsAccountId", "awsAccountId"
    )
    """
    12-digit number that uniquely identifies an AWS account.
    """
    AWS_RESOURCE_ID: ClassVar[KeywordField] = KeywordField(
        "awsResourceId", "awsResourceId"
    )
    """
    Unique resource ID assigned when a new resource is created.
    """
    AWS_OWNER_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "awsOwnerName", "awsOwnerName", "awsOwnerName.text"
    )
    """
    Root user's name.
    """
    AWS_OWNER_ID: ClassVar[KeywordField] = KeywordField("awsOwnerId", "awsOwnerId")
    """
    Root user's ID.
    """
    AWS_TAGS: ClassVar[KeywordField] = KeywordField("awsTags", "awsTags")
    """
    List of tags that have been applied to the asset in AWS.
    """
    CLOUD_UNIFORM_RESOURCE_NAME: ClassVar[KeywordField] = KeywordField(
        "cloudUniformResourceName", "cloudUniformResourceName"
    )
    """
    Uniform resource name (URN) for the asset: AWS ARN, Google Cloud URI, Azure resource ID, Oracle OCID, and so on.
    """
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
    SAGE_MAKER_MODELS: ClassVar[RelationField] = RelationField("sageMakerModels")
    """
    TBC
    """
    APPLICATIONS: ClassVar[RelationField] = RelationField("applications")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sage_maker_model_group_status",
        "sage_maker_s3_uri",
        "ethical_a_i_privacy_config",
        "ethical_a_i_fairness_config",
        "ethical_a_i_bias_mitigation_config",
        "ethical_a_i_reliability_and_safety_config",
        "ethical_a_i_transparency_config",
        "ethical_a_i_accountability_config",
        "ethical_a_i_environmental_consciousness_config",
        "aws_arn",
        "aws_partition",
        "aws_service",
        "aws_region",
        "aws_account_id",
        "aws_resource_id",
        "aws_owner_name",
        "aws_owner_id",
        "aws_tags",
        "cloud_uniform_resource_name",
        "ai_model_datasets_d_s_l",
        "ai_model_status",
        "ai_model_version",
        "ai_model_versions",
        "sage_maker_models",
        "applications",
    ]

    @property
    def sage_maker_model_group_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_model_group_status
        )

    @sage_maker_model_group_status.setter
    def sage_maker_model_group_status(
        self, sage_maker_model_group_status: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model_group_status = sage_maker_model_group_status

    @property
    def sage_maker_s3_uri(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sage_maker_s3_uri

    @sage_maker_s3_uri.setter
    def sage_maker_s3_uri(self, sage_maker_s3_uri: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_s3_uri = sage_maker_s3_uri

    @property
    def ethical_a_i_privacy_config(self) -> Optional[EthicalAIPrivacyConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_privacy_config
        )

    @ethical_a_i_privacy_config.setter
    def ethical_a_i_privacy_config(
        self, ethical_a_i_privacy_config: Optional[EthicalAIPrivacyConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_privacy_config = ethical_a_i_privacy_config

    @property
    def ethical_a_i_fairness_config(self) -> Optional[EthicalAIFairnessConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_fairness_config
        )

    @ethical_a_i_fairness_config.setter
    def ethical_a_i_fairness_config(
        self, ethical_a_i_fairness_config: Optional[EthicalAIFairnessConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_fairness_config = ethical_a_i_fairness_config

    @property
    def ethical_a_i_bias_mitigation_config(
        self,
    ) -> Optional[EthicalAIBiasMitigationConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_bias_mitigation_config
        )

    @ethical_a_i_bias_mitigation_config.setter
    def ethical_a_i_bias_mitigation_config(
        self,
        ethical_a_i_bias_mitigation_config: Optional[EthicalAIBiasMitigationConfig],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_bias_mitigation_config = (
            ethical_a_i_bias_mitigation_config
        )

    @property
    def ethical_a_i_reliability_and_safety_config(
        self,
    ) -> Optional[EthicalAIReliabilityAndSafetyConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_reliability_and_safety_config
        )

    @ethical_a_i_reliability_and_safety_config.setter
    def ethical_a_i_reliability_and_safety_config(
        self,
        ethical_a_i_reliability_and_safety_config: Optional[
            EthicalAIReliabilityAndSafetyConfig
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_reliability_and_safety_config = (
            ethical_a_i_reliability_and_safety_config
        )

    @property
    def ethical_a_i_transparency_config(self) -> Optional[EthicalAITransparencyConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_transparency_config
        )

    @ethical_a_i_transparency_config.setter
    def ethical_a_i_transparency_config(
        self, ethical_a_i_transparency_config: Optional[EthicalAITransparencyConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_transparency_config = (
            ethical_a_i_transparency_config
        )

    @property
    def ethical_a_i_accountability_config(
        self,
    ) -> Optional[EthicalAIAccountabilityConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_accountability_config
        )

    @ethical_a_i_accountability_config.setter
    def ethical_a_i_accountability_config(
        self, ethical_a_i_accountability_config: Optional[EthicalAIAccountabilityConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_accountability_config = (
            ethical_a_i_accountability_config
        )

    @property
    def ethical_a_i_environmental_consciousness_config(
        self,
    ) -> Optional[EthicalAIEnvironmentalConsciousnessConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_environmental_consciousness_config
        )

    @ethical_a_i_environmental_consciousness_config.setter
    def ethical_a_i_environmental_consciousness_config(
        self,
        ethical_a_i_environmental_consciousness_config: Optional[
            EthicalAIEnvironmentalConsciousnessConfig
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_environmental_consciousness_config = (
            ethical_a_i_environmental_consciousness_config
        )

    @property
    def aws_arn(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_arn

    @aws_arn.setter
    def aws_arn(self, aws_arn: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_arn = aws_arn

    @property
    def aws_partition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_partition

    @aws_partition.setter
    def aws_partition(self, aws_partition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_partition = aws_partition

    @property
    def aws_service(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_service

    @aws_service.setter
    def aws_service(self, aws_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_service = aws_service

    @property
    def aws_region(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_region

    @aws_region.setter
    def aws_region(self, aws_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_region = aws_region

    @property
    def aws_account_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_account_id

    @aws_account_id.setter
    def aws_account_id(self, aws_account_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_account_id = aws_account_id

    @property
    def aws_resource_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_resource_id

    @aws_resource_id.setter
    def aws_resource_id(self, aws_resource_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_resource_id = aws_resource_id

    @property
    def aws_owner_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_owner_name

    @aws_owner_name.setter
    def aws_owner_name(self, aws_owner_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_owner_name = aws_owner_name

    @property
    def aws_owner_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.aws_owner_id

    @aws_owner_id.setter
    def aws_owner_id(self, aws_owner_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_owner_id = aws_owner_id

    @property
    def aws_tags(self) -> Optional[List[AwsTag]]:
        return None if self.attributes is None else self.attributes.aws_tags

    @aws_tags.setter
    def aws_tags(self, aws_tags: Optional[List[AwsTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.aws_tags = aws_tags

    @property
    def cloud_uniform_resource_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cloud_uniform_resource_name
        )

    @cloud_uniform_resource_name.setter
    def cloud_uniform_resource_name(self, cloud_uniform_resource_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cloud_uniform_resource_name = cloud_uniform_resource_name

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
    def sage_maker_models(self) -> Optional[List[SageMakerModel]]:
        return None if self.attributes is None else self.attributes.sage_maker_models

    @sage_maker_models.setter
    def sage_maker_models(self, sage_maker_models: Optional[List[SageMakerModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_models = sage_maker_models

    @property
    def applications(self) -> Optional[List[AIApplication]]:
        return None if self.attributes is None else self.attributes.applications

    @applications.setter
    def applications(self, applications: Optional[List[AIApplication]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.applications = applications

    class Attributes(SageMaker.Attributes):
        sage_maker_model_group_status: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_s3_uri: Optional[str] = Field(default=None, description="")
        ethical_a_i_privacy_config: Optional[EthicalAIPrivacyConfig] = Field(
            default=None, description=""
        )
        ethical_a_i_fairness_config: Optional[EthicalAIFairnessConfig] = Field(
            default=None, description=""
        )
        ethical_a_i_bias_mitigation_config: Optional[EthicalAIBiasMitigationConfig] = (
            Field(default=None, description="")
        )
        ethical_a_i_reliability_and_safety_config: Optional[
            EthicalAIReliabilityAndSafetyConfig
        ] = Field(default=None, description="")
        ethical_a_i_transparency_config: Optional[EthicalAITransparencyConfig] = Field(
            default=None, description=""
        )
        ethical_a_i_accountability_config: Optional[EthicalAIAccountabilityConfig] = (
            Field(default=None, description="")
        )
        ethical_a_i_environmental_consciousness_config: Optional[
            EthicalAIEnvironmentalConsciousnessConfig
        ] = Field(default=None, description="")
        aws_arn: Optional[str] = Field(default=None, description="")
        aws_partition: Optional[str] = Field(default=None, description="")
        aws_service: Optional[str] = Field(default=None, description="")
        aws_region: Optional[str] = Field(default=None, description="")
        aws_account_id: Optional[str] = Field(default=None, description="")
        aws_resource_id: Optional[str] = Field(default=None, description="")
        aws_owner_name: Optional[str] = Field(default=None, description="")
        aws_owner_id: Optional[str] = Field(default=None, description="")
        aws_tags: Optional[List[AwsTag]] = Field(default=None, description="")
        cloud_uniform_resource_name: Optional[str] = Field(default=None, description="")
        ai_model_datasets_d_s_l: Optional[str] = Field(default=None, description="")
        ai_model_status: Optional[AIModelStatus] = Field(default=None, description="")
        ai_model_version: Optional[str] = Field(default=None, description="")
        ai_model_versions: Optional[List[AIModelVersion]] = Field(
            default=None, description=""
        )  # relationship
        sage_maker_models: Optional[List[SageMakerModel]] = Field(
            default=None, description=""
        )  # relationship
        applications: Optional[List[AIApplication]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SageMakerModelGroup.Attributes = Field(
        default_factory=lambda: SageMakerModelGroup.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .core.a_i_application import AIApplication  # noqa: E402, F401
from .core.a_i_model_version import AIModelVersion  # noqa: E402, F401
from .sage_maker_model import SageMakerModel  # noqa: E402, F401

SageMakerModelGroup.Attributes.update_forward_refs()
