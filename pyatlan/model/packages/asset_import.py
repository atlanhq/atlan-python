from __future__ import annotations

from json import dumps
from typing import List, Optional, Union

from pyatlan.model.enums import AssetInputHandling, WorkflowPackage
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.model.packages.base.custom_package import AbstractCustomPackage
from pyatlan.model.workflow import WorkflowMetadata


class AssetImport(AbstractCustomPackage):
    """
    Base configuration for a new Asset Import package.
    """

    _NAME = "asset-import"
    _PACKAGE_NAME = f"@csa/{_NAME}"
    _PACKAGE_PREFIX = WorkflowPackage.ASSET_IMPORT.value
    _PACKAGE_ICON = "http://assets.atlan.com/assets/ph-cloud-arrow-up-light.svg"
    _PACKAGE_LOGO = "http://assets.atlan.com/assets/ph-cloud-arrow-up-light.svg"

    def __init__(
        self,
    ):
        self._assets_advanced = False
        self._glossaries_advanced = False
        self._data_product_advanced = False
        super().__init__()

    def object_store(self) -> AssetImport:
        """
        Set up the package to import
        metadata directly from the object store.
        """
        self._parameters.append({"name": "import_type", "value": "CLOUD"})
        self._parameters.append({"name": "cloud_source", "value": "{{credentialGuid}}"})
        return self

    def s3(
        self,
        access_key: str,
        secret_key: str,
        region: str,
        bucket: str,
    ) -> AssetImport:
        """
        Set up package to import metadata from S3.

        :param access_key: AWS access key
        :param secret_key: AWS secret key
        :param region: AWS region
        :param bucket: bucket to retrieve object store object from

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
    ) -> AssetImport:
        """
        Set up package to import metadata from GCS.

        :param project_id: ID of GCP project
        :param service_account_json: service account credentials in JSON format
        :param bucket: bucket to retrieve object store object from

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
    ) -> AssetImport:
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

    def assets(
        self,
        prefix: str,
        object_key: str,
        input_handling: AssetInputHandling = AssetInputHandling.UPDATE,
    ) -> AssetImport:
        """
        Set up package to import assets.

        :param prefix: directory (path) within the object store from
            which to retrieve the file containing asset metadata
        :param object_key: object key (filename),
            including its extension, within the object store and prefix
        :param input_handling: specifies whether to allow the creation
            of new assets from the input CSV (full or partial assets)
            or only update existing assets in Atlan

        :returns: package, configured to import assets
        """
        self._parameters.append({"name": "assets_prefix", "value": prefix})
        self._parameters.append({"name": "assets_key", "value": object_key})
        self._parameters.append(
            {"name": "assets_upsert_semantic", "value": input_handling}
        )
        return self

    def assets_advanced(
        self,
        remove_attributes: Optional[Union[List[str], List[AtlanField]]] = None,
        fail_on_errors: Optional[bool] = None,
        case_sensitive_match: Optional[bool] = None,
        is_table_view_agnostic: Optional[bool] = None,
        field_separator: Optional[str] = None,
        batch_size: Optional[int] = None,
    ) -> AssetImport:
        """
        Set up package to import assets with advanced configuration.

        :param remove_attributes: list of attributes to clear (remove)
            from assets if their value is blank in the provided file.
        :param fail_on_errors: specifies whether an invalid value
            in a field should cause the import to fail (`True`) or
            log a warning, skip that value, and proceed (`False`).
        :param case_sensitive_match: indicates whether to use
            case-sensitive matching when running in update-only mode (`True`)
            or to try case-insensitive matching (`False`).
        :param is_table_view_agnostic: specifies whether to treat
            tables, views, and materialized views as interchangeable (`True`)
            or to strictly adhere to specified types in the input (`False`).
        :param field_separator: character used to separate
            fields in the input file (e.g., ',' or ';').
        :param batch_size: maximum number of rows
            to process at a time (per API request).

        :returns: package, configured to import
            assets with advanced configuration.
        """
        if isinstance(remove_attributes, list) and all(
            isinstance(field, AtlanField) for field in remove_attributes
        ):
            remove_attributes = [field.atlan_field_name for field in remove_attributes]  # type: ignore
        params = {
            "assets_attr_to_overwrite": dumps(remove_attributes, separators=(",", ":")),
            "assets_fail_on_errors": fail_on_errors,
            "assets_case_sensitive": case_sensitive_match,
            "assets_table_view_agnostic": is_table_view_agnostic,
            "assets_field_separator": field_separator,
            "assets_batch_size": batch_size,
        }
        self._add_optional_params(params)
        self._assets_advanced = True
        return self

    def glossaries(
        self,
        prefix: str,
        object_key: str,
        input_handling: AssetInputHandling = AssetInputHandling.UPDATE,
    ) -> AssetImport:
        """
        Set up package to import glossaries.

        :param prefix: directory (path) within the object store from
            which to retrieve the file containing glossaries, categories and terms
        :param object_key: object key (filename),
            including its extension, within the object store and prefix
        :param input_handling: specifies whether to allow the creation of new glossaries,
            categories and terms from the input CSV, or ensure these are only updated
            if they already exist in Atlan.

        :returns: package, configured to import glossaries, categories and terms.
        """
        self._parameters.append({"name": "glossaries_prefix", "value": prefix})
        self._parameters.append({"name": "glossaries_key", "value": object_key})
        self._parameters.append(
            {"name": "glossaries_upsert_semantic", "value": input_handling}
        )
        return self

    def glossaries_advanced(
        self,
        remove_attributes: Optional[Union[List[str], List[AtlanField]]] = None,
        fail_on_errors: Optional[bool] = None,
        field_separator: Optional[str] = None,
        batch_size: Optional[int] = None,
    ) -> AssetImport:
        """
        Set up package to import glossaries with advanced configuration.

        :param remove_attributes: list of attributes to clear (remove)
            from assets if their value is blank in the provided file.
        :param fail_on_errors: specifies whether an invalid value
            in a field should cause the import to fail (`True`) or
            log a warning, skip that value, and proceed (`False`).
        :param field_separator: character used to separate
            fields in the input file (e.g., ',' or ';').
        :param batch_size: maximum number of rows
            to process at a time (per API request).

        :returns: package, configured to import
            glossaries with advanced configuration.
        """
        if isinstance(remove_attributes, list) and all(
            isinstance(field, AtlanField) for field in remove_attributes
        ):
            remove_attributes = [field.atlan_field_name for field in remove_attributes]  # type: ignore
        params = {
            "glossaries_attr_to_overwrite": dumps(
                remove_attributes, separators=(",", ":")
            ),
            "glossaries_fail_on_errors": fail_on_errors,
            "glossaries_field_separator": field_separator,
            "glossaries_batch_size": batch_size,
        }
        self._add_optional_params(params)
        self._glossaries_advanced = True
        return self

    def data_products(
        self,
        prefix: str,
        object_key: str,
        input_handling: AssetInputHandling = AssetInputHandling.UPDATE,
    ) -> AssetImport:
        """
        Set up package to import data products.

        :param prefix: directory (path) within the object store from
            which to retrieve the file containing data domains, and data products
        :param object_key: object key (filename),
            including its extension, within the object store and prefix
        :param input_handling: specifies whether to allow the creation of new data domains, and data products
            from the input CSV, or ensure these are only updated if they already exist in Atlan.

        :returns: package, configured to import data domain and data products
        """
        self._parameters.append({"name": "data_products_prefix", "value": prefix})
        self._parameters.append({"name": "data_products_key", "value": object_key})
        self._parameters.append(
            {"name": "data_products_upsert_semantic", "value": input_handling}
        )
        return self

    def data_product_advanced(
        self,
        remove_attributes: Optional[Union[List[str], List[AtlanField]]] = None,
        fail_on_errors: Optional[bool] = None,
        field_separator: Optional[str] = None,
        batch_size: Optional[int] = None,
    ) -> AssetImport:
        """
        Set up package to import data domain
        and data products with advanced configuration.

        :param remove_attributes: list of attributes to clear (remove)
            from assets if their value is blank in the provided file.
        :param fail_on_errors: specifies whether an invalid value
            in a field should cause the import to fail (`True`) or
            log a warning, skip that value, and proceed (`False`).
        :param field_separator: character used to separate
            fields in the input file (e.g., ',' or ';').
        :param batch_size: maximum number of rows
            to process at a time (per API request).

        :returns: package, configured to import
            data domain and data products with advanced configuration.
        """
        if isinstance(remove_attributes, list) and all(
            isinstance(field, AtlanField) for field in remove_attributes
        ):
            remove_attributes = [field.atlan_field_name for field in remove_attributes]  # type: ignore
        params = {
            "data_products_attr_to_overwrite": dumps(
                remove_attributes, separators=(",", ":")
            ),
            "data_products_fail_on_errors": fail_on_errors,
            "data_products_field_separator": field_separator,
            "data_products_batch_size": batch_size,
        }
        self._add_optional_params(params)
        self._data_product_advanced = True
        return self

    def _set_required_metadata_params(self):
        self._parameters.append(
            dict(
                name="assets_config",
                value="advanced" if self._assets_advanced else "default",
            )
        )
        self._parameters.append(
            dict(
                name="glossaries_config",
                value="advanced" if self._glossaries_advanced else "default",
            )
        )
        self._parameters.append(
            dict(
                name="data_products_config",
                value="advanced" if self._data_product_advanced else "default",
            )
        )

    def _get_metadata(self) -> WorkflowMetadata:
        self._set_required_metadata_params()
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
                "orchestration.atlan.com/name": "Asset Import",
                "package.argoproj.io/author": "Atlan CSA",
                "package.argoproj.io/description": "Import assets from a CSV file.",
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
