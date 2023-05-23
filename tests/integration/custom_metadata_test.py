# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import logging
import time
from typing import Generator, List, Optional, Tuple

import pytest

from pyatlan.cache.custom_metadata_cache import CustomMetadataCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.error import NotFoundError
from pyatlan.model.assets import (
    AtlasGlossary,
    AtlasGlossaryTerm,
    Badge,
    BadgeCondition,
    Table,
)
from pyatlan.model.core import CustomMetadata, to_snake_case
from pyatlan.model.enums import (
    AtlanCustomAttributePrimitiveType,
    AtlanTypeCategory,
    BadgeComparisonOperator,
    BadgeConditionColor,
)
from pyatlan.model.group import AtlanGroup, CreateGroupResponse
from pyatlan.model.search import DSL, Bool, Exists, IndexSearchRequest, Term
from pyatlan.model.typedef import AttributeDef, CustomMetadataDef, EnumDef
from tests.integration.client import delete_asset
from tests.integration.glossary_test import create_glossary, create_term
from tests.integration.admin_test import create_group, delete_group

LOGGER = logging.getLogger(__name__)

PREFIX = "psdk-"
CM_PREFIX = f"{PREFIX}CM"
FIXED_USER = "ernest"

CM_RACI = f"{PREFIX}RACI"
CM_IPR = f"{PREFIX}IPR"
CM_QUALITY = f"{PREFIX}DQ"

CM_ATTR_RACI_RESPONSIBLE = "Responsible"
CM_ATTR_RACI_ACCOUNTABLE = "Accountable"
CM_ATTR_RACI_CONSULTED = "Consulted"
CM_ATTR_RACI_INFORMED = "Informed"
CM_ATTR_RACI_EXTRA = "Extra"

CM_ATTR_RACI_RESPONSIBLE_RENAMED = to_snake_case(CM_ATTR_RACI_RESPONSIBLE)
CM_ATTR_RACI_ACCOUNTABLE_RENAMED = to_snake_case(CM_ATTR_RACI_ACCOUNTABLE)
CM_ATTR_RACI_CONSULTED_RENAMED = to_snake_case(CM_ATTR_RACI_CONSULTED)
CM_ATTR_RACI_INFORMED_RENAMED = to_snake_case(CM_ATTR_RACI_INFORMED)
CM_ATTR_RACI_EXTRA_RENAMED = to_snake_case(CM_ATTR_RACI_EXTRA)

CM_ATTR_IPR_LICENSE = "License"
CM_ATTR_IPR_VERSION = "Version"
CM_ATTR_IPR_MANDATORY = "Mandatory"
CM_ATTR_IPR_DATE = "Date"
CM_ATTR_IPR_URL = "URL"

CM_ATTR_IPR_LICENSE_RENAMED = to_snake_case(CM_ATTR_IPR_LICENSE)
CM_ATTR_IPR_VERSION_RENAMED = to_snake_case(CM_ATTR_IPR_VERSION)
CM_ATTR_IPR_MANDATORY_RENAMED = to_snake_case(CM_ATTR_IPR_MANDATORY)
CM_ATTR_IPR_DATE_RENAMED = to_snake_case(CM_ATTR_IPR_DATE)
CM_ATTR_IPR_URL_RENAMED = to_snake_case(CM_ATTR_IPR_URL)

CM_ATTR_QUALITY_COUNT = "Count"
CM_ATTR_QUALITY_SQL = "SQL"
CM_ATTR_QUALITY_TYPE = "Type"
CM_ENUM_DQ_TYPE = f"{PREFIX.replace('-', '_')}DataQualityType"
DQ_TYPE_LIST = [
    "Accuracy",
    "Completeness",
    "Consistency",
    "Timeliness",
    "Validity",
    "Uniqueness",
]

