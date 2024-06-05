# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional, overload
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import (
    ADLSAccessTier,
    ADLSLeaseState,
    ADLSLeaseStatus,
    ADLSObjectArchiveStatus,
    ADLSObjectType,
    AtlanConnectorType,
)
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.utils import get_parent_qualified_name, init_guid, validate_required_fields

from .a_d_l_s import ADLS


class ADLSObject(ADLS):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        adls_container_qualified_name: str,
    ) -> ADLSObject: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        adls_container_qualified_name: str,
        adls_account_qualified_name: str,
        connection_qualified_name: str,
    ) -> ADLSObject: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        adls_container_qualified_name: str,
        adls_account_qualified_name: Optional[str] = None,
        connection_qualified_name: Optional[str] = None,
    ) -> ADLSObject:
        validate_required_fields(
            ["name", "adls_container_qualified_name"],
            [name, adls_container_qualified_name],
        )
        attributes = ADLSObject.Attributes.create(
            name=name,
            adls_container_qualified_name=adls_container_qualified_name,
            adls_account_qualified_name=adls_account_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(
        cls,
        *,
        name: str,
        adls_container_qualified_name: str,
    ) -> ADLSObject:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name, adls_container_qualified_name=adls_container_qualified_name
        )

    type_name: str = Field(default="ADLSObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADLSObject":
            raise ValueError("must be ADLSObject")
        return v

    def __setattr__(self, name, value):
        if name in ADLSObject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ADLS_OBJECT_URL: ClassVar[KeywordTextField] = KeywordTextField(
        "adlsObjectUrl", "adlsObjectUrl.keyword", "adlsObjectUrl"
    )
    """
    URL of this object.
    """
    ADLS_OBJECT_VERSION_ID: ClassVar[KeywordField] = KeywordField(
        "adlsObjectVersionId", "adlsObjectVersionId"
    )
    """
    Identifier of the version of this object, from ADLS.
    """
    ADLS_OBJECT_TYPE: ClassVar[KeywordField] = KeywordField(
        "adlsObjectType", "adlsObjectType"
    )
    """
    Type of this object.
    """
    ADLS_OBJECT_SIZE: ClassVar[NumericField] = NumericField(
        "adlsObjectSize", "adlsObjectSize"
    )
    """
    Size of this object.
    """
    ADLS_OBJECT_ACCESS_TIER: ClassVar[KeywordField] = KeywordField(
        "adlsObjectAccessTier", "adlsObjectAccessTier"
    )
    """
    Access tier of this object.
    """
    ADLS_OBJECT_ACCESS_TIER_LAST_MODIFIED_TIME: ClassVar[NumericField] = NumericField(
        "adlsObjectAccessTierLastModifiedTime", "adlsObjectAccessTierLastModifiedTime"
    )
    """
    Time (epoch) when the acccess tier for this object was last modified, in milliseconds.
    """
    ADLS_OBJECT_ARCHIVE_STATUS: ClassVar[KeywordField] = KeywordField(
        "adlsObjectArchiveStatus", "adlsObjectArchiveStatus"
    )
    """
    Archive status of this object.
    """
    ADLS_OBJECT_SERVER_ENCRYPTED: ClassVar[BooleanField] = BooleanField(
        "adlsObjectServerEncrypted", "adlsObjectServerEncrypted"
    )
    """
    Whether this object is server encrypted (true) or not (false).
    """
    ADLS_OBJECT_VERSION_LEVEL_IMMUTABILITY_SUPPORT: ClassVar[BooleanField] = (
        BooleanField(
            "adlsObjectVersionLevelImmutabilitySupport",
            "adlsObjectVersionLevelImmutabilitySupport",
        )
    )
    """
    Whether this object supports version-level immutability (true) or not (false).
    """
    ADLS_OBJECT_CACHE_CONTROL: ClassVar[TextField] = TextField(
        "adlsObjectCacheControl", "adlsObjectCacheControl"
    )
    """
    Cache control of this object.
    """
    ADLS_OBJECT_CONTENT_TYPE: ClassVar[TextField] = TextField(
        "adlsObjectContentType", "adlsObjectContentType"
    )
    """
    Content type of this object.
    """
    ADLS_OBJECT_CONTENT_MD5HASH: ClassVar[KeywordField] = KeywordField(
        "adlsObjectContentMD5Hash", "adlsObjectContentMD5Hash"
    )
    """
    MD5 hash of this object's contents.
    """
    ADLS_OBJECT_CONTENT_LANGUAGE: ClassVar[KeywordTextField] = KeywordTextField(
        "adlsObjectContentLanguage",
        "adlsObjectContentLanguage.keyword",
        "adlsObjectContentLanguage",
    )
    """
    Language of this object's contents.
    """
    ADLS_OBJECT_LEASE_STATUS: ClassVar[KeywordField] = KeywordField(
        "adlsObjectLeaseStatus", "adlsObjectLeaseStatus"
    )
    """
    Status of this object's lease.
    """
    ADLS_OBJECT_LEASE_STATE: ClassVar[KeywordField] = KeywordField(
        "adlsObjectLeaseState", "adlsObjectLeaseState"
    )
    """
    State of this object's lease.
    """
    ADLS_OBJECT_METADATA: ClassVar[KeywordField] = KeywordField(
        "adlsObjectMetadata", "adlsObjectMetadata"
    )
    """
    Metadata associated with this object, from ADLS.
    """
    ADLS_CONTAINER_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "adlsContainerQualifiedName",
        "adlsContainerQualifiedName",
        "adlsContainerQualifiedName.text",
    )
    """
    Unique name of the container this object exists within.
    """

    ADLS_CONTAINER: ClassVar[RelationField] = RelationField("adlsContainer")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "adls_object_url",
        "adls_object_version_id",
        "adls_object_type",
        "adls_object_size",
        "adls_object_access_tier",
        "adls_object_access_tier_last_modified_time",
        "adls_object_archive_status",
        "adls_object_server_encrypted",
        "adls_object_version_level_immutability_support",
        "adls_object_cache_control",
        "adls_object_content_type",
        "adls_object_content_m_d5_hash",
        "adls_object_content_language",
        "adls_object_lease_status",
        "adls_object_lease_state",
        "adls_object_metadata",
        "adls_container_qualified_name",
        "adls_container",
    ]

    @property
    def adls_object_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.adls_object_url

    @adls_object_url.setter
    def adls_object_url(self, adls_object_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_url = adls_object_url

    @property
    def adls_object_version_id(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.adls_object_version_id
        )

    @adls_object_version_id.setter
    def adls_object_version_id(self, adls_object_version_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_version_id = adls_object_version_id

    @property
    def adls_object_type(self) -> Optional[ADLSObjectType]:
        return None if self.attributes is None else self.attributes.adls_object_type

    @adls_object_type.setter
    def adls_object_type(self, adls_object_type: Optional[ADLSObjectType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_type = adls_object_type

    @property
    def adls_object_size(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.adls_object_size

    @adls_object_size.setter
    def adls_object_size(self, adls_object_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_size = adls_object_size

    @property
    def adls_object_access_tier(self) -> Optional[ADLSAccessTier]:
        return (
            None if self.attributes is None else self.attributes.adls_object_access_tier
        )

    @adls_object_access_tier.setter
    def adls_object_access_tier(
        self, adls_object_access_tier: Optional[ADLSAccessTier]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_access_tier = adls_object_access_tier

    @property
    def adls_object_access_tier_last_modified_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_access_tier_last_modified_time
        )

    @adls_object_access_tier_last_modified_time.setter
    def adls_object_access_tier_last_modified_time(
        self, adls_object_access_tier_last_modified_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_access_tier_last_modified_time = (
            adls_object_access_tier_last_modified_time
        )

    @property
    def adls_object_archive_status(self) -> Optional[ADLSObjectArchiveStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_archive_status
        )

    @adls_object_archive_status.setter
    def adls_object_archive_status(
        self, adls_object_archive_status: Optional[ADLSObjectArchiveStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_archive_status = adls_object_archive_status

    @property
    def adls_object_server_encrypted(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_server_encrypted
        )

    @adls_object_server_encrypted.setter
    def adls_object_server_encrypted(
        self, adls_object_server_encrypted: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_server_encrypted = adls_object_server_encrypted

    @property
    def adls_object_version_level_immutability_support(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_version_level_immutability_support
        )

    @adls_object_version_level_immutability_support.setter
    def adls_object_version_level_immutability_support(
        self, adls_object_version_level_immutability_support: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_version_level_immutability_support = (
            adls_object_version_level_immutability_support
        )

    @property
    def adls_object_cache_control(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_cache_control
        )

    @adls_object_cache_control.setter
    def adls_object_cache_control(self, adls_object_cache_control: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_cache_control = adls_object_cache_control

    @property
    def adls_object_content_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_content_type
        )

    @adls_object_content_type.setter
    def adls_object_content_type(self, adls_object_content_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_content_type = adls_object_content_type

    @property
    def adls_object_content_m_d5_hash(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_content_m_d5_hash
        )

    @adls_object_content_m_d5_hash.setter
    def adls_object_content_m_d5_hash(
        self, adls_object_content_m_d5_hash: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_content_m_d5_hash = adls_object_content_m_d5_hash

    @property
    def adls_object_content_language(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_content_language
        )

    @adls_object_content_language.setter
    def adls_object_content_language(self, adls_object_content_language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_content_language = adls_object_content_language

    @property
    def adls_object_lease_status(self) -> Optional[ADLSLeaseStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_object_lease_status
        )

    @adls_object_lease_status.setter
    def adls_object_lease_status(
        self, adls_object_lease_status: Optional[ADLSLeaseStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_lease_status = adls_object_lease_status

    @property
    def adls_object_lease_state(self) -> Optional[ADLSLeaseState]:
        return (
            None if self.attributes is None else self.attributes.adls_object_lease_state
        )

    @adls_object_lease_state.setter
    def adls_object_lease_state(
        self, adls_object_lease_state: Optional[ADLSLeaseState]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_lease_state = adls_object_lease_state

    @property
    def adls_object_metadata(self) -> Optional[Dict[str, str]]:
        return None if self.attributes is None else self.attributes.adls_object_metadata

    @adls_object_metadata.setter
    def adls_object_metadata(self, adls_object_metadata: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_object_metadata = adls_object_metadata

    @property
    def adls_container_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_container_qualified_name
        )

    @adls_container_qualified_name.setter
    def adls_container_qualified_name(
        self, adls_container_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container_qualified_name = adls_container_qualified_name

    @property
    def adls_container(self) -> Optional[ADLSContainer]:
        return None if self.attributes is None else self.attributes.adls_container

    @adls_container.setter
    def adls_container(self, adls_container: Optional[ADLSContainer]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_container = adls_container

    class Attributes(ADLS.Attributes):
        adls_object_url: Optional[str] = Field(default=None, description="")
        adls_object_version_id: Optional[str] = Field(default=None, description="")
        adls_object_type: Optional[ADLSObjectType] = Field(default=None, description="")
        adls_object_size: Optional[int] = Field(default=None, description="")
        adls_object_access_tier: Optional[ADLSAccessTier] = Field(
            default=None, description=""
        )
        adls_object_access_tier_last_modified_time: Optional[datetime] = Field(
            default=None, description=""
        )
        adls_object_archive_status: Optional[ADLSObjectArchiveStatus] = Field(
            default=None, description=""
        )
        adls_object_server_encrypted: Optional[bool] = Field(
            default=None, description=""
        )
        adls_object_version_level_immutability_support: Optional[bool] = Field(
            default=None, description=""
        )
        adls_object_cache_control: Optional[str] = Field(default=None, description="")
        adls_object_content_type: Optional[str] = Field(default=None, description="")
        adls_object_content_m_d5_hash: Optional[str] = Field(
            default=None, description=""
        )
        adls_object_content_language: Optional[str] = Field(
            default=None, description=""
        )
        adls_object_lease_status: Optional[ADLSLeaseStatus] = Field(
            default=None, description=""
        )
        adls_object_lease_state: Optional[ADLSLeaseState] = Field(
            default=None, description=""
        )
        adls_object_metadata: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        adls_container_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        adls_container: Optional[ADLSContainer] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            adls_container_qualified_name: str,
            adls_account_qualified_name: Optional[str] = None,
            connection_qualified_name: Optional[str] = None,
        ) -> ADLSObject.Attributes:
            validate_required_fields(
                ["name", "adls_container_qualified_name"],
                [name, adls_container_qualified_name],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    adls_container_qualified_name, "adls_container_qualified_name", 5
                )
            adls_account_qualified_name = (
                adls_account_qualified_name
                or get_parent_qualified_name(adls_container_qualified_name)
            )
            return ADLSObject.Attributes(
                name=name,
                adls_container_qualified_name=adls_container_qualified_name,
                qualified_name=f"{adls_container_qualified_name}/{name}",
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name or connection_qn,
                adls_container=ADLSContainer.ref_by_qualified_name(
                    adls_container_qualified_name
                ),
                adls_account_qualified_name=adls_account_qualified_name,
            )

    attributes: ADLSObject.Attributes = Field(
        default_factory=lambda: ADLSObject.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .a_d_l_s_container import ADLSContainer  # noqa
