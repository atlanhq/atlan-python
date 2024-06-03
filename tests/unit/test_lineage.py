# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import json
from datetime import date
from pathlib import Path
from typing import List
from unittest.mock import Mock

import pytest

from pyatlan.errors import AtlanError, InvalidRequestError
from pyatlan.model.assets import Asset
from pyatlan.model.enums import (
    AtlanComparisonOperator,
    CertificateStatus,
    EntityStatus,
    FileType,
    LineageDirection,
)
from pyatlan.model.fields.atlan_fields import (
    AtlanField,
    CustomMetadataField,
    LineageFilter,
    LineageFilterField,
    LineageFilterFieldBoolean,
    LineageFilterFieldCM,
    LineageFilterFieldNumeric,
    LineageFilterFieldString,
    SearchableField,
)
from pyatlan.model.lineage import (
    FilterList,
    FluentLineage,
    LineageGraph,
    LineageRelation,
    LineageResponse,
)
from pyatlan.model.typedef import AttributeDef

TODAY = date.today()
BASE_GUID = "75474eab-3105-4ef9-9f84-709e386a7d3e"
BASE_GUID_TARGET = "e44ed3a2-1de5-4f23-b3f1-6e005156fee9"
LINEAGE_RESPONSES_DIR = Path(__file__).parent / "data" / "lineage_responses"


@pytest.fixture(scope="session")
def lineage_json():
    with (LINEAGE_RESPONSES_DIR / "lineage.json").open() as input_file:
        return json.load(input_file)


@pytest.fixture(scope="session")
def lineage_response(lineage_json):
    return LineageResponse(**lineage_json)


@pytest.fixture(scope="session")
def lineage_graph(lineage_response):
    return LineageGraph.create(lineage_response.relations)


class TestLineageGraph:
    def test_create_when_relation_is_not_full_link_then_raises_invalid_request_exception(
        self,
    ):
        with pytest.raises(
            InvalidRequestError,
            match="Lineage was retrieved using hideProces=False. We do not provide a graph view in this case.",
        ):
            LineageGraph.create(
                [
                    LineageRelation(
                        from_entity_id="123", to_entity_id="456", process_id=None
                    )
                ]
            )

    def test_get_downstream_asset_guid_with_invalid_guid_returns_empty_set_of_guids(
        self,
        lineage_graph,
    ):
        assert len(lineage_graph.get_downstream_asset_guids("123")) == 0

    def test_get_downstream_asset_guid_with_valid_guid_returns_set_of_guids(
        self, lineage_graph
    ):
        assert (guids := lineage_graph.get_downstream_asset_guids(BASE_GUID))
        assert len(guids) == 1
        assert "e44ed3a2-1de5-4f23-b3f1-6e005156fee9" in guids

    def test_get_upstream_asset_guid_with_invalid_guid_returns_empty_set_of_guids(
        self,
        lineage_graph,
    ):
        assert len(lineage_graph.get_upstream_asset_guids("123")) == 0

    def test_get_upstream_asset_guid_with_base_guid_returns_empty_set_of_guids(
        self,
        lineage_graph,
    ):
        assert len(lineage_graph.get_upstream_asset_guids(BASE_GUID)) == 0

    def test_get_upstream_asset_guid_with_valid_guid_returns_set_of_guids(
        self, lineage_graph
    ):
        assert (guids := lineage_graph.get_upstream_asset_guids(BASE_GUID_TARGET))
        assert len(guids) == 1
        assert BASE_GUID in guids

    def test_get_downstream_process_guid_with_valid_guid_returns_set_of_guids(
        self,
        lineage_graph,
    ):
        assert (guids := lineage_graph.get_downstream_process_guids(BASE_GUID))
        assert len(guids) == 2
        assert "621d3fa2-54b0-4cc0-a858-5c5ea8c49349" in guids
        assert "d67d4188-010b-4adf-9886-10162f08c77b" in guids

    def test_get_upstream_process_guids_with_valid_guid_returns_set_of_guids(
        self, lineage_graph
    ):
        assert (guids := lineage_graph.get_upstream_process_guids(BASE_GUID_TARGET))
        assert len(guids) == 2
        assert "621d3fa2-54b0-4cc0-a858-5c5ea8c49349" in guids
        assert "d67d4188-010b-4adf-9886-10162f08c77b" in guids

    def test_get_downstream_process_guid_with_invalid_guid_returns_empty_set_of_guids(
        self,
        lineage_graph,
    ):
        assert len(lineage_graph.get_downstream_process_guids("123")) == 0

    def test_get_upstream_process_guid_with_invalid_guid_returns_empty_set_of_guids(
        self,
        lineage_graph,
    ):
        assert len(lineage_graph.get_upstream_process_guids("123")) == 0

    @pytest.mark.parametrize(
        "guid, expected_count",
        [
            ("a3585e50-a045-4349-b9d7-b0980961c1a1", 1),
            ("d043b6a8-7a24-42aa-8c3a-25e5901c57ab", 6),
            ("0279e19c-3ebb-4472-a737-d245e2914369", 2),
            ("0ba9763e-82c2-4765-ad7a-018d46dd5c80", 87),
            ("80680c12-f625-4b7f-a5fa-d3fd296e2db1", 18),
        ],
    )
    def test_get_all_downstream_asset_guids_dfs(
        self, guid, expected_count, lineage_graph
    ):
        assert (guids := lineage_graph.get_all_downstream_asset_guids_dfs(guid))
        assert len(guids) == expected_count

    @pytest.mark.parametrize(
        "guid, expected_count",
        [
            ("a3585e50-a045-4349-b9d7-b0980961c1a1", 1),
            ("d043b6a8-7a24-42aa-8c3a-25e5901c57ab", 8),
            ("0279e19c-3ebb-4472-a737-d245e2914369", 10),
            ("0ba9763e-82c2-4765-ad7a-018d46dd5c80", 4),
            ("80680c12-f625-4b7f-a5fa-d3fd296e2db1", 8),
        ],
    )
    def test_get_all_upstream_asset_guids_dfs(
        self, guid, expected_count, lineage_graph
    ):
        assert (guids := lineage_graph.get_all_upstream_asset_guids_dfs(guid))
        assert len(guids) == expected_count


