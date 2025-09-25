import json
from unittest.mock import Mock

import pytest

from pyatlan.errors import ErrorCode, InvalidRequestError
from pyatlan.model.assets import Column, DataQualityRule, Table
from pyatlan.model.dq_rule_conditions import DQRuleConditionsBuilder
from pyatlan.model.enums import (
    DataQualityDimension,
    DataQualityRuleAlertPriority,
    DataQualityRuleStatus,
    DataQualityRuleTemplateConfigRuleConditions,
    DataQualityRuleThresholdCompareOperator,
    DataQualityRuleThresholdUnit,
)
from tests.unit.model.constants import (
    DQ_COLUMN_QUALIFIED_NAME,
    DQ_RULE_CUSTOM_SQL,
    DQ_RULE_DESCRIPTION,
    DQ_RULE_NAME,
    DQ_RULE_THRESHOLD_VALUE,
    DQ_RULE_TYPE_COLUMN,
    DQ_RULE_TYPE_TABLE,
    DQ_TABLE_QUALIFIED_NAME,
)


@pytest.fixture
def mock_client():
    client = Mock()
    client.dq_template_config_cache = Mock()

    # Create a proper config object with a JSON string for threshold_object
    config = Mock()
    config.dq_rule_template_config_threshold_object = json.dumps(
        {
            "properties": {
                "dqRuleTemplateConfigThresholdUnit": {
                    "default": DataQualityRuleThresholdUnit.PERCENTAGE
                }
            }
        }
    )
    config.dq_rule_template_config_rule_conditions = json.dumps(
        {"enum": ["STRING_LENGTH_BETWEEN", "STRING_LENGTH_EQUAL"]}
    )
    config.dq_rule_template_config_advanced_settings = json.dumps(
        {"dqRuleRowScopeFilteringEnabled": True}
    )

    client.dq_template_config_cache.get_template_config.return_value = {
        "name": "Test Template",
        "qualified_name": "test/template/123",
        "dimension": DataQualityDimension.COMPLETENESS,
        "config": config,
    }
    return client


@pytest.mark.parametrize(
    "rule_name, asset, custom_sql, threshold_compare_operator, threshold_value, alert_priority, dimension, message",
    [
        (
            None,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            DQ_RULE_CUSTOM_SQL,
            DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL,
            DQ_RULE_THRESHOLD_VALUE,
            DataQualityRuleAlertPriority.NORMAL,
            DataQualityDimension.COMPLETENESS,
            "rule_name is required",
        ),
        (
            DQ_RULE_NAME,
            None,
            DQ_RULE_CUSTOM_SQL,
            DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL,
            DQ_RULE_THRESHOLD_VALUE,
            DataQualityRuleAlertPriority.NORMAL,
            DataQualityDimension.COMPLETENESS,
            "asset is required",
        ),
        (
            DQ_RULE_NAME,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            None,
            DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL,
            DQ_RULE_THRESHOLD_VALUE,
            DataQualityRuleAlertPriority.NORMAL,
            DataQualityDimension.COMPLETENESS,
            "custom_sql is required",
        ),
        (
            DQ_RULE_NAME,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            DQ_RULE_CUSTOM_SQL,
            None,
            DQ_RULE_THRESHOLD_VALUE,
            DataQualityRuleAlertPriority.NORMAL,
            DataQualityDimension.COMPLETENESS,
            "threshold_compare_operator is required",
        ),
        (
            DQ_RULE_NAME,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            DQ_RULE_CUSTOM_SQL,
            DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL,
            None,
            DataQualityRuleAlertPriority.NORMAL,
            DataQualityDimension.COMPLETENESS,
            "threshold_value is required",
        ),
        (
            DQ_RULE_NAME,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            DQ_RULE_CUSTOM_SQL,
            DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL,
            DQ_RULE_THRESHOLD_VALUE,
            None,
            DataQualityDimension.COMPLETENESS,
            "alert_priority is required",
        ),
        (
            DQ_RULE_NAME,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            DQ_RULE_CUSTOM_SQL,
            DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL,
            DQ_RULE_THRESHOLD_VALUE,
            DataQualityRuleAlertPriority.NORMAL,
            None,
            "dimension is required",
        ),
    ],
)
def test_custom_sql_creator_with_missing_parameters_raise_value_error(
    rule_name: str,
    asset,
    custom_sql: str,
    threshold_compare_operator: DataQualityRuleThresholdCompareOperator,
    threshold_value: int,
    alert_priority: DataQualityRuleAlertPriority,
    dimension: DataQualityDimension,
    message: str,
    mock_client,
):
    with pytest.raises(ValueError, match=message):
        DataQualityRule.custom_sql_creator(
            client=mock_client,
            rule_name=rule_name,
            asset=asset,
            custom_sql=custom_sql,
            threshold_compare_operator=threshold_compare_operator,
            threshold_value=threshold_value,
            alert_priority=alert_priority,
            dimension=dimension,
        )