CM_ATTR_QUALITY_COUNT_RENAMED = to_snake_case(CM_ATTR_QUALITY_COUNT)
CM_ATTR_QUALITY_SQL_RENAMED = to_snake_case(CM_ATTR_QUALITY_SQL)
CM_ATTR_QUALITY_TYPE_RENAMED = to_snake_case(CM_ATTR_QUALITY_TYPE)

GROUP_NAME1 = f"{CM_PREFIX}1"
GROUP_NAME2 = f"{CM_PREFIX}2"

_removal_epoch: Optional[int]


def create_custom_metadata(
    client: AtlanClient,
    name: str,
    attribute_defs: List[AttributeDef],
    logo: str,
    locked: bool,
) -> CustomMetadataDef:
    cm_def = CustomMetadataDef.create(display_name=name)
    cm_def.attribute_defs = attribute_defs
    if logo.startswith("http"):
        cm_def.options = CustomMetadataDef.Options.with_logo_from_url(logo, locked)
    else:
        cm_def.options = CustomMetadataDef.Options.with_logo_as_emoji(logo, locked)
    r = client.create_typedef(cm_def)
    return r.custom_metadata_defs[0]


def create_enum(client: AtlanClient, name: str, values: List[str]) -> EnumDef:
    enum_def = EnumDef.create(name=name, values=values)
    r = client.create_typedef(enum_def)
    return r.enum_defs[0]


@pytest.fixture(scope="module")
def cm_ipr(client: AtlanClient) -> Generator[CustomMetadataDef, None, None]:
    attribute_defs = [
        AttributeDef.create(
            display_name=CM_ATTR_IPR_LICENSE,
            attribute_type=AtlanCustomAttributePrimitiveType.STRING,
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
        client, name=CM_IPR, attribute_defs=attribute_defs, logo="⚖️", locked=False
    )
    yield cm
    client.purge_typedef(CM_IPR, CustomMetadataDef)


def test_cm_ipr(cm_ipr: CustomMetadataDef):
    assert cm_ipr.category == AtlanTypeCategory.CUSTOM_METADATA
    assert cm_ipr.guid
    assert cm_ipr.name != CM_IPR
    assert cm_ipr.display_name == CM_IPR
    attributes = cm_ipr.attribute_defs
    assert attributes
    assert len(attributes) == 5
    one = attributes[0]
    assert one
    assert one.display_name == CM_ATTR_IPR_LICENSE
    assert one.name
    assert one.name != CM_ATTR_IPR_LICENSE
    assert one.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert one.options
    assert not one.options.multi_value_select
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
def cm_raci(client: AtlanClient) -> Generator[CustomMetadataDef, None, None]:
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
        client, name=CM_RACI, attribute_defs=attribute_defs, logo="👪", locked=False
    )
    yield cm
    client.purge_typedef(CM_RACI, CustomMetadataDef)


def test_cm_raci(cm_raci: CustomMetadataDef):
    assert cm_raci.category == AtlanTypeCategory.CUSTOM_METADATA
    assert cm_raci.name
    assert cm_raci.guid
    assert cm_raci.name != CM_RACI
    assert cm_raci.display_name == CM_RACI
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
def cm_enum(client: AtlanClient) -> Generator[EnumDef, None, None]:
    enum_def = create_enum(client, name=CM_ENUM_DQ_TYPE, values=DQ_TYPE_LIST)
    yield enum_def
    client.purge_typedef(CM_ENUM_DQ_TYPE, EnumDef)


def test_cm_enum(cm_enum: EnumDef):
    assert cm_enum.category == AtlanTypeCategory.ENUM
    assert cm_enum.name == CM_ENUM_DQ_TYPE
    assert cm_enum.guid
    assert cm_enum.element_defs
    assert len(cm_enum.element_defs) == len(DQ_TYPE_LIST)


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
            options_name=CM_ENUM_DQ_TYPE,
        ),
    ]
    cm = create_custom_metadata(
        client,
        name=CM_QUALITY,
        attribute_defs=attribute_defs,
        logo="https://github.com/great-expectations/great_expectations/raw/develop/docs/docusaurus/static/img/"
        "gx-mark-160.png",
        locked=False,
    )
    yield cm
    client.purge_typedef(CM_QUALITY, CustomMetadataDef)


