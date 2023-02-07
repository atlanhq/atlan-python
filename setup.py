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

from setuptools import find_packages, setup

# External dependencies
requirements = ["requests>=2.24", "pydantic", "jinja2"]

long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyatlan",
    version="0.0.2",
    author="Atlan Pte, Ltd",
    author_email="engineering@atlan.com",
    description="Atlan Python Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atlanhq/atlan-python",
    license="Apache LICENSE 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
    keywords="atlas client, apache atlas",
    python_requires=">=3.9",
)
