import argparse
from sqlalchemy import create_engine
import logging
import time

from controller.ODSDBCreator import ODSDBCreator
from controller.ODSFileManager import ODSFileManager

# Set up logging
log = logging.getLogger('import_ods_xml')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

# Set up the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbose", action="store_true",
                    help="run the import in verbose mode")
parser.add_argument("-d", "--dbms", choices=["sqlite", "postgres"],
                    help="the DBMS to use (defaults to SQLite)")
parser.add_argument("-l", "--local", action="store_true",
                    help="skip the XML data file download and use a local copy")
parser.add_argument("-x", "--xml", type=str,
                    help="specify the path to the local XML data file")
parser.add_argument("-s", "--schema", type=str,
                    help="specify the path to the local XSD schema file")
parser.add_argument("-u", "--url", type=str,
                    help="specify the url to the official XML data file")
parser.add_argument("-c", "--connection", type=str,
                    help="specify the connection string for the database engine")

args = parser.parse_args()

# Set the logging level based on --verbose parameter
if args.verbose:
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)

# Set local mode based on command line parameters
local_mode = args.local

# Set the XML file path if specified, otherwise use default
if args.xml:
    xml_file_path = args.xml
    log.debug("XML parameter provided: %s" % xml_file_path)
else:
    xml_file_path = 'data/fullfile.zip'

# Set the schema file path if specified, otherwise use default
if args.schema:
    schema_file_path = args.schema
    log.debug("Schema parameter provided: %s" % schema_file_path)
else:
    schema_file_path = 'data/HSCOrgRefData.xsd'

# Set the schema file path if specified, otherwise use default
if args.url:
    url_path = args.url
    log.debug("URL parameter provided: %s" % url_path)
else:
    url_path = 'http://systems.hscic.gov.uk/data/ods/interfacechanges/fullfile.zip'

# Set the connection string using command line parameter
if args.connection:
    connection_string = args.connection
    log.debug("Connection parameter provided: %s" % connection_string)
else:
    connection_string = None

log.debug("Running in verbose mode")

if local_mode:
    log.debug("Running in local mode")

    # Instantiate an instance of the ODSFileManager to get us the validated XML data to work with
    File_manager = ODSFileManager(xml_file_path=xml_file_path,
                                  schema_file_path=schema_file_path)
else:
    log.debug("Running in download mode")
    # Instantiate an instance of the ODSFileManager to get us the validated XML data to work with
    File_manager = ODSFileManager(xml_file_path=xml_file_path,
                                  schema_file_path=schema_file_path,
                                  xml_url=url_path)
    

def get_engine():

    # Create the SQLAlchemy engine based on command line parameter (default to sqlite)
    log.debug("Creating SQLAlchemy engine")

    if args.dbms == "sqlite":
        log.debug("Using SQLite")
        engine = create_engine(connection_string or 'sqlite:///openods.sqlite', echo=False)

    elif args.dbms == "postgres":
        log.debug("Using PostgreSQL")
        engine = create_engine(connection_string or "postgresql://openods:openods@localhost/openods", isolation_level="READ UNCOMMITTED")

    elif args.dbms is None:
        log.debug("No DBMS specified - using SQLite")
        engine = create_engine(connection_string or 'sqlite:///openods.sqlite', echo=False)

    return engine


if __name__ == '__main__':
    total_start_time = time.time()
    ods_xml_data = File_manager.get_latest_xml()
    log.debug('Data Load Time = %s', time.strftime(
        "%H:%M:%S", time.gmtime(time.time() - total_start_time)))

    engine = get_engine()

    import_start_time = time.time()
    ODSDBCreator(engine).create_database(ods_xml_data)
    log.debug('Data Import Time = %s', time.strftime(
        "%H:%M:%S", time.gmtime(time.time() - import_start_time)))

    log.debug('Total Time = %s', time.strftime(
        "%H:%M:%S", time.gmtime(time.time() - total_start_time)))

