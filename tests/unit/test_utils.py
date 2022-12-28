from pyatlan.utils import list_attributes_to_params


def test_list_attributes_to_params_with_no_query_parms():
    assert list_attributes_to_params([{"first": "Dave"}]) == {"attr_0:first": "Dave"}


def test_list_attributes_to_params_with_query_parms():
    assert list_attributes_to_params([{"first": "Dave"}], {"last": "Jo"}) == {
        "attr_0:first": "Dave",
        "last": "Jo",
    }
