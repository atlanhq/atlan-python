# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Dict, Optional

from pyatlan.model.assets import Asset
from pyatlan.model.fluent_search import FluentSearch

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient


class DQTemplateConfigCache:
    """
    Lazily-loaded cache for DQ rule template configurations to avoid multiple API calls.
    """

    def __init__(self, client: AtlanClient):
        self.client: AtlanClient = client
        self._cache: Dict[str, Dict] = {}
        self._lock: threading.Lock = threading.Lock()
        self._initialized: bool = False

    def get_template_config(self, rule_type: str) -> Optional[Dict]:
        """
        Get template configuration for a specific rule type.

        :param rule_type: The display name of the rule type
        :returns: Template configuration dict or None if not found
        """
        if not self._initialized:
            self._refresh_cache()

        return self._cache.get(rule_type)

    def _refresh_cache(self) -> None:
        """Refresh the cache by fetching all template configurations."""
        with self._lock:
            if self._initialized:
                return

            try:
                from pyatlan.model.assets.core.alpha__d_q_rule_template import (
                    alpha_DQRuleTemplate,
                )

                request = (
                    FluentSearch()
                    .where(Asset.TYPE_NAME.eq(alpha_DQRuleTemplate.__name__))
                    .include_on_results(alpha_DQRuleTemplate.NAME)
                    .include_on_results(alpha_DQRuleTemplate.QUALIFIED_NAME)
                    .include_on_results(alpha_DQRuleTemplate.DISPLAY_NAME)
                    .include_on_results(
                        alpha_DQRuleTemplate.ALPHADQ_RULE_TEMPLATE_DIMENSION
                    )
                    .include_on_results(
                        alpha_DQRuleTemplate.ALPHADQ_RULE_TEMPLATE_CONFIG
                    )
                ).to_request()

                results = self.client.asset.search(request)
                for result in results:
                    template_config = {
                        "name": result.name,
                        "qualified_name": result.qualified_name,
                        "display_name": result.display_name,
                        "dimension": result.alpha_dq_rule_template_dimension,  # type: ignore
                        "config": result.alpha_dq_rule_template_config,  # type: ignore
                    }
                    self._cache[result.display_name] = template_config  # type: ignore

                self._initialized = True
            except Exception:
                # If cache refresh fails, mark as initialized to prevent infinite retries
                self._initialized = True
                raise