def test_cm_dq(cm_dq: CustomMetadataDef):
    assert cm_dq.category == AtlanTypeCategory.CUSTOM_METADATA
    assert cm_dq.name
    assert cm_dq.guid
    assert cm_dq.name != CM_QUALITY
    assert cm_dq.display_name == CM_QUALITY
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
    assert one.type_name == CM_ENUM_DQ_TYPE
    assert one.options
    assert not one.options.multi_value_select
    assert one.options.primitive_type == AtlanCustomAttributePrimitiveType.OPTIONS.value


@pytest.fixture(scope="module")
def glossary(client: AtlanClient) -> Generator[AtlasGlossary, None, None]:
    g = create_glossary(client, name=CM_PREFIX)
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
    t = create_term(client, name=CM_PREFIX, glossary_guid=glossary.guid)
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
    created = [g1, g2]
    yield created
    delete_group(client, g1.group)
    delete_group(client, g2.group)


def _get_groups(client: AtlanClient) -> Tuple[AtlanGroup, AtlanGroup]:
    candidates = client.get_group_by_name(GROUP_NAME1)
    assert candidates
    assert len(candidates) == 1
    group1 = candidates[0]
    candidates = client.get_group_by_name(GROUP_NAME2)
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
    raci_attrs = term.get_custom_metadata(CM_RACI)
    _validate_raci_empty(raci_attrs)
    group1, group2 = _get_groups(client)
    setattr(raci_attrs, CM_ATTR_RACI_RESPONSIBLE_RENAMED, [FIXED_USER])
    setattr(raci_attrs, CM_ATTR_RACI_ACCOUNTABLE_RENAMED, FIXED_USER)
    setattr(raci_attrs, CM_ATTR_RACI_CONSULTED_RENAMED, [group1.name])
    setattr(raci_attrs, CM_ATTR_RACI_INFORMED_RENAMED, [group1.name, group2.name])
    client.update_custom_metadata_attributes(term.guid, raci_attrs)
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_raci_attributes(client, t.get_custom_metadata(name=CM_RACI))


def test_add_term_cm_ipr(
    client: AtlanClient, cm_ipr: CustomMetadataDef, term: AtlasGlossaryTerm
):
    ipr_attrs = term.get_custom_metadata(CM_IPR)
    _validate_ipr_empty(ipr_attrs)
    setattr(ipr_attrs, CM_ATTR_IPR_LICENSE_RENAMED, "CC BY")
    setattr(ipr_attrs, CM_ATTR_IPR_VERSION_RENAMED, 2.0)
    setattr(ipr_attrs, CM_ATTR_IPR_MANDATORY_RENAMED, True)
    setattr(ipr_attrs, CM_ATTR_IPR_DATE_RENAMED, 1659308400000)
    setattr(
        ipr_attrs,
        CM_ATTR_IPR_URL_RENAMED,
        "https://creativecommons.org/licenses/by/2.0/",
    )
    client.update_custom_metadata_attributes(term.guid, ipr_attrs)
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_ipr_attributes(t.get_custom_metadata(name=CM_IPR))


def test_add_term_cm_dq(
    client: AtlanClient, cm_dq: CustomMetadataDef, term: AtlasGlossaryTerm
):
    dq_attrs = term.get_custom_metadata(CM_QUALITY)
    _validate_dq_empty(dq_attrs)
    setattr(dq_attrs, CM_ATTR_QUALITY_COUNT_RENAMED, 42)
    setattr(dq_attrs, CM_ATTR_QUALITY_SQL_RENAMED, "SELECT * from SOMEWHERE;")
    setattr(dq_attrs, CM_ATTR_QUALITY_TYPE_RENAMED, "Completeness")
    client.update_custom_metadata_attributes(term.guid, dq_attrs)
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))


