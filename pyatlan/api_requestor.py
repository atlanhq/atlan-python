# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
# Based on original code from https://github.com/stripe/stripe-python (under MIT license)
from __future__ import absolute_import, division, print_function

import calendar
import datetime
import json
import platform
import time
import uuid
from collections import OrderedDict
from urllib.parse import urlencode, urlsplit, urlunsplit

import pyatlan
from pyatlan import error, http_client, utils, version
from pyatlan.atlan_response import AtlanResponse, AtlanStreamResponse
from pyatlan.multipart_data_generator import MultipartDataGenerator


def _encode_datetime(dttime):
    if dttime.tzinfo and dttime.tzinfo.utcoffset(dttime) is not None:
        utc_timestamp = calendar.timegm(dttime.utctimetuple())
    else:
        utc_timestamp = time.mktime(dttime.timetuple())

    return int(utc_timestamp)


def _encode_nested_dict(key, data, fmt="%s[%s]"):
    d = OrderedDict()
    for subkey, subvalue in data:
        d[fmt % (key, subkey)] = subvalue
    return d


def _api_encode(data):
    for key, value in data:
        if value is None:
            continue
        elif isinstance(value, list) or isinstance(value, tuple):
            for i, sv in enumerate(value):
                if isinstance(sv, dict):
                    subdict = _encode_nested_dict("%s[%d]" % (key, i), sv)
                    for k, v in _api_encode(subdict):
                        yield (k, v)
                else:
                    yield "%s[%d]" % (key, i), sv
        elif isinstance(value, dict):
            subdict = _encode_nested_dict(key, value)
            for subkey, subvalue in _api_encode(subdict):
                yield subkey, subvalue
        elif isinstance(value, datetime.datetime):
            yield key, _encode_datetime(value)
        else:
            yield key, value


def _build_api_url(url, query):
    scheme, netloc, path, base_query, fragment = urlsplit(url)

    if base_query:
        query = "%s&%s" % (base_query, query)

    return urlunsplit((scheme, netloc, path, query, fragment))


