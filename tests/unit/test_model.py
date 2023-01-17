import json
from pathlib import Path

import pytest
from deepdiff import DeepDiff
from pydantic.error_wrappers import ValidationError

from pyatlan.model.assets import (
    AssetMutationResponse,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Connection,
    Database,
)
from pyatlan.model.core import Announcement, AssetResponse
from pyatlan.model.enums import AnnouncementType, AtlanConnectorType

DATA_DIR = Path(__file__).parent / "data"
GLOSSARY_JSON = "glossary.json"
GLOSSARY_TERM_JSON = "glossary_term.json"
GLOSSARY_CATEGORY_JSON = "glossary_category.json"


def load_json(filename):
    with (DATA_DIR / filename).open() as input_file:
        return json.load(input_file)


@pytest.fixture()
def glossary_json():
    return load_json(GLOSSARY_JSON)


@pytest.fixture()
def glossary(glossary_json):
    return AtlasGlossary(**glossary_json)


@pytest.fixture()
def announcement():
    return Announcement(
        announcement_title="Important Announcement",
        announcement_message="Very important info",
        announcement_type=AnnouncementType.ISSUE,
    )


@pytest.fixture()
def glossary_term_json():
    return load_json(GLOSSARY_TERM_JSON)


@pytest.fixture()
def glossary_category_json():
    return load_json(GLOSSARY_CATEGORY_JSON)


def test_wrong_json(glossary_json):
    with pytest.raises(ValidationError):
        AtlasGlossaryTerm(**glossary_json)


def test_asset_response(glossary_category_json):
    asset_response_json = {"referredEntities": {}, "entity": glossary_category_json}
    glossary_category = AssetResponse[AtlasGlossaryCategory](
        **asset_response_json
    ).entity
    assert glossary_category == AtlasGlossaryCategory(**glossary_category_json)


@pytest.fixture(scope="function")
def the_json(request):
    return load_json(request.param)


@pytest.mark.parametrize(
    "the_json, a_type",
    [
        ("glossary.json", AtlasGlossary),
        ("glossary_category.json", AtlasGlossaryCategory),
        ("glossary_term.json", AtlasGlossaryTerm),
        ("glossary_term2.json", AtlasGlossaryTerm),
        ("asset_mutated_response_empty.json", AssetMutationResponse),
        ("asset_mutated_response_update.json", AssetMutationResponse),
    ],
    indirect=["the_json"],
)
def test_constructor(the_json, a_type):
    asset = a_type(**the_json)
    assert not DeepDiff(
        the_json,
        json.loads(asset.json(by_alias=True, exclude_unset=True)),
        ignore_order=True,
    )


def test_has_announcement(glossary):
    assert glossary.has_announcement() == (
        bool(glossary.attributes.announcement_type)
        or bool(glossary.attributes.announcement_title)
    )


def test_set_announcement(glossary, announcement):
    glossary.set_announcement(announcement)
    assert glossary.has_announcement() is True
    assert announcement == glossary.get_announcment()


def test_create_glossary():
    glossary = AtlasGlossary(
        attributes=AtlasGlossary.Attributes(
            name="Integration Test Glossary", user_description="This a test glossary"
        )
    )
    assert "AtlasGlossary" == glossary.type_name


def test_clear_announcement(glossary, announcement):
    glossary.set_announcement(announcement)
    glossary.clear_announcment()
    assert not glossary.has_announcement()
    assert glossary.attributes.announcement_title is None
    assert glossary.attributes.announcement_type is None
    assert glossary.attributes.announcement_message is None


@pytest.mark.parametrize(
    "name, connector_type, admin_users, admin_groups, admin_roles, error",
    [
        (None, AtlanConnectorType.BIGQUERY, None, None, ["123"], ValidationError),
        ("", AtlanConnectorType.BIGQUERY, None, None, ["123"], ValueError),
        ("query", None, None, None, ["123"], ValidationError),
        ("query", AtlanConnectorType.BIGQUERY, None, None, None, ValueError),
        ("query", AtlanConnectorType.BIGQUERY, [], [], [], ValueError),
    ],
)
def test_connection_attributes_create_without_required_parameters_raises_validation_error(
    name, connector_type, admin_users, admin_groups, admin_roles, error
):
    with pytest.raises(error):
        Connection.Attributes.create(
            name=name,
            connector_type=connector_type,
            admin_users=admin_users,
            admin_groups=admin_groups,
            admin_roles=admin_roles,
        )


