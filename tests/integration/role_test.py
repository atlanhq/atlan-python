# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from pyatlan.cache.role_cache import RoleCache


def test_retrieve_admin():
    admin_role_guid = RoleCache.get_id_for_name("$admin")
    print(admin_role_guid)
    assert admin_role_guid


def test_retrieve_guest():
    guest_role_guid = RoleCache.get_id_for_name("$guest")
    print(guest_role_guid)
    assert guest_role_guid


def test_retrieve_member():
    member_role_guid = RoleCache.get_id_for_name("$member")
    print(member_role_guid)
    assert member_role_guid