class APIRequestor(object):
    def __init__(
        self,
        key=None,
        client=None,
        api_base=None,
    ):
        self.api_base = api_base or pyatlan.api_base
        self.api_key = key

        self._default_proxy = None

        from pyatlan import verify_ssl_certs as verify

        if client:
            self._client = client
        elif pyatlan.default_http_client:
            self._client = pyatlan.default_http_client
        else:
            # If the pyatlan.default_http_client has not been set by the user
            # yet, we'll set it here. This way, we aren't creating a new
            # HttpClient for every request.
            pyatlan.default_http_client = http_client.new_default_http_client(
                verify_ssl_certs=verify
            )
            self._client = pyatlan.default_http_client

    @classmethod
    def format_app_info(cls, info):
        str = info["name"]
        if info["version"]:
            str += "/%s" % (info["version"],)
        if info["url"]:
            str += " (%s)" % (info["url"],)
        return str

    def request(self, method, url, params=None, headers=None):
        rbody, rcode, rheaders, my_api_key = self.request_raw(
            method.lower(), url, params, headers, is_streaming=False
        )
        resp = self.interpret_response(rbody, rcode, rheaders)
        return resp, my_api_key

    def request_stream(self, method, url, params=None, headers=None):
        stream, rcode, rheaders, my_api_key = self.request_raw(
            method.lower(), url, params, headers, is_streaming=True
        )
        resp = self.interpret_streaming_response(stream, rcode, rheaders)
        return resp, my_api_key

    def handle_error_response(self, rbody, rcode, resp, rheaders):
        try:
            error_data = error.AtlanErrorObject(**resp)
        except (KeyError, TypeError):
            raise error.APIError(
                message="Invalid response object from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                code="ATLAN-PYTHON-400-019",
                status_code=400,
            )
        if not error_data:
            raise error.APIError(
                message="Invalid response object from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                code="ATLAN-PYTHON-400-019",
                status_code=400,
            )

        err = self.specific_api_error(rcode, error_data)

        raise err

    def specific_api_error(self, rcode, error_data):
        utils.log_info(
            "Atlan API error received",
            **error_data,
        )

        exception = None

        if rcode == 400:
            exception = error.InvalidRequestError(
                message="Server responded with %s: %s"
                % (
                    error_data.error_code if error_data.error_code else error_data.code,
                    error_data.error_message
                    if error_data.error_message
                    else error_data.message,
                ),
                param="",
                code="ATLAN-PYTHON-400-000",
            )
        elif rcode == 404:
            exception = error.NotFoundError(
                message="Server responded with %s: %s"
                % (
                    error_data.error_code if error_data.error_code else error_data.code,
                    error_data.error_message
                    if error_data.error_message
                    else error_data.message,
                ),
                code="ATLAN-PYTHON-404-000",
            )
        elif rcode == 401:
            exception = error.AuthenticationError(
                message="Server responded with %s: %s"
                % (
                    error_data.error_code if error_data.error_code else error_data.code,
                    error_data.error_message
                    if error_data.error_message
                    else error_data.message,
                ),
                code="ATLAN-PYTHON-401-000",
            )
        elif rcode == 403:
            exception = error.AtlanPermissionError(
                message="Server responded with %s: %s"
                % (
                    error_data.error_code if error_data.error_code else error_data.code,
                    error_data.error_message
                    if error_data.error_message
                    else error_data.message,
                ),
                code="ATLAN-PYTHON-403-000",
            )
        elif rcode == 409:
            exception = error.ConflictError(
                message="Server responded with %s: %s"
                % (
                    error_data.error_code if error_data.error_code else error_data.code,
                    error_data.error_message
                    if error_data.error_message
                    else error_data.message,
                ),
                code="ATLAN-PYTHON-409-000",
            )
        elif rcode == 429:
            # TODO: confirm that a 429 is raised rather than needing to check the X-RateLimit-Remaining-Minute
            #  header value of a response (if it is 0 then we are being rate-limited)
            exception = error.RateLimitError(
                message="Server responded with %s: %s"
                % (
                    error_data.error_code if error_data.error_code else error_data.code,
                    error_data.error_message
                    if error_data.error_message
                    else error_data.message,
                ),
                code="ATLAN-PYTHON-429-000",
            )
        else:
            exception = error.APIError(
                message="Server responded with %s: %s"
                % (
                    error_data.error_code if error_data.error_code else error_data.code,
                    error_data.error_message
                    if error_data.error_message
                    else error_data.message,
                ),
                code="ATLAN-PYTHON-500-000",
                status_code=500,
            )
        exception.atlan_error = error_data
        return exception

    def request_headers(self, api_key, method):
        user_agent = "Atlan-SDK/1.0 Python/%s" % (version.VERSION,)
        if pyatlan.app_info:
            user_agent += " " + self.format_app_info(pyatlan.app_info)

        ua = {
            "bindings_version": version.VERSION,
            "lang": "python",
            "publisher": "Atlan",
            "httplib": self._client.name,
        }
        for attr, func in [
            ["lang_version", platform.python_version],
            ["platform", platform.platform],
            ["uname", lambda: " ".join(platform.uname())],
        ]:
            try:
                val = func()
            except Exception:
                val = "(disabled)"
            ua[attr] = val
        if pyatlan.app_info:
            ua["application"] = pyatlan.app_info

        headers = {
            "X-Atlan-Client-User-Agent": json.dumps(ua),
            "User-Agent": user_agent,
            "Authorization": "Bearer %s" % (api_key,),
        }

        if method == "post":
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            headers.setdefault("Idempotency-Key", str(uuid.uuid4()))

        return headers

    def request_raw(
        self,
        method,
        url,
        params=None,
        supplied_headers=None,
        is_streaming=False,
    ):
        """
        Mechanism for issuing an API call
        """

        if self.api_key:
            my_api_key = self.api_key
        else:
            from pyatlan import api_key

            my_api_key = api_key

        if my_api_key is None:
            raise error.AuthenticationError(
                message="No API token provided.", code="ATLAN-PYTHON-401-001"
            )

        abs_url = "%s%s" % (self.api_base, url)

        encoded_params = urlencode(list(_api_encode(params or {})))

        # Don't use strict form encoding by changing the square bracket control
        # characters back to their literals. This is fine by the server, and
        # makes these parameter strings easier to read.
        encoded_params = encoded_params.replace("%5B", "[").replace("%5D", "]")

        post_data = None
        if method == "get" or method == "delete":
            if params:
                abs_url = _build_api_url(abs_url, encoded_params)
            post_data = None
        elif method == "post" or method == "put":
            if (
                supplied_headers is not None
                and supplied_headers.get("Content-Type") == "multipart/form-data"
            ):
                generator = MultipartDataGenerator()
                generator.add_params(params or {})
                post_data = generator.get_post_data()
                supplied_headers[
                    "Content-Type"
                ] = "multipart/form-data; boundary=%s" % (generator.boundary,)
            else:
                post_data = encoded_params

        headers = self.request_headers(my_api_key, method)
        if supplied_headers is not None:
            for key, value in supplied_headers:
                headers[key] = value

        utils.log_debug(
            "(%s) %s with: " % (method, abs_url),
            post_data=encoded_params,
        )

        if is_streaming:
            (rcontent, rcode, rheaders,) = self._client.request_stream_with_retries(
                method, abs_url, headers, post_data
            )
        else:
            rcontent, rcode, rheaders = self._client.request_with_retries(
                method, abs_url, headers, post_data
            )

        utils.log_info("Atlan API response", path=abs_url, response_code=rcode)
        utils.log_debug("API response body", body=rcontent)

        return rcontent, rcode, rheaders, my_api_key

    def _should_handle_code_as_error(self, rcode):
        return not 200 <= rcode < 300

    def interpret_response(self, rbody, rcode, rheaders):
        # Check for a 500 response first -- if found, we won't have a JSON body to parse,
        # so preemptively exit with a generic ApiException pass-through before attempting
        # the AtlanResponse translation (this will load the response as JSON).
        if rcode == 500:
            raise error.APIError(
                message=rbody if rbody else "",
                code="ATLAN-PYTHON-500-000",
                status_code=rcode,
            )
        # Check if the response is itself empty (not valid JSON), and return an empty response
        # straight away, if so
        if rbody is None or rbody == "null" or len(rbody) == 0 or rcode == 204:
            return None
        try:
            if hasattr(rbody, "decode"):
                rbody = rbody.decode("utf-8")
            resp = AtlanResponse(rbody, rcode, rheaders)
        except Exception:
            raise error.APIError(
                message="Invalid response object from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                code="ATLAN-PYTHON-400-019",
                status_code=400,
            )
        if self._should_handle_code_as_error(rcode):
            self.handle_error_response(rbody, rcode, resp.data, rheaders)
        return resp

    def interpret_streaming_response(self, stream, rcode, rheaders):
        # Streaming response are handled with minimal processing for the success
        # case (ie. we don't want to read the content). When an error is
        # received, we need to read from the stream and parse the received JSON,
        # treating it like a standard JSON response.
        if self._should_handle_code_as_error(rcode):
            if hasattr(stream, "getvalue"):
                json_content = stream.getvalue()
            elif hasattr(stream, "read"):
                json_content = stream.read()
            else:
                raise NotImplementedError(
                    "HTTP client %s does not return an IOBase object which "
                    "can be consumed when streaming a response."
                )

            return self.interpret_response(json_content, rcode, rheaders)
        else:
            return AtlanStreamResponse(stream, rcode, rheaders)
