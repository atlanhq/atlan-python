# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import logging.config
import os

from pyatlan.utils import REQUEST_ID_FILTER

# Version information
try:
    from importlib.metadata import version

    __version__ = version("pyatlan")
except ImportError:
    # Fallback for older Python versions
    try:
        import pkg_resources

        __version__ = pkg_resources.get_distribution("pyatlan").version
    except Exception:
        __version__ = "unknown"

if os.path.exists("logging.conf"):
    logging.config.fileConfig("logging.conf")
LOGGER = logging.getLogger(__name__)
for handler in LOGGER.handlers:
    handler.addFilter(REQUEST_ID_FILTER)
