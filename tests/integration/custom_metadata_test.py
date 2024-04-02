# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import json
import time
from typing import Generator, List, Optional, Tuple

import pytest

from pyatlan.cache.custom_metadata_cache import CustomMetadataCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    Asset,
    AtlasGlossary,
    AtlasGlossaryTerm,
    Badge,
    Connection,
)
from pyatlan.model.custom_metadata import CustomMetadataDict
from pyatlan.model.enums import (
    AtlanCustomAttributePrimitiveType,
    AtlanIcon,
    AtlanTagColor,
    AtlanTypeCategory,
    BadgeComparisonOperator,
    BadgeConditionColor,
    EntityStatus,
)
from pyatlan.model.fields.atlan_fields import CustomMetadataField
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch
from pyatlan.model.group import AtlanGroup, CreateGroupResponse
from pyatlan.model.structs import BadgeCondition
from pyatlan.model.typedef import AttributeDef, CustomMetadataDef, EnumDef
from tests.integration.admin_test import create_group, delete_group
from tests.integration.client import TestId, delete_asset
from tests.integration.glossary_test import create_glossary, create_term

MODULE_NAME = TestId.make_unique("CM")

FIXED_USER = "ernest"
GROUP_NAME1 = f"{MODULE_NAME}1"
GROUP_NAME2 = f"{MODULE_NAME}2"

CM_RACI = f"{MODULE_NAME}_RACI"
CM_ATTR_RACI_RESPONSIBLE = "Responsible"
CM_ATTR_RACI_ACCOUNTABLE = "Accountable"
CM_ATTR_RACI_CONSULTED = "Consulted"
CM_ATTR_RACI_INFORMED = "Informed"
CM_ATTR_RACI_EXTRA = "Extra"


CM_IPR = f"{MODULE_NAME}_IPR"
CM_ATTR_IPR_LICENSE = "License"
CM_ATTR_IPR_VERSION = "Version"
CM_ATTR_IPR_MANDATORY = "Mandatory"
CM_ATTR_IPR_DATE = "Date"
CM_ATTR_IPR_URL = "URL"


CM_QUALITY = f"{MODULE_NAME}_DQ"
CM_ATTR_QUALITY_COUNT = "Count"
CM_ATTR_QUALITY_SQL = "SQL"
CM_ATTR_QUALITY_TYPE = "Type"

DQ_ENUM = f"{MODULE_NAME}_DataQualityType"
DQ_TYPE_LIST = [
    "Accuracy",
    "Completeness",
    "Consistency",
    "Timeliness",
    "Validity",
    "Uniqueness",
]
DQ_TYPE_EXTRA_LIST = ["Unknown", "Others"]

_removal_epoch: Optional[int]


def create_custom_metadata(
    client: AtlanClient,
    name: str,
    attribute_defs: List[AttributeDef],
    locked: bool,
    logo: Optional[str] = None,
    icon: Optional[AtlanIcon] = None,
    color: Optional[AtlanTagColor] = None,
) -> CustomMetadataDef:
    cm_def = CustomMetadataDef.create(display_name=name)
    cm_def.attribute_defs = attribute_defs
    if icon and color:
        cm_def.options = CustomMetadataDef.Options.with_logo_from_icon(
            icon, color, locked
        )
    elif logo and logo.startswith("http"):
        cm_def.options = CustomMetadataDef.Options.with_logo_from_url(logo, locked)
    elif logo:
        cm_def.options = CustomMetadataDef.Options.with_logo_as_emoji(logo, locked)
    else:
        raise ValueError(
            "Invalid configuration for the visual to use for the custom metadata."
        )
    r = client.typedef.create(cm_def)
    return r.custom_metadata_defs[0]


def create_enum(client: AtlanClient, name: str, values: List[str]) -> EnumDef:
    enum_def = EnumDef.create(name=name, values=values)
    r = client.typedef.create(enum_def)
    return r.enum_defs[0]


def update_enum(
    client: AtlanClient, name: str, values: List[str], replace_existing: bool = False
) -> EnumDef:
    enum_def = EnumDef.update(
        name=name, values=values, replace_existing=replace_existing
    )
    r = client.typedef.update(enum_def)
    return r.enum_defs[0]


@pytest.fixture(scope="module")
def limit_attribute_applicability_kwargs(
    glossary: AtlasGlossary, connection: Connection
):
    return dict(
        applicable_asset_types={"Link"},
        applicable_other_asset_types={"File"},
        applicable_glossaries={glossary.qualified_name},
        applicable_glossary_types={"AtlasGlossary", "AtlasGlossaryTerm"},
        applicable_connections={connection.qualified_name},
    )


@pytest.fixture(scope="module")
def cm_ipr(
    client: AtlanClient, limit_attribute_applicability_kwargs
) -> Generator[CustomMetadataDef, None, None]:
    attribute_defs = [
        AttributeDef.create(
            display_name=CM_ATTR_IPR_LICENSE,
            attribute_type=AtlanCustomAttributePrimitiveType.STRING,
            **limit_attribute_applicability_kwargs,
        ),
        AttributeDef.create(
            display_name=CM_ATTR_IPR_VERSION,
            attribute_type=AtlanCustomAttributePrimitiveType.DECIMAL,
        ),
        AttributeDef.create(
            display_name=CM_ATTR_IPR_MANDATORY,
            attribute_type=AtlanCustomAttributePrimitiveType.BOOLEAN,
        ),
        AttributeDef.create(
            display_name=CM_ATTR_IPR_DATE,
            attribute_type=AtlanCustomAttributePrimitiveType.DATE,
        ),
        AttributeDef.create(
            display_name=CM_ATTR_IPR_URL,
            attribute_type=AtlanCustomAttributePrimitiveType.URL,
        ),
    ]
    cm = create_custom_metadata(
        client, name=CM_IPR, attribute_defs=attribute_defs, logo="⚖️", locked=True
    )
    yield cm
    client.typedef.purge(CM_IPR, CustomMetadataDef)


