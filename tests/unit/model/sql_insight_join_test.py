import json

import pytest

from pyatlan.model.assets import SqlInsightJoin, Table, View
from pyatlan.model.enums import SqlInsightJoinCardinality, SqlInsightJoinType

SOURCE_QUALIFIED_NAME = (
    "default/snowflake/1780005299/AI_DEMO/BANKING_FPNA_RAW_ORAAS/GL_BALANCES"
)
JOINED_QUALIFIED_NAME = (
    "default/snowflake/1780005299/AI_DEMO/BANKING_FPNA_RAW_REFDATA/DSMT_PRODUCT"
)
COLUMN_PAIRS = [{"source_column": "PRODUCT_ID", "joined_column": "PRODUCT_ID"}]
# Digest of a real, miner-written SqlInsightJoin row: the creator's
# qualifiedName derivation must stay byte-identical to the SQL-Intelligence
# miner so human-confirmed and mined joins converge on one entity.
LIVE_MINER_DIGEST = "1b92c9836aa403b330bbecd843460af7"
JOIN_QUALIFIED_NAME = f"{SOURCE_QUALIFIED_NAME}/join/{LIVE_MINER_DIGEST}"


def _source():
    return Table.ref_by_qualified_name(SOURCE_QUALIFIED_NAME)


def _joined():
    return Table.ref_by_qualified_name(JOINED_QUALIFIED_NAME)


