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

from setuptools import find_packages, setup

# External dependencies
requirements = ["requests>=2.24", "pydantic>=1.10.4", "jinja2>=3.1.2"]


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(
        os.path.join(os.path.dirname(__file__), file_name), encoding="utf-8"
    ) as f:
        return f.read()


long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyatlan",
    version=read("pyatlan/version.txt"),
    author="Atlan Technologies Pvt Ltd",
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
        "Development Status :: 4 - Beta",
    ],
    packages=find_packages(),
    install_requires=requirements,
    extra_requires={
        "dev": [
            "pytest>=7.2.0",
            "flake8>=5.0.4",
            "mypy>=0.991",
            "black>=22.10.0",
            "types-requests>=2.28.11.4",
            "pre-commit>=2.20.0",
            "deepdiff>=6.2.1",
            "pytest-cov>=4.0.0",
            "twine>=4.0.2",
        ]
    },
    include_package_data=True,
    zip_safe=False,
    keywords="atlan client",
    python_requires=">=3.9",
    repository="https://github.com/atlanhq/atlan-python",
)
