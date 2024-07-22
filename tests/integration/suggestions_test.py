from time import sleep
from typing import Callable, Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    Asset,
    AtlasGlossary,
    AtlasGlossaryTerm,
    Column,
    Connection,
    Database,
    Schema,
    Table,
    View,
)
from pyatlan.model.core import AtlanTag, AtlanTagName
from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.group import AtlanGroup
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.suggestions import Suggestions
from pyatlan.model.typedef import AtlanTagDef
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection
from tests.integration.glossary_test import create_term

PREFIX = TestId.make_unique("Trident")

CONNECTOR_TYPE = AtlanConnectorType.ROCKSET
CONNECTION_NAME = PREFIX
DESCRIPTION = "Automated testing of the Python SDK."
SYSTEM_DESCRIPTION = DESCRIPTION + "(system)"

DATABASE_NAME = PREFIX + "_db"
SCHEMA_NAME1 = PREFIX + "_schema1"
SCHEMA_NAME2 = PREFIX + "_schema2"
SCHEMA_NAME3 = PREFIX + "_schema3"
TABLE_NAME = PREFIX + "_table"
VIEW_NAME = PREFIX + "_view"
COLUMN_NAME1 = PREFIX + "_col1"

ATLAN_TAG_NAME1 = PREFIX + "tag1"
ATLAN_TAG_NAME2 = PREFIX + "tag2"

TERM_NAME1 = PREFIX + "term1"
TERM_NAME2 = PREFIX + "term2"


