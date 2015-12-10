from distutils import file_util
from lxml import etree as xml_tree_parser
import logging
import lxml
import os.path
import sys
import time
import urllib.request
import zipfile

log = logging.getLogger('import_ods_xml')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
log.addHandler(ch)


class ODSFileManager(object):

    __ods_xml_data = None
    __ods_schema = None

    def __init__(self):
        pass

    def __return_attribute(self, attribute_name):
        pass

    def __retrieve_latest_datafile(self):
        """The purpose of this function is to retrieve the latest
        published file from a public published location

        Parameters
        ----------
        None
        Returns
        -------
        String: Filename if found
        """

        url = "http://systems.hscic.gov.uk/data/ods/" \
            "interfacechanges/fullfile.zip"

        file_name = 'data/fullfile.zip'

        with urllib.request.urlopen(url) as response:
            with open(file_name, 'wb') as out_file:
                log.info("Retrieving data")
                out_file.write(response.read())

                if os.path.isfile(file_name):
                    return file_name
                else:
                    raise ValueError('unable to locate the data file')

    def __retrieve_latest_schema(self):
        """Get the latest XSD for the ODS XML data and return it as an
        XMLSchema object

        Parameters
        ----------
        None

        Returns
        -------
        xml_schema: the ODS XSD as an XMLSchema object
        """
        # TODO: Retrieve latest schema file from the local directory until
        # such time it is published and retrievable
        try:
            with open('data/HSCOrgRefData.xsd') as f:
                doc = xml_tree_parser.parse(f)
                return xml_tree_parser.XMLSchema(doc)

        except Exception as e:
            raise

    # The purpose of this function is to determine if we have a zip
    # for or xml file, check it is valid
    # and then populate an etree object for us to parse
    # TODO: validate the xml file against a schema
    def __import_latest_datafile(self, data_filename):
        """The purpose of this function is to determine if we have a zip
        for or xml file, check it is valid

        Parameters
        ----------
        String: filename of the zip file containing the xml
        Returns
        -------
        None
        """

        try:
            with zipfile.ZipFile(data_filename) as local_zipfile:
                # get to the name of the actual zip file
                zip_info = local_zipfile.namelist()

                # extract the first file in the zip, assumption there will be
                # only one
                with local_zipfile.open(zip_info[0]) as local_datafile:
                    self.__ods_xml_data = xml_tree_parser.parse(local_datafile)

        except:
            print('Unexpected error:', sys.exc_info()[0])
            raise

    def __validate_xml_against_schema(self):
        try:
            doc = self.__ods_xml_data
            schema = self.__ods_schema
            valid = schema.validate(doc)

            if not valid:
                raise Exception("XML file is not valid against the schema")

            else:
                return valid

        except Exception as e:
            raise
            sys.exit(1)

    def get_latest_xml(self):
        """The purpose of this function is to check if we have odsxml data
        if we don't it should retrieve the latest version available and
        explode it from zip format into a xmltree object

        Parameters
        ----------
        None
        Returns
        -------
        xml_tree_parser: containing the entire xml dataset
        """

        if self.__ods_schema is None:
            self.__ods_schema = self.__retrieve_latest_schema()

        if self.__ods_xml_data is None:
            data_filename = self.__retrieve_latest_datafile()
            self.__import_latest_datafile(data_filename)
            self.__validate_xml_against_schema()

        log.info("Data loaded")
        return self.__ods_xml_data
