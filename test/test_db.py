import unittest

from app.openods_core import db


class DBTests(unittest.TestCase):

    def test_none_type_method_removes_none_types(self):
        dict = {
            'value1': 'value1',
            'should_be_removed': None
        }

        new_dict = db.remove_none_values_from_dictionary(dict)

        target_dict = {
            'value1': 'value1',
        }
        self.assertDictEqual(new_dict, target_dict)

