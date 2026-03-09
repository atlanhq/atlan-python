# type: ignore
"""
Custom HTTP transport with retry support for Atlan Python SDK.

This module provides transport classes that properly integrate retry logic
with httpx's HTTPTransport while respecting proxy and SSL configurations.
"""

import json
import logging
from functools import partial
from typing import TYPE_CHECKING, Any, Optional, Union

import httpx
from httpx_retries import Retry

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient

logger = logging.getLogger(__name__)

def _find_existing_policy(
    client: "AtlanClient", policy_name: str, persona_guid: str
) -> Optional[dict]:
    """Search for an existing AuthPolicy by name and persona GUID."""
    try:
        from pyatlan.client.constants import INDEX_SEARCH
        from pyatlan.model.search import Bool, DSL, IndexSearchRequest, Term

        query = Bool(
            filter=[
                Term(field="__typeName.keyword", value="AuthPolicy"),
                Term(field="name.keyword", value=policy_name),
                Term(field="__persona", value=persona_guid),
            ]
        )
        search_request = IndexSearchRequest(
            dsl=DSL(query=query, size=1, from_=0),
            attributes=["name", "qualifiedName"],
        )
        raw_json = client._call_api(INDEX_SEARCH, request_obj=search_request)
        if raw_json and raw_json.get("entities"):
            return raw_json["entities"][0]
        return None
    except Exception as e:
        logger.debug(f"Error searching for existing policy: {e}")
        return None


def _create_mock_response(
    existing_policy: dict, temp_guid: str = "-1"
) -> httpx.Response:
    """Build a mock bulk-entity response containing an already-created policy."""
    response_body = {
        "mutatedEntities": {"CREATE": [existing_policy]},
        "guidAssignments": {temp_guid: existing_policy.get("guid")},
    }
    return httpx.Response(
        status_code=200,
        json=response_body,
        request=httpx.Request("POST", "http://mock"),
    )


async def _find_existing_policy_async(
    client: Any, policy_name: str, persona_guid: str
) -> Optional[dict]:
    """Async version of _find_existing_policy for use with AsyncAtlanClient."""
    try:
        from pyatlan.client.constants import INDEX_SEARCH
        from pyatlan.model.search import Bool, DSL, IndexSearchRequest, Term

        query = Bool(
            filter=[
                Term(field="__typeName.keyword", value="AuthPolicy"),
                Term(field="name.keyword", value=policy_name),
                Term(field="__persona", value=persona_guid),
            ]
        )
        search_request = IndexSearchRequest(
            dsl=DSL(query=query, size=1, from_=0),
            attributes=["name", "qualifiedName"],
        )
        raw_json = await client._call_api(INDEX_SEARCH, request_obj=search_request)
        if raw_json and raw_json.get("entities"):
            return raw_json["entities"][0]
        return None
    except Exception as e:
        logger.debug(f"Error searching for existing policy (async): {e}")
        return None


async def _check_for_duplicate_policy_async(
    client: Any, request: httpx.Request
) -> Optional[httpx.Response]:
    """Async version of _check_for_duplicate_policy for use with AsyncAtlanClient."""
    try:
        if request.method != "POST" or "/api/meta/entity/bulk" not in str(request.url):
            return None
        if not request.content:
            return None

        body = json.loads(request.content.decode("utf-8"))
        for entity in body.get("entities", []):
            if entity.get("typeName") != "AuthPolicy":
                continue
            policy_name = entity.get("attributes", {}).get("name")
            access_control = entity.get("attributes", {}).get("accessControl")
            persona_guid = (
                access_control.get("guid")
                if isinstance(access_control, dict)
                else None
            )
            if not (policy_name and persona_guid):
                continue
            existing_policy = await _find_existing_policy_async(
                client, policy_name, persona_guid
            )
            if existing_policy:
                logger.info(
                    f"Found existing policy '{policy_name}' with guid "
                    f"{existing_policy.get('guid')} during retry check"
                )
                return _create_mock_response(existing_policy, entity.get("guid", "-1"))
        return None
    except Exception as e:
        logger.debug(f"Duplicate policy check failed (will proceed with retry): {e}")
        return None