@pytest.mark.parametrize(
    "name, connector_type, admin_users, admin_groups, admin_roles",
    [
        ("query", AtlanConnectorType.BIGQUERY, ["bob"], None, None),
        ("query", AtlanConnectorType.BIGQUERY, None, ["bob"], None),
        ("query", AtlanConnectorType.BIGQUERY, None, None, ["bob"]),
        ("query", AtlanConnectorType.BIGQUERY, ["bob"], ["ted"], ["alice"]),
    ],
)
def test_connection_attributes_create_with_required_parameters(
    name, connector_type, admin_users, admin_groups, admin_roles
):
    c = Connection.Attributes.create(
        name=name,
        connector_type=connector_type,
        admin_users=admin_users,
        admin_groups=admin_groups,
        admin_roles=admin_roles,
    )
    assert c.qualified_name
    assert c.qualified_name <= connector_type.to_qualified_name()
    assert c.connector_name == connector_type.value
    assert c.category == connector_type.category.value
    assert c.admin_roles == admin_roles
    assert c.admin_users == admin_users
    assert c.admin_groups == admin_groups


@pytest.mark.parametrize(
    "name, connector_type, admin_users, admin_groups, admin_roles",
    [("somequery", AtlanConnectorType.BIGQUERY, ["bob"], ["ted"], ["alice"])],
)
def test_connection_create_with_required_parameters(
    name, connector_type, admin_users, admin_groups, admin_roles
):
    c = Connection.create(
        name=name,
        connector_type=connector_type,
        admin_users=admin_users,
        admin_groups=admin_groups,
        admin_roles=admin_roles,
    )
    assert c.attributes.qualified_name
    assert c.attributes.qualified_name <= connector_type.to_qualified_name()
    assert c.attributes.connector_name == connector_type.value
    assert c.attributes.category == connector_type.category.value
    assert c.attributes.admin_roles == admin_roles
    assert c.attributes.admin_users == admin_users
    assert c.attributes.admin_groups == admin_groups


@pytest.mark.parametrize(
    "name, connector_type, admin_users, admin_groups, admin_roles, error",
    [
        (None, AtlanConnectorType.BIGQUERY, None, None, ["123"], ValidationError),
        ("", AtlanConnectorType.BIGQUERY, None, None, ["123"], ValueError),
        ("SomeQuery", None, None, None, ["123"], ValidationError),
        ("SomeQuery", AtlanConnectorType.BIGQUERY, None, None, None, ValueError),
        ("SomeQuery", AtlanConnectorType.BIGQUERY, [], [], [], ValueError),
    ],
)
def test_connection_create_without_required_parameters_raises_validation_error(
    name, connector_type, admin_users, admin_groups, admin_roles, error
):
    with pytest.raises(error):
        Connection.create(
            name=name,
            connector_type=connector_type,
            admin_users=admin_users,
            admin_groups=admin_groups,
            admin_roles=admin_roles,
        )


@pytest.mark.parametrize(
    "name, qualified_name, connector_name, category, admin_users, admin_groups, admin_roles, msg",
    [
        (
            "Bob",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            AtlanConnectorType.BIGQUERY.value,
            AtlanConnectorType.BIGQUERY.category.value,
            None,
            None,
            None,
            "One of admin_user, admin_groups or admin_roles is required",
        ),
        (
            "Bob",
            "",
            AtlanConnectorType.BIGQUERY.value,
            AtlanConnectorType.BIGQUERY.category.value,
            ["Bob"],
            None,
            None,
            "qualified_name is required",
        ),
        (
            "Bob",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            AtlanConnectorType.BIGQUERY.value,
            "",
            ["Bob"],
            None,
            None,
            "category is required",
        ),
        (
            "Bob",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            "",
            AtlanConnectorType.BIGQUERY.category.value,
            ["Bob"],
            None,
            None,
            "connector_name is required",
        ),
        (
            "",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            AtlanConnectorType.BIGQUERY.value,
            AtlanConnectorType.BIGQUERY.category.value,
            ["Bob"],
            None,
            None,
            "name is required",
        ),
    ],
)
def test_connection_validate_required_when_fields_missing_raises_value_error(
    name,
    qualified_name,
    connector_name,
    category,
    admin_users,
    admin_groups,
    admin_roles,
    msg,
):
    a = Connection.Attributes(
        name=name,
        qualified_name=qualified_name,
        connector_name=connector_name,
        category=category,
        admin_users=admin_users,
        admin_groups=admin_groups,
        admin_roles=admin_roles,
    )
    with pytest.raises(ValueError) as ve:
        a.validate_required()
    assert str(ve.value) == msg


