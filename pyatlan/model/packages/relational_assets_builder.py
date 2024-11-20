from __future__ import annotations

from json import dumps
from typing import List, Optional, Union

from pyatlan.model.enums import (
    AssetDeltaHandling,
    AssetInputHandling,
    AssetRemovalType,
    WorkflowPackage,
)
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.model.packages.base.custom_package import AbstractCustomPackage
from pyatlan.model.workflow import WorkflowMetadata


class RelationalAssetsBuilder(AbstractCustomPackage):
    """
    Base configuration for the Relational Assets Builder package.
    """

    _NAME = "relational-assets-builder"
    _PACKAGE_NAME = f"@csa/{_NAME}"
    _PACKAGE_PREFIX = WorkflowPackage.RELATIONAL_ASSETS_BUILDER.value
    _PACKAGE_ICON = "http://assets.atlan.com/assets/ph-database-light.svg"
    _PACKAGE_LOGO = "http://assets.atlan.com/assets/ph-database-light.svg"

    def __init__(
        self,
    ):
        super().__init__()

    def direct(self) -> RelationalAssetsBuilder:
        """
        Set up package to directly upload the file.
        """
        self._parameters.append({"name": "import_type", "value": "DIRECT"})
        return self

    def object_store(
        self, prefix: Optional[str] = None, object_key: Optional[str] = None
    ) -> RelationalAssetsBuilder:
        """
        Set up the package to import
        metadata directly from the object store.

        :param prefix: directory (path) within the bucket/container from which to retrieve the object(s).
        :param object_key: object key (filename), including its extension, within the bucket/container and
        prefix.

        :returns: package, set up to import metadata from object store
        """
        self._parameters.append({"name": "import_type", "value": "CLOUD"})
        self._parameters.append({"name": "assets_prefix", "value": prefix})
        self._parameters.append({"name": "assets_key", "value": object_key})
        self._parameters.append({"name": "cloud_source", "value": "{{credentialGuid}}"})
        return self

    def s3(
        self,
        access_key: str,
        secret_key: str,
        region: str,
        bucket: str,
    ) -> RelationalAssetsBuilder:
        """
        Set up package to import metadata from S3.

        :param access_key: AWS access key
        :param secret_key: AWS secret key
        :param region: AWS region
        :param bucket: Enter the bucket from which to retrieve the object store object(s).

        :returns: package, set up to import metadata from S3
        """
        local_creds = {
            "name": f"csa-{self._NAME}-{self._epoch}-0",
            "auth_type": "s3",
            "username": access_key,
            "password": secret_key,
            "extra": {
                "region": region,
                "s3_bucket": bucket,
            },
            "connector_config_name": "csa-connectors-objectstore",
        }
        self._credentials_body.update(local_creds)
        return self

    def gcs(
        self, project_id: str, service_account_json: str, bucket: str
    ) -> RelationalAssetsBuilder:
        """
        Set up package to import metadata from GCS.

        :param project_id: ID of GCP project
        :param service_account_json: service account credentials in JSON format
        :param bucket: the bucket from which to retrieve the object store object(s)

        :returns: Package set up to import metadata from GCS
        """
        local_creds = {
            "name": f"csa-{self._NAME}-{self._epoch}-0",
            "auth_type": "gcs",
            "username": project_id,
            "password": service_account_json,
            "extra": {
                "gcs_bucket": bucket,
            },
            "connector_config_name": "csa-connectors-objectstore",
        }
        self._credentials_body.update(local_creds)
        return self

    def adls(
        self,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        account_name: str,
        container: str,
    ) -> RelationalAssetsBuilder:
        """
        Set up package to import metadata from ADLS.

        :param client_id: unique application (client) ID assigned by Azure AD when the app was registered
        :param client_secret: client secret for authentication
        :param tenant_id: unique ID of the Azure Active Directory instance
        :param account_name: name of the storage account
        :param container: container to retrieve object store objects from

        :returns: package, set up to import metadata from ADLS
        """
        local_creds = {
            "name": f"csa-{self._NAME}-{self._epoch}-0",
            "auth_type": "adls",
            "username": client_id,
            "password": client_secret,
            "extra": {
                "azure_tenant_id": tenant_id,
                "storage_account_name": account_name,
                "adls_container": container,
            },
            "connector_config_name": "csa-connectors-objectstore",
        }
        self._credentials_body.update(local_creds)
        return self

    def assets_semantics(
        self,
        input_handling: AssetInputHandling = AssetInputHandling.UPSERT,
        delta_handling: AssetDeltaHandling = AssetDeltaHandling.INCREMENTAL,
        removal_type: AssetRemovalType = AssetRemovalType.ARCHIVE,
    ) -> RelationalAssetsBuilder:
        """
        Set up the package to import metadata with semantics.

        :param input_handling: Whether to allow the creation of new (full or partial) assets from the input CSV,
                     or ensure assets are only updated if they already exist in Atlan.
        :param delta_handling: Whether to treat the input file as an initial load, full replacement (deleting any
                     existing assets not in the file) or only incremental (no deletion of existing assets).
        :param removal_type: If `delta_handling` is set to `FULL_REPLACEMENT`, this parameter specifies whether to
                    delete any assets not found in the latest file by archive (recoverable) or purge (non-recoverable).
                    If `delta_handling` is set to `INCREMENTAL`, this parameter is ignored and assets are archived.

        :returns: package, set up to import metadata with semantics
        """
        self._parameters.append(
            {"name": "assets_upsert_semantic", "value": input_handling}
        )
        self._parameters.append({"name": "delta_semantic", "value": delta_handling})
        if delta_handling == AssetDeltaHandling.FULL_REPLACEMENT:
            self._parameters.append(
                {"name": "delta_removal_type", "value": removal_type}
            )
        else:
            self._parameters.append(
                {"name": "delta_removal_type", "value": AssetRemovalType.ARCHIVE}
            )
        return self

    def options(
        self,
        remove_attributes: Optional[Union[List[str], List[AtlanField]]] = None,
        fail_on_errors: Optional[bool] = None,
        field_separator: Optional[str] = None,
        batch_size: Optional[int] = None,
    ) -> RelationalAssetsBuilder:
        """
        Set up package to import assets with advanced configuration.

        :param remove_attributes: list of attributes to clear (remove)
            from assets if their value is blank in the provided file.
        :param fail_on_errors: specifies whether an invalid value
            in a field should cause the import to fail (`True`) or
            log a warning, skip that value, and proceed (`False`).
        :param field_separator: character used to separate
            fields in the input file (e.g., ',' or ';').
        :param batch_size: maximum number of rows
            to process at a time (per API request).

        :returns: package, set up to import assets with advanced configuration
        """

        if isinstance(remove_attributes, list) and all(
            isinstance(field, AtlanField) for field in remove_attributes
        ):
            remove_attributes = [field.atlan_field_name for field in remove_attributes]  # type: ignore
        params = {
            "assets_attr_to_overwrite": dumps(remove_attributes, separators=(",", ":")),
            "assets_fail_on_errors": fail_on_errors,
            "assets_field_separator": field_separator,
            "assets_batch_size": batch_size,
        }
        self._add_optional_params(params)
        return self

    def _get_metadata(self) -> WorkflowMetadata:
        return WorkflowMetadata(
            labels={
                "orchestration.atlan.com/certified": "true",
                "orchestration.atlan.com/source": self._NAME,
                "orchestration.atlan.com/sourceCategory": "utility",
                "orchestration.atlan.com/type": "custom",
                "orchestration.atlan.com/preview": "true",
                "orchestration.atlan.com/verified": "true",
                "package.argoproj.io/installer": "argopm",
                "package.argoproj.io/name": f"a-t-rcsas-l-a-s-h{self._NAME}",
                "package.argoproj.io/registry": "httpsc-o-l-o-ns-l-a-s-hs-l-a-s-hpackages.atlan.com",
                "orchestration.atlan.com/atlan-ui": "true",
            },
            annotations={
                "orchestration.atlan.com/allowSchedule": "true",
                "orchestration.atlan.com/categories": "kotlin,utility",
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": f"https://solutions.atlan.com/{self._NAME}/",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,  # noqa
                "orchestration.atlan.com/name": "Relational Assets Builder",
                "package.argoproj.io/author": "Atlan CSA",
                "package.argoproj.io/description": "Build (and update) relational assets managed through a CSV file.",
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": "[\"kotlin\",\"utility\"]",  # fmt: skip
                "package.argoproj.io/name": self._PACKAGE_NAME,
                "package.argoproj.io/parent": ".",
                "package.argoproj.io/registry": "https://packages.atlan.com",
                "package.argoproj.io/repository": "git+https://github.com/atlanhq/marketplace-packages.git",
                "package.argoproj.io/support": "support@atlan.com",
                "orchestration.atlan.com/atlanName": f"csa-{self._NAME}-{self._epoch}",
            },
            name=f"csa-{self._NAME}-{self._epoch}",
            namespace="default",
        )
