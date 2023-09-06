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