@pytest.mark.parametrize(
    "rule_type, asset, threshold_compare_operator, threshold_value, alert_priority, message",
    [
        (
            None,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL,
            DQ_RULE_THRESHOLD_VALUE,
            DataQualityRuleAlertPriority.NORMAL,
            "rule_type is required",
        ),
        (
            DQ_RULE_TYPE_TABLE,
            None,
            DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL,
            DQ_RULE_THRESHOLD_VALUE,
            DataQualityRuleAlertPriority.NORMAL,
            "asset is required",
        ),
        (
            DQ_RULE_TYPE_TABLE,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            None,
            DQ_RULE_THRESHOLD_VALUE,
            DataQualityRuleAlertPriority.NORMAL,
            "threshold_compare_operator is required",
        ),
        (
            DQ_RULE_TYPE_TABLE,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL,
            None,
            DataQualityRuleAlertPriority.NORMAL,
            "threshold_value is required",
        ),
        (
            DQ_RULE_TYPE_TABLE,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL,
            DQ_RULE_THRESHOLD_VALUE,
            None,
            "alert_priority is required",
        ),
    ],
)
def test_table_level_rule_creator_with_missing_parameters_raise_value_error(
    rule_type: str,
    asset,
    threshold_compare_operator: DataQualityRuleThresholdCompareOperator,
    threshold_value: int,
    alert_priority: DataQualityRuleAlertPriority,
    message: str,
    mock_client,
):
    with pytest.raises(ValueError, match=message):
        DataQualityRule.table_level_rule_creator(
            client=mock_client,
            rule_type=rule_type,
            asset=asset,
            threshold_compare_operator=threshold_compare_operator,
            threshold_value=threshold_value,
            alert_priority=alert_priority,
        )


@pytest.mark.parametrize(
    "rule_type, asset, column, threshold_value, alert_priority, message",
    [
        (
            None,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            Column.ref_by_qualified_name(qualified_name=DQ_COLUMN_QUALIFIED_NAME),
            DQ_RULE_THRESHOLD_VALUE,
            DataQualityRuleAlertPriority.NORMAL,
            "rule_type is required",
        ),
        (
            DQ_RULE_TYPE_COLUMN,
            None,
            Column.ref_by_qualified_name(qualified_name=DQ_COLUMN_QUALIFIED_NAME),
            DQ_RULE_THRESHOLD_VALUE,
            DataQualityRuleAlertPriority.NORMAL,
            "asset is required",
        ),
        (
            DQ_RULE_TYPE_COLUMN,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            None,
            DQ_RULE_THRESHOLD_VALUE,
            DataQualityRuleAlertPriority.NORMAL,
            "column is required",
        ),
        (
            DQ_RULE_TYPE_COLUMN,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            Column.ref_by_qualified_name(qualified_name=DQ_COLUMN_QUALIFIED_NAME),
            None,
            DataQualityRuleAlertPriority.NORMAL,
            "threshold_value is required",
        ),
        (
            DQ_RULE_TYPE_COLUMN,
            Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME),
            Column.ref_by_qualified_name(qualified_name=DQ_COLUMN_QUALIFIED_NAME),
            DQ_RULE_THRESHOLD_VALUE,
            None,
            "alert_priority is required",
        ),
    ],
)
def test_column_level_rule_creator_with_missing_parameters_raise_value_error(
    rule_type: str,
    asset,
    column,
    threshold_value: int,
    alert_priority: DataQualityRuleAlertPriority,
    message: str,
    mock_client,
):
    with pytest.raises(ValueError, match=message):
        DataQualityRule.column_level_rule_creator(
            client=mock_client,
            rule_type=rule_type,
            asset=asset,
            column=column,
            threshold_value=threshold_value,
            alert_priority=alert_priority,
        )


