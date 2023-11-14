# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import logging.config
import os
from logging import NullHandler

# r_log = logging.getLogger('urllib3')
# r_log.setLevel(logging.DEBUG)
#
# # logging from urllib3 to console
# ch = logging.FileHandler("/tmp/requests.log")
# ch.setLevel(logging.DEBUG)
# r_log.addHandler(ch)

logging.getLogger(__name__).addHandler(NullHandler())
if os.path.exists("logging.conf"):
    logging.config.fileConfig("logging.conf")
