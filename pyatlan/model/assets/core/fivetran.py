# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import FivetranConnectorStatus
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField

from .catalog import Catalog


class Fivetran(Catalog):
    """Description"""

    type_name: str = Field(default="Fivetran", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Fivetran":
            raise ValueError("must be Fivetran")
        return v

    def __setattr__(self, name, value):
        if name in Fivetran._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FIVETRAN_WORKFLOW_NAME: ClassVar[KeywordField] = KeywordField(
        "fivetranWorkflowName", "fivetranWorkflowName"
    )
    """
    Name of the atlan fivetran workflow that updated this asset
    """
    FIVETRAN_LAST_SYNC_STATUS: ClassVar[KeywordField] = KeywordField(
        "fivetranLastSyncStatus", "fivetranLastSyncStatus"
    )
    """
    Status of the latest sync on Fivetran.
    """
    FIVETRAN_LAST_SYNC_RECORDS_UPDATED: ClassVar[NumericField] = NumericField(
        "fivetranLastSyncRecordsUpdated", "fivetranLastSyncRecordsUpdated"
    )
    """
    Number of records updated in the latest sync on Fivetran
    """

    _convenience_properties: ClassVar[List[str]] = [
        "fivetran_workflow_name",
        "fivetran_last_sync_status",
        "fivetran_last_sync_records_updated",
    ]

    @property
    def fivetran_workflow_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.fivetran_workflow_name
        )

    @fivetran_workflow_name.setter
    def fivetran_workflow_name(self, fivetran_workflow_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_workflow_name = fivetran_workflow_name

    @property
    def fivetran_last_sync_status(self) -> Optional[FivetranConnectorStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_last_sync_status
        )

    @fivetran_last_sync_status.setter
    def fivetran_last_sync_status(
        self, fivetran_last_sync_status: Optional[FivetranConnectorStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_last_sync_status = fivetran_last_sync_status

    @property
    def fivetran_last_sync_records_updated(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_last_sync_records_updated
        )

    @fivetran_last_sync_records_updated.setter
    def fivetran_last_sync_records_updated(
        self, fivetran_last_sync_records_updated: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_last_sync_records_updated = (
            fivetran_last_sync_records_updated
        )

    class Attributes(Catalog.Attributes):
        fivetran_workflow_name: Optional[str] = Field(default=None, description="")
        fivetran_last_sync_status: Optional[FivetranConnectorStatus] = Field(
            default=None, description=""
        )
        fivetran_last_sync_records_updated: Optional[int] = Field(
            default=None, description=""
        )

    attributes: Fivetran.Attributes = Field(
        default_factory=lambda: Fivetran.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
