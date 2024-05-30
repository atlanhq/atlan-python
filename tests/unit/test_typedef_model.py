# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import json
import random
from pathlib import Path
from re import escape
from unittest.mock import Mock, patch

import pytest

from pyatlan.cache.enum_cache import EnumCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.client.common import ApiCaller
from pyatlan.errors import InvalidRequestError, NotFoundError
from pyatlan.model.enums import AtlanCustomAttributePrimitiveType, AtlanTypeCategory
from pyatlan.model.typedef import (
    AtlanTagDef,
    AttributeDef,
    CustomMetadataDef,
    EntityDef,
    EnumDef,
    RelationshipDef,
    StructDef,
    TypeDef,
    TypeDefResponse,
    _all_domain_types,
    _all_glossary_types,
    _all_other_types,
    _complete_type_list,
)
from pyatlan.model.utils import to_camel_case, to_snake_case
from tests.unit.constants import (
    APPLICABLE_ASSET_TYPES,
    APPLICABLE_CONNECTIONS,
    APPLICABLE_DOMAIN_TYPES,
    APPLICABLE_DOMAINS,
    APPLICABLE_ENTITY_TYPES,
    APPLICABLE_GLOSSARIES,
    APPLICABLE_GLOSSARY_TYPES,
    APPLICABLE_OTHER_ASSET_TYPES,
    TEST_ATTRIBUTE_DEF_APPLICABLE_ASSET_TYPES,
    TEST_ENUM_DEF,
    TEST_STRUCT_DEF,
)

PARENT_DIR = Path(__file__).parent
TYPEDEFS_JSON = PARENT_DIR / "data" / "typedefs.json"


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")


@pytest.fixture()
def client():
    return AtlanClient()


@pytest.fixture(scope="module")
def mock_api_caller():
    return Mock(spec=ApiCaller)


@pytest.fixture()
def type_defs():
    with TYPEDEFS_JSON.open() as input_file:
        return json.load(input_file)


def check_type_def_properties(type_def: TypeDef, source: dict):
    def check_property(property_name: str):
        key = to_camel_case(property_name)
        value = getattr(type_def, property_name)
        if key in source:
            assert value == source[key]
        else:
            assert value is None

    check_property("create_time")
    check_property("created_by")
    check_property("description")
    check_property("guid")
    check_property("name")
    check_property("type_version")
    check_property("update_time")
    check_property("updated_by")
    check_property("version")


def check_attribute(model: object, attribute_name: str, source: dict):
    key = to_camel_case(attribute_name)
    attribute = getattr(model, attribute_name)
    if key in source:
        value = source[key]
        value = type(attribute)(value)
        assert attribute == value
    else:
        assert getattr(model, attribute_name) is None


def check_has_attributes(type_def: TypeDef, type_def_json: dict):
    for key in type_def_json:
        attribute_name = to_snake_case(key)
        assert hasattr(type_def, attribute_name)


