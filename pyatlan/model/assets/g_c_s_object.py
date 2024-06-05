# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional, overload
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

from .g_c_s import GCS


class GCSObject(GCS):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        gcs_bucket_qualified_name: str,
    ) -> GCSObject: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        gcs_bucket_qualified_name: str,
        connection_qualified_name: str,
    ) -> GCSObject: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        gcs_bucket_qualified_name: str,
        connection_qualified_name: Optional[str] = None,
    ) -> GCSObject:
        validate_required_fields(
            ["name", "gcs_bucket_qualified_name"], [name, gcs_bucket_qualified_name]
        )
        attributes = GCSObject.Attributes.create(
            name=name,
            gcs_bucket_qualified_name=gcs_bucket_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, gcs_bucket_qualified_name: str) -> GCSObject:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name, gcs_bucket_qualified_name=gcs_bucket_qualified_name
        )

    type_name: str = Field(default="GCSObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "GCSObject":
            raise ValueError("must be GCSObject")
        return v

    def __setattr__(self, name, value):
        if name in GCSObject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    GCS_BUCKET_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "gcsBucketName", "gcsBucketName.keyword", "gcsBucketName"
    )
    """
    Simple name of the bucket in which this object exists.
    """
    GCS_BUCKET_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "gcsBucketQualifiedName",
        "gcsBucketQualifiedName",
        "gcsBucketQualifiedName.text",
    )
    """
    Unique name of the bucket in which this object exists.
    """
    GCS_OBJECT_SIZE: ClassVar[NumericField] = NumericField(
        "gcsObjectSize", "gcsObjectSize"
    )
    """
    Object size in bytes.
    """
    GCS_OBJECT_KEY: ClassVar[KeywordTextField] = KeywordTextField(
        "gcsObjectKey", "gcsObjectKey", "gcsObjectKey.text"
    )
    """
    Key of this object, in GCS.
    """
    GCS_OBJECT_MEDIA_LINK: ClassVar[KeywordTextField] = KeywordTextField(
        "gcsObjectMediaLink", "gcsObjectMediaLink", "gcsObjectMediaLink.text"
    )
    """
    Media link to this object.
    """
    GCS_OBJECT_HOLD_TYPE: ClassVar[KeywordField] = KeywordField(
        "gcsObjectHoldType", "gcsObjectHoldType"
    )
    """
    Type of hold on this object.
    """
    GCS_OBJECT_GENERATION_ID: ClassVar[NumericField] = NumericField(
        "gcsObjectGenerationId", "gcsObjectGenerationId"
    )
    """
    Generation ID of this object.
    """
    GCS_OBJECT_CRC32C_HASH: ClassVar[KeywordField] = KeywordField(
        "gcsObjectCRC32CHash", "gcsObjectCRC32CHash"
    )
    """
    CRC32C hash of this object.
    """
    GCS_OBJECT_MD5HASH: ClassVar[KeywordField] = KeywordField(
        "gcsObjectMD5Hash", "gcsObjectMD5Hash"
    )
    """
    MD5 hash of this object.
    """
    GCS_OBJECT_DATA_LAST_MODIFIED_TIME: ClassVar[NumericField] = NumericField(
        "gcsObjectDataLastModifiedTime", "gcsObjectDataLastModifiedTime"
    )
    """
    Time (epoch) at which this object's data was last modified, in milliseconds.
    """
    GCS_OBJECT_CONTENT_TYPE: ClassVar[KeywordField] = KeywordField(
        "gcsObjectContentType", "gcsObjectContentType"
    )
    """
    Type of content in this object.
    """
    GCS_OBJECT_CONTENT_ENCODING: ClassVar[KeywordField] = KeywordField(
        "gcsObjectContentEncoding", "gcsObjectContentEncoding"
    )
    """
    Content encoding of this object.
    """
    GCS_OBJECT_CONTENT_DISPOSITION: ClassVar[KeywordField] = KeywordField(
        "gcsObjectContentDisposition", "gcsObjectContentDisposition"
    )
    """
    Information about how this object's content should be presented.
    """
    GCS_OBJECT_CONTENT_LANGUAGE: ClassVar[KeywordField] = KeywordField(
        "gcsObjectContentLanguage", "gcsObjectContentLanguage"
    )
    """
    Language of this object's contents.
    """
    GCS_OBJECT_RETENTION_EXPIRATION_DATE: ClassVar[NumericField] = NumericField(
        "gcsObjectRetentionExpirationDate", "gcsObjectRetentionExpirationDate"
    )
    """
    Retention expiration date of this object.
    """

    GCS_BUCKET: ClassVar[RelationField] = RelationField("gcsBucket")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "gcs_bucket_name",
        "gcs_bucket_qualified_name",
        "gcs_object_size",
        "gcs_object_key",
        "gcs_object_media_link",
        "gcs_object_hold_type",
        "gcs_object_generation_id",
        "gcs_object_c_r_c32_c_hash",
        "gcs_object_m_d5_hash",
        "gcs_object_data_last_modified_time",
        "gcs_object_content_type",
        "gcs_object_content_encoding",
        "gcs_object_content_disposition",
        "gcs_object_content_language",
        "gcs_object_retention_expiration_date",
        "gcs_bucket",
    ]

    @property
    def gcs_bucket_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_bucket_name

    @gcs_bucket_name.setter
    def gcs_bucket_name(self, gcs_bucket_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_name = gcs_bucket_name

    @property
    def gcs_bucket_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_qualified_name
        )

    @gcs_bucket_qualified_name.setter
    def gcs_bucket_qualified_name(self, gcs_bucket_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_qualified_name = gcs_bucket_qualified_name

    @property
    def gcs_object_size(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.gcs_object_size

    @gcs_object_size.setter
    def gcs_object_size(self, gcs_object_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_size = gcs_object_size

    @property
    def gcs_object_key(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_object_key

    @gcs_object_key.setter
    def gcs_object_key(self, gcs_object_key: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_key = gcs_object_key

    @property
    def gcs_object_media_link(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.gcs_object_media_link
        )

    @gcs_object_media_link.setter
    def gcs_object_media_link(self, gcs_object_media_link: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_media_link = gcs_object_media_link

    @property
    def gcs_object_hold_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_object_hold_type

    @gcs_object_hold_type.setter
    def gcs_object_hold_type(self, gcs_object_hold_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_hold_type = gcs_object_hold_type

    @property
    def gcs_object_generation_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_generation_id
        )

    @gcs_object_generation_id.setter
    def gcs_object_generation_id(self, gcs_object_generation_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_generation_id = gcs_object_generation_id

    @property
    def gcs_object_c_r_c32_c_hash(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_c_r_c32_c_hash
        )

    @gcs_object_c_r_c32_c_hash.setter
    def gcs_object_c_r_c32_c_hash(self, gcs_object_c_r_c32_c_hash: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_c_r_c32_c_hash = gcs_object_c_r_c32_c_hash

    @property
    def gcs_object_m_d5_hash(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_object_m_d5_hash

    @gcs_object_m_d5_hash.setter
    def gcs_object_m_d5_hash(self, gcs_object_m_d5_hash: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_m_d5_hash = gcs_object_m_d5_hash

    @property
    def gcs_object_data_last_modified_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_data_last_modified_time
        )

    @gcs_object_data_last_modified_time.setter
    def gcs_object_data_last_modified_time(
        self, gcs_object_data_last_modified_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_data_last_modified_time = (
            gcs_object_data_last_modified_time
        )

    @property
    def gcs_object_content_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.gcs_object_content_type
        )

    @gcs_object_content_type.setter
    def gcs_object_content_type(self, gcs_object_content_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_type = gcs_object_content_type

    @property
    def gcs_object_content_encoding(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_content_encoding
        )

    @gcs_object_content_encoding.setter
    def gcs_object_content_encoding(self, gcs_object_content_encoding: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_encoding = gcs_object_content_encoding

    @property
    def gcs_object_content_disposition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_content_disposition
        )

    @gcs_object_content_disposition.setter
    def gcs_object_content_disposition(
        self, gcs_object_content_disposition: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_disposition = gcs_object_content_disposition

    @property
    def gcs_object_content_language(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_content_language
        )

    @gcs_object_content_language.setter
    def gcs_object_content_language(self, gcs_object_content_language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_language = gcs_object_content_language

    @property
    def gcs_object_retention_expiration_date(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_retention_expiration_date
        )

    @gcs_object_retention_expiration_date.setter
    def gcs_object_retention_expiration_date(
        self, gcs_object_retention_expiration_date: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_retention_expiration_date = (
            gcs_object_retention_expiration_date
        )

    @property
    def gcs_bucket(self) -> Optional[GCSBucket]:
        return None if self.attributes is None else self.attributes.gcs_bucket

    @gcs_bucket.setter
    def gcs_bucket(self, gcs_bucket: Optional[GCSBucket]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket = gcs_bucket

    class Attributes(GCS.Attributes):
        gcs_bucket_name: Optional[str] = Field(default=None, description="")
        gcs_bucket_qualified_name: Optional[str] = Field(default=None, description="")
        gcs_object_size: Optional[int] = Field(default=None, description="")
        gcs_object_key: Optional[str] = Field(default=None, description="")
        gcs_object_media_link: Optional[str] = Field(default=None, description="")
        gcs_object_hold_type: Optional[str] = Field(default=None, description="")
        gcs_object_generation_id: Optional[int] = Field(default=None, description="")
        gcs_object_c_r_c32_c_hash: Optional[str] = Field(default=None, description="")
        gcs_object_m_d5_hash: Optional[str] = Field(default=None, description="")
        gcs_object_data_last_modified_time: Optional[datetime] = Field(
            default=None, description=""
        )
        gcs_object_content_type: Optional[str] = Field(default=None, description="")
        gcs_object_content_encoding: Optional[str] = Field(default=None, description="")
        gcs_object_content_disposition: Optional[str] = Field(
            default=None, description=""
        )
        gcs_object_content_language: Optional[str] = Field(default=None, description="")
        gcs_object_retention_expiration_date: Optional[datetime] = Field(
            default=None, description=""
        )
        gcs_bucket: Optional[GCSBucket] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            gcs_bucket_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
        ) -> GCSObject.Attributes:
            validate_required_fields(
                ["name", "gcs_bucket_qualified_name"], [name, gcs_bucket_qualified_name]
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    gcs_bucket_qualified_name, "gcs_bucket_qualified_name", 4
                )

            return GCSObject.Attributes(
                name=name,
                gcs_bucket_qualified_name=gcs_bucket_qualified_name,
                connection_qualified_name=connection_qualified_name or connection_qn,
                qualified_name=f"{gcs_bucket_qualified_name}/{name}",
                connector_name=connector_name,
                gcs_bucket=GCSBucket.ref_by_qualified_name(gcs_bucket_qualified_name),
            )

    attributes: GCSObject.Attributes = Field(
        default_factory=lambda: GCSObject.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .g_c_s_bucket import GCSBucket  # noqa
