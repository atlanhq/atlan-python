import hashlib
import re

import pytest

from pyatlan.model.assets import Column, SqlInsightFilter
from tests.unit.model.constants import (
    COLUMN_NAME,
    SQL_INSIGHT_FILTER_NAME,
    SQL_INSIGHT_FILTER_OPERATOR,
    SQL_INSIGHT_FILTER_OPERATOR_OTHER,
    SQL_INSIGHT_FILTER_PREDICATE_SQL,
    SQL_INSIGHT_FILTER_QUALIFIED_NAME,
    SQL_INSIGHT_FILTER_QUALIFIED_NAME_OTHER_OPERATOR,
    SQL_INSIGHT_FILTER_WHEN_TO_USE,
    TABLE_COLUMN_QUALIFIED_NAME,
    TABLE_QUALIFIED_NAME,
)


def _column():
    return Column.ref_by_qualified_name(TABLE_COLUMN_QUALIFIED_NAME)


@pytest.mark.parametrize(
    "column, operator, message",
    [
        (None, SQL_INSIGHT_FILTER_OPERATOR, "column is required"),
        (_column(), None, "operator is required"),
        (_column(), "", "operator cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    column: Column, operator: str, message: str
):
    with pytest.raises(ValueError, match=message):
        SqlInsightFilter.creator(column=column, operator=operator)


def test_md5_matches_rfc_1321():
    """Separates "md5 is broken" from "the formula is wrong".

    Every golden below is an md5 of something. Without this, a change to encoding
    or digest handling fails all of them at once with no signal about the cause.
    """
    assert hashlib.md5(b"abc").hexdigest() == "900150983cd24fb0d6963f7d28e17f72"


def test_generate_qualified_name():
    """Pinned to a literal, never to the formula recomputed here.

    The contract is byte-identity with the SQL-Intelligence miner and the UI, so an
    expectation derived from the code under test would assert nothing.
    """
    assert (
        SqlInsightFilter.generate_qualified_name(
            column_qualified_name=TABLE_COLUMN_QUALIFIED_NAME,
            operator=SQL_INSIGHT_FILTER_OPERATOR,
        )
        == SQL_INSIGHT_FILTER_QUALIFIED_NAME
    )


def test_qualified_name_shape():
    """The two ways this identity has been got wrong before: the wrong segment
    literal, and a digest that is not a full 32-hex lowercase md5 (a business
    question once shipped as `/businessQuestion/` + a truncated sha256)."""
    qn = SqlInsightFilter.generate_qualified_name(
        column_qualified_name=TABLE_COLUMN_QUALIFIED_NAME,
        operator=SQL_INSIGHT_FILTER_OPERATOR,
    )
    prefix, segment, digest = qn.rsplit("/", 2)
    assert prefix == TABLE_COLUMN_QUALIFIED_NAME
    assert segment == "filter"
    assert re.fullmatch(r"[0-9a-f]{32}", digest)


def test_same_filter_converges_on_one_qualified_name():
    """The reason the method exists: re-confirming a filter, or the miner observing
    it later, must land on the SAME entity rather than duplicating it."""
    first = SqlInsightFilter.creator(
        column=_column(), operator=SQL_INSIGHT_FILTER_OPERATOR
    )
    second = SqlInsightFilter.creator(
        column=_column(),
        operator=SQL_INSIGHT_FILTER_OPERATOR,
        when_to_use="a different note, same filter",
    )
    assert first.qualified_name == second.qualified_name


def test_different_operator_is_a_different_filter():
    """Discrimination. A formula that ignored its input would pass convergence."""
    assert (
        SqlInsightFilter.generate_qualified_name(
            column_qualified_name=TABLE_COLUMN_QUALIFIED_NAME,
            operator=SQL_INSIGHT_FILTER_OPERATOR_OTHER,
        )
        == SQL_INSIGHT_FILTER_QUALIFIED_NAME_OTHER_OPERATOR
    )


def test_creator():
    sql_insight_filter = SqlInsightFilter.creator(
        column=_column(),
        operator=SQL_INSIGHT_FILTER_OPERATOR,
        predicate_sql=SQL_INSIGHT_FILTER_PREDICATE_SQL,
        when_to_use=SQL_INSIGHT_FILTER_WHEN_TO_USE,
    )

    assert sql_insight_filter.qualified_name == SQL_INSIGHT_FILTER_QUALIFIED_NAME
    assert sql_insight_filter.name == SQL_INSIGHT_FILTER_NAME
    assert sql_insight_filter.sql_insight_filter_operator == (
        SQL_INSIGHT_FILTER_OPERATOR
    )
    assert sql_insight_filter.sql_insight_filter_predicate_s_q_l == (
        SQL_INSIGHT_FILTER_PREDICATE_SQL
    )
    assert sql_insight_filter.sql_insight_filter_when_to_use == (
        SQL_INSIGHT_FILTER_WHEN_TO_USE
    )


def test_creator_writes_both_anchorings():
    """A filter carrying only one of these is half-visible: the asset page's Usage
    & Intelligence tab finds filters by the DATASET ATTRIBUTE, while the COLUMN
    RELATIONSHIP is what renders the row on the column itself."""
    sql_insight_filter = SqlInsightFilter.creator(
        column=_column(), operator=SQL_INSIGHT_FILTER_OPERATOR
    )

    assert sql_insight_filter.sql_insight_filter_dataset_qualified_name == (
        TABLE_QUALIFIED_NAME
    )
    assert sql_insight_filter.sql_insight_filter_column_qualified_name == (
        TABLE_COLUMN_QUALIFIED_NAME
    )
    assert sql_insight_filter.sql_insight_column is not None
    assert sql_insight_filter.sql_insight_column.qualified_name == (
        TABLE_COLUMN_QUALIFIED_NAME
    )


def test_creator_claims_no_observed_usage():
    """A human-declared filter has no query history; reporting one would put
    invented popularity on the asset page."""
    sql_insight_filter = SqlInsightFilter.creator(
        column=_column(), operator=SQL_INSIGHT_FILTER_OPERATOR
    )

    assert sql_insight_filter.sql_insight_filter_query_count == 0
    assert sql_insight_filter.sql_insight_filter_unique_users == 0


def test_creator_default_name_reads_as_the_filter():
    sql_insight_filter = SqlInsightFilter.creator(
        column=_column(), operator=SQL_INSIGHT_FILTER_OPERATOR
    )

    assert sql_insight_filter.name == f"{COLUMN_NAME} {SQL_INSIGHT_FILTER_OPERATOR}"