class TestEnumDef:
    @pytest.fixture()
    def mock_get_enum_cache(self):
        with patch.object(EnumCache, "get_cache") as cache:
            yield cache

    def test_create_element_def(self):
        element_def = EnumDef.ElementDef(**(TEST_ENUM_DEF["elementDefs"][0]))
        assert element_def.description == TEST_ENUM_DEF["elementDefs"][0]["description"]
        assert element_def.value == TEST_ENUM_DEF["elementDefs"][0]["value"]
        assert element_def.ordinal == TEST_ENUM_DEF["elementDefs"][0]["ordinal"]

    def test_create_enum_def(self):
        enum_def = EnumDef(**TEST_ENUM_DEF)
        assert enum_def.category == AtlanTypeCategory.ENUM
        assert len(enum_def.element_defs) == 5
        check_type_def_properties(enum_def, TEST_ENUM_DEF)

    def test_enum_defs(self, type_defs):
        for enum_def_json in type_defs["enumDefs"]:
            enum_def = EnumDef(**enum_def_json)
            assert enum_def.category == AtlanTypeCategory.ENUM
            check_type_def_properties(enum_def, enum_def_json)

    @pytest.mark.parametrize(
        "test_name, test_values, error_msg",
        [
            [None, ["val1", "val2"], "name is required"],
            ["my_enum", None, "values is required"],
        ],
    )
    def test_enum_create_method_required_parameters(
        self, test_name, test_values, error_msg
    ):
        with pytest.raises(ValueError) as err:
            EnumDef.create(name=test_name, values=test_values)
        assert error_msg in str(err.value)

    def test_create_method(self):
        enum = EnumDef.create(name="test-enum", values=["test-val1", "test-val2"])
        assert enum
        assert enum.name == "test-enum"
        assert enum.category == AtlanTypeCategory.ENUM
        assert enum.element_defs
        assert len(enum.element_defs) == 2
        assert enum.element_defs[0].value == "test-val1"
        assert enum.element_defs[1].value == "test-val2"

    def test_update_method_enum_not_found(self, client, mock_get_enum_cache):
        mock_get_by_name = Mock(return_value=None)
        mock_get_enum_cache.return_value._get_by_name = mock_get_by_name

        with pytest.raises(
            NotFoundError,
            match="ATLAN-PYTHON-404-013 Enumeration with name test-enum does not exist.",
        ):
            EnumDef.update(
                name="test-enum",
                values=["test-val1", "test-val2"],
                replace_existing=False,
            )

    def test_update_method(self, client, mock_get_enum_cache):
        existing_enum = {
            "name": "test-enum",
            "elementDefs": [{"value": "test-val0"}],
        }
        mock_get_by_name = Mock(return_value=EnumDef(**existing_enum))
        mock_get_enum_cache.return_value._get_by_name = mock_get_by_name
        enum = EnumDef.update(
            name="test-enum", values=["test-val1", "test-val2"], replace_existing=False
        )
        assert enum
        assert enum.name == "test-enum"
        assert enum.category == AtlanTypeCategory.ENUM
        assert enum.element_defs
        assert len(enum.element_defs) == 3
        assert enum.element_defs[0].value == "test-val0"
        assert enum.element_defs[1].value == "test-val1"
        assert enum.element_defs[2].value == "test-val2"

        # Test no duplication
        existing_enum = {
            "name": "test-enum",
            "elementDefs": [
                {"value": "test-val0"},
                {"value": "test-val1"},
                {"value": "test-val2"},
            ],
        }
        mock_get_by_name = Mock(return_value=EnumDef(**existing_enum))
        mock_get_enum_cache.return_value._get_by_name = mock_get_by_name
        enum = EnumDef.update(
            name="test-enum", values=["test-val1", "test-val2"], replace_existing=False
        )
        assert enum
        assert enum.name == "test-enum"
        assert enum.category == AtlanTypeCategory.ENUM
        assert enum.element_defs
        assert len(enum.element_defs) == 3
        assert enum.element_defs[0].value == "test-val0"
        assert enum.element_defs[1].value == "test-val1"
        assert enum.element_defs[2].value == "test-val2"

        # Test with existing values and ordering
        existing_enum = {
            "name": "test-enum",
            "elementDefs": [
                {"value": "test-val0"},
                {"value": "test-val1"},
                {"value": "test-val2"},
            ],
        }
        mock_get_by_name = Mock(return_value=EnumDef(**existing_enum))
        mock_get_enum_cache.return_value._get_by_name = mock_get_by_name
        enum = EnumDef.update(
            name="test-enum",
            values=["new1", "test-val1", "new2", "test-val2", "new3", "new4"],
            replace_existing=False,
        )
        assert enum
        assert enum.name == "test-enum"
        assert enum.category == AtlanTypeCategory.ENUM
        assert enum.element_defs
        assert len(enum.element_defs) == 7
        assert enum.element_defs[0].value == "test-val0"
        assert enum.element_defs[1].value == "test-val1"
        assert enum.element_defs[2].value == "test-val2"
        # Make sure new ones are always append
        assert enum.element_defs[3].value == "new1"
        assert enum.element_defs[4].value == "new2"
        assert enum.element_defs[5].value == "new3"
        assert enum.element_defs[6].value == "new4"

        # Test when `replace_existing` is `True`
        existing_enum = {
            "name": "test-enum",
            "elementDefs": [
                {"value": "test-val0"},
                {"value": "test-val1"},
                {"value": "test-val2"},
            ],
        }
        mock_get_by_name = Mock(return_value=EnumDef(**existing_enum))
        mock_get_enum_cache.return_value._get_by_name = mock_get_by_name
        enum = EnumDef.update(
            name="test-enum",
            values=["new1", "test-val1", "new2", "test-val2", "new3", "new4"],
            replace_existing=True,
        )
        assert enum
        assert enum.name == "test-enum"
        assert enum.category == AtlanTypeCategory.ENUM
        assert enum.element_defs
        assert len(enum.element_defs) == 6
        assert enum.element_defs[0].value == "new1"
        assert enum.element_defs[1].value == "test-val1"
        assert enum.element_defs[2].value == "new2"
        assert enum.element_defs[3].value == "test-val2"
        assert enum.element_defs[4].value == "new3"
        assert enum.element_defs[5].value == "new4"


