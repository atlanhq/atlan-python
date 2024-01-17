import importlib.util
from pathlib import Path

import pytest

from pyatlan.pkg.models import CustomPackage, generate
from pyatlan.pkg.ui import UIConfig, UIStep
from pyatlan.pkg.widgets import TextInput


@pytest.fixture
def custom_package():
    return CustomPackage(
        package_id="@csa/owner-propagator",
        package_name="Owner Propagator",
        description="Propagate owners from schema downwards.",
        icon_url="https://assets.atlan.com/assets/ph-user-switch-light.svg",
        docs_url="https://solutions.atlan.com/",
        ui_config=UIConfig(
            steps=[
                UIStep(
                    title="Configuration",
                    description="Owner propagation configuration",
                    inputs={
                        "qn_prefix": TextInput(
                            label="Qualified name prefix",
                            help="Provide the starting name for schemas from which to propagate ownership",
                            required=False,
                            placeholder="default/snowflake/1234567890",
                            grid=4,
                        )
                    },
                )
            ]
        ),
        container_image="ghcr.io/atlanhq/csa-owner-propagator:123",
        container_command=["/dumb-init", "--", "java", "OwnerPropagator"],
    )


def test_generate_package(custom_package: CustomPackage, tmpdir):
    dir = Path(tmpdir.mkdir("generated_packages"))

    generate(pkg=custom_package, path=dir, operation="package")

    package_dir = dir / "csa-owner-propagator"
    assert package_dir.exists()
    assert (package_dir / "index.js").exists()
    assert (package_dir / "package.json").exists()
    configmaps_dir = package_dir / "configmaps"
    assert configmaps_dir.exists()
    assert (configmaps_dir / "default.yaml").exists()
    templates_dir = package_dir / "templates"
    assert templates_dir.exists()
    assert (templates_dir / "default.yaml").exists()


def test_generate_config(custom_package: CustomPackage, tmpdir):
    dir = Path(tmpdir)

    generate(pkg=custom_package, path=dir, operation="config")

    assert dir / "logging.conf"
    config_name = "owner_propagator_cfg.py"
    assert dir / config_name

    spec = importlib.util.spec_from_file_location(
        "owner_propagator_cfg", dir / config_name
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert module is not None
    assert spec.loader is not None
    spec.loader.exec_module(module)
