from lxml import etree as xml_tree_parser
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os.path
import sys
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.Addresses import Addresses
from controller.ODSFileManager import ODSFileManager
import zipfile

# Logging Setup
log = logging.getLogger('import_ods_xml')
log.setLevel(logging.DEBUG)


engine = create_engine('sqlite:///openods.db', echo=True)
Base = declarative_base(engine)
metadata = Base.metadata
File_Manager = ODSFileManager()
Session = sessionmaker(bind=engine)
session = Session()


class DataBaseSetup(object):

    __ods_xml_data = None

    def __init__(self):
        pass

    def __create_addresses(self):

        address = Addresses()

        #metadata.create_all(engine)

        address.organisation_ref = 123
        address.org_odscode = '123test'
        address.street_address_line1 = '123test'
        address.street_address_line2 = '123test'
        address.street_address_line3 = '123test'
        address.town = '123test'
        address.county = '123test'
        address.postal_code = '123test'
        address.location_id = '123test'
        log.info(address)
        #session.add(address)
        #session.commit()

    def create_database(self):
        self.__create_addresses()

if __name__ == '__main__':
    DataBaseSetup().create_database()
