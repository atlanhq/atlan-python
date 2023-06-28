# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
# Based on original code from https://github.com/stripe/stripe-python (under MIT license)
from __future__ import absolute_import, division, print_function

import json
import random
import textwrap
import threading
import time

import requests

import pyatlan
from pyatlan import error, utils
from pyatlan.request_metrics import RequestMetrics


def _now_ms():
    return int(round(time.time() * 1000))


def new_default_http_client(*args, **kwargs):
    impl = RequestsClient
    return impl(*args, **kwargs)


class HTTPClient(object):
    MAX_DELAY = 5
    INITIAL_DELAY = 0.5
    MAX_RETRY_AFTER = 60

    def __init__(self, verify_ssl_certs=True):
        self._verify_ssl_certs = verify_ssl_certs
        self._thread_local = threading.local()

    def request_with_retries(self, method, url, headers, post_data=None):
        return self._request_with_retries_internal(
            method, url, headers, post_data, is_streaming=False
        )

    def request_stream_with_retries(self, method, url, headers, post_data=None):
        return self._request_with_retries_internal(
            method, url, headers, post_data, is_streaming=True
        )

    def _request_with_retries_internal(
        self, method, url, headers, post_data, is_streaming
    ):
        self._add_telemetry_header(headers)

        num_retries = 0

        while True:
            request_start = _now_ms()

            try:
                if is_streaming:
                    response = self.request_stream(method, url, headers, post_data)
                else:
                    response = self.request(method, url, headers, post_data)
                connection_error = None
            except error.APIConnectionError as e:
                connection_error = e
                response = None

            if self._should_retry(response, connection_error, num_retries):
                if connection_error:
                    utils.log_info(
                        "Encountered a retryable error %s"
                        % connection_error.user_message
                    )
                num_retries += 1
                sleep_time = self._sleep_time_seconds(num_retries, response)
                utils.log_info(
                    (
                        "Initiating retry %i for request %s %s after "
                        "sleeping %.2f seconds."
                        % (num_retries, method, url, sleep_time)
                    )
                )
                time.sleep(sleep_time)
            else:
                if response is not None:
                    self._record_request_metrics(response, request_start)

                    return response
                else:
                    raise connection_error

    def request(self, method, url, headers, post_data=None):
        raise NotImplementedError("HTTPClient subclasses must implement `request`")

    def request_stream(self, method, url, headers, post_data=None):
        raise NotImplementedError(
            "HTTPClient subclasses must implement `request_stream`"
        )

    def _should_retry(self, response, api_connection_error, num_retries):
        if num_retries >= self._max_network_retries():
            return False

        if response is None:
            # We generally want to retry on timeout and connection
            # exceptions, but defer this decision to underlying subclass
            # implementations. They should evaluate the driver-specific
            # errors worthy of retries, and set flag on the error returned.
            return api_connection_error.should_retry

        _, status_code, rheaders = response

        # Retry on conflict errors.
        if status_code == 409:
            return True

        # Retry on 500, 503, and other internal errors.
        if status_code >= 500:
            return True

        return False

    def _max_network_retries(self):
        from pyatlan import max_network_retries

        # Configured retries, isolated here for tests
        return max_network_retries

    def _retry_after_header(self, response=None):
        if response is None:
            return None
        _, _, rheaders = response

        try:
            return int(rheaders["retry-after"])
        except (KeyError, ValueError):
            return None

    def _sleep_time_seconds(self, num_retries, response=None):
        # Apply exponential backoff with initial_network_retry_delay on the
        # number of num_retries so far as inputs.
        # Do not allow the number to exceed max_network_retry_delay.
        sleep_seconds = min(
            HTTPClient.INITIAL_DELAY * (2 ** (num_retries - 1)),
            HTTPClient.MAX_DELAY,
        )

        sleep_seconds = self._add_jitter_time(sleep_seconds)

        # But never sleep less than the base sleep seconds.
        sleep_seconds = max(HTTPClient.INITIAL_DELAY, sleep_seconds)

        # And never sleep less than the time the API asks us to wait, assuming it's a reasonable ask.
        retry_after = self._retry_after_header(response) or 0
        if retry_after <= HTTPClient.MAX_RETRY_AFTER:
            sleep_seconds = max(retry_after, sleep_seconds)

        return sleep_seconds

    def _add_jitter_time(self, sleep_seconds):
        # Randomize the value in [(sleep_seconds/ 2) to (sleep_seconds)]
        # Also separated method here to isolate randomness for tests
        sleep_seconds *= 0.5 * (1 + random.uniform(0, 1))  # noqa: S311
        return sleep_seconds

    def _add_telemetry_header(self, headers):
        last_request_metrics = getattr(self._thread_local, "last_request_metrics", None)
        if pyatlan.enable_telemetry and last_request_metrics:
            telemetry = {"last_request_metrics": last_request_metrics.payload()}
            headers["X-Atlan-Client-Telemetry"] = json.dumps(telemetry)

    def _record_request_metrics(self, response, request_start):
        _, _, rheaders = response
        if "Request-Id" in rheaders and pyatlan.enable_telemetry:
            request_id = rheaders["Request-Id"]
            request_duration_ms = _now_ms() - request_start
            self._thread_local.last_request_metrics = RequestMetrics(
                request_id, request_duration_ms
            )

    def close(self):
        raise NotImplementedError("HTTPClient subclasses must implement `close`")


