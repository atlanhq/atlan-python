from __future__ import annotations

from typing import List, Optional

from pyatlan.model.enums import CustomWorkflowPackage
from pyatlan.model.packages.base.custom_package import AbstractCustomPackage
from pyatlan.model.workflow import WorkflowMetadata


class AssetExportPackage(AbstractCustomPackage):
    """
    Base configuration for the Asset Export package.
    """

    _NAME = "asset-export"
    _PACKAGE_NAME = f"@csa/{_NAME}"
    _PACKAGE_PREFIX = CustomWorkflowPackage.ASSET_EXPORT.value
    _PACKAGE_ICON = "http://assets.atlan.com/assets/ph-cloud-arrow-down-light.svg"
    _PACKAGE_LOGO = "http://assets.atlan.com/assets/ph-cloud-arrow-down-light.svg"

    def __init__(
        self,
    ):
        super().__init__()
        self._email_addresses = None
        self._delivery_type = None
        self._export_scope = None
        self._parameters = []

    def glossaries_only(
        self, include_archived: Optional[bool] = None
    ) -> AssetExportPackage:
        """
        Set up the package to export only glossaries.
        :param include_archived: Whether to include archived glossaries in the export.
        """
        self._export_scope = "GLOSSARIES_ONLY"
        self._parameters.append({"name": "export_scope", "value": self._export_scope})
        self._parameters.append(
            {
                "name": "include_archived",
                "value": include_archived,
            }
        )
        return self

    def enriched_only(
        self,
        prefix: str,
        include_description: Optional[str] = None,
        include_glossaries: Optional[bool] = None,
        include_data_products: Optional[bool] = None,
        include_archived: Optional[bool] = None,
    ) -> AssetExportPackage:
        """
        Set up the package to export only enriched assets.
        :param prefix: Qualified name prefix to filter assets.
        :param include_description: Whether to include asset descriptions in the export.
        :param include_glossaries: Whether to include glossaries in the export.
        :param include_data_products: Whether to include data products in the export.
        :param include_archived: Whether to include archived assets in the export.
        """
        self._export_scope = "ENRICHED_ONLY"
        self._parameters.append({"name": "export_scope", "value": self._export_scope})
        params = {
            "qn_prefix": prefix,
            "include_description": include_description,
            "include_glossaries": include_glossaries,
            "include_data_products": include_data_products,
            "include_archived": include_archived,
        }
        self._add_optional_params(params)
        return self

    def products_only(
        self, include_archived: Optional[bool] = None
    ) -> AssetExportPackage:
        """
        Set up the package to export only data products.
        :param include_archived: Whether to include archived data products in the export.
        """
        self._export_scope = "PRODUCTS_ONLY"
        self._parameters.append({"name": "export_scope", "value": self._export_scope})
        self._parameters.append(
            {
                "name": "include_archived",
                "value": include_archived,
            }
        )
        return self

    def all_assets(
        self,
        prefix: str,
        include_description: Optional[str] = None,
        include_glossaries: Optional[bool] = None,
        include_data_products: Optional[bool] = None,
        include_archived: Optional[bool] = None,
    ) -> AssetExportPackage:
        """
        Set up the package to export all assets.
        :param prefix: Qualified name prefix to filter assets.
        :param include_description: Whether to include asset descriptions in the export.
        :param include_glossaries: Whether to include glossaries in the export.
        :param include_data_products: Whether to include data products in the export.
        :param include_archived: Whether to include archived assets in the export.
        """
        self._export_scope = "ALL"
        self._parameters.append({"name": "export_scope", "value": self._export_scope})
        params = {
            "qn_prefix": prefix,
            "include_description": include_description,
            "include_glossaries": include_glossaries,
            "include_data_products": include_data_products,
            "include_archived": include_archived,
        }
        self._add_optional_params(params)

        return self

    def direct(self) -> AssetExportPackage:
        """
        Set up the package to deliver the export via direct download.
        """
        self._delivery_type = "DIRECT"
        self._add_delivery_parameters()
        return self

    def email(self, email_addresses: List[str]) -> AssetExportPackage:
        """
        Set up the package to deliver the export via email.
        :param email_addresses: List of email addresses to send the export to.
        """
        self._delivery_type = "EMAIL"
        self._email_addresses = email_addresses
        self._add_delivery_parameters()

        return self

    def object_store(self, prefix: Optional[str] = None) -> AssetExportPackage:
        """
        Set up the package to export to an object storage location.
        :param prefix: The directory (path) within the object store to upload the exported file.
        """
        self._delivery_type = "CLOUD"
        self._add_delivery_parameters()
        self._parameters.append({"name": "target_prefix", "value": prefix})
        self._parameters.append({"name": "cloud_target", "value": "{{credentialGuid}}"})
        return self

    def s3(
        self, access_key: str, secret_key: str, region: str, bucket: str
    ) -> AssetExportPackage:
        """
        Set up package to export to S3.
        :param access_key: AWS access key
        :param secret_key: AWS secret key
        :param region: AWS region
        :param bucket: S3 bucket to upload the export file to
        """
        self._credentials_body.update(
            {
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
        )
        return self

    def gcs(
        self, project_id: str, service_account_json: str, bucket: str
    ) -> AssetExportPackage:
        """
        Set up package to export to Google Cloud Storage.
        :param project_id: GCP project ID
        :param service_account_json: GCP service account JSON credentials
        :param bucket: GCS bucket to upload the export file to
        """
        self._credentials_body.update(
            {
                "name": f"csa-{self._NAME}-{self._epoch}-0",
                "auth_type": "gcs",
                "username": project_id,
                "password": service_account_json,
                "extra": {
                    "gcs_bucket": bucket,
                },
                "connector_config_name": "csa-connectors-objectstore",
            }
        )
        return self

    def adls(
        self,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        account_name: str,
        container: str,
    ) -> AssetExportPackage:
        """
        Set up package to export to Azure Data Lake Storage.
        :param client_id: Azure AD client ID
        :param client_secret: Azure AD client secret
        :param tenant_id: Azure tenant ID
        :param account_name: ADLS storage account name
        :param container: ADLS container to upload the export file to
        """
        self._credentials_body.update(
            {
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
        )
        return self

    def _add_delivery_parameters(self):
        """
        Add delivery parameters to the parameters list.
        """
        self._parameters.append(
            {
                "name": "delivery_type",
                "value": self._delivery_type,
            }
        )
        if self._delivery_type == "EMAIL" and self._email_addresses:
            self._parameters.append(
                {
                    "name": "email_addresses",
                    "value": ",".join(
                        self._email_addresses
                    ),  # Join the email addresses if they are in a list
                }
            )

    def _get_metadata(self) -> WorkflowMetadata:
        return WorkflowMetadata(
            labels={
                "orchestration.atlan.com/certified": "true",
                "orchestration.atlan.com/preview": "true",
                "orchestration.atlan.com/source": self._NAME,
                "orchestration.atlan.com/sourceCategory": "utility",
                "orchestration.atlan.com/type": "custom",
                "orchestration.atlan.com/verified": "true",
                "package.argoproj.io/installer": "argopm",
                "package.argoproj.io/name": "a-t-rcsas-l-a-s-h{self._NAME}",
                "package.argoproj.io/parent": "",
                "package.argoproj.io/registry": "local",
                "package.argoproj.io/version": "2.3.1-SNAPSHOT",
                "orchestration.atlan.com/atlan-ui": "true",
            },
            annotations={
                "orchestration.atlan.com/allowSchedule": "true",
                "orchestration.atlan.com/categories": "kotlin,utility",
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": "https://solutions.atlan.com/{self._NAME}",
                "orchestration.atlan.com/emoji": "🚀",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,  # noqa
                "orchestration.atlan.com/name": "Asset Export (Basic)",
                "package.argoproj.io/author": "Atlan CSA",
                "package.argoproj.io/description": "Export assets with all enrichment that could be made against them "
                "via the Atlan UI.",
                "package.argoproj.io/homepage": "https://packages.atlan.com/-/web/detail/@csa/{self._PACKAGE_NAME}",
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