## Change below
def test_table_level_rule_creator(mock_client):
    asset = Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME)

    dq_rule = DataQualityRule.table_level_rule_creator(
        client=mock_client,
        rule_type=DQ_RULE_TYPE_TABLE,
        asset=asset,
        threshold_compare_operator=DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL,
        threshold_value=DQ_RULE_THRESHOLD_VALUE,
        alert_priority=DataQualityRuleAlertPriority.NORMAL,
    )

    assert dq_rule.dq_rule_alert_priority == DataQualityRuleAlertPriority.NORMAL
    assert dq_rule.dq_rule_status == DataQualityRuleStatus.ACTIVE
    assert dq_rule.qualified_name.startswith(f"{DQ_TABLE_QUALIFIED_NAME}/rule/")


def test_custom_sql_creator(mock_client):
    asset = Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME)

    dq_rule = DataQualityRule.custom_sql_creator(
        client=mock_client,
        rule_name=DQ_RULE_NAME,
        asset=asset,
        custom_sql=DQ_RULE_CUSTOM_SQL,
        threshold_compare_operator=DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL,
        threshold_value=DQ_RULE_THRESHOLD_VALUE,
        alert_priority=DataQualityRuleAlertPriority.NORMAL,
        dimension=DataQualityDimension.COMPLETENESS,
    )

    assert dq_rule.dq_rule_custom_s_q_l == DQ_RULE_CUSTOM_SQL
    assert dq_rule.dq_rule_alert_priority == DataQualityRuleAlertPriority.NORMAL
    assert dq_rule.dq_rule_dimension == DataQualityDimension.COMPLETENESS
    assert dq_rule.dq_rule_status == DataQualityRuleStatus.ACTIVE
    assert dq_rule.qualified_name.startswith(f"{DQ_TABLE_QUALIFIED_NAME}/rule/")


def test_custom_sql_creator_with_optional_parameters(mock_client):
    asset = Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME)

    dq_rule = DataQualityRule.custom_sql_creator(
        client=mock_client,
        rule_name=DQ_RULE_NAME,
        asset=asset,
        custom_sql=DQ_RULE_CUSTOM_SQL,
        threshold_compare_operator=DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL,
        threshold_value=DQ_RULE_THRESHOLD_VALUE,
        alert_priority=DataQualityRuleAlertPriority.NORMAL,
        dimension=DataQualityDimension.COMPLETENESS,
        description=DQ_RULE_DESCRIPTION,
    )

    assert dq_rule.dq_rule_custom_s_q_l == DQ_RULE_CUSTOM_SQL
    assert dq_rule.dq_rule_alert_priority == DataQualityRuleAlertPriority.NORMAL
    assert dq_rule.dq_rule_dimension == DataQualityDimension.COMPLETENESS
    assert dq_rule.user_description == DQ_RULE_DESCRIPTION


def test_column_level_rule_creator(mock_client):
    asset = Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME)
    column = Column.ref_by_qualified_name(qualified_name=DQ_COLUMN_QUALIFIED_NAME)

    dq_rule = DataQualityRule.column_level_rule_creator(
        client=mock_client,
        rule_type=DQ_RULE_TYPE_COLUMN,
        asset=asset,
        column=column,
        threshold_value=DQ_RULE_THRESHOLD_VALUE,
        alert_priority=DataQualityRuleAlertPriority.NORMAL,
    )

    assert dq_rule.dq_rule_alert_priority == DataQualityRuleAlertPriority.NORMAL
    assert dq_rule.dq_rule_status == DataQualityRuleStatus.ACTIVE
    assert dq_rule.dq_rule_base_column_qualified_name == DQ_COLUMN_QUALIFIED_NAME
    assert dq_rule.qualified_name.startswith(f"{DQ_TABLE_QUALIFIED_NAME}/rule/")


