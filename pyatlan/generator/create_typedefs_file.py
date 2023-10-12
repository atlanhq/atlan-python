# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
"""
This script will retrieve the typedefs from an Atlan instance and write them to a json file. This class_generator will
use this file to produce code for assets, structs and enums for atlan. The ATLAN_BASE_URL and ATLAN_API_KEY
environment variables should be set before running this script.
"""

from pyatlan.client.atlan import AtlanClient
from pyatlan.generator.class_generator import TYPE_DEF_FILE


class ServerError(Exception):
    pass


def create_typedef_file():
    client = AtlanClient()
    type_defs = client.typedef.get_all()
    if len(type_defs.entity_defs) == 0:
        raise ServerError("No entity definitions were returned from the server.")
    with TYPE_DEF_FILE.open("w") as output_file:
        output_file.write(type_defs.json())
    print(f"{TYPE_DEF_FILE} has been created.")


if __name__ == "__main__":
    create_typedef_file()
