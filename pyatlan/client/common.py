# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Generator, Protocol, runtime_checkable

from urllib3.util.retry import Retry

HTTPS_PREFIX = "https://"
HTTP_PREFIX = "http://"
CONNECTION_RETRY = Retry(
    total=10,
    backoff_factor=1,
    status_forcelist=[403],
    allowed_methods=["GET"],
)


@runtime_checkable
class ApiCaller(Protocol):
    def _call_api(
        self, api, query_params=None, request_obj=None, exclude_unset: bool = True
    ):
        pass

    def max_retries(
        self, max_retries: Retry = CONNECTION_RETRY
    ) -> Generator[None, None, None]:
        pass
