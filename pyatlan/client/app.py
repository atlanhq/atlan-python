# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Client for the App workflow APIs.

Creates, runs, schedules, and manages app workflows through the ``/v1/app*`` REST
surface. A workflow is created from an ``app_id`` plus a generic ``inputs`` dict
validated server-side against the app's live input contract — so a connector
never needs a hand-maintained package class.

Obtain via :attr:`pyatlan.client.atlan.AtlanClient.app`.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional, Union

from httpx_retries import Retry
from pydantic.v1 import validate_arguments

from pyatlan.client.common import ApiCaller
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
from pyatlan.model.enums import AppWorkflowRunStatus
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch

LOGGER = logging.getLogger(__name__)

# App-workflow runs are Atlan assets under this qualifiedName prefix; their status
# lives on ``AppWorkflowRun.appWorkflowRunStatus``.
_APP_WORKFLOW_RUN_QN_PREFIX = "default/apps/automation_engine/workflows/"
# Non-terminal run statuses — a workflow with a run in one of these is "running".
_ACTIVE_RUN_STATUSES = [
    AppWorkflowRunStatus.PENDING.value,
    AppWorkflowRunStatus.RUNNING.value,
]
# App-management calls must not retry HTTP 500 (AICHAT-1659): a 500 here is not
# transient (e.g. submitting a workflow that already has an active run), and
# retrying a non-idempotent POST can spawn duplicate runs. This policy mirrors the
# client default but drops 500 from the retryable statuses; every AppClient call
# goes through it via ``_call``.
_APP_NO_500_RETRY = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
    respect_retry_after_header=True,
)

# Search is eventually consistent (~seconds), so a just-started run may not be
# indexed yet. When an idempotent submit gets a server error (most often
# "already running"), briefly poll the index to confirm before surfacing the
# ambiguous 500. Tunable (module-level so callers/tests can override).
_RUN_CHECK_TIMEOUT_SECONDS = 6.0
_RUN_CHECK_INTERVAL_SECONDS = 1.5


def _already_running_error(slug: str):
    return ErrorCode.APP_WORKFLOW_ALREADY_RUNNING.exception_with_parameters(slug)


def _is_server_error(exc: AtlanError) -> bool:
    return getattr(exc.error_code, "http_error_code", 0) >= 500