def test_cm_ipr(cm_ipr: CustomMetadataDef, limit_attribute_applicability_kwargs):
    cm_name = CM_IPR
    assert cm_ipr.category == AtlanTypeCategory.CUSTOM_METADATA
    assert cm_ipr.guid
    assert cm_ipr.name != cm_name
    assert cm_ipr.display_name == cm_name
    attributes = cm_ipr.attribute_defs
    assert attributes
    assert len(attributes) == 5
    one_with_limited = attributes[0]
    assert one_with_limited
    assert one_with_limited.options
    assert one_with_limited.display_name == CM_ATTR_IPR_LICENSE
    assert one_with_limited.name
    assert one_with_limited.name != CM_ATTR_IPR_LICENSE
    assert one_with_limited.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert not one_with_limited.options.multi_value_select
    options = one_with_limited.options
    for attribute in limit_attribute_applicability_kwargs.keys():
        assert getattr(
            one_with_limited, attribute
        ) == limit_attribute_applicability_kwargs.get(attribute)
        assert getattr(options, attribute) == json.dumps(
            list(limit_attribute_applicability_kwargs.get(attribute))
        )
    one = attributes[1]
    assert one.display_name == CM_ATTR_IPR_VERSION
    assert one.name != CM_ATTR_IPR_VERSION
    assert one.type_name == AtlanCustomAttributePrimitiveType.DECIMAL.value
    assert one.options
    assert not one.options.multi_value_select
    one = attributes[2]
    assert one.display_name == CM_ATTR_IPR_MANDATORY
    assert one.name != CM_ATTR_IPR_MANDATORY
    assert one.type_name == AtlanCustomAttributePrimitiveType.BOOLEAN.value
    assert one.options
    assert not one.options.multi_value_select
    one = attributes[3]
    assert one.display_name == CM_ATTR_IPR_DATE
    assert one.name != CM_ATTR_IPR_DATE
    assert one.type_name == AtlanCustomAttributePrimitiveType.DATE.value
    assert one.options
    assert not one.options.multi_value_select
    one = attributes[4]
    assert one.display_name == CM_ATTR_IPR_URL
    assert one.name != CM_ATTR_IPR_URL
    assert one.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert one.options
    assert not one.options.multi_value_select


@pytest.fixture(scope="module")
def cm_raci(
    client: AtlanClient,
) -> Generator[CustomMetadataDef, None, None]:
    attribute_defs = [
        AttributeDef.create(
            display_name=CM_ATTR_RACI_RESPONSIBLE,
            attribute_type=AtlanCustomAttributePrimitiveType.USERS,
            multi_valued=True,
        ),
        AttributeDef.create(
            display_name=CM_ATTR_RACI_ACCOUNTABLE,
            attribute_type=AtlanCustomAttributePrimitiveType.USERS,
        ),
        AttributeDef.create(
            display_name=CM_ATTR_RACI_CONSULTED,
            attribute_type=AtlanCustomAttributePrimitiveType.GROUPS,
            multi_valued=True,
        ),
        AttributeDef.create(
            display_name=CM_ATTR_RACI_INFORMED,
            attribute_type=AtlanCustomAttributePrimitiveType.GROUPS,
            multi_valued=True,
        ),
        AttributeDef.create(
            display_name=CM_ATTR_RACI_EXTRA,
            attribute_type=AtlanCustomAttributePrimitiveType.STRING,
        ),
    ]
    cm = create_custom_metadata(
        client,
        name=CM_RACI,
        attribute_defs=attribute_defs,
        icon=AtlanIcon.USERS_THREE,
        color=AtlanTagColor.GRAY,
        locked=False,
    )
    yield cm
    client.typedef.purge(CM_RACI, CustomMetadataDef)


def test_cm_raci(
    cm_raci: CustomMetadataDef,
):
    assert cm_raci.category == AtlanTypeCategory.CUSTOM_METADATA
    assert cm_raci.name
    assert cm_raci.guid
    cm_name = CM_RACI
    assert cm_raci.name != cm_name
    assert cm_raci.display_name == cm_name
    attributes = cm_raci.attribute_defs
    assert attributes
    assert len(attributes) == 5
    one = attributes[0]
    assert one
    assert one.display_name == CM_ATTR_RACI_RESPONSIBLE
    assert one.name
    assert one.name != CM_ATTR_RACI_RESPONSIBLE
    assert one.type_name == f"array<{AtlanCustomAttributePrimitiveType.STRING.value}>"
    assert one.options
    assert one.options.multi_value_select
    one = attributes[1]
    assert one.display_name == CM_ATTR_RACI_ACCOUNTABLE
    assert one.name != CM_ATTR_RACI_ACCOUNTABLE
    assert one.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert one.options
    assert not one.options.multi_value_select
    one = attributes[2]
    assert one.display_name == CM_ATTR_RACI_CONSULTED
    assert one.name != CM_ATTR_RACI_CONSULTED
    assert one.type_name == f"array<{AtlanCustomAttributePrimitiveType.STRING.value}>"
    assert one.options
    assert one.options.multi_value_select
    one = attributes[3]
    assert one.display_name == CM_ATTR_RACI_INFORMED
    assert one.name != CM_ATTR_RACI_INFORMED
    assert one.type_name == f"array<{AtlanCustomAttributePrimitiveType.STRING.value}>"
    assert one.options
    assert one.options.multi_value_select
    one = attributes[4]
    assert one.display_name == CM_ATTR_RACI_EXTRA
    assert one.name != CM_ATTR_RACI_EXTRA
    assert one.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert one.options
    assert not one.options.multi_value_select


