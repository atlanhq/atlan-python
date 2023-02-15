# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
import enum
import logging
import time
from functools import reduce
from typing import Optional

ADMIN_URI = "api/service/"
BASE_URI = "api/meta/"
APPLICATION_JSON = "application/json"
APPLICATION_OCTET_STREAM = "application/octet-stream"
MULTIPART_FORM_DATA = "multipart/form-data"
PREFIX_ATTR = "attr:"
PREFIX_ATTR_ = "attr_"

s_nextId = milliseconds = int(round(time.time() * 1000)) + 1


def get_logger(name: str = __name__, level: str = "WARN"):
    """
    name - defaults to __name__
    """
    logging.basicConfig(
        level=logging.WARN,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    )
    logger = logging.getLogger(name)
    logger.setLevel(level=level)
    return logger


def next_id() -> str:
    global s_nextId

    s_nextId += 1

    return f"-{s_nextId}"


def list_attributes_to_params(
    attributes_list: list, query_params: Optional[dict] = None
) -> dict:
    if query_params is None:
        query_params = {}

    for i, attr in enumerate(attributes_list):
        for key, value in attr.items():
            new_key = PREFIX_ATTR_ + str(i) + ":" + key
            query_params[new_key] = value

    return query_params


def attributes_to_params(
    attributes: list[tuple[str, object]], query_params: Optional[dict] = None
) -> dict:
    if query_params is None:
        query_params = {}

    if attributes:
        for key, value in attributes:
            new_key = PREFIX_ATTR + key
            query_params[new_key] = value

    return query_params


def non_null(obj: Optional[object], def_value: object):
    return obj if obj is not None else def_value


def type_coerce(obj, obj_type):
    if isinstance(obj, obj_type):
        ret = obj
    elif isinstance(obj, dict):
        ret = obj_type(obj)

        ret.type_coerce_attrs()
    else:
        ret = None

    return ret


def type_coerce_list(obj, obj_type):
    return (
        [type_coerce(entry, obj_type) for entry in obj]
        if isinstance(obj, list)
        else None
    )


def type_coerce_dict(obj, obj_type):
    return (
        {k: type_coerce(v, obj_type) for k, v in obj.items()}
        if isinstance(obj, dict)
        else None
    )


def type_coerce_dict_list(obj, obj_type):
    return (
        {k: type_coerce_list(v, obj_type) for k, v in obj.items()}
        if isinstance(obj, dict)
        else None
    )


class API:
    def __init__(
        self,
        path,
        method,
        expected_status,
        consumes=APPLICATION_JSON,
        produces=APPLICATION_JSON,
    ):
        self.path = path
        self.method = method
        self.expected_status = expected_status
        self.consumes = consumes
        self.produces = produces

    @staticmethod
    def multipart_urljoin(base_path, *path_elems):
        """Join a base path and multiple context path elements. Handle single
        leading and trailing `/` characters transparently.

        Args:
            base_path (string): the base path or url (ie. `http://atlas/v2/`)
            *path_elems (string): multiple relative path elements (ie. `/my/relative`, `/path`)

        Returns:
            string: the result of joining the base_path with the additional path elements
        """

        def urljoin_pair(left, right):
            return "/".join([left.rstrip("/"), right.strip("/")])

        return reduce(urljoin_pair, path_elems, base_path)

    def format_path(self, params):
        return API(
            self.path.format(**params),
            self.method,
            self.expected_status,
            self.consumes,
            self.produces,
        )

    def format_path_with_params(self, *params):
        request_path = API.multipart_urljoin(self.path, *params)
        return API(
            request_path,
            self.method,
            self.expected_status,
            self.consumes,
            self.produces,
        )


class HTTPMethod(enum.Enum):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    DELETE = "DELETE"


class HTTPStatus:
    OK = 200
    NO_CONTENT = 204
    NOT_FOUND = 404
    SERVICE_UNAVAILABLE = 503
