import os.path
import sys
import unittest
import sys
import os.path
from distutils import file_util

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from controller.ODSFileManager import ODSFileManager

File_manager = ODSFileManager()
Src_file = 'data/odsfull.xml.zip'
Dst_file = 'controller/odsfull.xml.zip'


class ods_file_manager_test(unittest.TestCase):

    __ods_xml_data = None

    def setUp(self):
        self.__ods_xml_data = None

    def test_local_file_available(self):

        file_util.copy_file(Src_file,
                            Dst_file, update=True)

        __ods_xml_data__ = File_manager.get_latest_xml()
        self.assertIs(None, self.__ods_xml_data, False)

    def test_newer_remote_file_available(self):
        pass

    def test_not_zip_file(self):
        pass

    def test_zip_file_invalid(self):
        pass

    def test_schema_invalid(self):
        pass

    def tearDownClass():
        os.remove(Dst_file)


if __name__ == '__main__':
    unittest.main()
