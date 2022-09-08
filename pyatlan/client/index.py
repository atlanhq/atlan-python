#!/usr/bin/env/python
# Copyright 2022 Atlan Pte, Ltd
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
from pyatlan.model.index_search_criteria import IndexSearchRequest
from pyatlan.utils import API, BASE_URI, HTTPMethod, HTTPStatus

CRITERIA = {
    "dsl": {
        "from": 6,
        "size": 2,
        "post_filter": {"bool": {}},
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "announcementTitle": {
                                "value": "Monte",
                                "boost": 1.0,
                                "case_insensitive": True,
                            }
                        }
                    },
                    {
                        "term": {
                            "announcementTitle": {
                                "value": "Carlo",
                                "boost": 1.0,
                                "case_insensitive": True,
                            }
                        }
                    },
                    {
                        "term": {
                            "announcementTitle": {
                                "value": "Incident",
                                "boost": 1.0,
                                "case_insensitive": True,
                            }
                        }
                    },
                ]
            }
        },
    },
    "attributes": [
        "announcementMessage",
        "announcementTitle",
        "announcementType",
        "announcementUpdatedAt",
        "announcementUpdatedBy",
        "databaseName",
        "schemaName",
    ],
}


class IndexClient:
    INDEX_API = BASE_URI + "search/indexsearch"
    INDEX_SEARCH = API(INDEX_API, HTTPMethod.POST, HTTPStatus.OK)

    def __init__(self, client):
        self.client = client

    def index_search(self, criteria: IndexSearchRequest):
        while True:
            start = criteria.dsl.from_
            size = criteria.dsl.size
            response = self.client.call_api(
                IndexClient.INDEX_SEARCH, dict, request_obj=criteria.to_json()
            )
            approximate_count = response["approximateCount"]
            if "entities" in response:
                yield from response["entities"]
                if start + size < approximate_count:
                    criteria.dsl.from_ = start + size
                else:
                    break
            else:
                break
