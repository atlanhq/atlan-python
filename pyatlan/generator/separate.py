import inspect
from enum import Enum
from pathlib import Path

import pyatlan.model.enums
from pyatlan.generator.class_generator import get_type, get_type_defs

PARENT = Path(__file__).parent
HEADER = """# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
from datetime import datetime
from enum import Enum

"""
WARNING = """# **************************************
# CODE BELOW IS GENERATED NOT MODIFY  **
# **************************************
"""

type_defs = get_type_defs()
enum_def_names = {get_type(enum_def.name) for enum_def in type_defs.enum_defs}
enums_by_name = {
    cls_name: cls_obj
    for cls_name, cls_obj in inspect.getmembers(pyatlan.model.enums)
    if inspect.isclass(cls_obj) and issubclass(cls_obj, Enum) and cls_name != "Enum"
}
all_enum_names = set(enums_by_name.keys())
generated_enum_names = sorted(enum_def_names.intersection(all_enum_names))
manual_enum_names = sorted(all_enum_names.difference(enum_def_names))
with (PARENT / "generated").open("w") as output:
    output.write(HEADER)
    for name in manual_enum_names:
        source = inspect.getsource(enums_by_name[name])
        output.write(source)
    output.write(WARNING)
    for name in generated_enum_names:
        source = inspect.getsource(enums_by_name[name])
        output.write(source)