@pytest.fixture(scope="module")
def cm_enum(
    client: AtlanClient,
) -> Generator[EnumDef, None, None]:
    enum_def = create_enum(client, name=DQ_ENUM, values=DQ_TYPE_LIST)
    yield enum_def
    client.typedef.purge(DQ_ENUM, EnumDef)


def test_cm_enum(
    cm_enum: EnumDef,
):
    assert cm_enum.category == AtlanTypeCategory.ENUM
    assert cm_enum.name == DQ_ENUM
    assert cm_enum.guid
    assert cm_enum.element_defs
    assert len(cm_enum.element_defs) == len(DQ_TYPE_LIST)


@pytest.mark.order(after="test_cm_enum")
def test_cm_enum_get_by_name(client: AtlanClient):
    cm_enum = client.typedef.get_by_name(name=DQ_ENUM)

    assert cm_enum and isinstance(cm_enum, EnumDef)
    assert cm_enum.guid
    assert cm_enum.element_defs
    assert cm_enum.name == DQ_ENUM
    assert cm_enum.category == AtlanTypeCategory.ENUM
    assert len(cm_enum.element_defs) == len(DQ_TYPE_LIST)


@pytest.fixture(scope="module")
def cm_enum_update(
    client: AtlanClient,
) -> Generator[EnumDef, None, None]:
    enum_def = update_enum(client, name=DQ_ENUM, values=DQ_TYPE_EXTRA_LIST)
    yield enum_def


@pytest.fixture(scope="module")
def cm_enum_update_with_replace(
    client: AtlanClient,
) -> Generator[EnumDef, None, None]:
    enum_def = update_enum(
        client, name=DQ_ENUM, values=DQ_TYPE_LIST, replace_existing=True
    )
    yield enum_def


@pytest.mark.order(after="test_cm_enum")
def test_cm_enum_update(
    cm_enum_update: EnumDef,
    cm_enum_update_with_replace: EnumDef,
):
    assert cm_enum_update.guid
    assert cm_enum_update.name == DQ_ENUM
    assert cm_enum_update.element_defs
    assert cm_enum_update.category == AtlanTypeCategory.ENUM
    EM_VALUES = DQ_TYPE_LIST + DQ_TYPE_EXTRA_LIST
    assert len(cm_enum_update.element_defs) == len(EM_VALUES)
    for index, element_def in enumerate(cm_enum_update.element_defs):
        assert element_def.value == EM_VALUES[index]

    assert cm_enum_update_with_replace.guid
    assert cm_enum_update_with_replace.name == DQ_ENUM
    assert cm_enum_update_with_replace.element_defs
    assert cm_enum_update_with_replace.category == AtlanTypeCategory.ENUM
    assert len(cm_enum_update_with_replace.element_defs) == len(DQ_TYPE_LIST)


@pytest.fixture(scope="module")
def cm_dq(
    client: AtlanClient,
    cm_enum: EnumDef,
) -> Generator[CustomMetadataDef, None, None]:
    attribute_defs = [
        AttributeDef.create(
            display_name=CM_ATTR_QUALITY_COUNT,
            attribute_type=AtlanCustomAttributePrimitiveType.INTEGER,
        ),
        AttributeDef.create(
            display_name=CM_ATTR_QUALITY_SQL,
            attribute_type=AtlanCustomAttributePrimitiveType.SQL,
        ),
        AttributeDef.create(
            display_name=CM_ATTR_QUALITY_TYPE,
            attribute_type=AtlanCustomAttributePrimitiveType.OPTIONS,
            options_name=DQ_ENUM,
        ),
    ]
    cm = create_custom_metadata(
        client,
        name=CM_QUALITY,
        attribute_defs=attribute_defs,
        logo="https://github.com/great-expectations/great_expectations/raw/develop/docs/docusaurus/static/img/"
        "gx-mark-160.png",
        locked=True,
    )
    yield cm
    client.typedef.purge(CM_QUALITY, CustomMetadataDef)


def test_cm_dq(
    cm_dq: CustomMetadataDef,
):
    cm_name = CM_QUALITY
    assert cm_dq.category == AtlanTypeCategory.CUSTOM_METADATA
    assert cm_dq.name
    assert cm_dq.guid
    assert cm_dq.name != cm_name
    assert cm_dq.display_name == cm_name
    attributes = cm_dq.attribute_defs
    assert attributes
    assert len(attributes) == 3
    one = attributes[0]
    assert one
    assert one.display_name == CM_ATTR_QUALITY_COUNT
    assert one.name
    assert one.name != CM_ATTR_QUALITY_COUNT
    assert one.type_name == AtlanCustomAttributePrimitiveType.INTEGER.value
    assert one.options
    assert not one.options.multi_value_select
    one = attributes[1]
    assert one.display_name == CM_ATTR_QUALITY_SQL
    assert one.name != CM_ATTR_QUALITY_SQL
    assert one.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert one.options
    assert not one.options.multi_value_select
    assert one.options.custom_type == AtlanCustomAttributePrimitiveType.SQL.value
    one = attributes[2]
    assert one.display_name == CM_ATTR_QUALITY_TYPE
    assert one.name != CM_ATTR_QUALITY_TYPE
    assert one.type_name == DQ_ENUM
    assert one.options
    assert not one.options.multi_value_select
    assert one.options.primitive_type == AtlanCustomAttributePrimitiveType.OPTIONS.value


