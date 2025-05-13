# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import logging
from datetime import datetime
from typing import List, Set

from pyatlan.client.asset import IndexSearchResults
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Asset, AtlasGlossaryTerm
from pyatlan.model.fluent_search import FluentSearch
from pyatlan.model.structs import StarredDetails

client = AtlanClient()
logger = logging.getLogger(__name__)


def find_assets() -> IndexSearchResults:
    """
    In this method you would code the logic for determining which assets
    you want to star. (This example will star all glossary terms in the
    "Metrics" glossary.)

    :returns: results of the search
    """
    glossary = client.asset.find_glossary_by_name("Metrics")
    search_request = (
        FluentSearch()
        .where(FluentSearch.active_assets())
        .where(FluentSearch.asset_type(AtlasGlossaryTerm))
        .where(AtlasGlossaryTerm.ANCHOR.eq(glossary.qualified_name or ""))
        .page_size(100)
        .include_on_results(Asset.STARRED_DETAILS_LIST)
        .include_on_results(Asset.STARRED_BY)
        .include_on_results(AtlasGlossaryTerm.ANCHOR)
    ).to_request()
    return client.asset.search(search_request)


def list_users_in_group(name: str) -> List[str]:
    """
    Given the name of a group in Atlan, return a list of all the usernames
    of users in that group.

    :param name: human-readable name of the group in Atlan
    :returns: list of all the usernames of users in that group in Atlan
    """
    usernames: List[str] = []
    if groups := client.group.get_by_name(alias=name):
        if groups.records[0].id is not None and (  # type: ignore
            response := client.group.get_members(guid=groups.records[0].id)  # type: ignore
        ):
            if response.records and len(response.records) > 0:
                usernames.extend(
                    str(user.username)
                    for user in response.records
                    if user.username is not None
                )
    return usernames


def star_asset(asset: Asset, usernames: List[str]) -> None:
    """
    Given an asset and a list of usernames, ensure all the users listed
    have starred the asset.

    :param asset: to be starred
    :param usernames: to ensure have starred the asset
    :return: nothing (void)
    """
    starred_details_list: List[StarredDetails] = asset.starred_details_list or []
    starred_count = len(starred_details_list)
    starred_by: Set[str] = asset.starred_by or set()
    for user in usernames:
        if user not in starred_by:
            starred_by.add(user)
            starred_count += 1
            starred_details_list.append(
                StarredDetails(asset_starred_by=user, asset_starred_at=datetime.now())
            )
    to_update = asset.trim_to_required()
    to_update.starred_details_list = starred_details_list
    to_update.starred_count = starred_count
    to_update.starred_by = starred_by
    logger.info(
        "Updating '%s' (%s) with total stars: %s", asset.name, asset.guid, starred_count
    )
    client.asset.save(to_update)


def main():
    assets = find_assets()
    usernames = list_users_in_group("Admins")
    for asset in assets:
        if isinstance(asset, AtlasGlossaryTerm):
            star_asset(asset, usernames)


if __name__ == "__main__":
    main()
