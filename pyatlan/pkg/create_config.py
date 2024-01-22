import sys
from pathlib import Path

FILE_NAME = "package_config.py"
OUTPUT_FILE = Path("package_config.py")
CODE = """
from pathlib import Path
from pyatlan.pkg.models import CustomPackage, generate, PullPolicy
from pyatlan.pkg.ui import UIConfig, UIRule, UIStep
from pyatlan.pkg.widgets import (
    APITokenSelector,
    BooleanInput,
    ConnectionCreator,
    ConnectionSelector,
    ConnectorTypeSelector,
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

    )

if __name__ == "__main__":
    package = create_package()
    generate(pkg=package, path=TOP / "generated_packages", operation="package")
    generate(pkg=package, path=PARENT, operation="config")
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Please specify where {FILE_NAME} should be created")
        exit(1)
    output_dir = Path(sys.argv[1])
    output_file = output_dir / FILE_NAME

    if output_file.exists():
        answer = input(
            f"{output_file.absolute()} already exists. Do you want to overwrite it? (Y, N) "
        )
        if answer != "Y":
            print("file is unchanged.")
            exit(0)
    with output_file.open("w") as output:
        output.write(CODE)