class RequestsClient(HTTPClient):
    name = "requests"

    def __init__(self, timeout=80, session=None, **kwargs):
        super(RequestsClient, self).__init__(**kwargs)
        self._session = session
        self._timeout = timeout

    def request(self, method, url, headers, post_data=None):
        return self._request_internal(
            method, url, headers, post_data, is_streaming=False
        )

    def request_stream(self, method, url, headers, post_data=None):
        return self._request_internal(
            method, url, headers, post_data, is_streaming=True
        )

    def _request_internal(self, method, url, headers, post_data, is_streaming):
        kwargs = {}
        if self._verify_ssl_certs:
            kwargs["verify"] = pyatlan.ca_bundle_path
        else:
            kwargs["verify"] = False

        if is_streaming:
            kwargs["stream"] = True

        if getattr(self._thread_local, "session", None) is None:
            self._thread_local.session = self._session or requests.Session()

        try:
            try:
                result = self._thread_local.session.request(
                    method,
                    url,
                    headers=headers,
                    data=post_data,
                    timeout=self._timeout,
                    **kwargs
                )
            except TypeError as e:
                raise TypeError(
                    "Warning: It looks like your installed version of the "
                    '"requests" library is not compatible with Atlan\'s '
                    "usage thereof. (HINT: The most likely cause is that "
                    'your "requests" library is out of date. You can fix '
                    'that by running "pip install -U requests".) The '
                    "underlying error was: %s" % (e,)
                )

            if is_streaming:
                content = result.raw
            else:
                # This causes the content to actually be read, which could cause
                # e.g. a socket timeout. TODO: The other fetch methods probably
                # are susceptible to the same and should be updated.
                content = result.content

            status_code = result.status_code
        except Exception as e:
            # Would catch just requests.exceptions.RequestException, but can
            # also raise ValueError, RuntimeError, etc.
            self._handle_request_error(e)
        return content, status_code, result.headers

    def _handle_request_error(self, e):

        # Catch SSL error first as it belongs to ConnectionError,
        # but we don't want to retry
        if isinstance(e, requests.exceptions.SSLError):
            msg = (
                "Could not verify Atlan's SSL certificate.  Please make "
                "sure that your network is not intercepting certificates.  "
                "If this problem persists, let us know at "
                "support@atlan.com."
            )
            err = "%s: %s" % (type(e).__name__, str(e))
            should_retry = False
        # Retry only timeout and connect errors; similar to urllib3 Retry
        elif isinstance(
            e,
            (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        ):
            msg = (
                "Unexpected error communicating with Atlan.  "
                "If this problem persists, let us know at "
                "support@atlan.com."
            )
            err = "%s: %s" % (type(e).__name__, str(e))
            should_retry = True
        # Catch remaining request exceptions
        elif isinstance(e, requests.exceptions.RequestException):
            msg = (
                "Unexpected error communicating with Atlan.  "
                "If this problem persists, let us know at "
                "support@atlan.com."
            )
            err = "%s: %s" % (type(e).__name__, str(e))
            should_retry = False
        else:
            msg = (
                "Unexpected error communicating with Atlan. "
                "It looks like there's probably a configuration "
                "issue locally.  If this problem persists, let us "
                "know at support@atlan.com."
            )
            err = "A %s was raised" % (type(e).__name__,)
            if str(e):
                err += " with error message %s" % (str(e),)
            else:
                err += " with no error message"
            should_retry = False

        msg = textwrap.fill(msg) + "\n\n(Network error: %s)" % (err,)
        raise error.APIConnectionError(msg, should_retry=should_retry)

    def close(self):
        if getattr(self._thread_local, "session", None) is not None:
            self._thread_local.session.close()
