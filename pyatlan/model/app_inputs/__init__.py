# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Typed, contract-generated input models for native (v3) app workflows.

``AppInput`` is the base; each ``*Inputs`` class is generated per app/entrypoint
from the app's live input contract (see
``pyatlan.generator.generate_app_inputs``). Pass an instance straight to
``client.app.create(..., inputs=...)``.
"""

from pyatlan.model.app_inputs._base import AppInput
from pyatlan.model.app_inputs.atlan_mssql import AtlanMssqlInputs
from pyatlan.model.app_inputs.bigquery_crawler import BigqueryCrawlerInputs
from pyatlan.model.app_inputs.bigquery_miner import BigqueryMinerInputs
from pyatlan.model.app_inputs.oracle_crawler import OracleCrawlerInputs
from pyatlan.model.app_inputs.postgres_crawler import PostgresCrawlerInputs
from pyatlan.model.app_inputs.snowflake_crawler import SnowflakeCrawlerInputs

__all__ = [
    "AppInput",
    "AtlanMssqlInputs",
    "BigqueryCrawlerInputs",
    "BigqueryMinerInputs",
    "OracleCrawlerInputs",
    "PostgresCrawlerInputs",
    "SnowflakeCrawlerInputs",
]
