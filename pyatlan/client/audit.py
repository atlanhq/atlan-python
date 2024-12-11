# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import List

from pydantic.v1 import ValidationError, parse_obj_as, validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import AUDIT_SEARCH
from pyatlan.errors import ErrorCode
from pyatlan.model.audit import AuditSearchRequest, AuditSearchResults, EntityAudit
from pyatlan.model.search import SortItem
import logging

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
    def _prepare_sorts_for_bulk_search(sorts: List[SortItem]) -> List[SortItem]:
        """
        Ensures that sorting by creation timestamp is prioritized for bulk searches.
        :param sorts: List of existing sorting options.
        :returns: A modified list of sorting options with creation timestamp as the top priority.
        """
        if not AuditSearchResults.presorted_by_timestamp(sorts):
            return AuditSearchResults.sort_by_timestamp_first(sorts)
        return sorts

    def _get_bulk_search_log_message(self, bulk):
        return (
            (
                "Bulk search option is enabled. "
                if bulk
                else "Result size (%s) exceeds threshold (%s). "
            )
            + "Ignoring requests for offset-based paging and using timestamp-based paging instead."
        )

    @validate_arguments
    def search(self, criteria: AuditSearchRequest, bulk=False) -> AuditSearchResults:
        """
        Search for assets using the provided criteria.

        :param criteria: detailing the search query, parameters, and so on to run
        :param bulk: whether to enable timestamp-based pagination for large datasets.
        :returns: the results of the search
        :raises AtlanError: on any API communication issue
        """
        if bulk:
            print(self._get_bulk_search_log_message(bulk))
            if criteria.dsl.sort and len(criteria.dsl.sort) > 1:
                raise ErrorCode.UNABLE_TO_RUN_BULK_WITH_SORTS.exception_with_parameters()
            criteria.dsl.sort = self._prepare_sorts_for_bulk_search(criteria.dsl.sort)
            LOGGER.debug(self._get_bulk_search_log_message(bulk))

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

        count = raw_json.get("totalCount", 0)
        if (
            count > AuditSearchResults._MASS_EXTRACT_THRESHOLD
            and not AuditSearchResults.presorted_by_timestamp(criteria.dsl.sort)
        ):
            if criteria.dsl.sort and len(criteria.dsl.sort) > 1:
                raise ErrorCode.UNABLE_TO_RUN_BULK_WITH_SORTS.exception_with_parameters()
            criteria.dsl.sort = self._prepare_sorts_for_bulk_search(criteria.dsl.sort)
            LOGGER.debug(
                self._get_bulk_search_log_message(bulk),
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
            aggregations=None,
        )
