# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from pyatlan.cache.role_cache import RoleCache

import logging

LOGGER = logging.getLogger(__name__)


def test_retrieve_admin():
    admin_role_guid = RoleCache.get_id_for_name("$admin")
    assert admin_role_guid
    LOGGER.info(f"Admin role: {admin_role_guid}")


def test_retrieve_guest():
    guest_role_guid = RoleCache.get_id_for_name("$guest")
    assert guest_role_guid
    LOGGER.info(f"Guest role: {guest_role_guid}")


def test_retrieve_member():
    member_role_guid = RoleCache.get_id_for_name("$member")
    assert member_role_guid
    LOGGER.info(f"Member role: {member_role_guid}")
