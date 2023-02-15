# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import absolute_import, division, print_function

from typing import Optional

from pyatlan.model.core import AtlanObject


class AtlanErrorObject(AtlanObject):
    def __init__(
        self,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None,
        entity_guid: Optional[str] = None,
    ):
        super(AtlanObject, self).__init__()
        self.error_code = error_code
        self.error_message = error_message
        self.entity_guid = entity_guid


class AtlanError(Exception):
    """
    Base class for any error raised by interactions with Atlan's APIs.
    """

    def __init__(self, message: str, code: str, status_code: Optional[int]):
        super().__init__(message)
        self._message = message
        self.code = code
        self.status_code = status_code

    def __str__(self):
        return self._message or "<empty message>"

    # Returns the underlying `Exception` (base class) message, which is usually
    # the raw message returned by Atlan's API.
    @property
    def user_message(self):
        return self._message

    def __repr__(self):
        return "%s(message=%r, code=%r, status=%r)" % (
            self.__class__.__name__,
            self._message,
            self.code,
            self.status_code,
        )


class APIError(AtlanError):
    """
    Error that occurs when the SDK receives a response that indicates a problem, but that the SDK currently has no
    other way of interpreting. Basically, this is a catch-all for errors that do not fit any more specific exception.
    """

    pass


class APIConnectionError(AtlanError):
    def __init__(
        self,
        message: str,
        code: str,
        status_code: Optional[int] = None,
        should_retry: bool = False,
    ):

        super(APIConnectionError, self).__init__(message, code, status_code)
        self.should_retry = should_retry


class AtlanErrorWithParamCode(AtlanError):
    def __init__(self, message: str, param: str, code: str, status_code: int):
        self.param = param
        super().__init__(message=message, code=code, status_code=status_code)

    def __repr__(self):
        return "%s(message=%r, param=%r, code=%r, status_code=%r)" % (
            self.__class__.__name__,
            self._message,
            self.param,
            self.code,
            self.status_code,
        )


class InvalidRequestError(AtlanErrorWithParamCode):
    """
    Error that occurs if the request being attempted is not valid for some reason, such as containing insufficient
    parameters or incorrect values for those parameters.
    """

    def __init__(self, message: str, param: str, code: str, status_code: int = 400):
        super().__init__(message, param, code, status_code)
        self.param = param


class AuthenticationError(AtlanError):
    """
    Error that occurs when there is a problem with the API token configured in the SDK.
    """

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 403,
        should_retry: bool = False,
    ):
        super().__init__(message, code, status_code)
        self.should_retry = should_retry


class AtlanPermissionError(AuthenticationError):
    """
    Error that occurs if the API token configured for the SDK does not have permission to access or carry out the
    requested operation on a given object. These can be temporary in nature, as there is some asynchronous processing
    that occurs when permissions are granted.
    """

    def __init__(
        self, message: str, code: str, status_code: int = 403, should_retry: bool = True
    ):
        super(AuthenticationError, self).__init__(message, code, status_code)
        self.should_retry = should_retry


class RateLimitError(AtlanError):
    """
    Error that occurs when no further requests are being accepted from the IP address on which the SDK is running.
    By default, Atlan allows 1800 requests per minute. If your use of the SDK exceed this, you will begin to see
    these exceptions.
    """

    def __init__(self, message: str, code: str, status_code: int = 429):
        super().__init__(message, code, status_code)


class NotFoundError(AtlanError):
    """
    Error that occurs if a requested object does not exist. For example, trying to retrieve an asset that does not
    exist.
    """

    def __init__(self, message: str, code: str, status_code: int = 404):
        super().__init__(message, code, status_code)


class ConflictError(AtlanError):
    """
    Error that occurs if the operation being attempted hits a conflict within Atlan. For example, trying to create
    an object that already exists.
    """

    def __init__(self, message: str, code: str, status_code: int = 409):
        super().__init__(message, code, status_code)


class LogicError(AtlanError):
    """
    Error that occurs when an unexpected logic problem arises. If these are ever experienced, they should be
    immediately reported against the SDK as bugs.
    """

    def __init__(self, message: str, code: str, status_code: int = 500):
        super().__init__(message, code, status_code)
