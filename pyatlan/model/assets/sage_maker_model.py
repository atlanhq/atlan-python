# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import (
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
)
from pyatlan.model.structs import AwsTag

from .sage_maker import SageMaker


class SageMakerModel(SageMaker):
    """Description"""

    type_name: str = Field(default="SageMakerModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SageMakerModel":
            raise ValueError("must be SageMakerModel")
        return v

    def __setattr__(self, name, value):
        if name in SageMakerModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAGE_MAKER_MODEL_CONTAINER_IMAGE: ClassVar[KeywordField] = KeywordField(
        "sageMakerModelContainerImage", "sageMakerModelContainerImage"
    )
    """
    Docker container image used for the model.
    """
    SAGE_MAKER_MODEL_EXECUTION_ROLE_ARN: ClassVar[KeywordField] = KeywordField(
        "sageMakerModelExecutionRoleArn", "sageMakerModelExecutionRoleArn"
    )
    """
    ARN of the IAM role used by the model for accessing AWS resources.
    """
    SAGE_MAKER_MODEL_MODEL_GROUP_NAME: ClassVar[KeywordField] = KeywordField(
        "sageMakerModelModelGroupName", "sageMakerModelModelGroupName"
    )
    """
    Name of the parent Model Group.
    """
    SAGE_MAKER_MODEL_MODEL_GROUP_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "sageMakerModelModelGroupQualifiedName", "sageMakerModelModelGroupQualifiedName"
    )
    """
    Qualified name of the parent Model Group.
    """
    SAGE_MAKER_MODEL_VERSION: ClassVar[KeywordField] = KeywordField(
        "sageMakerModelVersion", "sageMakerModelVersion"
    )
    """
    Version of the SageMaker Model Package.
    """
    SAGE_MAKER_MODEL_STATUS: ClassVar[KeywordField] = KeywordField(
        "sageMakerModelStatus", "sageMakerModelStatus"
    )
    """
    Status of the SageMaker Model Package (ACTIVE or INACTIVE).
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

    SAGE_MAKER_MODEL_GROUP: ClassVar[RelationField] = RelationField(
        "sageMakerModelGroup"
    )
    """
    TBC
    """
    SAGE_MAKER_MODEL_DEPLOYMENTS: ClassVar[RelationField] = RelationField(
        "sageMakerModelDeployments"
    )
    """
    TBC
    """
    AI_MODEL: ClassVar[RelationField] = RelationField("aiModel")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sage_maker_model_container_image",
        "sage_maker_model_execution_role_arn",
        "sage_maker_model_model_group_name",
        "sage_maker_model_model_group_qualified_name",
        "sage_maker_model_version",
        "sage_maker_model_status",
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
        "sage_maker_model_group",
        "sage_maker_model_deployments",
        "ai_model",
    ]

    @property
    def sage_maker_model_container_image(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_model_container_image
        )

    @sage_maker_model_container_image.setter
    def sage_maker_model_container_image(
        self, sage_maker_model_container_image: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model_container_image = (
            sage_maker_model_container_image
        )

    @property
    def sage_maker_model_execution_role_arn(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_model_execution_role_arn
        )

    @sage_maker_model_execution_role_arn.setter
    def sage_maker_model_execution_role_arn(
        self, sage_maker_model_execution_role_arn: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model_execution_role_arn = (
            sage_maker_model_execution_role_arn
        )

    @property
    def sage_maker_model_model_group_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_model_model_group_name
        )

    @sage_maker_model_model_group_name.setter
    def sage_maker_model_model_group_name(
        self, sage_maker_model_model_group_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model_model_group_name = (
            sage_maker_model_model_group_name
        )

    @property
    def sage_maker_model_model_group_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_model_model_group_qualified_name
        )

    @sage_maker_model_model_group_qualified_name.setter
    def sage_maker_model_model_group_qualified_name(
        self, sage_maker_model_model_group_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model_model_group_qualified_name = (
            sage_maker_model_model_group_qualified_name
        )

    @property
    def sage_maker_model_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_model_version
        )

    @sage_maker_model_version.setter
    def sage_maker_model_version(self, sage_maker_model_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model_version = sage_maker_model_version

    @property
    def sage_maker_model_status(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sage_maker_model_status
        )

    @sage_maker_model_status.setter
    def sage_maker_model_status(self, sage_maker_model_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model_status = sage_maker_model_status

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
    def sage_maker_model_group(self) -> Optional[SageMakerModelGroup]:
        return (
            None if self.attributes is None else self.attributes.sage_maker_model_group
        )

    @sage_maker_model_group.setter
    def sage_maker_model_group(
        self, sage_maker_model_group: Optional[SageMakerModelGroup]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model_group = sage_maker_model_group

    @property
    def sage_maker_model_deployments(self) -> Optional[List[SageMakerModelDeployment]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_model_deployments
        )

    @sage_maker_model_deployments.setter
    def sage_maker_model_deployments(
        self, sage_maker_model_deployments: Optional[List[SageMakerModelDeployment]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model_deployments = sage_maker_model_deployments

    @property
    def ai_model(self) -> Optional[AIModel]:
        return None if self.attributes is None else self.attributes.ai_model

    @ai_model.setter
    def ai_model(self, ai_model: Optional[AIModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model = ai_model

    class Attributes(SageMaker.Attributes):
        sage_maker_model_container_image: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_model_execution_role_arn: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_model_model_group_name: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_model_model_group_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_model_version: Optional[str] = Field(default=None, description="")
        sage_maker_model_status: Optional[str] = Field(default=None, description="")
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
        sage_maker_model_group: Optional[SageMakerModelGroup] = Field(
            default=None, description=""
        )  # relationship
        sage_maker_model_deployments: Optional[List[SageMakerModelDeployment]] = Field(
            default=None, description=""
        )  # relationship
        ai_model: Optional[AIModel] = Field(
            default=None, description=""
        )  # relationship

    attributes: SageMakerModel.Attributes = Field(
        default_factory=lambda: SageMakerModel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .core.a_i_model import AIModel  # noqa: E402, F401
from .sage_maker_model_deployment import SageMakerModelDeployment  # noqa: E402, F401
from .sage_maker_model_group import SageMakerModelGroup  # noqa: E402, F401

SageMakerModel.Attributes.update_forward_refs()