@pytest.mark.parametrize(
    "name, qualified_name, connector_name, category, admin_users, admin_groups, admin_roles",
    [
        (
            "Bob",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            AtlanConnectorType.BIGQUERY.value,
            AtlanConnectorType.BIGQUERY.category.value,
            ["Bob"],
            None,
            None,
        ),
        (
            "Bob",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            AtlanConnectorType.BIGQUERY.value,
            AtlanConnectorType.BIGQUERY.category.value,
            None,
            ["Bob"],
            None,
        ),
        (
            "Bob",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            AtlanConnectorType.BIGQUERY.value,
            AtlanConnectorType.BIGQUERY.category.value,
            None,
            None,
            ["Bob"],
        ),
    ],
)
def test_connection_validate_required_when_fields_are_present(
    name,
    qualified_name,
    connector_name,
    category,
    admin_users,
    admin_groups,
    admin_roles,
):
    a = Connection.Attributes(
        name=name,
        qualified_name=qualified_name,
        connector_name=connector_name,
        category=category,
        admin_users=admin_users,
        admin_groups=admin_groups,
        admin_roles=admin_roles,
    )
    a.validate_required()


@pytest.mark.parametrize(
    "name, connection_qualified_name, error",
    [
        (None, "default/snowflake/1673868111909", ValidationError),
        ("DB", None, ValidationError),
        ("", "default/snowflake/1673868111909", ValueError),
        ("DB", "", ValueError),
        ("DB", "default/snwflake/1673868111909", ValueError),
        ("DB", "snowflake/1673868111909", ValueError),
        ("DB", "default/snwflake", ValueError),
    ],
)
def test_database_attributes_create_without_required_parameters_raises_validation_error(
    name, connection_qualified_name, error
):
    with pytest.raises(error):
        Database.Attributes.create(
            name=name, connection_qualified_name=connection_qualified_name
        )


@pytest.mark.parametrize(
    "name, connection_qualified_name",
    [
        ("TestDB", "default/snowflake/1673868111909"),
    ],
)
def test_database_attributes_create_with_required_parameters(
    name, connection_qualified_name
):

    attributes = Database.Attributes.create(
        name=name, connection_qualified_name=connection_qualified_name
    )
    assert attributes.name == name
    assert attributes.connection_qualified_name == connection_qualified_name
    assert attributes.qualified_name == f"{connection_qualified_name}/{name}"
    assert attributes.connector_name == connection_qualified_name.split("/")[1]


@pytest.mark.parametrize(
    "name, connection_qualified_name, error",
    [
        (None, "default/snowflake/1673868111909", ValidationError),
        ("DB", None, ValidationError),
        ("", "default/snowflake/1673868111909", ValueError),
        ("DB", "", ValueError),
        ("DB", "default/snwflake/1673868111909", ValueError),
        ("DB", "snowflake/1673868111909", ValueError),
        ("DB", "default/snwflake", ValueError),
    ],
)
def test_database_create_without_required_parameters_raises_validation_error(
    name, connection_qualified_name, error
):
    with pytest.raises(error):
        Database.create(name=name, connection_qualified_name=connection_qualified_name)


@pytest.mark.parametrize(
    "name, connection_qualified_name",
    [
        ("TestDB", "default/snowflake/1673868111909"),
    ],
)
def test_database_create_with_required_parameters(name, connection_qualified_name):

    database = Database.create(
        name=name, connection_qualified_name=connection_qualified_name
    )
    attributes = database.attributes
    assert attributes.name == name
    assert attributes.connection_qualified_name == connection_qualified_name
    assert attributes.qualified_name == f"{connection_qualified_name}/{name}"
    assert attributes.connector_name == connection_qualified_name.split("/")[1]
