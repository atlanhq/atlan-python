# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Typed models and fluent builders for app workflows.

Each per-app builder mirrors the UI's 3-step wizard (Credential ->
Connection -> Metadata); see ``pyatlan.generator.generate_apps``.
"""

from pyatlan.model.apps._base import AppBuilder, AppInput
from pyatlan.model.apps.bigquery_crawler import BigqueryCrawler, BigqueryCrawlerInputs
from pyatlan.model.apps.anaplan import Anaplan, AnaplanInputs
from pyatlan.model.apps.atlan_athena import AtlanAthena, AtlanAthenaInputs
from pyatlan.model.apps.atlan_dbt import AtlanDbt, AtlanDbtInputs
from pyatlan.model.apps.atlan_dynamodb import AtlanDynamodb, AtlanDynamodbInputs
from pyatlan.model.apps.atlan_glue import AtlanGlue, AtlanGlueInputs
from pyatlan.model.apps.atlan_knowledge_catalog import (
    AtlanKnowledgeCatalog,
    AtlanKnowledgeCatalogInputs,
)
from pyatlan.model.apps.atlan_metabase import AtlanMetabase, AtlanMetabaseInputs
from pyatlan.model.apps.atlan_mssql import AtlanMssql, AtlanMssqlInputs
from pyatlan.model.apps.atlan_mysql import AtlanMysql, AtlanMysqlInputs
from pyatlan.model.apps.atlan_presto import AtlanPresto, AtlanPrestoInputs
from pyatlan.model.apps.atlan_quicksight import AtlanQuicksight, AtlanQuicksightInputs
from pyatlan.model.apps.atlan_redash import AtlanRedash, AtlanRedashInputs
from pyatlan.model.apps.atlan_sigma import AtlanSigma, AtlanSigmaInputs
from pyatlan.model.apps.atlan_tableau import AtlanTableau, AtlanTableauInputs
from pyatlan.model.apps.atlan_trino import AtlanTrino, AtlanTrinoInputs
from pyatlan.model.apps.databricks_crawler import (
    DatabricksCrawler,
    DatabricksCrawlerInputs,
)
from pyatlan.model.apps.databricks_miner import DatabricksMiner, DatabricksMinerInputs
from pyatlan.model.apps.hive_crawler import HiveCrawler, HiveCrawlerInputs
from pyatlan.model.apps.kafka_apache import KafkaApache, KafkaApacheInputs
from pyatlan.model.apps.kafka_confluent import KafkaConfluent, KafkaConfluentInputs
from pyatlan.model.apps.mongodbatlas_atlas import (
    MongodbatlasAtlas,
    MongodbatlasAtlasInputs,
)
from pyatlan.model.apps.oracle_crawler import OracleCrawler, OracleCrawlerInputs
from pyatlan.model.apps.oracle_miner import OracleMiner, OracleMinerInputs
from pyatlan.model.apps.postgres_crawler import PostgresCrawler, PostgresCrawlerInputs
from pyatlan.model.apps.postgres_miner import PostgresMiner, PostgresMinerInputs
from pyatlan.model.apps.powerbi_crawler import PowerbiCrawler, PowerbiCrawlerInputs
from pyatlan.model.apps.powerbi_miner import PowerbiMiner, PowerbiMinerInputs
from pyatlan.model.apps.snowflake_crawler import (
    SnowflakeCrawler,
    SnowflakeCrawlerInputs,
)
from pyatlan.model.apps.snowflake_miner import SnowflakeMiner, SnowflakeMinerInputs
from pyatlan.model.apps.teradata_crawler import TeradataCrawler, TeradataCrawlerInputs
from pyatlan.model.apps.teradata_miner import TeradataMiner, TeradataMinerInputs

__all__ = [
    "AppInput",
    "AppBuilder",
    "BigqueryCrawler",
    "BigqueryCrawlerInputs",
    "Anaplan",
    "AnaplanInputs",
    "AtlanAthena",
    "AtlanAthenaInputs",
    "AtlanDbt",
    "AtlanDbtInputs",
    "AtlanDynamodb",
    "AtlanDynamodbInputs",
    "AtlanGlue",
    "AtlanGlueInputs",
    "AtlanKnowledgeCatalog",
    "AtlanKnowledgeCatalogInputs",
    "AtlanMetabase",
    "AtlanMetabaseInputs",
    "AtlanMssql",
    "AtlanMssqlInputs",
    "AtlanMysql",
    "AtlanMysqlInputs",
    "AtlanPresto",
    "AtlanPrestoInputs",
    "AtlanQuicksight",
    "AtlanQuicksightInputs",
    "AtlanRedash",
    "AtlanRedashInputs",
    "AtlanSigma",
    "AtlanSigmaInputs",
    "AtlanTableau",
    "AtlanTableauInputs",
    "AtlanTrino",
    "AtlanTrinoInputs",
    "DatabricksCrawler",
    "DatabricksCrawlerInputs",
    "DatabricksMiner",
    "DatabricksMinerInputs",
    "HiveCrawler",
    "HiveCrawlerInputs",
    "KafkaApache",
    "KafkaApacheInputs",
    "KafkaConfluent",
    "KafkaConfluentInputs",
    "MongodbatlasAtlas",
    "MongodbatlasAtlasInputs",
    "OracleCrawler",
    "OracleCrawlerInputs",
    "OracleMiner",
    "OracleMinerInputs",
    "PostgresCrawler",
    "PostgresCrawlerInputs",
    "PostgresMiner",
    "PostgresMinerInputs",
    "PowerbiCrawler",
    "PowerbiCrawlerInputs",
    "PowerbiMiner",
    "PowerbiMinerInputs",
    "SnowflakeCrawler",
    "SnowflakeCrawlerInputs",
    "SnowflakeMiner",
    "SnowflakeMinerInputs",
    "TeradataCrawler",
    "TeradataCrawlerInputs",
    "TeradataMiner",
    "TeradataMinerInputs",
]
