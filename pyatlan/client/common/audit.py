# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
import logging
from typing import List

from pydantic.v1 import ValidationError, parse_obj_as

from pyatlan.client.constants import AUDIT_SEARCH
from pyatlan.errors import ErrorCode
from pyatlan.model.audit import AuditSearchRequest, EntityAudit
from pyatlan.model.search import SortItem
from pyatlan.utils import API

ENTITY_AUDITS = "entityAudits"
LOGGER = logging.getLogger(__name__)


class AuditSearch:
    """
    Shared business logic for audit search operations.

    This class centralizes the common logic for searching audit logs
    that is used by both sync and async audit clients.
    """

    @staticmethod
    def prepare_request(
        criteria: AuditSearchRequest, bulk: bool = False
    ) -> tuple[API, AuditSearchRequest]:
        """
        Prepare the request for audit search.

        :param criteria: detailing the audit search query, parameters, and so on to run
        :param bulk: whether to run the search as bulk search
        :returns: tuple of (api_endpoint, prepared_criteria)
        """
        if bulk:
            if criteria.dsl.sort and len(criteria.dsl.sort) > 1:
                raise ErrorCode.UNABLE_TO_RUN_AUDIT_BULK_WITH_SORTS.exception_with_parameters()
            criteria.dsl.sort = AuditSearch.prepare_sorts_for_bulk_search(
                criteria.dsl.sort
            )
            LOGGER.debug(AuditSearch.get_bulk_search_log_message(bulk))

        return AUDIT_SEARCH, criteria

    @staticmethod
    def process_response(
        raw_json: dict,
    ) -> dict:
        """
        Process the raw API response into a response dictionary.

        :param raw_json: raw API response
        :returns: dictionary with parsed data for search results creation
        """
        # Parse entity audits
        entity_audits = AuditSearch.parse_entity_audits(raw_json)

        # Get total count
        count = AuditSearch.get_total_count(raw_json)

        return {
            "entity_audits": entity_audits,
            "count": count,
            "aggregations": raw_json.get("aggregations"),
        }

    @staticmethod
    def check_for_bulk_search(
        count: int,
        criteria: AuditSearchRequest,
        bulk: bool = False,
        search_results_class=None,
    ) -> bool:
        """
        Check if the search should be converted to bulk search based on result count.

        :param count: total number of results
        :param criteria: the audit search criteria
        :param bulk: whether bulk search is already enabled
        :param search_results_class: the search results class to use for thresholds
        :returns: True if conversion to bulk search is needed
        """
        # Use provided search results class or default to sync version
        if search_results_class is None:
            # Import here to avoid circular import
            from pyatlan.model.audit import AuditSearchResults

            search_results_class = AuditSearchResults

        if bulk:
            return False

        if (
            count > search_results_class._MASS_EXTRACT_THRESHOLD
            and not search_results_class.presorted_by_timestamp(criteria.dsl.sort)
        ):
            if criteria.dsl.sort and len(criteria.dsl.sort) > 1:
                raise ErrorCode.UNABLE_TO_RUN_AUDIT_BULK_WITH_SORTS.exception_with_parameters()
            # Update criteria for bulk search
            criteria.dsl.sort = AuditSearch.prepare_sorts_for_bulk_search(
                criteria.dsl.sort
            )
            LOGGER.debug(
                AuditSearch.get_bulk_search_log_message(False),
                count,
                search_results_class._MASS_EXTRACT_THRESHOLD,
            )
            return True
        return False

    @staticmethod
    def prepare_sorts_for_bulk_search(
        sorts: List[SortItem], search_results_class=None
    ) -> List[SortItem]:
        """
        Ensures that sorting by creation timestamp is prioritized for Audit bulk searches.

        :param sorts: List of existing sorting options
        :param search_results_class: the search results class to use for sorting logic
        :returns: A modified list of sorting options with creation timestamp as the top priority
        """
        # Use provided search results class or default to sync version
        if search_results_class is None:
            # Import here to avoid circular import
            from pyatlan.model.audit import AuditSearchResults

            search_results_class = AuditSearchResults

        if not search_results_class.presorted_by_timestamp(sorts):
            return search_results_class.sort_by_timestamp_first(sorts)
        return sorts

    @staticmethod
    def get_bulk_search_log_message(bulk: bool) -> str:
        """
        Get the appropriate log message for bulk search operations.

        :param bulk: whether bulk search is enabled
        :returns: appropriate log message
        """
        return (
            (
                "Audit bulk search option is enabled. "
                if bulk
                else "Result size (%s) exceeds threshold (%s). "
            )
            + "Ignoring requests for offset-based paging and using timestamp-based paging instead."
        )

    @staticmethod
    def parse_entity_audits(raw_json: dict) -> List[EntityAudit]:
        """
        Parse entity audits from raw JSON response.

        :param raw_json: the raw JSON response from audit search API
        :returns: list of parsed EntityAudit objects
        :raises JSON_ERROR: if parsing fails
        """
        if ENTITY_AUDITS in raw_json:
            try:
                return parse_obj_as(List[EntityAudit], raw_json[ENTITY_AUDITS])
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        return []

    @staticmethod
    def get_total_count(raw_json: dict) -> int:
        """
        Extract total count from audit search response.

        :param raw_json: the raw JSON response from audit search API
        :returns: total count of audit entries
        """
        return raw_json.get("totalCount", 0)
