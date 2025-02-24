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
        AtlanTagName: AtlanTagName.json_encode_atlan_tag,
    }


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
