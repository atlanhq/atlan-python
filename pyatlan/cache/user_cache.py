# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from threading import Lock
from typing import TYPE_CHECKING, Dict, Iterable, Optional

from pyatlan.errors import ErrorCode
from pyatlan.model.constants import SERVICE_ACCOUNT_

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient

lock = Lock()


class UserCache:
    """
    Lazily-loaded cache for translating Atlan-internal users into their various IDs.
    """

    def __init__(self, client: AtlanClient):
        self.client: AtlanClient = client
        self.map_id_to_name: Dict[str, str] = {}
        self.map_name_to_id: Dict[str, str] = {}
        self.map_email_to_id: Dict[str, str] = {}
        self.lock: Lock = Lock()

    def get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided human-readable username to its GUID.

        :param name: human-readable name of the user
        :returns: unique identifier (GUID) of the user
        """
        return self._get_id_for_name(name=name)

    def get_id_for_email(self, email: str) -> Optional[str]:
        """
        Translate the provided email to its GUID.

        :param email: email address of the user
        :returns: unique identifier (GUID) of the user
        """
        return self._get_id_for_email(email=email)

    def get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided user GUID to the human-readable username.

        :param idstr: unique identifier (GUID) of the user
        :returns: username of the user
        """
        return self._get_name_for_id(idstr=idstr)

    def validate_names(self, names: Iterable[str]):
        """
        Validate that the given human-readable usernames are valid. A ValueError will be raised in any are not.

        :param names: a collection of usernames to be checked
        """
        return self._validate_names(names)

    def _refresh_cache(self) -> None:
        with self.lock:
            users = self.client.user.get_all()
            if not users:
                return
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
        # If we are translating an API token,
        # short-circuit any further cache refresh
        if name.startswith(SERVICE_ACCOUNT_):
            token = self.client.token.get_by_id(client_id=name)
            if token and token.guid:
                self.map_name_to_id[name] = token.guid
                return token.guid
            else:
                raise ErrorCode.API_TOKEN_NOT_FOUND_BY_NAME.exception_with_parameters(
                    name
                )
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
        # If the username isn't found, check if it is an API token
        token = self.client.token.get_by_guid(guid=idstr)
        if token and token.client_id:
            return token.username
        else:
            self._refresh_cache()
            return self.map_id_to_name.get(idstr)

    def _validate_names(self, names: Iterable[str]):
        """
        Validate that the given human-readable usernames are valid. A ValueError will be raised in any are not.

        :param names: a collection of usernames to be checked
        """
        for username in names:
            if not self.get_id_for_name(username) and not self.client.token.get_by_id(
                username
            ):
                raise ValueError(
                    f"Provided username {username} was not found in Atlan."
                )
