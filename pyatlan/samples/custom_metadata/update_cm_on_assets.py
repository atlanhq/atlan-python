# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import logging
from typing import List, Optional

from pyatlan.cache.custom_metadata_cache import CustomMetadataCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Asset
from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fluent_search import FluentSearch

CUSTOM_METADATA_NAME = "Quality Data"
client = AtlanClient()
logger = logging.getLogger(__name__)


def find_asset(
    connector_type: AtlanConnectorType,
    connection_name: str,
    asset_name: str,
    attributes: Optional[List[str]] = None,
) -> Optional[Asset]:
    """
    Given a connector type and otherwise-qualified name (not including the
    connection portion of the qualified_name), finds and returns the asset in
    question.

    :param connector_type: the type of connector in which the asset can be found
    :param connection_name: the simple name of the connection
    :param asset_name: the qualified_name of the asset, not including the
        connection portion
    :param attributes: a list of attributes to retrieve for the asset
    :returns: the asset, if found
    """

    connections = client.asset.find_connections_by_name(
        name=connection_name, connector_type=connector_type
    )
    qualified_names = [
        f"{connection.qualified_name}/{asset_name}" for connection in connections
    ]
    search_request = (
        FluentSearch(_includes_on_results=attributes).where(
            Asset.QUALIFIED_NAME.within(qualified_names)
        )
    ).to_request()
    if results := client.asset.search(search_request):
        return results.current_page()[0]
    return None


def update_custom_metadata(
    asset: Asset,
    rating: str,
    passed: int = 0,
    failed: int = 0,
    reports: Optional[List[str]] = None,
) -> Optional[Asset]:
    """
    Update the custom metadata on the provided asset.

    :param asset: the asset on which to update the custom metadata
    :param rating: the overall quality rating to give the asset
    :param passed: numer of checks that passed
    :param failed: number of checks that failed
    :param reports: URLs to detailed quality reports
    :returns: the result of the update
    """

    cma = asset.get_custom_metadata(client=client, name=CUSTOM_METADATA_NAME)
    cma["Rating"] = rating
    cma["Passed count"] = passed
    cma["Failed count"] = failed
    cma["Detailed reports"] = reports
    to_update = asset.trim_to_required()
    to_update.set_custom_metadata(custom_metadata=cma, client=client)
    result = client.asset.save_merging_cm(to_update)
    updates = result.assets_updated(asset_type=type(asset))
    return updates[0] if updates else None


def main():
    if asset := find_asset(
        connector_type=AtlanConnectorType.SNOWFLAKE,
        connection_name="development",
        asset_name="RAW/WIDEWORLDIMPORTERS_PURCHASING/SUPPLIERS",
        attributes=CustomMetadataCache.get_attributes_for_search_results(
            CUSTOM_METADATA_NAME
        ),
    ):
        logger.info("Found asset: %s", asset)
        updated = update_custom_metadata(
            asset=asset,
            rating="OK",
            passed=10,
            failed=5,
            reports=["https://www.example.com", "https://www.atlan.com"],
        )
        # Note that the updated asset will NOT show the custom metadata, if you want
        # to see the custom metadata you need to re-retrieve the asset itself
        assert updated  # noqa: S101
        result = client.asset.get_by_guid(
            guid=updated.guid, asset_type=type(updated), ignore_relationships=True
        )
        logger.info("Asset's custom metadata was updated: %s", result)
    else:
        logger.warning(
            "Unable to find asset: (development)/RAW/WIDEWORLDIMPORTERS_PURCHASING/SUPPLIERS"
        )


if __name__ == "__main__":
    main()