def test_column_level_rule_creator_with_optional_parameters(mock_client):
    asset = Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME)
    column = Column.ref_by_qualified_name(qualified_name=DQ_COLUMN_QUALIFIED_NAME)

    dq_rule = DataQualityRule.column_level_rule_creator(
        client=mock_client,
        rule_type=DQ_RULE_TYPE_COLUMN,
        asset=asset,
        column=column,
        threshold_value=DQ_RULE_THRESHOLD_VALUE,
        alert_priority=DataQualityRuleAlertPriority.NORMAL,
        threshold_compare_operator=DataQualityRuleThresholdCompareOperator.GREATER_THAN_EQUAL,
        threshold_unit=DataQualityRuleThresholdUnit.PERCENTAGE,
    )

    assert dq_rule.dq_rule_alert_priority == DataQualityRuleAlertPriority.NORMAL
    assert dq_rule.dq_rule_status == DataQualityRuleStatus.ACTIVE
    assert dq_rule.dq_rule_base_column_qualified_name == DQ_COLUMN_QUALIFIED_NAME


def test_column_level_rule_creator_with_row_scope_filtering(mock_client):
    asset = Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME)
    asset.asset_d_q_row_scope_filter_column_qualified_name = DQ_COLUMN_QUALIFIED_NAME
    column = Column.ref_by_qualified_name(qualified_name=DQ_COLUMN_QUALIFIED_NAME)

    dq_rule = DataQualityRule.column_level_rule_creator(
        client=mock_client,
        rule_type=DQ_RULE_TYPE_COLUMN,
        asset=asset,
        column=column,
        threshold_value=DQ_RULE_THRESHOLD_VALUE,
        alert_priority=DataQualityRuleAlertPriority.NORMAL,
        row_scope_filtering_enabled=True,
    )

    assert dq_rule.dq_rule_alert_priority == DataQualityRuleAlertPriority.NORMAL
    assert dq_rule.dq_rule_status == DataQualityRuleStatus.ACTIVE
    assert dq_rule.dq_rule_row_scope_filtering_enabled is True
    assert dq_rule.dq_rule_base_column_qualified_name == DQ_COLUMN_QUALIFIED_NAME


def test_column_level_rule_creator_with_rule_conditions(mock_client):
    asset = Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME)
    column = Column.ref_by_qualified_name(qualified_name=DQ_COLUMN_QUALIFIED_NAME)

    rule_conditions = (
        DQRuleConditionsBuilder()
        .add_condition(
            type=DataQualityRuleTemplateConfigRuleConditions.STRING_LENGTH_BETWEEN,
            min_value=5,
            max_value=50,
        )
        .build()
    )

    dq_rule = DataQualityRule.column_level_rule_creator(
        client=mock_client,
        rule_type=DQ_RULE_TYPE_COLUMN,
        asset=asset,
        column=column,
        threshold_value=DQ_RULE_THRESHOLD_VALUE,
        alert_priority=DataQualityRuleAlertPriority.NORMAL,
        rule_conditions=rule_conditions,
    )

    assert dq_rule.dq_rule_alert_priority == DataQualityRuleAlertPriority.NORMAL
    assert dq_rule.dq_rule_status == DataQualityRuleStatus.ACTIVE
    assert (
        dq_rule.dq_rule_config_arguments.dq_rule_config_rule_conditions
        == rule_conditions
    )
    assert dq_rule.dq_rule_base_column_qualified_name == DQ_COLUMN_QUALIFIED_NAME


def test_validate_template_features_rule_conditions_not_supported(mock_client):
    config = Mock()
    config.dq_rule_template_config_rule_conditions = None
    config.dq_rule_template_config_advanced_settings = json.dumps({})

    template_config = {
        "name": "Test Template",
        "qualified_name": "test/template/123",
        "config": config,
    }

    mock_client.dq_template_config_cache.get_template_config.return_value = (
        template_config
    )

    rule_conditions = (
        DQRuleConditionsBuilder()
        .add_condition(
            type=DataQualityRuleTemplateConfigRuleConditions.STRING_LENGTH_BETWEEN,
            min_value=5,
            max_value=50,
        )
        .build()
    )

    with pytest.raises(
        InvalidRequestError,
        match="Rule type 'Blank Count' does not support rule conditions",
    ):
        DataQualityRule.Attributes._validate_template_features(
            rule_type="Blank Count",
            rule_conditions=rule_conditions,
            row_scope_filtering_enabled=False,
            template_config=template_config,
            threshold_compare_operator=DataQualityRuleThresholdCompareOperator.EQUAL,
        )


