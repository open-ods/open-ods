import pytest


@pytest.mark.xfail()
def test_method_converts_dict_to_piped_kv_pairs():
    from openods import request_utils
    input_dict = {
        'q': 'search term',
        'limit': 1000,
        'postCode': 'AB13DF'
    }
    result = request_utils.dict_to_piped_kv_pairs(input_dict)
    assert result == 'limit=1000|postCode=AB13DF|q=search term|'
