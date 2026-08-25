# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Async client for the App workflow APIs.

Async mirror of :class:`pyatlan.client.app.AppClient` — same request building and
response parsing (shared via :mod:`pyatlan.client.common.app`); only ``_call_api``
is awaited. Obtain via :attr:`pyatlan.client.aio.client.AsyncAtlanClient.app`.
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Dict, Optional, Union

from pydantic.v1 import validate_arguments

from pyatlan.client.app import (
    _ACTIVE_RUN_STATUSES,
    _APP_NO_500_RETRY,
    _APP_WORKFLOW_RUN_QN_PREFIX,
    _RUN_CHECK_INTERVAL_SECONDS,
    _RUN_CHECK_TIMEOUT_SECONDS,
    _already_running_error,
    _is_server_error,
)
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
    existing_slug_from_conflict,
    is_duplicate_name_conflict,
)
from pyatlan.errors import AtlanError, ErrorCode
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
from pyatlan.model.apps import AppInput
from pyatlan.model.assets import AppWorkflowRun
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch

LOGGER = logging.getLogger(__name__)


class AsyncAppClient:
    """Async version of :class:`pyatlan.client.app.AppClient`."""

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    async def _call(self, api, **kwargs):
        """Invoke an app API under the app-management retry policy (AICHAT-1659).

        Async mirror of :meth:`pyatlan.client.app.AppClient._call`.
        """
        async with self._client.max_retries(_APP_NO_500_RETRY):
            return await self._client._call_api(api, **kwargs)

    # ----------------------------- discovery ----------------------------- #
    @validate_arguments
    async def describe(self, app_id: str) -> AppInfo:
        """Describe an app: native-readiness + entrypoints (contrast :meth:`get`)."""
        raw = await self._call(AppGetInfo.prepare_request(app_id))
        return AppGetInfo.process_response(raw)

    @validate_arguments
    async def get_input_contract(
        self, app_id: str, entrypoint: Optional[str] = None
    ) -> AppInputContract:
        """Fetch the app's input contract (JSON Schema) for an entrypoint."""
        endpoint, query_params = AppGetInputContract.prepare_request(app_id, entrypoint)
        raw = await self._call(endpoint, query_params=query_params)
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
        """Create a workflow (create + version + publish + optional schedule/run).

        On a duplicate ``name`` the server responds ``409``; this resolves the existing
        workflow by name and returns it (idempotent *create-or-reuse-by-name*). A
        non-unique name re-raises the conflict — disambiguate with :meth:`get_all`.
        """
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
        try:
            raw = await self._call(endpoint, request_obj=request_obj)
        except AtlanError as exc:
            if is_duplicate_name_conflict(exc):
                return await self._reuse_on_conflict(name, exc)
            raise
        return AppCreate.process_response(raw)

    async def _reuse_on_conflict(self, name: str, conflict: AtlanError) -> AppResponse:
        """Resolve a duplicate-name ``409`` to the existing workflow's slug (reuse).

        Prefer the slug carried in the ``409`` body; fall back to a by-name lookup. A
        non-unique name can't be reused safely, so the conflict is re-raised.
        """
        slug = existing_slug_from_conflict(conflict)
        if slug:
            LOGGER.info("App workflow %r already exists; reusing slug %s", name, slug)
            return AppResponse(slug=slug)
        existing = [w for w in (await self.get_all(name=name)).workflows if w.slug]
        if len(existing) == 1:
            slug = existing[0].slug
            assert slug is not None  # guaranteed by the filter above
            LOGGER.info("App workflow %r already exists; reusing slug %s", name, slug)
            return AppResponse(slug=slug, version=existing[0].version)
        raise conflict

    @validate_arguments
    async def get_all(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        name: Optional[str] = None,
    ) -> AppList:
        """List published native app workflows (paginate via ``next_cursor``).

        :param name: filter to workflows with this exact ``name`` (server ``?name=``);
            use it to resolve a workflow's slug from its name.
        """
        endpoint, query_params = AppListAll.prepare_request(limit, cursor, name)
        raw = await self._call(endpoint, query_params=query_params)
        return AppListAll.process_response(raw)

    @validate_arguments
    async def get(self, slug: str) -> AppSummary:
        """Get a single workflow by slug."""
        raw = await self._call(AppGet.prepare_request(slug))
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
        raw = await self._call(endpoint, request_obj=request_obj)
        return AppUpdate.process_response(raw)

    @validate_arguments
    async def delete(self, slug: str) -> AppDeleteResponse:
        """Archive/delete a workflow."""
        raw = await self._call(AppDelete.prepare_request(slug))
        return AppDelete.process_response(raw)

    # ------------------------------ running ------------------------------ #
    async def _find_current_run(self, slug: str) -> Optional[AppWorkflowRun]:
        """Async mirror of :meth:`pyatlan.client.app.AppClient._find_current_run`."""
        request = (
            FluentSearch()
            .where(CompoundQuery.active_assets())
            .where(CompoundQuery.asset_type(AppWorkflowRun))
            .where(
                AppWorkflowRun.QUALIFIED_NAME.startswith(
                    f"{_APP_WORKFLOW_RUN_QN_PREFIX}{slug}/"
                )
            )
            .where(AppWorkflowRun.APP_WORKFLOW_RUN_STATUS.within(_ACTIVE_RUN_STATUSES))
            .include_on_results(AppWorkflowRun.APP_WORKFLOW_RUN_STATUS)
            .page_size(1)
        ).to_request()
        results = await self._client.asset.search(request)  # type: ignore[attr-defined]
        for asset in results.current_page() or []:
            if isinstance(asset, AppWorkflowRun):
                return asset
        return None

    async def _await_active_run(self, slug: str) -> Optional[AppWorkflowRun]:
        """Async mirror of :meth:`pyatlan.client.app.AppClient._await_active_run`."""
        deadline = time.monotonic() + _RUN_CHECK_TIMEOUT_SECONDS
        while True:
            run = await self._find_current_run(slug)
            if run is not None:
                return run
            if time.monotonic() >= deadline:
                return None
            await asyncio.sleep(_RUN_CHECK_INTERVAL_SECONDS)

    @validate_arguments
    async def submit(self, slug: str, idempotent: bool = False) -> AppRunResponse:
        """Run the workflow's current published version.

        :param idempotent: opt-in guard against launching a duplicate run
            (default ``False``). When ``True``, refuse to submit if a run is
            already in progress — checked before submitting and reconfirmed
            against the search index if the submit fails with a server error.
        :raises InvalidRequestError: if ``idempotent`` and a run is already in
            progress for this workflow.
        """
        if idempotent:
            current = await self._find_current_run(slug)
            if current is not None:
                raise _already_running_error(slug, current)
        try:
            raw = await self._call(AppSubmit.prepare_request(slug))
        except AtlanError as exc:
            if idempotent and _is_server_error(exc):
                current = await self._await_active_run(slug)
                if current is not None:
                    raise _already_running_error(slug, current) from exc
            raise
        return AppSubmit.process_response(raw)

    @validate_arguments
    async def get_run(self, run_id: str) -> AppRunResponse:
        """Get a run's status. Poll until :attr:`AppRunResponse.is_terminal`."""
        raw = await self._call(AppGetRun.prepare_request(run_id))
        return AppGetRun.process_response(raw)

    @validate_arguments
    async def cancel_run(self, run_id: str) -> AppRunCancelResponse:
        """Cancel an in-flight run."""
        raw = await self._call(AppCancelRun.prepare_request(run_id))
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
        raw = await self._call(endpoint, request_obj=request_obj)
        return AppAddSchedule.process_response(raw)

    @validate_arguments
    async def remove_schedule(
        self, slug: str, trigger_id: str
    ) -> AppScheduleDeleteResponse:
        """Remove one schedule (by its ``trigger_id``) from a workflow."""
        raw = await self._call(AppRemoveSchedule.prepare_request(slug, trigger_id))
        return AppRemoveSchedule.process_response(raw)
