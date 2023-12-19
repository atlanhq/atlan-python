# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import json
import logging
import textwrap
from enum import Enum
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field, PrivateAttr

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.pkg.ui import UIConfig

LOGGER = logging.getLogger(__name__)


class PackageConfig(BaseModel):
    labels: dict[str, str]
    annotations: dict[str, str]


class _PackageDefinition(BaseModel):
    name: str
    version: str
    description: str
    keywords: list[str]
    homepage: str
    main: str
    scripts: dict[str, str]
    author: dict[str, str]
    repository: dict[str, str]
    license: str
    bugs: dict[str, str]
    config: PackageConfig


class ConfigMap(BaseModel):
    api_version: Literal["v1"] = "v1"
    kind: Literal["ConfigMap"] = "ConfigMap"
    metadata: dict[str, str] = Field(default_factory=dict)
    data: dict[str, str] = Field(default_factory=dict)

    def __init__(self, name: str, **data):
        super().__init__(**data)
        self.metadata = {"name": name}


class PackageDefinition(BaseModel):
    package_id: str
    package_name: str
    description: str
    icon_url: str
    docs_url: str
    keywords: list[str] = Field(default_factory=list)
    scripts: dict[str, str] = Field(default_factory=dict)
    allow_schedule: bool = True
    certified: bool = True
    preview: bool = False
    connector_type: Optional[AtlanConnectorType] = None
    category: str = "custom"
    _package_definition: _PackageDefinition = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        source = self.connector_type.value if self.connector_type else "atlan"
        source_category = (
            self.connector_type.value if self.connector_type else "utility"
        )
        self._package_definition = _PackageDefinition(
            name=self.package_id,
            version="1.6.5",
            description=self.description,
            keywords=self.keywords,
            homepage=f"https://packages.atlan.com/-/web/detail/{self.package_id}",
            main="index.js",
            scripts=self.scripts,
            author={
                "name": "Atlan CSA",
                "email": "csa@atlan.com",
                "url": "https://atlan.com",
            },
            repository={
                "type": "git",
                "url": "https://github.com/atlanhq/marketplace-packages.git",
            },
            license="MIT",
            bugs={
                "url": "https://atlan.com",
                "email": "support@atlan.com",
            },
            config=PackageConfig(
                labels={
                    "orchestration.atlan.com/verified": "true",
                    "orchestration.atlan.com/type": self.category,
                    "orchestration.atlan.com/source": source,
                    "orchestration.atlan.com/sourceCategory": source_category,
                    "orchestration.atlan.com/certified": str(self.certified).lower(),
                    "orchestration.atlan.com/preview": str(self.preview).lower(),
                },
                annotations={
                    "orchestration.atlan.com/name": self.package_name,
                    "orchestration.atlan.com/allowSchedule": str(
                        self.allow_schedule
                    ).lower(),
                    "orchestration.atlan.com/dependentPackage": "",
                    "orchestration.atlan.com/emoji": "🚀",
                    "orchestration.atlan.com/categories": ",".join(self.keywords),
                    "orchestration.atlan.com/icon": self.icon_url,
                    "orchestration.atlan.com/logo": self.icon_url,
                    "orchestration.atlan.com/docsUrl": self.docs_url,
                },
            ),
        )

    @property
    def packageJSON(self):
        json_object = json.loads(self._package_definition.json())
        return json.dumps(json_object, indent=2, ensure_ascii=False)


class PullPolicy(str, Enum):
    ALWAYS = "Always"
    IF_NOT_PRESENT = "IfNotPresent"


class CustomPackage(BaseModel):
    package_id: str
    package_name: str
    description: str
    icon_url: str
    docs_url: str
    ui_config: UIConfig
    keywords: list[str] = Field(default_factory=list)
    container_image: str
    container_image_pull_policy: PullPolicy = PullPolicy.IF_NOT_PRESENT
    container_command: list[str]
    allow_schedule: bool = True
    certified: bool = True
    preview: bool = False
    connector_type: Optional[AtlanConnectorType] = None
    category: str = "custom"
    _pkg: PackageDefinition = PrivateAttr()
    _name: str = PrivateAttr()

    def _init_private_attributes(self) -> None:
        super()._init_private_attributes()
        self._pkg = PackageDefinition(
            package_id=self.package_id,
            package_name=self.package_name,
            description=self.description,
            icon_url=self.icon_url,
            docs_url=self.docs_url,
            keywords=self.keywords,
            allow_schedule=self.allow_schedule,
            certified=self.certified,
            preview=self.preview,
            connector_type=self.connector_type,
            category=self.category,
        )
        self._name = self.package_id.replace("@", "").replace("/", "-")

    @property
    def name(self) -> str:
        return self._name

    @property
    def packageJSON(self) -> str:
        return self._pkg.packageJSON

    @staticmethod
    def indexJS() -> str:
        return textwrap.dedent(
            """\
        function dummy() {
            console.log("don't call this.")
        }
        module.exports = dummy;
        """
        )

    @staticmethod
    def create_package(pkg: "CustomPackage", args: list[str]):
        path = args[0]
        root_dir = Path(path) / pkg.name
        root_dir.mkdir(parents=True, exist_ok=True)
        with (root_dir / "index.js").open("w") as index:
            index.write(CustomPackage.indexJS())
        with (root_dir / "package.json").open("w") as package:
            package.write(pkg.packageJSON)
        config_maps_dir = root_dir / "configmaps"
        config_maps_dir.mkdir(parents=True, exist_ok=True)
        templates_dir = root_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)