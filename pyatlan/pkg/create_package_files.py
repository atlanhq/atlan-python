import re
import sys
from pathlib import Path
from typing import Optional

FILE_NAME = "package_config.py"
OUTPUT_FILE = Path("package_config.py")
CODE = """from pathlib import Path
from pyatlan.pkg.models import CustomPackage, generate, PullPolicy
from pyatlan.pkg.ui import UIConfig, UIRule, UIStep
from pyatlan.pkg.widgets import (
    APITokenSelector,
    BooleanInput,
    ConnectionCreator,
    ConnectionSelector,
    ConnectorTypeSelector,
    Credential,
    DateInput,
    DropDown,
    FileUploader,
    KeygenInput,
    MultipleGroups,
    MultipleUsers,
    NumericInput,
    PasswordInput,
    Radio,
    SingleGroup,
    SingleUser,
    TextInput,
)

PARENT = Path(__file__).parent
TOP = PARENT.parent

def create_package() -> CustomPackage:
    \"\"\"Create the custom package\"\"\"
    return CustomPackage(
        package_id="{package_id}",

        container_image="ghcr.io/atlanhq/{image}",
        container_command=["python", "'-m'", "{package_name}.main"],
        outputs={{
            "debug-logs": "/tmp/debug.log",
        }}
    )

if __name__ == "__main__":
    package = create_package()
    generate(pkg=package, path=TOP / "generated_packages", operation="package")
    generate(pkg=package, path=PARENT, operation="config")
"""

LOGGING_CONF = """[loggers]
keys=root,pyatlan,urllib3

[handlers]
keys=consoleHandler,fileHandler,jsonHandler

[formatters]
keys=simpleFormatter,jsonFormatter

[logger_root]
level=INFO
handlers=consoleHandler,fileHandler

[logger_pyatlan]
level=DEBUG
handlers=fileHandler,jsonHandler
qualname=pyatlan
propagate=0

[logger_urllib3]
level=DEBUG
handlers=fileHandler,jsonHandler
qualname=urllib3
propagate=0

[handler_consoleHandler]
class=StreamHandler
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('/tmp/debug.log',)

[handler_jsonHandler]
class=FileHandler
level=DEBUG
formatter=jsonFormatter
args=('/tmp/pyatlan.json',)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s

[formatter_jsonFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
class=pyatlan.utils.JsonFormatter
"""
REQUIREMENTS = """pyatlan
"""
DOCKER_FILE = """FROM python:3.9-bookworm


RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64
RUN chmod +x /usr/local/bin/dumb-init

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /app

ADD {package_name} /app/{package_name}

ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
"""
MAIN = """import logging
from {package_name}.{package_name}_cfg import RuntimeConfig
from pyatlan.pkg.utils import set_package_ops

LOGGER = logging.getLogger(__name__)

def main():
    \"\"\""Main logic\"\"\"
    runtime_config = RuntimeConfig()
    custom_config = runtime_config.custom_config
    client = set_package_ops(runtime_config)

if __name__ == '__main__':
    main()
"""


def write_file(output_file: Path, data: Optional[str] = None):
    if output_file.exists():
        print(f"{output_file.absolute()} already exists. Leaving unchanged.")
        return
    with output_file.open("w") as output:
        if data:
            output.write(data)


def main(package_name: str):
    output_dir = Path(package_name)
    package_id = f"@csa/{sys.argv[1].replace('_', '-')}"
    output_file = output_dir / FILE_NAME
    output_dir.mkdir(exist_ok=True)
    write_file(Path("requirements.txt"), REQUIREMENTS)
    write_file(Path("Dockerfile"), DOCKER_FILE.format(package_name=package_name))
    write_file((output_dir / "__init__.py"))
    write_file((output_dir / "logging.conf"), LOGGING_CONF)
    write_file(
        output_file,
        CODE.format(
            package_id=package_id,
            package_name=package_name,
            image=f"csa-{package_name.replace('_', '-')}",
        ),
    )
    write_file(Path(output_dir / "main.py"), MAIN.format(package_name=package_name))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify the python package name for the package")
        exit(1)
    if not re.fullmatch(r"\w+", sys.argv[1], re.ASCII):
        print(
            "The package name can only consist of alphanumeric characters and the underscore"
        )

    main(sys.argv[1])
