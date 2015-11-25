from distutils import file_util
from lxml import etree as xml_tree_parser
import logging
import os.path
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from controller.ODSFileManager import ODSFileManager

# Logging Setup
log = logging.getLogger('import_ods_xml')
log.setLevel(logging.DEBUG)


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

        self.__ods_xml_data = File_manager.get_latest_xml()
        self.assertTrue(self.__ods_xml_data)
        log.info(self.__ods_xml_data
                 .find('./Manifest/Version')
                 .attrib.get('value'))

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
