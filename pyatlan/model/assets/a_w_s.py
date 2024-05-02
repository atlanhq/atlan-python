# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField
from pyatlan.model.structs import AwsTag

from .cloud import Cloud


class AWS(Cloud):
    """Description"""

    type_name: str = Field(default="AWS", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AWS":
            raise ValueError("must be AWS")
        return v

    def __setattr__(self, name, value):
        if name in AWS._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AWS_ARN: ClassVar[KeywordTextField] = KeywordTextField(
        "awsArn", "awsArn", "awsArn.text"
    )
    """
    Amazon Resource Name (ARN) for this asset. This uniquely identifies the asset in AWS, and thus must be unique across all AWS asset instances.
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

    _convenience_properties: ClassVar[List[str]] = [
        "aws_arn",
        "aws_partition",
        "aws_service",
        "aws_region",
        "aws_account_id",
        "aws_resource_id",
        "aws_owner_name",
        "aws_owner_id",
        "aws_tags",
    ]

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

    class Attributes(Cloud.Attributes):
        aws_arn: Optional[str] = Field(default=None, description="")
        aws_partition: Optional[str] = Field(default=None, description="")
        aws_service: Optional[str] = Field(default=None, description="")
        aws_region: Optional[str] = Field(default=None, description="")
        aws_account_id: Optional[str] = Field(default=None, description="")
        aws_resource_id: Optional[str] = Field(default=None, description="")
        aws_owner_name: Optional[str] = Field(default=None, description="")
        aws_owner_id: Optional[str] = Field(default=None, description="")
        aws_tags: Optional[List[AwsTag]] = Field(default=None, description="")

    attributes: AWS.Attributes = Field(
        default_factory=lambda: AWS.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