@pytest.mark.order(after="test_add_term_cm_dq")
def test_update_term_cm_ipr(
    client: AtlanClient, cm_ipr: CustomMetadataDef, term: AtlasGlossaryTerm
):
    ipr = term.get_custom_metadata(CM_IPR)
    # Note: MUST access the getter / setter, not the underlying store
    setattr(ipr, CM_ATTR_IPR_MANDATORY_RENAMED, False)
    client.update_custom_metadata_attributes(term.guid, ipr)
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_ipr_attributes(t.get_custom_metadata(name=CM_IPR), mandatory=False)
    _validate_raci_attributes(client, t.get_custom_metadata(name=CM_RACI))
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))


@pytest.mark.order(after="test_update_term_cm_ipr")
def test_replace_term_cm_raci(
    client: AtlanClient, cm_raci: CustomMetadataDef, term: AtlasGlossaryTerm
):
    raci = term.get_custom_metadata(CM_RACI)
    group1, group2 = _get_groups(client)
    # Note: MUST access the getter / setter, not the underlying store
    setattr(raci, CM_ATTR_RACI_RESPONSIBLE_RENAMED, [FIXED_USER])
    setattr(raci, CM_ATTR_RACI_ACCOUNTABLE_RENAMED, FIXED_USER)
    setattr(raci, CM_ATTR_RACI_CONSULTED_RENAMED, None)
    setattr(raci, CM_ATTR_RACI_INFORMED_RENAMED, [group1.name, group2.name])
    client.replace_custom_metadata(term.guid, raci)
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_raci_attributes_replacement(client, t.get_custom_metadata(name=CM_RACI))
    _validate_ipr_attributes(t.get_custom_metadata(name=CM_IPR), mandatory=False)
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))


@pytest.mark.order(after="test_replace_term_cm_raci")
def test_replace_term_cm_ipr(
    client: AtlanClient, cm_ipr: CustomMetadataDef, term: AtlasGlossaryTerm
):
    client.replace_custom_metadata(term.guid, term.get_custom_metadata(CM_IPR))
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
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
    be_active = Term.with_state("ACTIVE")
    be_a_term = Term.with_type_name("AtlasGlossaryTerm")
    have_attr = Exists.with_custom_metadata(
        set_name=CM_RACI, attr_name=CM_ATTR_RACI_ACCOUNTABLE_RENAMED
    )
    query = Bool(must=[be_active, be_a_term, have_attr])
    dsl = DSL(query=query)
    request = IndexSearchRequest(
        dsl=dsl, attributes=["name", "anchor"], relation_attributes=["name"]
    )
    response = client.search(criteria=request)
    assert response
    count = 0
    # TODO: replace with exponential back-off and jitter
    while response.count == 0 and count < 10:
        time.sleep(2)
        response = client.search(criteria=request)
        count += 1
    assert response.count == 1
    for t in response:
        assert isinstance(t, AtlasGlossaryTerm)
        assert t.guid == term.guid
        assert t.qualified_name == term.qualified_name
        anchor = t.attributes.anchor
        assert anchor
        assert anchor.name == glossary.name


@pytest.mark.order(after="test_replace_term_cm_ipr")
def test_search_by_specific_accountable(
    client: AtlanClient,
    cm_raci: CustomMetadataDef,
    glossary: AtlasGlossary,
    term: AtlasGlossaryTerm,
):
    be_active = Term.with_state("ACTIVE")
    be_a_term = Term.with_type_name("AtlasGlossaryTerm")
    have_attr = Term.with_custom_metadata(
        set_name=CM_RACI, attr_name=CM_ATTR_RACI_ACCOUNTABLE_RENAMED, value=FIXED_USER
    )
    query = Bool(must=[be_active, be_a_term, have_attr])
    dsl = DSL(query=query)
    request = IndexSearchRequest(
        dsl=dsl, attributes=["name", "anchor"], relation_attributes=["name"]
    )
    response = client.search(criteria=request)
    assert response
    count = 0
    # TODO: replace with exponential back-off and jitter
    while response.count == 0 and count < 10:
        time.sleep(2)
        response = client.search(criteria=request)
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
    client: AtlanClient, cm_raci: CustomMetadataDef, term: AtlasGlossaryTerm
):
    client.remove_custom_metadata(term.guid, cm_name=CM_RACI)
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))
    _validate_ipr_empty(t.get_custom_metadata(name=CM_IPR))
    _validate_raci_empty(t.get_custom_metadata(name=CM_RACI))


