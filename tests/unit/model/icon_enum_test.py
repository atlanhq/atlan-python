"""Tests for AtlanIcon enum — deprecated Phosphor icon backward compat (BLDX-1096)."""

import pytest

from pyatlan.model.enums import AtlanIcon

# Mapping of deprecated enum names to their string values
DEPRECATED_ICONS = {
    "ACTIVITY": "PhActivity",
    "CIRCLE_WAVY": "PhCircleWavy",
    "CIRCLE_WAVY_CHECK": "PhCircleWavyCheck",
    "CIRCLE_WAVY_QUESTION": "PhCircleWavyQuestion",
    "CIRCLE_WAVY_WARNING": "PhCircleWavyWarning",
    "FILE_DOTTED": "PhFileDotted",
    "FILE_SEARCH": "PhFileSearch",
    "FOLDER_DOTTED": "PhFolderDotted",
    "FOLDER_SIMPLE_DOTTED": "PhFolderSimpleDotted",
    "PEDESTRIAN": "PhPedestrian",
    "TEXT_BOLDER": "PhTextBolder",
}

# Mapping of deprecated → replacement enum names
REPLACEMENT_MAP = {
    "ACTIVITY": "PULSE",
    "CIRCLE_WAVY": "SEAL",
    "CIRCLE_WAVY_CHECK": "SEAL_CHECK",
    "CIRCLE_WAVY_QUESTION": "SEAL_QUESTION",
    "CIRCLE_WAVY_WARNING": "SEAL_WARNING",
    "FILE_DOTTED": "FILE_DASHED",
    "FILE_SEARCH": "FILE_MAGNIFYING_GLASS",
    "FOLDER_DOTTED": "FOLDER_DASHED",
    "FOLDER_SIMPLE_DOTTED": "FOLDER_SIMPLE_DASHED",
    "PEDESTRIAN": "PERSON",
    "TEXT_BOLDER": "TEXT_B",
}


class TestDeprecatedIconsExist:
    """All deprecated Phosphor icon names must be valid AtlanIcon enum members."""

    @pytest.mark.parametrize("name,value", DEPRECATED_ICONS.items())
    def test_deprecated_icon_exists_in_enum(self, name, value):
        icon = AtlanIcon[name]
        assert icon.value == value

    @pytest.mark.parametrize("name,value", DEPRECATED_ICONS.items())
    def test_deprecated_icon_deserializes_from_value(self, name, value):
        """Simulates deserialization — looking up by string value."""
        icon = AtlanIcon(value)
        assert icon.name == name


class TestReplacementIconsExist:
    """Each deprecated icon has a valid replacement in the enum."""

    @pytest.mark.parametrize("deprecated,replacement", REPLACEMENT_MAP.items())
    def test_replacement_exists(self, deprecated, replacement):
        assert replacement in AtlanIcon.__members__

    @pytest.mark.parametrize("deprecated,replacement", REPLACEMENT_MAP.items())
    def test_deprecated_and_replacement_are_different_values(
        self, deprecated, replacement
    ):
        """Deprecated and replacement icons have different string values."""
        assert AtlanIcon[deprecated].value != AtlanIcon[replacement].value


class TestIconEnumIntegrity:
    """General enum health checks."""

    def test_no_duplicate_values(self):
        """All enum values must be unique."""
        values = [icon.value for icon in AtlanIcon]
        assert len(values) == len(set(values)), "Duplicate values found in AtlanIcon"

    def test_all_values_are_non_empty(self):
        """All AtlanIcon values must be non-empty strings."""
        for icon in AtlanIcon:
            assert icon.value, f"{icon.name} has empty value"
