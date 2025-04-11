import pytest

from pyatlan.model.assets import DocumentDB


def test_type_name():
    sut = DocumentDB()
    assert sut.type_name == "DocumentDB"


def test_type_name_is_immutable():
    sut = DocumentDB()
    with pytest.raises(TypeError):
        sut.type_name = "Invalid"
