# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import time
from typing import List, Generator, Optional

import pytest

from pyatlan.cache.custom_metadata_cache import CustomMetadataCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    Table,
    AtlasGlossaryTerm,
    AtlasGlossary,
)
from pyatlan.model.core import CustomMetadata, to_snake_case
from pyatlan.model.enums import AtlanCustomAttributePrimitiveType, AtlanTypeCategory
from pyatlan.model.search import Term, DSL, Bool, IndexSearchRequest, Exists
from pyatlan.model.typedef import AttributeDef, CustomMetadataDef, EnumDef
from tests.integration.glossary_test import GlossaryTest

PREFIX = "psdk2-"
CM_PREFIX = PREFIX + "CM"
FIXED_USER = "ernest"

CM_RACI = PREFIX + "RACI"
CM_IPR = PREFIX + "IPR"
CM_QUALITY = PREFIX + "DQ"

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
CM_ENUM_DQ_TYPE = PREFIX.replace("-", "_") + "DataQualityType"
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

GROUP_NAME1 = PREFIX + "1"
GROUP_NAME2 = PREFIX + "2"

_removal_epoch: Optional[int]


@pytest.fixture(scope="session")
def client() -> AtlanClient:
    return AtlanClient()


@pytest.fixture(scope="module")
def cm_ipr(client: AtlanClient) -> Generator[CustomMetadataDef, None, None]:
    cm = CustomMetadataDef.create(display_name=CM_IPR)
    cm.attribute_defs = [
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
    cm.options = CustomMetadataDef.Options.with_logo_as_emoji(emoji="⚖️", locked=False)
    response = client.create_typedef(cm)
    assert response
    assert len(response.custom_metadata_defs) == 1
    cm_created = response.custom_metadata_defs[0]
    assert cm_created.category == AtlanTypeCategory.CUSTOM_METADATA
    assert cm_created.name
    assert cm_created.guid
    assert cm_created.name != CM_IPR
    assert cm_created.display_name == CM_IPR
    attributes = cm_created.attribute_defs
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
    assert not one.options.multi_value_select
    one = attributes[3]
    assert one.display_name == CM_ATTR_IPR_DATE
    assert one.name != CM_ATTR_IPR_DATE
    assert one.type_name == AtlanCustomAttributePrimitiveType.DATE.value
    assert not one.options.multi_value_select
    one = attributes[4]
    assert one.display_name == CM_ATTR_IPR_URL
    assert one.name != CM_ATTR_IPR_URL
    assert one.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert not one.options.multi_value_select
    yield cm_created
    # Purge the custom metadata, after a little wait for eventual consistency
    time.sleep(5)
    client.purge_typedef(cm_created.name)


@pytest.fixture(scope="module")
def cm_raci(client: AtlanClient) -> Generator[CustomMetadataDef, None, None]:
    cm = CustomMetadataDef.create(display_name=CM_RACI)
    cm.attribute_defs = [
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
    cm.options = CustomMetadataDef.Options.with_logo_as_emoji(emoji="👪")
    response = client.create_typedef(cm)
    assert response
    assert len(response.custom_metadata_defs) == 1
    cm_created = response.custom_metadata_defs[0]
    assert cm_created.category == AtlanTypeCategory.CUSTOM_METADATA
    assert cm_created.name
    assert cm_created.guid
    assert cm_created.name != CM_RACI
    assert cm_created.display_name == CM_RACI
    attributes = cm_created.attribute_defs
    assert attributes
    assert len(attributes) == 5
    one = attributes[0]
    assert one
    assert one.display_name == CM_ATTR_RACI_RESPONSIBLE
    assert one.name
    assert one.name != CM_ATTR_RACI_RESPONSIBLE
    assert (
        one.type_name == "array<" + AtlanCustomAttributePrimitiveType.STRING.value + ">"
    )
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
    assert (
        one.type_name == "array<" + AtlanCustomAttributePrimitiveType.STRING.value + ">"
    )
    assert one.options.multi_value_select
    one = attributes[3]
    assert one.display_name == CM_ATTR_RACI_INFORMED
    assert one.name != CM_ATTR_RACI_INFORMED
    assert (
        one.type_name == "array<" + AtlanCustomAttributePrimitiveType.STRING.value + ">"
    )
    assert one.options.multi_value_select
    one = attributes[4]
    assert one.display_name == CM_ATTR_RACI_EXTRA
    assert one.name != CM_ATTR_RACI_EXTRA
    assert one.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert not one.options.multi_value_select
    yield cm_created
    # Cleanup after completion, after a little wait for eventual consistency
    time.sleep(5)
    client.purge_typedef(cm_created.name)


@pytest.fixture(scope="module")
def cm_enum(client: AtlanClient) -> Generator[EnumDef, None, None]:
    enum_def = EnumDef.create(name=CM_ENUM_DQ_TYPE, values=DQ_TYPE_LIST)
    response = client.create_typedef(enum_def)
    assert response
    assert len(response.enum_defs) == 1
    enum_created = response.enum_defs[0]
    assert enum_created.category == AtlanTypeCategory.ENUM
    assert enum_created.name == CM_ENUM_DQ_TYPE
    assert enum_created.guid
    assert enum_created.element_defs
    assert len(enum_created.element_defs) == len(DQ_TYPE_LIST)
    yield enum_created
    # Cleanup after a little wait for eventual consistency
    time.sleep(5)
    client.purge_typedef(CM_ENUM_DQ_TYPE)


@pytest.fixture(scope="module")
def cm_dq(
    client: AtlanClient, cm_enum: EnumDef
) -> Generator[CustomMetadataDef, None, None]:
    cm = CustomMetadataDef.create(display_name=CM_QUALITY)
    cm.attribute_defs = [
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
    cm.options = CustomMetadataDef.Options.with_logo_from_url(
        url="https://github.com/great-expectations/great_expectations/raw/develop/docs/docusaurus/static/img/gx-mark-160.png",
        locked=False,
    )
    response = client.create_typedef(cm)
    assert response
    assert len(response.custom_metadata_defs) == 1
    cm_created = response.custom_metadata_defs[0]
    assert cm_created.category == AtlanTypeCategory.CUSTOM_METADATA
    assert cm_created.name
    assert cm_created.guid
    assert cm_created.name != CM_QUALITY
    assert cm_created.display_name == CM_QUALITY
    attributes = cm_created.attribute_defs
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
    assert not one.options.multi_value_select
    assert one.options.primitive_type == AtlanCustomAttributePrimitiveType.OPTIONS.value
    yield cm_created
    # Cleanup after a little wait for eventual consistency
    time.sleep(5)
    client.purge_typedef(cm_created.name)


@pytest.fixture(scope="module")
def glossary(client: AtlanClient) -> Generator[AtlasGlossary, None, None]:
    g = GlossaryTest.create_glossary(client, CM_PREFIX)
    assert g
    assert g.guid
    assert g.name == CM_PREFIX
    yield g
    client.purge_entity_by_guid(g.guid)


@pytest.fixture(scope="module")
def term(
    client: AtlanClient, glossary: AtlasGlossary
) -> Generator[AtlasGlossaryTerm, None, None]:
    t = GlossaryTest.create_term(client, name=CM_PREFIX, glossary_guid=glossary.guid)
    assert t
    assert t.guid
    assert t.name == CM_PREFIX
    yield t
    client.purge_entity_by_guid(t.guid)


# TODO: create the groups, once they're modeled in the SDK...
# @pytest.fixure
# def groups(client: AtlanClient) -> Generator[List[], None, None]:


@pytest.mark.usefixtures("cm_raci")
def test_add_term_cm_raci(client: AtlanClient, term: AtlasGlossaryTerm):
    raci_attrs = term.get_custom_metadata(CM_RACI)
    _validate_raci_empty(raci_attrs)
    setattr(raci_attrs, CM_ATTR_RACI_RESPONSIBLE_RENAMED, [FIXED_USER])
    setattr(raci_attrs, CM_ATTR_RACI_ACCOUNTABLE_RENAMED, FIXED_USER)
    # TODO: set Consulted and Informed once groups are available
    client.update_custom_metadata_attributes(term.guid, raci_attrs)
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_raci_attributes(t.get_custom_metadata(name=CM_RACI))


@pytest.mark.usefixtures("cm_ipr")
def test_add_term_cm_ipr(client: AtlanClient, term: AtlasGlossaryTerm):
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


@pytest.mark.usefixtures("cm_dq")
def test_add_term_cm_dq(client: AtlanClient, term: AtlasGlossaryTerm):
    dq_attrs = term.get_custom_metadata(CM_QUALITY)
    _validate_dq_empty(dq_attrs)
    setattr(dq_attrs, CM_ATTR_QUALITY_COUNT_RENAMED, 42)
    setattr(dq_attrs, CM_ATTR_QUALITY_SQL_RENAMED, "SELECT * from SOMEWHERE;")
    setattr(dq_attrs, CM_ATTR_QUALITY_TYPE_RENAMED, "Completeness")
    client.update_custom_metadata_attributes(term.guid, dq_attrs)
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))


@pytest.mark.usefixtures("cm_ipr")
@pytest.mark.order(after="test_add_term_cm_dq")
def test_update_term_cm_ipr(client: AtlanClient, term: AtlasGlossaryTerm):
    ipr = term.get_custom_metadata(CM_IPR)
    # Note: MUST access the getter / setter, not the underlying store
    setattr(ipr, CM_ATTR_IPR_MANDATORY_RENAMED, False)
    client.update_custom_metadata_attributes(term.guid, ipr)
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_ipr_attributes(t.get_custom_metadata(name=CM_IPR), mandatory=False)
    _validate_raci_attributes(t.get_custom_metadata(name=CM_RACI))
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))


