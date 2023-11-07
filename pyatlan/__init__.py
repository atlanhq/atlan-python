# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import logging.config
import os
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
if os.path.exists("logging.conf"):
    logging.config.fileConfig("logging.conf")