class TestLineageResponse:
    @pytest.mark.parametrize(
        "guid, expected_count",
        [
            ("a3585e50-a045-4349-b9d7-b0980961c1a1", 1),
            ("d043b6a8-7a24-42aa-8c3a-25e5901c57ab", 6),
            ("0279e19c-3ebb-4472-a737-d245e2914369", 2),
            ("0ba9763e-82c2-4765-ad7a-018d46dd5c80", 87),
            ("80680c12-f625-4b7f-a5fa-d3fd296e2db1", 18),
        ],
    )
    def test_get_all_downstream_asset_guids_dfs(
        self, guid, expected_count, lineage_response
    ):
        assert (guids := lineage_response.get_all_downstream_asset_guids_dfs(guid))
        assert len(guids) == expected_count

    @pytest.mark.parametrize(
        "guid, expected_count",
        [
            ("a3585e50-a045-4349-b9d7-b0980961c1a1", 1),
            ("d043b6a8-7a24-42aa-8c3a-25e5901c57ab", 6),
            ("0279e19c-3ebb-4472-a737-d245e2914369", 2),
            ("0ba9763e-82c2-4765-ad7a-018d46dd5c80", 87),
            ("80680c12-f625-4b7f-a5fa-d3fd296e2db1", 18),
        ],
    )
    def test_get_all_downstream_assets_dfs(
        self, guid, expected_count, lineage_response
    ):
        assert (assets := lineage_response.get_all_downstream_assets_dfs(guid))
        assert len(assets) == expected_count

    @pytest.mark.parametrize(
        "guid, expected_count",
        [
            ("a3585e50-a045-4349-b9d7-b0980961c1a1", 1),
            ("d043b6a8-7a24-42aa-8c3a-25e5901c57ab", 8),
            ("0279e19c-3ebb-4472-a737-d245e2914369", 10),
            ("0ba9763e-82c2-4765-ad7a-018d46dd5c80", 4),
            ("80680c12-f625-4b7f-a5fa-d3fd296e2db1", 8),
        ],
    )
    def test_get_all_upstream_asset_guids_dfs(
        self, guid, expected_count, lineage_response
    ):
        assert (guids := lineage_response.get_all_upstream_asset_guids_dfs(guid))
        assert len(guids) == expected_count

    @pytest.mark.parametrize(
        "guid, expected_count",
        [
            ("a3585e50-a045-4349-b9d7-b0980961c1a1", 1),
            ("d043b6a8-7a24-42aa-8c3a-25e5901c57ab", 8),
            ("0279e19c-3ebb-4472-a737-d245e2914369", 10),
            ("0ba9763e-82c2-4765-ad7a-018d46dd5c80", 4),
            ("80680c12-f625-4b7f-a5fa-d3fd296e2db1", 8),
        ],
    )
    def test_get_all_upstream_assets_dfs(self, guid, expected_count, lineage_response):
        assert (guids := lineage_response.get_all_upstream_assets_dfs(guid))
        assert len(guids) == expected_count

    def test_get_downstream_asset_guid_with_invalid_guid_returns_empty_set_of_guids(
        self,
        lineage_response,
    ):
        assert len(lineage_response.get_downstream_asset_guids("123")) == 0

    def test_get_downstream_asset_guid_with_valid_guid_returns_set_of_guids(
        self, lineage_response
    ):
        assert (guids := lineage_response.get_downstream_asset_guids(BASE_GUID))
        assert len(guids) == 1
        assert "e44ed3a2-1de5-4f23-b3f1-6e005156fee9" in guids

    def test_get_downstream_assets_with_valid_guid_returns_set_of_guids(
        self, lineage_response
    ):
        assert (assets := lineage_response.get_downstream_assets(BASE_GUID))
        assert len(assets) == 1

    def test_get_upstream_asset_guid_with_invalid_guid_returns_empty_set_of_guids(
        self,
        lineage_response,
    ):
        assert len(lineage_response.get_upstream_asset_guids("123")) == 0

    def test_get_upstream_asset_guid_with_base_guid_returns_empty_set_of_guids(
        self,
        lineage_response,
    ):
        assert len(lineage_response.get_upstream_asset_guids(BASE_GUID)) == 0

    def test_get_upstream_asset_guid_with_valid_guid_returns_set_of_guids(
        self, lineage_response
    ):
        assert (guids := lineage_response.get_upstream_asset_guids(BASE_GUID_TARGET))
        assert len(guids) == 1
        assert BASE_GUID in guids

    def test_get_downstream_process_guid_with_valid_guid_returns_set_of_guids(
        self,
        lineage_response,
    ):
        assert (guids := lineage_response.get_downstream_process_guids(BASE_GUID))
        assert len(guids) == 2
        assert "621d3fa2-54b0-4cc0-a858-5c5ea8c49349" in guids
        assert "d67d4188-010b-4adf-9886-10162f08c77b" in guids

    def test_get_upstream_process_guids_with_valid_guid_returns_set_of_guids(
        self, lineage_response
    ):
        assert (guids := lineage_response.get_upstream_process_guids(BASE_GUID_TARGET))
        assert len(guids) == 2
        assert "621d3fa2-54b0-4cc0-a858-5c5ea8c49349" in guids
        assert "d67d4188-010b-4adf-9886-10162f08c77b" in guids

    def test_get_upstream_assets_with_valid_guid_returns_set_of_assets(
        self, lineage_response
    ):
        assert (assets := lineage_response.get_upstream_process_guids(BASE_GUID_TARGET))
        assert len(assets) == 2

    def test_get_downstream_process_guid_with_invalid_guid_returns_empty_set_of_guids(
        self,
        lineage_response,
    ):
        assert len(lineage_response.get_downstream_process_guids("123")) == 0

    def test_get_upstream_process_guid_with_invalid_guid_returns_empty_set_of_guids(
        self,
        lineage_response,
    ):
        assert len(lineage_response.get_upstream_process_guids("123")) == 0


