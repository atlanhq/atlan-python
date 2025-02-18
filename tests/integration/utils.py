from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from pyatlan.client.atlan import AtlanClient
from pyatlan.errors import AtlanError
from pyatlan.model.typedef import AtlanTagDef, CustomMetadataDef, EnumDef


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
