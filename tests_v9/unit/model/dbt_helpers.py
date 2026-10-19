# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Shared inputs and assertions for the dbt creator unit tests.

Each ``dbt_*_test.py`` pins the literal qualifiedName atlan-dbt-app emits today
(FND-3838 census), so a creator change that would re-key existing dbt assets fails.
"""

import pytest

CONNECTION_QN = "default/dbt/1712345678"
ACCOUNT_ID = "70403103932498"
PROJECT_ID = "70403104069713"
ENVIRONMENT_ID = "70403103991524"
BASE = f"{CONNECTION_QN}/account/{ACCOUNT_ID}/project/{PROJECT_ID}"
ENV = f"{BASE}/env/{ENVIRONMENT_ID}"

PROJECT_KWARGS = dict(
    connection_qualified_name=CONNECTION_QN,
    account_id=ACCOUNT_ID,
    project_id=PROJECT_ID,
)
ENV_KWARGS = dict(**PROJECT_KWARGS, environment_id=ENVIRONMENT_ID)

MODEL_UID = "model.jaffle_shop.orders"
SEED_UID = "seed.jaffle_shop.raw_customers"
SEMANTIC_MODEL_UID = "semantic_model.jaffle_shop.orders"
MODEL_QN = f"{ENV}/{MODEL_UID}"
SEED_QN = f"{ENV}/{SEED_UID}"
SEMANTIC_MODEL_QN = f"{ENV}/{SEMANTIC_MODEL_UID}"

NAME = "orders"

# Parent qualifiedNames that are not an env-scoped dbt model, seed or semantic model.
MALFORMED_PARENT_QNS = pytest.mark.parametrize(
    "bad_parent_qn",
    [
        CONNECTION_QN,
        BASE,
        # a source qn has no env segment
        f"{BASE}/source.jaffle_shop.raw.orders",
        # a column qn is one segment too deep
        f"{MODEL_QN}/{NAME}",
        # the app's literal-None rendering of a missing id
        f"{CONNECTION_QN}/account/None/project/{PROJECT_ID}/env//{MODEL_UID}",
    ],
    ids=["connection", "project", "source", "column", "blank-env"],
)


def assert_created(sut, expected_qn: str, name: str = NAME) -> None:
    assert sut.qualified_name == expected_qn
    assert sut.name == name
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "dbt"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def assert_rejects_missing_or_blank(asset_type, kwargs: dict, param: str) -> None:
    # The app renders a missing id as the literal "None"; the creator must raise.
    args = {"name": NAME, **kwargs}
    args[param] = None
    with pytest.raises(ValueError, match=f"{param} is required"):
        asset_type.creator(**args)
    args[param] = "  "
    with pytest.raises(ValueError, match=f"{param} cannot be blank"):
        asset_type.creator(**args)


def assert_rejects_slash(asset_type, kwargs: dict, param: str) -> None:
    with pytest.raises(ValueError, match=f"{param} cannot contain '/'"):
        asset_type.creator(name=NAME, **{**kwargs, param: "a/b"})


def assert_rejects_malformed_connection(asset_type, kwargs: dict) -> None:
    with pytest.raises(ValueError, match="Invalid connection_qualified_name"):
        asset_type.creator(name=NAME, **{**kwargs, "connection_qualified_name": BASE})


def assert_updater(asset_type, qualified_name: str) -> None:
    for args, message in [
        (dict(qualified_name=None, name=NAME), "qualified_name is required"),
        (dict(qualified_name=qualified_name, name=None), "name is required"),
    ]:
        with pytest.raises(ValueError, match=message):
            asset_type.updater(**args)

    sut = asset_type.updater(qualified_name=qualified_name, name=NAME)
    assert sut.qualified_name == qualified_name
    assert sut.name == NAME
    assert (
        asset_type.create_for_modification(
            qualified_name=qualified_name, name=NAME
        ).qualified_name
        == qualified_name
    )

    trimmed = sut.trim_to_required()
    assert trimmed.qualified_name == qualified_name
    assert trimmed.name == NAME
