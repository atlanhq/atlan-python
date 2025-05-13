# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .s_q_l import SQL


class SnowflakeStage(SQL):
    """Description"""

    type_name: str = Field(default="SnowflakeStage", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakeStage":
            raise ValueError("must be SnowflakeStage")
        return v

    def __setattr__(self, name, value):
        if name in SnowflakeStage._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SNOWFLAKE_STAGE_EXTERNAL_LOCATION: ClassVar[KeywordField] = KeywordField(
        "snowflakeStageExternalLocation", "snowflakeStageExternalLocation"
    )
    """
    The URL or cloud storage path specifying the external location where the stage data files are stored. This is NULL for internal stages.
    """  # noqa: E501
    SNOWFLAKE_STAGE_EXTERNAL_LOCATION_REGION: ClassVar[KeywordField] = KeywordField(
        "snowflakeStageExternalLocationRegion", "snowflakeStageExternalLocationRegion"
    )
    """
    The geographic region identifier where the external stage is located in cloud storage. This is NULL for internal stages.
    """  # noqa: E501
    SNOWFLAKE_STAGE_STORAGE_INTEGRATION: ClassVar[KeywordField] = KeywordField(
        "snowflakeStageStorageIntegration", "snowflakeStageStorageIntegration"
    )
    """
    The name of the storage integration associated with the stage; NULL for internal stages or stages that do not use a storage integration.
    """  # noqa: E501
    SNOWFLAKE_STAGE_TYPE: ClassVar[KeywordField] = KeywordField(
        "snowflakeStageType", "snowflakeStageType"
    )
    """
    Categorization of the stage type in Snowflake, which can be 'Internal Named' or 'External Named', indicating whether the stage storage is within Snowflake or in external cloud storage.
    """  # noqa: E501

    SQL_STAGE_SCHEMA: ClassVar[RelationField] = RelationField("sqlStageSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "snowflake_stage_external_location",
        "snowflake_stage_external_location_region",
        "snowflake_stage_storage_integration",
        "snowflake_stage_type",
        "sql_stage_schema",
    ]

    @property
    def snowflake_stage_external_location(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_stage_external_location
        )

    @snowflake_stage_external_location.setter
    def snowflake_stage_external_location(
        self, snowflake_stage_external_location: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stage_external_location = (
            snowflake_stage_external_location
        )

    @property
    def snowflake_stage_external_location_region(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_stage_external_location_region
        )

    @snowflake_stage_external_location_region.setter
    def snowflake_stage_external_location_region(
        self, snowflake_stage_external_location_region: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stage_external_location_region = (
            snowflake_stage_external_location_region
        )

    @property
    def snowflake_stage_storage_integration(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_stage_storage_integration
        )

    @snowflake_stage_storage_integration.setter
    def snowflake_stage_storage_integration(
        self, snowflake_stage_storage_integration: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stage_storage_integration = (
            snowflake_stage_storage_integration
        )

    @property
    def snowflake_stage_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.snowflake_stage_type

    @snowflake_stage_type.setter
    def snowflake_stage_type(self, snowflake_stage_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_stage_type = snowflake_stage_type

    @property
    def sql_stage_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.sql_stage_schema

    @sql_stage_schema.setter
    def sql_stage_schema(self, sql_stage_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_stage_schema = sql_stage_schema

    class Attributes(SQL.Attributes):
        snowflake_stage_external_location: Optional[str] = Field(
            default=None, description=""
        )
        snowflake_stage_external_location_region: Optional[str] = Field(
            default=None, description=""
        )
        snowflake_stage_storage_integration: Optional[str] = Field(
            default=None, description=""
        )
        snowflake_stage_type: Optional[str] = Field(default=None, description="")
        sql_stage_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship

    attributes: SnowflakeStage.Attributes = Field(
        default_factory=lambda: SnowflakeStage.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .schema import Schema  # noqa: E402, F401
