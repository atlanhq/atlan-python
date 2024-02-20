# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import List

from pydantic.v1 import ValidationError, parse_obj_as, validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import AUDIT_SEARCH
from pyatlan.errors import ErrorCode
from pyatlan.model.audit import AuditSearchRequest, AuditSearchResults, EntityAudit

ENTITY_AUDITS = "entityAudits"


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

    @validate_arguments
    def search(self, criteria: AuditSearchRequest) -> AuditSearchResults:
        """
        Search for assets using the provided criteria.

        :param criteria: detailing the search query, parameters, and so on to run
        :returns: the results of the search
        :raises AtlanError: on any API communication issue
        """
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
        return AuditSearchResults(
            client=self._client,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            count=count,
            entity_audits=entity_audits,
            aggregations=None,
        )