@pytest.mark.order(after="test_remove_term_cm_raci")
def test_remove_term_cm_ipr(
    client: AtlanClient, cm_ipr: CustomMetadataDef, term: AtlasGlossaryTerm
):
    client.remove_custom_metadata(term.guid, cm_name=CM_IPR)
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))
    _validate_ipr_empty(t.get_custom_metadata(name=CM_IPR))
    _validate_raci_empty(t.get_custom_metadata(name=CM_RACI))


@pytest.mark.order(after="test_remove_term_cm_raci")
def test_remove_attribute(client: AtlanClient, cm_raci: CustomMetadataDef):
    global _removal_epoch
    existing = CustomMetadataCache.get_custom_metadata_def(name=CM_RACI)
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
    response = client.update_typedef(existing)
    assert response
    assert len(response.custom_metadata_defs) == 1
    updated = response.custom_metadata_defs[0]
    assert updated.category == AtlanTypeCategory.CUSTOM_METADATA
    assert updated.name != CM_RACI
    assert updated.guid
    assert updated.display_name == CM_RACI
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
    assert "Database" in extra.options.custom_applicable_entity_types
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
    response = client.update_typedef(existing)
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
    assert "Database" in extra.options.custom_applicable_entity_types
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
    assert "Database" in extra.options.custom_applicable_entity_types
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
    raci = term.get_custom_metadata(CM_RACI)
    group1, group2 = _get_groups(client)
    setattr(raci, CM_ATTR_RACI_RESPONSIBLE_RENAMED, [FIXED_USER])
    setattr(raci, CM_ATTR_RACI_ACCOUNTABLE_RENAMED, FIXED_USER)
    setattr(raci, CM_ATTR_RACI_CONSULTED_RENAMED, [group1.name])
    setattr(raci, CM_ATTR_RACI_INFORMED_RENAMED, [group1.name, group2.name])
    setattr(raci, CM_ATTR_RACI_EXTRA_RENAMED, "something extra...")
    to_update = AtlasGlossaryTerm.create_for_modification(
        qualified_name=term.qualified_name, name=term.name, glossary_guid=glossary.guid
    )
    to_update.set_custom_metadata(custom_metadata=raci)
    response = client.upsert_replacing_cm(to_update, replace_classifications=False)
    assert response
    assert len(response.assets_deleted(asset_type=AtlasGlossaryTerm)) == 0
    assert len(response.assets_created(asset_type=AtlasGlossaryTerm)) == 0
    assert len(response.assets_updated(asset_type=AtlasGlossaryTerm)) == 1
    t = response.assets_updated(asset_type=AtlasGlossaryTerm)[0]
    assert isinstance(t, AtlasGlossaryTerm)
    assert t.guid == term.guid
    assert t.qualified_name == term.qualified_name
    x = client.get_asset_by_qualified_name(
        qualified_name=term.qualified_name, asset_type=AtlasGlossaryTerm
    )
    assert x
    assert not x.is_incomplete
    assert x.qualified_name == term.qualified_name
    raci = x.get_custom_metadata(CM_RACI)
    _validate_raci_attributes(client, raci)
    assert getattr(raci, CM_ATTR_RACI_EXTRA_RENAMED) == "something extra..."
    _validate_ipr_empty(x.get_custom_metadata(CM_IPR))
    _validate_dq_empty(x.get_custom_metadata(CM_QUALITY))