@pytest.fixture(scope="module")
def wait_for_consistency():
    """
    Wait for suggestions to be indexed
    """
    sleep(15)


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=CONNECTION_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def database(
    client: AtlanClient,
    connection: Connection,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    to_create = Database.creator(
        name=DATABASE_NAME, connection_qualified_name=connection.qualified_name
    )
    result = upsert(to_create)
    assert result
    database = result.assets_created(asset_type=Database)[0]
    assert database.connector_name == CONNECTOR_TYPE
    yield database


@pytest.fixture(scope="module")
def schema1(
    client: AtlanClient,
    database: Database,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    assert database and database.qualified_name
    schema1 = Schema.creator(
        name=SCHEMA_NAME1,
        database_qualified_name=database.qualified_name,
    )
    response = upsert(schema1)
    assert (schemas := response.assets_created(asset_type=Schema))
    assert len(schemas) == 1 and schemas[0].database_name == DATABASE_NAME
    yield schema1


@pytest.fixture(scope="module")
def schema2(
    client: AtlanClient,
    database: Database,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    assert database and database.qualified_name
    schema2 = Schema.creator(
        name=SCHEMA_NAME2,
        database_qualified_name=database.qualified_name,
    )
    response = upsert(schema2)
    assert (schemas := response.assets_created(asset_type=Schema))
    assert len(schemas) == 1 and schemas[0].database_name == DATABASE_NAME
    yield schema2


@pytest.fixture(scope="module")
def schema3(
    client: AtlanClient,
    database: Database,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    assert database and database.qualified_name
    schema3 = Schema.creator(
        name=SCHEMA_NAME3,
        database_qualified_name=database.qualified_name,
    )
    response = upsert(schema3)
    assert (schemas := response.assets_created(asset_type=Schema))
    assert len(schemas) == 1
    yield schema3


@pytest.fixture(scope="module")
def table1(
    client: AtlanClient,
    schema1: Schema,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    assert schema1 and schema1.qualified_name
    table = Table.creator(
        name=TABLE_NAME,
        schema_qualified_name=schema1.qualified_name,
    )
    response = upsert(table)
    assert (tables := response.assets_created(asset_type=Table))
    assert len(tables) == 1
    yield tables[0]


@pytest.fixture(scope="module")
def table2(
    client: AtlanClient,
    schema2: Schema,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    assert schema2 and schema2.qualified_name
    table = Table.creator(
        name=TABLE_NAME,
        schema_qualified_name=schema2.qualified_name,
    )
    response = upsert(table)
    assert (tables := response.assets_created(asset_type=Table))
    assert len(tables) == 1
    yield tables[0]


@pytest.fixture(scope="module")
def view1(
    client: AtlanClient,
    schema1: Schema,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    assert schema1 and schema1.qualified_name
    view = View.creator(
        name=VIEW_NAME,
        schema_qualified_name=schema1.qualified_name,
    )
    response = upsert(view)
    assert (views := response.assets_created(asset_type=View))
    assert len(views) == 1
    yield views[0]


@pytest.fixture(scope="module")
def view2(
    client: AtlanClient,
    schema2: Schema,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    assert schema2 and schema2.qualified_name
    view = View.creator(
        name=VIEW_NAME,
        schema_qualified_name=schema2.qualified_name,
    )
    response = upsert(view)
    assert (views := response.assets_created(asset_type=View))
    assert len(views) == 1
    yield views[0]


@pytest.fixture(scope="module")
def t1c1(
    client: AtlanClient,
    table1: Table,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    assert table1 and table1.qualified_name
    column = Column.creator(
        name=COLUMN_NAME1,
        parent_qualified_name=table1.qualified_name,
        parent_type=Table,
        order=1,
    )
    response = upsert(column)
    assert (columns := response.assets_created(asset_type=Column))
    assert len(columns) == 1
    yield columns[0]


@pytest.fixture(scope="module")
def t2c1(
    client: AtlanClient,
    table2: Table,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    assert table2 and table2.qualified_name
    column = Column.creator(
        name=COLUMN_NAME1,
        parent_qualified_name=table2.qualified_name,
        parent_type=Table,
        order=1,
    )
    response = upsert(column)
    assert (columns := response.assets_created(asset_type=Column))
    assert len(columns) == 1
    yield columns[0]


@pytest.fixture(scope="module")
def v1c1(
    client: AtlanClient,
    view1: View,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    assert view1 and view1.qualified_name
    column = Column.creator(
        name=COLUMN_NAME1,
        parent_qualified_name=view1.qualified_name,
        parent_type=View,
        order=1,
    )
    response = upsert(column)
    assert (columns := response.assets_created(asset_type=Column))
    assert len(columns) == 1
    yield columns[0]


@pytest.fixture(scope="module")
def v2c1(
    client: AtlanClient,
    view2: View,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    assert view2 and view2.qualified_name
    column = Column.creator(
        name=COLUMN_NAME1,
        parent_qualified_name=view2.qualified_name,
        parent_type=View,
        order=1,
    )
    response = upsert(column)
    assert (columns := response.assets_created(asset_type=Column))
    assert len(columns) == 1
    yield columns[0]


@pytest.fixture(scope="module")
def create_atlan_tag1(
    client: AtlanClient,
    table1: Table,
    table3: Table,
    t1c1: Column,
    v2c1: Column,
) -> Generator[AtlanTagDef, None, None]:
    assert table1.qualified_name and table3.qualified_name
    assert t1c1.qualified_name and v2c1.qualified_name
    cls = AtlanTagDef.create(
        name=ATLAN_TAG_NAME1,
    )
    yield client.typedef.create(cls).atlan_tag_defs[0]
    client.asset.remove_atlan_tag(
        asset_type=Table,
        qualified_name=table1.qualified_name,
        atlan_tag_name=ATLAN_TAG_NAME1,
    )
    client.asset.remove_atlan_tag(
        asset_type=Table,
        qualified_name=table3.qualified_name,
        atlan_tag_name=ATLAN_TAG_NAME1,
    )
    client.asset.remove_atlan_tag(
        asset_type=Column,
        qualified_name=t1c1.qualified_name,
        atlan_tag_name=ATLAN_TAG_NAME1,
    )
    client.asset.remove_atlan_tag(
        asset_type=Column,
        qualified_name=v2c1.qualified_name,
        atlan_tag_name=ATLAN_TAG_NAME1,
    )
    client.typedef.purge(ATLAN_TAG_NAME1, typedef_type=AtlanTagDef)


@pytest.fixture(scope="module")
def create_atlan_tag2(
    client: AtlanClient,
    table1: Table,
    table3: Table,
    t1c1: Column,
    t2c1: Column,
    v1c1: Column,
    v2c1: Column,
) -> Generator[AtlanTagDef, None, None]:
    assert table1.qualified_name and table3.qualified_name
    assert t1c1.qualified_name and t2c1.qualified_name
    assert v1c1.qualified_name and v2c1.qualified_name
    cls = AtlanTagDef.create(
        name=ATLAN_TAG_NAME2,
    )
    yield client.typedef.create(cls).atlan_tag_defs[0]
    client.asset.remove_atlan_tag(
        asset_type=Table,
        qualified_name=table1.qualified_name,
        atlan_tag_name=ATLAN_TAG_NAME2,
    )
    client.asset.remove_atlan_tag(
        asset_type=Table,
        qualified_name=table3.qualified_name,
        atlan_tag_name=ATLAN_TAG_NAME2,
    )
    client.asset.remove_atlan_tag(
        asset_type=Column,
        qualified_name=t1c1.qualified_name,
        atlan_tag_name=ATLAN_TAG_NAME2,
    )
    client.asset.remove_atlan_tag(
        asset_type=Column,
        qualified_name=v1c1.qualified_name,
        atlan_tag_name=ATLAN_TAG_NAME2,
    )
    client.asset.remove_atlan_tag(
        asset_type=Column,
        qualified_name=t2c1.qualified_name,
        atlan_tag_name=ATLAN_TAG_NAME2,
    )
    client.asset.remove_atlan_tag(
        asset_type=Column,
        qualified_name=v2c1.qualified_name,
        atlan_tag_name=ATLAN_TAG_NAME2,
    )
    client.typedef.purge(ATLAN_TAG_NAME2, typedef_type=AtlanTagDef)


@pytest.fixture(scope="module")
def term1(
    client: AtlanClient,
    table1: Table,
    table3: Table,
    t1c1: Column,
    glossary: AtlasGlossary,
) -> Generator[AtlasGlossaryTerm, None, None]:
    assert table1.qualified_name and table3.qualified_name and t1c1.qualified_name
    assert glossary and glossary.guid
    t = create_term(client, name=TERM_NAME2, glossary_guid=glossary.guid)
    yield t
    client.asset.remove_terms(
        asset_type=Table,
        qualified_name=table1.qualified_name,
        terms=[AtlasGlossaryTerm.ref_by_guid(t.guid)],
    )
    client.asset.remove_terms(
        asset_type=Table,
        qualified_name=table3.qualified_name,
        terms=[AtlasGlossaryTerm.ref_by_guid(t.guid)],
    )
    client.asset.remove_terms(
        asset_type=Column,
        qualified_name=t1c1.qualified_name,
        terms=[AtlasGlossaryTerm.ref_by_guid(t.guid)],
    )
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


@pytest.fixture(scope="module")
def term2(
    client: AtlanClient,
    table1: Table,
    table3: Table,
    t1c1: Column,
    t2c1: Column,
    v1c1: Column,
    glossary: AtlasGlossary,
) -> Generator[AtlasGlossaryTerm, None, None]:
    assert table1.qualified_name and table3.qualified_name
    assert t1c1.qualified_name and t2c1.qualified_name
    assert v1c1.qualified_name
    assert glossary and glossary.guid
    t = create_term(client, name=TERM_NAME2, glossary_guid=glossary.guid)
    yield t
    client.asset.remove_terms(
        asset_type=Table,
        qualified_name=table1.qualified_name,
        terms=[AtlasGlossaryTerm.ref_by_guid(t.guid)],
    )
    client.asset.remove_terms(
        asset_type=Table,
        qualified_name=table3.qualified_name,
        terms=[AtlasGlossaryTerm.ref_by_guid(t.guid)],
    )
    client.asset.remove_terms(
        asset_type=Column,
        qualified_name=t1c1.qualified_name,
        terms=[AtlasGlossaryTerm.ref_by_guid(t.guid)],
    )
    client.asset.remove_terms(
        asset_type=Column,
        qualified_name=t2c1.qualified_name,
        terms=[AtlasGlossaryTerm.ref_by_guid(t.guid)],
    )
    client.asset.remove_terms(
        asset_type=Column,
        qualified_name=v1c1.qualified_name,
        terms=[AtlasGlossaryTerm.ref_by_guid(t.guid)],
    )
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


@pytest.fixture(scope="module")
def owner_group(
    client: AtlanClient,
) -> Generator[AtlanGroup, None, None]:
    to_create = AtlanGroup.create(PREFIX)
    response = client.group.create(group=to_create)
    assert response
    group = client.group.get_by_name(PREFIX)
    assert group and len(group) == 1
    assert group[0].id
    yield group[0]
    client.group.purge(group[0].id)


def test_connection(client: AtlanClient, connection: Connection):
    results = client.asset.find_connections_by_name(
        name=CONNECTION_NAME, connector_type=CONNECTOR_TYPE
    )
    assert results and len(results) == 1
    assert results[0].guid == connection.guid
    assert results[0].qualified_name == connection.qualified_name


def test_schemas(
    schema1: Schema,
    schema2: Schema,
    schema3: Schema,
):
    assert schema1.connector_name == CONNECTOR_TYPE
    assert schema1.database_name == DATABASE_NAME

    assert schema2.connector_name == CONNECTOR_TYPE
    assert schema2.database_name == DATABASE_NAME

    assert schema3.connector_name == CONNECTOR_TYPE
    assert schema3.database_name == DATABASE_NAME


@pytest.fixture(scope="module")
def table3(
    client: AtlanClient,
    schema3: Schema,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    assert schema3 and schema3.qualified_name
    table = Table.creator(
        name=TABLE_NAME,
        schema_qualified_name=schema3.qualified_name,
    )
    response = upsert(table)
    assert (tables := response.assets_created(asset_type=Table))
    assert len(tables) == 1
    yield tables[0]
    # delete_asset(client, guid=tables[0].guid, asset_type=Table)


def test_tables(
    table1: Table,
    table2: Table,
    table3: Table,
    database: Database,
    connection: Connection,
):
    assert table1.connector_name == CONNECTOR_TYPE
    assert table1.schema_name == SCHEMA_NAME1
    assert table1.database_name == DATABASE_NAME
    assert table1.database_qualified_name == database.qualified_name
    assert table1.connection_qualified_name == connection.qualified_name

    assert table2.connector_name == CONNECTOR_TYPE
    assert table2.schema_name == SCHEMA_NAME2
    assert table2.database_name == DATABASE_NAME
    assert table2.database_qualified_name == database.qualified_name
    assert table2.connection_qualified_name == connection.qualified_name

    assert table3.connector_name == CONNECTOR_TYPE
    assert table3.schema_name == SCHEMA_NAME3
    assert table3.database_name == DATABASE_NAME
    assert table3.database_qualified_name == database.qualified_name
    assert table3.connection_qualified_name == connection.qualified_name


def test_views(
    view1: View,
    view2: View,
    database: Database,
    connection: Connection,
):
    assert view1.connector_name == CONNECTOR_TYPE
    assert view1.schema_name == SCHEMA_NAME1
    assert view1.database_name == DATABASE_NAME
    assert view1.database_qualified_name == database.qualified_name
    assert view1.connection_qualified_name == connection.qualified_name

    assert view2.connector_name == CONNECTOR_TYPE
    assert view2.schema_name == SCHEMA_NAME2
    assert view2.database_name == DATABASE_NAME
    assert view2.database_qualified_name == database.qualified_name
    assert view2.connection_qualified_name == connection.qualified_name


def test_column1(
    connection: Connection,
    t1c1: Column,
    t2c1: Column,
    v1c1: Column,
    v2c1: Column,
    schema1: Schema,
    schema2: Schema,
    database: Database,
):

    # Table column 1
    assert t1c1.connector_name == CONNECTOR_TYPE
    assert t1c1.table_name == TABLE_NAME
    assert t1c1.schema_name == SCHEMA_NAME1
    assert t1c1.schema_qualified_name == schema1.qualified_name
    assert t1c1.database_name == DATABASE_NAME
    assert t1c1.database_qualified_name == database.qualified_name
    assert t1c1.connection_qualified_name == connection.qualified_name

    assert t2c1.connector_name == CONNECTOR_TYPE
    assert t2c1.table_name == TABLE_NAME
    assert t2c1.schema_name == SCHEMA_NAME2
    assert t2c1.schema_qualified_name == schema2.qualified_name
    assert t2c1.database_name == DATABASE_NAME
    assert t2c1.database_qualified_name == database.qualified_name
    assert t2c1.connection_qualified_name == connection.qualified_name

    # View column 1
    assert v1c1.connector_name == CONNECTOR_TYPE
    assert v1c1.view_name == VIEW_NAME
    assert v1c1.schema_name == SCHEMA_NAME1
    assert v1c1.schema_qualified_name == schema1.qualified_name
    assert v1c1.database_name == DATABASE_NAME
    assert v1c1.database_qualified_name == database.qualified_name
    assert v1c1.connection_qualified_name == connection.qualified_name

    assert v2c1.connector_name == CONNECTOR_TYPE
    assert v2c1.view_name == VIEW_NAME
    assert v2c1.schema_name == SCHEMA_NAME2
    assert v2c1.schema_qualified_name == schema2.qualified_name
    assert v2c1.database_name == DATABASE_NAME
    assert v2c1.database_qualified_name == database.qualified_name
    assert v2c1.connection_qualified_name == connection.qualified_name


def test_update_table1(
    client: AtlanClient,
    table1: Table,
    owner_group: AtlanGroup,
    create_atlan_tag1: AtlanTagDef,
    create_atlan_tag2: AtlanTagDef,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
):
    assert table1 and table1.qualified_name
    assert owner_group and owner_group.name
    to_update = Table.updater(qualified_name=table1.qualified_name, name=TABLE_NAME)
    to_update.owner_groups = {owner_group.name}
    to_update.description = SYSTEM_DESCRIPTION
    to_update.user_description = DESCRIPTION
    to_update.atlan_tags = [
        AtlanTag(
            type_name=AtlanTagName(ATLAN_TAG_NAME1),
            propagate=False,
        ),
        AtlanTag(
            type_name=AtlanTagName(ATLAN_TAG_NAME2),
            propagate=False,
        ),
    ]
    to_update.assigned_terms = [
        AtlasGlossaryTerm.ref_by_guid(term1.guid),
        AtlasGlossaryTerm.ref_by_guid(term2.guid),
    ]

    response = client.asset.save(to_update, replace_atlan_tags=True)
    assert response and response.mutated_entities
    assert (
        response.mutated_entities.UPDATE and len(response.mutated_entities.UPDATE) == 3
    )  # table + 2x terms
    expected_types = {asset.type_name for asset in response.mutated_entities.UPDATE}
    assert expected_types == {Table.__name__, AtlasGlossaryTerm.__name__}
    assert (tables := response.assets_updated(asset_type=Table))
    assert len(tables) == 1
    assert tables[0].owner_groups and len(tables[0].owner_groups) == 1
    assert tables[0].owner_groups == {owner_group.name}


def test_update_table3(
    client: AtlanClient,
    table3: Table,
    owner_group: AtlanGroup,
    create_atlan_tag1: AtlanTagDef,
    create_atlan_tag2: AtlanTagDef,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
):
    assert table3 and table3.qualified_name
    assert owner_group and owner_group.name
    # Updating `table3.name` with `VIEW_NAME` used in
    # `test_suggestions_across_types` to view table suggestions for `view1`
    to_update = Table.updater(qualified_name=table3.qualified_name, name=VIEW_NAME)
    to_update.owner_groups = {owner_group.name}
    to_update.description = SYSTEM_DESCRIPTION
    to_update.user_description = DESCRIPTION
    to_update.atlan_tags = [
        AtlanTag(
            type_name=AtlanTagName(ATLAN_TAG_NAME1),
            propagate=False,
        ),
        AtlanTag(
            type_name=AtlanTagName(ATLAN_TAG_NAME2),
            propagate=False,
        ),
    ]
    to_update.assigned_terms = [
        AtlasGlossaryTerm.ref_by_guid(term1.guid),
        AtlasGlossaryTerm.ref_by_guid(term2.guid),
    ]

    response = client.asset.save(to_update, replace_atlan_tags=True)

    assert response and response.mutated_entities
    assert (
        response.mutated_entities.UPDATE and len(response.mutated_entities.UPDATE) == 3
    )  # table + 2x terms
    expected_types = {asset.type_name for asset in response.mutated_entities.UPDATE}
    assert expected_types == {Table.__name__, AtlasGlossaryTerm.__name__}
    assert (tables := response.assets_updated(asset_type=Table))
    assert len(tables) == 1
    assert tables[0].owner_groups and len(tables[0].owner_groups) == 1
    assert tables[0].owner_groups == {owner_group.name}


def test_update_table1_column1(
    client: AtlanClient,
    owner_group: AtlanGroup,
    t1c1: Column,
    create_atlan_tag1: AtlanTagDef,
    create_atlan_tag2: AtlanTagDef,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
):
    assert t1c1 and t1c1.qualified_name
    assert owner_group and owner_group.name
    to_update = Column.updater(qualified_name=t1c1.qualified_name, name=COLUMN_NAME1)
    to_update.owner_groups = {owner_group.name}
    to_update.description = SYSTEM_DESCRIPTION
    to_update.user_description = DESCRIPTION
    to_update.atlan_tags = [
        AtlanTag(
            type_name=AtlanTagName(ATLAN_TAG_NAME1),
            propagate=False,
        ),
        AtlanTag(
            type_name=AtlanTagName(ATLAN_TAG_NAME2),
            propagate=False,
        ),
    ]
    to_update.assigned_terms = [
        AtlasGlossaryTerm.ref_by_guid(term1.guid),
        AtlasGlossaryTerm.ref_by_guid(term2.guid),
    ]

    response = client.asset.save(to_update, replace_atlan_tags=True)

    assert response and response.mutated_entities
    assert (
        response.mutated_entities.UPDATE and len(response.mutated_entities.UPDATE) == 3
    )  # column + 2x terms
    expected_types = {asset.type_name for asset in response.mutated_entities.UPDATE}
    assert expected_types == {Column.__name__, AtlasGlossaryTerm.__name__}
    assert (columns := response.assets_updated(asset_type=Column))
    assert len(columns) == 1
    assert columns[0].owner_groups and len(columns[0].owner_groups) == 1
    assert columns[0].owner_groups == {owner_group.name}


def test_update_view1_column1(
    client: AtlanClient,
    owner_group: AtlanGroup,
    v1c1: Column,
    create_atlan_tag1: AtlanTagDef,
    create_atlan_tag2: AtlanTagDef,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
):
    assert v1c1 and v1c1.qualified_name
    assert owner_group and owner_group.name
    to_update = Column.updater(qualified_name=v1c1.qualified_name, name=COLUMN_NAME1)
    to_update.owner_groups = {owner_group.name}
    to_update.description = SYSTEM_DESCRIPTION
    to_update.user_description = DESCRIPTION
    to_update.atlan_tags = [
        AtlanTag(
            type_name=AtlanTagName(ATLAN_TAG_NAME2),
            propagate=False,
        ),
    ]
    to_update.assigned_terms = [
        AtlasGlossaryTerm.ref_by_guid(term2.guid),
    ]

    response = client.asset.save(to_update, replace_atlan_tags=True)

    assert response and response.mutated_entities
    assert (
        response.mutated_entities.UPDATE and len(response.mutated_entities.UPDATE) == 2
    )  # column + term
    expected_types = {asset.type_name for asset in response.mutated_entities.UPDATE}
    assert expected_types == {Column.__name__, AtlasGlossaryTerm.__name__}
    assert (columns := response.assets_updated(asset_type=Column))
    assert len(columns) == 1
    assert columns[0].owner_groups and len(columns[0].owner_groups) == 1
    assert columns[0].owner_groups == {owner_group.name}


def test_suggestions_default(
    t2c1: Column,
    owner_group: AtlanGroup,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    wait_for_consistency,
):
    assert owner_group and owner_group.name
    assert term1.qualified_name and term2.qualified_name
    response = Suggestions(includes=Suggestions.TYPE.all()).finder(t2c1).get()

    assert response
    assert response.owner_groups and len(response.owner_groups) == 1
    assert response.owner_groups[0].count == 2
    assert response.owner_groups[0].value == owner_group.name
    assert response.system_descriptions and len(response.system_descriptions) == 1
    assert response.system_descriptions[0].count == 2
    assert response.system_descriptions[0].value == SYSTEM_DESCRIPTION
    assert response.user_descriptions and len(response.user_descriptions) == 1
    assert response.user_descriptions[0].count == 2
    assert response.user_descriptions[0].value == DESCRIPTION
    assert response.atlan_tags and len(response.atlan_tags) == 2
    assert response.atlan_tags[0].count == 2
    assert response.atlan_tags[0].value == ATLAN_TAG_NAME2
    assert response.atlan_tags[1].count == 1
    assert response.atlan_tags[1].value == ATLAN_TAG_NAME1
    assert response.assigned_terms and len(response.assigned_terms) == 2
    assert response.assigned_terms[0].count == 2
    assert response.assigned_terms[0].value == AtlasGlossaryTerm.ref_by_qualified_name(
        term2.qualified_name
    )
    assert response.assigned_terms[1].count == 1
    assert response.assigned_terms[1].value == AtlasGlossaryTerm.ref_by_qualified_name(
        term1.qualified_name
    )


def test_suggestions_accross_types(
    view1: View,
    owner_group: AtlanGroup,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    wait_for_consistency,
):
    assert term1 and term1.qualified_name
    assert term2 and term2.qualified_name
    assert owner_group and owner_group.name
    response = (
        Suggestions(includes=Suggestions.TYPE.all())
        .finder(view1)
        .with_other_type("Table")
        .get()
    )

    assert response
    assert response.owner_groups and len(response.owner_groups) == 1
    assert response.owner_groups[0].count == 1
    assert response.owner_groups[0].value == owner_group.name
    assert response.system_descriptions and len(response.system_descriptions) == 1
    assert response.system_descriptions[0].count == 1
    assert response.system_descriptions[0].value == SYSTEM_DESCRIPTION
    assert response.user_descriptions and len(response.user_descriptions) == 1
    assert response.user_descriptions[0].count == 1
    assert response.user_descriptions[0].value == DESCRIPTION
    assert response.atlan_tags and len(response.atlan_tags) == 2
    assert response.atlan_tags[0].count == 1
    for tag in response.atlan_tags:
        assert tag.count == 1
        assert tag.value in {ATLAN_TAG_NAME1, ATLAN_TAG_NAME2}
    assert response.assigned_terms and len(response.assigned_terms) == 2
    for term in response.assigned_terms:
        assert term.count == 1
        assert term.value in (
            AtlasGlossaryTerm.ref_by_qualified_name(term1.qualified_name),
            AtlasGlossaryTerm.ref_by_qualified_name(term2.qualified_name),
        )


def test_limited_suggestions(
    table2: Table,
    owner_group: AtlanGroup,
    wait_for_consistency,
):
    assert owner_group and owner_group.name
    response = (
        Suggestions()
        .finder(table2)
        .include(Suggestions.TYPE.GROUP_OWNERS)
        .include(Suggestions.TYPE.SYSTEM_DESCRIPTION)
        .get()
    )

    assert response
    assert response.owner_groups and len(response.owner_groups) == 1
    assert response.owner_groups[0].count == 1
    assert response.owner_groups[0].value == owner_group.name
    assert response.system_descriptions and len(response.system_descriptions) == 1
    assert response.system_descriptions[0].count == 1
    assert response.system_descriptions[0].value == SYSTEM_DESCRIPTION
    assert response.atlan_tags == []
    assert response.assigned_terms == []
    assert response.user_descriptions == []


def test_apply_t2c1(
    t2c1: Column,
    owner_group: AtlanGroup,
    term2: AtlasGlossaryTerm,
    wait_for_consistency,
):
    assert term2 and term2.qualified_name
    assert owner_group and owner_group.name
    response = (
        Suggestions()
        .finder(t2c1)
        .include(Suggestions.TYPE.TAGS)
        .include(Suggestions.TYPE.TERMS)
        .include(Suggestions.TYPE.GROUP_OWNERS)
        .include(Suggestions.TYPE.USER_DESCRIPTION)
        .include(Suggestions.TYPE.INDIVIDUAL_OWNERS)
        .apply()
    )

    assert response and response.mutated_entities
    assert (
        response.mutated_entities.UPDATE and len(response.mutated_entities.UPDATE) == 2
    )  # column + term
    one = response.mutated_entities.UPDATE[0]
    assert one and one.owner_groups == {owner_group.name}
    # System description should be untouched (still empty)
    assert one.description is None
    assert one.user_description == DESCRIPTION
    assert one.atlan_tags and len(one.atlan_tags) == 1
    assert one.atlan_tags[0].type_name == AtlanTagName(ATLAN_TAG_NAME2)
    assert one.meanings and len(one.meanings) == 1
    assert one.meanings[0].term_guid == term2.guid


def test_apply_v2c1(
    v2c1: Column,
    wait_for_consistency,
):
    response = (
        Suggestions()
        .finder(v2c1)
        .include(Suggestions.TYPE.TAGS)
        .include(Suggestions.TYPE.SYSTEM_DESCRIPTION)
        .apply(allow_multiple=True)
    )

    assert response and response.mutated_entities
    assert (
        response.mutated_entities.UPDATE and len(response.mutated_entities.UPDATE) == 1
    )
    one = response.mutated_entities.UPDATE[0]
    assert one and one.owner_groups == set()
    # System description should be untouched (still empty)
    assert one.description is None
    assert one.meanings == []
    # System description should be applied to user description
    assert one.user_description == SYSTEM_DESCRIPTION
    assert one.atlan_tags and len(one.atlan_tags) == 2
    for tag in one.atlan_tags:
        assert tag.type_name in (
            AtlanTagName(ATLAN_TAG_NAME1),
            AtlanTagName(ATLAN_TAG_NAME2),
        )