@pytest.fixture(scope="module")
def glossary(
    client: AtlanClient,
) -> Generator[AtlasGlossary, None, None]:
    glossary_name = MODULE_NAME
    g = create_glossary(client, name=glossary_name)
    yield g
    delete_asset(client, guid=g.guid, asset_type=AtlasGlossary)


@pytest.fixture(scope="module")
def term(
    client: AtlanClient,
    glossary: AtlasGlossary,
    cm_raci: CustomMetadataDef,
    cm_ipr: CustomMetadataDef,
    cm_dq: CustomMetadataDef,
) -> Generator[AtlasGlossaryTerm, None, None]:
    term_name = MODULE_NAME
    t = create_term(client, name=term_name, glossary_guid=glossary.guid)
    yield t
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


@pytest.fixture(scope="module")
def groups(
    client: AtlanClient,
    glossary: AtlasGlossary,
    term: AtlasGlossaryTerm,
    cm_raci: CustomMetadataDef,
    cm_ipr: CustomMetadataDef,
    cm_dq: CustomMetadataDef,
) -> Generator[List[CreateGroupResponse], None, None]:
    g1 = create_group(client, GROUP_NAME1)
    g2 = create_group(client, GROUP_NAME2)
    yield [g1, g2]
    delete_group(client, g1.group)
    delete_group(client, g2.group)


def _get_groups(
    client: AtlanClient,
) -> Tuple[AtlanGroup, AtlanGroup]:
    candidates = client.group.get_by_name(GROUP_NAME1)
    assert candidates
    assert len(candidates) == 1
    group1 = candidates[0]
    candidates = client.group.get_by_name(GROUP_NAME2)
    assert candidates
    assert len(candidates) == 1
    group2 = candidates[0]
    return group1, group2


def test_add_term_cm_raci(
    client: AtlanClient,
    cm_raci: CustomMetadataDef,
    term: AtlasGlossaryTerm,
    groups: List[AtlanGroup],
):
    cm_name = CM_RACI
    raci_attrs = CustomMetadataDict(cm_name)
    _validate_raci_empty(raci_attrs)
    group1, group2 = _get_groups(client)
    raci_attrs[CM_ATTR_RACI_RESPONSIBLE] = [FIXED_USER]
    raci_attrs[CM_ATTR_RACI_ACCOUNTABLE] = FIXED_USER
    raci_attrs[CM_ATTR_RACI_CONSULTED] = [group1.name]
    raci_attrs[CM_ATTR_RACI_INFORMED] = [group1.name, group2.name]
    client.asset.update_custom_metadata_attributes(term.guid, raci_attrs)
    t = client.asset.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_raci_attributes(client, t.get_custom_metadata(name=cm_name))


def test_add_term_cm_ipr(
    client: AtlanClient,
    cm_ipr: CustomMetadataDef,
    term: AtlasGlossaryTerm,
):
    cm_name = CM_IPR
    ipr_attrs = CustomMetadataDict(cm_name)
    _validate_ipr_empty(ipr_attrs)
    ipr_attrs[CM_ATTR_IPR_LICENSE] = "CC BY"
    ipr_attrs[CM_ATTR_IPR_VERSION] = 2.0
    ipr_attrs[CM_ATTR_IPR_MANDATORY] = True
    ipr_attrs[CM_ATTR_IPR_DATE] = 1659308400000
    ipr_attrs[CM_ATTR_IPR_URL] = "https://creativecommons.org/licenses/by/2.0/"

    client.asset.update_custom_metadata_attributes(term.guid, ipr_attrs)
    t = client.asset.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_ipr_attributes(t.get_custom_metadata(name=cm_name))


def test_add_term_cm_dq(
    client: AtlanClient,
    cm_dq: CustomMetadataDef,
    term: AtlasGlossaryTerm,
):
    cm_name = CM_QUALITY
    dq_attrs = CustomMetadataDict(cm_name)
    _validate_dq_empty(dq_attrs)
    dq_attrs[CM_ATTR_QUALITY_COUNT] = 42
    dq_attrs[CM_ATTR_QUALITY_SQL] = "SELECT * from SOMEWHERE;"
    dq_attrs[CM_ATTR_QUALITY_TYPE] = "Completeness"
    client.asset.update_custom_metadata_attributes(term.guid, dq_attrs)
    t = client.asset.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_dq_attributes(t.get_custom_metadata(name=cm_name))


@pytest.mark.order(after="test_add_term_cm_dq")
def test_update_term_cm_ipr(
    client: AtlanClient,
    cm_ipr: CustomMetadataDef,
    term: AtlasGlossaryTerm,
):
    cm_name = CM_IPR
    ipr = CustomMetadataDict(cm_name)
    # Note: MUST access the getter / setter, not the underlying store
    ipr[CM_ATTR_IPR_MANDATORY] = False
    client.asset.update_custom_metadata_attributes(term.guid, ipr)
    t = client.asset.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_ipr_attributes(t.get_custom_metadata(name=cm_name), mandatory=False)
    _validate_raci_attributes(client, t.get_custom_metadata(name=CM_RACI))
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))