# TODO: test entity audit retrieval and parsing, once available


def test_get_custom_metadata_when_name_is_invalid_then_raises_not_found_error():
    with pytest.raises(
        NotFoundError, match="Custom metadata with name Bogs does not exist"
    ):
        CustomMetadataCache.get_custom_metadata(name="Bogs", asset_type=Table)


def _validate_raci_attributes(client: AtlanClient, cma: CustomMetadata):
    assert cma
    # Note: MUST access the getter / setter, not the underlying store
    responsible = getattr(cma, CM_ATTR_RACI_RESPONSIBLE_RENAMED)
    accountable = getattr(cma, CM_ATTR_RACI_ACCOUNTABLE_RENAMED)
    consulted = getattr(cma, CM_ATTR_RACI_CONSULTED_RENAMED)
    informed = getattr(cma, CM_ATTR_RACI_INFORMED_RENAMED)
    group1, group2 = _get_groups(client)
    assert responsible
    assert len(responsible) == 1
    assert FIXED_USER in responsible
    assert accountable
    assert accountable == FIXED_USER
    assert consulted == [group1.name]
    assert informed == [group1.name, group2.name]


def _validate_raci_attributes_replacement(client: AtlanClient, cma: CustomMetadata):
    assert cma
    # Note: MUST access the getter / setter, not the underlying store
    responsible = getattr(cma, CM_ATTR_RACI_RESPONSIBLE_RENAMED)
    accountable = getattr(cma, CM_ATTR_RACI_ACCOUNTABLE_RENAMED)
    consulted = getattr(cma, CM_ATTR_RACI_CONSULTED_RENAMED)
    informed = getattr(cma, CM_ATTR_RACI_INFORMED_RENAMED)
    group1, group2 = _get_groups(client)
    assert responsible
    assert responsible == [FIXED_USER]
    assert accountable
    assert accountable == FIXED_USER
    assert not consulted
    assert informed == [group1.name, group2.name]


def _validate_raci_empty(raci_attrs: CustomMetadata):
    assert hasattr(raci_attrs, CM_ATTR_RACI_RESPONSIBLE_RENAMED)
    assert hasattr(raci_attrs, CM_ATTR_RACI_ACCOUNTABLE_RENAMED)
    assert hasattr(raci_attrs, CM_ATTR_RACI_CONSULTED_RENAMED)
    assert hasattr(raci_attrs, CM_ATTR_RACI_INFORMED_RENAMED)
    assert hasattr(raci_attrs, CM_ATTR_RACI_EXTRA_RENAMED)
    assert not getattr(
        raci_attrs, CM_ATTR_RACI_RESPONSIBLE_RENAMED
    )  # could be empty list
    assert getattr(raci_attrs, CM_ATTR_RACI_ACCOUNTABLE_RENAMED) is None
    assert not getattr(
        raci_attrs, CM_ATTR_RACI_CONSULTED_RENAMED
    )  # could be empty list
    assert not getattr(raci_attrs, CM_ATTR_RACI_INFORMED_RENAMED)  # could be empty list
    assert getattr(raci_attrs, CM_ATTR_RACI_EXTRA_RENAMED) is None


def _validate_ipr_attributes(cma: CustomMetadata, mandatory: bool = True):
    assert cma
    license = getattr(cma, CM_ATTR_IPR_LICENSE_RENAMED)
    v = getattr(cma, CM_ATTR_IPR_VERSION_RENAMED)
    m = getattr(cma, CM_ATTR_IPR_MANDATORY_RENAMED)
    d = getattr(cma, CM_ATTR_IPR_DATE_RENAMED)
    u = getattr(cma, CM_ATTR_IPR_URL_RENAMED)
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


