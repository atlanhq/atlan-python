# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
from typing import Optional


class AtlanServiceException(Exception):
    """Exception raised for errors in API calls.
    Attributes:
        api -- api endpoint which caused the error
        response -- response from the server
    """

    def __init__(self, api, response):
        msg = ""

        if api:
            msg = "Metadata service API {method} : {path} failed".format(
                **{"method": api.method, "path": api.path}
            )

        if response.content is not None:
            status = response.status_code if response.status_code is not None else -1
            msg = (
                "Metadata service API with url {url} and method {method} : failed with status {status} and "
                "Response Body is :{response}".format(
                    **{
                        "url": response.url,
                        "method": api.method,
                        "status": status,
                        "response": response.json(),
                    }
                )
            )

        Exception.__init__(self, msg)


class AtlanException(Exception):
    """
    Base class for any error raised by interactions with Atlan's APIs.
    """

    def __init__(
        self,
        message: str,
        status_code: int,
        code: Optional[str],
        cause: Optional[Exception] = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.cause = cause


class InvalidRequestException(AtlanException):
    """
    Error that occurs if the request being attempted is not valid for some reason, such as containing insufficient
    parameters of incorrect values for those parameters.
    """

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        param: Optional[str] = None,
        cause: Optional[Exception] = None,
    ):
        super().__init__(message, 400, code, cause)
        self.param = param


class LogicException(AtlanException):
    """
    Error that occurs when an unexpected logic problem arises. If these are ever experienced, they should be
    immediately reported against the SDK as bugs.
    """

    def __init__(self, message: str, code: str, cause: Optional[Exception] = None):
        super().__init__(message, 500, code, cause)
