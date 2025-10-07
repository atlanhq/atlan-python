# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
This script will retrieve the typedefs from an Atlan instance and write them to a json file. This class_generator will
use this file to produce code for assets, structs and enums for atlan. The ATLAN_BASE_URL and ATLAN_API_KEY
environment variables should be set before running this script.
"""

import argparse
import os
from pathlib import Path

from pyatlan.client.atlan import AtlanClient


class ServerError(Exception):
    pass


def create_typedef_file(typedefs_file_path=None):
    # Use provided path or default to tmp directory
    if typedefs_file_path:
        # file deepcode ignore PT: used in class generator script
        typedef_file = Path(typedefs_file_path)
    else:
        typedef_file = Path(os.getenv("TMPDIR", "/tmp")) / "typedefs.json"

    client = AtlanClient()
    type_defs = client.typedef.get_all()
    if len(type_defs.entity_defs) == 0:
        raise ServerError("No entity definitions were returned from the server.")

    # Create directory if it doesn't exist
    typedef_file.parent.mkdir(parents=True, exist_ok=True)

    with typedef_file.open("w") as output_file:
        output_file.write(type_defs.json())
    print(f"{typedef_file} has been created.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create typedefs file from Atlan instance"
    )
    parser.add_argument(
        "--typedefs-file",
        type=str,
        help="Path to the typedefs file (default: /tmp/typedefs.json or $TMPDIR/typedefs.json)",
    )
    args = parser.parse_args()

    create_typedef_file(args.typedefs_file)