def _validate_ipr_empty(ipr_attrs: CustomMetadata):
    assert hasattr(ipr_attrs, CM_ATTR_IPR_LICENSE_RENAMED)
    assert hasattr(ipr_attrs, CM_ATTR_IPR_VERSION_RENAMED)
    assert hasattr(ipr_attrs, CM_ATTR_IPR_MANDATORY_RENAMED)
    assert hasattr(ipr_attrs, CM_ATTR_IPR_DATE_RENAMED)
    assert hasattr(ipr_attrs, CM_ATTR_IPR_URL_RENAMED)
    assert getattr(ipr_attrs, CM_ATTR_IPR_LICENSE_RENAMED) is None
    assert getattr(ipr_attrs, CM_ATTR_IPR_VERSION_RENAMED) is None
    assert getattr(ipr_attrs, CM_ATTR_IPR_MANDATORY_RENAMED) is None
    assert getattr(ipr_attrs, CM_ATTR_IPR_DATE_RENAMED) is None
    assert getattr(ipr_attrs, CM_ATTR_IPR_URL_RENAMED) is None


def _validate_dq_attributes(cma: CustomMetadata):
    assert cma
    c = getattr(cma, CM_ATTR_QUALITY_COUNT_RENAMED)
    s = getattr(cma, CM_ATTR_QUALITY_SQL_RENAMED)
    t = getattr(cma, CM_ATTR_QUALITY_TYPE_RENAMED)
    assert c
    assert c == 42
    assert s
    assert s == "SELECT * from SOMEWHERE;"
    assert t
    assert t == "Completeness"


def _validate_dq_empty(dq_attrs: CustomMetadata):
    assert hasattr(dq_attrs, CM_ATTR_QUALITY_COUNT_RENAMED)
    assert hasattr(dq_attrs, CM_ATTR_QUALITY_SQL_RENAMED)
    assert hasattr(dq_attrs, CM_ATTR_QUALITY_TYPE_RENAMED)
    assert getattr(dq_attrs, CM_ATTR_QUALITY_COUNT_RENAMED) is None
    assert getattr(dq_attrs, CM_ATTR_QUALITY_SQL_RENAMED) is None
    assert getattr(dq_attrs, CM_ATTR_QUALITY_TYPE_RENAMED) is None


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
    assert "Database" in str(one.options.custom_applicable_entity_types)
    assert not one.is_archived()
    assert one.options.multi_value_select
    assert one.options.custom_type == AtlanCustomAttributePrimitiveType.USERS.value
    one = attributes[1]
    assert one.display_name == CM_ATTR_RACI_ACCOUNTABLE
    assert one.name != CM_ATTR_RACI_ACCOUNTABLE
    assert one.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert one.options
    assert "Table" in str(one.options.custom_applicable_entity_types)
    assert not one.is_archived()
    assert not one.options.multi_value_select
    assert one.options.custom_type == AtlanCustomAttributePrimitiveType.USERS.value
    one = attributes[2]
    assert one.display_name == CM_ATTR_RACI_CONSULTED
    assert one.name != CM_ATTR_RACI_CONSULTED
    assert one.type_name == f"array<{AtlanCustomAttributePrimitiveType.STRING.value}>"
    assert one.options
    assert "Column" in str(one.options.custom_applicable_entity_types)
    assert not one.is_archived()
    assert one.options.multi_value_select
    assert one.options.custom_type == AtlanCustomAttributePrimitiveType.GROUPS.value
    one = attributes[3]
    assert one.display_name == CM_ATTR_RACI_INFORMED
    assert not one.name == CM_ATTR_RACI_INFORMED
    assert one.type_name == f"array<{AtlanCustomAttributePrimitiveType.STRING.value}>"
    assert one.options
    assert "MaterialisedView" in str(one.options.custom_applicable_entity_types)
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
        assert "AtlasGlossaryTerm" in str(one.options.custom_applicable_entity_types)
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
        cm_attribute=CM_ATTR_QUALITY_COUNT_RENAMED,
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
    response = client.upsert(badge)
    assert (badges := response.assets_created(asset_type=Badge))
    assert len(badges) == 1
    client.purge_entity_by_guid(badges[0].guid)
