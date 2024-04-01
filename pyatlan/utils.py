# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
from __future__ import annotations

import enum
import json
import logging
import random
import re
import time
from contextvars import ContextVar
from datetime import datetime
from enum import Enum
from functools import reduce, wraps
from typing import Any, Dict, List, Mapping, Optional

from pydantic.v1 import HttpUrl
from pydantic.v1.dataclasses import dataclass

from pyatlan.errors import ErrorCode

REQUESTID = "requestid"

APPLICATION_JSON = "application/json"
APPLICATION_ENCODED_FORM = "application/x-www-form-urlencoded;charset=UTF-8"

APPLICATION_OCTET_STREAM = "application/octet-stream"
MULTIPART_FORM_DATA = "multipart/form-data"
PREFIX_ATTR = "attr:"
PREFIX_ATTR_ = "attr_"

s_nextId = milliseconds = int(round(time.time() * 1000)) + 1


def to_camel_case(s: str) -> str:
    s = re.sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


def get_epoch_timestamp() -> float:
    return datetime.now().timestamp()


def next_id() -> str:
    global s_nextId

    s_nextId += 1

    return f"-{s_nextId}"


def get_parent_qualified_name(qualified_name: str) -> str:
    """
    Returns qualified name of the parent asset
    :param qualified_name: qualified of the asset
    """
    qn = qualified_name.split("/")
    return "/".join(qn[:-1])


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
    attributes: List[tuple[str, object]], query_params: Optional[dict] = None
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


def validate_required_fields(field_names: List[str], values: List[Any]):
    for field_name, value in zip(field_names, values):
        if value is None:
            raise ValueError(f"{field_name} is required")
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{field_name} cannot be blank")
        if isinstance(value, list) and len(value) == 0:
            raise ValueError(f"{field_name} cannot be an empty list")


@dataclass
class EndpointMixin:
    prefix: str
    service: HttpUrl


class EndPoint(EndpointMixin, Enum):
    ATLAS = (
        "api/meta/",
        "http://atlas-service-atlas.atlas.svc.cluster.local/api/atlas/v2/",
    )
    HEKA = "api/sql/", "http://heka-service.heka.svc.cluster.local/"
    IMPERSONATION = "", "http://keycloak-http.keycloak.svc.cluster.local/"
    HERACLES = "api/service/", "http://heracles-service.heracles.svc.cluster.local/"


