from lxml import etree as xml_tree_parser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os.path
import sys
import time
import zipfile

# setup path so we can import our own models and controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


# import controllers
from controller.ODSFileManager import ODSFileManager

# import models
from models.Addresses import Addresses
from models.base import Base
from models.CodeSystem import CodeSystem
from models.Organisation import Organisation
from models.Relationship import Relationship
from models.Role import Role
from models.Settings import Settings
from models.Versions import Versions

# Logging Setup
log = logging.getLogger('import_ods_xml')
log.setLevel(logging.DEBUG)

# We need a filemanager to bring the xml data tree structure in
File_manager = ODSFileManager()

# SQLAlchemy objects
engine = create_engine('sqlite:///openods.sqlite', echo=False)
metadata = Base.metadata
Session = sessionmaker(bind=engine)
session = Session()


class DataBaseSetup(object):

    __ods_xml_data = None
    __version = Versions()
    __code_system_dict = {}

    def __init__(self):
        # Creates the tables of all objects derived from our Base object
        metadata.create_all(engine)

    def __create_settings(self):

        codesystem = CodeSystem()

        session.add(codesystem)

    def __create_codesystems(self):
        """Loops through all the code systems in an organisation and adds them
        to the database

        Parameters
        ----------
        None
        Returns
        -------
        None
        """

        # these are all code systems, we have a DRY concept here as so much of
        # this code is common, it doesn't make sense to do it 3 times, lets
        # loop
        code_system_types = [
            './CodeSystems/CodeSystem[@name="OrganisationRelationship"]',
            './CodeSystems/CodeSystem[@name="OrganisationRecordClass"]',
            './CodeSystems/CodeSystem[@name="OrganisationRole"]']

        for code_system_type in code_system_types:
            # we are going to need to append a lot of data into this array
            codesystems = {}

            relationships = self.__ods_xml_data.find(code_system_type)
            relationship_types = {}

            # enumerate the iter as it doesn't provide an index which we need
            for idx, relationship in enumerate(relationships.iter('concept')):

                codesystems[idx] = CodeSystem()

                relationship_id = relationship.attrib.get('id')
                display_name = relationship.attrib.get('displayName')
                relationship_types[relationship_id] = display_name

                code_system_type_name = code_system_type
                code_system_type_name = code_system_type_name.replace(
                    './CodeSystems/CodeSystem[@name="', '').replace('"]', '')

                codesystems[idx].id = relationship_id
                codesystems[idx].name = code_system_type_name
                codesystems[idx].displayname = display_name

                # pop these in a global dictionary, we will use these later in
                # __create_organisations
                self.__code_system_dict[relationship_id] = display_name

                # append this instance of code system to the session
                session.add(codesystems[idx])

            codesystems = None

    def __create_organisations(self):
        """Creates the organisations and adds them to the session

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        organisations = {}

        for idx, organisation in enumerate(self.__ods_xml_data.findall(
                '.Organisations/Organisation')):

            organisations[idx] = Organisation()

            organisations[idx].odscode = organisation.find(
                'OrgId').attrib.get('extension')

            organisations[idx].name = organisation.find('Name').text

            organisations[idx].status = organisation.find(
                'Status').attrib.get('value')

            organisations[idx].record_class = self.__code_system_dict[
                organisation.attrib.get('orgRecordClass')]

            organisations[idx].last_changed = organisation.find(
                'LastChangeDate').attrib.get('value')

            session.add(organisations[idx])

            self.__create_roles(organisations[idx], organisation)

            self.__create_relationships(organisations[idx], organisation)

        organisations = None

    def __create_roles(self, organisation, organisation_xml):
        """Creates the roles, this should only be called from
         __create_organisations()

        Parameters
        ----------
        organisation = xml element of the full organisation

        Returns
        -------
        None
        """
        roles_xml = organisation_xml.find('Roles')
        roles = {}

        for idx, role in enumerate(roles_xml):

            roles[idx] = Role()

            roles[idx].organisation_ref = organisation.ref
            roles[idx].org_odscode = organisation.odscode
            roles[idx].code = role.attrib.get('id')

            session.add(roles[idx])

        roles = None

    def __create_relationships(self, organisation, organisation_xml):
        """Creates the relationships, this should only be called from
         __create_organisations()

        Parameters
        ----------
        organisation = xml element of the full organisation

        Returns
        -------
        None
        """
        relationships_xml = organisation_xml.find('Rels')
        relationships = {}

        for idx, relationship in enumerate(relationships_xml):

            relationships[idx] = Relationship()

            relationships[idx].organisation_ref = organisation.ref
            relationships[idx].org_odscode = organisation.odscode
            relationships[idx].code = relationship.attrib.get('id')
            relationships[idx].target_odscode = self.__code_system_dict[
                relationships[idx].code]

            session.add(relationships[idx])

        relationships = None

    def __create_addresses(self):

        pass
        # address = Addresses()

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
        """adds all the version information to the versions table

        Parameters
        ----------
        None
        Returns
        -------
        None
        """
        # TODO: Change to local variable from private class variable
        self.__version.file_version = self.__ods_xml_data.find(
            './Manifest/Version').attrib.get('value')
        self.__version.publication_date = self.__ods_xml_data.find(
            './Manifest/PublicationDate').attrib.get('value')
        self.__version.publication_type = self.__ods_xml_data.find(
            './Manifest/PublicationType').attrib.get('value')
        self.__version.publication_seqno = self.__ods_xml_data.find(
            './Manifest/PublicationSeqNum').attrib.get('value')

        session.add(self.__version)

    def create_database(self, ods_xml_data):
        """creates a sqlite database in the current path with all the data

        Parameters
        ----------
        ods_xml_data: xml_tree_parser object required that is valid
        TODO: check validity here
        Returns
        -------
        None
        """

        self.__ods_xml_data = ods_xml_data
        if self.__ods_xml_data is not None:
            try:
                self.__create_addresses()
                self.__create_version()
                self.__create_codesystems()
                self.__create_organisations()

                session.commit()
            except:
                # If anything fails, let's not commit anything
                session.rollback()
            finally:
                session.close()

if __name__ == '__main__':
    # get the latest xml data and get it into an xmltree object
    start_time = time.time()
    log.info('Starting data import...')

    ods_xml_data = File_manager.get_latest_xml()
    DataBaseSetup().create_database(ods_xml_data)

    log.info('Data Import Time = %s', time.strftime(
        "%H:%M:%S", time.gmtime(time.time() - start_time)))