@pytest.mark.order(after="test_update_term_cm_ipr")
def test_replace_term_cm_raci(
    client: AtlanClient,
    cm_raci: CustomMetadataDef,
    term: AtlasGlossaryTerm,
):
    raci = CustomMetadataDict(CM_RACI)
    group1, group2 = _get_groups(client)
    raci[CM_ATTR_RACI_RESPONSIBLE] = [FIXED_USER]
    raci[CM_ATTR_RACI_ACCOUNTABLE] = FIXED_USER
    raci[CM_ATTR_RACI_CONSULTED] = None
    raci[CM_ATTR_RACI_INFORMED] = [group1.name, group2.name]
    client.asset.replace_custom_metadata(term.guid, raci)
    t = client.asset.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_raci_attributes_replacement(client, t.get_custom_metadata(name=CM_RACI))
    _validate_ipr_attributes(t.get_custom_metadata(name=CM_IPR), mandatory=False)
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))


@pytest.mark.order(after="test_replace_term_cm_raci")
def test_replace_term_cm_ipr(
    client: AtlanClient,
    cm_ipr: CustomMetadataDef,
    term: AtlasGlossaryTerm,
):
    term_cm_ipr = CustomMetadataDict(CM_IPR)
    client.asset.replace_custom_metadata(term.guid, term_cm_ipr)
    t = client.asset.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_raci_attributes_replacement(client, t.get_custom_metadata(name=CM_RACI))
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))
    _validate_ipr_empty(t.get_custom_metadata(name=CM_IPR))


@pytest.mark.order(after="test_replace_term_cm_ipr")
def test_search_by_any_accountable(
    client: AtlanClient,
    cm_raci: CustomMetadataDef,
    glossary: AtlasGlossary,
    term: AtlasGlossaryTerm,
):
    attributes = ["name", "anchor"]
    cm_attributes = CustomMetadataCache.get_attributes_for_search_results(
        set_name=CM_RACI
    )
    assert cm_attributes
    attributes.extend(cm_attributes)
    request = (
        FluentSearch(_includes_on_results=attributes)
        .where(CompoundQuery.active_assets())
        .where(CompoundQuery.asset_type(AtlasGlossaryTerm))
        .where(CustomMetadataField(CM_RACI, CM_ATTR_RACI_ACCOUNTABLE).has_any_value())
        .include_on_relations(Asset.NAME)
    ).to_request()
    response = client.asset.search(criteria=request)
    assert response
    count = 0
    # TODO: replace with exponential back-off and jitter
    while response.count == 0 and count < 10:
        time.sleep(2)
        response = client.asset.search(criteria=request)
        count += 1
    assert response.count == 1
    for t in response:
        assert isinstance(t, AtlasGlossaryTerm)
        assert t.guid == term.guid
        assert t.qualified_name == term.qualified_name
        anchor = t.attributes.anchor
        assert anchor
        assert anchor.name == glossary.name
        _validate_raci_attributes_replacement(
            client, t.get_custom_metadata(name=CM_RACI)
        )


@pytest.mark.order(after="test_replace_term_cm_ipr")
def test_search_by_specific_accountable(
    client: AtlanClient,
    cm_raci: CustomMetadataDef,
    glossary: AtlasGlossary,
    term: AtlasGlossaryTerm,
):
    request = (
        FluentSearch()
        .where(CompoundQuery.active_assets())
        .where(CompoundQuery.asset_type(AtlasGlossaryTerm))
        .where(CustomMetadataField(CM_RACI, CM_ATTR_RACI_ACCOUNTABLE).eq(FIXED_USER))
        .include_on_results(Asset.NAME)
        .include_on_results(AtlasGlossaryTerm.ANCHOR)
        .include_on_relations(Asset.NAME)
    ).to_request()
    response = client.asset.search(criteria=request)
    assert response
    count = 0
    # TODO: replace with exponential back-off and jitter
    while response.count == 0 and count < 10:
        time.sleep(2)
        response = client.asset.search(criteria=request)
        count += 1
    assert response.count == 1
    for t in response:
        assert isinstance(t, AtlasGlossaryTerm)
        assert t.guid == term.guid
        assert t.qualified_name == term.qualified_name
        anchor = t.attributes.anchor
        assert anchor
        assert anchor.name == glossary.name


@pytest.mark.order(
    after=["test_search_by_any_accountable", "test_search_by_specific_accountable"]
)
def test_remove_term_cm_raci(
    client: AtlanClient,
    cm_raci: CustomMetadataDef,
    term: AtlasGlossaryTerm,
):
    client.asset.remove_custom_metadata(term.guid, cm_name=CM_RACI)
    t = client.asset.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))
    _validate_ipr_empty(t.get_custom_metadata(name=CM_IPR))
    _validate_raci_empty(t.get_custom_metadata(name=CM_RACI))


@pytest.mark.order(after="test_remove_term_cm_raci")
def test_remove_term_cm_ipr(
    client: AtlanClient,
    cm_ipr: CustomMetadataDef,
    term: AtlasGlossaryTerm,
):
    client.asset.remove_custom_metadata(term.guid, cm_name=CM_IPR)
    t = client.asset.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))
    _validate_ipr_empty(t.get_custom_metadata(name=CM_IPR))
    _validate_raci_empty(t.get_custom_metadata(name=CM_RACI))


