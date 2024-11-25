import time
from typing import List

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from pyatlan.client.atlan import AtlanClient
from pyatlan.errors import AtlanError, ErrorCode, NotFoundError
from pyatlan.model.assets import Asset
from pyatlan.model.enums import EntityStatus
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.typedef import AtlanTagDef, CustomMetadataDef, EnumDef


def block(
    client: AtlanClient, response: AssetMutationResponse
) -> AssetMutationResponse:
    if response.mutated_entities and response.mutated_entities.DELETE:
        retrieve_and_check_assets(client, response.mutated_entities.DELETE, 0)
    return response


def retrieve_and_check_assets(
    client: AtlanClient, to_check: List[Asset], retry_count: int
):
    """
    Retrieve and check the status of a list of assets and retry if needed.
    """
    leftovers = []
    for one in to_check:
        try:
            candidate = client.asset.get_by_guid(one.guid, asset_type=type(one))
            if candidate and candidate.status == EntityStatus.ACTIVE:
                leftovers.append(candidate)
        except NotFoundError:
            # If it is not found, it was successfully deleted (purged), so we
            # do not need to look for it any further
            print("Asset no longer exists.")
        except AtlanError:
            leftovers.append(one)
    if leftovers:
        if retry_count == 20:
            raise ErrorCode.RETRY_OVERRUN.exception_with_parameters()
        time.sleep(2)
        retrieve_and_check_assets(client, leftovers, retry_count + 1)


@retry(
    retry=retry_if_exception_type(AtlanError),
    wait=wait_random_exponential(multiplier=1, max=5),
    stop=stop_after_attempt(3),
)
def wait_for_successful_tagdef_purge(name: str, client: AtlanClient):
    client.typedef.purge(name, typedef_type=AtlanTagDef)


@retry(
    retry=retry_if_exception_type(AtlanError),
    wait=wait_random_exponential(multiplier=1, max=5),
    stop=stop_after_attempt(3),
)
def wait_for_successful_custometadatadef_purge(name: str, client: AtlanClient):
    client.typedef.purge(name, typedef_type=CustomMetadataDef)


@retry(
    retry=retry_if_exception_type(AtlanError),
    wait=wait_random_exponential(multiplier=1, max=5),
    stop=stop_after_attempt(3),
)
def wait_for_successful_enumadef_purge(name: str, client: AtlanClient):
    client.typedef.purge(name, typedef_type=EnumDef)
