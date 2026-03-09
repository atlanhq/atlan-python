# STDLIB_IMPORT: import json
# STDLIB_IMPORT: import time
# STDLIB_IMPORT: import uuid
# IMPORT: from pyatlan.errors import ErrorCode
# IMPORT: from pyatlan.model.enums import DataQualityDimension, DataQualityRuleAlertPriority, DataQualityRuleCustomSQLReturnType, DataQualityRuleStatus, DataQualityRuleTemplateType, DataQualityRuleThresholdCompareOperator, DataQualityRuleThresholdUnit, DataQualitySourceSyncStatus
# INTERNAL_IMPORT: from pyatlan.model.structs import DataQualityRuleConfigArguments, DataQualityRuleThresholdObject
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def custom_sql_creator(
        cls,
        *,
        client: "AtlanClient",
        rule_name: str,
        asset: Asset,
        custom_sql: str,
        threshold_compare_operator: DataQualityRuleThresholdCompareOperator,
        threshold_value: int,
        alert_priority: DataQualityRuleAlertPriority,
        dimension: DataQualityDimension,
        custom_sql_return_type: Optional[DataQualityRuleCustomSQLReturnType] = None,
        description: Optional[str] = None,
    ) -> "DataQualityRule":
        validate_required_fields(
            [
                "client",
                "rule_name",
                "asset",
                "threshold_compare_operator",
                "threshold_value",
                "alert_priority",
                "dimension",
                "custom_sql",
            ],
            [
                client,
                rule_name,
                asset,
                threshold_compare_operator,
                threshold_value,
                alert_priority,
                dimension,
                custom_sql,
            ],
        )
        return cls._build_rule(
            client=client,
            rule_name=rule_name,
            rule_type=DataQualityRuleTemplateType.CUSTOM_SQL,
            asset=asset,
            threshold_compare_operator=threshold_compare_operator,
            threshold_value=threshold_value,
            alert_priority=alert_priority,
            dimension=dimension,
            custom_sql=custom_sql,
            custom_sql_return_type=custom_sql_return_type,
            description=description,
            column=None,
            threshold_unit=None,
        )

    @classmethod
    @init_guid
    def table_level_rule_creator(
        cls,
        *,
        client: "AtlanClient",
        rule_type: DataQualityRuleTemplateType,
        asset: Asset,
        threshold_value: int,
        alert_priority: DataQualityRuleAlertPriority,
        threshold_compare_operator: Optional[
            DataQualityRuleThresholdCompareOperator
        ] = None,
        threshold_unit: Optional[DataQualityRuleThresholdUnit] = None,
        rule_conditions: Optional[str] = None,
        row_scope_filtering_enabled: Optional[bool] = False,
    ) -> "DataQualityRule":
        validate_required_fields(
            ["client", "rule_type", "asset", "threshold_value", "alert_priority"],
            [client, rule_type, asset, threshold_value, alert_priority],
        )
        template_config = client.dq_template_config_cache.get_template_config(
            rule_type.value
        )
        asset_for_validation, target_table_asset = (
            cls._fetch_assets_for_row_scope_validation(
                client, asset, rule_conditions, row_scope_filtering_enabled or False
            )
        )
        validated_threshold_operator = cls._validate_template_features(
            rule_type,
            rule_conditions,
            row_scope_filtering_enabled,
            template_config,
            threshold_compare_operator,
            asset_for_validation,
            target_table_asset,
        )
        final_threshold_compare_operator = (
            validated_threshold_operator
            or threshold_compare_operator
            or DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL
        )
        return cls._build_rule(
            client=client,
            rule_type=rule_type,
            asset=asset,
            threshold_compare_operator=final_threshold_compare_operator,
            threshold_value=threshold_value,
            alert_priority=alert_priority,
            rule_name=None,
            column=None,
            threshold_unit=threshold_unit,
            dimension=None,
            custom_sql=None,
            description=None,
            rule_conditions=rule_conditions,
            row_scope_filtering_enabled=row_scope_filtering_enabled,
        )

    @classmethod
    @init_guid
    def column_level_rule_creator(
        cls,
        *,
        client: "AtlanClient",
        rule_type: DataQualityRuleTemplateType,
        asset: Asset,
        column: Asset,
        threshold_value: int,
        alert_priority: DataQualityRuleAlertPriority,
        threshold_compare_operator: Optional[
            DataQualityRuleThresholdCompareOperator
        ] = None,
        threshold_unit: Optional[DataQualityRuleThresholdUnit] = None,
        rule_conditions: Optional[str] = None,
        row_scope_filtering_enabled: Optional[bool] = False,
    ) -> "DataQualityRule":
        validate_required_fields(
            [
                "client",
                "rule_type",
                "asset",
                "column",
                "threshold_value",
                "alert_priority",
            ],
            [client, rule_type, asset, column, threshold_value, alert_priority],
        )
        template_config = client.dq_template_config_cache.get_template_config(
            rule_type.value
        )
        asset_for_validation, target_table_asset = (
            cls._fetch_assets_for_row_scope_validation(
                client, asset, rule_conditions, row_scope_filtering_enabled or False
            )
        )
        validated_threshold_operator = cls._validate_template_features(
            rule_type,
            rule_conditions,
            row_scope_filtering_enabled,
            template_config,
            threshold_compare_operator,
            asset_for_validation,
            target_table_asset,
        )
        final_threshold_compare_operator = (
            validated_threshold_operator
            or threshold_compare_operator
            or DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL
        )
        return cls._build_rule(
            client=client,
            rule_type=rule_type,
            asset=asset,
            column=column,
            threshold_compare_operator=final_threshold_compare_operator,
            threshold_value=threshold_value,
            alert_priority=alert_priority,
            threshold_unit=threshold_unit,
            rule_name=None,
            dimension=None,
            custom_sql=None,
            description=None,
            rule_conditions=rule_conditions,
            row_scope_filtering_enabled=row_scope_filtering_enabled,
        )

    @classmethod
    @init_guid
    def updater(
        cls,
        client: "AtlanClient",
        qualified_name: str,
        threshold_compare_operator: Optional[
            DataQualityRuleThresholdCompareOperator
        ] = None,
        threshold_value: Optional[int] = None,
        alert_priority: Optional[DataQualityRuleAlertPriority] = None,
        threshold_unit: Optional[DataQualityRuleThresholdUnit] = None,
        dimension: Optional[DataQualityDimension] = None,
        custom_sql: Optional[str] = None,
        custom_sql_return_type: Optional[DataQualityRuleCustomSQLReturnType] = None,
        rule_name: Optional[str] = None,
        description: Optional[str] = None,
        rule_conditions: Optional[str] = None,
        row_scope_filtering_enabled: Optional[bool] = False,
    ) -> "DataQualityRule":
        from pyatlan_v9.model.fluent_search import FluentSearch

        validate_required_fields(
            ["client", "qualified_name"],
            [client, qualified_name],
        )
        request = (
            FluentSearch()
            .where(DataQualityRule.QUALIFIED_NAME.eq(qualified_name))
            .include_on_results(DataQualityRule.NAME)
            .include_on_results(DataQualityRule.DQ_RULE_TEMPLATE_NAME)
            .include_on_results(DataQualityRule.DQ_RULE_TEMPLATE)
            .include_on_results(DataQualityRule.DQ_RULE_BASE_DATASET)
            .include_on_results(DataQualityRule.DQ_RULE_BASE_COLUMN)
            .include_on_results(DataQualityRule.DQ_RULE_ALERT_PRIORITY)
            .include_on_results(DataQualityRule.DISPLAY_NAME)
            .include_on_results(DataQualityRule.DQ_RULE_CUSTOM_SQL)
            .include_on_results(DataQualityRule.DQ_RULE_CUSTOM_SQL_RETURN_TYPE)
            .include_on_results(DataQualityRule.USER_DESCRIPTION)
            .include_on_results(DataQualityRule.DQ_RULE_DIMENSION)
            .include_on_results(DataQualityRule.DQ_RULE_CONFIG_ARGUMENTS)
            .include_on_results(DataQualityRule.DQ_RULE_ROW_SCOPE_FILTERING_ENABLED)
            .include_on_results(DataQualityRule.DQ_RULE_SOURCE_SYNC_STATUS)
            .include_on_results(DataQualityRule.DQ_RULE_STATUS)
        ).to_request()

        results = client.asset.search(request)

        if results.count != 1:
            raise ValueError(
                f"Expected exactly 1 asset for qualified_name: {qualified_name}, "
                f"but found: {results.count}"
            )
        search_result = results.current_page()[0]

        retrieved_custom_sql = getattr(search_result, "dq_rule_custom_sql", None)
        retrieved_custom_sql_return_type = getattr(
            search_result, "dq_rule_custom_sql_return_type", None
        )
        retrieved_rule_name = getattr(search_result, "display_name", None)
        retrieved_dimension = getattr(search_result, "dq_rule_dimension", None)
        retrieved_column = getattr(search_result, "dq_rule_base_column", None)
        retrieved_alert_priority = getattr(
            search_result, "dq_rule_alert_priority", None
        )
        retrieved_row_scope_filtering_enabled = getattr(
            search_result, "dq_rule_row_scope_filtering_enabled", None
        )
        retrieved_description = getattr(search_result, "user_description", None)
        retrieved_asset = getattr(search_result, "dq_rule_base_dataset", None)
        retrieved_template_rule_name = getattr(
            search_result, "dq_rule_template_name", None
        )
        retrieved_template = getattr(search_result, "dq_rule_template", None)

        config_args = getattr(search_result, "dq_rule_config_arguments", None)
        threshold_obj = (
            getattr(config_args, "dq_rule_threshold_object", None)
            if config_args
            else None
        )
        retrieved_threshold_compare_operator = (
            getattr(threshold_obj, "dq_rule_threshold_compare_operator", None)
            if threshold_obj
            else None
        )
        retrieved_threshold_value = (
            getattr(threshold_obj, "dq_rule_threshold_value", None)
            if threshold_obj
            else None
        )
        retrieved_threshold_unit = (
            getattr(threshold_obj, "dq_rule_threshold_unit", None)
            if threshold_obj
            else None
        )

        template_config = None
        if retrieved_template_rule_name:
            template_config = client.dq_template_config_cache.get_template_config(
                retrieved_template_rule_name
            )

        if rule_conditions:
            final_rule_conditions = rule_conditions
        elif config_args is not None:
            final_rule_conditions = getattr(
                config_args, "dq_rule_config_rule_conditions", None
            )
        else:
            final_rule_conditions = None

        final_row_scope_filtering_enabled = (
            row_scope_filtering_enabled or retrieved_row_scope_filtering_enabled
        )
        if retrieved_asset:
            retrieved_asset, target_table_asset = (
                cls._fetch_assets_for_row_scope_validation(
                    client,
                    retrieved_asset,
                    final_rule_conditions,
                    final_row_scope_filtering_enabled,
                )
            )
        else:
            target_table_asset = None

        validated_threshold_operator = None
        if retrieved_template_rule_name and template_config:
            try:
                retrieved_rule_type = DataQualityRuleTemplateType(
                    retrieved_template_rule_name
                )
                validated_threshold_operator = cls._validate_template_features(
                    retrieved_rule_type,
                    final_rule_conditions,
                    final_row_scope_filtering_enabled,
                    template_config,
                    threshold_compare_operator or retrieved_threshold_compare_operator,
                    retrieved_asset,
                    target_table_asset,
                )
            except ValueError:
                pass

        final_compare_operator = (
            validated_threshold_operator
            or threshold_compare_operator
            or retrieved_threshold_compare_operator
            or DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL
        )

        # Deferred import to avoid circular dependency
        from .data_quality_rule_template import DataQualityRuleTemplate

        rule = cls(
            name="",
            dq_rule_config_arguments=DataQualityRuleConfigArguments(
                dq_rule_threshold_object=DataQualityRuleThresholdObject(
                    dq_rule_threshold_compare_operator=final_compare_operator,
                    dq_rule_threshold_value=threshold_value
                    or retrieved_threshold_value,
                    dq_rule_threshold_unit=threshold_unit or retrieved_threshold_unit,
                ),
                dq_rule_config_rule_conditions=final_rule_conditions,
            ),
            dq_rule_base_dataset_qualified_name=(
                retrieved_asset.qualified_name if retrieved_asset else None
            ),
            dq_rule_alert_priority=alert_priority or retrieved_alert_priority,
            dq_rule_row_scope_filtering_enabled=final_row_scope_filtering_enabled,
            dq_rule_base_dataset=retrieved_asset,
            qualified_name=qualified_name,
            dq_rule_dimension=dimension or retrieved_dimension,
            dq_rule_template_name=retrieved_template_rule_name,
            dq_rule_template=(
                DataQualityRuleTemplate.ref_by_qualified_name(
                    qualified_name=retrieved_template.qualified_name
                )
                if retrieved_template
                else None
            ),
        )

        if retrieved_column is not None:
            rule.dq_rule_base_column_qualified_name = retrieved_column.qualified_name
            rule.dq_rule_base_column = retrieved_column

        final_custom_sql = custom_sql or retrieved_custom_sql
        if final_custom_sql is not None:
            rule.dq_rule_custom_sql = final_custom_sql
            rule.display_name = rule_name or retrieved_rule_name
            rule.dq_rule_custom_sql_return_type = (
                custom_sql_return_type or retrieved_custom_sql_return_type
            )
            if description is not None:
                rule.user_description = description or retrieved_description

        return rule

    @classmethod
    def _build_rule(
        cls,
        *,
        client: "AtlanClient",
        rule_type: DataQualityRuleTemplateType,
        asset: Asset,
        threshold_compare_operator: DataQualityRuleThresholdCompareOperator,
        threshold_value: int,
        alert_priority: DataQualityRuleAlertPriority,
        rule_name: Optional[str] = None,
        column: Optional[Asset] = None,
        threshold_unit: Optional[DataQualityRuleThresholdUnit] = None,
        dimension: Optional[DataQualityDimension] = None,
        custom_sql: Optional[str] = None,
        custom_sql_return_type: Optional[DataQualityRuleCustomSQLReturnType] = None,
        description: Optional[str] = None,
        rule_conditions: Optional[str] = None,
        row_scope_filtering_enabled: Optional[bool] = False,
    ) -> "DataQualityRule":
        """Internal helper that mirrors the legacy ``Attributes.creator`` logic."""
        template_config = client.dq_template_config_cache.get_template_config(
            rule_type.value
        )
        if template_config is None:
            raise ErrorCode.DQ_RULE_NOT_FOUND.exception_with_parameters(rule_type.value)

        template_rule_name = template_config.get("name")
        template_qualified_name = template_config.get("qualified_name")

        if dimension is None:
            dimension = template_config.get("dimension")

        if threshold_unit is None:
            config = template_config.get("config")
            if config is not None:
                threshold_unit = cls._get_template_config_value(
                    config.dq_rule_template_config_threshold_object,
                    "dqRuleTemplateConfigThresholdUnit",
                    "default",
                )

        # Deferred import to avoid circular dependency
        from .data_quality_rule_template import DataQualityRuleTemplate

        rule = cls(
            name="",
            dq_rule_config_arguments=DataQualityRuleConfigArguments(
                dq_rule_threshold_object=DataQualityRuleThresholdObject(
                    dq_rule_threshold_compare_operator=threshold_compare_operator,
                    dq_rule_threshold_value=threshold_value,
                    dq_rule_threshold_unit=threshold_unit,
                ),
                dq_rule_config_rule_conditions=rule_conditions,
            ),
            dq_rule_base_dataset_qualified_name=asset.qualified_name,
            dq_rule_alert_priority=alert_priority,
            dq_rule_row_scope_filtering_enabled=row_scope_filtering_enabled,
            dq_rule_source_sync_status=DataQualitySourceSyncStatus.IN_PROGRESS,
            dq_rule_status=DataQualityRuleStatus.ACTIVE,
            dq_rule_base_dataset=asset,
            qualified_name=f"{asset.qualified_name}/rule/{cls._generate_uuid()}",
            dq_rule_dimension=dimension,
            dq_rule_template_name=template_rule_name,
            dq_rule_template=DataQualityRuleTemplate.ref_by_qualified_name(
                qualified_name=template_qualified_name,
            ),
        )

        if column is not None:
            rule.dq_rule_base_column_qualified_name = column.qualified_name
            rule.dq_rule_base_column = column

        if custom_sql is not None:
            rule.dq_rule_custom_sql = custom_sql
            rule.display_name = rule_name
            if custom_sql_return_type is not None:
                rule.dq_rule_custom_sql_return_type = custom_sql_return_type
            if description is not None:
                rule.user_description = description

        return rule

    @staticmethod
    def _generate_uuid() -> str:
        d = int(time.time() * 1000)
        random_bytes = uuid.uuid4().bytes
        rand_index = 0

        def replace_char(c: str) -> str:
            nonlocal d, rand_index
            r = (d + random_bytes[rand_index % 16]) % 16
            rand_index += 1
            d = d // 16
            if c == "x":
                return hex(r)[2:]
            elif c == "y":
                return hex((r & 0x3) | 0x8)[2:]
            else:
                return c

        template = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
        return "".join(replace_char(c) if c in "xy" else c for c in template)

    @staticmethod
    def _get_template_config_value(
        config_value: str,
        property_name: Optional[str] = None,
        value_key: str = "default",
    ):
        if not config_value:
            return None
        try:
            config_json = json.loads(config_value)
            if property_name:
                properties = config_json.get("properties", {})
                field = properties.get(property_name, {})
                return field.get(value_key)
            else:
                return config_json.get(value_key)
        except (json.JSONDecodeError, KeyError):
            return None

    @staticmethod
    def _validate_template_features(
        rule_type: DataQualityRuleTemplateType,
        rule_conditions: Optional[str],
        row_scope_filtering_enabled: Optional[bool],
        template_config: Optional[dict],
        threshold_compare_operator: Optional[
            DataQualityRuleThresholdCompareOperator
        ] = None,
        asset: Optional[Asset] = None,
        target_table_asset: Optional[Asset] = None,
    ) -> Optional[DataQualityRuleThresholdCompareOperator]:
        if not template_config or not template_config.get("config"):
            return None

        config = template_config["config"]

        if rule_conditions and config.dq_rule_template_config_rule_conditions is None:
            raise ErrorCode.DQ_RULE_TYPE_NOT_SUPPORTED.exception_with_parameters(
                rule_type.value, "rule conditions"
            )

        if row_scope_filtering_enabled:
            advanced_settings = config.dq_rule_template_config_advanced_settings or ""
            if "dqRuleRowScopeFilteringEnabled" not in str(advanced_settings):
                raise ErrorCode.DQ_RULE_TYPE_NOT_SUPPORTED.exception_with_parameters(
                    rule_type.value, "row scope filtering"
                )
            if asset and not getattr(
                asset,
                "asset_dq_row_scope_filter_column_qualified_name",
                None,
            ):
                raise ErrorCode.DQ_ROW_SCOPE_FILTER_COLUMN_MISSING.exception_with_parameters(
                    getattr(asset, "qualified_name", "unknown")
                )
            if target_table_asset:
                if not getattr(
                    target_table_asset,
                    "asset_dq_row_scope_filter_column_qualified_name",
                    None,
                ):
                    raise ErrorCode.DQ_ROW_SCOPE_FILTER_COLUMN_MISSING.exception_with_parameters(
                        getattr(target_table_asset, "qualified_name", "unknown")
                    )

        if rule_conditions:
            allowed_rule_conditions = DataQualityRule._get_template_config_value(
                config.dq_rule_template_config_rule_conditions or "",
                None,
                "enum",
            )
            if allowed_rule_conditions:
                try:
                    rule_conditions_json = json.loads(rule_conditions)
                    conditions = rule_conditions_json.get("conditions", [])
                    if len(conditions) != 1:
                        raise ErrorCode.DQ_RULE_CONDITIONS_INVALID.exception_with_parameters(
                            f"exactly one condition required, found {len(conditions)}"
                        )
                    condition_type = conditions[0].get("type")
                except json.JSONDecodeError:
                    condition_type = rule_conditions

                if condition_type not in allowed_rule_conditions:
                    raise ErrorCode.DQ_RULE_CONDITIONS_INVALID.exception_with_parameters(
                        f"condition type '{condition_type}' not supported, allowed: {allowed_rule_conditions}"
                    )

            if threshold_compare_operator is None:
                return DataQualityRuleThresholdCompareOperator.EQUAL
            elif (
                threshold_compare_operator
                != DataQualityRuleThresholdCompareOperator.EQUAL
            ):
                raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                    f"threshold_compare_operator={threshold_compare_operator.value}",
                    "threshold_compare_operator",
                    "EQUAL when rule_conditions are provided",
                )

        if threshold_compare_operator is not None:
            allowed_operators = DataQualityRule._get_template_config_value(
                config.dq_rule_template_config_threshold_object,
                "dqRuleTemplateConfigThresholdCompareOperator",
                "enum",
            )
            if (
                allowed_operators
                and threshold_compare_operator.value not in allowed_operators
            ):
                raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                    f"threshold_compare_operator={threshold_compare_operator.value}",
                    "threshold_compare_operator",
                    f"must be one of {allowed_operators}",
                )
        elif threshold_compare_operator is None:
            default_value = DataQualityRule._get_template_config_value(
                config.dq_rule_template_config_threshold_object,
                "dqRuleTemplateConfigThresholdCompareOperator",
                "default",
            )
            if default_value:
                threshold_compare_operator = DataQualityRuleThresholdCompareOperator(
                    default_value
                )

        return (
            threshold_compare_operator
            or DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL
        )

    @staticmethod
    def _fetch_assets_for_row_scope_validation(
        client: "AtlanClient",
        base_asset: Asset,
        rule_conditions: Optional[str],
        row_scope_filtering_enabled: bool,
    ) -> tuple[Asset, Optional[Asset]]:
        asset_for_validation = base_asset
        target_table_asset = None

        if not row_scope_filtering_enabled:
            return asset_for_validation, target_table_asset

        # Extract target_table from rule_conditions
        target_table_qualified_name = None
        if rule_conditions:
            try:
                rule_conditions_json = json.loads(rule_conditions)
                conditions = rule_conditions_json.get("conditions", [])
                if conditions:
                    condition_value = conditions[0].get("value", {})
                    target_table_qualified_name = condition_value.get("target_table")
            except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
                pass

        qualified_names_to_search = []
        if base_asset.qualified_name:
            qualified_names_to_search.append(base_asset.qualified_name)
        if target_table_qualified_name:
            qualified_names_to_search.append(target_table_qualified_name)

        if qualified_names_to_search:
            from pyatlan_v9.model.fluent_search import FluentSearch

            search_request = (
                FluentSearch()
                .where(Asset.QUALIFIED_NAME.within(qualified_names_to_search))
                .include_on_results(
                    Asset.ASSET_DQ_ROW_SCOPE_FILTER_COLUMN_QUALIFIED_NAME
                )
            ).to_request()
            results = client.asset.search(search_request)

            for result in results.current_page():
                if result.qualified_name == base_asset.qualified_name:
                    asset_for_validation = result
                elif (
                    target_table_qualified_name
                    and result.qualified_name == target_table_qualified_name
                ):
                    target_table_asset = result

        return asset_for_validation, target_table_asset