@pytest.mark.order(after="test_remove_term_cm_raci")
def test_remove_attribute(client: AtlanClient, cm_raci: CustomMetadataDef):
    global _removal_epoch
    cm_name = CM_RACI
    existing = CustomMetadataCache.get_custom_metadata_def(name=cm_name)
    existing_attrs = existing.attribute_defs
    updated_attrs = []
    for existing_attr in existing_attrs:
        to_keep = existing_attr
        if existing_attr.display_name == CM_ATTR_RACI_EXTRA:
            to_keep = existing_attr.archive(by="test-automation")
            assert to_keep.options
            _removal_epoch = to_keep.options.archived_at
        updated_attrs.append(to_keep)
    existing.attribute_defs = updated_attrs
    response = client.typedef.update(existing)
    assert response
    assert len(response.custom_metadata_defs) == 1
    updated = response.custom_metadata_defs[0]
    assert updated.category == AtlanTypeCategory.CUSTOM_METADATA
    assert updated.name != cm_name
    assert updated.guid
    assert updated.display_name == cm_name
    attributes = updated.attribute_defs
    archived = _validate_raci_structure(attributes, 5)
    assert archived
    assert (
        archived.display_name == f"{CM_ATTR_RACI_EXTRA}-archived-{str(_removal_epoch)}"
    )
    assert archived.name != CM_ATTR_RACI_EXTRA
    assert archived.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert not archived.options.multi_value_select
    assert archived.is_archived()


@pytest.mark.order(after="test_remove_attribute")
def test_retrieve_structures(client: AtlanClient, cm_raci: CustomMetadataDef):
    global _removal_epoch
    custom_attributes = CustomMetadataCache.get_all_custom_attributes()
    assert custom_attributes
    assert len(custom_attributes) >= 3
    assert CM_RACI in custom_attributes.keys()
    assert CM_IPR in custom_attributes.keys()
    assert CM_QUALITY in custom_attributes.keys()
    extra = _validate_raci_structure(custom_attributes.get(CM_RACI), 4)
    assert not extra
    custom_attributes = CustomMetadataCache.get_all_custom_attributes(
        include_deleted=True
    )
    assert custom_attributes
    assert CM_RACI in custom_attributes.keys()
    assert CM_IPR in custom_attributes.keys()
    assert CM_QUALITY in custom_attributes.keys()
    extra = _validate_raci_structure(custom_attributes.get(CM_RACI), 5)
    assert extra
    assert extra.display_name == f"{CM_ATTR_RACI_EXTRA}-archived-{str(_removal_epoch)}"
    assert extra.name != CM_ATTR_RACI_EXTRA
    assert extra.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert "Database" in extra.applicable_asset_types
    assert not extra.options.multi_value_select
    assert extra.is_archived()


@pytest.mark.order(after="test_retrieve_structures")
def test_recreate_attribute(client: AtlanClient, cm_raci: CustomMetadataDef):
    existing = CustomMetadataCache.get_custom_metadata_def(name=CM_RACI)
    existing_attrs = existing.attribute_defs
    updated_attrs = []
    for existing_attr in existing_attrs:
        existing_attr.is_new = None
        updated_attrs.append(existing_attr)
    new_attr = AttributeDef.create(
        display_name=CM_ATTR_RACI_EXTRA,
        attribute_type=AtlanCustomAttributePrimitiveType.STRING,
    )
    updated_attrs.append(new_attr)
    existing.attribute_defs = updated_attrs
    response = client.typedef.update(existing)
    assert response
    assert len(response.custom_metadata_defs) == 1
    updated = response.custom_metadata_defs[0]
    assert updated.category == AtlanTypeCategory.CUSTOM_METADATA
    assert updated.name != CM_RACI
    assert updated.guid
    assert updated.display_name == CM_RACI
    attributes = updated.attribute_defs
    extra = _validate_raci_structure(attributes, 6)
    assert extra
    assert extra.display_name == CM_ATTR_RACI_EXTRA
    assert extra.name != CM_ATTR_RACI_EXTRA
    assert extra.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert not extra.options.multi_value_select
    assert not extra.is_archived()


@pytest.mark.order(after="test_recreate_attribute")
def test_retrieve_structure_without_archived(
    client: AtlanClient, cm_raci: CustomMetadataDef
):
    custom_attributes = CustomMetadataCache.get_all_custom_attributes()
    assert custom_attributes
    assert len(custom_attributes) >= 3
    assert CM_RACI in custom_attributes.keys()
    assert CM_IPR in custom_attributes.keys()
    assert CM_QUALITY in custom_attributes.keys()
    extra = _validate_raci_structure(custom_attributes.get(CM_RACI), 5)
    assert extra
    assert extra.display_name == CM_ATTR_RACI_EXTRA
    assert extra.name != CM_ATTR_RACI_EXTRA
    assert extra.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert "Database" in extra.applicable_asset_types
    assert not extra.is_archived()


@pytest.mark.order(after="test_recreate_attribute")
def test_retrieve_structure_with_archived(
    client: AtlanClient, cm_raci: CustomMetadataDef
):
    custom_attributes = CustomMetadataCache.get_all_custom_attributes(
        include_deleted=True
    )
    assert custom_attributes
    assert len(custom_attributes) >= 3
    assert CM_RACI in custom_attributes.keys()
    assert CM_IPR in custom_attributes.keys()
    assert CM_QUALITY in custom_attributes.keys()
    extra = _validate_raci_structure(custom_attributes.get(CM_RACI), 6)
    assert extra
    assert extra.display_name == CM_ATTR_RACI_EXTRA
    assert extra.name != CM_ATTR_RACI_EXTRA
    assert extra.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert "Database" in extra.applicable_asset_types
    assert not extra.is_archived()


