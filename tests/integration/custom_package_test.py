from pyatlan.pkg.models import CustomPackage
from pyatlan.pkg.ui import UIConfig, UIStep
from pyatlan.pkg.utils import PackageWriter
from pyatlan.pkg.widgets import TextInput


def test_custom_package():
    pkg = CustomPackage(
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
    writer = PackageWriter(path="../../generated_packages", pkg=pkg)
    writer.create_package()
    writer.create_templates()
