#!/usr/bin/env/python
# Copyright 2022 Atlan Pte, Ltd
# Copyright [2015-2021] The Apache Software Foundation
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import copy
import json
import logging
import os


import requests

from pydantic import BaseSettings, HttpUrl, PrivateAttr, Field
from pyatlan.exceptions import AtlanServiceException
from pyatlan.utils import HTTPMethod, HTTPStatus, get_logger
from pyatlan.model.core import AtlanObject

LOGGER = get_logger()


class AtlanClient(BaseSettings):
    host: HttpUrl
    api_key: str
    session: requests.Session = Field(default_factory=requests.Session)
    _request_params: dict = PrivateAttr()

    class Config:
        env_prefix = "atlan_"

    def __init__(self, **data):
        super().__init__(**data)
        self._request_params = {"headers": {"authorization": f"Bearer {self.api_key}"}}

    def call_api(self, api, query_params=None, request_obj=None):
        params = copy.deepcopy(self._request_params)
        path = os.path.join(self.host, api.path)
        params["headers"]["Accept"] = api.consumes
        params["headers"]["content-type"] = api.produces

        if query_params is not None:
            params["params"] = query_params

        if request_obj is not None:
            if isinstance(request_obj, AtlanObject):
                params["data"] = request_obj.json(by_alias=True)
            else:
                params["data"] = json.dumps(request_obj)

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("------------------------------------------------------")
            LOGGER.debug("Call         : %s %s", api.method, path)
            LOGGER.debug("Content-type_ : %s", api.consumes)
            LOGGER.debug("Accept       : %s", api.produces)

        response = None

        if api.method == HTTPMethod.GET:
            response = self.session.get(path, **params)
        elif api.method == HTTPMethod.POST:
            response = self.session.post(path, **params)
        elif api.method == HTTPMethod.PUT:
            response = self.session.put(path, **params)
        elif api.method == HTTPMethod.DELETE:
            response = self.session.delete(path, **params)

        if response is not None:
            LOGGER.debug("HTTP Status: %s", response.status_code)

        if response is None:
            return None
        elif response.status_code == api.expected_status:
            try:
                if response.content is None or response.status_code == HTTPStatus.NO_CONTENT:
                    return None
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug(
                        "<== __call_api(%s,%s,%s), result = %s",
                        vars(api),
                        params,
                        request_obj,
                        response,
                    )
                    LOGGER.debug(response.json())
                return response.json()
            except Exception as e:
                print(e)
                LOGGER.exception(
                    "Exception occurred while parsing response with msg: %s", e
                )
                raise AtlanServiceException(api, response) from e
        elif response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
            LOGGER.error(
                "Atlas Service unavailable. HTTP Status: %s",
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

            return None
        else:
            raise AtlanServiceException(api, response)


if __name__ == "__main__":
    client = AtlanClient()
    print(client.dict())