@pytest.fixture
def searchable_field() -> SearchableField:
    return SearchableField(
        atlan_field_name="atlan_field", elastic_field_name="elastic_field"
    )


class TestLineageFilterField:
    @pytest.fixture
    def sut(self, searchable_field: SearchableField) -> LineageFilterField:
        return LineageFilterField(field=searchable_field)

    def test_init(self, sut: LineageFilterField, searchable_field: SearchableField):
        assert sut.field == searchable_field

    def test_has_any_value(self, sut: LineageFilterField):
        _filter = sut.has_any_value()
        assert _filter.field == sut.field
        assert _filter.operator == AtlanComparisonOperator.NOT_NULL
        assert _filter.value == ""

    def test_has_no_value(self, sut: LineageFilterField):
        _filter = sut.has_no_value()
        assert _filter.field == sut.field
        assert _filter.operator == AtlanComparisonOperator.IS_NULL
        assert _filter.value == ""


class TestLineageFilterFieldBoolean:
    @pytest.fixture
    def sut(self, searchable_field: SearchableField) -> LineageFilterFieldBoolean:
        return LineageFilterFieldBoolean(field=searchable_field)

    def test_init(
        self, sut: LineageFilterFieldBoolean, searchable_field: SearchableField
    ):
        assert sut.field == searchable_field

    @pytest.mark.parametrize(
        "value, expected", [(True, str(True)), (False, str(False))]
    )
    def test_eq(self, value, expected, sut: LineageFilterFieldBoolean):
        _filter = sut.eq(value)
        assert _filter.field == sut.field
        assert _filter.operator == AtlanComparisonOperator.EQ
        assert _filter.value == expected

    @pytest.mark.parametrize(
        "value, expected", [(True, str(True)), (False, str(False))]
    )
    def test_neq(self, value, expected, sut: LineageFilterFieldBoolean):
        _filter = sut.neq(value)
        assert _filter.field == sut.field
        assert _filter.operator == AtlanComparisonOperator.NEQ
        assert _filter.value == expected


