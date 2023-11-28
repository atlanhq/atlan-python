# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import logging.config
import os
from logging import NullHandler

from pyatlan.utils import REQUEST_ID_FILTER

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(NullHandler())
if os.path.exists("logging.conf"):
    logging.config.fileConfig("logging.conf")
for handler in LOGGER.handlers:
    handler.addFilter(REQUEST_ID_FILTER)
