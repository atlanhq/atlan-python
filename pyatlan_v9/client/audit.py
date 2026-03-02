# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import List

import msgspec

from pyatlan.client.common import ApiCaller, AuditSearch
from pyatlan.errors import ErrorCode
from pyatlan.validate import validate_arguments
from pyatlan_v9.model.audit import (
    AuditSearchRequest,
    AuditSearchResults,
    EntityAudit,
)

ENTITY_AUDITS = "entityAudits"
_MS_TIMESTAMP_THRESHOLD = 1e12
_AUDIT_TS_FIELDS = ("timestamp", "created")


def _normalize_ms_timestamps(record: dict, fields: tuple) -> dict:
    """Return a shallow copy with millisecond epoch timestamps converted to seconds."""
    out = dict(record)
    for field in fields:
        val = out.get(field)
        if isinstance(val, (int, float)) and val > _MS_TIMESTAMP_THRESHOLD:
            out[field] = val / 1000
    return out


def _parse_entity_audits(raw_json: dict) -> List[EntityAudit]:
    """Parse entity audits from raw JSON response using msgspec."""
    if ENTITY_AUDITS in raw_json and raw_json[ENTITY_AUDITS]:
        audits = [
            _normalize_ms_timestamps(a, _AUDIT_TS_FIELDS)
            for a in raw_json[ENTITY_AUDITS]
        ]
        return msgspec.convert(audits, list[EntityAudit], strict=False)
    return []


class V9AuditClient:
    """
    This class can be used to configure and run a search against Atlan's activity log.
    This class does not need to be instantiated directly but can be obtained
    through the audit property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def search(self, criteria: AuditSearchRequest, bulk=False) -> AuditSearchResults:
        """
        Search for assets using the provided criteria.
        `Note:` if the number of results exceeds the predefined threshold
        (10,000 assets) this will be automatically converted into an audit `bulk` search.

        :param criteria: detailing the search query, parameters, and so on to run
        :param bulk: whether to run the search to retrieve assets that match the supplied criteria,
        for large numbers of results (> `10,000`), defaults to `False`. Note: this will reorder the results
        (based on creation timestamp) in order to iterate through a large number (more than `10,000`) results.
        :raises InvalidRequestError:

            - if audit bulk search is enabled (`bulk=True`) and any
              user-specified sorting options are found in the search request.
            - if audit bulk search is disabled (`bulk=False`) and the number of results
              exceeds the predefined threshold (i.e: `10,000` assets)
              and any user-specified sorting options are found in the search request.

        :raises AtlanError: on any API communication issue
        :returns: the results of the search
        """
        endpoint, request_obj = AuditSearch.prepare_request(criteria, bulk)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)

        entity_audits = _parse_entity_audits(raw_json)
        count = raw_json.get("totalCount", 0)
        aggregations = raw_json.get("aggregations")

        if AuditSearch.check_for_bulk_search(
            count, criteria, bulk, AuditSearchResults
        ):
            return self.search(criteria)

        return AuditSearchResults(
            client=self._client,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            entity_audits=entity_audits,
            count=count,
            bulk=bulk,
            aggregations=aggregations,
        )
