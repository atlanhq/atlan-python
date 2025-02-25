from __future__ import annotations

from typing import Optional

from pyatlan.model.enums import AssetInputHandling, WorkflowPackage
from pyatlan.model.packages.base.custom_package import AbstractCustomPackage
from pyatlan.model.workflow import WorkflowMetadata


class LineageBuilder(AbstractCustomPackage):
    """
    Base configuration for a new lineage builder package.
    """

    _NAME = "lineage-builder"
    _PACKAGE_NAME = f"@csa/{_NAME}"
    _PACKAGE_PREFIX = WorkflowPackage.LINEAGE_BUILDER.value
    _PACKAGE_ICON = "http://assets.atlan.com/assets/ph-tree-structure-light.svg"
    _PACKAGE_LOGO = "http://assets.atlan.com/assets/ph-tree-structure-light.svg"

    def object_store(
        self,
        prefix: str,
        object_key: str,
    ) -> LineageBuilder:
        """
        Set up the package to retrieve the lineage file from cloud object storage.

        :param prefix: directory (path) within the object store from
            which to retrieve the file containing asset metadata
        :param object_key: object key (filename),
            including its extension, within the object store and prefix

        :returns: package, set up to import lineage details from the object store
        """
        self._parameters.append({"name": "lineage_prefix", "value": prefix})
        self._parameters.append({"name": "lineage_key", "value": object_key})
        self._parameters.append({"name": "lineage_import_type", "value": "CLOUD"})
        self._parameters.append({"name": "cloud_source", "value": "{{credentialGuid}}"})
        return self

    def s3(
        self,
        access_key: str,
        secret_key: str,
        region: str,
        bucket: str,
    ) -> LineageBuilder:
        """
        Set up package to import lineage details from S3.

        :param access_key: AWS access key
        :param secret_key: AWS secret key
        :param region: AWS region
        :param bucket: bucket to retrieve object store object from

        :returns: package, set up to import lineage details from S3
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
    ) -> LineageBuilder:
        """
        Set up package to import lineage details from GCS.

        :param project_id: ID of GCP project
        :param service_account_json: service account credentials in JSON format
        :param bucket: bucket to retrieve object store object from

        :returns: Package set up to import lineage details from GCS
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
    ) -> LineageBuilder:
        """
        Set up package to import lineage details from ADLS.

        :param client_id: unique application (client) ID assigned by Azure AD when the app was registered
        :param client_secret: client secret for authentication
        :param tenant_id: unique ID of the Azure Active Directory instance
        :param account_name: name of the storage account
        :param container: container to retrieve object store objects from

        :returns: package, set up to import lineage details from ADLS
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

    def options(
        self,
        input_handling: AssetInputHandling = AssetInputHandling.PARTIAL,
        fail_on_errors: Optional[bool] = None,
        case_sensitive_match: Optional[bool] = None,
        field_separator: Optional[str] = None,
        batch_size: Optional[int] = None,
    ) -> LineageBuilder:
        """
        Set up the lineage builder with the specified options.

        :param input_handling: specifies whether to allow the creation
            of new assets from the input CSV (full or partial assets)
            or only update existing (skip) assets in Atlan.
        :param fail_on_errors: specifies whether an invalid value
            in a field should cause the import to fail (`True`) or
            log a warning, skip that value, and proceed (`False`).
        :param case_sensitive_match: indicates whether to use
            case-sensitive matching when running in update-only mode (`True`)
            or to try case-insensitive matching (`False`).
        :param field_separator: character used to separate
            fields in the input file (e.g., ',' or ';').
        :param batch_size: maximum number of rows
            to process at a time (per API request).

        :returns: package, configured to import
            assets with advanced configuration.
        """
        params = {
            "lineage_upsert_semantic": input_handling,
            "lineage_fail_on_errors": fail_on_errors,
            "lineage_case_sensitive": case_sensitive_match,
            "field_separator": field_separator,
            "batch_size": batch_size,
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
                "orchestration.atlan.com/name": "Lineage Builder",
                "package.argoproj.io/author": "Atlan CSA",
                "package.argoproj.io/description": "Build lineage from a CSV file.",
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": '["kotlin","utility"]',  # fmt: skip
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
