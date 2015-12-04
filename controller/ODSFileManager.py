from lxml import etree as xml_tree_parser
import lxml
import os.path
import sys
import zipfile
import logging
import time

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

        # TODO: Retrieve latest file from the local directory until
        # such time it is published and retrievable
        if os.path.isfile('data/HSCOrgRefData_Full_20151130.xml.zip'):
            return 'data/HSCOrgRefData_Full_20151130.xml.zip'
        # if os.path.isfile('data/test.xml.zip'):
        #     return 'data/test.xml.zip'
        else:
            raise ValueError('unable to locate the data file')


    def retrieve_latest_schema(self):
        """Get the latest XSD for the ODS XML data and return it as an XMLSchema object

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
                # TODO: this is a horrible impementation
                data_filename = data_filename.replace('.zip', '')
                data_filename = data_filename.split('/', 1)
                data_filename = data_filename[1]

                with local_zipfile.open(data_filename) as local_datafile:
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
            self.__ods_schema = self.retrieve_latest_schema()

        if self.__ods_xml_data is None:
            data_filename = self.__retrieve_latest_datafile()
            self.__import_latest_datafile(data_filename)
            self.__validate_xml_against_schema()

        return self.__ods_xml_data
