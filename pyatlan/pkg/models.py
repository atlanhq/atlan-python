# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import json
import logging
import textwrap
from enum import Enum
from pathlib import Path
from typing import Literal, Optional

from jinja2 import Environment, PackageLoader
from pydantic import BaseModel, Field, PrivateAttr, StrictStr, validate_arguments

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.pkg.ui import UIConfig

LOGGER = logging.getLogger(__name__)


class PackageConfig(BaseModel):
    labels: dict[StrictStr, StrictStr]
    annotations: dict[StrictStr, StrictStr]


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


class NamePathS3Tuple:
    name: str
    path: str
    s3: dict[str, str]

    def __init__(self, input_name: str):
        self.name = f"{input_name}_s3"
        self.path = (
            f"/tmp/{input_name}/{{{{inputs.parameters.{input_name}}}}}"  # noqa: S108
        )
        self.s3 = {"key": f"{{{{inputs.parameters.{input_name}}}}}"}


class WorkflowInputs:
    parameters: list[tuple[str, str]]
    artifacts: list[NamePathS3Tuple]

    @validate_arguments()
    def __init__(self, config: UIConfig, pkg_name: str):
        self.parameters = []
        self.artifacts = []
        for _key, value in config.properties.items():
            value.ui


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


class PackageWriter(BaseModel):
    path: Path
    pkg: CustomPackage
    _root_dir: Path = PrivateAttr()
    _config_maps_dir: Path = PrivateAttr()
    _templates_dir: Path = PrivateAttr()
    _env: Environment = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._root_dir = self.path / self.pkg.name
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
        self.create_templates()
        self.create_configmaps()

    def create_templates(self):
        self._templates_dir.mkdir(parents=True, exist_ok=True)
        template = self._env.get_template("default_template.jinja2")
        content = template.render({"pkg": self.pkg})
        with (self._templates_dir / "default.yaml").open("w") as script:
            script.write(content)

    def create_configmaps(self):
        self._config_maps_dir.mkdir(parents=True, exist_ok=True)
        template = self._env.get_template("default_configmap.jinja2")
        content = template.render({"pkg": self.pkg})
        with (self._config_maps_dir / "default.yaml").open("w") as script:
            script.write(content)


@validate_arguments()
def generate(pkg: CustomPackage, path: Path, operation: Literal["package", "config"]):
    writer = PackageWriter(pkg=pkg, path=path)
    if operation == "package":
        writer.create_package()
    else:
        writer.create_configmaps()