class TestLineageFilterFieldCM:
    @pytest.fixture()
    def custom_metadata_field(self) -> CustomMetadataField:
        return Mock(spec=CustomMetadataField)

    @pytest.fixture
    def sut(self, custom_metadata_field: CustomMetadataField) -> LineageFilterFieldCM:
        return LineageFilterFieldCM(field=custom_metadata_field)

    @staticmethod
    def configure_custom_metadata_field(custom_metadata_field, type_name):
        attribute_def = Mock(spec=AttributeDef)
        attribute_def.configure_mock(**{"type_name": type_name})
        custom_metadata_field.attach_mock(attribute_def, "attribute_def")
        custom_metadata_field.attach_mock(attribute_def, "attribute_def")
        custom_metadata_field.configure_mock(
            **{"set_name": "something", "attribute_name": "an_attribute"}
        )

    def test_init(
        self, sut: LineageFilterFieldCM, custom_metadata_field: CustomMetadataField
    ):
        assert sut.field == custom_metadata_field
        assert sut.cm_field == custom_metadata_field

    @pytest.mark.parametrize(
        "value, expected", [("value", "value"), (FileType.CSV, FileType.CSV.value)]
    )
    def test_eq(self, value, expected, sut: LineageFilterFieldCM):
        _filter = sut.eq(value)
        assert _filter.field == sut.field
        assert _filter.operator == AtlanComparisonOperator.EQ
        assert _filter.value == expected

    @pytest.mark.parametrize(
        "value, expected", [("value", "value"), (FileType.CSV, FileType.CSV.value)]
    )
    def test_neq(self, value, expected, sut: LineageFilterFieldCM):
        _filter = sut.neq(value)
        assert _filter.field == sut.field
        assert _filter.operator == AtlanComparisonOperator.NEQ
        assert _filter.value == expected

    @pytest.mark.parametrize(
        "method, type_name, value, operator",
        [
            ("eq", "int", 1, AtlanComparisonOperator.EQ),
            ("eq", "boolean", True, AtlanComparisonOperator.EQ),
            ("neq", "int", 1, AtlanComparisonOperator.NEQ),
            ("neq", "boolean", True, AtlanComparisonOperator.NEQ),
            ("gte", "int", 1, AtlanComparisonOperator.GTE),
            ("lte", "int", 1, AtlanComparisonOperator.LTE),
            ("gt", "int", 1, AtlanComparisonOperator.GT),
            ("lt", "int", 1, AtlanComparisonOperator.LT),
            ("does_not_contain", "string", "abc", AtlanComparisonOperator.NOT_CONTAINS),
            ("contains", "string", "abc", AtlanComparisonOperator.CONTAINS),
            ("ends_with", "string", "abc", AtlanComparisonOperator.ENDS_WITH),
            ("starts_with", "string", "abc", AtlanComparisonOperator.STARTS_WITH),
        ],
    )
    def test_comparable_type(
        self,
        method: str,
        type_name: str,
        value,
        operator: AtlanComparisonOperator,
        sut: LineageFilterFieldCM,
        custom_metadata_field,
    ):
        self.configure_custom_metadata_field(custom_metadata_field, type_name=type_name)

        _filter = getattr(sut, method)(value)

        assert _filter.field == sut.field
        assert _filter.operator == operator
        assert _filter.value == str(value)

    @pytest.mark.parametrize(
        "method, query_type, type_name, value",
        [
            ("eq", "=", "boolean", 1),
            ("eq", "=", "int", True),
            ("neq", "!=", "boolean", 1),
            ("neq", "!=", "int", True),
            ("gt", ">", "boolean", 1),
            ("gte", ">=", "boolean", 1),
            ("lt", "<", "boolean", 1),
            ("lte", "<=", "boolean", 1),
            ("does_not_contain", "not_contains", "int", "abc"),
            ("contains", "contains", "int", "abc"),
            ("ends_with", "endsWith", "int", "abc"),
            ("starts_with", "startsWith", "int", "abc"),
        ],
    )
    def test_non_comparable_type_raises_atlan_error(
        self,
        method: str,
        query_type: str,
        type_name: str,
        value,
        sut: LineageFilterFieldCM,
        custom_metadata_field,
    ):
        self.configure_custom_metadata_field(custom_metadata_field, type_name=type_name)

        with pytest.raises(
            AtlanError,
            match=f"ATLAN-PYTHON-400-039 Cannot create a {query_type} query on field: something.an_attribute.",
        ):
            getattr(sut, method)(value)

    @pytest.mark.parametrize(
        "method, valid_types",
        [
            ("eq", "str, Enum, bool, int, float or date"),
            ("neq", "str, Enum, bool, int, float or date"),
            ("starts_with", "str"),
            ("lt", "int, float or date"),
            ("lte", "int, float or date"),
            ("gt", "int, float or date"),
            ("gte", "int, float or date"),
        ],
    )
    def test_method_with_wrong_type_raise_atlan_error(
        self, method, valid_types, sut: LineageFilterFieldCM
    ):
        with pytest.raises(
            AtlanError,
            match="ATLAN-PYTHON-400-048 Invalid parameter type for dict should be "
            + valid_types,
        ):
            getattr(sut, method)({})


