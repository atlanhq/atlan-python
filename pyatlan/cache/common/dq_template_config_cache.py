# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Shared logic for dq template config cache operations.
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple

from pyatlan.model.assets import Asset
from pyatlan.model.assets.core.alpha__d_q_rule_template import alpha_DQRuleTemplate
from pyatlan.model.fluent_search import FluentSearch


class DQTemplateConfigCacheCommon:
    """
    Common logic for DQ rule template configuration cache operations.
    Provides shared functionality between sync and async implementations.
    """

    @classmethod
    def prepare_search_request(cls) -> FluentSearch:
        """
        Prepare the search request for fetching DQ rule template configurations.

        :returns: FluentSearch configured for DQ rule templates
        """
        try:
            return (
                FluentSearch()
                .where(Asset.TYPE_NAME.eq(alpha_DQRuleTemplate.__name__))
                .include_on_results(alpha_DQRuleTemplate.NAME)
                .include_on_results(alpha_DQRuleTemplate.QUALIFIED_NAME)
                .include_on_results(alpha_DQRuleTemplate.DISPLAY_NAME)
                .include_on_results(
                    alpha_DQRuleTemplate.ALPHADQ_RULE_TEMPLATE_DIMENSION
                )
                .include_on_results(alpha_DQRuleTemplate.ALPHADQ_RULE_TEMPLATE_CONFIG)
            )
        except ImportError:
            # If the alpha_DQRuleTemplate is not available, return empty search
            return FluentSearch()

    @classmethod
    def process_search_results(
        cls, search_results, cache: Dict[str, Dict]
    ) -> Tuple[bool, Optional[Exception]]:
        """
        Process search results and populate the cache.

        :param search_results: Iterator of search results
        :param cache: Cache dictionary to populate
        :returns: Tuple of (success, exception if any)
        """
        try:
            for result in search_results:
                template_config = {
                    "name": result.name,
                    "qualified_name": result.qualified_name,
                    "display_name": result.display_name,
                    "dimension": result.alpha_dq_rule_template_dimension,  # type: ignore
                    "config": result.alpha_dq_rule_template_config,  # type: ignore
                }
                cache[result.display_name] = template_config  # type: ignore
            return True, None
        except Exception as e:
            return False, e
