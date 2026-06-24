# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Typed, contract-generated input models for native (v3) app workflows.

``AppInput`` is the base; each ``*Inputs`` class is generated per app/entrypoint
from the app's live input contract (see
``pyatlan.generator.generate_app_inputs``). Pass an instance straight to
``client.app.create(..., inputs=...)``.
"""

from pyatlan.model.app_inputs._base import AppInput
from pyatlan.model.app_inputs.atlan_athena import AtlanAthenaInputs
from pyatlan.model.app_inputs.atlan_mssql import AtlanMssqlInputs
from pyatlan.model.app_inputs.atlan_mysql import AtlanMysqlInputs
from pyatlan.model.app_inputs.atlan_tableau import AtlanTableauInputs
from pyatlan.model.app_inputs.atlan_trino import AtlanTrinoInputs
from pyatlan.model.app_inputs.bigquery_crawler import BigqueryCrawlerInputs
from pyatlan.model.app_inputs.databricks_crawler import DatabricksCrawlerInputs
from pyatlan.model.app_inputs.databricks_miner import DatabricksMinerInputs
from pyatlan.model.app_inputs.kafka_apache import KafkaApacheInputs
from pyatlan.model.app_inputs.kafka_confluent import KafkaConfluentInputs
from pyatlan.model.app_inputs.oracle_crawler import OracleCrawlerInputs
from pyatlan.model.app_inputs.oracle_miner import OracleMinerInputs
from pyatlan.model.app_inputs.postgres_crawler import PostgresCrawlerInputs
from pyatlan.model.app_inputs.postgres_miner import PostgresMinerInputs
from pyatlan.model.app_inputs.powerbi_crawler import PowerbiCrawlerInputs
from pyatlan.model.app_inputs.powerbi_miner import PowerbiMinerInputs
from pyatlan.model.app_inputs.teradata_crawler import TeradataCrawlerInputs
from pyatlan.model.app_inputs.teradata_miner import TeradataMinerInputs

__all__ = [
    "AppInput",
    "AtlanAthenaInputs",
    "AtlanMssqlInputs",
    "AtlanMysqlInputs",
    "AtlanTableauInputs",
    "AtlanTrinoInputs",
    "BigqueryCrawlerInputs",
    "DatabricksCrawlerInputs",
    "DatabricksMinerInputs",
    "KafkaApacheInputs",
    "KafkaConfluentInputs",
    "OracleCrawlerInputs",
    "OracleMinerInputs",
    "PostgresCrawlerInputs",
    "PostgresMinerInputs",
    "PowerbiCrawlerInputs",
    "PowerbiMinerInputs",
    "TeradataCrawlerInputs",
    "TeradataMinerInputs",
]