def test_validate_template_features_row_scope_filtering_not_supported(mock_client):
    config = Mock()
    config.dq_rule_template_config_rule_conditions = json.dumps(
        {"enum": ["STRING_LENGTH_BETWEEN"]}
    )
    config.dq_rule_template_config_advanced_settings = json.dumps({})

    template_config = {
        "name": "Test Template",
        "qualified_name": "test/template/123",
        "config": config,
    }

    mock_client.dq_template_config_cache.get_template_config.return_value = (
        template_config
    )

    with pytest.raises(
        InvalidRequestError,
        match="Rule type 'Blank Count' does not support row scope filtering",
    ):
        DataQualityRule.Attributes._validate_template_features(
            rule_type="Blank Count",
            rule_conditions=None,
            row_scope_filtering_enabled=True,
            template_config=template_config,
            threshold_compare_operator=DataQualityRuleThresholdCompareOperator.EQUAL,
        )


@pytest.mark.parametrize(
    "qualified_name, message",
    [
        (None, "qualified_name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, message: str, mock_client
):
    with pytest.raises(ValueError, match=message):
        DataQualityRule.updater(
            client=mock_client,
            qualified_name=qualified_name,
        )


def test_validate_template_features_invalid_rule_conditions(mock_client):
    config = Mock()
    config.dq_rule_template_config_rule_conditions = json.dumps(
        {"enum": ["STRING_LENGTH_BETWEEN"]}
    )
    config.dq_rule_template_config_advanced_settings = json.dumps({})

    template_config = {
        "name": "Test Template",
        "qualified_name": "test/template/123",
        "config": config,
    }

    mock_client.dq_template_config_cache.get_template_config.return_value = (
        template_config
    )

    unsupported_condition = json.dumps(
        {"conditions": [{"type": "UNSUPPORTED_CONDITION", "value": "test"}]}
    )

    with pytest.raises(
        InvalidRequestError,
        match="Invalid rule conditions: condition type 'UNSUPPORTED_CONDITION' not supported, allowed: \\['STRING_LENGTH_BETWEEN'\\]",
    ):
        DataQualityRule.Attributes._validate_template_features(
            rule_type="Test Rule",
            rule_conditions=unsupported_condition,
            row_scope_filtering_enabled=False,
            template_config=template_config,
            threshold_compare_operator=DataQualityRuleThresholdCompareOperator.EQUAL,
        )


def test_validate_template_features_row_scope_filter_column_missing(mock_client):
    config = Mock()
    config.dq_rule_template_config_rule_conditions = json.dumps(
        {"enum": ["STRING_LENGTH_BETWEEN"]}
    )
    config.dq_rule_template_config_advanced_settings = json.dumps(
        {"dqRuleRowScopeFilteringEnabled": True}
    )

    template_config = {
        "name": "Test Template",
        "qualified_name": "test/template/123",
        "config": config,
    }

    mock_client.dq_template_config_cache.get_template_config.return_value = (
        template_config
    )

    table_asset = Table.ref_by_qualified_name(qualified_name=DQ_TABLE_QUALIFIED_NAME)

    with pytest.raises(
        InvalidRequestError,
        match=ErrorCode.DQ_ROW_SCOPE_FILTER_COLUMN_MISSING.error_message.format(
            DQ_TABLE_QUALIFIED_NAME
        ),
    ):
        DataQualityRule.Attributes._validate_template_features(
            rule_type="Test Rule",
            rule_conditions=None,
            row_scope_filtering_enabled=True,
            template_config=template_config,
            threshold_compare_operator=DataQualityRuleThresholdCompareOperator.EQUAL,
            asset=table_asset,
        )
