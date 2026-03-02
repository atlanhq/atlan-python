# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

# Import all constants from the original unit-test constants for parity.
from tests.unit.constants import *  # noqa: F401, F403
from tests.unit.constants import TEST_WORKFLOW_CLIENT_METHODS as _LEGACY_WF_METHODS

TEST_WORKFLOW_CLIENT_METHODS = {  # noqa: F811
    ("updater" if k == "update" else k): v for k, v in _LEGACY_WF_METHODS.items()
}
