# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Shared business logic for the native (v3) App APIs (BLDX-1472).

Each operation exposes ``prepare_request`` / ``process_response`` static methods
so the sync (:class:`pyatlan.client.app.AppClient`) and async
(:class:`pyatlan.client.aio.app.AsyncAppClient`) clients share identical request
building and response parsing — only the ``_call_api`` await differs.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from pyatlan.client.constants import (
    ADD_APP_SCHEDULE,
    CANCEL_APP_RUN,
    CREATE_APP_WORKFLOW,
    DELETE_APP_WORKFLOW,
    GET_APP,
    GET_APP_INPUT_CONTRACT,
    GET_APP_RUN,
    GET_APP_WORKFLOW,
    LIST_APP_WORKFLOWS,
    REMOVE_APP_SCHEDULE,
    SUBMIT_APP_WORKFLOW,
    UPDATE_APP_WORKFLOW,
)
from pyatlan.client.constants import API
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


class AppGetInfo:
    """``GET /v1/apps/{app_id}`` — describe an app (native-readiness, entrypoints)."""

    @staticmethod
    def prepare_request(app_id: str) -> API:
        return GET_APP.format_path({"app_id": app_id})

    @staticmethod
    def process_response(raw_json: Any) -> AppInfo:
        return AppInfo.parse_obj(raw_json)


class AppGetInputContract:
    """``GET /v1/apps/{app_id}/inputs`` — the app's input contract (JSON Schema)."""

    @staticmethod
    def prepare_request(
        app_id: str, entrypoint: Optional[str] = None
    ) -> Tuple[API, Dict[str, Any]]:
        endpoint = GET_APP_INPUT_CONTRACT.format_path({"app_id": app_id})
        query_params: Dict[str, Any] = {}
        if entrypoint:
            query_params["entrypoint"] = entrypoint
        return endpoint, query_params

    @staticmethod
    def process_response(raw_json: Any) -> AppInputContract:
        return AppInputContract.parse_obj(raw_json)


class AppCreate:
    """``POST /v1/app`` — create + version + publish + (schedule) + (run)."""

    @staticmethod
    def prepare_request(request: CreateApp) -> Tuple[API, CreateApp]:
        return CREATE_APP_WORKFLOW, request

    @staticmethod
    def process_response(raw_json: Any) -> AppResponse:
        return AppResponse.parse_obj(raw_json)


class AppListAll:
    """``GET /v1/app`` — list published native app workflows."""

    @staticmethod
    def prepare_request(
        limit: Optional[int] = None, cursor: Optional[str] = None
    ) -> Tuple[API, Dict[str, Any]]:
        query_params: Dict[str, Any] = {}
        if limit is not None:
            query_params["limit"] = limit
        if cursor is not None:
            query_params["cursor"] = cursor
        return LIST_APP_WORKFLOWS, query_params

    @staticmethod
    def process_response(raw_json: Any) -> AppList:
        return AppList.parse_obj(raw_json)


class AppGet:
    """``GET /v1/app/{slug}`` — get one."""

    @staticmethod
    def prepare_request(slug: str) -> API:
        return GET_APP_WORKFLOW.format_path({"slug": slug})

    @staticmethod
    def process_response(raw_json: Any) -> AppSummary:
        return AppSummary.parse_obj(raw_json)


class AppUpdate:
    """``PUT /v1/app/{slug}`` — full-replace inputs, publish new version on same slug."""

    @staticmethod
    def prepare_request(slug: str, request: UpdateApp) -> Tuple[API, UpdateApp]:
        return UPDATE_APP_WORKFLOW.format_path({"slug": slug}), request

    @staticmethod
    def process_response(raw_json: Any) -> AppResponse:
        return AppResponse.parse_obj(raw_json)


class AppDelete:
    """``DELETE /v1/app/{slug}`` — archive/delete."""

    @staticmethod
    def prepare_request(slug: str) -> API:
        return DELETE_APP_WORKFLOW.format_path({"slug": slug})

    @staticmethod
    def process_response(raw_json: Any) -> AppDeleteResponse:
        return AppDeleteResponse.parse_obj(raw_json)


class AppSubmit:
    """``POST /v1/app/{slug}/submit`` — run the current published version."""

    @staticmethod
    def prepare_request(slug: str) -> API:
        return SUBMIT_APP_WORKFLOW.format_path({"slug": slug})

    @staticmethod
    def process_response(raw_json: Any) -> AppRunResponse:
        return AppRunResponse.parse_obj(raw_json)


class AppGetRun:
    """``GET /v1/app/runs/{run_id}`` — run status."""

    @staticmethod
    def prepare_request(run_id: str) -> API:
        return GET_APP_RUN.format_path({"run_id": run_id})

    @staticmethod
    def process_response(raw_json: Any) -> AppRunResponse:
        return AppRunResponse.parse_obj(raw_json)


class AppCancelRun:
    """``POST /v1/app/runs/{run_id}/cancel`` — cancel an in-flight run."""

    @staticmethod
    def prepare_request(run_id: str) -> API:
        return CANCEL_APP_RUN.format_path({"run_id": run_id})

    @staticmethod
    def process_response(raw_json: Any) -> AppRunCancelResponse:
        return AppRunCancelResponse.parse_obj(raw_json)


class AppAddSchedule:
    """``POST /v1/app/{slug}/schedule`` — attach a cron schedule."""

    @staticmethod
    def prepare_request(slug: str, schedule: AppSchedule) -> Tuple[API, AppSchedule]:
        return ADD_APP_SCHEDULE.format_path({"slug": slug}), schedule

    @staticmethod
    def process_response(raw_json: Any) -> AppScheduleResponse:
        return AppScheduleResponse.parse_obj(raw_json)


class AppRemoveSchedule:
    """``DELETE /v1/app/{slug}/schedule/{trigger_id}`` — remove a schedule."""

    @staticmethod
    def prepare_request(slug: str, trigger_id: str) -> API:
        return REMOVE_APP_SCHEDULE.format_path({"slug": slug, "trigger_id": trigger_id})

    @staticmethod
    def process_response(raw_json: Any) -> AppScheduleDeleteResponse:
        return AppScheduleDeleteResponse.parse_obj(raw_json)
