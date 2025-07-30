# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import (
    AIModelStatus,
    EthicalAIAccountabilityConfig,
    EthicalAIBiasMitigationConfig,
    EthicalAIEnvironmentalConsciousnessConfig,
    EthicalAIFairnessConfig,
    EthicalAIPrivacyConfig,
    EthicalAIReliabilityAndSafetyConfig,
    EthicalAITransparencyConfig,
)
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)

from .a_i_model import AIModel


class SnowflakeAIModelContext(AIModel):
    """Description"""

    type_name: str = Field(default="SnowflakeAIModelContext", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakeAIModelContext":
            raise ValueError("must be SnowflakeAIModelContext")
        return v

    def __setattr__(self, name, value):
        if name in SnowflakeAIModelContext._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AI_MODEL_DATASETS_DSL: ClassVar[TextField] = TextField(
        "aiModelDatasetsDSL", "aiModelDatasetsDSL"
    )
    """
    Search DSL used to define which assets/datasets are part of the AI model.
    """
    AI_MODEL_STATUS: ClassVar[KeywordField] = KeywordField(
        "aiModelStatus", "aiModelStatus"
    )
    """
    Status of the AI model.
    """
    AI_MODEL_VERSION: ClassVar[KeywordField] = KeywordField(
        "aiModelVersion", "aiModelVersion"
    )
    """
    Version of the AI model.
    """
    ETHICAL_AI_PRIVACY_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIPrivacyConfig", "ethicalAIPrivacyConfig"
    )
    """
    Privacy configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_FAIRNESS_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIFairnessConfig", "ethicalAIFairnessConfig"
    )
    """
    Fairness configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_BIAS_MITIGATION_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIBiasMitigationConfig", "ethicalAIBiasMitigationConfig"
    )
    """
    Bias mitigation configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_RELIABILITY_AND_SAFETY_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIReliabilityAndSafetyConfig", "ethicalAIReliabilityAndSafetyConfig"
    )
    """
    Reliability and safety configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_TRANSPARENCY_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAITransparencyConfig", "ethicalAITransparencyConfig"
    )
    """
    Transparency configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_ACCOUNTABILITY_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIAccountabilityConfig", "ethicalAIAccountabilityConfig"
    )
    """
    Accountability configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_ENVIRONMENTAL_CONSCIOUSNESS_CONFIG: ClassVar[KeywordField] = (
        KeywordField(
            "ethicalAIEnvironmentalConsciousnessConfig",
            "ethicalAIEnvironmentalConsciousnessConfig",
        )
    )
    """
    Environmental consciousness configuration for ensuring the ethical use of an AI asset
    """
    QUERY_COUNT: ClassVar[NumericField] = NumericField("queryCount", "queryCount")
    """
    Number of times this asset has been queried.
    """
    QUERY_USER_COUNT: ClassVar[NumericField] = NumericField(
        "queryUserCount", "queryUserCount"
    )
    """
    Number of unique users who have queried this asset.
    """
    QUERY_USER_MAP: ClassVar[KeywordField] = KeywordField(
        "queryUserMap", "queryUserMap"
    )
    """
    Map of unique users who have queried this asset to the number of times they have queried it.
    """
    QUERY_COUNT_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "queryCountUpdatedAt", "queryCountUpdatedAt"
    )
    """
    Time (epoch) at which the query count was last updated, in milliseconds.
    """
    DATABASE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "databaseName", "databaseName.keyword", "databaseName"
    )
    """
    Simple name of the database in which this SQL asset exists, or empty if it does not exist within a database.
    """
    DATABASE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "databaseQualifiedName", "databaseQualifiedName"
    )
    """
    Unique name of the database in which this SQL asset exists, or empty if it does not exist within a database.
    """
    SCHEMA_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "schemaName", "schemaName.keyword", "schemaName"
    )
    """
    Simple name of the schema in which this SQL asset exists, or empty if it does not exist within a schema.
    """
    SCHEMA_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "schemaQualifiedName", "schemaQualifiedName"
    )
    """
    Unique name of the schema in which this SQL asset exists, or empty if it does not exist within a schema.
    """
    TABLE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "tableName", "tableName.keyword", "tableName"
    )
    """
    Simple name of the table in which this SQL asset exists, or empty if it does not exist within a table.
    """
    TABLE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "tableQualifiedName", "tableQualifiedName"
    )
    """
    Unique name of the table in which this SQL asset exists, or empty if it does not exist within a table.
    """
    VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "viewName", "viewName.keyword", "viewName"
    )
    """
    Simple name of the view in which this SQL asset exists, or empty if it does not exist within a view.
    """
    VIEW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "viewQualifiedName", "viewQualifiedName"
    )
    """
    Unique name of the view in which this SQL asset exists, or empty if it does not exist within a view.
    """
    CALCULATION_VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "calculationViewName", "calculationViewName.keyword", "calculationViewName"
    )
    """
    Simple name of the calculation view in which this SQL asset exists, or empty if it does not exist within a calculation view.
    """  # noqa: E501
    CALCULATION_VIEW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "calculationViewQualifiedName", "calculationViewQualifiedName"
    )
    """
    Unique name of the calculation view in which this SQL asset exists, or empty if it does not exist within a calculation view.
    """  # noqa: E501
    IS_PROFILED: ClassVar[BooleanField] = BooleanField("isProfiled", "isProfiled")
    """
    Whether this asset has been profiled (true) or not (false).
    """
    LAST_PROFILED_AT: ClassVar[NumericField] = NumericField(
        "lastProfiledAt", "lastProfiledAt"
    )
    """
    Time (epoch) at which this asset was last profiled, in milliseconds.
    """
    SQL_AI_MODEL_CONTEXT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "sqlAIModelContextQualifiedName", "sqlAIModelContextQualifiedName"
    )
    """
    Unique name of the context in which the model versions exist, or empty if it does not exist within an AI model context.
    """  # noqa: E501

    DBT_SOURCES: ClassVar[RelationField] = RelationField("dbtSources")
    """
    TBC
    """
    SQL_DBT_MODELS: ClassVar[RelationField] = RelationField("sqlDbtModels")
    """
    TBC
    """
    DBT_TESTS: ClassVar[RelationField] = RelationField("dbtTests")
    """
    TBC
    """
    SNOWFLAKE_AI_MODEL_SCHEMA: ClassVar[RelationField] = RelationField(
        "snowflakeAIModelSchema"
    )
    """
    TBC
    """
    SNOWFLAKE_AI_MODEL_VERSIONS: ClassVar[RelationField] = RelationField(
        "snowflakeAIModelVersions"
    )
    """
    TBC
    """
    SQL_DBT_SOURCES: ClassVar[RelationField] = RelationField("sqlDBTSources")
    """
    TBC
    """
    DBT_MODELS: ClassVar[RelationField] = RelationField("dbtModels")
    """
    TBC
    """
    DBT_SEED_ASSETS: ClassVar[RelationField] = RelationField("dbtSeedAssets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "ai_model_datasets_d_s_l",
        "ai_model_status",
        "ai_model_version",
        "ethical_a_i_privacy_config",
        "ethical_a_i_fairness_config",
        "ethical_a_i_bias_mitigation_config",
        "ethical_a_i_reliability_and_safety_config",
        "ethical_a_i_transparency_config",
        "ethical_a_i_accountability_config",
        "ethical_a_i_environmental_consciousness_config",
        "query_count",
        "query_user_count",
        "query_user_map",
        "query_count_updated_at",
        "database_name",
        "database_qualified_name",
        "schema_name",
        "schema_qualified_name",
        "table_name",
        "table_qualified_name",
        "view_name",
        "view_qualified_name",
        "calculation_view_name",
        "calculation_view_qualified_name",
        "is_profiled",
        "last_profiled_at",
        "sql_a_i_model_context_qualified_name",
        "dbt_sources",
        "sql_dbt_models",
        "dbt_tests",
        "snowflake_a_i_model_schema",
        "snowflake_a_i_model_versions",
        "sql_dbt_sources",
        "dbt_models",
        "dbt_seed_assets",
    ]

    @property
    def ai_model_datasets_d_s_l(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.ai_model_datasets_d_s_l
        )

    @ai_model_datasets_d_s_l.setter
    def ai_model_datasets_d_s_l(self, ai_model_datasets_d_s_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model_datasets_d_s_l = ai_model_datasets_d_s_l

    @property
    def ai_model_status(self) -> Optional[AIModelStatus]:
        return None if self.attributes is None else self.attributes.ai_model_status

    @ai_model_status.setter
    def ai_model_status(self, ai_model_status: Optional[AIModelStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model_status = ai_model_status

    @property
    def ai_model_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ai_model_version

    @ai_model_version.setter
    def ai_model_version(self, ai_model_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model_version = ai_model_version

    @property
    def ethical_a_i_privacy_config(self) -> Optional[EthicalAIPrivacyConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_privacy_config
        )

    @ethical_a_i_privacy_config.setter
    def ethical_a_i_privacy_config(
        self, ethical_a_i_privacy_config: Optional[EthicalAIPrivacyConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_privacy_config = ethical_a_i_privacy_config

    @property
    def ethical_a_i_fairness_config(self) -> Optional[EthicalAIFairnessConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_fairness_config
        )

    @ethical_a_i_fairness_config.setter
    def ethical_a_i_fairness_config(
        self, ethical_a_i_fairness_config: Optional[EthicalAIFairnessConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_fairness_config = ethical_a_i_fairness_config

    @property
    def ethical_a_i_bias_mitigation_config(
        self,
    ) -> Optional[EthicalAIBiasMitigationConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_bias_mitigation_config
        )

    @ethical_a_i_bias_mitigation_config.setter
    def ethical_a_i_bias_mitigation_config(
        self,
        ethical_a_i_bias_mitigation_config: Optional[EthicalAIBiasMitigationConfig],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_bias_mitigation_config = (
            ethical_a_i_bias_mitigation_config
        )

    @property
    def ethical_a_i_reliability_and_safety_config(
        self,
    ) -> Optional[EthicalAIReliabilityAndSafetyConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_reliability_and_safety_config
        )

    @ethical_a_i_reliability_and_safety_config.setter
    def ethical_a_i_reliability_and_safety_config(
        self,
        ethical_a_i_reliability_and_safety_config: Optional[
            EthicalAIReliabilityAndSafetyConfig
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_reliability_and_safety_config = (
            ethical_a_i_reliability_and_safety_config
        )

    @property
    def ethical_a_i_transparency_config(self) -> Optional[EthicalAITransparencyConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_transparency_config
        )

    @ethical_a_i_transparency_config.setter
    def ethical_a_i_transparency_config(
        self, ethical_a_i_transparency_config: Optional[EthicalAITransparencyConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_transparency_config = (
            ethical_a_i_transparency_config
        )

    @property
    def ethical_a_i_accountability_config(
        self,
    ) -> Optional[EthicalAIAccountabilityConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_accountability_config
        )

    @ethical_a_i_accountability_config.setter
    def ethical_a_i_accountability_config(
        self, ethical_a_i_accountability_config: Optional[EthicalAIAccountabilityConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_accountability_config = (
            ethical_a_i_accountability_config
        )

    @property
    def ethical_a_i_environmental_consciousness_config(
        self,
    ) -> Optional[EthicalAIEnvironmentalConsciousnessConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_environmental_consciousness_config
        )

    @ethical_a_i_environmental_consciousness_config.setter
    def ethical_a_i_environmental_consciousness_config(
        self,
        ethical_a_i_environmental_consciousness_config: Optional[
            EthicalAIEnvironmentalConsciousnessConfig
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_environmental_consciousness_config = (
            ethical_a_i_environmental_consciousness_config
        )

    @property
    def query_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_count

    @query_count.setter
    def query_count(self, query_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_count = query_count

    @property
    def query_user_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_user_count

    @query_user_count.setter
    def query_user_count(self, query_user_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_user_count = query_user_count

    @property
    def query_user_map(self) -> Optional[Dict[str, int]]:
        return None if self.attributes is None else self.attributes.query_user_map

    @query_user_map.setter
    def query_user_map(self, query_user_map: Optional[Dict[str, int]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_user_map = query_user_map

    @property
    def query_count_updated_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.query_count_updated_at
        )

    @query_count_updated_at.setter
    def query_count_updated_at(self, query_count_updated_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_count_updated_at = query_count_updated_at

    @property
    def database_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.database_name

    @database_name.setter
    def database_name(self, database_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database_name = database_name

    @property
    def database_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.database_qualified_name
        )

    @database_qualified_name.setter
    def database_qualified_name(self, database_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database_qualified_name = database_qualified_name

    @property
    def schema_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.schema_name

    @schema_name.setter
    def schema_name(self, schema_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_name = schema_name

    @property
    def schema_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.schema_qualified_name
        )

    @schema_qualified_name.setter
    def schema_qualified_name(self, schema_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_qualified_name = schema_qualified_name

    @property
    def table_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.table_name

    @table_name.setter
    def table_name(self, table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_name = table_name

    @property
    def table_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.table_qualified_name

    @table_qualified_name.setter
    def table_qualified_name(self, table_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_qualified_name = table_qualified_name

    @property
    def view_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.view_name

    @view_name.setter
    def view_name(self, view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_name = view_name

    @property
    def view_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.view_qualified_name

    @view_qualified_name.setter
    def view_qualified_name(self, view_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_qualified_name = view_qualified_name

    @property
    def calculation_view_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.calculation_view_name
        )

    @calculation_view_name.setter
    def calculation_view_name(self, calculation_view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculation_view_name = calculation_view_name

    @property
    def calculation_view_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.calculation_view_qualified_name
        )

    @calculation_view_qualified_name.setter
    def calculation_view_qualified_name(
        self, calculation_view_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculation_view_qualified_name = (
            calculation_view_qualified_name
        )

    @property
    def is_profiled(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_profiled

    @is_profiled.setter
    def is_profiled(self, is_profiled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_profiled = is_profiled

    @property
    def last_profiled_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.last_profiled_at

    @last_profiled_at.setter
    def last_profiled_at(self, last_profiled_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_profiled_at = last_profiled_at

    @property
    def sql_a_i_model_context_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_a_i_model_context_qualified_name
        )

    @sql_a_i_model_context_qualified_name.setter
    def sql_a_i_model_context_qualified_name(
        self, sql_a_i_model_context_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_a_i_model_context_qualified_name = (
            sql_a_i_model_context_qualified_name
        )

    @property
    def dbt_sources(self) -> Optional[List[DbtSource]]:
        return None if self.attributes is None else self.attributes.dbt_sources

    @dbt_sources.setter
    def dbt_sources(self, dbt_sources: Optional[List[DbtSource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_sources = dbt_sources

    @property
    def sql_dbt_models(self) -> Optional[List[DbtModel]]:
        return None if self.attributes is None else self.attributes.sql_dbt_models

    @sql_dbt_models.setter
    def sql_dbt_models(self, sql_dbt_models: Optional[List[DbtModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_dbt_models = sql_dbt_models

    @property
    def dbt_tests(self) -> Optional[List[DbtTest]]:
        return None if self.attributes is None else self.attributes.dbt_tests

    @dbt_tests.setter
    def dbt_tests(self, dbt_tests: Optional[List[DbtTest]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tests = dbt_tests

    @property
    def snowflake_a_i_model_schema(self) -> Optional[Schema]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_a_i_model_schema
        )

    @snowflake_a_i_model_schema.setter
    def snowflake_a_i_model_schema(self, snowflake_a_i_model_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_a_i_model_schema = snowflake_a_i_model_schema

    @property
    def snowflake_a_i_model_versions(self) -> Optional[List[SnowflakeAIModelVersion]]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_a_i_model_versions
        )

    @snowflake_a_i_model_versions.setter
    def snowflake_a_i_model_versions(
        self, snowflake_a_i_model_versions: Optional[List[SnowflakeAIModelVersion]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_a_i_model_versions = snowflake_a_i_model_versions

    @property
    def sql_dbt_sources(self) -> Optional[List[DbtSource]]:
        return None if self.attributes is None else self.attributes.sql_dbt_sources

    @sql_dbt_sources.setter
    def sql_dbt_sources(self, sql_dbt_sources: Optional[List[DbtSource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_dbt_sources = sql_dbt_sources

    @property
    def dbt_models(self) -> Optional[List[DbtModel]]:
        return None if self.attributes is None else self.attributes.dbt_models

    @dbt_models.setter
    def dbt_models(self, dbt_models: Optional[List[DbtModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_models = dbt_models

    @property
    def dbt_seed_assets(self) -> Optional[List[DbtSeed]]:
        return None if self.attributes is None else self.attributes.dbt_seed_assets

    @dbt_seed_assets.setter
    def dbt_seed_assets(self, dbt_seed_assets: Optional[List[DbtSeed]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_seed_assets = dbt_seed_assets

    class Attributes(AIModel.Attributes):
        ai_model_datasets_d_s_l: Optional[str] = Field(default=None, description="")
        ai_model_status: Optional[AIModelStatus] = Field(default=None, description="")
        ai_model_version: Optional[str] = Field(default=None, description="")
        ethical_a_i_privacy_config: Optional[EthicalAIPrivacyConfig] = Field(
            default=None, description=""
        )
        ethical_a_i_fairness_config: Optional[EthicalAIFairnessConfig] = Field(
            default=None, description=""
        )
        ethical_a_i_bias_mitigation_config: Optional[EthicalAIBiasMitigationConfig] = (
            Field(default=None, description="")
        )
        ethical_a_i_reliability_and_safety_config: Optional[
            EthicalAIReliabilityAndSafetyConfig
        ] = Field(default=None, description="")
        ethical_a_i_transparency_config: Optional[EthicalAITransparencyConfig] = Field(
            default=None, description=""
        )
        ethical_a_i_accountability_config: Optional[EthicalAIAccountabilityConfig] = (
            Field(default=None, description="")
        )
        ethical_a_i_environmental_consciousness_config: Optional[
            EthicalAIEnvironmentalConsciousnessConfig
        ] = Field(default=None, description="")
        query_count: Optional[int] = Field(default=None, description="")
        query_user_count: Optional[int] = Field(default=None, description="")
        query_user_map: Optional[Dict[str, int]] = Field(default=None, description="")
        query_count_updated_at: Optional[datetime] = Field(default=None, description="")
        database_name: Optional[str] = Field(default=None, description="")
        database_qualified_name: Optional[str] = Field(default=None, description="")
        schema_name: Optional[str] = Field(default=None, description="")
        schema_qualified_name: Optional[str] = Field(default=None, description="")
        table_name: Optional[str] = Field(default=None, description="")
        table_qualified_name: Optional[str] = Field(default=None, description="")
        view_name: Optional[str] = Field(default=None, description="")
        view_qualified_name: Optional[str] = Field(default=None, description="")
        calculation_view_name: Optional[str] = Field(default=None, description="")
        calculation_view_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        is_profiled: Optional[bool] = Field(default=None, description="")
        last_profiled_at: Optional[datetime] = Field(default=None, description="")
        sql_a_i_model_context_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        dbt_sources: Optional[List[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        sql_dbt_models: Optional[List[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        dbt_tests: Optional[List[DbtTest]] = Field(
            default=None, description=""
        )  # relationship
        snowflake_a_i_model_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship
        snowflake_a_i_model_versions: Optional[List[SnowflakeAIModelVersion]] = Field(
            default=None, description=""
        )  # relationship
        sql_dbt_sources: Optional[List[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        dbt_models: Optional[List[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        dbt_seed_assets: Optional[List[DbtSeed]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SnowflakeAIModelContext.Attributes = Field(
        default_factory=lambda: SnowflakeAIModelContext.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .dbt_model import DbtModel  # noqa: E402, F401
from .dbt_seed import DbtSeed  # noqa: E402, F401
from .dbt_source import DbtSource  # noqa: E402, F401
from .dbt_test import DbtTest  # noqa: E402, F401
from .schema import Schema  # noqa: E402, F401
from .snowflake_a_i_model_version import SnowflakeAIModelVersion  # noqa: E402, F401
