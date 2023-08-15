# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Optional

from pyatlan.client.atlan import AtlanClient


class UserCache:
    """
    Lazily-loaded cache for translating Atlan-internal users into their various IDs.
    """

    map_id_to_name: dict[str, str] = dict()
    map_name_to_id: dict[str, str] = dict()
    map_email_to_id: dict[str, str] = dict()

    @classmethod
    def _refresh_cache(cls) -> None:
        client = AtlanClient.get_default_client()
        if client is None:
            client = AtlanClient()
        users = client.get_all_users()
        if users is not None:
            cls.map_id_to_name = {}
            cls.map_name_to_id = {}
            cls.map_email_to_id = {}
            for user in users:
                user_id = str(user.id)
                username = str(user.username)
                user_email = str(user.email)
                cls.map_id_to_name[user_id] = username
                cls.map_name_to_id[username] = user_id
                cls.map_email_to_id[user_email] = user_id

    @classmethod
    def get_id_for_name(cls, name: str) -> Optional[str]:
        """
        Translate the provided human-readable username to its GUID.

        :param name: human-readable name of the user
        :returns: unique identifier (GUID) of the user
        """
        if user_id := cls.map_name_to_id.get(name):
            return user_id
        cls._refresh_cache()
        return cls.map_name_to_id.get(name)

    @classmethod
    def get_id_for_email(cls, email: str) -> Optional[str]:
        """
        Translate the provided email to its GUID.

        :param email: email address of the user
        :returns: unique identifier (GUID) of the user
        """
        if user_id := cls.map_email_to_id.get(email):
            return user_id
        cls._refresh_cache()
        return cls.map_email_to_id.get(email)

    @classmethod
    def get_name_for_id(cls, idstr: str) -> Optional[str]:
        """
        Translate the provided user GUID to the human-readable username.

        :param idstr: unique identifier (GUID) of the user
        :returns: username of the user
        """
        if username := cls.map_id_to_name.get(idstr):
            return username
        cls._refresh_cache()
        return cls.map_id_to_name.get(idstr)
