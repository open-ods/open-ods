import unittest

from openods.openods_core import db


class DBTests(unittest.TestCase):

    def test_none_type_method_removes_none_types(self):
        dirty_dictionary = {
            'value1': 'value1',
            'should_be_removed': None
        }

        clean_dictionary = {
            'value1': 'value1',
        }

        self.assertDictEqual(db.remove_none_values_from_dictionary(dirty_dictionary), clean_dictionary)
