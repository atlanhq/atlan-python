# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import logging.config
from importlib import resources

from pyatlan.utils import REQUEST_ID_FILTER

if resources.is_resource("pyatlan", "logging.conf"):
    with resources.open_text("pyatlan", "logging.conf") as logging_conf:
        logging.config.fileConfig(logging_conf)
LOGGER = logging.getLogger(__name__)
for handler in LOGGER.handlers:
    handler.addFilter(REQUEST_ID_FILTER)
