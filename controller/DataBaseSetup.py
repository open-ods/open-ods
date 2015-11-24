from lxml import etree as xml_tree_parser
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import models.*


import os.path
import sys
import zipfile

engine = create_engine('sqlite:///openods.db', echo=True)
Base = declarative_base(engine)
metadata = Base.metadata


class DataBaseSetup(object):

    __ods_xml_data = None

    def __init__(self):
        pass

    def create_addresses(self):

        address = Addresses()

        address.organisation_ref = '123test'
        address.org_odscode = Column('123test'
        address.street_address_line1 = '123test'
        address.street_address_line2 = '123test'
        address.street_address_line3 = '123test'
        address.town = '123test'
        address.county = '123test'
        address.postal_code = '123test'
        address.location_id = '123test'

    def create_database(self):
        pass
