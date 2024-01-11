# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import logging
import os
from pathlib import Path

from jinja2 import Environment, PackageLoader
from pydantic import BaseModel, PrivateAttr

from pyatlan.client.atlan import AtlanClient
from pyatlan.pkg.models import CustomPackage

LOGGER = logging.getLogger(__name__)


class PackageWriter(BaseModel):
    path: str
    pkg: CustomPackage
    _root_dir: Path = PrivateAttr()
    _config_maps_dir: Path = PrivateAttr()
    _templates_dir: Path = PrivateAttr()
    _env: Environment = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._root_dir = Path(self.path) / self.pkg.name
        self._config_maps_dir = self._root_dir / "configmaps"
        self._templates_dir = self._root_dir / "templates"
        self._env = Environment(  # noqa: S701
            loader=PackageLoader("pyatlan.pkg", "templates")
        )

    def create_package(self):
        self._root_dir.mkdir(parents=True, exist_ok=True)
        with (self._root_dir / "index.js").open("w") as index:
            index.write(CustomPackage.indexJS())
        with (self._root_dir / "index.js").open("w") as index:
            index.write(CustomPackage.indexJS())
        with (self._root_dir / "package.json").open("w") as package:
            package.write(self.pkg.packageJSON)

    def create_templates(self):
        self._templates_dir.mkdir(parents=True, exist_ok=True)
        template = self._env.get_template("default_template.jinja2")
        content = template.render({"pkg": self.pkg})
        with (self._templates_dir / "default.yaml").open("w") as script:
            script.write(content)


def set_client(impersonate_user_id: str) -> AtlanClient:

    base_url = os.environ.get("ATLAN_BASE_URL", "INTERNAL")
    api_token = os.environ.get("ATLAN_API_KEY", "")
    user_id = os.environ.get("ATLAN_USER_ID", impersonate_user_id)
    if api_token:
        LOGGER.info("Using provided API token for authentication.")
        api_key = api_token
    elif user_id:
        LOGGER.info("No API token found, attempting to impersonate user: %s", user_id)
        api_key = AtlanClient(base_url=base_url, api_key="").impersonate.user(
            user_id=user_id
        )
    else:
        LOGGER.info(
            "No API token or impersonation user, attempting short-lived escalation."
        )
        api_key = AtlanClient(base_url=base_url, api_key="").impersonate.escolate()
    return AtlanClient(base_url=base_url, api_key=api_key)