@pytest.mark.order(after="test_recreate_attribute")
def test_update_replacing_cm(
    term: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
    cm_raci: CustomMetadataDef,
    cm_ipr: CustomMetadataDef,
    cm_dq: CustomMetadataDef,
    client: AtlanClient,
):
    raci = CustomMetadataDict(CM_RACI)
    group1, group2 = _get_groups(client)
    raci[CM_ATTR_RACI_RESPONSIBLE] = [FIXED_USER]
    raci[CM_ATTR_RACI_ACCOUNTABLE] = FIXED_USER
    raci[CM_ATTR_RACI_CONSULTED] = [group1.name]
    raci[CM_ATTR_RACI_INFORMED] = [group1.name, group2.name]
    raci[CM_ATTR_RACI_EXTRA] = "something extra..."
    assert term.qualified_name
    assert term.name
    to_update = AtlasGlossaryTerm.create_for_modification(
        qualified_name=term.qualified_name, name=term.name, glossary_guid=glossary.guid
    )
    to_update.set_custom_metadata(custom_metadata=raci)
    response = client.asset.update_replacing_cm(to_update, replace_atlan_tags=False)
    assert response
    assert len(response.assets_deleted(asset_type=AtlasGlossaryTerm)) == 0
    assert len(response.assets_created(asset_type=AtlasGlossaryTerm)) == 0
    assert len(response.assets_updated(asset_type=AtlasGlossaryTerm)) == 1
    t = response.assets_updated(asset_type=AtlasGlossaryTerm)[0]
    assert isinstance(t, AtlasGlossaryTerm)
    assert t.guid == term.guid
    assert t.qualified_name == term.qualified_name
    assert term.qualified_name
    x = client.asset.get_by_qualified_name(
        qualified_name=term.qualified_name, asset_type=AtlasGlossaryTerm
    )
    assert x
    assert not x.is_incomplete
    assert x.qualified_name == term.qualified_name
    raci = x.get_custom_metadata(CM_RACI)
    _validate_raci_attributes(client, raci)
    assert raci[CM_ATTR_RACI_EXTRA] == "something extra..."
    _validate_ipr_empty(x.get_custom_metadata(CM_IPR))
    _validate_dq_empty(x.get_custom_metadata(CM_QUALITY))


# TODO: test entity audit retrieval and parsing, once available


def _validate_raci_attributes(client: AtlanClient, cma: CustomMetadataDict):
    assert cma
    # Note: MUST access the getter / setter, not the underlying store
    responsible = cma[CM_ATTR_RACI_RESPONSIBLE]
    accountable = cma[CM_ATTR_RACI_ACCOUNTABLE]
    consulted = cma[CM_ATTR_RACI_CONSULTED]
    informed = cma[CM_ATTR_RACI_INFORMED]
    group1, group2 = _get_groups(client)
    assert responsible
    assert len(responsible) == 1
    assert FIXED_USER in responsible
    assert accountable
    assert accountable == FIXED_USER
    assert consulted == [group1.name]
    assert informed == [group1.name, group2.name]


def _validate_raci_attributes_replacement(client: AtlanClient, cma: CustomMetadataDict):
    assert cma
    # Note: MUST access the getter / setter, not the underlying store
    responsible = cma[CM_ATTR_RACI_RESPONSIBLE]
    accountable = cma[CM_ATTR_RACI_ACCOUNTABLE]
    consulted = cma[CM_ATTR_RACI_CONSULTED]
    informed = cma[CM_ATTR_RACI_INFORMED]
    group1, group2 = _get_groups(client)
    assert responsible
    assert responsible == [FIXED_USER]
    assert accountable
    assert accountable == FIXED_USER
    assert not consulted
    assert informed == [group1.name, group2.name]


def _validate_raci_empty(raci_attrs: CustomMetadataDict):
    attribute_names = raci_attrs.attribute_names
    assert CM_ATTR_RACI_RESPONSIBLE in attribute_names
    assert CM_ATTR_RACI_ACCOUNTABLE in attribute_names
    assert CM_ATTR_RACI_CONSULTED in attribute_names
    assert CM_ATTR_RACI_INFORMED in attribute_names
    assert CM_ATTR_RACI_EXTRA in attribute_names
    assert not raci_attrs[CM_ATTR_RACI_RESPONSIBLE]
    assert raci_attrs[CM_ATTR_RACI_ACCOUNTABLE] is None
    assert not raci_attrs[CM_ATTR_RACI_CONSULTED]  # could be empty list
    assert not raci_attrs[CM_ATTR_RACI_INFORMED]  # could be empty list
    assert raci_attrs[CM_ATTR_RACI_EXTRA] is None


def _validate_ipr_attributes(cma: CustomMetadataDict, mandatory: bool = True):
    assert cma
    license = cma[CM_ATTR_IPR_LICENSE]
    v = cma[CM_ATTR_IPR_VERSION]
    m = cma[CM_ATTR_IPR_MANDATORY]
    d = cma[CM_ATTR_IPR_DATE]
    u = cma[CM_ATTR_IPR_URL]
    assert license
    assert license == "CC BY"
    assert v
    assert v == 2.0
    if mandatory:
        assert m
    else:
        assert not m
    assert d
    assert d == 1659308400000
    assert u
    assert u == "https://creativecommons.org/licenses/by/2.0/"


