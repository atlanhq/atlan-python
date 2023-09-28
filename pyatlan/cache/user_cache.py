# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Iterable, Optional

from pyatlan.model.user import UserProvider


class UserCache:
    """
    Lazily-loaded cache for translating Atlan-internal users into their various IDs.
    """

    caches: dict[int, "UserCache"] = {}

    @classmethod
    def get_cache(cls) -> "UserCache":
        from pyatlan.client.atlan import AtlanClient

        client = AtlanClient.get_default_client()
        cache_key = client.cache_key
        if cache_key not in cls.caches:
            cls.caches[cache_key] = UserCache(provider=client)
        return cls.caches[cache_key]

    @classmethod
    def get_id_for_name(cls, name: str) -> Optional[str]:
        """
        Translate the provided human-readable username to its GUID.

        :param name: human-readable name of the user
        :returns: unique identifier (GUID) of the user
        """
        return cls.get_cache()._get_id_for_name(name=name)

    @classmethod
    def get_id_for_email(cls, email: str) -> Optional[str]:
        """
        Translate the provided email to its GUID.

        :param email: email address of the user
        :returns: unique identifier (GUID) of the user
        """
        return cls.get_cache()._get_id_for_email(email=email)

    @classmethod
    def get_name_for_id(cls, idstr: str) -> Optional[str]:
        """
        Translate the provided user GUID to the human-readable username.

        :param idstr: unique identifier (GUID) of the user
        :returns: username of the user
        """
        return cls.get_cache()._get_name_for_id(idstr=idstr)

    @classmethod
    def validate_names(cls, names: Iterable[str]):
        """
        Validate that the given human-readable usernames are valid. A ValueError will be raised in any are not.

        :param names: a collection of usernames to be checked
        """
        return cls.get_cache()._validate_names(names)

    def __init__(self, provider: UserProvider):
        self.provider = provider
        self.map_id_to_name: dict[str, str] = {}
        self.map_name_to_id: dict[str, str] = {}
        self.map_email_to_id: dict[str, str] = {}

    def _refresh_cache(self) -> None:
        users = self.provider.get_all_users()
        if users is not None:
            self.map_id_to_name = {}
            self.map_name_to_id = {}
            self.map_email_to_id = {}
            for user in users:
                user_id = str(user.id)
                username = str(user.username)
                user_email = str(user.email)
                self.map_id_to_name[user_id] = username
                self.map_name_to_id[username] = user_id
                self.map_email_to_id[user_email] = user_id

    def _get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided human-readable username to its GUID.

        :param name: human-readable name of the user
        :returns: unique identifier (GUID) of the user
        """
        if user_id := self.map_name_to_id.get(name):
            return user_id
        self._refresh_cache()
        return self.map_name_to_id.get(name)

    def _get_id_for_email(self, email: str) -> Optional[str]:
        """
        Translate the provided email to its GUID.

        :param email: email address of the user
        :returns: unique identifier (GUID) of the user
        """
        if user_id := self.map_email_to_id.get(email):
            return user_id
        self._refresh_cache()
        return self.map_email_to_id.get(email)

    def _get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided user GUID to the human-readable username.

        :param idstr: unique identifier (GUID) of the user
        :returns: username of the user
        """
        if username := self.map_id_to_name.get(idstr):
            return username
        self._refresh_cache()
        return self.map_id_to_name.get(idstr)

    def _validate_names(self, names: Iterable[str]):
        """
        Validate that the given human-readable usernames are valid. A ValueError will be raised in any are not.

        :param names: a collection of usernames to be checked
        """
        for username in names:
            if not self.get_id_for_name(
                username
            ) and not self.provider.get_api_token_by_id(username):
                raise ValueError(
                    f"Provided username {username} was not found in Atlan."
                )