class API:
    def __init__(
        self,
        path: str,
        method: "HTTPMethod",
        expected_status: int,
        endpoint: EndPoint,
        consumes: str = APPLICATION_JSON,
        produces: str = APPLICATION_JSON,
    ):
        self.path = path
        self.method = method
        self.expected_status = expected_status
        self.consumes = consumes
        self.produces = produces
        self.endpoint: EndPoint = endpoint

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
            endpoint=self.endpoint,
            consumes=self.consumes,
            produces=self.produces,
        )

    def format_path_with_params(self, *params):
        request_path = API.multipart_urljoin(self.path, *params)
        return API(
            request_path,
            self.method,
            self.expected_status,
            endpoint=self.endpoint,
            consumes=self.consumes,
            produces=self.produces,
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


def unflatten_custom_metadata(
    attributes: Optional[List[str]], asset_attributes: Optional[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    if not attributes or not asset_attributes:
        return None
    retval: Dict[str, Any] = {}
    metadata_attribute = re.compile(r"(\w+)[.](\w+)")
    for attribute_of_interest in attributes:
        if matched := metadata_attribute.match(attribute_of_interest):
            if attribute_of_interest in asset_attributes:
                key = matched[1]
                if key not in retval:
                    retval[key] = {}
                retval[key][matched[2]] = asset_attributes[attribute_of_interest]
    return retval


def unflatten_custom_metadata_for_entity(
    entity: Dict[str, Any], attributes: Optional[List[str]]
):
    if custom_metadata := unflatten_custom_metadata(
        attributes=attributes, asset_attributes=entity.get("attributes")
    ):
        entity["businessAttributes"] = custom_metadata


def init_guid(func):
    """Decorator function that can be used on the Create method of an asset to initialize the guid."""

    @wraps(func)
    def call(*args, **kwargs):
        ret_value = func(*args, **kwargs)
        if hasattr(ret_value, "guid"):
            ret_value.guid = str(
                -int(random.random() * 10000000000000000)  # noqa: S311
            )
        return ret_value

    return call


class ComparisonCategory(str, Enum):
    STRING = "str"
    NUMBER = "number"
    BOOLEAN = "bool"


def _get_embedded_type(attribute_type: str):
    return attribute_type[
        attribute_type.index("<") + 1 : attribute_type.index(">")  # noqa: E203
    ]


def get_base_type(attribute_type: str):
    base_type = attribute_type
    if "<" in attribute_type:
        if attribute_type.startswith("array<") and attribute_type.startswith(
            "array<map<"
        ):
            return _get_embedded_type(attribute_type[len("array<") : -1])  # noqa: E203
        elif attribute_type.startswith("array<") or attribute_type.startswith("map<"):
            return _get_embedded_type(attribute_type)
    return base_type


def is_comparable_type(attribute_type: str, to: ComparisonCategory) -> bool:
    base_type = get_base_type(attribute_type)
    if base_type == "boolean":
        return to == ComparisonCategory.BOOLEAN
    if base_type in ["int", "long", "date", "float"]:
        return to == ComparisonCategory.NUMBER
    return to == ComparisonCategory.STRING


def validate_type(name: str, _type, value):
    """
    Validate that the given value is of the specified type.

    :param name: the name of the variable to be used in the error message
    :param _type: the type of the variable to be validated
    :param value: the value to be validated that it is of the specified type

    """
    if _type is int:
        if isinstance(value, _type) and not isinstance(value, bool):
            return
    elif isinstance(_type, tuple):
        if any(isinstance(value, t) for t in _type):
            return
    elif isinstance(value, _type):
        return

    type_name = (
        ", ".join(t.__name__ for t in _type)
        if isinstance(_type, tuple)
        else _type.__name__
    )

    raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(name, type_name)


class AuthorizationFilter(logging.Filter):
    """
    A Filter that will replace the authorization header with the text '***REDACTED***'
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if record.args and hasattr(record.args, "__iter__"):
            for arg in record.args:
                if (
                    isinstance(arg, dict)
                    and "headers" in arg
                    and "authorization" in arg["headers"]
                ):
                    arg["headers"]["authorization"] = "***REDACTED***"

        return True


class JsonFormatter(logging.Formatter):
    """
    A custom JSON log formatter
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record

        :param record: The log record to be formatted
        :returns: The formatted log message
        """
        log_record = {
            "asctime": self.formatTime(record, self.datefmt),
            "name": record.name,
            "levelname": record.levelname,
            "message": (
                record.msg if isinstance(record.msg, dict) else record.getMessage()
            ),
        }
        return json.dumps(log_record, ensure_ascii=False)


class RequestIdFilter(logging.Filter):
    """
    A filter that will add requestid to the LogRecord if it is not already present. This is to support adding
    the requestid to the logging formatter
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if hasattr(record, REQUESTID):
            return True
        record.requestid = None
        return True


REQUEST_ID_FILTER = RequestIdFilter()


class ContextVarWrapper(Mapping):
    """
    This class implements the Mapping protocol on a ContextVar. This allows 'extra' information needed for a
    LogAdaptor to be obtained from a ContextVar.
    """

    def __init__(self, contextvar: ContextVar, key_name: str):
        """
        Create the ContextVarWrapper
        :param contextvar: the ContextVar that will provide the data
        :param key_name: the name that should be used to obtain a value from the contextvar
        """
        self.contextvar = contextvar
        self.key_name = key_name

    def __getitem__(self, item):
        if item == self.key_name:
            return self.contextvar.get()
        else:
            raise KeyError(f"Key must by '{self.key_name}' but was {item}")

    def __iter__(self):
        yield self.contextvar.get()

    def __len__(self):
        return 1


class RequestIdAdapter(logging.LoggerAdapter):
    """
    This is a LoggerAdapter that can be used to provide a reqquestid from a ContextVar
    """

    def __init__(self, logger: logging.Logger, contextvar: ContextVar):
        """
        Create the LoggerAdapter the will get the value to be used for 'requestid'  from the given ContextVar
        :param logger: the Logger to wrap
        :param contextvar: the ContextVar from which to obtain the value to be used for 'requestid'

        """
        super().__init__(
            logger, ContextVarWrapper(contextvar=contextvar, key_name=REQUESTID)
        )

    def process(self, msg, kwargs):
        return f"[{self.extra['requestid']}] {msg}", kwargs


def validate_single_required_field(field_names: List[str], values: List[Any]):
    indexes = [idx for idx, value in enumerate(values) if value is not None]
    if not indexes:
        raise ValueError(
            f"One of the following parameters are required: {', '.join(field_names)}"
        )
    if len(indexes) > 1:
        names = [field_names[idx] for idx in indexes]
        raise ValueError(
            f"Only one of the following parameters are allowed: {', '.join(names)}"
        )