def _check_for_duplicate_policy(
    client: "AtlanClient", request: httpx.Request
) -> Optional[httpx.Response]:
    """
    Check whether a bulk POST is creating an AuthPolicy that already exists.
    Only called during retry attempts, never on the first request.

    Returns a mock response with the existing policy if a duplicate is found,
    or None to let the retry proceed normally.
    """
    try:
        if request.method != "POST" or "/api/meta/entity/bulk" not in str(request.url):
            return None
        if not request.content:
            return None

        body = json.loads(request.content.decode("utf-8"))
        for entity in body.get("entities", []):
            if entity.get("typeName") != "AuthPolicy":
                continue
            policy_name = entity.get("attributes", {}).get("name")
            access_control = entity.get("attributes", {}).get("accessControl")
            persona_guid = (
                access_control.get("guid")
                if isinstance(access_control, dict)
                else None
            )
            if not (policy_name and persona_guid):
                continue
            existing_policy = _find_existing_policy(client, policy_name, persona_guid)
            if existing_policy:
                logger.info(
                    f"Found existing policy '{policy_name}' with guid "
                    f"{existing_policy.get('guid')} during retry check"
                )
                return _create_mock_response(existing_policy, entity.get("guid", "-1"))
        return None
    except Exception as e:
        logger.debug(f"Duplicate policy check failed (will proceed with retry): {e}")
        return None


class PyatlanSyncTransport(httpx.BaseTransport):
    """
    A synchronous transport that wraps httpx.HTTPTransport with retry logic.

    This transport properly handles proxy and SSL configurations by passing
    them directly to the underlying HTTPTransport, unlike the default
    RetryTransport which creates its own transport instances.

    Example:
        ```python
        transport = PyatlanSyncTransport(
            retry=Retry(total=5),
            proxy="http://proxy.example.com:8080",
            verify="/path/to/cert.pem"
        )
        client = httpx.Client(transport=transport)
        ```

    Args:
        retry: The retry configuration. Defaults to Retry() if not provided.
        **kwargs: All other arguments are passed to httpx.HTTPTransport,
                 including proxy, verify, cert, trust_env, http1, http2, limits, etc.
    """

    def __init__(
        self,
        retry: Optional[Retry] = None,
        client: Optional["AtlanClient"] = None,
        **kwargs: Any,
    ) -> None:
        self.retry = retry or Retry()
        self._client = client  # Reference to AtlanClient for duplicate checking
        # Ensure trust_env is True by default to respect environment variables
        # unless explicitly overridden
        if "trust_env" not in kwargs:
            kwargs["trust_env"] = True
        # Create the underlying HTTPTransport with all proxy/SSL config
        self._transport = httpx.HTTPTransport(**kwargs)

    def __enter__(self):
        self._transport.__enter__()
        return self

    def __exit__(self, *args):
        return self._transport.__exit__(*args)

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        """
        Sends an HTTP request, possibly with retries.

        Args:
            request: The request to send.

        Returns:
            The final response.
        """
        logger.debug("handle_request started request=%s", request)

        if self.retry.is_retryable_method(request.method):
            send_method = partial(self._transport.handle_request)
            response = self._retry_operation(request, send_method)
        else:
            response = self._transport.handle_request(request)

        logger.debug(
            "handle_request finished request=%s response=%s", request, response
        )
        return response

    def _retry_operation(
        self,
        request: httpx.Request,
        send_method: partial,
    ) -> httpx.Response:
        """Execute a request with retry logic."""
        retry = self.retry
        response: Union[httpx.Response, httpx.HTTPError, None] = None

        while True:
            if response is not None:
                logger.debug(
                    "_retry_operation retrying response=%s retry=%s", response, retry
                )

                # ONLY during retry: check if this is a policy creation and if duplicate exists
                if self._client:
                    duplicate_response = _check_for_duplicate_policy(self._client, request)
                    if duplicate_response:
                        logger.warning(
                            "RETRY PREVENTED: Policy already exists (likely from previous "
                            "request that timed out but succeeded). Returning existing policy."
                        )
                        return duplicate_response

                retry = retry.increment()
                retry.sleep(response)

            try:
                response = send_method(request)
            except httpx.HTTPError as e:
                if retry.is_exhausted() or not retry.is_retryable_exception(e):
                    raise
                response = e
                continue

            if retry.is_exhausted() or not retry.is_retryable_status_code(
                response.status_code
            ):
                return response

    def close(self) -> None:
        """Close the underlying transport."""
        self._transport.close()


