# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .s_q_l import SQL


class SnowflakePipe(SQL):
    """Description"""

    type_name: str = Field(default="SnowflakePipe", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakePipe":
            raise ValueError("must be SnowflakePipe")
        return v

    def __setattr__(self, name, value):
        if name in SnowflakePipe._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DEFINITION: ClassVar[KeywordField] = KeywordField("definition", "definition")
    """
    SQL definition of this pipe.
    """
    SNOWFLAKE_PIPE_IS_AUTO_INGEST_ENABLED: ClassVar[BooleanField] = BooleanField(
        "snowflakePipeIsAutoIngestEnabled", "snowflakePipeIsAutoIngestEnabled"
    )
    """
    Whether auto-ingest is enabled for this pipe (true) or not (false).
    """
    SNOWFLAKE_PIPE_NOTIFICATION_CHANNEL_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "snowflakePipeNotificationChannelName",
            "snowflakePipeNotificationChannelName",
            "snowflakePipeNotificationChannelName.text",
        )
    )
    """
    Name of the notification channel for this pipe.
    """

    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "definition",
        "snowflake_pipe_is_auto_ingest_enabled",
        "snowflake_pipe_notification_channel_name",
        "atlan_schema",
    ]

    @property
    def definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.definition

    @definition.setter
    def definition(self, definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.definition = definition

    @property
    def snowflake_pipe_is_auto_ingest_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_pipe_is_auto_ingest_enabled
        )

    @snowflake_pipe_is_auto_ingest_enabled.setter
    def snowflake_pipe_is_auto_ingest_enabled(
        self, snowflake_pipe_is_auto_ingest_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_pipe_is_auto_ingest_enabled = (
            snowflake_pipe_is_auto_ingest_enabled
        )

    @property
    def snowflake_pipe_notification_channel_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_pipe_notification_channel_name
        )

    @snowflake_pipe_notification_channel_name.setter
    def snowflake_pipe_notification_channel_name(
        self, snowflake_pipe_notification_channel_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_pipe_notification_channel_name = (
            snowflake_pipe_notification_channel_name
        )

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    class Attributes(SQL.Attributes):
        definition: Optional[str] = Field(default=None, description="")
        snowflake_pipe_is_auto_ingest_enabled: Optional[bool] = Field(
            default=None, description=""
        )
        snowflake_pipe_notification_channel_name: Optional[str] = Field(
            default=None, description=""
        )
        atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship

    attributes: SnowflakePipe.Attributes = Field(
        default_factory=lambda: SnowflakePipe.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .schema import Schema  # noqa
