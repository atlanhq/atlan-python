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
)

from .s_q_l import SQL


class SnowflakeStream(SQL):
    """Description"""

    type_name: str = Field(default="SnowflakeStream", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakeStream":
            raise ValueError("must be SnowflakeStream")
        return v

    def __setattr__(self, name, value):
        if name in SnowflakeStream._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SNOWFLAKE_STREAM_TYPE: ClassVar[KeywordField] = KeywordField(
        "snowflakeStreamType", "snowflakeStreamType"
    )
    """
    Type of this stream, for example: standard, append-only, insert-only, etc.
    """
    SNOWFLAKE_STREAM_SOURCE_TYPE: ClassVar[KeywordField] = KeywordField(
        "snowflakeStreamSourceType", "snowflakeStreamSourceType"
    )
    """
    Type of the source of this stream.
    """
    SNOWFLAKE_STREAM_MODE: ClassVar[KeywordField] = KeywordField(
        "snowflakeStreamMode", "snowflakeStreamMode"
    )
    """
    Mode of this stream.
    """
    SNOWFLAKE_STREAM_IS_STALE: ClassVar[BooleanField] = BooleanField(
        "snowflakeStreamIsStale", "snowflakeStreamIsStale"
    )
    """
    Whether this stream is stale (true) or not (false).
    """
    SNOWFLAKE_STREAM_STALE_AFTER: ClassVar[NumericField] = NumericField(
        "snowflakeStreamStaleAfter", "snowflakeStreamStaleAfter"
    )
    """
    Time (epoch) after which this stream will be stale, in milliseconds.
    """

    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "snowflake_stream_type",
        "snowflake_stream_source_type",
        "snowflake_stream_mode",
        "snowflake_stream_is_stale",
        "snowflake_stream_stale_after",
        "atlan_schema",
    ]

    @property
    def snowflake_stream_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.snowflake_stream_type
        )

    @snowflake_stream_type.setter
    def snowflake_stream_type(self, snowflake_stream_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_type = snowflake_stream_type

    @property
    def snowflake_stream_source_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_stream_source_type
        )

    @snowflake_stream_source_type.setter
    def snowflake_stream_source_type(self, snowflake_stream_source_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_source_type = snowflake_stream_source_type

    @property
    def snowflake_stream_mode(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.snowflake_stream_mode
        )

    @snowflake_stream_mode.setter
    def snowflake_stream_mode(self, snowflake_stream_mode: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_mode = snowflake_stream_mode

    @property
    def snowflake_stream_is_stale(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_stream_is_stale
        )

    @snowflake_stream_is_stale.setter
    def snowflake_stream_is_stale(self, snowflake_stream_is_stale: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_is_stale = snowflake_stream_is_stale

    @property
    def snowflake_stream_stale_after(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_stream_stale_after
        )

    @snowflake_stream_stale_after.setter
    def snowflake_stream_stale_after(
        self, snowflake_stream_stale_after: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stream_stale_after = snowflake_stream_stale_after

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    class Attributes(SQL.Attributes):
        snowflake_stream_type: Optional[str] = Field(default=None, description="")
        snowflake_stream_source_type: Optional[str] = Field(
            default=None, description=""
        )
        snowflake_stream_mode: Optional[str] = Field(default=None, description="")
        snowflake_stream_is_stale: Optional[bool] = Field(default=None, description="")
        snowflake_stream_stale_after: Optional[datetime] = Field(
            default=None, description=""
        )
        atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship

    attributes: SnowflakeStream.Attributes = Field(
        default_factory=lambda: SnowflakeStream.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .schema import Schema  # noqa
