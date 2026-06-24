# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Async client for the App workflow APIs.

Async mirror of :class:`pyatlan.client.app.AppClient` — same request building and
response parsing (shared via :mod:`pyatlan.client.common.app`); only ``_call_api``
is awaited. Obtain via :attr:`pyatlan.client.aio.client.AsyncAtlanClient.app`.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union

from pydantic.v1 import validate_arguments

from pyatlan.client.common import AsyncApiCaller
from pyatlan.client.common.app import (
    AppAddSchedule,
    AppCancelRun,
    AppCreate,
    AppDelete,
    AppGet,
    AppGetInfo,
    AppGetInputContract,
    AppGetRun,
    AppListAll,
    AppRemoveSchedule,
    AppSubmit,
    AppUpdate,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.apps import AppInput
from pyatlan.model.app import (
    AppDeleteResponse,
    AppInfo,
    AppInputContract,
    AppList,
    AppResponse,
    AppRunCancelResponse,
    AppRunResponse,
    AppSchedule,
    AppScheduleDeleteResponse,
    AppScheduleResponse,
    AppSummary,
    CreateApp,
    UpdateApp,
)


class AsyncAppClient:
    """Async version of :class:`pyatlan.client.app.AppClient`."""

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    # ----------------------------- discovery ----------------------------- #
    @validate_arguments
    async def describe(self, app_id: str) -> AppInfo:
        """Describe an app: native-readiness + entrypoints (contrast :meth:`get`)."""
        raw = await self._client._call_api(AppGetInfo.prepare_request(app_id))
        return AppGetInfo.process_response(raw)

    @validate_arguments
    async def get_input_contract(
        self, app_id: str, entrypoint: Optional[str] = None
    ) -> AppInputContract:
        """Fetch the app's input contract (JSON Schema) for an entrypoint."""
        endpoint, query_params = AppGetInputContract.prepare_request(app_id, entrypoint)
        raw = await self._client._call_api(endpoint, query_params=query_params)
        return AppGetInputContract.process_response(raw)

    # ----------------------------- lifecycle ----------------------------- #
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    async def create(
        self,
        app_id: str,
        name: str,
        inputs: Union[Dict[str, Any], AppInput],
        entrypoint: Optional[str] = None,
        schedule: Optional[AppSchedule] = None,
        run: Optional[bool] = None,
    ) -> AppResponse:
        """Create a workflow (create + version + publish + optional schedule/run)."""
        if isinstance(inputs, AppInput):
            inputs = inputs.to_inputs()
        # Only include optional fields when provided so exclude_unset omits them
        # (passing None explicitly would serialize as null and reach the server).
        request_kwargs: Dict[str, Any] = {
            "app_id": app_id,
            "name": name,
            "inputs": inputs,
        }
        if entrypoint is not None:
            request_kwargs["entrypoint"] = entrypoint
        if schedule is not None:
            request_kwargs["schedule"] = schedule
        if run is not None:
            request_kwargs["run"] = run
        request = CreateApp(**request_kwargs)
        endpoint, request_obj = AppCreate.prepare_request(request)
        raw = await self._client._call_api(endpoint, request_obj=request_obj)
        return AppCreate.process_response(raw)

    @validate_arguments
    async def get_all(
        self, limit: Optional[int] = None, cursor: Optional[str] = None
    ) -> AppList:
        """List published native app workflows (paginate via ``next_cursor``)."""
        endpoint, query_params = AppListAll.prepare_request(limit, cursor)
        raw = await self._client._call_api(endpoint, query_params=query_params)
        return AppListAll.process_response(raw)

    @validate_arguments
    async def get(self, slug: str) -> AppSummary:
        """Get a single workflow by slug."""
        raw = await self._client._call_api(AppGet.prepare_request(slug))
        return AppGet.process_response(raw)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    async def update(
        self,
        slug: str,
        inputs: Union[Dict[str, Any], AppInput],
        entrypoint: Optional[str] = None,
    ) -> AppResponse:
        """Replace a workflow's inputs and publish a new version on the same slug."""
        if isinstance(inputs, AppInput):
            inputs = inputs.to_inputs()
        request_kwargs: Dict[str, Any] = {"inputs": inputs}
        if entrypoint is not None:
            request_kwargs["entrypoint"] = entrypoint
        request = UpdateApp(**request_kwargs)
        endpoint, request_obj = AppUpdate.prepare_request(slug, request)
        raw = await self._client._call_api(endpoint, request_obj=request_obj)
        return AppUpdate.process_response(raw)

    @validate_arguments
    async def delete(self, slug: str) -> AppDeleteResponse:
        """Archive/delete a workflow."""
        raw = await self._client._call_api(AppDelete.prepare_request(slug))
        return AppDelete.process_response(raw)

    # ------------------------------ running ------------------------------ #
    @validate_arguments
    async def submit(self, slug: str) -> AppRunResponse:
        """Run the workflow's current published version."""
        raw = await self._client._call_api(AppSubmit.prepare_request(slug))
        return AppSubmit.process_response(raw)

    @validate_arguments
    async def get_run(self, run_id: str) -> AppRunResponse:
        """Get a run's status. Poll until :attr:`AppRunResponse.is_terminal`."""
        raw = await self._client._call_api(AppGetRun.prepare_request(run_id))
        return AppGetRun.process_response(raw)

    @validate_arguments
    async def cancel_run(self, run_id: str) -> AppRunCancelResponse:
        """Cancel an in-flight run."""
        raw = await self._client._call_api(AppCancelRun.prepare_request(run_id))
        return AppCancelRun.process_response(raw)

    # ---------------------------- scheduling ----------------------------- #
    @validate_arguments
    async def add_schedule(
        self, slug: str, cron: str, timezone: Optional[str] = None
    ) -> AppScheduleResponse:
        """Attach a cron schedule to the latest published version."""
        # The server rejects a null timezone, so apply the documented UTC default.
        schedule = AppSchedule(cron=cron, timezone=timezone or "UTC")
        endpoint, request_obj = AppAddSchedule.prepare_request(slug, schedule)
        raw = await self._client._call_api(endpoint, request_obj=request_obj)
        return AppAddSchedule.process_response(raw)

    @validate_arguments
    async def remove_schedule(
        self, slug: str, trigger_id: str
    ) -> AppScheduleDeleteResponse:
        """Remove one schedule (by its ``trigger_id``) from a workflow."""
        raw = await self._client._call_api(
            AppRemoveSchedule.prepare_request(slug, trigger_id)
        )
        return AppRemoveSchedule.process_response(raw)