class TestLineageFilterFieldNumeric:
    @pytest.fixture
    def sut(self, searchable_field: SearchableField) -> LineageFilterFieldNumeric:
        return LineageFilterFieldNumeric(field=searchable_field)

    def test_init(
        self, sut: LineageFilterFieldNumeric, searchable_field: SearchableField
    ):
        assert sut.field == searchable_field

    @pytest.mark.parametrize(
        "method",
        ["eq", "neq", "lt", "lte", "gt", "gte"],
    )
    def test_method_with_wrong_type_raise_atlan_error(
        self, method: str, sut: LineageFilterFieldNumeric
    ):
        with pytest.raises(
            AtlanError,
            match="ATLAN-PYTHON-400-048 Invalid parameter type for dict should be int, float or date",
        ):
            getattr(sut, method)({})

    @pytest.mark.parametrize(
        "method, operator",
        [
            ("eq", AtlanComparisonOperator.EQ),
            ("neq", AtlanComparisonOperator.NEQ),
            ("lt", AtlanComparisonOperator.LT),
            ("lte", AtlanComparisonOperator.LTE),
            ("gt", AtlanComparisonOperator.GT),
            ("gte", AtlanComparisonOperator.GTE),
        ],
    )
    @pytest.mark.parametrize("value", [1, 1.23, TODAY])
    def test_eq(self, method, operator, value, sut: LineageFilterFieldBoolean):
        _filter = getattr(sut, method)(value)
        assert _filter.field == sut.field
        assert _filter.operator == operator
        assert _filter.value == str(value)


class TestLineageFilterFieldString:
    @pytest.fixture
    def sut(self, searchable_field: SearchableField) -> LineageFilterFieldString:
        return LineageFilterFieldString(field=searchable_field)

    def test_init(
        self, sut: LineageFilterFieldString, searchable_field: SearchableField
    ):
        assert sut.field == searchable_field

    @pytest.mark.parametrize(
        "method",
        [
            "eq",
            "neq",
            "starts_with",
            "ends_with",
            "contains",
            "does_not_contain",
        ],
    )
    def test_method_with_wrong_type_raise_atlan_error(
        self, method: str, sut: LineageFilterFieldNumeric
    ):
        with pytest.raises(
            AtlanError,
            match="ATLAN-PYTHON-400-048 Invalid parameter type for dict should be int, float or date",
        ):
            getattr(sut, method)({})

    @pytest.mark.parametrize(
        "method, operator",
        [
            ("eq", AtlanComparisonOperator.EQ),
            ("neq", AtlanComparisonOperator.NEQ),
            ("starts_with", AtlanComparisonOperator.STARTS_WITH),
            ("ends_with", AtlanComparisonOperator.ENDS_WITH),
            ("contains", AtlanComparisonOperator.CONTAINS),
            ("does_not_contain", AtlanComparisonOperator.NOT_CONTAINS),
        ],
    )
    @pytest.mark.parametrize(
        "value, expected", [("abc", "abc"), (FileType.CSV, FileType.CSV.value)]
    )
    def test_eq(
        self, method, operator, value, expected, sut: LineageFilterFieldBoolean
    ):
        _filter = getattr(sut, method)(value)
        assert _filter.field == sut.field
        assert _filter.operator == operator
        assert _filter.value == expected


GOOD_DEPTH = 1
GOOD_EXCLUDE_MEANINGS = False
GOOD_EXCLUDE_CLASSIFICATIONS = True
GOOD_INCLUDES_IN_RESULTS: List[AtlanField] = []
GOOD_INCLUDE_ON_RESULTS: List[LineageFilter] = []
GOOD_WHERE_ASSETS: List[LineageFilter] = []
GOOD_WHERE_RELATIONSHIPS: List[LineageFilter] = []
BAD_STRING = True
GOOD_GUID = "123"
GOOD_SIZE = 10
GOOD_DIRECTION = LineageDirection.DOWNSTREAM
BAD_INT = 12.3
BAD_LINEAGE_DIRECTION = "abc"
BAD_BOOL = "True"
BAD_LINEAGE_FILTER_LIST = [{"field": "1", "operator": "eq", "value": "1"}]


