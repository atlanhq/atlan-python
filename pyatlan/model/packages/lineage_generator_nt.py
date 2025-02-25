from __future__ import annotations

from enum import Enum
from typing import Optional

from pyatlan.model.enums import WorkflowPackage
from pyatlan.model.packages.base.custom_package import AbstractCustomPackage
from pyatlan.model.workflow import WorkflowMetadata


class LineageGenerator(AbstractCustomPackage):
    """
    Base configuration for a new lineage generator package.
    """

    _NAME = "lineage-generator"
    _PACKAGE_NAME = f"@csa/{_NAME}"
    _PACKAGE_PREFIX = WorkflowPackage.LINEAGE_GENERATOR.value
    _PACKAGE_ICON = "https://assets.atlan.com/assets/add-lineage.svg"
    _PACKAGE_LOGO = "https://assets.atlan.com/assets/add-lineage.svg"

    class OutputType(str, Enum):
        PREVIEW = "preview"
        GENERATE = "generate"
        DELETE = "delete"

    class SourceAssetType(str, Enum):
        Table = "Table"
        View = "View"
        MaterializedView = "Materialized View"
        Column = "Column"
        SalesforceObject = "Salesforce Object"
        SalesforceField = "Salesforce Field"
        MongoDBCollection = "MongoDB Collection"
        S3Object = "S3 Object"
        ADLSObject = "ADLS Object"
        PowerBITable = "Power BI Table"
        PowerBIColumn = "Power BI Column"
        GCSObject = "GCS Object"
        KafkaTopic = "Kafka Topic"
        CalculationView = "Calculation View"
        LookerField = "Looker Field"
        LookerView = "Looker View"

    class TargetAssetType(str, Enum):
        Table = "Table"
        View = "View"
        MaterializedView = "Materialized View"
        Column = "Column"
        SalesforceObject = "Salesforce Object"
        SalesforceField = "Salesforce Field"
        MongoDBCollection = "MongoDB Collection"
        S3Object = "S3 Object"
        ADLSObject = "ADLS Object"
        PowerBITable = "Power BI Table"
        PowerBIColumn = "Power BI Column"
        GCSObject = "GCS Object"
        KafkaTopic = "Kafka Topic"
        CalculationView = "Calculation View"
        LookerField = "Looker Field"
        LookerView = "Looker View"

    def config(
        self,
        source_asset_type: SourceAssetType,
        source_qualified_name: str,
        target_asset_type: TargetAssetType,
        target_qualified_name: str,
        case_sensitive_match: bool = False,
        match_on_schema: bool = False,
        output_type: OutputType = OutputType.PREVIEW,
        generate_on_child_assets: bool = False,
        regex_match: Optional[str] = None,
        regex_replace: Optional[str] = None,
        regex_match_schema: Optional[str] = None,
        regex_replace_schema: Optional[str] = None,
        regex_match_schema_name: Optional[str] = None,
        regex_replace_schema_name: Optional[str] = None,
        match_prefix: Optional[str] = None,
        match_suffix: Optional[str] = None,
        file_advanced_seperator: Optional[str] = None,
        file_advanced_position: Optional[str] = None,
        process_connection_qn: Optional[str] = None,
    ) -> LineageGenerator:
        """
        Set up the lineage generator with the specified configuration.

        :param source_asset_type: type name of the lineage input assets (sources).
        :param source_qualified_name: qualified name prefix of the lineage input assets (sources).
        :param target_asset_type: type name of the lineage output assets (targets).
        :param target_qualified_name: qualified name prefix of the lineage output assets (targets).
        :param case_sensitive_match: whether to match asset names using a case sensitive logic, default: `False`
        :param match_on_schema: whether to include the schema name to match source and target assets, default: `False`.
        If one of `"Source asset type"` or `"Target asset type"`
        is not a relational type (`Table`, `View`, `Materialized View`,
        `Calculation View` or `Column`) or a `MongoDB Collection` the option is ignored, default: `False`
        :param output_type: default to `Preview` lineage
            - `Preview` lineage: to generate a csv with the lineage preview.
            - `Generate` lineage: to generate the lineage on Atlan.
            - `Delete` lineage: to delete the lineage on Atlan.

        :param generate_on_child_assets: whether to generate the lineage on the
        child assets specified on `Source` asset type and `Target` asset type, default: `False`.
        :param regex_match (optional): if there is a re-naming happening between
        the source and the target that can be identified by a regex pattern,
        use this field to identify the characters to be replaced.
        :param regex_replace (optional): if there is a re-naming happening between the source
        and the target that can be identified by a regex pattern, use this field to specify the replacements characters.
        :param regex_match_schema (optional): if there is a re-naming happening between
        the source and the target schema that can be identified by a regex pattern,
        use this field to identify the characters to be replaced. Applicable only if `match_on_schema` is `False`.
        :param regex_replace_schema (optional): if there is a re-naming happening between
        the source and the target schema that can be identified by a regex pattern,
        use this field to specify the replacements characters. Applicable only if `match_on_schema` is `True`.
        :param regex_match_schema_name (optional): if there is a re-naming happening between
        the source and the target name + schema that can be identified by a regex pattern,
        use this field to identify the characters to be replaced. Applicable only if `match_on_schema`
        is `True`. It overrides any other regex defined.
        :param regex_replace_schema_name (optional): if there is a re-naming happening between
        the source and the target name + schema that can be identified by a regex pattern, use this
        field to specify the replacements characters. Applicable only if `match_on_schema` is `True`.
        It overrides any other regex defined.
        :param match_prefix (optional): prefix to add to source assets to match with target ones.
        :param match_suffix (optional): suffix to add to source assets to match with target ones.
        :param file_advanced_seperator (optional): sepator used to split the qualified name.
        It's applicable to file based assets only. eg: if the separator is equal to
        `/`: `default/s3/1707397085/arn:aws:s3:::mybucket/prefix/myobject.csv`
        -> [`default,s3,1707397085,arn:aws:s3:::mybucket,prefix,myobject.csv`]
        :param file_advanced_position (optional): number of substrings (created using "File advanced separator")
        to use for the asset match. The count is from right to left. It's applicable to file based assets only.
        In the above example if the value is equal to `3` -> [`arn:aws:s3:::mybucket,prefix,myobject.csv`]
        :param process_connection_qn (optional): connection for the process assets.
        If blank the process assets will be assigned to the source assets connection.

        :returns: package, set up lineage generator with the specified configuration.
        """
        params = {
            "source-asset-type": source_asset_type.value,
            "source-qualified-name-prefix": source_qualified_name,
            "target-asset-type": target_asset_type.value,
            "target-qualified-name-prefix": target_qualified_name,
            "case-sensitive": "yes" if case_sensitive_match else "no",
            "match-on-schema": "yes" if match_on_schema else "no",
            "output-option": output_type.value,
            "child-lineage": "yes" if generate_on_child_assets else "no",
            "regex-match": regex_match,
            "regex-replace": regex_replace,
            "regex-match-schema": regex_match_schema,
            "regex-replace-schema": regex_replace_schema,
            "regex-match-schema-name": regex_match_schema_name,
            "regex-replace-schema-name": regex_replace_schema_name,
            "name-prefix": match_prefix,
            "name-suffix": match_suffix,
            "file-advanced-separator": file_advanced_seperator,
            "file-advanced-positions": file_advanced_position,
            "connection-qualified-name": process_connection_qn,
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
                "orchestration.atlan.com/categories": "python,utility",
                "orchestration.atlan.com/dependentPackage": "",
                "orchestration.atlan.com/docsUrl": f"https://solutions.atlan.com/{self._NAME}/",
                "orchestration.atlan.com/emoji": "\U0001f680",
                "orchestration.atlan.com/icon": self._PACKAGE_ICON,
                "orchestration.atlan.com/logo": self._PACKAGE_LOGO,  # noqa
                "orchestration.atlan.com/name": "Lineage Generator (no transformations)",
                "package.argoproj.io/author": "Atlan CSA",
                "package.argoproj.io/description": "Package to generate lineage between two systems - no transformations involved.",  # noqa
                "package.argoproj.io/homepage": f"https://packages.atlan.com/-/web/detail/{self._PACKAGE_NAME}",
                "package.argoproj.io/keywords": '["python","utility", "custom-package"]',  # fmt: skip
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
