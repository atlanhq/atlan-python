# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .s3 import S3


class S3Object(S3):
    """Description"""

    @classmethod
    @init_guid
    def creator(
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

    @classmethod
    @init_guid
    def create(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        aws_arn: str,
        s3_bucket_qualified_name: str,
    ) -> S3Object:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            aws_arn=aws_arn,
            s3_bucket_qualified_name=s3_bucket_qualified_name,
        )

    @classmethod
    @init_guid
    def create_with_prefix(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        prefix: str,
        s3_bucket_qualified_name: str,
    ) -> S3Object:
        validate_required_fields(
            [
                "name",
                "connection_qualified_name",
                "prefix",
                "s3_bucket_qualified_name",
            ],
            [name, connection_qualified_name, prefix, s3_bucket_qualified_name],
        )
        attributes = S3Object.Attributes.create_with_prefix(
            name=name,
            connection_qualified_name=connection_qualified_name,
            prefix=prefix,
            s3_bucket_qualified_name=s3_bucket_qualified_name,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="S3Object", allow_mutation=False)

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
    Time (epoch) at which this object was last updated, in milliseconds, or when it was created if it has never been modified.
    """  # noqa: E501
    S3BUCKET_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "s3BucketName", "s3BucketName", "s3BucketName.text"
    )
    """
    Simple name of the bucket in which this object exists.
    """
    S3BUCKET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "s3BucketQualifiedName", "s3BucketQualifiedName"
    )
    """
    Unique name of the bucket in which this object exists.
    """
    S3OBJECT_SIZE: ClassVar[NumericField] = NumericField("s3ObjectSize", "s3ObjectSize")
    """
    Object size in bytes.
    """
    S3OBJECT_STORAGE_CLASS: ClassVar[KeywordField] = KeywordField(
        "s3ObjectStorageClass", "s3ObjectStorageClass"
    )
    """
    Storage class used for storing this object, for example: standard, intelligent-tiering, glacier, etc.
    """
    S3OBJECT_KEY: ClassVar[KeywordTextField] = KeywordTextField(
        "s3ObjectKey", "s3ObjectKey", "s3ObjectKey.text"
    )
    """
    Unique identity of this object in an S3 bucket. This is usually the concatenation of any prefix (folder) in the S3 bucket with the name of the object (file) itself.
    """  # noqa: E501
    S3OBJECT_CONTENT_TYPE: ClassVar[KeywordField] = KeywordField(
        "s3ObjectContentType", "s3ObjectContentType"
    )
    """
    Type of content in this object, for example: text/plain, application/json, etc.
    """
    S3OBJECT_CONTENT_DISPOSITION: ClassVar[KeywordField] = KeywordField(
        "s3ObjectContentDisposition", "s3ObjectContentDisposition"
    )
    """
    Information about how this object's content should be presented.
    """
    S3OBJECT_VERSION_ID: ClassVar[KeywordField] = KeywordField(
        "s3ObjectVersionId", "s3ObjectVersionId"
    )
    """
    Version of this object. This is only applicable when versioning is enabled on the bucket in which this object exists.
    """  # noqa: E501

    BUCKET: ClassVar[RelationField] = RelationField("bucket")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
            default=None, description=""
        )
        s3_bucket_name: Optional[str] = Field(default=None, description="")
        s3_bucket_qualified_name: Optional[str] = Field(default=None, description="")
        s3_object_size: Optional[int] = Field(default=None, description="")
        s3_object_storage_class: Optional[str] = Field(default=None, description="")
        s3_object_key: Optional[str] = Field(default=None, description="")
        s3_object_content_type: Optional[str] = Field(default=None, description="")
        s3_object_content_disposition: Optional[str] = Field(
            default=None, description=""
        )
        s3_object_version_id: Optional[str] = Field(default=None, description="")
        bucket: Optional[S3Bucket] = Field(default=None, description="")  # relationship

        @classmethod
        @init_guid
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

        @classmethod
        @init_guid
        def create_with_prefix(
            cls,
            *,
            name: str,
            connection_qualified_name: str,
            prefix: str,
            s3_bucket_qualified_name: str,
        ) -> S3Object.Attributes:
            validate_required_fields(
                [
                    "name",
                    "connection_qualified_name",
                    "prefix",
                    "s3_bucket_qualified_name",
                ],
                [name, connection_qualified_name, prefix, s3_bucket_qualified_name],
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
            object_key = f"{prefix}/{name}"
            return S3Object.Attributes(
                name=name,
                s3_object_key=object_key,
                connection_qualified_name=connection_qualified_name,
                qualified_name=f"{connection_qualified_name}/{object_key}",
                connector_name=connector_type.value,
                s3_bucket_qualified_name=s3_bucket_qualified_name,
                bucket=S3Bucket.ref_by_qualified_name(s3_bucket_qualified_name),
            )

    attributes: S3Object.Attributes = Field(
        default_factory=lambda: S3Object.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s3_bucket import S3Bucket  # noqa
