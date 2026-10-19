# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SodaCheck model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-soda-app emits today
(``{connectionQN}/check/{checkId}``, FND-3838 census), so a creator change that
would re-key existing checks fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import SodaCheck

CONNECTION_QUALIFIED_NAME = "default/soda/123456789"
CONNECTOR_NAME = "soda"
CHECK_NAME = "row_count > 0"
CHECK_ID = "8f6a2c1e-check-id"
CHECK_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/check/{CHECK_ID}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-soda-app's build_soda_check_entity inputs and output."""
    sut = SodaCheck.creator(
        name="orders has rows",
        soda_check_id="a1b2c3",
        connection_qualified_name="default/soda/1700000000",
    )

    assert sut.qualified_name == "default/soda/1700000000/check/a1b2c3"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, soda_check_id, connection_qualified_name, message",
    [
        (None, CHECK_ID, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", CHECK_ID, CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (CHECK_NAME, None, CONNECTION_QUALIFIED_NAME, "soda_check_id is required"),
        (CHECK_NAME, " ", CONNECTION_QUALIFIED_NAME, "soda_check_id cannot be blank"),
        (CHECK_NAME, CHECK_ID, None, "connection_qualified_name is required"),
        (CHECK_NAME, CHECK_ID, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, soda_check_id: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SodaCheck.creator(
            name=name,
            soda_check_id=soda_check_id,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator sets the check id and denormalised connection attributes."""
    sut = SodaCheck.creator(
        name=CHECK_NAME,
        soda_check_id=CHECK_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.type_name == "SodaCheck"
    assert sut.name == CHECK_NAME
    assert sut.soda_check_id == CHECK_ID
    assert sut.qualified_name == CHECK_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.guid
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, CHECK_NAME, "qualified_name is required"),
        (CHECK_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SodaCheck.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a SodaCheck for modification."""
    sut = SodaCheck.updater(qualified_name=CHECK_QUALIFIED_NAME, name=CHECK_NAME)

    assert sut.qualified_name == CHECK_QUALIFIED_NAME
    assert sut.name == CHECK_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = SodaCheck.creator(
        name=CHECK_NAME,
        soda_check_id=CHECK_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == CHECK_QUALIFIED_NAME
    assert sut.name == CHECK_NAME
    assert sut.soda_check_id is UNSET
