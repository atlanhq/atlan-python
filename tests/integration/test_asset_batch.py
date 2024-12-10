import logging
from time import sleep
from typing import Callable, Generator

import pytest

from pyatlan.client.asset import Batch
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    Asset,
    Connection,
    Database,
    MaterialisedView,
    Schema,
    Table,
    View,
)
from pyatlan.model.enums import AssetCreationHandling
from pyatlan.model.fluent_search import FluentSearch
from pyatlan.model.response import AssetMutationResponse
from pyatlan.test_utils import get_random_connector
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection

LOGGER = logging.getLogger(__name__)
PREFIX = TestId.make_unique("Batch")

CONNECTION_NAME = PREFIX
DATABASE_NAME = PREFIX + "_db"
SCHEMA_NAME = PREFIX + "_schema"
TABLE_NAME = PREFIX + "_table"
VIEW_NAME = PREFIX + "_view"
MVIEW_NAME = PREFIX + "_mview"
BATCH_MAX_SIZE = 10
CONNECTOR_TYPE = get_random_connector()
DESCRIPTION = "Automated testing of the Python SDK."


@pytest.fixture(scope="module")
def wait_for_consistency():
    """
    Wait for assets to be indexed
    """
    sleep(10)


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=CONNECTION_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def database(
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
def schema(
    client: AtlanClient,
    database: Database,
    upsert: Callable[[Asset], AssetMutationResponse],
):
    assert database and database.qualified_name
    schema1 = Schema.creator(
        name=SCHEMA_NAME,
        database_qualified_name=database.qualified_name,
    )
    response = upsert(schema1)
    assert (schemas := response.assets_created(asset_type=Schema))
    assert len(schemas) == 1 and schemas[0].database_name == DATABASE_NAME
    yield schema1


@pytest.fixture(scope="module")
def batch_table_create(
    client: AtlanClient, schema: Schema
) -> Generator[Batch, None, None]:
    assert schema and schema.qualified_name
    batch = Batch(
        client=client,
        track=True,
        max_size=BATCH_MAX_SIZE,
        capture_failures=True,
    )
    # 3 tables
    for i in range(1, 4):
        table = Table.creator(
            name=f"{TABLE_NAME}{i}",
            schema_qualified_name=schema.qualified_name,
        )
        batch.add(table)

    # 1 view
    view = View.creator(
        name=VIEW_NAME,
        schema_qualified_name=schema.qualified_name,
    )
    batch.add(view)

    # 1 materialized view
    mview = MaterialisedView.creator(
        name=MVIEW_NAME,
        schema_qualified_name=schema.qualified_name,
    )
    batch.add(mview)

    batch.flush()
    yield batch

    assert batch and batch.created
    for asset in reversed(batch.created):
        assert asset and asset.qualified_name
        created = client.asset.get_by_qualified_name(
            qualified_name=asset.qualified_name,
            asset_type=asset.__class__,
            min_ext_info=True,
            ignore_relationships=True,
        )
        assert created and created.guid
        response = client.asset.purge_by_guid(created.guid)
        if (
            not response
            or not response.mutated_entities
            or not response.mutated_entities.DELETE
        ):
            LOGGER.error(f"Failed to remove asset with GUID {asset.guid}.")


@pytest.fixture(scope="module")
def batch_table_update(
    client: AtlanClient, schema: Schema
) -> Generator[Batch, None, None]:
    assert schema and schema.qualified_name
    batch = Batch(
        client=client,
        track=True,
        max_size=BATCH_MAX_SIZE,
    )
    for i in range(1, 6):
        table = Table.creator(
            name=f"{TABLE_NAME}{i}",
            schema_qualified_name=schema.qualified_name,
        )
        batch.add(table)
    yield batch


def test_batch_create(batch_table_create: Batch, schema: Schema):
    batch = batch_table_create

    # Ensure the batch has no failures
    assert batch and batch.failures == []

    # Verify no assets were skipped or restored
    assert batch.skipped == [] and batch.num_skipped == 0
    assert batch.restored == [] and batch.num_restored == 0

    # Verify that 5 assets (3 tables, 1 view, 1 materialized view) were created
    assert batch.created and len(batch.created) == 5 and batch.num_created == 5
    assert all(
        asset.type_name in {Table.__name__, View.__name__, MaterialisedView.__name__}
        for asset in batch.created
    )

    # Ensure the schema was updated
    assert batch.updated and len(batch.updated) == 1 and batch.num_updated == 1
    assert batch.updated[0].qualified_name == schema.qualified_name


@pytest.mark.order(after="test_batch_create")
def test_batch_update(
    wait_for_consistency, client: AtlanClient, batch_table_create: Batch
):
    # Table with view qn / mview qn
    # 1. table_view_agnostic and update only -- update -- table? -> view? -> mview
    # 2. not table_view_agnostic and update only -- skip -- table? -> view? -> mview? - not found
    # 3. not table_view_agnostic and not update only -- create -- new table (with view qn)

    create_batch = batch_table_create
    for asset in create_batch.created:
        if asset.name == f"{TABLE_NAME}1":
            table1 = asset
        elif asset.name == VIEW_NAME:
            view = asset
        elif asset.name == MVIEW_NAME:
            mview = asset

    assert table1 and table1.qualified_name
    assert view and view.qualified_name
    assert mview and mview.qualified_name

    # An asset in the batch marked as a table will attempt
    # to match a view or mview if not found as a table, and vice versa
    # [sub-test-1]: Table with view qn (table_view_agnostic=True, update_only=True)
    # Expect the view to be updated since `table_view_agnostic=True` and `update_only=True`
    batch1 = Batch(
        client=client,
        track=True,
        update_only=True,
        table_view_agnostic=True,
        max_size=BATCH_MAX_SIZE,
    )
    SUB_TEST1_DESCRIPTION = f"[sub-test1] {DESCRIPTION}"

    table = Table.updater(qualified_name=view.qualified_name, name=view.name)
    table.user_description = SUB_TEST1_DESCRIPTION
    batch1.add(table)
    batch1.flush()

    # Validate that the view was updated
    assert batch1.num_updated == 1
    assert batch1.num_created == 0
    assert batch1.num_skipped == 0
    assert batch1.num_restored == 0

    # Wait for assets to be indexed
    sleep(5)
    # Make sure user description should be updated on view
    results = (
        FluentSearch()
        .where(Asset.TYPE_NAME.eq(View.__name__))
        .where(Asset.QUALIFIED_NAME.eq(view.qualified_name))
        .include_on_results(Asset.USER_DESCRIPTION)
        .execute(client=client)
    )
    assert results and results.count == 1
    assert results.current_page() and len(results.current_page()) == 1
    updated_view = results.current_page()[0]
    assert updated_view.qualified_name == view.qualified_name
    assert updated_view.user_description == SUB_TEST1_DESCRIPTION

    # [sub-test-11]: Table with mview qn (table_view_agnostic=True, update_only=True)
    # Expect the mview to be updated since `table_view_agnostic=True` and `update_only=True`
    batch11 = Batch(
        client=client,
        track=True,
        update_only=True,
        table_view_agnostic=True,
        max_size=BATCH_MAX_SIZE,
    )
    SUB_TEST11_DESCRIPTION = f"[sub-test11] {DESCRIPTION}"

    table = Table.updater(qualified_name=mview.qualified_name, name=mview.name)
    table.user_description = SUB_TEST11_DESCRIPTION
    batch11.add(table)
    batch11.flush()

    # Validate that the mview was updated
    assert batch11.num_updated == 1
    assert batch11.num_created == 0
    assert batch11.num_skipped == 0
    assert batch11.num_restored == 0

    # Wait for assets to be indexed
    sleep(5)
    # Make sure user description should be updated on mview
    results = (
        FluentSearch()
        .where(Asset.TYPE_NAME.eq(MaterialisedView.__name__))
        .where(Asset.QUALIFIED_NAME.eq(mview.qualified_name))
        .include_on_results(Asset.USER_DESCRIPTION)
        .execute(client=client)
    )
    assert results and results.count == 1
    assert results.current_page() and len(results.current_page()) == 1
    updated_mview = results.current_page()[0]
    assert updated_mview.qualified_name == mview.qualified_name
    assert updated_mview.user_description == SUB_TEST11_DESCRIPTION

    # [sub-test-2]: Table with view qn (table_view_agnostic=False, update_only=True)
    # Expect the operation to be skipped since a table with the view's qualified name does not exist
    batch2 = Batch(
        client=client,
        track=True,
        update_only=True,
        table_view_agnostic=False,
        max_size=BATCH_MAX_SIZE,
    )
    SUB_TEST2_DESCRIPTION = f"[sub-test2] {DESCRIPTION}"

    table = Table.updater(qualified_name=view.qualified_name, name=view.name)
    table.user_description = SUB_TEST2_DESCRIPTION
    batch2.add(table)
    batch2.flush()

    # Neither create or update (since table_view_agnostic = False)
    assert batch2.num_skipped == 1
    assert batch2.num_created == 0
    assert batch2.num_updated == 0
    assert batch2.num_restored == 0

    # [sub-test-3]: Table with view qn (table_view_agnostic=False, update_only=False)
    # Expect a new table to be created with the view's qualified name
    batch3 = Batch(
        client=client,
        track=True,
        update_only=False,
        table_view_agnostic=False,
        max_size=BATCH_MAX_SIZE,
    )
    SUB_TEST3_DESCRIPTION = f"[sub-test3] {DESCRIPTION}"

    table = Table.updater(qualified_name=view.qualified_name, name=view.name)
    table.user_description = SUB_TEST3_DESCRIPTION
    batch3.add(table)
    batch3.flush()

    # Validate that a new table with view qn was created
    assert batch3.num_created == 1
    assert batch3.num_skipped == 0
    assert batch3.num_updated == 0
    assert batch3.num_restored == 0

    # Wait for assets to be indexed
    sleep(5)
    results = (
        FluentSearch()
        .where(Asset.TYPE_NAME.eq(Table.__name__))
        .where(Asset.QUALIFIED_NAME.eq(view.qualified_name))
        .include_on_results(Asset.USER_DESCRIPTION)
        .execute(client=client)
    )

    assert results and results.count == 1
    assert results.current_page() and len(results.current_page()) == 1
    created_table = results.current_page()[0]
    assert (
        created_table
        and created_table.guid
        and created_table.qualified_name == view.qualified_name
    )
    # Verify the new table was created and has the updated user description
    assert created_table.user_description == SUB_TEST3_DESCRIPTION

    # Cleanup: Delete the newly created table
    response = client.asset.purge_by_guid(created_table.guid)
    assert response.mutated_entities and response.mutated_entities.DELETE

    # Table with table qn
    # 4. case_insensitive and update_only - update
    # 5. not case_insensitive and update_only - update
    # 6. not case_insensitive and update_only (same operation) - restore
    # 7. case_insensitive and not update_only - create

    # [sub-test-4]: Table with table qn [lowercase] (case_insensitive=True, update_only=True)
    # Expect the table to be updated
    batch4 = Batch(
        client=client,
        track=True,
        update_only=True,
        case_insensitive=True,
        max_size=BATCH_MAX_SIZE,
    )
    SUB_TEST4_DESCRIPTION = f"[sub-test4] {DESCRIPTION}"

    table = Table.updater(
        qualified_name=table1.qualified_name.lower(), name=table1.name
    )
    table.user_description = SUB_TEST4_DESCRIPTION
    batch4.add(table)
    batch4.flush()

    # Validate that the table was updated
    assert batch4.num_updated == 1
    assert batch4.num_created == 0
    assert batch4.num_skipped == 0
    assert batch4.num_restored == 0

    # Wait for assets to be indexed
    sleep(5)
    results = (
        FluentSearch()
        .where(Asset.TYPE_NAME.eq(Table.__name__))
        .where(Asset.QUALIFIED_NAME.eq(table1.qualified_name))
        .include_on_results(Asset.USER_DESCRIPTION)
        .execute(client=client)
    )

    assert results and results.count == 1
    assert results.current_page() and len(results.current_page()) == 1
    updated_table = results.current_page()[0]
    assert (
        updated_table
        and updated_table.guid
        and updated_table.qualified_name == table1.qualified_name
    )
    assert updated_table.user_description == SUB_TEST4_DESCRIPTION

    # [sub-test-5]: Table with table qn (case_insensitive=False, update_only=True)
    # Expect the table to be updated
    batch5 = Batch(
        client=client,
        track=True,
        update_only=True,
        case_insensitive=False,
        max_size=BATCH_MAX_SIZE,
    )
    SUB_TEST5_DESCRIPTION = f"[sub-test5] {DESCRIPTION}"

    table = Table.updater(qualified_name=table1.qualified_name, name=table1.name)
    table.user_description = SUB_TEST5_DESCRIPTION
    batch5.add(table)
    batch5.flush()

    # Validate that the table was updated
    assert batch5.num_updated == 1
    assert batch5.num_created == 0
    assert batch5.num_skipped == 0
    assert batch5.num_restored == 0

    # Wait for assets to be indexed
    sleep(5)
    results = (
        FluentSearch()
        .where(Asset.TYPE_NAME.eq(Table.__name__))
        .where(Asset.QUALIFIED_NAME.eq(table1.qualified_name))
        .include_on_results(Asset.USER_DESCRIPTION)
        .execute(client=client)
    )

    assert results and results.count == 1
    assert results.current_page() and len(results.current_page()) == 1
    updated_table = results.current_page()[0]
    assert (
        updated_table
        and updated_table.guid
        and updated_table.qualified_name == table1.qualified_name
    )
    assert updated_table.user_description == SUB_TEST5_DESCRIPTION

    # [sub-test-6]: (same operation as sub-test-5)
    # Table with table qn (case_insensitive=False, update_only=True)
    # Expect no operation as update is identical
    batch6 = Batch(
        client=client,
        track=True,
        update_only=True,
        case_insensitive=False,
        max_size=BATCH_MAX_SIZE,
    )

    table = Table.updater(qualified_name=table1.qualified_name, name=table1.name)
    # Use the same user description as before
    table.user_description = SUB_TEST5_DESCRIPTION
    batch6.add(table)
    batch6.flush()

    # No operation as update is identical
    assert batch6.num_restored == 1
    assert batch6.num_created == 0
    assert batch6.num_updated == 0
    assert batch6.num_skipped == 0

    # [sub-test-7]: (Table with table qn (case_insensitive=True, update_only=False)
    # Expect table to be created
    batch7 = Batch(
        client=client,
        track=True,
        update_only=False,
        case_insensitive=False,
        max_size=BATCH_MAX_SIZE,
        # Also test partial creation handling
        creation_handling=AssetCreationHandling.PARTIAL,
    )
    SUB_TEST7_DESCRIPTION = f"[sub-test7] {DESCRIPTION}"

    table = Table.updater(
        qualified_name=table1.qualified_name.lower(), name=table1.name
    )
    table.user_description = SUB_TEST7_DESCRIPTION
    batch7.add(table)
    batch7.flush()

    # Validate that the table was created
    assert batch7.num_created == 1
    assert batch7.num_updated == 0
    assert batch7.num_skipped == 0
    assert batch7.num_restored == 0

    # Wait for assets to be indexed
    sleep(5)
    results = (
        FluentSearch()
        .where(Asset.TYPE_NAME.eq(Table.__name__))
        .where(Asset.QUALIFIED_NAME.eq(table.qualified_name))
        .include_on_results(Asset.IS_PARTIAL)
        .include_on_results(Asset.USER_DESCRIPTION)
        .execute(client=client)
    )

    assert results and results.count == 1
    assert results.current_page() and len(results.current_page()) == 1
    created_table = results.current_page()[0]

    assert (
        created_table
        and created_table.guid
        and created_table.qualified_name == table.qualified_name
    )
    assert created_table.is_partial
    assert created_table.user_description == SUB_TEST7_DESCRIPTION

    # Cleanup: Delete the created table
    response = client.asset.purge_by_guid(created_table.guid)
    assert response.mutated_entities and response.mutated_entities.DELETE
