#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os.path
import sys
import datetime
import time

# setup path so we can import our own models and controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# import controllers
from controller.ODSFileManager import ODSFileManager

# import models
from models.Address import Address
from models.base import Base
from models.CodeSystem import CodeSystem
from models.Organisation import Organisation
from models.Relationship import Relationship
from models.Role import Role
from models.Successor import Successor
from models.Version import Version
from models.Setting import Setting

schema_version = '009'

# Logging Setup
log = logging.getLogger('import_ods_xml')
log.setLevel(logging.DEBUG)

# We need a filemanager to bring the xml data tree structure in
File_manager = ODSFileManager()

# SQLAlchemy objects
# engine = create_engine('sqlite:///openods.sqlite', echo=False)
engine = create_engine(
    "postgresql://openods:openods@localhost/openods", isolation_level="READ UNCOMMITTED")
metadata = Base.metadata
Session = sessionmaker(bind=engine)
session = Session()


def convert_string_to_date(string):
    return datetime.datetime.strptime(string, '%Y-%m-%d')


class DataBaseSetup(object):

    __ods_xml_data = None
    __code_system_dict = {}

    def __init__(self):
        # Creates the tables of all objects derived from our Base object
        metadata.create_all(engine)

    def __create_settings(self):

        setting = Setting()

        setting.key = 'schema_version'
        setting.value = schema_version

        session.add(setting)

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

            organisations[idx].odscode = organisation.find('OrgId').attrib.get('extension')

            organisations[idx].name = organisation.find('Name').text

            organisations[idx].status = organisation.find('Status').attrib.get('value')

            organisations[idx].record_class = self.__code_system_dict[organisation.attrib.get('orgRecordClass')]

            organisations[idx].last_changed = organisation.find('LastChangeDate').attrib.get('value')

            organisations[idx].ref_only = bool(organisation.attrib.get('refOnly'))

            for date in organisation.iter('Date'):
                if date.find('Type').attrib.get('value') == 'Legal':

                    try:
                        organisations[idx].legal_start_date = \
                            convert_string_to_date(date.find('Start').attrib.get('value'))
                    except:
                        pass

                    try:
                        organisations[idx].legal_end_date = \
                            convert_string_to_date(date.find('End').attrib.get('value'))
                    except:
                        pass

                elif date.find('Type').attrib.get('value') == 'Operational':
                    try:
                        organisations[idx].operational_start_date = \
                            convert_string_to_date(date.find('Start').attrib.get('value'))
                    except:
                        pass

                    try:
                        organisations[idx].operational_end_date = \
                            convert_string_to_date(date.find('End').attrib.get('value'))
                    except:
                        pass

            session.add(organisations[idx])

            self.__create_addresses(organisations[idx], organisation)

            self.__create_roles(organisations[idx], organisation)

            self.__create_relationships(organisations[idx], organisation)

            self.__create_successors(organisations[idx], organisation)

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
            roles[idx].primary_role = bool(role.attrib.get('primaryRole'))
            roles[idx].status = role.find('Status').attrib.get('value')
            roles[idx].unique_id = role.attrib.get('uniqueRoleId')

            # Add Operational and Legal start/end dates if present
            for date in role.iter('Date'):
                if date.find('Type').attrib.get('value') == 'Legal':
                    try:
                        roles[idx].legal_start_date = \
                            convert_string_to_date(date.find('Start').attrib.get('value'))
                    except:
                        pass
                    try:
                        roles[idx].legal_end_date = \
                            convert_string_to_date(date.find('End').attrib.get('value'))
                    except:
                        pass

                elif date.find('Type').attrib.get('value') == 'Operational':
                    try:
                        roles[idx].operational_start_date = \
                            convert_string_to_date(date.find('Start').attrib.get('value'))
                    except:
                        pass
                    try:
                        roles[idx].operational_end_date = \
                            convert_string_to_date(date.find('End').attrib.get('value'))
                    except:
                        pass

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
            relationships[idx].target_odscode = relationship.find(
                'Target/OrgId').attrib.get('extension')
            relationships[idx].status = relationship.find(
                'Status').attrib.get('value')
            relationships[idx].unique_id = relationship.attrib.get(
                'uniqueRelId')

            for date in relationship.iter('Date'):
                if date.find('Type').attrib.get('value') == 'Legal':
                    try:
                        relationships[idx].legal_start_date = \
                            convert_string_to_date(date.find('Start').attrib.get('value'))
                    except:
                        pass
                    try:
                        relationships[idx].legal_end_date = \
                            convert_string_to_date(date.find('End').attrib.get('value'))
                    except:
                        pass

                elif date.find('Type').attrib.get('value') == 'Operational':
                    try:
                        relationships[idx].operational_start_date = \
                            convert_string_to_date(date.find('Start').attrib.get('value'))
                    except:
                        pass
                    try:
                        relationships[idx].operational_end_date = \
                            convert_string_to_date(date.find('End').attrib.get('value'))
                    except:
                        pass

            # self.__code_system_dict[]

            session.add(relationships[idx])

        relationships = None

    def __create_addresses(self, organisation, organisation_xml):

        for idx, location in enumerate(organisation_xml.findall(
                'GeoLoc/Location')):

            address = Address()

            try:
                address.org_odscode = organisation.odscode
            except AttributeError:
                pass

            try:
                address.street_address_line1 = location.find('StreetAddressLine1').text
            except AttributeError:
                pass

            try:
                address.street_address_line2 = location.find('StreetAddressLine2').text
            except AttributeError:
                pass

            try:
                address.street_address_line3 = location.find('StreetAddressLine3').text
            except AttributeError:
                pass

            try:
                address.town = location.find('Town').text
            except AttributeError:
                pass

            try:
                address.county = location.find('County').text
            except AttributeError:
                pass

            try:
                address.postal_code = location.find('PostalCode').text
            except AttributeError:
                pass

            try:
                address.country = location.find('Country').text
            except AttributeError:
                pass

            try:
                address.uprn = location.find('UPRN').text
            except AttributeError:
                pass

            session.add(address)

    def __create_successors(self, organisation, organisation_xml):

        for idx, succ in enumerate(organisation_xml.findall(
                'Succs/Succ')):

            successor = Successor()

            try:
                successor.unique_id = succ.attrib.get('uniqueSuccId')
            except AttributeError:
                pass

            try:
                successor.org_odscode = organisation.odscode
            except AttributeError:
                pass

            try:
                successor.legal_start_date = \
                    convert_string_to_date(succ.find('Date/Start').attrib.get('value'))
            except AttributeError:
                pass

            try:
                successor.type = \
                    succ.find('Type').text
            except AttributeError:
                pass

            try:
                successor.target_odscode = \
                    succ.find('Target/OrgId').attrib.get('extension')
            except AttributeError:
                pass

            try:
                successor.target_primary_role_code = \
                    succ.find('Target/PrimaryRoleId').attrib.get('id')
            except AttributeError:
                pass

            try:
                successor.target_unique_role_id = \
                    succ.find('Target/PrimaryRoleId').attrib.get('uniqueRoleId')
            except AttributeError:
                pass

            session.add(successor)

    def __create_version(self):
        """adds all the version information to the versions table

        Parameters
        ----------
        None
        Returns
        -------
        None
        """

        version = Version()

        version.file_version = self.__ods_xml_data.find(
            './Manifest/Version').attrib.get('value')
        version.publication_date = self.__ods_xml_data.find(
            './Manifest/PublicationDate').attrib.get('value')
        version.publication_type = self.__ods_xml_data.find(
            './Manifest/PublicationType').attrib.get('value')
        version.publication_seqno = self.__ods_xml_data.find(
            './Manifest/PublicationSeqNum').attrib.get('value')
        version.import_timestamp = datetime.datetime.now()

        session.add(version)

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
        log.info('Starting import')

        self.__ods_xml_data = ods_xml_data
        if self.__ods_xml_data is not None:
            try:
                self.__create_version()
                self.__create_codesystems()
                self.__create_organisations()
                self.__create_settings()

                session.commit()

            except Exception as e:
                # If anything fails, let's not commit anything
                session.rollback()
                print("Unexpected error:", sys.exc_info()[0])
                log.error(e)
                raise

            finally:
                session.close()

if __name__ == '__main__':
    start_time = time.time()

    ods_xml_data = File_manager.get_latest_xml()
    DataBaseSetup().create_database(ods_xml_data)

    log.info('Data Import Time = %s', time.strftime(
        "%H:%M:%S", time.gmtime(time.time() - start_time)))
