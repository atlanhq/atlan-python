# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


CAMEL_CASE_OVERRIDES = {
    "index_type_es_fields": "IndexTypeESFields",
    "source_url": "sourceURL",
    "source_embed_url": "sourceEmbedURL",
    "sql_dbt_sources": "sqlDBTSources",
    "purpose_atlan_tags": "purposeClassifications",
    "mapped_atlan_tag_name": "mappedClassificationName",
    "has_lineage": "__hasLineage",
    "atlan_tags": "classifications",
}


def encoders():
    from datetime import datetime

    from pyatlan.model.core import AtlanTagName

    return {
        datetime: lambda v: int(v.timestamp() * 1000),
        AtlanTagName: lambda atn: atn._display_text,
    }


def convert_with_fixed_prefix(input_str, fixed_prefix):
    prefix = fixed_prefix
    remaining = input_str[len(prefix) + 1 :]
    parts = remaining.split("_")
    camel_part = "".join(word.capitalize() for word in parts)
    return prefix + camel_part


def to_camel_case(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Value must be a string")
    if value == "__root__":
        return value
    if value in CAMEL_CASE_OVERRIDES:
        return CAMEL_CASE_OVERRIDES[value]
    value = "".join(word.capitalize() for word in value.split("_"))
    if value.startswith("__"):
        value = value[2:]
    return f"{value[0].lower()}{value[1:]}"


def to_python_class_name(string):
    """
    Convert any string to a valid Python class name following PEP 8 conventions.
    If the string is already a valid class name, it returns it unchanged.

    Args:
        string (str): Input string to convert

    Returns:
        str: Valid Python class name or empty string if conversion results in invalid name

    Examples:
        >>> to_python_class_name("AtlasGlossaryPreferredTerm")
        'AtlasGlossaryPreferredTerm'
        >>> to_python_class_name("hello-world-123")
        'HelloWorld123'
        >>> to_python_class_name("my.email@address.com")
        'MyEmailAddressCom'
        >>> to_python_class_name("123_start_with_number")
        'StartWithNumber'
        >>> to_python_class_name("class")
        'Class_'
    """
    import keyword
    import re

    def is_valid_python_class_name(string):
        """
        Check if a string is already a valid Python class name.

        Args:
            string (str): String to check

        Returns:
            bool: True if valid class name, False otherwise
        """
        if not string:
            return False

        # Check if it's a valid identifier
        if not string.isidentifier():
            return False

        # Check if it's a keyword
        if keyword.iskeyword(string):
            return False

        # Check if it starts with capital letter (PEP 8 convention for classes)
        if not string[0].isupper():
            return False

        return True

    # Handle empty string
    if not string:
        return ""

    # If it's already a valid class name, return as is
    if is_valid_python_class_name(string):
        return string

    # Check if it's a valid identifier but needs conversion from snake_case
    if string.isidentifier() and not keyword.iskeyword(string):
        # If it contains underscores, convert from snake_case to PascalCase
        if "_" in string:
            words = string.split("_")
            return "".join(word.capitalize() for word in words if word)
        # Otherwise just capitalize first letter
        return string[0].upper() + string[1:]

    # Otherwise, perform full conversion
    # Replace common separators with spaces
    converted = re.sub(r'[-_./@#$%^&*()+=\[\]{};:\'",<>?\\|`~]', " ", string)

    # Remove any remaining non-alphanumeric characters except spaces
    converted = re.sub(r"[^a-zA-Z0-9\s]", "", converted)

    # Split on spaces and filter out empty strings
    words = [word for word in converted.split() if word]

    # If no words remain after cleaning, return empty string
    if not words:
        return ""

    # Capitalize each word (PascalCase for class names)
    words = [word.capitalize() for word in words]

    # Join words
    class_name = "".join(words)

    # Ensure it doesn't start with a digit
    if class_name and class_name[0].isdigit():
        # Remove leading digits
        class_name = re.sub(r"^\d+", "", class_name)
        if not class_name:
            return ""

    # Handle Python keywords
    if keyword.iskeyword(class_name.lower()):
        class_name += "_"

    return class_name


def to_snake_case(value):
    if value.startswith("__"):
        value = value[2:]
    if value == "purposeClassifications":
        return "purpose_atlan_tags"
    elif value == "mappedClassificationName":
        return "mapped_atlan_tag_name"
    res = [value[0].lower()]
    for c in (
        value.replace("URL", "Url").replace("DBT", "Dbt").replace("GDPR", "Gdpr")[1:]
    ):
        if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            res.append("_")
            res.append(c.lower())
        else:
            res.append(c)
    return "".join(res).replace(" _", "_").replace(" ", "_")


def construct_object_key(prefix: str, name: str) -> str:
    """
    Construct an object key by joining a prefix and a name.
    If the prefix is empty, the name is returned as-is.
    """
    if not prefix:
        return name  # Preserve the key as-is if no prefix

    # Ensure correct joining while preserving leading slashes
    if prefix.endswith("/") or name.startswith("/"):
        return f"{prefix}{name.strip('/')}"
    return f"{prefix}/{name.strip('/')}"
