# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .g_c_s import GCS


class GCSBucket(GCS):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> GCSBucket:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = GCSBucket.Attributes.create(
            name=name, connection_qualified_name=connection_qualified_name
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, connection_qualified_name: str) -> GCSBucket:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )

    type_name: str = Field(default="GCSBucket", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "GCSBucket":
            raise ValueError("must be GCSBucket")
        return v

    def __setattr__(self, name, value):
        if name in GCSBucket._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    GCS_OBJECT_COUNT: ClassVar[NumericField] = NumericField(
        "gcsObjectCount", "gcsObjectCount"
    )
    """
    Number of objects within the bucket.
    """
    GCS_BUCKET_VERSIONING_ENABLED: ClassVar[BooleanField] = BooleanField(
        "gcsBucketVersioningEnabled", "gcsBucketVersioningEnabled"
    )
    """
    Whether versioning is enabled on the bucket (true) or not (false).
    """
    GCS_BUCKET_RETENTION_LOCKED: ClassVar[BooleanField] = BooleanField(
        "gcsBucketRetentionLocked", "gcsBucketRetentionLocked"
    )
    """
    Whether retention is locked for this bucket (true) or not (false).
    """
    GCS_BUCKET_RETENTION_PERIOD: ClassVar[NumericField] = NumericField(
        "gcsBucketRetentionPeriod", "gcsBucketRetentionPeriod"
    )
    """
    Retention period for objects in this bucket.
    """
    GCS_BUCKET_RETENTION_EFFECTIVE_TIME: ClassVar[NumericField] = NumericField(
        "gcsBucketRetentionEffectiveTime", "gcsBucketRetentionEffectiveTime"
    )
    """
    Effective time for retention of objects in this bucket.
    """
    GCS_BUCKET_LIFECYCLE_RULES: ClassVar[TextField] = TextField(
        "gcsBucketLifecycleRules", "gcsBucketLifecycleRules"
    )
    """
    Lifecycle rules for this bucket.
    """
    GCS_BUCKET_RETENTION_POLICY: ClassVar[TextField] = TextField(
        "gcsBucketRetentionPolicy", "gcsBucketRetentionPolicy"
    )
    """
    Retention policy for this bucket.
    """

    GCS_OBJECTS: ClassVar[RelationField] = RelationField("gcsObjects")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "gcs_object_count",
        "gcs_bucket_versioning_enabled",
        "gcs_bucket_retention_locked",
        "gcs_bucket_retention_period",
        "gcs_bucket_retention_effective_time",
        "gcs_bucket_lifecycle_rules",
        "gcs_bucket_retention_policy",
        "gcs_objects",
    ]

    @property
    def gcs_object_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.gcs_object_count

    @gcs_object_count.setter
    def gcs_object_count(self, gcs_object_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_count = gcs_object_count

    @property
    def gcs_bucket_versioning_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_versioning_enabled
        )

    @gcs_bucket_versioning_enabled.setter
    def gcs_bucket_versioning_enabled(
        self, gcs_bucket_versioning_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_versioning_enabled = gcs_bucket_versioning_enabled

    @property
    def gcs_bucket_retention_locked(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_retention_locked
        )

    @gcs_bucket_retention_locked.setter
    def gcs_bucket_retention_locked(self, gcs_bucket_retention_locked: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_locked = gcs_bucket_retention_locked

    @property
    def gcs_bucket_retention_period(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_retention_period
        )

    @gcs_bucket_retention_period.setter
    def gcs_bucket_retention_period(self, gcs_bucket_retention_period: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_period = gcs_bucket_retention_period

    @property
    def gcs_bucket_retention_effective_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_retention_effective_time
        )

    @gcs_bucket_retention_effective_time.setter
    def gcs_bucket_retention_effective_time(
        self, gcs_bucket_retention_effective_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_effective_time = (
            gcs_bucket_retention_effective_time
        )

    @property
    def gcs_bucket_lifecycle_rules(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_lifecycle_rules
        )

    @gcs_bucket_lifecycle_rules.setter
    def gcs_bucket_lifecycle_rules(self, gcs_bucket_lifecycle_rules: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_lifecycle_rules = gcs_bucket_lifecycle_rules

    @property
    def gcs_bucket_retention_policy(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_retention_policy
        )

    @gcs_bucket_retention_policy.setter
    def gcs_bucket_retention_policy(self, gcs_bucket_retention_policy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_policy = gcs_bucket_retention_policy

    @property
    def gcs_objects(self) -> Optional[List[GCSObject]]:
        return None if self.attributes is None else self.attributes.gcs_objects

    @gcs_objects.setter
    def gcs_objects(self, gcs_objects: Optional[List[GCSObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_objects = gcs_objects

    class Attributes(GCS.Attributes):
        gcs_object_count: Optional[int] = Field(default=None, description="")
        gcs_bucket_versioning_enabled: Optional[bool] = Field(
            default=None, description=""
        )
        gcs_bucket_retention_locked: Optional[bool] = Field(
            default=None, description=""
        )
        gcs_bucket_retention_period: Optional[int] = Field(default=None, description="")
        gcs_bucket_retention_effective_time: Optional[datetime] = Field(
            default=None, description=""
        )
        gcs_bucket_lifecycle_rules: Optional[str] = Field(default=None, description="")
        gcs_bucket_retention_policy: Optional[str] = Field(default=None, description="")
        gcs_objects: Optional[List[GCSObject]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls, *, name: str, connection_qualified_name: str
        ) -> GCSBucket.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return GCSBucket.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: GCSBucket.Attributes = Field(
        default_factory=lambda: GCSBucket.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .g_c_s_object import GCSObject  # noqa