class AppClient:
    """Create, run, schedule, and manage app workflows."""

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    def _call(self, api, **kwargs):
        """Invoke an app API under the app-management retry policy.

        Applies :data:`_APP_NO_500_RETRY` so app management never retries HTTP 500
        (AICHAT-1659) — a 500 here is not transient and retrying a non-idempotent
        POST can spawn duplicate runs.
        """
        with self._client.max_retries(_APP_NO_500_RETRY):
            return self._client._call_api(api, **kwargs)

    # ----------------------------- discovery ----------------------------- #
    @validate_arguments
    def describe(self, app_id: str) -> AppInfo:
        """Describe an app: native-readiness + entrypoints.

        App-level info (keyed by ``app_id``) — contrast with :meth:`get`, which
        fetches a single workflow by slug.

        :param app_id: marketplace application id (e.g. ``bigquery-crawler``).
        :returns: an :class:`AppInfo`.
        """
        raw = self._call(AppGetInfo.prepare_request(app_id))
        return AppGetInfo.process_response(raw)

    @validate_arguments
    def get_input_contract(
        self, app_id: str, entrypoint: Optional[str] = None
    ) -> AppInputContract:
        """Fetch the app's input contract (JSON Schema) for an entrypoint.

        The source of truth for field names/types/defaults — discover at runtime
        rather than hard-coding inputs.

        :param app_id: marketplace application id.
        :param entrypoint: optional; omit to resolve the app's default.
        :returns: an :class:`AppInputContract`.
        """
        endpoint, query_params = AppGetInputContract.prepare_request(app_id, entrypoint)
        raw = self._call(endpoint, query_params=query_params)
        return AppGetInputContract.process_response(raw)

    # ----------------------------- lifecycle ----------------------------- #
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def create(
        self,
        app_id: str,
        name: str,
        inputs: Union[Dict[str, Any], AppInput],
        entrypoint: Optional[str] = None,
        schedule: Optional[AppSchedule] = None,
        run: Optional[bool] = None,
    ) -> AppResponse:
        """Create a workflow (create + version + publish + optional schedule/run).

        :param app_id: marketplace application id.
        :param name: display label (NOT the identifier — the server mints a slug).
        :param inputs: a values dict matching the app's input contract, or an
            :class:`AppInput` (e.g. from a per-app builder's ``.create()``).
        :param entrypoint: optional; omit to use the app's default.
        :param schedule: optional cron schedule to attach on create.
        :param run: submit a run on create; server defaults to ``True`` when omitted.
        :returns: an :class:`AppResponse` — **persist** ``slug`` for lifecycle ops.

        On a duplicate ``name`` the server responds ``409``; rather than failing, this
        resolves the existing workflow by name and returns it (so re-running a
        migration script is idempotent — *create-or-reuse-by-name*). If more than one
        workflow shares the name, the conflict is re-raised — disambiguate with
        :meth:`get_all` (``name=``).
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
            raw = self._call(endpoint, request_obj=request_obj)
        except AtlanError as exc:
            if is_duplicate_name_conflict(exc):
                return self._reuse_on_conflict(name, exc)
            raise
        return AppCreate.process_response(raw)

    def _reuse_on_conflict(self, name: str, conflict: AtlanError) -> AppResponse:
        """Resolve a duplicate-name ``409`` to the existing workflow's slug.

        Heracles returns ``409`` with the existing slug in the body when ``name``
        already exists; prefer that, and fall back to a by-name lookup. Either way we
        return the existing workflow so callers don't special-case re-runs. A
        non-unique name can't be reused safely, so the conflict is re-raised.
        """
        slug = existing_slug_from_conflict(conflict)
        if slug:
            LOGGER.info("App workflow %r already exists; reusing slug %s", name, slug)
            return AppResponse(slug=slug)
        existing = [w for w in self.get_all(name=name).workflows if w.slug]
        if len(existing) == 1:
            slug = existing[0].slug
            assert slug is not None  # guaranteed by the filter above
            LOGGER.info("App workflow %r already exists; reusing slug %s", name, slug)
            return AppResponse(slug=slug, version=existing[0].version)
        raise conflict

    @validate_arguments
    def get_all(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        name: Optional[str] = None,
    ) -> AppList:
        """List published native app workflows (paginate via ``next_cursor``).

        :param limit: page size (server default 50).
        :param cursor: opaque pagination cursor (pass ``next_cursor`` back).
        :param name: filter to workflows with this exact ``name`` (server ``?name=``);
            use it to resolve a workflow's slug from its name.
        :returns: an :class:`AppList`.
        """
        endpoint, query_params = AppListAll.prepare_request(limit, cursor, name)
        raw = self._call(endpoint, query_params=query_params)
        return AppListAll.process_response(raw)

    @validate_arguments
    def get(self, slug: str) -> AppSummary:
        """Get a single workflow by slug.

        :param slug: the server-minted workflow identity.
        :returns: an :class:`AppSummary`.
        """
        raw = self._call(AppGet.prepare_request(slug))
        return AppGet.process_response(raw)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def update(
        self,
        slug: str,
        inputs: Union[Dict[str, Any], AppInput],
        entrypoint: Optional[str] = None,
    ) -> AppResponse:
        """Replace a workflow's inputs and publish a new version on the same slug.

        Full-replace (send the complete ``inputs``), owner- and
        credential-preserving (omit the credential to keep the persisted one).

        :param slug: the workflow identity.
        :param inputs: the complete input-contract values (dict or
            :class:`AppInput`).
        :param entrypoint: optional; omit to use the app's default.
        :returns: an :class:`AppResponse` with the new ``version``.
        """
        if isinstance(inputs, AppInput):
            inputs = inputs.to_inputs()
        request_kwargs: Dict[str, Any] = {"inputs": inputs}
        if entrypoint is not None:
            request_kwargs["entrypoint"] = entrypoint
        request = UpdateApp(**request_kwargs)
        endpoint, request_obj = AppUpdate.prepare_request(slug, request)
        raw = self._call(endpoint, request_obj=request_obj)
        return AppUpdate.process_response(raw)

    @validate_arguments
    def delete(self, slug: str) -> AppDeleteResponse:
        """Archive/delete a workflow.

        :param slug: the workflow identity.
        :returns: an :class:`AppDeleteResponse`.
        """
        raw = self._call(AppDelete.prepare_request(slug))
        return AppDelete.process_response(raw)

    # ------------------------------ running ------------------------------ #
    def _find_current_run(self, slug: str) -> Optional[AppWorkflowRun]:
        """Return an in-progress (Pending/Running) run for this workflow, else ``None``.

        App-workflow runs are Atlan assets (:class:`AppWorkflowRun`) under the
        workflow's qualifiedName; this searches for one whose
        ``appWorkflowRunStatus`` is non-terminal. Used by :meth:`submit` to guard
        against launching a duplicate run. There is a brief (~seconds) indexing
        lag after a run starts, so a just-started run may not be found yet.
        """
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
        results = self._client.asset.search(request)  # type: ignore[attr-defined]
        for asset in results.current_page() or []:
            if isinstance(asset, AppWorkflowRun):
                return asset
        return None

    def _await_active_run(self, slug: str) -> Optional[AppWorkflowRun]:
        """Poll the search index for an active run, tolerating indexing lag.

        Returns the run once it appears within :data:`_RUN_CHECK_TIMEOUT_SECONDS`,
        else ``None``. Used only on the submit error-recovery path (see
        :meth:`submit`), never on the happy path.
        """
        deadline = time.monotonic() + _RUN_CHECK_TIMEOUT_SECONDS
        while True:
            run = self._find_current_run(slug)
            if run is not None:
                return run
            if time.monotonic() >= deadline:
                return None
            time.sleep(_RUN_CHECK_INTERVAL_SECONDS)

    @validate_arguments
    def submit(self, slug: str, idempotent: bool = False) -> AppRunResponse:
        """Run the workflow's current published version.

        :param slug: the workflow identity.
        :param idempotent: opt-in guard against launching a duplicate run
            (default ``False``). When ``True``, refuse to submit if the workflow
            already has an in-progress run — checked before submitting and, if the
            submit still fails with a server error (the run may not have been
            indexed yet), reconfirmed against the search index before the error is
            surfaced.
        :returns: an :class:`AppRunResponse` with the new ``run_id``.
        :raises InvalidRequestError: if ``idempotent`` and a run is already in
            progress for this workflow.
        """
        if idempotent:
            current = self._find_current_run(slug)
            if current is not None:
                raise _already_running_error(slug)
        try:
            raw = self._call(AppSubmit.prepare_request(slug))
        except AtlanError as exc:
            # A server error on submit is most often "already running", but the
            # run may not have been indexed when we pre-checked. Confirm against
            # the (eventually-consistent) index before surfacing the raw 500.
            if idempotent and _is_server_error(exc):
                current = self._await_active_run(slug)
                if current is not None:
                    raise _already_running_error(slug) from exc
            raise
        return AppSubmit.process_response(raw)

    @validate_arguments
    def get_run(self, run_id: str) -> AppRunResponse:
        """Get a run's status. Poll until :attr:`AppRunResponse.is_terminal`.

        :param run_id: the run identifier.
        :returns: an :class:`AppRunResponse`.
        """
        raw = self._call(AppGetRun.prepare_request(run_id))
        return AppGetRun.process_response(raw)

    @validate_arguments
    def cancel_run(self, run_id: str) -> AppRunCancelResponse:
        """Cancel an in-flight run.

        :param run_id: the run identifier.
        :returns: an :class:`AppRunCancelResponse`.
        """
        raw = self._call(AppCancelRun.prepare_request(run_id))
        return AppCancelRun.process_response(raw)

    # ---------------------------- scheduling ----------------------------- #
    @validate_arguments
    def add_schedule(
        self, slug: str, cron: str, timezone: Optional[str] = None
    ) -> AppScheduleResponse:
        """Attach a cron schedule to the latest published version.

        :param slug: the workflow identity.
        :param cron: cron expression (e.g. ``0 9 * * *``).
        :param timezone: IANA timezone; defaults to ``UTC``.
        :returns: an :class:`AppScheduleResponse` with the new ``trigger_id``.
        """
        # The server rejects a null timezone, so apply the documented UTC default.
        schedule = AppSchedule(cron=cron, timezone=timezone or "UTC")
        endpoint, request_obj = AppAddSchedule.prepare_request(slug, schedule)
        raw = self._call(endpoint, request_obj=request_obj)
        return AppAddSchedule.process_response(raw)

    @validate_arguments
    def remove_schedule(self, slug: str, trigger_id: str) -> AppScheduleDeleteResponse:
        """Remove one schedule (by its ``trigger_id``) from a workflow.

        :param slug: the workflow identity.
        :param trigger_id: the schedule's trigger id.
        :returns: an :class:`AppScheduleDeleteResponse`.
        """
        raw = self._call(AppRemoveSchedule.prepare_request(slug, trigger_id))
        return AppRemoveSchedule.process_response(raw)