@pytest.mark.parametrize(
    "source_dataset, joined_dataset, column_pairs, message",
    [
        (None, _joined(), COLUMN_PAIRS, "source_dataset is required"),
        (_source(), None, COLUMN_PAIRS, "joined_dataset is required"),
        (_source(), _joined(), None, "column_pairs is required"),
        (_source(), _joined(), [], "column_pairs cannot be an empty list"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    source_dataset, joined_dataset, column_pairs, message: str
):
    with pytest.raises(ValueError, match=message):
        SqlInsightJoin.creator(
            source_dataset=source_dataset,
            joined_dataset=joined_dataset,
            column_pairs=column_pairs,
        )


def test_creator_with_dataset_missing_qualified_name_raises_value_error():
    with pytest.raises(ValueError, match="qualified_name cannot be blank"):
        SqlInsightJoin.creator(
            source_dataset=Table(),
            joined_dataset=_joined(),
            column_pairs=COLUMN_PAIRS,
        )


@pytest.mark.parametrize(
    "column_pairs",
    [
        [{"source_column": "A"}],
        [{"joined_column": "B"}],
        [{"source_column": "", "joined_column": "B"}],
        [{"source_column": "A", "joined_column": ""}],
        ["A=B"],
    ],
)
def test_creator_with_invalid_column_pairs_raises_value_error(column_pairs):
    with pytest.raises(ValueError, match="each column pair must be a dict"):
        SqlInsightJoin.creator(
            source_dataset=_source(),
            joined_dataset=_joined(),
            column_pairs=column_pairs,
        )


def test_creator():
    join = SqlInsightJoin.creator(
        source_dataset=_source(),
        joined_dataset=_joined(),
        column_pairs=COLUMN_PAIRS,
        join_type=SqlInsightJoinType.LEFT,
        cardinality=SqlInsightJoinCardinality.MANY_TO_ONE,
    )

    # identity converges with the miner-written row (byte-exact digest)
    assert join.qualified_name == JOIN_QUALIFIED_NAME
    assert join.name == "GL_BALANCES JOIN DSMT_PRODUCT"
    assert join.sql_insight_join_source_dataset_qualified_name == SOURCE_QUALIFIED_NAME
    assert join.sql_insight_join_joined_dataset_qualified_name == JOINED_QUALIFIED_NAME
    assert join.sql_insight_join_type == SqlInsightJoinType.LEFT
    assert join.sql_insight_join_cardinality == SqlInsightJoinCardinality.MANY_TO_ONE
    # a human-declared join has no observed usage
    assert join.sql_insight_join_query_count == 0
    assert join.sql_insight_join_unique_users == 0
    # column-pair struct carries fully-qualified column names
    pair = join.sql_insight_join_column_pairs[0]
    assert (
        pair.sql_insight_join_column_pair_source_column_qualified_name
        == f"{SOURCE_QUALIFIED_NAME}/PRODUCT_ID"
    )
    assert (
        pair.sql_insight_join_column_pair_joined_column_qualified_name
        == f"{JOINED_QUALIFIED_NAME}/PRODUCT_ID"
    )
    # both relationship edges are anchored to the passed datasets
    assert join.attributes.sql_insight_source_dataset.qualified_name == (
        SOURCE_QUALIFIED_NAME
    )
    assert join.attributes.sql_insight_joined_dataset.qualified_name == (
        JOINED_QUALIFIED_NAME
    )


def test_creator_with_optional_parameters():
    join = SqlInsightJoin.creator(
        source_dataset=_source(),
        joined_dataset=_joined(),
        column_pairs=COLUMN_PAIRS,
        join_type=SqlInsightJoinType.LEFT,
        when_to_use="Enrich GL balance rows with product hierarchy",
        name="My custom join name",
    )

    assert join.name == "My custom join name"
    assert (
        join.sql_insight_join_when_to_use
        == "Enrich GL balance rows with product hierarchy"
    )
    # custom name must not change the derived identity
    assert join.qualified_name == JOIN_QUALIFIED_NAME


def test_creator_serialization_carries_both_anchorings():
    join = SqlInsightJoin.creator(
        source_dataset=_source(),
        joined_dataset=View.ref_by_qualified_name(JOINED_QUALIFIED_NAME),
        column_pairs=COLUMN_PAIRS,
        join_type=SqlInsightJoinType.LEFT,
    )
    request = json.loads(join.json(by_alias=True, exclude_unset=True))
    attributes = request["attributes"]
    # string attributes (read by metadata-lakehouse consumers)
    assert attributes["sqlInsightJoinSourceDatasetQualifiedName"] == (
        SOURCE_QUALIFIED_NAME
    )
    assert attributes["sqlInsightJoinColumnPairs"][0][
        "sqlInsightJoinColumnPairSourceColumnQualifiedName"
    ] == (f"{SOURCE_QUALIFIED_NAME}/PRODUCT_ID")
    # relationship edges (rendered on the asset page) with concrete types
    assert attributes["sqlInsightSourceDataset"]["typeName"] == "Table"
    assert attributes["sqlInsightJoinedDataset"]["typeName"] == "View"
    assert attributes["sqlInsightJoinQueryCount"] == 0
    assert attributes["sqlInsightJoinUniqueUsers"] == 0


def test_generate_qualified_name_is_pair_order_invariant():
    pairs = [
        {"source_column": "B_COL", "joined_column": "X"},
        {"source_column": "A_COL", "joined_column": "Y"},
    ]
    forward = SqlInsightJoin.generate_qualified_name(
        source_qualified_name=SOURCE_QUALIFIED_NAME,
        joined_qualified_name=JOINED_QUALIFIED_NAME,
        column_pairs=pairs,
        join_type=SqlInsightJoinType.INNER,
    )
    reordered = SqlInsightJoin.generate_qualified_name(
        source_qualified_name=SOURCE_QUALIFIED_NAME,
        joined_qualified_name=JOINED_QUALIFIED_NAME,
        column_pairs=list(reversed(pairs)),
        join_type=SqlInsightJoinType.INNER,
    )
    assert forward == reordered


def test_generate_qualified_name_accepts_enum_or_string_join_type():
    from_enum = SqlInsightJoin.generate_qualified_name(
        source_qualified_name=SOURCE_QUALIFIED_NAME,
        joined_qualified_name=JOINED_QUALIFIED_NAME,
        column_pairs=COLUMN_PAIRS,
        join_type=SqlInsightJoinType.LEFT,
    )
    from_string = SqlInsightJoin.generate_qualified_name(
        source_qualified_name=SOURCE_QUALIFIED_NAME,
        joined_qualified_name=JOINED_QUALIFIED_NAME,
        column_pairs=COLUMN_PAIRS,
        join_type="LEFT",
    )
    assert from_enum == from_string == JOIN_QUALIFIED_NAME


def test_generate_qualified_name_varies_by_join_type():
    left = SqlInsightJoin.generate_qualified_name(
        source_qualified_name=SOURCE_QUALIFIED_NAME,
        joined_qualified_name=JOINED_QUALIFIED_NAME,
        column_pairs=COLUMN_PAIRS,
        join_type=SqlInsightJoinType.LEFT,
    )
    inner = SqlInsightJoin.generate_qualified_name(
        source_qualified_name=SOURCE_QUALIFIED_NAME,
        joined_qualified_name=JOINED_QUALIFIED_NAME,
        column_pairs=COLUMN_PAIRS,
        join_type=SqlInsightJoinType.INNER,
    )
    assert left != inner


def test_updater():
    join = SqlInsightJoin.updater(
        qualified_name=JOIN_QUALIFIED_NAME, name="GL_BALANCES JOIN DSMT_PRODUCT"
    )
    assert join.qualified_name == JOIN_QUALIFIED_NAME
    assert join.name == "GL_BALANCES JOIN DSMT_PRODUCT"
