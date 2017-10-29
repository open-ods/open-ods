import pytest


@pytest.mark.xfail()
def test_none_type_method_removes_none_types():
    from openods import db

    dirty_dictionary = {
        'value1': 'value1',
        'should_be_removed': None
    }

    clean_dictionary = {
        'value1': 'value1',
    }

    assert db.remove_none_values_from_dictionary(dirty_dictionary) == clean_dictionary
