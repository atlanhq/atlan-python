import hashlib
import re

import pytest

from pyatlan.model.assets import SqlInsightBusinessQuestion, Table
from tests.unit.model.constants import (
    SQL_INSIGHT_QUESTION_CANONICAL_SQL,
    SQL_INSIGHT_QUESTION_QUALIFIED_NAME,
    SQL_INSIGHT_QUESTION_QUALIFIED_NAME_OTHER_TEXT,
    SQL_INSIGHT_QUESTION_TEXT,
    SQL_INSIGHT_QUESTION_TEXT_OTHER,
    TABLE_QUALIFIED_NAME,
)


def _dataset():
    return Table.ref_by_qualified_name(TABLE_QUALIFIED_NAME)


@pytest.mark.parametrize(
    "dataset, question_text, message",
    [
        (None, SQL_INSIGHT_QUESTION_TEXT, "dataset is required"),
        (_dataset(), None, "question_text is required"),
        (_dataset(), "", "question_text cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    dataset: Table, question_text: str, message: str
):
    with pytest.raises(ValueError, match=message):
        SqlInsightBusinessQuestion.creator(dataset=dataset, question_text=question_text)


def test_md5_matches_rfc_1321():
    """Separates "md5 is broken" from "the formula is wrong"."""
    assert hashlib.md5(b"abc").hexdigest() == "900150983cd24fb0d6963f7d28e17f72"


def test_generate_qualified_name():
    """Pinned to a literal, never to the formula recomputed here."""
    assert (
        SqlInsightBusinessQuestion.generate_qualified_name(
            dataset_qualified_name=TABLE_QUALIFIED_NAME,
            question_text=SQL_INSIGHT_QUESTION_TEXT,
        )
        == SQL_INSIGHT_QUESTION_QUALIFIED_NAME
    )


def test_qualified_name_shape():
    """This type shipped once as `/businessQuestion/` plus a truncated sha256, so
    the segment literal and the full 32-hex lowercase digest are asserted directly
    rather than left implicit in the golden."""
    qn = SqlInsightBusinessQuestion.generate_qualified_name(
        dataset_qualified_name=TABLE_QUALIFIED_NAME,
        question_text=SQL_INSIGHT_QUESTION_TEXT,
    )
    prefix, segment, digest = qn.rsplit("/", 2)
    assert prefix == TABLE_QUALIFIED_NAME
    assert segment == "question"
    assert re.fullmatch(r"[0-9a-f]{32}", digest)


def test_same_question_converges_on_one_qualified_name():
    """Re-confirming a question, or the miner observing it later, must land on the
    SAME entity rather than duplicating it."""
    first = SqlInsightBusinessQuestion.creator(
        dataset=_dataset(), question_text=SQL_INSIGHT_QUESTION_TEXT
    )
    second = SqlInsightBusinessQuestion.creator(
        dataset=_dataset(),
        question_text=SQL_INSIGHT_QUESTION_TEXT,
        canonical_sql="SELECT 1  -- a different answer to the same question",
    )
    assert first.qualified_name == second.qualified_name


def test_reworded_question_is_a_new_entity():
    """The hash is over the question TEXT alone, so rewording creates a new entity
    rather than silently rewriting the old one. Called out because it is a real
    consequence callers need to expect, not an accident of the formula."""
    assert (
        SqlInsightBusinessQuestion.generate_qualified_name(
            dataset_qualified_name=TABLE_QUALIFIED_NAME,
            question_text=SQL_INSIGHT_QUESTION_TEXT_OTHER,
        )
        == SQL_INSIGHT_QUESTION_QUALIFIED_NAME_OTHER_TEXT
    )


def test_creator():
    question = SqlInsightBusinessQuestion.creator(
        dataset=_dataset(),
        question_text=SQL_INSIGHT_QUESTION_TEXT,
        canonical_sql=SQL_INSIGHT_QUESTION_CANONICAL_SQL,
    )

    assert question.qualified_name == SQL_INSIGHT_QUESTION_QUALIFIED_NAME
    assert question.name == SQL_INSIGHT_QUESTION_TEXT
    assert question.sql_insight_business_question_text == SQL_INSIGHT_QUESTION_TEXT
    assert question.sql_insight_business_question_canonical_s_q_l == (
        SQL_INSIGHT_QUESTION_CANONICAL_SQL
    )


def test_creator_writes_both_anchorings():
    """The dataset ATTRIBUTE and the dataset RELATIONSHIP are both load-bearing; a
    question carrying only one is half-visible on the asset."""
    question = SqlInsightBusinessQuestion.creator(
        dataset=_dataset(), question_text=SQL_INSIGHT_QUESTION_TEXT
    )

    assert question.sql_insight_business_question_dataset_qualified_name == (
        TABLE_QUALIFIED_NAME
    )
    assert question.sql_insight_dataset is not None
    assert question.sql_insight_dataset.qualified_name == TABLE_QUALIFIED_NAME


def test_creator_claims_no_observed_usage():
    """A human-declared question has no query history; reporting one would put
    invented popularity on the asset page."""
    question = SqlInsightBusinessQuestion.creator(
        dataset=_dataset(), question_text=SQL_INSIGHT_QUESTION_TEXT
    )

    assert question.sql_insight_business_question_query_count == 0
    assert question.sql_insight_business_question_unique_users == 0
