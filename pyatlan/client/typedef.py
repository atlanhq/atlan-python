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

from pyatlan.model.typedef import TypeDefResponse
from pyatlan.utils import API, BASE_URI, HTTPMethod, HTTPStatus
from pyatlan.client.atlan import AtlanClient


class TypeDefClient:
    TYPES_API = BASE_URI + "types/"
    TYPEDEFS_API = TYPES_API + "typedefs/"
    TYPEDEF_BY_NAME = TYPES_API + "typedef.py/name"
    TYPEDEF_BY_GUID = TYPES_API + "typedef.py/guid"
    GET_BY_NAME_TEMPLATE = TYPES_API + "{path_type}/name/{name}"
    GET_BY_GUID_TEMPLATE = TYPES_API + "{path_type}/guid/{guid}"

    GET_TYPEDEF_BY_NAME = API(TYPEDEF_BY_NAME, HTTPMethod.GET, HTTPStatus.OK)
    GET_TYPEDEF_BY_GUID = API(TYPEDEF_BY_GUID, HTTPMethod.GET, HTTPStatus.OK)
    GET_ALL_TYPE_DEFS = API(TYPEDEFS_API, HTTPMethod.GET, HTTPStatus.OK)
    GET_ALL_TYPE_DEF_HEADERS = API(
        TYPEDEFS_API + "headers", HTTPMethod.GET, HTTPStatus.OK
    )
    UPDATE_TYPE_DEFS = API(TYPEDEFS_API, HTTPMethod.PUT, HTTPStatus.OK)
    CREATE_TYPE_DEFS = API(TYPEDEFS_API, HTTPMethod.POST, HTTPStatus.OK)
    DELETE_TYPE_DEFS = API(TYPEDEFS_API, HTTPMethod.DELETE, HTTPStatus.NO_CONTENT)
    DELETE_TYPE_DEF_BY_NAME = API(
        TYPEDEF_BY_NAME, HTTPMethod.DELETE, HTTPStatus.NO_CONTENT
    )

    def __init__(self, client):
        self.client = client

    def get_all_typedefs(self) -> TypeDefResponse:
        raw_json = self.client.call_api(TypeDefClient.GET_ALL_TYPE_DEFS)
        return TypeDefResponse(**raw_json)


if __name__ == "__main__":
    client = TypeDefClient(AtlanClient())
    type_def_response = client.get_all_typedefs()
    pass
