# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import json
from datetime import date
from pathlib import Path
from unittest.mock import Mock

import pytest

from pyatlan.errors import AtlanError, InvalidRequestError
from pyatlan.model.enums import AtlanComparisonOperator, FileType
from pyatlan.model.fields.atlan_fields import CustomMetadataField, SearchableField
from pyatlan.model.lineage import (
    LineageFilterField,
    LineageFilterFieldBoolean,
    LineageFilterFieldCM,
    LineageFilterFieldNumeric,
    LineageFilterFieldString,
    LineageGraph,
    LineageRelation,
    LineageResponse,
)
from pyatlan.model.typedef import AttributeDef

BASE_GUID_TARGET = "e44ed3a2-1de5-4f23-b3f1-6e005156fee9"

DATA_DIR = Path(__file__).parent / "data"
BASE_GUID = "75474eab-3105-4ef9-9f84-709e386a7d3e"
TODAY = date.today()


@pytest.fixture(scope="session")
def lineage_response_json():
    with (DATA_DIR / "lineage_response.json").open() as input_file:
        return json.load(input_file)


@pytest.fixture(scope="session")
def lineage_response(lineage_response_json):
    return LineageResponse(**lineage_response_json)


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
        filter = sut.has_any_value()
        assert filter.field == sut.field
        assert filter.operator == AtlanComparisonOperator.NOT_NULL
        assert filter.value == ""

    def test_has_no_value(self, sut: LineageFilterField):
        filter = sut.has_no_value()
        assert filter.field == sut.field
        assert filter.operator == AtlanComparisonOperator.IS_NULL
        assert filter.value == ""


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
        filter = sut.eq(value)
        assert filter.field == sut.field
        assert filter.operator == AtlanComparisonOperator.EQ
        assert filter.value == expected

    @pytest.mark.parametrize(
        "value, expected", [(True, str(True)), (False, str(False))]
    )
    def test_neq(self, value, expected, sut: LineageFilterFieldBoolean):
        filter = sut.neq(value)
        assert filter.field == sut.field
        assert filter.operator == AtlanComparisonOperator.NEQ
        assert filter.value == expected


class TestLineageFilterFieldCM:
    @pytest.fixture()
    def custom_metadata_field(self) -> CustomMetadataField:
        return Mock(spec=CustomMetadataField)

    @pytest.fixture
    def sut(self, custom_metadata_field: CustomMetadataField) -> LineageFilterFieldCM:
        return LineageFilterFieldCM(field=custom_metadata_field)

    def configure_custom_metadata_field(self, custom_metadata_field, type_name):
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
        filter = sut.eq(value)
        assert filter.field == sut.field
        assert filter.operator == AtlanComparisonOperator.EQ
        assert filter.value == expected

    @pytest.mark.parametrize(
        "value, expected", [("value", "value"), (FileType.CSV, FileType.CSV.value)]
    )
    def test_neq(self, value, expected, sut: LineageFilterFieldCM):
        filter = sut.neq(value)
        assert filter.field == sut.field
        assert filter.operator == AtlanComparisonOperator.NEQ
        assert filter.value == expected

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

        filter = getattr(sut, method)(value)

        assert filter.field == sut.field
        assert filter.operator == operator
        assert filter.value == str(value)

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
        [("eq"), ("neq"), ("lt"), ("lte"), ("gt"), ("gte")],
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
    @pytest.mark.parametrize("value", [(1), (1.23), (TODAY)])
    def test_eq(self, method, operator, value, sut: LineageFilterFieldBoolean):
        filter = getattr(sut, method)(value)
        assert filter.field == sut.field
        assert filter.operator == operator
        assert filter.value == str(value)


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
            ("eq"),
            ("neq"),
            ("starts_with"),
            ("ends_with"),
            ("contains"),
            ("does_not_contain"),
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
        filter = getattr(sut, method)(value)
        assert filter.field == sut.field
        assert filter.operator == operator
        assert filter.value == expected
