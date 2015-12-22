from lxml import etree as xml_tree_parser
import logging
import os.path
import sys
import urllib.request
import zipfile

log = logging.getLogger('import_ods_xml')

# # setup path so we can import our own models and controllers
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class ODSFileManager(object):

    __ods_xml_data = None
    __ods_schema = None

    def __init__(self, xml_file_path, schema_file_path, xml_url=None):
        try:
            self.xml_file_path = xml_file_path
            log.debug('xml_file_path is %s' % self.xml_file_path)

            self.schema_file_path = schema_file_path
            log.debug('schema_file_path is %s' % self.schema_file_path)

            # If the xml_url has been passed in to the constructor, we will retrieve the zip file from the remote url
            if xml_url:
                self.__local_mode = False
                self.xml_url = xml_url
                log.debug('xml_url is %s' % self.xml_url)

            # Otherwise we will set local_mode which will skip the download and just look for the zip file locally
            else:
                self.__local_mode = True

        except Exception as e:
            log.error(e)

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

        file_name = self.xml_file_path
        tmp_file_name = str.format("%s.tmp" % file_name)

        # If we are not running in local mode, we attempt to download the latest zip file first
        if not self.__local_mode:
            url = self.xml_url

            with urllib.request.urlopen(url) as response:
                # Download the file and save it to a temporary file name
                with open(tmp_file_name, 'wb') as out_file:
                    log.info("Downloading data")
                    out_file.write(response.read())

                    # Check that the temporary file has downloaded properly
                    if os.path.isfile(tmp_file_name):
                        # If the data file already exists, remove it
                        if os.path.isfile(file_name):
                            os.remove(file_name)
                        # Rename the temporary download file to the xml file name
                        os.rename(tmp_file_name, file_name)
                        log.info("Download complete")
                        return file_name
                    else:
                        raise ValueError('Unable to locate the data file')

        # Otherwise we simply check that the zip file is already there locally and return the file name
        else:
            if os.path.isfile(file_name):
                return file_name

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
            with open(self.schema_file_path) as f:
                doc = xml_tree_parser.parse(f)
                return xml_tree_parser.XMLSchema(doc)

        except Exception as e:
            raise

    # The purpose of this function is to determine if we have a zip
    # for or xml file, check it is valid
    # and then populate an etree object for us to parse
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
                    log.debug("Loading data")
                    self.__ods_xml_data = xml_tree_parser.parse(local_datafile)

        except:
            print('Unexpected error:', sys.exc_info()[0])
            raise

    def __validate_xml_against_schema(self):
        try:

            log.debug("Validating data against schema")

            doc = self.__ods_xml_data
            schema = self.__ods_schema
            valid = schema.validate(doc)

            if not valid:
                raise Exception("XML file is not valid against the schema")

            else:
                log.debug("Data is valid against schema")
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
