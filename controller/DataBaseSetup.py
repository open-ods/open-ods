from lxml import etree as xml_tree_parser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os.path
import sys
import zipfile

# setup path so we can import our own models and controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


# import controllers
from controller.ODSFileManager import ODSFileManager

# import models
from models.Addresses import Addresses
from models.Versions import Versions
from models.Organisation import Organisation
from models.Relationship import Relationship
from models.CodeSystem import CodeSystem
from models.Role import Role
from models.Settings import Settings
from models.base import Base

# Logging Setup
log = logging.getLogger('import_ods_xml')
log.setLevel(logging.DEBUG)

# We need a filemanager to bring the xml data tree structure in
File_manager = ODSFileManager()

# SQLAlchemy objects
engine = create_engine('sqlite:///openods.sqlite', echo=True)
metadata = Base.metadata
Session = sessionmaker(bind=engine)
session = Session()


class DataBaseSetup(object):

    __ods_xml_data = None
    __version = Versions()

    def __init__(self):
        metadata.create_all(engine)

    def __create_settings(self):

        codesystem = CodeSystem()

        session.add(codesystem)

    def __create_roles(self):

        role = Role()

        session.add(role)

    def __create_codesystems(self):

        # we are going to need to append a lot of data into this array
        codesystems = {}

        relationships = self.__ods_xml_data.find(
            './CodeSystems/CodeSystem[@name="OrganisationRelationship"]')
        relationship_types = {}

        # enumerate the iter as it doesn't provide an index which we need
        for idx, relationship in enumerate(relationships.iter('concept')):
            log.info(idx)
            codesystems[idx] = CodeSystem()

            relationship_id = relationship.attrib.get('id')
            display_name = relationship.attrib.get('displayName')
            relationship_types[relationship_id] = display_name

            codesystems[idx].id = relationship_id
            codesystems[idx].name = 'OrganisationRelationship'
            codesystems[idx].displayname = display_name

            # append this instance of code system to the session
            session.add(codesystems[idx])

    def __create_organisations(self):
        pass
        # organisation = Organisation()

        # for node in
        # self.__ods_xml_data.findall('.Organisations/Organisation'):

        #     organisation.odscode = node.find(
        #         'OrgId').attrib.get('extension')
        #     organisation.name = node.find('Name').text
        #     organisation.status = node.find('Status').attrib.get('value')
        #     organisation.record_class = record_classes[
        #         node.attrib.get('orgRecordClass')]
        #     organisation.last_changed = node.find(
        #         'LastChangeDate').attrib.get('value')

        # session.add(organisation)

    def __create_relationships(self):
        pass
        # relationship = Relationship()

        # session.add(relationship)

    def __create_addresses(self):
        pass
        #address = Addresses()

        # address.organisation_ref = 123
        # address.org_odscode = '123test'
        # address.street_address_line1 = '123test'
        # address.street_address_line2 = '123test'
        # address.street_address_line3 = '123test'
        # address.town = '123test'
        # address.county = '123test'
        # address.postal_code = '123test'
        # address.location_id = '123test'

        # session.add(address)

    def __create_version(self):

        self.__version.file_version = self.__ods_xml_data.find(
            './Manifest/Version').attrib.get('value')
        self.__version.publication_date = self.__ods_xml_data.find(
            './Manifest/PublicationDate').attrib.get('value')
        self.__version.publication_type = self.__ods_xml_data.find(
            './Manifest/PublicationType').attrib.get('value')
        self.__version.publication_seqno = self.__ods_xml_data.find(
            './Manifest/PublicationSeqNum').attrib.get('value')

        session.add(self.__version)

    # expects and xmltree object
    def create_database(self, ods_xml_data):
        self.__ods_xml_data = ods_xml_data
        if self.__ods_xml_data is not None:

            self.__create_addresses()
            self.__create_version()
            self.__create_organisations()
            self.__create_codesystems()
            session.commit()

if __name__ == '__main__':
    # get the latest xml data and get it into an xmltree object
    ods_xml_data = File_manager.get_latest_xml()
    DataBaseSetup().create_database(ods_xml_data)
