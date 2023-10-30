import pytest

from pyatlan.model.assets import Asset
from pyatlan.model.enums import CertificateStatus, EntityStatus, LineageDirection
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.model.lineage import FluentLineage, LineageFilter

GOOD_DEPTH = 1
GOOD_EXCLUDE_MEANINGS = False
GOOD_EXCLUDE_CLASSIFICATIONS = True
GOOD_INCLUDES_IN_RESULTS: list[AtlanField] = []
GOOD_INCLUDE_ON_RESULTS: list[LineageFilter] = []
GOOD_WHERE_ASSETS: list[LineageFilter] = []
GOOD_WHERE_RELATIONSHIPS: list[LineageFilter] = []
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
        "starting_guid, depth, direction, size, exclude_meanings, exclude_classifications, includes_in_results, "
        "include_on_results, where_assets, where_relationships, message",
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
                r"1 validation error for Init\nexclude_classifications\n  value is not a valid boolean "
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
                r"2 validation errors for Init\nincludes_in_results",
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
                r"1 validation error for Init\ninclude_on_results",
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
                r"2 validation errors for Init\nwhere_assets",
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
                r"2 validation errors for Init\nwhere_relationships",
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
        exclude_classifications,
        includes_in_results,
        include_on_results,
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
                exclude_classifications=exclude_classifications,
                include_on_results=include_on_results,
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
        "starting_guid, depth, direction, size, exclude_meanings, exclude_classifications, include_on_results, "
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
    def test_reqeust(
        self,
        starting_guid,
        depth,
        direction,
        size,
        exclude_meanings,
        exclude_classifications,
        include_on_results,
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
            exclude_classifications=exclude_classifications,
            include_on_results=include_on_results,
            includes_in_results=includes_in_results,
            where_assets=where_assets,
            where_relationships=where_relationships,
        ).request

        assert request.guid == GOOD_GUID
        assert request.size == size
        assert request.depth == depth
        assert request.direction == direction
        assert request.exclude_meanings == exclude_meanings
        assert request.exclude_classifications == exclude_classifications
        assert request.attributes == [
            field.atlan_field_name for field in include_on_results
        ]
        self.validate_filter(request.entity_filters, includes_in_results)
        self.validate_filter(request.entity_traversal_filters, where_assets)
        self.validate_filter(
            request.relationship_traversal_filters, where_relationships
        )

    def validate_filter(self, filter, results):
        assert filter.condition == "AND"
        assert len(filter.criteria) == len(results)
        for entity_filter, include_in in zip(filter.criteria, results):
            assert entity_filter.attribute_name == include_in.field.internal_field_name
            assert entity_filter.operator == include_in.operator
            assert entity_filter.attribute_value == include_in.value
