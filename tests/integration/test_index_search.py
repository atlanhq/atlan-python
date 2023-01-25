import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.entity import EntityClient
from pyatlan.model.assets import (
    AtlasGlossary,
    Connection,
    Database,
    MaterialisedView,
    Schema,
    Table,
    View,
)
from pyatlan.model.search import (
    DSL,
    Exists,
    IndexSearchRequest,
    SortItem,
    SortOrder,
    Term,
)


@pytest.fixture(scope="module")
def client() -> EntityClient:
    return EntityClient(AtlanClient())


@pytest.mark.parametrize(
    "query,  post_filter,attributes, sort_order, a_class",
    [
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="AtlasGlossary"),
            ["schemaName", "databaseName"],
            None,
            AtlasGlossary,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="Connection")
            + Exists(field="category")
            + Term(field="adminUsers", value="ernest"),
            ["schemaName", "databaseName"],
            None,
            Connection,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="Database"),
            ["schemaName", "databaseName"],
            None,
            Database,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="Schema"),
            ["schemaName", "databaseName"],
            None,
            Schema,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="Table"),
            ["schemaName", "databaseName"],
            [SortItem(field="__typeName.keyword", order=SortOrder.ASCENDING)],
            Table,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="View"),
            ["schemaName", "databaseName"],
            None,
            View,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="MaterialisedView"),
            ["schemaName", "databaseName"],
            None,
            MaterialisedView,
        ),
        (
            Term(field="__typeName.keyword", value="AtlasGlossary"),
            None,
            ["schemaName", "databaseName"],
            None,
            AtlasGlossary,
        ),
    ],
)
def test_search(
    client: EntityClient, query, post_filter, attributes, sort_order, a_class
):
    dsl = DSL(query=query, post_filter=post_filter, sort=sort_order)
    request = IndexSearchRequest(dsl=dsl, attributes=attributes)
    results = client.search(criteria=request)
    counter = 0
    for asset in results:
        assert isinstance(asset, a_class)
        counter += 1
        if counter > 3:
            break
    assert counter > 0


def test_search_next_page(client: EntityClient):
    size = 15
    dsl = DSL(
        query=Term(field="__state", value="ACTIVE"),
        post_filter=Term(field="__typeName.keyword", value="Database"),
        size=size,
    )
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["databaseName"],
    )
    results = client.search(criteria=request)
    assert results.count > size
    assert len(results.current_page()) == size
    counter = 0
    while True:
        for _ in results.current_page():
            counter += 1
        if results.next_page() is not True:
            break
    assert counter == results.count


def test_search_iter(client: EntityClient):
    size = 15
    dsl = DSL(
        query=Term(field="__state", value="ACTIVE"),
        post_filter=Term(field="__typeName.keyword", value="Database"),
        size=size,
    )
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["databaseName"],
    )
    results = client.search(criteria=request)
    assert results.count > size
    assert len([a for a in results]) == results.count


def test_search_next_when_start_changed_returns_remaining(client: EntityClient):
    size = 2
    dsl = DSL(
        query=Term(field="__state", value="ACTIVE"),
        post_filter=Term(field="__typeName.keyword", value="Database"),
        size=size,
    )
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["databaseName"],
    )
    results = client.search(criteria=request)
    assert results.next_page(start=results.count - size) is True
    assert len(list(results)) == size


@pytest.fixture()
def query_value(request):
    method_name = request.param
    if method_name == "with_categories":
        return "VBsYc9dUoEcAtDxZmjby6@mweSfpXBwfYWedQTvA3Gi"
    if method_name == "with_classification_names":
        return "|RBmhFJqX50bl5RAeJhwt1a|"  # Fixme
    if method_name == "with_classifications_text":
        return "VBsYc9dUoEcAtDxZmjby6@mweSfpXBwfYWedQTvA3Gi"
    if method_name == "with_created_by":
        return "bryan"
    if method_name == "with_glossary":
        return "mweSfpXBwfYWedQTvA3Gi"
    if method_name == "with_guid":
        return "331bae42-5f97-4068-a084-1557f31de770"
    if method_name == "with_has_lineage":
        return True
    if method_name == "with_meanings":
        return "|RBmhFJqX50bl5RAeJhwt1a|"  # Fixme
    if method_name == "with_meanings_text":
        return "VBsYc9dUoEcAtDxZmjby6@mweSfpXBwfYWedQTvA3Gi"
    if method_name == "with_modification_timestamp":
        return 1665086276846
    if method_name == "with_modified_by":
        return "bryan"
    if method_name == "with_name":
        return "Schema"
    if method_name == "with_parent_category":
        return "VBsYc9dUoEcAtDxZmjby6@mweSfpXBwfYWedQTvA3Gi"
    if method_name == "with_propagated_classification_names":
        return "|RBmhFJqX50bl5RAeJhwt1a|"  # Fixme
    if method_name == "with_qualified_name":
        return "default/oracle/1665680872/ORCL/SCALE_TEST/TABLE_MVD_3042/PERSON_ID"
    if method_name == "with_state":
        return "ACTIVE"
    if method_name == "with_super_type_name":
        return "Asset"
    if method_name == "with_timestamp":
        return 1665086276846
    if method_name == "with_propagated_trait_names":
        return "abc"
    print(f"Missing: {method_name}")
    return "abc"


@pytest.mark.parametrize(
    "query_value, method, clazz",
    [(method, method, Term) for method in dir(Term) if method.startswith("with_")],
    indirect=["query_value"],
)
def test_factory(client: EntityClient, query_value, method, clazz):
    assert hasattr(clazz, method)
    query = getattr(clazz, method)(query_value)
    filter = ~Term.with_type_name("__AtlasAuditEntry")
    dsl = DSL(query=query, post_filter=filter, size=1)
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["name"],
    )
    # print(request.json(by_alias=True, exclude_none=True))
    results = client.search(criteria=request)
    assert results.count >= 0


@pytest.mark.parametrize(
    "with_name", [(method) for method in dir(Exists) if method.startswith("with_")]
)
def test_exists_query_factory(client: EntityClient, with_name):
    assert hasattr(Exists, with_name)
    query = getattr(Exists, with_name)()
    dsl = DSL(query=query, size=1)
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["name"],
    )
    results = client.search(criteria=request)
    assert results.count > 0