class TestStuctDef:
    @pytest.mark.skip("Need get a new version of the typedefs.json file")
    def test_struct_defs(self, type_defs):
        for struct_def_json in type_defs["structDefs"]:
            struct_def = StructDef(**struct_def_json)
            assert struct_def.category == AtlanTypeCategory.STRUCT
            check_type_def_properties(struct_def, struct_def_json)
            for index, attribute_def in enumerate(struct_def.attribute_defs):
                attribute_defs = struct_def_json["attributeDefs"][index]
                for key in attribute_def.__dict__.keys():
                    check_attribute(attribute_def, key, attribute_defs)
            check_has_attributes(struct_def, struct_def_json)

    def test_create_struct_def(self):
        struct_def = StructDef(**TEST_STRUCT_DEF)
        assert struct_def.category == AtlanTypeCategory.STRUCT
        check_type_def_properties(struct_def, TEST_STRUCT_DEF)
        for index, attribute_def in enumerate(struct_def.attribute_defs):
            attribute_defs = TEST_STRUCT_DEF["attributeDefs"][index]
            for key in attribute_def.__dict__.keys():
                check_attribute(attribute_def, key, attribute_defs)


class TestAtlanTagDef:
    def test_classification_def(self, type_defs):
        for classification_def_json in type_defs["classificationDefs"]:
            classification_def = AtlanTagDef(**classification_def_json)
            assert classification_def.category == AtlanTypeCategory.CLASSIFICATION
            check_type_def_properties(classification_def, classification_def_json)
            check_has_attributes(classification_def, classification_def_json)


class TestEntityDef:
    def test_entity_def(self, type_defs):
        for entity_def_json in type_defs["entityDefs"]:
            entity_def = EntityDef(**entity_def_json)
            assert entity_def.category == AtlanTypeCategory.ENTITY
            check_type_def_properties(entity_def, entity_def_json)
            check_has_attributes(entity_def, entity_def_json)


class TestRelationshipDef:
    def test_relationship_def(self, type_defs):
        for relationship_def_json in type_defs["relationshipDefs"]:
            relationship_def = RelationshipDef(**relationship_def_json)
            assert relationship_def.category == AtlanTypeCategory.RELATIONSHIP
            check_type_def_properties(relationship_def, relationship_def_json)
            check_has_attributes(relationship_def, relationship_def_json)


class TestCustomMetadataDef:
    def test_business_metadata_def(self, type_defs):
        for business_metadata_def_json in type_defs["businessMetadataDefs"]:
            business_metadata_def = CustomMetadataDef(**business_metadata_def_json)
            assert business_metadata_def.category == AtlanTypeCategory.CUSTOM_METADATA
            check_type_def_properties(business_metadata_def, business_metadata_def_json)
            check_has_attributes(business_metadata_def, business_metadata_def_json)


class TestTypeDefResponse:
    def test_type_def_response(self, type_defs):
        type_def_response = TypeDefResponse(**type_defs)
        assert isinstance(type_def_response, TypeDefResponse)


