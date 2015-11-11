from lxml import etree as xml_tree_parser
import os.path
import zipfile
import sys


class OdsXml2SQL(object):

    __ods_xml_data = None
    __database_connection = None

    def __init__(self, database_connection):
        self.__database_connection = database_connection

    def __return_attribute(self, attribute_name):
        pass

    # The purpose of this function is to retrieve the latest published
    # file from a public published location
    def __retrieve_latest_datafile(self):
        # TODO: Retrieve latest file from the local directory until
        # such time it is published and retrievable
        if os.path.isfile('odsfull.xml.zip'):
            return "odsfull.xml.zip"
        else:
            raise ValueError("unable to locate the data file")

    # The purpose of this function is to determine if we have a zip
    # for or xml file, check it is valid
    # and then populate an etree object for us to parse
    # TODO: validate the xml file against a schema
    def __import_latest_datafile(self, data_filename):

        try:
            with zipfile.ZipFile(data_filename) as local_zipfile:
                data_filename = data_filename.replace("zip", "")
                with local_zipfile.open(data_filename) as local_datafile:
                    self.__ods_xml_data = xml_tree_parser.parse(local_datafile)
                return True
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
