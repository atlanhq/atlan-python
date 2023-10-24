# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import json
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
    LineageGraph,
    LineageRelation,
    LineageResponse,
)
from pyatlan.model.typedef import AttributeDef

BASE_GUID_TARGET = "e44ed3a2-1de5-4f23-b3f1-6e005156fee9"

DATA_DIR = Path(__file__).parent / "data"
BASE_GUID = "75474eab-3105-4ef9-9f84-709e386a7d3e"


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

    def test_starts_with_comparable_type(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        value = "abc"
        self.configure_custom_metadata_field(custom_metadata_field, type_name="string")

        filter = sut.starts_with(value=value)

        assert filter.field == sut.field
        assert filter.operator == AtlanComparisonOperator.STARTS_WITH
        assert filter.value == value

    def test_starts_with_incomparable_type_raises_atlan_error(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        self.configure_custom_metadata_field(custom_metadata_field, type_name="int")

        with pytest.raises(
            AtlanError,
            match="ATLAN-PYTHON-400-039 Cannot create a startsWith query on field: something.an_attribute",
        ):
            sut.starts_with(value="abc")

    def test_ends_with_comparable_type(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        value = "abc"
        self.configure_custom_metadata_field(custom_metadata_field, type_name="string")

        filter = sut.ends_with(value=value)

        assert filter.field == sut.field
        assert filter.operator == AtlanComparisonOperator.ENDS_WITH
        assert filter.value == value

    def test_ends_with_incomparable_type_raises_atlan_error(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        self.configure_custom_metadata_field(custom_metadata_field, type_name="int")

        with pytest.raises(
            AtlanError,
            match="ATLAN-PYTHON-400-039 Cannot create a endsWith query on field: something.an_attribute",
        ):
            sut.ends_with(value="abc")

    def test_contains_comparable_type(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        value = "abc"
        self.configure_custom_metadata_field(custom_metadata_field, type_name="string")

        filter = sut.contains(value=value)

        assert filter.field == sut.field
        assert filter.operator == AtlanComparisonOperator.CONTAINS
        assert filter.value == value

    def test_contains_with_incomparable_type_raises_atlan_error(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        value = "abc"
        self.configure_custom_metadata_field(custom_metadata_field, type_name="int")

        with pytest.raises(
            AtlanError,
            match="ATLAN-PYTHON-400-039 Cannot create a contains query on field: something.an_attribute",
        ):
            sut.contains(value=value)

    def test_does_not_contain_comparable_type(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        value = "abc"
        self.configure_custom_metadata_field(custom_metadata_field, type_name="string")

        filter = sut.does_not_contain(value=value)

        assert filter.field == sut.field
        assert filter.operator == AtlanComparisonOperator.NOT_CONTAINS
        assert filter.value == value

    def test_does_not_contain_incomparable_type_raises_atlan_error(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        self.configure_custom_metadata_field(custom_metadata_field, type_name="int")

        with pytest.raises(
            AtlanError,
            match="ATLAN-PYTHON-400-039 Cannot create a not_contains query on field: something.an_attribute",
        ):
            sut.does_not_contain(value="abc")

    def test_less_than_comparable_type(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        self.configure_custom_metadata_field(custom_metadata_field, type_name="int")
        value = 1

        filter = sut.lt(value=value)

        assert filter.field == sut.field
        assert filter.operator == AtlanComparisonOperator.LT
        assert filter.value == str(value)

    def test_less_than_non_comparable_type_raises_atlan_error(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        self.configure_custom_metadata_field(custom_metadata_field, type_name="boolean")

        with pytest.raises(
            AtlanError,
            match="ATLAN-PYTHON-400-039 Cannot create a < query on field: something.an_attribute.",
        ):
            sut.lt(value=1)

    def test_less_than_invalid_parameter_raises_atlan_error(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        self.configure_custom_metadata_field(custom_metadata_field, type_name="int")

        with pytest.raises(
            AtlanError,
            match="ATLAN-PYTHON-400-048 Invalid parameter type for bool should be int, float or date",
        ):
            sut.lt(value=True)

    def test_greater_than_comparable_type(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        self.configure_custom_metadata_field(custom_metadata_field, type_name="int")
        value = 1

        filter = sut.gt(value=value)

        assert filter.field == sut.field
        assert filter.operator == AtlanComparisonOperator.GT
        assert filter.value == str(value)

    def test_greater_than_non_comparable_type_raises_atlan_error(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        self.configure_custom_metadata_field(custom_metadata_field, type_name="boolean")

        with pytest.raises(
            AtlanError,
            match="ATLAN-PYTHON-400-039 Cannot create a > query on field: something.an_attribute.",
        ):
            sut.gt(value=1)

    def test_greater_than_invalid_parameter_raises_atlan_error(
        self, sut: LineageFilterFieldCM, custom_metadata_field
    ):
        self.configure_custom_metadata_field(custom_metadata_field, type_name="int")

        with pytest.raises(
            AtlanError,
            match="ATLAN-PYTHON-400-048 Invalid parameter type for bool should be int, float or date",
        ):
            sut.gt(value=True)

    @pytest.mark.parametrize(
        "method, valid_types",
        [("eq", "str or Enum"), ("neq", "str or Enum"), ("starts_with", "str")],
    )
    def test_method_with_wrong_type_raise_atlan_error(
        self, method, valid_types, sut: LineageFilterFieldCM
    ):
        with pytest.raises(
            AtlanError,
            match="ATLAN-PYTHON-400-048 Invalid parameter type for int should be "
            + valid_types,
        ):
            getattr(sut, method)(1)
