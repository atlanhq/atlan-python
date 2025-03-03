# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import logging
from typing import List

from pydantic.v1 import ValidationError, parse_obj_as, validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import AUDIT_SEARCH
from pyatlan.errors import ErrorCode
from pyatlan.model.audit import AuditSearchRequest, AuditSearchResults, EntityAudit
from pyatlan.model.search import SortItem

ENTITY_AUDITS = "entityAudits"
LOGGER = logging.getLogger(__name__)


class AuditClient:
    """
    This class can be used to configure and run a search against Atlan's activity log. This class does not need to be
    instantiated directly but can be obtained through the audit property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @staticmethod
    def _prepare_sorts_for_audit_bulk_search(sorts: List[SortItem]) -> List[SortItem]:
        """
        Ensures that sorting by creation timestamp is prioritized for Audit bulk searches.
        :param sorts: List of existing sorting options.
        :returns: A modified list of sorting options with creation timestamp as the top priority.
        """
        if not AuditSearchResults.presorted_by_timestamp(sorts):
            return AuditSearchResults.sort_by_timestamp_first(sorts)
        return sorts

    def _get_audit_bulk_search_log_message(self, bulk):
        return (
            (
                "Audit bulk search option is enabled. "
                if bulk
                else "Result size (%s) exceeds threshold (%s). "
            )
            + "Ignoring requests for offset-based paging and using timestamp-based paging instead."
        )

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
        if bulk:
            if criteria.dsl.sort and len(criteria.dsl.sort) > 1:
                raise ErrorCode.UNABLE_TO_RUN_AUDIT_BULK_WITH_SORTS.exception_with_parameters()
            criteria.dsl.sort = self._prepare_sorts_for_audit_bulk_search(
                criteria.dsl.sort
            )
            LOGGER.debug(self._get_audit_bulk_search_log_message(bulk))

        raw_json = self._client._call_api(
            AUDIT_SEARCH,
            request_obj=criteria,
        )
        if ENTITY_AUDITS in raw_json:
            try:
                entity_audits = parse_obj_as(List[EntityAudit], raw_json[ENTITY_AUDITS])
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            entity_audits = []

        count = raw_json["totalCount"] if "totalCount" in raw_json else 0

        if (
            count > AuditSearchResults._MASS_EXTRACT_THRESHOLD
            and not AuditSearchResults.presorted_by_timestamp(criteria.dsl.sort)
        ):
            # If there is any user-specified sorting present in the search request
            if criteria.dsl.sort and len(criteria.dsl.sort) > 1:
                raise ErrorCode.UNABLE_TO_RUN_AUDIT_BULK_WITH_SORTS.exception_with_parameters()
            # Re-fetch the first page results with updated timestamp sorting
            # for bulk search if count > _MASS_EXTRACT_THRESHOLD (10,000 assets)
            criteria.dsl.sort = self._prepare_sorts_for_audit_bulk_search(
                criteria.dsl.sort
            )
            LOGGER.debug(
                self._get_audit_bulk_search_log_message(bulk),
                count,
                AuditSearchResults._MASS_EXTRACT_THRESHOLD,
            )
            return self.search(criteria)
        return AuditSearchResults(
            client=self._client,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            count=count,
            entity_audits=entity_audits,
            bulk=bulk,
            aggregations=raw_json.get("aggregations"),
        )