@pytest.mark.usefixtures("cm_raci")
@pytest.mark.order(after="test_update_term_cm_ipr")
def test_replace_term_cm_raci(client: AtlanClient, term: AtlasGlossaryTerm):
    raci = term.get_custom_metadata(CM_RACI)
    # Note: MUST access the getter / setter, not the underlying store
    setattr(raci, CM_ATTR_RACI_RESPONSIBLE_RENAMED, None)
    setattr(raci, CM_ATTR_RACI_ACCOUNTABLE_RENAMED, FIXED_USER)
    # TODO: replace consulted or informed (not yet defined, waiting on groups support)
    client.replace_custom_metadata(term.guid, raci)
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_raci_attributes_replacement(t.get_custom_metadata(name=CM_RACI))
    _validate_ipr_attributes(t.get_custom_metadata(name=CM_IPR), mandatory=False)
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))


@pytest.mark.usefixtures("cm_ipr")
@pytest.mark.order(after="test_replace_term_cm_raci")
def test_replace_term_cm_ipr(client: AtlanClient, term: AtlasGlossaryTerm):
    client.replace_custom_metadata(term.guid, term.get_custom_metadata(CM_IPR))
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_raci_attributes_replacement(t.get_custom_metadata(name=CM_RACI))
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))
    _validate_ipr_empty(t.get_custom_metadata(name=CM_IPR))


