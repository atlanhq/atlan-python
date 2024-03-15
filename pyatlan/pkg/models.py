# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import json
import logging
import textwrap
from enum import Enum
from importlib import resources
from pathlib import Path
from typing import Dict, List, Literal, Optional, Protocol

from jinja2 import Environment, PackageLoader
from pydantic.v1 import (
    BaseModel,
    Extra,
    Field,
    PrivateAttr,
    StrictStr,
    validate_arguments,
)

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.pkg.ui import UIConfig

LOGGER = logging.getLogger(__name__)

VERSION = resources.read_text("pyatlan", "version.txt").strip()


class RuntimeConfig(Protocol):
    """Classes the provide runtime configuration will have these properties"""

    user_id: Optional[str]
    """user through whom to impersonate any activities"""
    agent: Optional[str]
    """type of agent being used (for example, workflow)"""
    agent_id: Optional[str]
    """unique ID of the agent"""
    agent_pkg: Optional[str]
    """unique name of the package that runs the agent"""
    agent_wfl: Optional[str]
    """unique instance of the run of the package"""


class PackageConfig(BaseModel):
    labels: Dict[StrictStr, StrictStr]
    annotations: Dict[StrictStr, StrictStr]


class _PackageDefinition(BaseModel):
    name: str
    version: str
    description: str
    keywords: List[str]
    homepage: str
    main: str
    scripts: Dict[str, str]
    author: Dict[str, str]
    repository: Dict[str, str]
    license: str
    bugs: Dict[str, str]
    config: PackageConfig


class PackageDefinition(BaseModel):
    package_id: str
    package_name: str
    description: str
    icon_url: str
    docs_url: str
    keywords: List[str] = Field(default_factory=list)
    scripts: Dict[str, str] = Field(default_factory=dict)
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
            self.connector_type.category.value if self.connector_type else "utility"
        )
        self._package_definition = _PackageDefinition(
            name=self.package_id,
            version=VERSION,
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
    """
    Single class through which you can define a custom package.

    :ivar package_id str: unique identifier for the package, including its namespace
    :ivar package_name str: display name for the package, as it should be shown in the UI
    :ivar description str: description for the package, as it should be shown in the UI
    :ivar icon_url str: link to an icon to use for the package, as it should be shown in the UI
    :ivar docs_url str: link to an online document describing the package
    :ivar ui_config UIConfig: configuration for the UI of the custom package
    :ivar keywords List[str]: (optional) list of any keyword labels to apply to the package
    :ivar container_image str: container image to run the logic of the custom package
    :ivar container_image_pull_policy PullPolicy: (optional) override the default IfNotPresent policy
    :ivar container_command List[str]: the full command to run in the container image, as a list rather than spaced
    (must be provided if you have not specified the class above)
    :ivar allow_schedule bool: (optional) whether to allow the package to be scheduled (default, true) or only run
    immediately (false)
    :ivar certified  bool: (optional) whether the package should be listed as certified (default, true) or not (false)
    :ivar preview bool:(optional) whether the package should be labeled as an early preview in the UI (true)
    or not (default, false)
    :ivar connector_type Optional[AtlanConnectorType]: (optional) if the package needs to configure a connector,
    specify its type here
    :ivar category str:  name of the pill under which the package should be categorized in the marketplace in the UI
    :ivar outputs Dict[str,str]: (optional) any outputs that the custom package logic is expected to produce
    """

    package_id: str
    package_name: str
    description: str
    icon_url: str
    docs_url: str
    ui_config: UIConfig
    keywords: List[str] = Field(default_factory=list)
    container_image: str
    container_image_pull_policy: PullPolicy = PullPolicy.IF_NOT_PRESENT
    container_command: List[str]
    allow_schedule: bool = True
    certified: bool = True
    preview: bool = False
    connector_type: Optional[AtlanConnectorType] = None
    category: str = "custom"
    outputs: Dict[str, str] = Field(default_factory=dict)
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

    class Config:
        extra = Extra.forbid


class PackageWriter(BaseModel):
    """
    The class that will be used to create the custom package or python module files
    """

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
        self._env.globals.update({"isinstanceof": isinstance})

    def create_package(self):
        self._root_dir.mkdir(parents=True, exist_ok=True)
        with (self._root_dir / "index.js").open("w") as index:
            index.write(CustomPackage.indexJS())
        with (self._root_dir / "package.json").open("w") as package:
            package.write(self.pkg.packageJSON)
        self.create_templates()
        self.create_configmaps()

    def create_config(self):
        self.create_config_class()

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

    def create_config_class(self):
        template = self._env.get_template("package_config.jinja2")
        content = template.render({"pkg": self.pkg})
        file_name = f'{self.pkg.package_id[5:].replace("-","_")}_cfg.py'

        with (self.path / file_name).open("w") as script:
            script.write(content)


@validate_arguments()
def generate(pkg: CustomPackage, path: Path, operation: Literal["package", "config"]):
    """
    Generate either the files needed to define the custom package or a java module containing the RuntimeConfig class
    that can be used to provide runtime data from the custom package user interface.

    :param pkg: the custom package that will be used as the source of information for the file generation
    :param path: the path where the files should be created
    :param operation: a string indicating which operation to perform either 'package' to generate the custom package
    files or 'config' to generate the python module
    """
    writer = PackageWriter(pkg=pkg, path=path)
    if operation == "package":
        writer.create_package()
    else:
        writer.create_config()


class ConnectorAndConnection(BaseModel):
    source: AtlanConnectorType
    connections: List[str]
