# type: ignore
"""
Custom HTTP transport with retry support for Atlan Python SDK.

This module provides transport classes that properly integrate retry logic
with httpx's HTTPTransport while respecting proxy and SSL configurations.
"""

import logging
from functools import partial
from typing import Any, Optional, Union

import httpx
from httpx_retries import Retry

logger = logging.getLogger(__name__)


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
        **kwargs: Any,
    ) -> None:
        self.retry = retry or Retry()
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
        **kwargs: Any,
    ) -> None:
        self.retry = retry or Retry()
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