class PyatlanAsyncTransport(httpx.AsyncBaseTransport):
    """
    An asynchronous transport that wraps httpx.AsyncHTTPTransport with retry logic.

    This transport properly handles proxy and SSL configurations by passing
    them directly to the underlying AsyncHTTPTransport.

    Example:
        ```python
        transport = PyatlanAsyncTransport(
            retry=Retry(total=5),
            proxy="http://proxy.example.com:8080",
            verify="/path/to/cert.pem"
        )
        async with httpx.AsyncClient(transport=transport) as client:
            response = await client.get("https://example.com")
        ```

    Args:
        retry: The retry configuration. Defaults to Retry() if not provided.
        **kwargs: All other arguments are passed to httpx.AsyncHTTPTransport,
                 including proxy, verify, cert, trust_env, http1, http2, limits, etc.
    """

    def __init__(
        self,
        retry: Optional[Retry] = None,
        client: Optional["AtlanClient"] = None,
        **kwargs: Any,
    ) -> None:
        self.retry = retry or Retry()
        self._client = client  # Reference to AtlanClient for duplicate checking
        # Ensure trust_env is True by default to respect environment variables
        # unless explicitly overridden
        if "trust_env" not in kwargs:
            kwargs["trust_env"] = True
        # Create the underlying AsyncHTTPTransport with all proxy/SSL config
        self._transport = httpx.AsyncHTTPTransport(**kwargs)

    async def __aenter__(self):
        await self._transport.__aenter__()
        return self

    async def __aexit__(self, *args):
        return await self._transport.__aexit__(*args)

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        """
        Sends an HTTP request asynchronously, possibly with retries.

        Args:
            request: The request to perform.

        Returns:
            The final response.
        """
        logger.debug("handle_async_request started request=%s", request)

        if self.retry.is_retryable_method(request.method):
            send_method = partial(self._transport.handle_async_request)
            response = await self._retry_operation_async(request, send_method)
        else:
            response = await self._transport.handle_async_request(request)

        logger.debug(
            "handle_async_request finished request=%s response=%s", request, response
        )
        return response

    async def _retry_operation_async(
        self,
        request: httpx.Request,
        send_method: partial,
    ) -> httpx.Response:
        """Execute an async request with retry logic."""
        retry = self.retry
        response: Union[httpx.Response, httpx.HTTPError, None] = None

        while True:
            if response is not None:
                logger.debug(
                    "_retry_operation_async retrying response=%s retry=%s",
                    response,
                    retry,
                )

                # ONLY during retry: check if this is a policy creation and if duplicate exists
                if self._client:
                    duplicate_response = await _check_for_duplicate_policy_async(
                        self._client, request
                    )
                    if duplicate_response:
                        logger.warning(
                            "RETRY PREVENTED: Policy already exists (likely from previous "
                            "request that timed out but succeeded). Returning existing policy."
                        )
                        return duplicate_response

                retry = retry.increment()
                await retry.asleep(response)

            try:
                response = await send_method(request)
            except httpx.HTTPError as e:
                if retry.is_exhausted() or not retry.is_retryable_exception(e):
                    raise
                response = e
                continue

            if retry.is_exhausted() or not retry.is_retryable_status_code(
                response.status_code
            ):
                return response

    async def aclose(self) -> None:
        """Close the underlying transport."""
        await self._transport.aclose()
