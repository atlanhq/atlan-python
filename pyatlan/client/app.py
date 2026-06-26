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
from typing import Any, Dict, Optional, Union

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


LOGGER = logging.getLogger(__name__)


class AppClient:
    """Create, run, schedule, and manage app workflows."""

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    # ----------------------------- discovery ----------------------------- #
    @validate_arguments
    def describe(self, app_id: str) -> AppInfo:
        """Describe an app: native-readiness + entrypoints.

        App-level info (keyed by ``app_id``) — contrast with :meth:`get`, which
        fetches a single workflow by slug.

        :param app_id: marketplace application id (e.g. ``bigquery-crawler``).
        :returns: an :class:`AppInfo`.
        """
        raw = self._client._call_api(AppGetInfo.prepare_request(app_id))
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
        raw = self._client._call_api(endpoint, query_params=query_params)
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
            raw = self._client._call_api(endpoint, request_obj=request_obj)
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
        raw = self._client._call_api(endpoint, query_params=query_params)
        return AppListAll.process_response(raw)

    @validate_arguments
    def get(self, slug: str) -> AppSummary:
        """Get a single workflow by slug.

        :param slug: the server-minted workflow identity.
        :returns: an :class:`AppSummary`.
        """
        raw = self._client._call_api(AppGet.prepare_request(slug))
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
        raw = self._client._call_api(endpoint, request_obj=request_obj)
        return AppUpdate.process_response(raw)

    @validate_arguments
    def delete(self, slug: str) -> AppDeleteResponse:
        """Archive/delete a workflow.

        :param slug: the workflow identity.
        :returns: an :class:`AppDeleteResponse`.
        """
        raw = self._client._call_api(AppDelete.prepare_request(slug))
        return AppDelete.process_response(raw)

    # ------------------------------ running ------------------------------ #
    @validate_arguments
    def submit(self, slug: str) -> AppRunResponse:
        """Run the workflow's current published version.

        :param slug: the workflow identity.
        :returns: an :class:`AppRunResponse` with the new ``run_id``.
        """
        raw = self._client._call_api(AppSubmit.prepare_request(slug))
        return AppSubmit.process_response(raw)

    @validate_arguments
    def get_run(self, run_id: str) -> AppRunResponse:
        """Get a run's status. Poll until :attr:`AppRunResponse.is_terminal`.

        :param run_id: the run identifier.
        :returns: an :class:`AppRunResponse`.
        """
        raw = self._client._call_api(AppGetRun.prepare_request(run_id))
        return AppGetRun.process_response(raw)

    @validate_arguments
    def cancel_run(self, run_id: str) -> AppRunCancelResponse:
        """Cancel an in-flight run.

        :param run_id: the run identifier.
        :returns: an :class:`AppRunCancelResponse`.
        """
        raw = self._client._call_api(AppCancelRun.prepare_request(run_id))
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
        raw = self._client._call_api(endpoint, request_obj=request_obj)
        return AppAddSchedule.process_response(raw)

    @validate_arguments
    def remove_schedule(self, slug: str, trigger_id: str) -> AppScheduleDeleteResponse:
        """Remove one schedule (by its ``trigger_id``) from a workflow.

        :param slug: the workflow identity.
        :param trigger_id: the schedule's trigger id.
        :returns: an :class:`AppScheduleDeleteResponse`.
        """
        raw = self._client._call_api(
            AppRemoveSchedule.prepare_request(slug, trigger_id)
        )
        return AppRemoveSchedule.process_response(raw)
