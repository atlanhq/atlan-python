# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import BooleanField, NumericField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .s3 import S3


class S3Bucket(S3):
    """Description"""

    @overload
    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        aws_arn: str,
    ) -> S3Bucket: ...

    @overload
    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        aws_arn: Optional[str] = None,
    ) -> S3Bucket: ...

    @classmethod
    @init_guid
    def creator(
        cls, *, name: str, connection_qualified_name: str, aws_arn: Optional[str] = None
    ) -> S3Bucket:
        validate_required_fields(
            ["name", "connection_qualified_name"],
            [name, connection_qualified_name],
        )
        attributes = S3Bucket.Attributes.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
            aws_arn=aws_arn,
        )
        return cls(attributes=attributes)

    @overload
    @classmethod
    @init_guid
    def create(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        aws_arn: str,
    ) -> S3Bucket: ...

    @overload
    @classmethod
    @init_guid
    def create(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        aws_arn: Optional[str] = None,
    ) -> S3Bucket: ...

    @classmethod
    @init_guid
    def create(
        cls, *, name: str, connection_qualified_name: str, aws_arn: Optional[str] = None
    ) -> S3Bucket:
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
        )

    type_name: str = Field(default="S3Bucket", allow_mutation=False)

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
    Number of objects within the bucket.
    """
    S3BUCKET_VERSIONING_ENABLED: ClassVar[BooleanField] = BooleanField(
        "s3BucketVersioningEnabled", "s3BucketVersioningEnabled"
    )
    """
    Whether versioning is enabled for the bucket (true) or not (false).
    """

    OBJECTS: ClassVar[RelationField] = RelationField("objects")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
    def objects(self) -> Optional[List[S3Object]]:
        return None if self.attributes is None else self.attributes.objects

    @objects.setter
    def objects(self, objects: Optional[List[S3Object]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.objects = objects

    class Attributes(S3.Attributes):
        s3_object_count: Optional[int] = Field(default=None, description="")
        s3_bucket_versioning_enabled: Optional[bool] = Field(
            default=None, description=""
        )
        objects: Optional[List[S3Object]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            connection_qualified_name: str,
            aws_arn: Optional[str] = None,
        ) -> S3Bucket.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"],
                [name, connection_qualified_name],
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
                qualified_name=f"{connection_qualified_name}/{aws_arn if aws_arn else name}",
                connector_name=connector_type.value,
            )

    attributes: S3Bucket.Attributes = Field(
        default_factory=lambda: S3Bucket.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s3_object import S3Object  # noqa