class TestFluentLineage:
    @pytest.fixture()
    def sut(self) -> FluentLineage:
        return FluentLineage(starting_guid=GOOD_GUID)

    @pytest.mark.parametrize(
        "starting_guid, depth, direction, size, exclude_meanings, exclude_atlan_tags, includes_in_results, "
        "includes_on_results, where_assets, where_relationships, message",
        [
            (
                None,
                GOOD_DEPTH,
                GOOD_DIRECTION,
                GOOD_SIZE,
                GOOD_EXCLUDE_MEANINGS,
                GOOD_EXCLUDE_CLASSIFICATIONS,
                GOOD_INCLUDES_IN_RESULTS,
                GOOD_INCLUDE_ON_RESULTS,
                GOOD_WHERE_ASSETS,
                GOOD_WHERE_RELATIONSHIPS,
                r"1 validation error for Init\nstarting_guid\n  none is not an allowed value "
                r"\(type=type_error.none.not_allowed\)",
            ),
            (
                BAD_STRING,
                GOOD_DEPTH,
                GOOD_DIRECTION,
                GOOD_SIZE,
                GOOD_EXCLUDE_MEANINGS,
                GOOD_EXCLUDE_CLASSIFICATIONS,
                GOOD_INCLUDES_IN_RESULTS,
                GOOD_INCLUDE_ON_RESULTS,
                GOOD_WHERE_ASSETS,
                GOOD_WHERE_RELATIONSHIPS,
                r"1 validation error for Init\nstarting_guid\n  str type expected \(type=type_error.str\)",
            ),
            (
                GOOD_GUID,
                BAD_INT,
                GOOD_DIRECTION,
                GOOD_SIZE,
                GOOD_EXCLUDE_MEANINGS,
                GOOD_EXCLUDE_CLASSIFICATIONS,
                GOOD_INCLUDES_IN_RESULTS,
                GOOD_INCLUDE_ON_RESULTS,
                GOOD_WHERE_ASSETS,
                GOOD_WHERE_RELATIONSHIPS,
                r"1 validation error for Init\ndepth\n  value is not a valid integer \(type=type_error.integer\)",
            ),
            (
                GOOD_GUID,
                GOOD_DEPTH,
                BAD_LINEAGE_DIRECTION,
                GOOD_SIZE,
                GOOD_EXCLUDE_MEANINGS,
                GOOD_EXCLUDE_CLASSIFICATIONS,
                GOOD_INCLUDES_IN_RESULTS,
                GOOD_INCLUDE_ON_RESULTS,
                GOOD_WHERE_ASSETS,
                GOOD_WHERE_RELATIONSHIPS,
                r"1 validation error for Init\ndirection\n  value is not a valid enumeration member; permitted:",
            ),
            (
                GOOD_GUID,
                GOOD_DEPTH,
                LineageDirection.DOWNSTREAM,
                BAD_INT,
                GOOD_EXCLUDE_MEANINGS,
                GOOD_EXCLUDE_CLASSIFICATIONS,
                GOOD_INCLUDES_IN_RESULTS,
                GOOD_INCLUDE_ON_RESULTS,
                GOOD_WHERE_ASSETS,
                GOOD_WHERE_RELATIONSHIPS,
                r"1 validation error for Init\nsize\n  value is not a valid integer \(type=type_error.integer\)",
            ),
            (
                GOOD_GUID,
                GOOD_DEPTH,
                LineageDirection.DOWNSTREAM,
                GOOD_SIZE,
                BAD_BOOL,
                GOOD_EXCLUDE_CLASSIFICATIONS,
                GOOD_INCLUDES_IN_RESULTS,
                GOOD_INCLUDE_ON_RESULTS,
                GOOD_WHERE_ASSETS,
                GOOD_WHERE_RELATIONSHIPS,
                r"1 validation error for Init\nexclude_meanings\n  value is not a valid boolean "
                r"\(type=value_error.strictbool\)",
            ),
            (
                GOOD_GUID,
                GOOD_DEPTH,
                LineageDirection.DOWNSTREAM,
                GOOD_SIZE,
                GOOD_EXCLUDE_MEANINGS,
                BAD_BOOL,
                GOOD_INCLUDES_IN_RESULTS,
                GOOD_INCLUDE_ON_RESULTS,
                GOOD_WHERE_ASSETS,
                GOOD_WHERE_RELATIONSHIPS,
                r"1 validation error for Init\nexclude_atlan_tags\n  value is not a valid boolean "
                r"\(type=value_error.strictbool\)",
            ),
            (
                GOOD_GUID,
                GOOD_DEPTH,
                LineageDirection.DOWNSTREAM,
                GOOD_SIZE,
                GOOD_EXCLUDE_MEANINGS,
                GOOD_EXCLUDE_CLASSIFICATIONS,
                BAD_LINEAGE_FILTER_LIST,
                GOOD_INCLUDE_ON_RESULTS,
                GOOD_WHERE_ASSETS,
                GOOD_WHERE_RELATIONSHIPS,
                r"3 validation errors for Init\nincludes_in_results",
            ),
            (
                GOOD_GUID,
                GOOD_DEPTH,
                LineageDirection.DOWNSTREAM,
                GOOD_SIZE,
                GOOD_EXCLUDE_MEANINGS,
                GOOD_EXCLUDE_CLASSIFICATIONS,
                GOOD_INCLUDES_IN_RESULTS,
                BAD_LINEAGE_FILTER_LIST,
                GOOD_WHERE_ASSETS,
                GOOD_WHERE_RELATIONSHIPS,
                r"4 validation errors for Init\nincludes_on_results",
            ),
            (
                GOOD_GUID,
                GOOD_DEPTH,
                LineageDirection.DOWNSTREAM,
                GOOD_SIZE,
                GOOD_EXCLUDE_MEANINGS,
                GOOD_EXCLUDE_CLASSIFICATIONS,
                GOOD_INCLUDES_IN_RESULTS,
                GOOD_INCLUDE_ON_RESULTS,
                BAD_LINEAGE_FILTER_LIST,
                GOOD_WHERE_RELATIONSHIPS,
                r"3 validation errors for Init\nwhere_assets",
            ),
            (
                GOOD_GUID,
                GOOD_DEPTH,
                LineageDirection.DOWNSTREAM,
                GOOD_SIZE,
                GOOD_EXCLUDE_MEANINGS,
                GOOD_EXCLUDE_CLASSIFICATIONS,
                GOOD_INCLUDES_IN_RESULTS,
                GOOD_INCLUDE_ON_RESULTS,
                GOOD_WHERE_ASSETS,
                BAD_LINEAGE_FILTER_LIST,
                r"3 validation errors for Init\nwhere_relationships",
            ),
        ],
    )
    def test_init_with_bad_parameters_raise_value_error(
        self,
        starting_guid,
        depth,
        direction,
        size,
        exclude_meanings,
        exclude_atlan_tags,
        includes_in_results,
        includes_on_results,
        where_assets,
        where_relationships,
        message,
    ):
        with pytest.raises(ValueError, match=message):
            FluentLineage(
                starting_guid=starting_guid,
                depth=depth,
                direction=direction,
                size=size,
                exclude_meanings=exclude_meanings,
                exclude_atlan_tags=exclude_atlan_tags,
                includes_on_results=includes_on_results,
                includes_in_results=includes_in_results,
                where_assets=where_assets,
                where_relationships=where_relationships,
            )

    def test_request_with_defaults(self, sut: FluentLineage):
        request = sut.request

        assert request.guid == GOOD_GUID
        assert request.size == 10
        assert request.depth == 1000000
        assert request.direction == LineageDirection.DOWNSTREAM
        assert request.exclude_meanings is True
        assert request.exclude_classifications is True
        assert request.entity_filters is None
        assert request.entity_traversal_filters is None
        assert request.relationship_traversal_filters is None

    @pytest.mark.parametrize(
        "starting_guid, depth, direction, size, exclude_meanings, exclude_atlan_tags, includes_on_results, "
        "includes_in_results, where_assets, where_relationships",
        [
            (
                GOOD_GUID,
                GOOD_DEPTH,
                GOOD_DIRECTION,
                GOOD_SIZE,
                GOOD_EXCLUDE_MEANINGS,
                GOOD_EXCLUDE_CLASSIFICATIONS,
                [Asset.NAME],
                [Asset.CERTIFICATE_STATUS.in_lineage.eq(CertificateStatus.DRAFT)],
                [Asset.STATUS.in_lineage.eq(EntityStatus.ACTIVE)],
                [Asset.STATUS.in_lineage.eq(EntityStatus.DELETED)],
            ),
        ],
    )
    def test_request(
        self,
        starting_guid,
        depth,
        direction,
        size,
        exclude_meanings,
        exclude_atlan_tags,
        includes_on_results,
        includes_in_results,
        where_assets,
        where_relationships,
    ):
        request = FluentLineage(
            starting_guid=starting_guid,
            depth=depth,
            direction=direction,
            size=size,
            exclude_meanings=exclude_meanings,
            exclude_atlan_tags=exclude_atlan_tags,
            includes_on_results=includes_on_results,
            includes_in_results=includes_in_results,
            where_assets=where_assets,
            where_relationships=where_relationships,
        ).request

        assert request.guid == GOOD_GUID
        assert request.size == size
        assert request.depth == depth
        assert request.direction == direction
        assert request.exclude_meanings == exclude_meanings
        assert request.exclude_classifications == exclude_atlan_tags
        assert request.attributes == [
            field.atlan_field_name for field in includes_on_results
        ]
        self.validate_filter(
            filter_=request.entity_filters,
            filter_condition=FilterList.Condition.AND,
            results=includes_in_results,
        )
        self.validate_filter(
            filter_=request.entity_traversal_filters,
            filter_condition=FilterList.Condition.AND,
            results=where_assets,
        )
        self.validate_filter(
            filter_=request.relationship_traversal_filters,
            filter_condition=FilterList.Condition.AND,
            results=where_relationships,
        )
        request = FluentLineage(
            starting_guid=starting_guid,
            depth=depth,
            direction=direction,
            size=size,
            exclude_meanings=exclude_meanings,
            exclude_atlan_tags=exclude_atlan_tags,
            includes_on_results=includes_on_results,
            includes_in_results=includes_in_results,
            includes_condition=FilterList.Condition.OR,
            where_assets=where_assets,
            assets_condition=FilterList.Condition.OR,
            where_relationships=where_relationships,
            relationships_condition=FilterList.Condition.OR,
        ).request

        assert request.guid == GOOD_GUID
        assert request.size == size
        assert request.depth == depth
        assert request.direction == direction
        assert request.exclude_meanings == exclude_meanings
        assert request.exclude_classifications == exclude_atlan_tags
        assert request.attributes == [
            field.atlan_field_name for field in includes_on_results
        ]
        self.validate_filter(
            filter_=request.entity_filters,
            filter_condition=FilterList.Condition.OR,
            results=includes_in_results,
        )
        self.validate_filter(
            filter_=request.entity_traversal_filters,
            filter_condition=FilterList.Condition.OR,
            results=where_assets,
        )
        self.validate_filter(
            filter_=request.relationship_traversal_filters,
            filter_condition=FilterList.Condition.OR,
            results=where_relationships,
        )

    @staticmethod
    def validate_filter(filter_, filter_condition, results):
        assert filter_.condition == filter_condition
        assert len(filter_.criteria) == len(results)
        for entity_filter, include_in in zip(filter_.criteria, results):
            assert entity_filter.attribute_name == include_in.field.internal_field_name
            assert entity_filter.operator == include_in.operator
            assert entity_filter.attribute_value == include_in.value

    @pytest.mark.parametrize(
        "method, value, message",
        [
            (
                "depth",
                False,
                r"ATLAN-PYTHON-400-048 Invalid parameter type for depth should be int",
            ),
            (
                "direction",
                False,
                r"ATLAN-PYTHON-400-048 Invalid parameter type for direction should be LineageDirection",
            ),
            (
                "size",
                False,
                r"ATLAN-PYTHON-400-048 Invalid parameter type for size should be int",
            ),
            (
                "exclude_atlan_tags",
                1,
                r"ATLAN-PYTHON-400-048 Invalid parameter type for exclude_atlan_tags should be bool",
            ),
            (
                "exclude_meanings",
                1,
                r"ATLAN-PYTHON-400-048 Invalid parameter type for exclude_meanings should be bool",
            ),
            (
                "include_on_results",
                1,
                r"ATLAN-PYTHON-400-048 Invalid parameter type for field should be str, AtlanField",
            ),
            (
                "include_in_results",
                1,
                r"ATLAN-PYTHON-400-048 Invalid parameter type for lineage_filter should be LineageFilter. "
                r"Suggestion: Check that you have used the correct type of parameter.",
            ),
            (
                "where_assets",
                1,
                r"ATLAN-PYTHON-400-048 Invalid parameter type for lineage_filter should be LineageFilter. "
                r"Suggestion: Check that you have used the correct type of parameter.",
            ),
            (
                "where_relationships",
                1,
                r"ATLAN-PYTHON-400-048 Invalid parameter type for lineage_filter should be LineageFilter. "
                r"Suggestion: Check that you have used the correct type of parameter.",
            ),
        ],
    )
    def test_methods_with_invalid_parameter_raises_invalid_request_error(
        self, method, value, message, sut: FluentLineage
    ):
        with pytest.raises(InvalidRequestError, match=message):
            getattr(sut, method)(value)

    @pytest.mark.parametrize(
        "method, value",
        [
            ("depth", 12),
            ("direction", LineageDirection.BOTH),
            ("size", 12),
            ("exclude_atlan_tags", True),
            ("exclude_meanings", True),
        ],
    )
    def test_method_with_valid_parameter(self, method, value, sut: FluentLineage):
        lineage = getattr(sut, method)(value)

        assert lineage is not sut
        assert getattr(lineage, f"_{method}") == value

    @pytest.mark.parametrize(
        "method, value, internal_name",
        [
            ("include_on_results", Asset.NAME, "_includes_on_results"),
            (
                "include_in_results",
                Asset.STATUS.in_lineage.eq(EntityStatus.ACTIVE),
                "_includes_in_results",
            ),
            (
                "where_assets",
                Asset.STATUS.in_lineage.eq(EntityStatus.ACTIVE),
                "_where_assets",
            ),
            (
                "where_relationships",
                Asset.STATUS.in_lineage.eq(EntityStatus.ACTIVE),
                "_where_relationships",
            ),
        ],
    )
    def test_method_adds_to_list_valid_parameter(
        self, method, value, internal_name, sut: FluentLineage
    ):
        lineage = getattr(sut, method)(value)

        assert lineage is not sut
        assert value in getattr(lineage, internal_name)