class TestAttributeDef:
    @pytest.fixture()
    def sut(self) -> AttributeDef:
        with patch("pyatlan.model.typedef._get_all_qualified_names") as mock_get_qa:
            mock_get_qa.return_value = set()
            return AttributeDef.create(
                display_name="My Count",
                attribute_type=AtlanCustomAttributePrimitiveType.INTEGER,
            )

    @pytest.mark.parametrize(
        "attribute, value",
        [
            (APPLICABLE_ASSET_TYPES, {"Table"}),
            (APPLICABLE_GLOSSARY_TYPES, {"AtlasGlossary"}),
            (APPLICABLE_DOMAIN_TYPES, {"DataDomain", "DataProduct"}),
            (APPLICABLE_OTHER_ASSET_TYPES, {"File"}),
            (APPLICABLE_ENTITY_TYPES, {"Asset"}),
        ],
    )
    def test_applicable_types_with_no_options_raises_invalid_request_error(
        self, attribute, value, sut: AttributeDef
    ):
        sut = AttributeDef()

        with pytest.raises(
            InvalidRequestError,
            match="ATLAN-PYTHON-400-050 Options is not present in the AttributeDef",
        ):
            setattr(sut, attribute, value)

    @pytest.mark.parametrize(
        "attribute, value, message",
        TEST_ATTRIBUTE_DEF_APPLICABLE_ASSET_TYPES,
    )
    def test_applicable_types_with_invalid_type_raises_invalid_request_error(
        self, attribute, value, message, sut: AttributeDef
    ):
        with pytest.raises(InvalidRequestError, match=escape(message)):
            setattr(sut, attribute, value)

    @pytest.mark.parametrize(
        "attribute, value",
        [
            (APPLICABLE_ASSET_TYPES, {random.choice(list(_complete_type_list))}),
            (APPLICABLE_GLOSSARY_TYPES, {random.choice(list(_all_glossary_types))}),
            (APPLICABLE_DOMAIN_TYPES, {random.choice(list(_all_domain_types))}),
            (APPLICABLE_OTHER_ASSET_TYPES, {random.choice(list(_all_other_types))}),
            (APPLICABLE_ENTITY_TYPES, {"Asset"}),
            (APPLICABLE_CONNECTIONS, {"default/snowflake/1699268171"}),
            (APPLICABLE_GLOSSARIES, {"8Jdg4PdxcURBBNDt2RZD3"}),
            (APPLICABLE_DOMAINS, {"default/domain/uuBI8WSqeom1PXs7oo20L/super"}),
        ],
    )
    def test_applicable_types_with_valid_value(
        self, attribute, value, sut: AttributeDef
    ):
        setattr(sut, attribute, value)
        assert getattr(sut, attribute) == value
        options = sut.options
        assert getattr(options, attribute) == json.dumps(list(value))

    def test_attribute_create_with_limited_applicability(self):
        applicable_kwargs = dict(
            applicable_asset_types={"Link"},
            applicable_other_asset_types={"File"},
            applicable_glossaries={"8Jdg4PdxcURBBNDt2RZD3"},
            applicable_glossary_types={"AtlasGlossaryTerm", "AtlasGlossaryCategory"},
            applicable_domain_types={"DataDomain", "DataProduct"},
            applicable_connections={
                "default/snowflake/1699268171",
                "default/snowflake/16992681799",
            },
            applicable_domains={"default/domain/uuBI8WSqeom1PXs7oo20L/super"},
        )
        attribute_def_with_limited = AttributeDef.create(
            display_name="test-attr-def",
            attribute_type=AtlanCustomAttributePrimitiveType.STRING,
            # Optional kwargs that allow limiting
            # the applicability of an attribute within Atlan
            **applicable_kwargs
        )

        assert attribute_def_with_limited
        assert attribute_def_with_limited.options
        options = attribute_def_with_limited.options
        for attribute in applicable_kwargs.keys():
            assert getattr(
                attribute_def_with_limited, attribute
            ) == applicable_kwargs.get(attribute)
            assert getattr(options, attribute) == json.dumps(
                list(applicable_kwargs.get(attribute))
            )
