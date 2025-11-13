# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .s3 import S3


class S3Prefix(S3):
    """Description"""

    type_name: str = Field(default="S3Prefix", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "S3Prefix":
            raise ValueError("must be S3Prefix")
        return v

    def __setattr__(self, name, value):
        if name in S3Prefix._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    S3BUCKET_NAME: ClassVar[KeywordField] = KeywordField("s3BucketName", "s3BucketName")
    """
    Simple name of the bucket in which this prefix exists.
    """
    S3BUCKET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "s3BucketQualifiedName", "s3BucketQualifiedName"
    )
    """
    Unique name of the bucket in which this prefix exists.
    """
    S3PREFIX_COUNT: ClassVar[NumericField] = NumericField(
        "s3PrefixCount", "s3PrefixCount"
    )
    """
    Number of prefixes immediately contained within the prefix.
    """
    S3OBJECT_COUNT: ClassVar[NumericField] = NumericField(
        "s3ObjectCount", "s3ObjectCount"
    )
    """
    Number of objects immediately contained within the prefix.
    """

    S3BUCKET: ClassVar[RelationField] = RelationField("s3Bucket")
    """
    TBC
    """
    S3OBJECTS: ClassVar[RelationField] = RelationField("s3Objects")
    """
    TBC
    """
    S3PARENT_PREFIX: ClassVar[RelationField] = RelationField("s3ParentPrefix")
    """
    TBC
    """
    S3CHILD_PREFIXES: ClassVar[RelationField] = RelationField("s3ChildPrefixes")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "s3_bucket_name",
        "s3_bucket_qualified_name",
        "s3_prefix_count",
        "s3_object_count",
        "s3_bucket",
        "s3_objects",
        "s3_parent_prefix",
        "s3_child_prefixes",
    ]

    @property
    def s3_bucket_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.s3_bucket_name

    @s3_bucket_name.setter
    def s3_bucket_name(self, s3_bucket_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_bucket_name = s3_bucket_name

    @property
    def s3_bucket_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.s3_bucket_qualified_name
        )

    @s3_bucket_qualified_name.setter
    def s3_bucket_qualified_name(self, s3_bucket_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_bucket_qualified_name = s3_bucket_qualified_name

    @property
    def s3_prefix_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.s3_prefix_count

    @s3_prefix_count.setter
    def s3_prefix_count(self, s3_prefix_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_prefix_count = s3_prefix_count

    @property
    def s3_object_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.s3_object_count

    @s3_object_count.setter
    def s3_object_count(self, s3_object_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_count = s3_object_count

    @property
    def s3_bucket(self) -> Optional[S3Bucket]:
        return None if self.attributes is None else self.attributes.s3_bucket

    @s3_bucket.setter
    def s3_bucket(self, s3_bucket: Optional[S3Bucket]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_bucket = s3_bucket

    @property
    def s3_objects(self) -> Optional[List[S3Object]]:
        return None if self.attributes is None else self.attributes.s3_objects

    @s3_objects.setter
    def s3_objects(self, s3_objects: Optional[List[S3Object]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_objects = s3_objects

    @property
    def s3_parent_prefix(self) -> Optional[S3Prefix]:
        return None if self.attributes is None else self.attributes.s3_parent_prefix

    @s3_parent_prefix.setter
    def s3_parent_prefix(self, s3_parent_prefix: Optional[S3Prefix]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_parent_prefix = s3_parent_prefix

    @property
    def s3_child_prefixes(self) -> Optional[List[S3Prefix]]:
        return None if self.attributes is None else self.attributes.s3_child_prefixes

    @s3_child_prefixes.setter
    def s3_child_prefixes(self, s3_child_prefixes: Optional[List[S3Prefix]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_child_prefixes = s3_child_prefixes

    class Attributes(S3.Attributes):
        s3_bucket_name: Optional[str] = Field(default=None, description="")
        s3_bucket_qualified_name: Optional[str] = Field(default=None, description="")
        s3_prefix_count: Optional[int] = Field(default=None, description="")
        s3_object_count: Optional[int] = Field(default=None, description="")
        s3_bucket: Optional[S3Bucket] = Field(
            default=None, description=""
        )  # relationship
        s3_objects: Optional[List[S3Object]] = Field(
            default=None, description=""
        )  # relationship
        s3_parent_prefix: Optional[S3Prefix] = Field(
            default=None, description=""
        )  # relationship
        s3_child_prefixes: Optional[List[S3Prefix]] = Field(
            default=None, description=""
        )  # relationship

    attributes: S3Prefix.Attributes = Field(
        default_factory=lambda: S3Prefix.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s3_bucket import S3Bucket  # noqa: E402, F401
from .s3_object import S3Object  # noqa: E402, F401

S3Prefix.Attributes.update_forward_refs()
