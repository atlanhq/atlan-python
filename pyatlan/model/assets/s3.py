# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
)
from pyatlan.model.structs import AwsTag

from .object_store import ObjectStore


class S3(ObjectStore):
    """Description"""

    type_name: str = Field(default="S3", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "S3":
            raise ValueError("must be S3")
        return v

    def __setattr__(self, name, value):
        if name in S3._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    S3E_TAG: ClassVar[KeywordTextField] = KeywordTextField(
        "s3ETag", "s3ETag", "s3ETag.text"
    )
    """
    Entity tag for the asset. An entity tag is a hash of the object and represents changes to the contents of an object only, not its metadata.
    """  # noqa: E501
    S3ENCRYPTION: ClassVar[KeywordField] = KeywordField("s3Encryption", "s3Encryption")
    """

    """
    S3PARENT_PREFIX_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField("s3ParentPrefixQualifiedName", "s3ParentPrefixQualifiedName")
    """
    Unique name of the immediate parent prefix in which this asset exists.
    """
    S3PREFIX_HIERARCHY: ClassVar[KeywordField] = KeywordField("s3PrefixHierarchy", "s3PrefixHierarchy")
    """
    Ordered array of prefix assets with qualified name and name representing the complete prefix hierarchy path for this asset, from immediate parent to root prefix.
    """
    CATALOG_HAS_PARTIAL_FIELDS: ClassVar[BooleanField] = BooleanField(
        "catalogHasPartialFields", "catalogHasPartialFields"
    )
    """
    Indicates this catalog asset has partial fields, if true.
    """
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
        "s3_e_tag",
        "s3_encryption",
        "s3_parent_prefix_qualified_name",
        "s3_prefix_hierarchy",
        "catalog_has_partial_fields",
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
    def s3_e_tag(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.s3_e_tag

    @s3_e_tag.setter
    def s3_e_tag(self, s3_e_tag: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_e_tag = s3_e_tag

    @property
    def s3_encryption(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.s3_encryption

    @s3_encryption.setter
    def s3_encryption(self, s3_encryption: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_encryption = s3_encryption

    @property
    def s3_parent_prefix_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.s3_parent_prefix_qualified_name

    @s3_parent_prefix_qualified_name.setter
    def s3_parent_prefix_qualified_name(self, s3_parent_prefix_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_parent_prefix_qualified_name = s3_parent_prefix_qualified_name

    @property
    def s3_prefix_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.s3_prefix_hierarchy

    @s3_prefix_hierarchy.setter
    def s3_prefix_hierarchy(self, s3_prefix_hierarchy: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_prefix_hierarchy = s3_prefix_hierarchy

    @property
    def catalog_has_partial_fields(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.catalog_has_partial_fields
        )

    @catalog_has_partial_fields.setter
    def catalog_has_partial_fields(self, catalog_has_partial_fields: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.catalog_has_partial_fields = catalog_has_partial_fields

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

    class Attributes(ObjectStore.Attributes):
        s3_e_tag: Optional[str] = Field(default=None, description="")
        s3_encryption: Optional[str] = Field(default=None, description="")
        s3_parent_prefix_qualified_name: Optional[str] = Field(default=None, description="")
        s3_prefix_hierarchy: Optional[List[Dict[str, str]]] = Field(default=None, description="")
        catalog_has_partial_fields: Optional[bool] = Field(default=None, description="")
        aws_arn: Optional[str] = Field(default=None, description="")
        aws_partition: Optional[str] = Field(default=None, description="")
        aws_service: Optional[str] = Field(default=None, description="")
        aws_region: Optional[str] = Field(default=None, description="")
        aws_account_id: Optional[str] = Field(default=None, description="")
        aws_resource_id: Optional[str] = Field(default=None, description="")
        aws_owner_name: Optional[str] = Field(default=None, description="")
        aws_owner_id: Optional[str] = Field(default=None, description="")
        aws_tags: Optional[List[AwsTag]] = Field(default=None, description="")

    attributes: S3.Attributes = Field(
        default_factory=lambda: S3.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


S3.Attributes.update_forward_refs()
