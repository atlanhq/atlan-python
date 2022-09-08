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
from dataclasses import dataclass, field


@dataclass()
class DSL:
    from_: int = 0
    size: int = 100
    post_filter: dict = field(default_factory=dict)
    query: dict = field(default_factory=dict)

    def to_json(self):
        json = {"from": self.from_, "size": self.size, "query": self.query}
        if self.post_filter:
            json["post_filter"] = self.post_filter
        return json


@dataclass()
class IndexSearchRequest:
    dsl: DSL = DSL()
    attributes: list = field(default_factory=list)
    relation_attributes: list = field(default_factory=list)

    def to_json(self):
        json = {"dsl": self.dsl.to_json(), "attributes": self.attributes}
        if self.relation_attributes:
            json["relationAttributes"] = self.relation_attributes
        return json
