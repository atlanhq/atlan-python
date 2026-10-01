# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import NotificationState
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, TextField
from pyatlan.model.structs import NotificationExternalReference

from .asset import Asset


class Notification(Asset, type_name="Notification"):
    """Description"""

    type_name: str = Field(default="Notification", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Notification":
            raise ValueError("must be Notification")
        return v

    def __setattr__(self, name, value):
        if name in Notification._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    NOTIFICATION_STATE: ClassVar[KeywordField] = KeywordField(
        "notificationState", "notificationState"
    )
    """
    Where the notification is in its lifecycle. Also how a check decides whether a live notification already exists before raising another.
    """  # noqa: E501
    NOTIFICATION_RECIPIENT_USERS: ClassVar[KeywordField] = KeywordField(
        "notificationRecipientUsers", "notificationRecipientUsers"
    )
    """
    Usernames the notification was addressed to. Drives the assigned-to-me view together with the group and role recipients.
    """  # noqa: E501
    NOTIFICATION_RECIPIENT_GROUPS: ClassVar[KeywordField] = KeywordField(
        "notificationRecipientGroups", "notificationRecipientGroups"
    )
    """
    Identifiers of the Atlan groups the notification is meant for. A group outlives its members, so a rule addressing a group stays generic as people join and leave.
    """  # noqa: E501
    NOTIFICATION_RECIPIENT_ROLES: ClassVar[KeywordField] = KeywordField(
        "notificationRecipientRoles", "notificationRecipientRoles"
    )
    """
    Identifiers of the Atlan roles that need to see the notification. Resolved to individuals by the interface at read time rather than stored.
    """  # noqa: E501
    NOTIFICATION_LAST_ACTED_BY: ClassVar[KeywordField] = KeywordField(
        "notificationLastActedBy", "notificationLastActedBy"
    )
    """
    Username of the person who last moved the state. Declared separately because the write is service-mediated, so the entity's own modifier records the service and not the person.
    """  # noqa: E501
    NOTIFICATION_LAST_ACTED_AT: ClassVar[NumericField] = NumericField(
        "notificationLastActedAt", "notificationLastActedAt"
    )
    """
    When a person last moved the state. Read against the creation timestamp this gives time to resolution.
    """
    NOTIFICATION_LAST_ACTED_REASON: ClassVar[TextField] = TextField(
        "notificationLastActedReason", "notificationLastActedReason"
    )
    """
    Reason or note the person gave for the last action. Mandatory for some actions and optional for others, so it is free text rather than a code.
    """  # noqa: E501
    NOTIFICATION_EXTERNAL_REFERENCES: ClassVar[KeywordField] = KeywordField(
        "notificationExternalReferences", "notificationExternalReferences"
    )
    """
    Where this notification also lives outside Atlan, one entry per surface. This is what lets an action taken in the inbox go back and update the message it came from.
    """  # noqa: E501

    _convenience_properties: ClassVar[List[str]] = [
        "notification_state",
        "notification_recipient_users",
        "notification_recipient_groups",
        "notification_recipient_roles",
        "notification_last_acted_by",
        "notification_last_acted_at",
        "notification_last_acted_reason",
        "notification_external_references",
    ]

    @property
    def notification_state(self) -> Optional[NotificationState]:
        return None if self.attributes is None else self.attributes.notification_state

    @notification_state.setter
    def notification_state(self, notification_state: Optional[NotificationState]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.notification_state = notification_state

    @property
    def notification_recipient_users(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.notification_recipient_users
        )

    @notification_recipient_users.setter
    def notification_recipient_users(
        self, notification_recipient_users: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.notification_recipient_users = notification_recipient_users

    @property
    def notification_recipient_groups(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.notification_recipient_groups
        )

    @notification_recipient_groups.setter
    def notification_recipient_groups(
        self, notification_recipient_groups: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.notification_recipient_groups = notification_recipient_groups

    @property
    def notification_recipient_roles(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.notification_recipient_roles
        )

    @notification_recipient_roles.setter
    def notification_recipient_roles(
        self, notification_recipient_roles: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.notification_recipient_roles = notification_recipient_roles

    @property
    def notification_last_acted_by(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.notification_last_acted_by
        )

    @notification_last_acted_by.setter
    def notification_last_acted_by(self, notification_last_acted_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.notification_last_acted_by = notification_last_acted_by

    @property
    def notification_last_acted_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.notification_last_acted_at
        )

    @notification_last_acted_at.setter
    def notification_last_acted_at(
        self, notification_last_acted_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.notification_last_acted_at = notification_last_acted_at

    @property
    def notification_last_acted_reason(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.notification_last_acted_reason
        )

    @notification_last_acted_reason.setter
    def notification_last_acted_reason(
        self, notification_last_acted_reason: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.notification_last_acted_reason = notification_last_acted_reason

    @property
    def notification_external_references(
        self,
    ) -> Optional[List[NotificationExternalReference]]:
        return (
            None
            if self.attributes is None
            else self.attributes.notification_external_references
        )

    @notification_external_references.setter
    def notification_external_references(
        self,
        notification_external_references: Optional[List[NotificationExternalReference]],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.notification_external_references = (
            notification_external_references
        )

    class Attributes(Asset.Attributes):
        notification_state: Optional[NotificationState] = Field(
            default=None, description=""
        )
        notification_recipient_users: Optional[Set[str]] = Field(
            default=None, description=""
        )
        notification_recipient_groups: Optional[Set[str]] = Field(
            default=None, description=""
        )
        notification_recipient_roles: Optional[Set[str]] = Field(
            default=None, description=""
        )
        notification_last_acted_by: Optional[str] = Field(default=None, description="")
        notification_last_acted_at: Optional[datetime] = Field(
            default=None, description=""
        )
        notification_last_acted_reason: Optional[str] = Field(
            default=None, description=""
        )
        notification_external_references: Optional[
            List[NotificationExternalReference]
        ] = Field(default=None, description="")

    attributes: Notification.Attributes = Field(
        default_factory=lambda: Notification.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