def _validate_ipr_empty(ipr_attrs: CustomMetadataDict):
    attribute_names = ipr_attrs.attribute_names
    assert CM_ATTR_IPR_LICENSE in attribute_names
    assert CM_ATTR_IPR_VERSION in attribute_names
    assert CM_ATTR_IPR_MANDATORY in attribute_names
    assert CM_ATTR_IPR_DATE in attribute_names
    assert CM_ATTR_IPR_URL in attribute_names
    assert ipr_attrs[CM_ATTR_IPR_LICENSE] is None
    assert ipr_attrs[CM_ATTR_IPR_VERSION] is None
    assert ipr_attrs[CM_ATTR_IPR_MANDATORY] is None
    assert ipr_attrs[CM_ATTR_IPR_DATE] is None
    assert ipr_attrs[CM_ATTR_IPR_URL] is None


def _validate_dq_attributes(cma: CustomMetadataDict):
    assert cma
    c = cma[CM_ATTR_QUALITY_COUNT]
    s = cma[CM_ATTR_QUALITY_SQL]
    t = cma[CM_ATTR_QUALITY_TYPE]
    assert c
    assert c == 42
    assert s
    assert s == "SELECT * from SOMEWHERE;"
    assert t
    assert t == "Completeness"


def _validate_dq_empty(dq_attrs: CustomMetadataDict):
    attribute_names = dq_attrs.attribute_names
    assert CM_ATTR_QUALITY_COUNT in attribute_names
    assert CM_ATTR_QUALITY_SQL in attribute_names
    assert CM_ATTR_QUALITY_TYPE in attribute_names
    assert dq_attrs[CM_ATTR_QUALITY_COUNT] is None
    assert dq_attrs[CM_ATTR_QUALITY_SQL] is None
    assert dq_attrs[CM_ATTR_QUALITY_TYPE] is None


def _validate_raci_structure(
    attributes: Optional[List[AttributeDef]], total_expected: int
):
    global _removal_epoch
    assert attributes
    assert len(attributes) == total_expected
    one = attributes[0]
    assert one.display_name == CM_ATTR_RACI_RESPONSIBLE
    assert one.name != CM_ATTR_RACI_RESPONSIBLE
    assert one.type_name == f"array<{AtlanCustomAttributePrimitiveType.STRING.value}>"
    assert one.options
    assert "Database" in one.applicable_asset_types
    assert not one.is_archived()
    assert one.options.multi_value_select
    assert one.options.custom_type == AtlanCustomAttributePrimitiveType.USERS.value
    one = attributes[1]
    assert one.display_name == CM_ATTR_RACI_ACCOUNTABLE
    assert one.name != CM_ATTR_RACI_ACCOUNTABLE
    assert one.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert one.options
    assert "Table" in one.applicable_asset_types
    assert not one.is_archived()
    assert not one.options.multi_value_select
    assert one.options.custom_type == AtlanCustomAttributePrimitiveType.USERS.value
    one = attributes[2]
    assert one.display_name == CM_ATTR_RACI_CONSULTED
    assert one.name != CM_ATTR_RACI_CONSULTED
    assert one.type_name == f"array<{AtlanCustomAttributePrimitiveType.STRING.value}>"
    assert one.options
    assert "Column" in one.applicable_asset_types
    assert not one.is_archived()
    assert one.options.multi_value_select
    assert one.options.custom_type == AtlanCustomAttributePrimitiveType.GROUPS.value
    one = attributes[3]
    assert one.display_name == CM_ATTR_RACI_INFORMED
    assert not one.name == CM_ATTR_RACI_INFORMED
    assert one.type_name == f"array<{AtlanCustomAttributePrimitiveType.STRING.value}>"
    assert one.options
    assert "MaterialisedView" in one.applicable_asset_types
    assert not one.is_archived()
    assert one.options.multi_value_select
    assert one.options.custom_type == AtlanCustomAttributePrimitiveType.GROUPS.value
    if total_expected > 5:
        # If we're expecting more than 5, then the penultimate must be an archived CM_ATTR_EXTRA
        one = attributes[4]
        assert (
            one.display_name == f"{CM_ATTR_RACI_EXTRA}-archived-{str(_removal_epoch)}"
        )
        assert one.name != CM_ATTR_RACI_EXTRA
        assert one.type_name == AtlanCustomAttributePrimitiveType.STRING.value
        assert one.options
        assert "AtlasGlossaryTerm" in one.applicable_glossary_types
        assert not one.options.multi_value_select
        assert one.is_archived()
    if total_expected > 4:
        return attributes[total_expected - 1]
    return None


def test_add_badge_cm_dq(
    client: AtlanClient,
    cm_dq: CustomMetadataDef,
):
    badge = Badge.create(
        name=CM_ATTR_QUALITY_COUNT,
        cm_name=CM_QUALITY,
        cm_attribute=CM_ATTR_QUALITY_COUNT,
        badge_conditions=[
            BadgeCondition.create(
                badge_condition_operator=BadgeComparisonOperator.GTE,
                badge_condition_value="5",
                badge_condition_colorhex=BadgeConditionColor.GREEN,
            ),
            BadgeCondition.create(
                badge_condition_operator=BadgeComparisonOperator.LT,
                badge_condition_value="5",
                badge_condition_colorhex=BadgeConditionColor.YELLOW,
            ),
            BadgeCondition.create(
                badge_condition_operator=BadgeComparisonOperator.LTE,
                badge_condition_value="2",
                badge_condition_colorhex=BadgeConditionColor.RED,
            ),
        ],
    )
    badge.user_description = "How many data quality checks ran against this asset."
    assert badge.status == EntityStatus.ACTIVE
    response = client.asset.save(badge)
    assert (badges := response.assets_created(asset_type=Badge))
    assert len(badges) == 1
    client.asset.purge_by_guid(badges[0].guid)
