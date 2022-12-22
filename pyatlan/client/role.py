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
from typing import Optional

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.role import RoleResponse
from pyatlan.utils import ADMIN_URI, API, HTTPMethod, HTTPStatus


class RoleClient:
    ROLE_API = ADMIN_URI + "roles"

    # Role APIs
    GET_ROLES = API(ROLE_API, HTTPMethod.GET, HTTPStatus.OK)

    def __init__(self, client: AtlanClient):
        self.client = client

    def get_roles(
        self,
        limit: int,
        filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> RoleResponse:
        if filter is None:
            filter = ""
        if sort is None:
            sort = ""
        query_params = {
            "filter": filter,
            "sort": sort,
            "count": count,
            "offset": offset,
            "limit": limit,
        }
        raw_json = self.client.call_api(
            RoleClient.GET_ROLES.format_path_with_params(), query_params
        )
        response = RoleResponse(**raw_json)
        return response

    def get_all_roles(self) -> RoleResponse:
        """
        Retrieve all roles defined in Atlan.
        """
        raw_json = self.client.call_api(RoleClient.GET_ROLES.format_path_with_params())
        response = RoleResponse(**raw_json)
        return response
