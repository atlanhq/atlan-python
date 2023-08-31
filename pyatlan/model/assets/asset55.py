# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)
from pyatlan.utils import validate_required_fields

from .asset31 import S3


class S3Bucket(S3):
    """Description"""

    @classmethod
    # @validate_arguments()
    def create(
        cls, *, name: str, connection_qualified_name: str, aws_arn: str
    ) -> S3Bucket:
        validate_required_fields(
            ["name", "connection_qualified_name", "aws_arn"],
            [name, connection_qualified_name, aws_arn],
        )
        attributes = S3Bucket.Attributes.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
            aws_arn=aws_arn,
        )
        return cls(attributes=attributes)

    type_name: str = Field("S3Bucket", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "S3Bucket":
            raise ValueError("must be S3Bucket")
        return v

    def __setattr__(self, name, value):
        if name in S3Bucket._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    S3OBJECT_COUNT: ClassVar[NumericField] = NumericField(
        "s3ObjectCount", "s3ObjectCount"
    )
    """
    TBC
    """
    S3BUCKET_VERSIONING_ENABLED: ClassVar[BooleanField] = BooleanField(
        "s3BucketVersioningEnabled", "s3BucketVersioningEnabled"
    )
    """
    TBC
    """

    OBJECTS: ClassVar[RelationField] = RelationField("objects")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "s3_object_count",
        "s3_bucket_versioning_enabled",
        "objects",
    ]

    @property
    def s3_object_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.s3_object_count

    @s3_object_count.setter
    def s3_object_count(self, s3_object_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_count = s3_object_count

    @property
    def s3_bucket_versioning_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.s3_bucket_versioning_enabled
        )

    @s3_bucket_versioning_enabled.setter
    def s3_bucket_versioning_enabled(
        self, s3_bucket_versioning_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_bucket_versioning_enabled = s3_bucket_versioning_enabled

    @property
    def objects(self) -> Optional[list[S3Object]]:
        return None if self.attributes is None else self.attributes.objects

    @objects.setter
    def objects(self, objects: Optional[list[S3Object]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.objects = objects

    class Attributes(S3.Attributes):
        s3_object_count: Optional[int] = Field(
            None, description="", alias="s3ObjectCount"
        )
        s3_bucket_versioning_enabled: Optional[bool] = Field(
            None, description="", alias="s3BucketVersioningEnabled"
        )
        objects: Optional[list[S3Object]] = Field(
            None, description="", alias="objects"
        )  # relationship

        @classmethod
        # @validate_arguments()
        def create(
            cls, *, name: str, connection_qualified_name: str, aws_arn: str
        ) -> S3Bucket.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name", "aws_arn"],
                [name, connection_qualified_name, aws_arn],
            )
            fields = connection_qualified_name.split("/")
            if len(fields) != 3:
                raise ValueError("Invalid connection_qualified_name")
            try:
                if fields[0].replace(" ", "") == "" or fields[2].replace(" ", "") == "":
                    raise ValueError("Invalid connection_qualified_name")
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
                if connector_type != AtlanConnectorType.S3:
                    raise ValueError("Connector type must be s3")
            except ValueError as e:
                raise ValueError("Invalid connection_qualified_name") from e
            return S3Bucket.Attributes(
                aws_arn=aws_arn,
                name=name,
                connection_qualified_name=connection_qualified_name,
                qualified_name=f"{connection_qualified_name}/{aws_arn}",
                connector_name=connector_type.value,
            )

    attributes: "S3Bucket.Attributes" = Field(
        default_factory=lambda: S3Bucket.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class S3Object(S3):
    """Description"""

    @classmethod
    # @validate_arguments()
    def create(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        aws_arn: str,
        s3_bucket_qualified_name: str,
    ) -> S3Object:
        validate_required_fields(
            [
                "name",
                "connection_qualified_name",
                "aws_arn",
                "s3_bucket_qualified_name",
            ],
            [name, connection_qualified_name, aws_arn, s3_bucket_qualified_name],
        )
        attributes = S3Object.Attributes.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
            aws_arn=aws_arn,
            s3_bucket_qualified_name=s3_bucket_qualified_name,
        )
        return cls(attributes=attributes)

    type_name: str = Field("S3Object", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "S3Object":
            raise ValueError("must be S3Object")
        return v

    def __setattr__(self, name, value):
        if name in S3Object._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    S3OBJECT_LAST_MODIFIED_TIME: ClassVar[NumericField] = NumericField(
        "s3ObjectLastModifiedTime", "s3ObjectLastModifiedTime"
    )
    """
    TBC
    """
    S3BUCKET_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "s3BucketName", "s3BucketName", "s3BucketName.text"
    )
    """
    TBC
    """
    S3BUCKET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "s3BucketQualifiedName", "s3BucketQualifiedName"
    )
    """
    TBC
    """
    S3OBJECT_SIZE: ClassVar[NumericField] = NumericField("s3ObjectSize", "s3ObjectSize")
    """
    TBC
    """
    S3OBJECT_STORAGE_CLASS: ClassVar[KeywordField] = KeywordField(
        "s3ObjectStorageClass", "s3ObjectStorageClass"
    )
    """
    TBC
    """
    S3OBJECT_KEY: ClassVar[KeywordTextField] = KeywordTextField(
        "s3ObjectKey", "s3ObjectKey", "s3ObjectKey.text"
    )
    """
    TBC
    """
    S3OBJECT_CONTENT_TYPE: ClassVar[KeywordField] = KeywordField(
        "s3ObjectContentType", "s3ObjectContentType"
    )
    """
    TBC
    """
    S3OBJECT_CONTENT_DISPOSITION: ClassVar[KeywordField] = KeywordField(
        "s3ObjectContentDisposition", "s3ObjectContentDisposition"
    )
    """
    TBC
    """
    S3OBJECT_VERSION_ID: ClassVar[KeywordField] = KeywordField(
        "s3ObjectVersionId", "s3ObjectVersionId"
    )
    """
    TBC
    """

    BUCKET: ClassVar[RelationField] = RelationField("bucket")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "s3_object_last_modified_time",
        "s3_bucket_name",
        "s3_bucket_qualified_name",
        "s3_object_size",
        "s3_object_storage_class",
        "s3_object_key",
        "s3_object_content_type",
        "s3_object_content_disposition",
        "s3_object_version_id",
        "bucket",
    ]

    @property
    def s3_object_last_modified_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.s3_object_last_modified_time
        )

    @s3_object_last_modified_time.setter
    def s3_object_last_modified_time(
        self, s3_object_last_modified_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_last_modified_time = s3_object_last_modified_time

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
    def s3_object_size(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.s3_object_size

    @s3_object_size.setter
    def s3_object_size(self, s3_object_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_size = s3_object_size

    @property
    def s3_object_storage_class(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.s3_object_storage_class
        )

    @s3_object_storage_class.setter
    def s3_object_storage_class(self, s3_object_storage_class: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_storage_class = s3_object_storage_class

    @property
    def s3_object_key(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.s3_object_key

    @s3_object_key.setter
    def s3_object_key(self, s3_object_key: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_key = s3_object_key

    @property
    def s3_object_content_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.s3_object_content_type
        )

    @s3_object_content_type.setter
    def s3_object_content_type(self, s3_object_content_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_content_type = s3_object_content_type

    @property
    def s3_object_content_disposition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.s3_object_content_disposition
        )

    @s3_object_content_disposition.setter
    def s3_object_content_disposition(
        self, s3_object_content_disposition: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_content_disposition = s3_object_content_disposition

    @property
    def s3_object_version_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.s3_object_version_id

    @s3_object_version_id.setter
    def s3_object_version_id(self, s3_object_version_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.s3_object_version_id = s3_object_version_id

    @property
    def bucket(self) -> Optional[S3Bucket]:
        return None if self.attributes is None else self.attributes.bucket

    @bucket.setter
    def bucket(self, bucket: Optional[S3Bucket]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.bucket = bucket

    class Attributes(S3.Attributes):
        s3_object_last_modified_time: Optional[datetime] = Field(
            None, description="", alias="s3ObjectLastModifiedTime"
        )
        s3_bucket_name: Optional[str] = Field(
            None, description="", alias="s3BucketName"
        )
        s3_bucket_qualified_name: Optional[str] = Field(
            None, description="", alias="s3BucketQualifiedName"
        )
        s3_object_size: Optional[int] = Field(
            None, description="", alias="s3ObjectSize"
        )
        s3_object_storage_class: Optional[str] = Field(
            None, description="", alias="s3ObjectStorageClass"
        )
        s3_object_key: Optional[str] = Field(None, description="", alias="s3ObjectKey")
        s3_object_content_type: Optional[str] = Field(
            None, description="", alias="s3ObjectContentType"
        )
        s3_object_content_disposition: Optional[str] = Field(
            None, description="", alias="s3ObjectContentDisposition"
        )
        s3_object_version_id: Optional[str] = Field(
            None, description="", alias="s3ObjectVersionId"
        )
        bucket: Optional[S3Bucket] = Field(
            None, description="", alias="bucket"
        )  # relationship

        @classmethod
        # @validate_arguments()
        def create(
            cls,
            *,
            name: str,
            connection_qualified_name: str,
            aws_arn: str,
            s3_bucket_qualified_name: str,
        ) -> S3Object.Attributes:
            validate_required_fields(
                [
                    "name",
                    "connection_qualified_name",
                    "aws_arn",
                    "s3_bucket_qualified_name",
                ],
                [name, connection_qualified_name, aws_arn, s3_bucket_qualified_name],
            )
            fields = connection_qualified_name.split("/")
            if len(fields) != 3:
                raise ValueError("Invalid connection_qualified_name")
            try:
                if fields[0].replace(" ", "") == "" or fields[2].replace(" ", "") == "":
                    raise ValueError("Invalid connection_qualified_name")
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
                if connector_type != AtlanConnectorType.S3:
                    raise ValueError("Connector type must be s3")
            except ValueError as e:
                raise ValueError("Invalid connection_qualified_name") from e
            return S3Object.Attributes(
                aws_arn=aws_arn,
                name=name,
                connection_qualified_name=connection_qualified_name,
                qualified_name=f"{connection_qualified_name}/{aws_arn}",
                connector_name=connector_type.value,
                s3_bucket_qualified_name=s3_bucket_qualified_name,
                bucket=S3Bucket.ref_by_qualified_name(s3_bucket_qualified_name),
            )

    attributes: "S3Object.Attributes" = Field(
        default_factory=lambda: S3Object.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


S3Bucket.Attributes.update_forward_refs()


S3Object.Attributes.update_forward_refs()
