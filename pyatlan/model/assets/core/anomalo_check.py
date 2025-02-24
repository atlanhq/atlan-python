# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)

from .anomalo import Anomalo


class AnomaloCheck(Anomalo):
    """Description"""

    type_name: str = Field(default="AnomaloCheck", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AnomaloCheck":
            raise ValueError("must be AnomaloCheck")
        return v

    def __setattr__(self, name, value):
        if name in AnomaloCheck._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ANOMALO_CHECK_LINKED_ASSET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "anomaloCheckLinkedAssetQualifiedName", "anomaloCheckLinkedAssetQualifiedName"
    )
    """
    QualifiedName of the asset associated with the check
    """
    ANOMALO_CHECK_CATEGORY_TYPE: ClassVar[KeywordField] = KeywordField(
        "anomaloCheckCategoryType", "anomaloCheckCategoryType"
    )
    """
    Category type of the check in Anomalo
    """
    ANOMALO_CHECK_TYPE: ClassVar[KeywordField] = KeywordField(
        "anomaloCheckType", "anomaloCheckType"
    )
    """
    Type of check in Anomalo
    """
    ANOMALO_CHECK_PRIORITY_LEVEL: ClassVar[KeywordField] = KeywordField(
        "anomaloCheckPriorityLevel", "anomaloCheckPriorityLevel"
    )
    """
    Priority level of the check in Anomalo
    """
    ANOMALO_CHECK_IS_SYSTEM_ADDED: ClassVar[BooleanField] = BooleanField(
        "anomaloCheckIsSystemAdded", "anomaloCheckIsSystemAdded"
    )
    """
    Flag to indicate if the check is an out of the box available check
    """
    ANOMALO_CHECK_STATUS: ClassVar[KeywordField] = KeywordField(
        "anomaloCheckStatus", "anomaloCheckStatus"
    )
    """
    Status of the check in Anomalo
    """
    ANOMALO_CHECK_STATUS_IMAGE_URL: ClassVar[TextField] = TextField(
        "anomaloCheckStatusImageUrl", "anomaloCheckStatusImageUrl"
    )
    """
    Image URL for the status of the check in Anomalo
    """
    ANOMALO_CHECK_LAST_RUN_COMPLETED_AT: ClassVar[NumericField] = NumericField(
        "anomaloCheckLastRunCompletedAt", "anomaloCheckLastRunCompletedAt"
    )
    """
    Timestamp when the check was last run
    """
    ANOMALO_CHECK_LAST_RUN_EVALUATED_MESSAGE: ClassVar[TextField] = TextField(
        "anomaloCheckLastRunEvaluatedMessage", "anomaloCheckLastRunEvaluatedMessage"
    )
    """
    Evaluated message of the latest check run.
    """
    ANOMALO_CHECK_LAST_RUN_URL: ClassVar[TextField] = TextField(
        "anomaloCheckLastRunUrl", "anomaloCheckLastRunUrl"
    )
    """
    URL to the latest check run.
    """
    ANOMALO_CHECK_HISTORIC_RUN_STATUS: ClassVar[TextField] = TextField(
        "anomaloCheckHistoricRunStatus", "anomaloCheckHistoricRunStatus"
    )
    """
    Historic run status of the check in Anomalo
    """

    ANOMALO_CHECK_ASSET: ClassVar[RelationField] = RelationField("anomaloCheckAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "anomalo_check_linked_asset_qualified_name",
        "anomalo_check_category_type",
        "anomalo_check_type",
        "anomalo_check_priority_level",
        "anomalo_check_is_system_added",
        "anomalo_check_status",
        "anomalo_check_status_image_url",
        "anomalo_check_last_run_completed_at",
        "anomalo_check_last_run_evaluated_message",
        "anomalo_check_last_run_url",
        "anomalo_check_historic_run_status",
        "anomalo_check_asset",
    ]

    @property
    def anomalo_check_linked_asset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.anomalo_check_linked_asset_qualified_name
        )

    @anomalo_check_linked_asset_qualified_name.setter
    def anomalo_check_linked_asset_qualified_name(
        self, anomalo_check_linked_asset_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anomalo_check_linked_asset_qualified_name = (
            anomalo_check_linked_asset_qualified_name
        )

    @property
    def anomalo_check_category_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.anomalo_check_category_type
        )

    @anomalo_check_category_type.setter
    def anomalo_check_category_type(self, anomalo_check_category_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anomalo_check_category_type = anomalo_check_category_type

    @property
    def anomalo_check_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.anomalo_check_type

    @anomalo_check_type.setter
    def anomalo_check_type(self, anomalo_check_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anomalo_check_type = anomalo_check_type

    @property
    def anomalo_check_priority_level(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.anomalo_check_priority_level
        )

    @anomalo_check_priority_level.setter
    def anomalo_check_priority_level(self, anomalo_check_priority_level: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anomalo_check_priority_level = anomalo_check_priority_level

    @property
    def anomalo_check_is_system_added(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.anomalo_check_is_system_added
        )

    @anomalo_check_is_system_added.setter
    def anomalo_check_is_system_added(
        self, anomalo_check_is_system_added: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anomalo_check_is_system_added = anomalo_check_is_system_added

    @property
    def anomalo_check_status(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.anomalo_check_status

    @anomalo_check_status.setter
    def anomalo_check_status(self, anomalo_check_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anomalo_check_status = anomalo_check_status

    @property
    def anomalo_check_status_image_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.anomalo_check_status_image_url
        )

    @anomalo_check_status_image_url.setter
    def anomalo_check_status_image_url(
        self, anomalo_check_status_image_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anomalo_check_status_image_url = anomalo_check_status_image_url

    @property
    def anomalo_check_last_run_completed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.anomalo_check_last_run_completed_at
        )

    @anomalo_check_last_run_completed_at.setter
    def anomalo_check_last_run_completed_at(
        self, anomalo_check_last_run_completed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anomalo_check_last_run_completed_at = (
            anomalo_check_last_run_completed_at
        )

    @property
    def anomalo_check_last_run_evaluated_message(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.anomalo_check_last_run_evaluated_message
        )

    @anomalo_check_last_run_evaluated_message.setter
    def anomalo_check_last_run_evaluated_message(
        self, anomalo_check_last_run_evaluated_message: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anomalo_check_last_run_evaluated_message = (
            anomalo_check_last_run_evaluated_message
        )

    @property
    def anomalo_check_last_run_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.anomalo_check_last_run_url
        )

    @anomalo_check_last_run_url.setter
    def anomalo_check_last_run_url(self, anomalo_check_last_run_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anomalo_check_last_run_url = anomalo_check_last_run_url

    @property
    def anomalo_check_historic_run_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.anomalo_check_historic_run_status
        )

    @anomalo_check_historic_run_status.setter
    def anomalo_check_historic_run_status(
        self, anomalo_check_historic_run_status: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anomalo_check_historic_run_status = (
            anomalo_check_historic_run_status
        )

    @property
    def anomalo_check_asset(self) -> Optional[Asset]:
        return None if self.attributes is None else self.attributes.anomalo_check_asset

    @anomalo_check_asset.setter
    def anomalo_check_asset(self, anomalo_check_asset: Optional[Asset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anomalo_check_asset = anomalo_check_asset

    class Attributes(Anomalo.Attributes):
        anomalo_check_linked_asset_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        anomalo_check_category_type: Optional[str] = Field(default=None, description="")
        anomalo_check_type: Optional[str] = Field(default=None, description="")
        anomalo_check_priority_level: Optional[str] = Field(
            default=None, description=""
        )
        anomalo_check_is_system_added: Optional[bool] = Field(
            default=None, description=""
        )
        anomalo_check_status: Optional[str] = Field(default=None, description="")
        anomalo_check_status_image_url: Optional[str] = Field(
            default=None, description=""
        )
        anomalo_check_last_run_completed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        anomalo_check_last_run_evaluated_message: Optional[str] = Field(
            default=None, description=""
        )
        anomalo_check_last_run_url: Optional[str] = Field(default=None, description="")
        anomalo_check_historic_run_status: Optional[str] = Field(
            default=None, description=""
        )
        anomalo_check_asset: Optional[Asset] = Field(
            default=None, description=""
        )  # relationship

    attributes: AnomaloCheck.Attributes = Field(
        default_factory=lambda: AnomaloCheck.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa
