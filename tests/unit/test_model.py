# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import json
from datetime import datetime
from inspect import signature
from pathlib import Path
from unittest.mock import create_autospec, patch

import pytest
from deepdiff import DeepDiff
from pydantic.error_wrappers import ValidationError

import pyatlan.cache.classification_cache
from pyatlan.cache.custom_metadata_cache import CustomMetadataCache
from pyatlan.model.assets import (
    ADLSAccountStatus,
    ADLSEncryptionTypes,
    ADLSReplicationType,
    Asset,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    AtlasServer,
    AwsTag,
    AzureTag,
    BadgeCondition,
    ColumnValueFrequencyMap,
    Connection,
    Database,
    DbtMetricFilter,
    GoogleLabel,
    GoogleTag,
    Histogram,
    PopularityInsights,
    Readme,
    S3Bucket,
    S3Object,
    Schema,
    Table,
    View,
    validate_single_required_field,
)
from pyatlan.model.core import Announcement, AssetResponse
from pyatlan.model.enums import (
    ADLSAccessTier,
    ADLSLeaseState,
    ADLSLeaseStatus,
    ADLSObjectArchiveStatus,
    ADLSObjectType,
    ADLSPerformance,
    ADLSProvisionState,
    ADLSStorageKind,
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    GoogleDatastudioAssetType,
    IconType,
    KafkaTopicCompressionType,
    PowerbiEndorsement,
    QueryUsernameStrategy,
    QuickSightAnalysisStatus,
    QuickSightDatasetFieldType,
    QuickSightDatasetImportMode,
    QuickSightFolderType,
    SourceCostUnitType,
)
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.structs import KafkaTopicConsumption
from pyatlan.model.typedef import TypeDefResponse

SCHEMA_QUALIFIED_NAME = "default/snowflake/1646836521/ATLAN_SAMPLE_DATA/FOOD_BEVERAGE"

TABLE_NAME = "MKT_EXPENSES"

TABLE_URL = "POsWut55wIYsXZ5v4z3K98"

FRESHNESS = "VdRC4dyNdTJHfFjCiNaKt9"

MONTE_CARLO = "AFq4ctARP76ctapiTbuT92"

MOON = "FAq4ctARP76ctapiTbuT92"

DATA_DIR = Path(__file__).parent / "data"
GLOSSARY_JSON = "glossary.json"
GLOSSARY_TERM_JSON = "glossary_term.json"
GLOSSARY_CATEGORY_JSON = "glossary_category.json"
STRING_VALUE = "Bob"
INT_VALUE = 42
FLOAT_VALUE = 42.00
ATTRIBUTE_VALUES_BY_TYPE = {
    "str": STRING_VALUE,
    "Optional[set[str]]": {STRING_VALUE},
    "Optional[str]": STRING_VALUE,
    "Optional[datetime]": datetime.now(),
    "Optional[bool]": True,
    "Optional[CertificateStatus]": CertificateStatus.DRAFT,
    "Optional[int]": INT_VALUE,
    "Optional[float]": FLOAT_VALUE,
    "Optional[dict[str, str]]": {STRING_VALUE: STRING_VALUE},
    "Optional[dict[str, int]]": {STRING_VALUE: INT_VALUE},
    "Optional[list[AtlasServer]]": [AtlasServer()],
    "Optional[SourceCostUnitType]": SourceCostUnitType.CREDITS,
    "Optional[list[PopularityInsights]]": [PopularityInsights()],
    "Optional[QueryUsernameStrategy]": QueryUsernameStrategy.CONNECTION_USERNAME,
    "Optional[list[GoogleLabel]]": [GoogleLabel()],
    "Optional[list[GoogleTag]]": [GoogleTag()],
    "Optional[GoogleDatastudioAssetType]": GoogleDatastudioAssetType.REPORT,
    "Optional[list[AzureTag]]": [AzureTag()],
    "Optional[list[AwsTag]]": [AwsTag()],
    "Optional[list[Catalog]]": [S3Object()],
    "Optional[list[BadgeCondition]]": [BadgeCondition()],
    "Optional[IconType]": IconType.EMOJI,
    "Optional[ADLSAccessTier]": ADLSAccessTier.HOT,
    "Optional[ADLSStorageKind]": ADLSStorageKind.STORAGE_V2,
    "Optional[ADLSPerformance]": ADLSPerformance.STANDARD,
    "Optional[ADLSProvisionState]": ADLSProvisionState.SUCCEEDED,
    "Optional[ADLSReplicationType]": ADLSReplicationType.GRS,
    "Optional[ADLSEncryptionTypes]": ADLSEncryptionTypes.MICROSOFT_STORAGE,
    "Optional[ADLSAccountStatus]": ADLSAccountStatus.AVAILABLE,
    "Optional[ADLSLeaseState]": ADLSLeaseState.LEASED,
    "Optional[ADLSLeaseStatus]": ADLSLeaseStatus.LOCKED,
    "Optional[ADLSObjectArchiveStatus]": ADLSObjectArchiveStatus.REHYDRATE_PENDING_TO_HOT,
    "Optional[ADLSObjectType]": ADLSObjectType.PAGE_BLOB,
    "Optional[PowerbiEndorsement]": PowerbiEndorsement.PROMOTED,
    "Optional[list[dict[str, str]]]": [{STRING_VALUE: STRING_VALUE}],
    "Optional[list[DbtMetricFilter]]": [DbtMetricFilter()],
    "Optional[Histogram]": Histogram(),
    "Optional[list[ColumnValueFrequencyMap]]": [ColumnValueFrequencyMap()],
    "Optional[KafkaTopicCompressionType]": KafkaTopicCompressionType.GZIP,
    "Optional[QuickSightFolderType]": QuickSightFolderType.SHARED,
    "Optional[QuickSightDatasetFieldType]": QuickSightDatasetFieldType.STRING,
    "Optional[QuickSightAnalysisStatus]": QuickSightAnalysisStatus.CREATION_FAILED,
    "Optional[QuickSightDatasetImportMode]": QuickSightDatasetImportMode.SPICE,
    "Optional[list[KafkaTopicConsumption]]": [KafkaTopicConsumption()],
    "list[AtlasGlossaryTerm]": [AtlasGlossaryTerm()],
}


def load_json(filename):
    with (DATA_DIR / filename).open() as input_file:
        return json.load(input_file)


def get_all_subclasses(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


@pytest.fixture()
def glossary_json():
    return load_json(GLOSSARY_JSON)


@pytest.fixture()
def glossary(glossary_json):
    return AtlasGlossary(**glossary_json)


@pytest.fixture()
def announcement():
    return Announcement(
        announcement_title="Important Announcement",
        announcement_message="Very important info",
        announcement_type=AnnouncementType.ISSUE,
    )


@pytest.fixture()
def table():
    return Table.create(
        name=TABLE_NAME,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    )


@pytest.fixture()
def type_def_response():
    data = {
        "enumDefs": [],
        "structDefs": [],
        "classificationDefs": [],
        "entityDefs": [],
        "relationshipDefs": [],
        "businessMetadataDefs": [
            {
                "category": "BUSINESS_METADATA",
                "guid": "733fcf3a-30f3-4ecc-8e4a-02a8bac775ea",
                "createdBy": "markpavletich",
                "updatedBy": "ernest",
                "createTime": 1649133333317,
                "updateTime": 1659328396300,
                "version": 7,
                "name": "AFq4ctARP76ctapiTbuT92",
                "description": "Data from Monte Carlo",
                "typeVersion": "1.0",
                "options": {
                    "imageId": "b053efca-c5b1-43f3-8dd3-b1e81dc47b70",
                    "logoType": "image",
                    "emoji": None,
                },
                "attributeDefs": [
                    {
                        "name": "POsWut55wIYsXZ5v4z3K98",
                        "typeName": "string",
                        "isOptional": True,
                        "cardinality": "SINGLE",
                        "valuesMinCount": 0,
                        "valuesMaxCount": 1,
                        "isUnique": False,
                        "isIndexable": True,
                        "includeInNotification": False,
                        "skipScrubbing": False,
                        "searchWeight": -1,
                        "indexType": "STRING",
                        "options": {
                            "showInOverview": "false",
                            "enumType": "",
                            "isEnum": "false",
                            "description": "https://getmontecarlo.com/catalog/",
                            "multiValueSelect": "false",
                            "customType": "url",
                            "customApplicableEntityTypes": '["Query","Folder","Collection",'
                            '"Database","Schema","View","Table","TablePartition",'
                            '"MaterialisedView","Column"]',
                            "allowSearch": "false",
                            "maxStrLength": "100000000",
                            "allowFiltering": "true",
                            "applicableEntityTypes": '["Asset"]',
                            "primitiveType": "url",
                        },
                        "displayName": "Table URL",
                        "isDefaultValueNull": False,
                        "indexTypeESConfig": {"normalizer": "atlan_normalizer"},
                        "indexTypeESFields": {
                            "text": {"analyzer": "atlan_text_analyzer", "type": "text"}
                        },
                    },
                    {
                        "name": "VdRC4dyNdTJHfFjCiNaKt9",
                        "typeName": "Data Freshness",
                        "isOptional": True,
                        "cardinality": "SINGLE",
                        "valuesMinCount": 0,
                        "valuesMaxCount": 1,
                        "isUnique": False,
                        "isIndexable": True,
                        "includeInNotification": False,
                        "skipScrubbing": False,
                        "searchWeight": -1,
                        "indexType": "STRING",
                        "options": {
                            "customApplicableEntityTypes": '["Database","Schema","View","Table","TablePartition",'
                            '"MaterialisedView","Column"]',
                            "showInOverview": "false",
                            "enumType": "Data Freshness",
                            "allowSearch": "false",
                            "maxStrLength": "100000000",
                            "isEnum": "true",
                            "allowFiltering": "true",
                            "applicableEntityTypes": '["Asset"]',
                            "multiValueSelect": "false",
                            "primitiveType": "enum",
                        },
                        "displayName": "Freshness",
                        "isDefaultValueNull": False,
                        "indexTypeESConfig": {"normalizer": "atlan_normalizer"},
                        "indexTypeESFields": {
                            "text": {"analyzer": "atlan_text_analyzer", "type": "text"}
                        },
                    },
                    {
                        "name": "loYJQi6ycokTirQTGVCHpD",
                        "typeName": "date",
                        "isOptional": True,
                        "cardinality": "SINGLE",
                        "valuesMinCount": 0,
                        "valuesMaxCount": 1,
                        "isUnique": False,
                        "isIndexable": True,
                        "includeInNotification": False,
                        "skipScrubbing": False,
                        "searchWeight": -1,
                        "options": {
                            "customApplicableEntityTypes": '["Database","Schema","View","Table","TablePartition",'
                            '"MaterialisedView","Column","Query","Folder","Collection",'
                            '"Process","ColumnProcess","BIProcess","AtlasGlossary","AtlasGlossaryTerm",'
                            '"AtlasGlossaryCategory"]',
                            "showInOverview": "false",
                            "enumType": "",
                            "allowSearch": "false",
                            "maxStrLength": "100000000",
                            "isEnum": "false",
                            "allowFiltering": "true",
                            "applicableEntityTypes": '["Asset"]',
                            "multiValueSelect": "false",
                            "primitiveType": "date",
                        },
                        "displayName": "Freshness Date",
                        "isDefaultValueNull": False,
                        "indexTypeESFields": {
                            "date": {"format": "epoch_millis", "type": "date"}
                        },
                    },
                ],
                "displayName": "Monte Carlo",
            },
            {
                "category": "BUSINESS_METADATA",
                "guid": "833fcf3a-30f3-4ecc-8e4a-02a8bac775ea",
                "createdBy": "markpavletich",
                "updatedBy": "ernest",
                "createTime": 1649133333317,
                "updateTime": 1659328396300,
                "version": 7,
                "name": "FAq4ctARP76ctapiTbuT92",
                "description": "Data from Moon",
                "typeVersion": "1.0",
                "options": {
                    "imageId": "b053efca-c5b1-43f3-8dd3-b1e81dc47b70",
                    "logoType": "image",
                    "emoji": None,
                },
                "attributeDefs": [
                    {
                        "name": "dVRC4dyNdTJHfFjCiNaKt9",
                        "typeName": "Data Freshness",
                        "isOptional": True,
                        "cardinality": "SINGLE",
                        "valuesMinCount": 0,
                        "valuesMaxCount": 1,
                        "isUnique": False,
                        "isIndexable": True,
                        "includeInNotification": False,
                        "skipScrubbing": False,
                        "searchWeight": -1,
                        "indexType": "STRING",
                        "options": {
                            "customApplicableEntityTypes": '["Database"]',
                            "showInOverview": "false",
                            "enumType": "",
                            "allowSearch": "false",
                            "maxStrLength": "100000000",
                            "isEnum": "true",
                            "allowFiltering": "true",
                            "applicableEntityTypes": '["Database"]',
                            "multiValueSelect": "false",
                            "primitiveType": "text",
                        },
                        "displayName": "Name",
                        "isDefaultValueNull": False,
                        "indexTypeESConfig": {"normalizer": "atlan_normalizer"},
                        "indexTypeESFields": {
                            "text": {"analyzer": "atlan_text_analyzer", "type": "text"}
                        },
                    }
                ],
                "displayName": "Moon",
            },
        ],
    }
    return TypeDefResponse(**data)


@pytest.fixture()
def glossary_term_json():
    return load_json(GLOSSARY_TERM_JSON)


@pytest.fixture()
def glossary_category_json():
    return load_json(GLOSSARY_CATEGORY_JSON)


def test_wrong_json(glossary_json):
    with pytest.raises(ValidationError):
        AtlasGlossaryTerm(**glossary_json)


def test_asset_response(glossary_category_json):
    asset_response_json = {"referredEntities": {}, "entity": glossary_category_json}
    glossary_category = AssetResponse[AtlasGlossaryCategory](
        **asset_response_json
    ).entity
    assert glossary_category == AtlasGlossaryCategory(**glossary_category_json)


@pytest.fixture(scope="function")
def the_json(request):
    return load_json(request.param)


@pytest.mark.parametrize(
    "the_json, a_type",
    [
        ("glossary.json", AtlasGlossary),
        ("glossary_category.json", AtlasGlossaryCategory),
        ("glossary_term.json", AtlasGlossaryTerm),
        ("glossary_term2.json", AtlasGlossaryTerm),
        ("asset_mutated_response_empty.json", AssetMutationResponse),
        ("asset_mutated_response_update.json", AssetMutationResponse),
    ],
    indirect=["the_json"],
)
def test_constructor(the_json, a_type, monkeypatch):
    def get_name_for_id(value):
        return "PII"

    def get_id_for_name(value):
        return "WQ6XGXwq9o7UnZlkWyKhQN"

    monkeypatch.setattr(
        pyatlan.cache.classification_cache.ClassificationCache,
        "get_id_for_name",
        get_id_for_name,
    )

    monkeypatch.setattr(
        pyatlan.cache.classification_cache.ClassificationCache,
        "get_name_for_id",
        get_name_for_id,
    )

    asset = a_type(**the_json)
    assert not DeepDiff(
        the_json,
        json.loads(asset.json(by_alias=True, exclude_unset=True)),
        ignore_order=True,
    )


def test_has_announcement(glossary):
    assert glossary.has_announcement() == (
        bool(glossary.attributes.announcement_type)
        or bool(glossary.attributes.announcement_title)
    )


def test_set_announcement(glossary, announcement):
    glossary.set_announcement(announcement)
    assert glossary.has_announcement() is True
    assert announcement == glossary.get_announcment()


def test_create_glossary():
    glossary = AtlasGlossary(
        attributes=AtlasGlossary.Attributes(
            name="Integration Test Glossary", user_description="This a test glossary"
        )
    )
    assert "AtlasGlossary" == glossary.type_name


def test_clear_announcement(glossary, announcement):
    glossary.set_announcement(announcement)
    glossary.remove_announcement()
    assert not glossary.has_announcement()
    assert glossary.attributes.announcement_title is None
    assert glossary.attributes.announcement_type is None
    assert glossary.attributes.announcement_message is None


@pytest.mark.parametrize(
    "name, connector_type, admin_users, admin_groups, admin_roles, error",
    [
        (None, AtlanConnectorType.BIGQUERY, None, None, ["123"], ValueError),
        ("", AtlanConnectorType.BIGQUERY, None, None, ["123"], ValueError),
        ("query", None, None, None, ["123"], ValueError),
        ("query", AtlanConnectorType.BIGQUERY, None, None, None, ValueError),
        ("query", AtlanConnectorType.BIGQUERY, [], [], [], ValueError),
    ],
)
def test_connection_attributes_create_without_required_parameters_raises_validation_error(
    name, connector_type, admin_users, admin_groups, admin_roles, error
):
    with pytest.raises(error):
        Connection.Attributes.create(
            name=name,
            connector_type=connector_type,
            admin_users=admin_users,
            admin_groups=admin_groups,
            admin_roles=admin_roles,
        )


@pytest.mark.parametrize(
    "name, connector_type, admin_users, admin_groups, admin_roles",
    [
        ("query", AtlanConnectorType.BIGQUERY, {"bob"}, None, None),
        ("query", AtlanConnectorType.BIGQUERY, None, {"bob"}, None),
        ("query", AtlanConnectorType.BIGQUERY, None, None, {"bob"}),
        ("query", AtlanConnectorType.BIGQUERY, {"bob"}, {"ted"}, {"alice"}),
    ],
)
def test_connection_attributes_create_with_required_parameters(
    name, connector_type, admin_users, admin_groups, admin_roles
):
    c = Connection.Attributes.create(
        name=name,
        connector_type=connector_type,
        admin_users=admin_users,
        admin_groups=admin_groups,
        admin_roles=admin_roles,
    )
    assert c.qualified_name
    assert c.qualified_name <= connector_type.to_qualified_name()
    assert c.connector_name == connector_type.value
    assert c.category == connector_type.category.value
    assert c.admin_roles == admin_roles
    assert c.admin_users == admin_users
    assert c.admin_groups == admin_groups


@pytest.mark.parametrize(
    "name, connector_type, admin_users, admin_groups, admin_roles",
    [("somequery", AtlanConnectorType.BIGQUERY, {"bob"}, {"ted"}, {"alice"})],
)
def test_connection_create_with_required_parameters(
    name, connector_type, admin_users, admin_groups, admin_roles
):
    c = Connection.create(
        name=name,
        connector_type=connector_type,
        admin_users=admin_users,
        admin_groups=admin_groups,
        admin_roles=admin_roles,
    )
    assert c.attributes.qualified_name
    assert c.attributes.qualified_name <= connector_type.to_qualified_name()
    assert c.attributes.connector_name == connector_type.value
    assert c.attributes.category == connector_type.category.value
    assert c.attributes.admin_roles == admin_roles
    assert c.attributes.admin_users == admin_users
    assert c.attributes.admin_groups == admin_groups


@pytest.mark.parametrize(
    "name, connector_type, admin_users, admin_groups, admin_roles, error",
    [
        (None, AtlanConnectorType.BIGQUERY, None, None, ["123"], ValueError),
        ("", AtlanConnectorType.BIGQUERY, None, None, ["123"], ValueError),
        ("SomeQuery", None, None, None, ["123"], ValueError),
        ("SomeQuery", AtlanConnectorType.BIGQUERY, None, None, None, ValueError),
        ("SomeQuery", AtlanConnectorType.BIGQUERY, [], [], [], ValueError),
    ],
)
def test_connection_create_without_required_parameters_raises_validation_error(
    name, connector_type, admin_users, admin_groups, admin_roles, error
):
    with pytest.raises(error):
        Connection.create(
            name=name,
            connector_type=connector_type,
            admin_users=admin_users,
            admin_groups=admin_groups,
            admin_roles=admin_roles,
        )


@pytest.mark.parametrize(
    "name, qualified_name, connector_name, category, admin_users, admin_groups, admin_roles, msg",
    [
        (
            "Bob",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            AtlanConnectorType.BIGQUERY.value,
            AtlanConnectorType.BIGQUERY.category.value,
            None,
            None,
            None,
            "One of admin_user, admin_groups or admin_roles is required",
        ),
        (
            "Bob",
            "",
            AtlanConnectorType.BIGQUERY.value,
            AtlanConnectorType.BIGQUERY.category.value,
            ["Bob"],
            None,
            None,
            "qualified_name is required",
        ),
        (
            "Bob",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            AtlanConnectorType.BIGQUERY.value,
            "",
            ["Bob"],
            None,
            None,
            "category is required",
        ),
        (
            "Bob",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            "",
            AtlanConnectorType.BIGQUERY.category.value,
            ["Bob"],
            None,
            None,
            "connector_name is required",
        ),
        (
            "",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            AtlanConnectorType.BIGQUERY.value,
            AtlanConnectorType.BIGQUERY.category.value,
            ["Bob"],
            None,
            None,
            "name is required",
        ),
    ],
)
def test_connection_validate_required_when_fields_missing_raises_value_error(
    name,
    qualified_name,
    connector_name,
    category,
    admin_users,
    admin_groups,
    admin_roles,
    msg,
):
    a = Connection.Attributes(
        name=name,
        qualified_name=qualified_name,
        connector_name=connector_name,
        category=category,
        admin_users=admin_users,
        admin_groups=admin_groups,
        admin_roles=admin_roles,
    )
    with pytest.raises(ValueError) as ve:
        a.validate_required()
    assert str(ve.value) == msg


@pytest.mark.parametrize(
    "name, qualified_name, connector_name, category, admin_users, admin_groups, admin_roles",
    [
        (
            "Bob",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            AtlanConnectorType.BIGQUERY.value,
            AtlanConnectorType.BIGQUERY.category.value,
            ["Bob"],
            None,
            None,
        ),
        (
            "Bob",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            AtlanConnectorType.BIGQUERY.value,
            AtlanConnectorType.BIGQUERY.category.value,
            None,
            ["Bob"],
            None,
        ),
        (
            "Bob",
            AtlanConnectorType.BIGQUERY.to_qualified_name(),
            AtlanConnectorType.BIGQUERY.value,
            AtlanConnectorType.BIGQUERY.category.value,
            None,
            None,
            ["Bob"],
        ),
    ],
)
def test_connection_validate_required_when_fields_are_present(
    name,
    qualified_name,
    connector_name,
    category,
    admin_users,
    admin_groups,
    admin_roles,
):
    a = Connection.Attributes(
        name=name,
        qualified_name=qualified_name,
        connector_name=connector_name,
        category=category,
        admin_users=admin_users,
        admin_groups=admin_groups,
        admin_roles=admin_roles,
    )
    a.validate_required()


@pytest.mark.parametrize(
    "name, connection_qualified_name, error",
    [
        (None, "default/snowflake/1673868111909", ValueError),
        ("DB", None, ValueError),
        ("", "default/snowflake/1673868111909", ValueError),
        ("DB", "", ValueError),
        ("DB", "default/snwflake/1673868111909", ValueError),
        ("DB", "snowflake/1673868111909", ValueError),
        ("DB", "default/snwflake", ValueError),
    ],
)
def test_database_attributes_create_without_required_parameters_raises_validation_error(
    name, connection_qualified_name, error
):
    with pytest.raises(error):
        Database.Attributes.create(
            name=name, connection_qualified_name=connection_qualified_name
        )


@pytest.mark.parametrize(
    "name, connection_qualified_name",
    [
        ("TestDB", "default/snowflake/1673868111909"),
    ],
)
def test_database_attributes_create_with_required_parameters(
    name, connection_qualified_name
):

    attributes = Database.Attributes.create(
        name=name, connection_qualified_name=connection_qualified_name
    )
    assert attributes.name == name
    assert attributes.connection_qualified_name == connection_qualified_name
    assert attributes.qualified_name == f"{connection_qualified_name}/{name}"
    assert attributes.connector_name == connection_qualified_name.split("/")[1]


@pytest.mark.parametrize(
    "name, connection_qualified_name, error",
    [
        (None, "default/snowflake/1673868111909", ValueError),
        ("DB", None, ValueError),
        ("", "default/snowflake/1673868111909", ValueError),
        ("DB", "", ValueError),
        ("DB", "default/snwflake/1673868111909", ValueError),
        ("DB", "snowflake/1673868111909", ValueError),
        ("DB", "default/snwflake", ValueError),
    ],
)
def test_database_create_without_required_parameters_raises_validation_error(
    name, connection_qualified_name, error
):
    with pytest.raises(error):
        Database.create(name=name, connection_qualified_name=connection_qualified_name)


@pytest.mark.parametrize(
    "name, connection_qualified_name",
    [
        ("TestDB", "default/snowflake/1673868111909"),
    ],
)
def test_database_create_with_required_parameters(name, connection_qualified_name):

    database = Database.create(
        name=name, connection_qualified_name=connection_qualified_name
    )
    attributes = database.attributes
    assert attributes.name == name
    assert attributes.connection_qualified_name == connection_qualified_name
    assert attributes.qualified_name == f"{connection_qualified_name}/{name}"
    assert attributes.connector_name == connection_qualified_name.split("/")[1]


@pytest.mark.parametrize(
    "name, database_qualified_name, error",
    [
        (None, "default/snowflake/1673868111909/TestDb", ValueError),
        ("Schema1", None, ValueError),
        ("", "default/snowflake/1673868111909/TestDb", ValueError),
        ("Schema1", "", ValueError),
        ("Schema1", "default/snwflake/1673868111909/TestDb", ValueError),
        ("Schema1", "snowflake/1673868111909", ValueError),
        ("Schema1", "default/snwflake", ValueError),
    ],
)
def test_schema_attributes_create_without_required_parameters_raises_validation_error(
    name, database_qualified_name, error
):
    with pytest.raises(error):
        Schema.Attributes.create(
            name=name, database_qualified_name=database_qualified_name
        )


@pytest.mark.parametrize(
    "name, database_qualified_name",
    [
        ("Schema1", "default/snowflake/1673868111909/TestDb"),
    ],
)
def test_schema_attributes_create_with_required_parameters(
    name, database_qualified_name
):
    attributes = Schema.Attributes.create(
        name=name, database_qualified_name=database_qualified_name
    )
    assert isinstance(attributes, Schema.Attributes)
    assert attributes.name == name
    assert attributes.database_qualified_name == database_qualified_name
    assert (
        attributes.connection_qualified_name
        == database_qualified_name[: database_qualified_name.rindex("/")]
    )
    assert attributes.qualified_name == f"{database_qualified_name}/{name}"
    assert attributes.connector_name == database_qualified_name.split("/")[1]
    assert attributes.database_name == database_qualified_name.split(("/"))[3]


@pytest.mark.parametrize(
    "name, database_qualified_name, error",
    [
        (None, "default/snowflake/1673868111909/TestDb", ValueError),
        ("Schema1", None, ValueError),
        ("", "default/snowflake/1673868111909/TestDb", ValueError),
        ("Schema1", "", ValueError),
        ("Schema1", "default/snwflake/1673868111909/TestDb", ValueError),
        ("Schema1", "snowflake/1673868111909", ValueError),
        ("Schema1", "default/snwflake", ValueError),
    ],
)
def test_schema__create_without_required_parameters_raises_validation_error(
    name, database_qualified_name, error
):
    with pytest.raises(error):
        Schema.create(name=name, database_qualified_name=database_qualified_name)


@pytest.mark.parametrize(
    "cls, name, schema_qualified_name, error",
    [
        (cls, values[0], values[1], values[2])
        for values in [
            (None, "default/snowflake/1673868111909/TestDb/Schema1", ValueError),
            ("Table_1", None, ValueError),
            ("", "default/snowflake/1673868111909/TestDb/Schema1", ValueError),
            ("Table_1", "", ValueError),
            ("Table_1", "default/snwflake/1673868111909/TestDb/Schema1", ValueError),
            ("Table_1", "default/snowflake/1673868111909/TestDb", ValueError),
            ("Table_1", "snowflake/1673868111909", ValueError),
            ("Table_1", "default/snwflake", ValueError),
        ]
        for cls in [Table.Attributes, View.Attributes]
    ],
)
def test_table_attributes_create_without_required_parameters_raises_validation_error(
    cls, name, schema_qualified_name, error
):
    with pytest.raises(error):
        cls.create(name=name, schema_qualified_name=schema_qualified_name)


@pytest.mark.parametrize(
    "cls, name, schema_qualified_name",
    [
        (cls, "Table_1", "default/snowflake/1673868111909/TestDb/Schema1")
        for cls in [Table.Attributes, View.Attributes]
    ],
)
def test_table_attributes_create_with_required_parameters(
    cls, name, schema_qualified_name
):
    attributes = cls.create(name=name, schema_qualified_name=schema_qualified_name)
    assert isinstance(attributes, cls)
    assert attributes.name == name
    assert attributes.schema_qualified_name == schema_qualified_name
    assert attributes.qualified_name == f"{schema_qualified_name}/{name}"
    assert attributes.connector_name == schema_qualified_name.split("/")[1]
    assert attributes.database_name == schema_qualified_name.split(("/"))[3]
    assert attributes.schema_name == schema_qualified_name.split(("/"))[4]
    fields = schema_qualified_name.split("/")
    assert attributes.connection_qualified_name == "/".join(fields[:3])
    assert attributes.database_qualified_name == "/".join(fields[:4])


@pytest.mark.parametrize(
    "cls, name, schema_qualified_name, error",
    [
        (cls, values[0], values[1], values[2])
        for values in [
            (None, "default/snowflake/1673868111909/TestDb/Schema1", ValueError),
            ("Table_1", None, ValueError),
            ("", "default/snowflake/1673868111909/TestDb/Schema1", ValueError),
            ("Table_1", "", ValueError),
            ("Table_1", "default/snwflake/1673868111909/TestDb/Schema1", ValueError),
            ("Table_1", "default/snowflake/1673868111909/TestDb", ValueError),
            ("Table_1", "snowflake/1673868111909", ValueError),
            ("Table_1", "default/snwflake", ValueError),
        ]
        for cls in [Table.Attributes, View.Attributes]
    ],
)
def test_table_create_without_required_parameters_raises_validation_error(
    cls, name, schema_qualified_name, error
):
    with pytest.raises(error):
        cls.create(name=name, schema_qualified_name=schema_qualified_name)


@pytest.mark.parametrize(
    "cls, name, schema_qualified_name",
    [
        (cls, "Table_1", "default/snowflake/1673868111909/TestDb/Schema1")
        for cls in [Table, View]
    ],
)
def test_table_create_with_required_parameters(cls, name, schema_qualified_name):
    attributes = cls.create(
        name=name, schema_qualified_name=schema_qualified_name
    ).attributes
    assert isinstance(attributes, cls.Attributes)
    assert attributes.name == name
    assert attributes.schema_qualified_name == schema_qualified_name
    assert attributes.qualified_name == f"{schema_qualified_name}/{name}"
    assert attributes.connector_name == schema_qualified_name.split("/")[1]
    assert attributes.database_name == schema_qualified_name.split(("/"))[3]
    assert attributes.schema_name == schema_qualified_name.split(("/"))[4]
    fields = schema_qualified_name.split("/")
    assert attributes.connection_qualified_name == "/".join(fields[:3])
    assert attributes.database_qualified_name == "/".join(fields[:4])


@pytest.mark.parametrize(
    "clazz, method_name, property_names, values",
    [
        (clazz, attribute_info[1], attribute_info[2:], attribute_info[0])
        for clazz in get_all_subclasses(Asset.Attributes)
        for attribute_info in [
            (["abc"], "remove_description", "description"),
            (["abc"], "remove_user_description", "user_description"),
            ([["bob"], ["dave"]], "remove_owners", "owner_groups", "owner_users"),
            (
                [CertificateStatus.DRAFT, "some message"],
                "remove_certificate",
                "certificate_status",
                "certificate_status_message",
            ),
            (
                ["a message", "a title", "issue"],
                "remove_announcement",
                "announcement_message",
                "announcement_title",
                "announcement_type",
            ),
        ]
    ],
)
def test_remove_desscription(clazz, method_name, property_names, values):
    attributes = clazz()
    for property, value in zip(property_names, values):
        setattr(attributes, property, value)
    getattr(attributes, method_name)()
    for property in property_names:
        assert getattr(attributes, property) is None


@pytest.mark.parametrize(
    "clazz, method_name",
    [
        (clazz, method_name)
        for clazz in get_all_subclasses(Asset)
        for method_name in [
            "remove_description",
            "remove_user_description",
            "remove_owners",
            "remove_certificate",
            "remove_owners",
            "remove_announcement",
        ]
    ],
)
def test_class_remove_methods(clazz, method_name):
    mock_attributes = create_autospec(clazz.Attributes)
    sut = clazz(attributes=mock_attributes)
    sut.remove_owners()
    sut.attributes.remove_owners.assert_called_once()


def test_glossary_attributes_create_when_missing_name_raises_validation_error():
    with pytest.raises(ValueError):
        AtlasGlossary.Attributes.create(name=None)


def test_glossary_attributes_create_sets_name():
    sut = AtlasGlossary.Attributes.create(name="Bob")
    assert sut.name == "Bob"


@pytest.mark.parametrize(
    "name, anchor",
    [("A Category", None), (None, AtlasGlossary.create(name="glossary"))],
)
def test_glossary_category_attributes_create_when_missing_name_raises_validation_error(
    name, anchor
):
    with pytest.raises(ValueError):
        AtlasGlossaryCategory.Attributes.create(name=name, anchor=anchor)


def test_glossary_category_attributes_create_sets_name_anchor():
    glossary = AtlasGlossary.create(name="Glossary")
    sut = AtlasGlossaryCategory.Attributes.create(name="Bob", anchor=glossary)
    assert sut.name == "Bob"
    assert sut.anchor == glossary


@pytest.mark.parametrize(
    "name, anchor",
    [("A Category", None), (None, AtlasGlossary.create(name="glossary"))],
)
def test_glossary_term_attributes_create_when_missing_name_raises_validation_error(
    name, anchor
):
    with pytest.raises(ValueError):
        a = AtlasGlossaryTerm.Attributes.create(name=name, anchor=anchor)
        a.validate_required()


def test_glossary_term_attributes_create_sets_name_anchor():
    glossary = AtlasGlossary.create(name="Glossary")
    sut = AtlasGlossaryTerm.Attributes.create(name="Bob", anchor=glossary)
    assert sut.name == "Bob"
    assert sut.anchor == glossary


@patch("pyatlan.cache.custom_metadata_cache.AtlanClient")
def test_get_business_attributes_when_name_not_valid_raises_value_error(
    mock_client, table, type_def_response
):
    mock_client.return_value.get_typedefs.return_value = type_def_response
    with pytest.raises(
        ValueError, match="No custom metadata with the name: Zoro exist"
    ):
        table.get_custom_metadata("Zoro")


@patch("pyatlan.cache.custom_metadata_cache.AtlanClient")
def test_get_business_attributes_when_name_not_appropriate_for_asset_raises_value_error(
    mock_client, table, type_def_response
):
    mock_client.get_default_client.return_value = mock_client
    mock_client.get_typedefs.return_value = type_def_response
    with pytest.raises(
        ValueError, match="Custom metadata attributes Moon are not applicable to Table"
    ):
        table.get_custom_metadata("Moon")


@patch("pyatlan.cache.custom_metadata_cache.AtlanClient")
def test_get_business_attributes_with_valid_name_returns_empty_attribute_when_table_does_not_have_attribute(
    mock_client, table, type_def_response
):
    mock_client.return_value.get_typedefs.return_value = type_def_response

    monte_carlo = table.get_custom_metadata("Monte Carlo")

    assert monte_carlo is not None
    assert monte_carlo.freshness is None
    assert monte_carlo.freshness_date is None
    assert monte_carlo.table_url is None


@patch("pyatlan.cache.custom_metadata_cache.AtlanClient")
def test_get_business_attributes_with_valid_name_returns_attribute_when_table_has_attribute(
    mock_client, table, type_def_response
):
    mock_client.return_value.get_typedefs.return_value = type_def_response
    table.business_attributes = {
        MONTE_CARLO: {
            FRESHNESS: "pass",
            TABLE_URL: "https://getmontecarlo.com/catalog/",
        }
    }

    monte_carlo = table.get_custom_metadata("Monte Carlo")

    assert monte_carlo is not None
    assert monte_carlo.freshness == "pass"
    assert monte_carlo.table_url == "https://getmontecarlo.com/catalog/"


def test_set_busines_attributes_with_non_business_attributes_object_raises_value_error(
    table,
):
    with pytest.raises(
        ValueError,
        match="business_attributes must be an instance of CustomMetadata",
    ):
        table.set_custom_metadata({})


def test_set_business_attributes_with_non_appropriate_meta_data_type_name_raises_value_error(
    table,
):

    with pytest.raises(
        ValueError,
        match="business_attributes must be an instance of CustomMetadata",
    ):
        table.set_custom_metadata({})


@patch("pyatlan.cache.custom_metadata_cache.AtlanClient")
def test_assigning_to_invalid_business_attribute_raises_attribute_error(
    mock_client, table, type_def_response
):
    mock_client.return_value.get_typedefs.return_value = type_def_response
    table.business_attributes = {
        MONTE_CARLO: {
            FRESHNESS: "pass",
            TABLE_URL: "https://getmontecarlo.com/catalog/",
        }
    }
    business_attributes = table.get_custom_metadata("Monte Carlo")
    with pytest.raises(AttributeError, match="Attribute bogus does not exist"):
        business_attributes.bogus = "123"


@patch("pyatlan.cache.custom_metadata_cache.AtlanClient")
def test_set_business_attributes_with_business_attribute_not_appropriate_to_asset_raises_value_error(
    mock_client, table, type_def_response
):
    mock_client.return_value.get_typedefs.return_value = type_def_response

    moon = CustomMetadataCache.get_type_for_id(MOON)()

    with pytest.raises(
        ValueError,
        match="Business attributes Moon are not applicable to Table",
    ):
        table.set_custom_metadata(moon)


@patch("pyatlan.cache.custom_metadata_cache.AtlanClient")
def test_set_business_attributes_with_appropriate_business_attribute_updates_dictionary(
    mock_client, table, type_def_response
):
    mock_client.return_value.get_typedefs.return_value = type_def_response

    table.business_attributes = {
        MONTE_CARLO: {
            FRESHNESS: "pass",
            TABLE_URL: "https://getmontecarlo.com/catalog/",
        }
    }
    monte_carlo = table.get_custom_metadata("Monte Carlo")

    monte_carlo.freshness = "fail"
    monte_carlo.table_url = "http://anywhere.com"
    table.set_custom_metadata(monte_carlo)

    monte_carlo_dict = table.business_attributes[MONTE_CARLO]
    assert monte_carlo_dict[FRESHNESS] == monte_carlo.freshness
    assert monte_carlo_dict[TABLE_URL] == monte_carlo.table_url


@pytest.mark.parametrize(
    "cls, name, connection_qualified_name, aws_arn, msg",
    [
        (cls, values[0], values[1], values[2], values[3])
        for values in [
            (None, "default/s3/production", "abc", "name is required"),
            ("my-bucket", None, "abc", "connection_qualified_name is required"),
            ("", "default/s3/production", "abc", "name cannot be blank"),
            ("my-bucket", "", "abc", "connection_qualified_name cannot be blank"),
            ("my-bucket", "default/s3/", "abc", "Invalid connection_qualified_name"),
            ("my-bucket", "/s3/", "abc", "Invalid connection_qualified_name"),
            (
                "my-bucket",
                "default/s3/production/TestDb",
                "abc",
                "Invalid connection_qualified_name",
            ),
            ("my-bucket", "s3/production", "abc", "Invalid connection_qualified_name"),
            (
                "my-bucket",
                "default/s33/production",
                "abc",
                "Invalid connection_qualified_name",
            ),
            ("my-bucket", "default/s3", None, "aws_arn is required"),
            ("my-bucket", "default/s3", "", "aws_arn cannot be blank"),
        ]
        for cls in [S3Bucket.Attributes, S3Bucket, S3Object.Attributes, S3Object]
    ],
)
def test_s3bucket_attributes_create_without_required_parameters_raises_validation_error(
    cls, name, connection_qualified_name, aws_arn, msg
):
    with pytest.raises(ValueError) as exc_info:
        cls.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
            aws_arn=aws_arn,
        )
    assert exc_info.value.args[0] == msg


@pytest.mark.parametrize(
    "name, connection_qualified_name, aws_arn",
    [("my-bucket", "default/s3/production", "my-arn")],
)
def test_s3bucket_attributes_create_with_required_parameters(
    name, connection_qualified_name, aws_arn
):
    attributes = S3Bucket.Attributes.create(
        name=name, connection_qualified_name=connection_qualified_name, aws_arn=aws_arn
    )
    assert attributes.name == name
    assert attributes.connection_qualified_name == connection_qualified_name
    assert attributes.qualified_name == f"{connection_qualified_name}/{aws_arn}"
    assert attributes.connector_name == connection_qualified_name.split("/")[1]


@pytest.mark.parametrize(
    "name, connection_qualified_name, aws_arn",
    [
        ("my-bucket", "default/s3/production", "my-arn"),
    ],
)
def test_s3bucket_create_with_required_parameters(
    name, connection_qualified_name, aws_arn
):
    attributes = S3Bucket.create(
        name=name, connection_qualified_name=connection_qualified_name, aws_arn=aws_arn
    ).attributes
    assert attributes.name == name
    assert attributes.connection_qualified_name == connection_qualified_name
    assert attributes.qualified_name == f"{connection_qualified_name}/{aws_arn}"
    assert attributes.connector_name == connection_qualified_name.split("/")[1]


@pytest.mark.parametrize(
    "name, connection_qualified_name, aws_arn, , s3_bucket_qualified_name",
    [
        ("my-bucket", "default/s3/production", "my-arn", None),
        (
            "my-bucket",
            "default/s3/production",
            "my-arn",
            "default/s3/production/bucket_123",
        ),
    ],
)
def test_s3object_create_with_required_parameters(
    name, connection_qualified_name, aws_arn, s3_bucket_qualified_name
):
    attributes = S3Object.create(
        name=name,
        connection_qualified_name=connection_qualified_name,
        aws_arn=aws_arn,
        s3_bucket_qualified_name=s3_bucket_qualified_name,
    ).attributes
    assert attributes.name == name
    assert attributes.connection_qualified_name == connection_qualified_name
    assert attributes.qualified_name == f"{connection_qualified_name}/{aws_arn}"
    assert attributes.connector_name == connection_qualified_name.split("/")[1]
    assert attributes.s3_bucket_qualified_name == s3_bucket_qualified_name


@pytest.mark.parametrize(
    "name, connection_qualified_name, aws_arn, s3_bucket_qualified_name",
    [
        ("my-bucket", "default/s3/production", "my-arn", None),
        (
            "my-bucket",
            "default/s3/production",
            "my-arn",
            "default/s3/production/bucket_123",
        ),
    ],
)
def test_s3object_attributes_create_with_required_parameters(
    name, connection_qualified_name, aws_arn, s3_bucket_qualified_name
):
    attributes = S3Object.Attributes.create(
        name=name,
        connection_qualified_name=connection_qualified_name,
        aws_arn=aws_arn,
        s3_bucket_qualified_name=s3_bucket_qualified_name,
    )
    assert attributes.name == name
    assert attributes.connection_qualified_name == connection_qualified_name
    assert attributes.qualified_name == f"{connection_qualified_name}/{aws_arn}"
    assert attributes.connector_name == connection_qualified_name.split("/")[1]
    assert attributes.s3_bucket_qualified_name == s3_bucket_qualified_name


@pytest.fixture()
def attribute_value(request):
    sig = signature(getattr(request.param[0], request.param[1]).fget)
    return ATTRIBUTE_VALUES_BY_TYPE[sig.return_annotation]


@pytest.mark.parametrize(
    "clazz, property_name, attribute_value",
    [
        (asset_type, property_name, (asset_type, property_name))
        for asset_type in get_all_subclasses(Asset)
        for property_name in [
            p for p in dir(asset_type) if isinstance(getattr(asset_type, p), property)
        ]
    ],
    indirect=["attribute_value"],
)
def test_attributes(clazz, property_name, attribute_value):
    local_ns = {}
    sut = clazz(attributes=clazz.Attributes())
    exec(f"sut.{property_name} = attribute_value")
    exec(
        f"ret_value = sut.{property_name}",
        {"sut": sut, "property_name": property_name},
        local_ns,
    )
    assert attribute_value == local_ns["ret_value"]
    exec(
        f"ret_value = sut.attributes.{property_name if property_name != 'terms' else 'meanings'}",
        {"sut": sut, "property_name": property_name},
        local_ns,
    )
    assert attribute_value == local_ns["ret_value"]


@pytest.mark.parametrize(
    "names, values, message",
    [
        (
            ("one", "two"),
            (None, None),
            "One of the following parameters are required: one, two",
        ),
        (
            ("one", "two"),
            (1, 2),
            "Only one of the following parameters are allowed: one, two",
        ),
        (
            ("one", "two", "three"),
            (1, None, 3),
            "Only one of the following parameters are allowed: one, three",
        ),
    ],
)
def test_validate_single_required_field_with_bad_values_raises_value_error(
    names, values, message
):
    with pytest.raises(ValueError, match=message):
        validate_single_required_field(names, values)


def test_validate_single_required_field_with_only_one_field_does_not_raise_value_error():
    validate_single_required_field(["One", "Two", "Three"], [None, None, 3])


@pytest.mark.parametrize(
    "asset, content, asset_name, error, message",
    [
        (None, "stuff", None, ValueError, "asset is required"),
        (table, None, None, ValueError, "content is required"),
        (
            Table(),
            "stuff",
            None,
            AttributeError,
            "'NoneType' object has no attribute 'name'",
        ),
        (
            Table(attributes=Table.Attributes()),
            "stuff",
            None,
            ValueError,
            "asset_name is required when name is not available from asset",
        ),
    ],
)
def test_create_readme_attributes_without_required_parameters_raises_exception(
    asset, content, asset_name, error, message
):

    with pytest.raises(error, match=message):
        Readme.Attributes.create(asset=asset, content=content, asset_name=asset_name)


@pytest.mark.parametrize(
    "asset, content, asset_name, error, message",
    [
        (None, "stuff", None, ValueError, "asset is required"),
        (
            Table.create(
                name=TABLE_NAME,
                schema_qualified_name=SCHEMA_QUALIFIED_NAME,
            ),
            None,
            None,
            ValueError,
            "content is required",
        ),
        (
            Table(),
            "stuff",
            None,
            AttributeError,
            "'NoneType' object has no attribute 'name'",
        ),
        (
            Table(attributes=Table.Attributes()),
            "stuff",
            None,
            ValueError,
            "asset_name is required when name is not available from asset",
        ),
    ],
)
def test_create_readme_without_required_parameters_raises_exception(
    asset, content, asset_name, error, message
):

    with pytest.raises(error, match=message):
        Readme.create(asset=asset, content=content, asset_name=asset_name)


@pytest.mark.parametrize(
    "asset, content, asset_name, expected_name",
    [
        (
            Table.create(
                name=TABLE_NAME,
                schema_qualified_name=SCHEMA_QUALIFIED_NAME,
            ),
            "<h1>stuff</h1>",
            None,
            TABLE_NAME,
        ),
        (
            Table(attributes=Table.Attributes()),
            "<h1>stuff</h1>",
            TABLE_NAME,
            TABLE_NAME,
        ),
    ],
)
def test_create_readme(asset, content, asset_name, expected_name):
    readme = Readme.create(asset=asset, content=content, asset_name=asset_name)
    assert readme.qualified_name == f"{asset.guid}/readme"
    assert readme.name == f"{expected_name} Readme"
    assert readme.attributes.asset == asset
    assert readme.description == content
