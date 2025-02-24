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
import io
import os
import re
import sys


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(
        os.path.join(os.path.dirname(__file__), file_name), encoding="utf-8"
    ) as f:
        return f.read()


def main(env_var="GITHUB_REF") -> int:
    git_ref = os.getenv(env_var, "none")
    tag = re.sub("^refs/tags/v*", "", git_ref.lower())
    version = read("pyatlan/version.txt").strip()
    if tag == version:
        return 0
    else:
        print(
            f"✖ {env_var} env var {git_ref!r} does not match package version: {tag!r} != {version!r}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