@pytest.mark.usefixtures("cm_raci")
@pytest.mark.order(after="test_replace_term_cm_ipr")
def test_search_by_any_accountable(
    client: AtlanClient, glossary: AtlasGlossary, term: AtlasGlossaryTerm
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


@pytest.mark.usefixtures("cm_raci")
@pytest.mark.order(after="test_replace_term_cm_ipr")
def test_search_by_specific_accountable(
    client: AtlanClient, glossary: AtlasGlossary, term: AtlasGlossaryTerm
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
        return t


@pytest.mark.usefixtures("cm_raci")
@pytest.mark.order(
    after=["test_search_by_any_accountable", "test_search_by_specific_accountable"]
)
def test_remove_term_cm_raci(client: AtlanClient, term: AtlasGlossaryTerm):
    client.remove_custom_metadata(term.guid, cm_name=CM_RACI)
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))
    _validate_ipr_empty(t.get_custom_metadata(name=CM_IPR))
    _validate_raci_empty(t.get_custom_metadata(name=CM_RACI))


@pytest.mark.usefixtures("cm_ipr")
@pytest.mark.order(after="test_remove_term_cm_raci")
def test_remove_term_cm_ipr(client: AtlanClient, term: AtlasGlossaryTerm):
    client.remove_custom_metadata(term.guid, cm_name=CM_IPR)
    t = client.retrieve_minimal(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert t
    _validate_dq_attributes(t.get_custom_metadata(name=CM_QUALITY))
    _validate_ipr_empty(t.get_custom_metadata(name=CM_IPR))
    _validate_raci_empty(t.get_custom_metadata(name=CM_RACI))


@pytest.mark.usefixtures("cm_raci")
@pytest.mark.order(after="test_remove_term_cm_raci")
def test_remove_attribute(client: AtlanClient):
    global _removal_epoch
    existing = CustomMetadataCache.get_custom_metadata_def(name=CM_RACI)
    existing_attrs = existing.attribute_defs
    updated_attrs = []
    for existing_attr in existing_attrs:
        to_keep = existing_attr
        if existing_attr.display_name == CM_ATTR_RACI_EXTRA:
            to_keep = existing_attr.archive(by="test-automation")
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
    assert archived.display_name == CM_ATTR_RACI_EXTRA + "-archived-" + str(
        _removal_epoch
    )
    assert archived.name != CM_ATTR_RACI_EXTRA
    assert archived.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert not archived.options.multi_value_select
    assert archived.is_archived()


@pytest.mark.usefixtures("cm_raci")
@pytest.mark.order(after="test_remove_attribute")
def test_retrieve_structures(client: AtlanClient):
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
    assert extra.display_name == CM_ATTR_RACI_EXTRA + "-archived-" + str(_removal_epoch)
    assert extra.name != CM_ATTR_RACI_EXTRA
    assert extra.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert "Database" in extra.options.custom_applicable_entity_types
    assert not extra.options.multi_value_select
    assert extra.is_archived()


@pytest.mark.usefixtures("cm_raci")
@pytest.mark.order(after="test_retrieve_structures")
def test_recreate_attribute(client: AtlanClient):
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


@pytest.mark.usefixtures("cm_raci")
@pytest.mark.order(after="test_recreate_attribute")
def test_retrieve_structure_without_archived(client: AtlanClient):
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


@pytest.mark.usefixtures("cm_raci")
@pytest.mark.order(after="test_recreate_attribute")
def test_retrieve_structure_with_archived(client: AtlanClient):
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


@pytest.mark.usefixtures("cm_raci", "cm_ipr", "cm_dq")
@pytest.mark.order(after="test_recreate_attribute")
def test_update_replacing_cm(
    client: AtlanClient, term: AtlasGlossaryTerm, glossary: AtlasGlossary
):
    raci = term.get_custom_metadata(CM_RACI)
    setattr(raci, CM_ATTR_RACI_RESPONSIBLE_RENAMED, [FIXED_USER])
    setattr(raci, CM_ATTR_RACI_ACCOUNTABLE_RENAMED, FIXED_USER)
    # TODO: set consulted and informed once groups are available
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
    _validate_raci_attributes(raci)
    assert getattr(raci, CM_ATTR_RACI_EXTRA_RENAMED) == "something extra..."
    _validate_ipr_empty(x.get_custom_metadata(CM_IPR))
    _validate_dq_empty(x.get_custom_metadata(CM_QUALITY))


# TODO: test entity audit retrieval and parsing, once available


def test_get_custom_metadata_when_name_is_invalid_then_raises_value_error():
    with pytest.raises(
        ValueError, match="No custom metadata with the name: Bogs exist"
    ):
        CustomMetadataCache.get_custom_metadata(name="Bogs", asset_type=Table)


def _validate_raci_attributes(cma: CustomMetadata):
    assert cma
    # Note: MUST access the getter / setter, not the underlying store
    responsible = getattr(cma, CM_ATTR_RACI_RESPONSIBLE_RENAMED)
    accountable = getattr(cma, CM_ATTR_RACI_ACCOUNTABLE_RENAMED)
    assert responsible
    assert len(responsible) == 1
    assert FIXED_USER in responsible
    assert accountable
    assert accountable == FIXED_USER
    # TODO: validate consulted and informed, once groups are included


def _validate_raci_attributes_replacement(cma: CustomMetadata):
    assert cma
    # Note: MUST access the getter / setter, not the underlying store
    responsible = getattr(cma, CM_ATTR_RACI_RESPONSIBLE_RENAMED)
    accountable = getattr(cma, CM_ATTR_RACI_ACCOUNTABLE_RENAMED)
    assert not responsible
    assert accountable
    assert accountable == FIXED_USER
    # TODO: validate consulted and informed, once groups are included


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
    l = getattr(cma, CM_ATTR_IPR_LICENSE_RENAMED)
    v = getattr(cma, CM_ATTR_IPR_VERSION_RENAMED)
    m = getattr(cma, CM_ATTR_IPR_MANDATORY_RENAMED)
    d = getattr(cma, CM_ATTR_IPR_DATE_RENAMED)
    u = getattr(cma, CM_ATTR_IPR_URL_RENAMED)
    assert l
    assert l == "CC BY"
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
    assert attributes
    assert len(attributes) == total_expected
    one = attributes[0]
    assert one.display_name == CM_ATTR_RACI_RESPONSIBLE
    assert one.name != CM_ATTR_RACI_RESPONSIBLE
    assert (
        one.type_name == "array<" + AtlanCustomAttributePrimitiveType.STRING.value + ">"
    )
    assert "Database" in str(one.options.custom_applicable_entity_types)
    assert not one.is_archived()
    assert one.options.multi_value_select
    assert one.options.custom_type == AtlanCustomAttributePrimitiveType.USERS.value
    one = attributes[1]
    assert one.display_name == CM_ATTR_RACI_ACCOUNTABLE
    assert one.name != CM_ATTR_RACI_ACCOUNTABLE
    assert one.type_name == AtlanCustomAttributePrimitiveType.STRING.value
    assert "Table" in str(one.options.custom_applicable_entity_types)
    assert not one.is_archived()
    assert not one.options.multi_value_select
    assert one.options.custom_type == AtlanCustomAttributePrimitiveType.USERS.value
    one = attributes[2]
    assert one.display_name == CM_ATTR_RACI_CONSULTED
    assert one.name != CM_ATTR_RACI_CONSULTED
    assert (
        one.type_name == "array<" + AtlanCustomAttributePrimitiveType.STRING.value + ">"
    )
    assert "Column" in str(one.options.custom_applicable_entity_types)
    assert not one.is_archived()
    assert one.options.multi_value_select
    assert one.options.custom_type == AtlanCustomAttributePrimitiveType.GROUPS.value
    one = attributes[3]
    assert one.display_name == CM_ATTR_RACI_INFORMED
    assert not one.name == CM_ATTR_RACI_INFORMED
    assert (
        one.type_name == "array<" + AtlanCustomAttributePrimitiveType.STRING.value + ">"
    )
    assert "MaterialisedView" in str(one.options.custom_applicable_entity_types)
    assert not one.is_archived()
    assert one.options.multi_value_select
    assert one.options.custom_type == AtlanCustomAttributePrimitiveType.GROUPS.value
    if total_expected > 5:
        # If we're expecting more than 5, then the penultimate must be an archived CM_ATTR_EXTRA
        one = attributes[4]
        assert one.display_name == CM_ATTR_RACI_EXTRA + "-archived-" + str(
            _removal_epoch
        )
        assert one.name != CM_ATTR_RACI_EXTRA
        assert one.type_name == AtlanCustomAttributePrimitiveType.STRING.value
        assert "AtlasGlossaryTerm" in str(one.options.custom_applicable_entity_types)
        assert not one.options.multi_value_select
        assert one.is_archived()
    if total_expected > 4:
        return attributes[total_expected - 1]
    return None
