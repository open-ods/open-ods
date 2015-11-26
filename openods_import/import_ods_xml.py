from lxml import etree as ET
import psycopg2
import uuid
import time
import zipfile
import logging
import sys
# import elasticsearch
# from elasticsearch_dsl import Search

log = logging.getLogger('import_ods_xml')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
log.addHandler(ch)

start = time.time()
log.info("Starting timer")

# Open ODS XML file from zip file
log.info("Loading source data...")
try:
    with zipfile.ZipFile('../data/odsfull.xml.zip') as myzip:
        with myzip.open('odsfull.xml') as myfile:
            tree = ET.parse(myfile)
except:
    sys.exit(1)

try:
    conn = psycopg2.connect('postgresql://openods:openods@localhost:5432/openods')
    log.info("Connected to database")
except:
    log.info("I am unable to connect to the database")
    sys.exit(1)

try:
    es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200
except:
    pass


def add_es_document(doc):
    return es.index(index='organisations', doc_type='org', body=doc)


def xstr(s):
    if s is None:
        return ''
    return str(s)


# Get the record count from the Manifest
log.info("Reading manifest data from XML file...")
record_count = int(tree.find('./Manifest/RecordCount').attrib.get('value'))
file_version = tree.find('./Manifest/Version').attrib.get('value')
publication_date = tree.find('./Manifest/PublicationDate').attrib.get('value')
publication_type = tree.find('./Manifest/PublicationType').attrib.get('value')
publication_seqno = tree.find('./Manifest/PublicationSeqNum').attrib.get('value')
content_description = tree.find('./Manifest/ContentDescription').attrib.get('value')
log.info(str.format("Record Count: ", record_count))
log.info(str.format("File Version: ", file_version))
log.info(str.format("Publication Date: ", publication_date))
log.info(str.format("Publication Sequence Number: ", publication_seqno))
log.info(str.format("Publication Type: ", publication_type))
log.info(str.format("Content Description: ", content_description))

organisation_count = 0

log.info("Starting import routine")

# Clear out existing data
cur = conn.cursor()
log.info("Truncating tables...")
cur.execute('TRUNCATE organisations, '
            'roles, '
            'codesystems, '
            'relationships, '
            'addresses '
            'RESTART IDENTITY;')
conn.commit()
cur.close()
input("Old data removed. Press any key to import new data...")

log.info("Importing data...")

# Import the relationship types and add to a dictionary
rels = tree.find('./CodeSystems/CodeSystem[@name="OrganisationRelationship"]')

relationship_types = {}

for rel in rels.iter('concept'):
    rel_id = rel.attrib.get('id')
    displayName = rel.attrib.get('displayName')
    relationship_types[rel_id] = displayName

    # Add the OrganisationRelationships to the database
    cur = conn.cursor()
    cur.execute('INSERT INTO codesystems (codesystem_name, codesystem_id, codesystem_displayname) '
                'VALUES (%s, %s, %s)', ('OrganisationRelationship', rel_id, displayName))
    conn.commit()
    cur.close()

    log.debug("Imported Relationships")

# Import the record class types and add to a dictionary
recs = tree.find('./CodeSystems/CodeSystem[@name="OrganisationRecordClass"]')

record_classes = {}

for rec in recs.iter('concept'):
    rec_id = rec.attrib.get('id')
    displayName = rec.attrib.get('displayName')
    record_classes[rec_id] = displayName

    # Add the OrganisationRecordClasses to the database
    cur = conn.cursor()
    cur.execute('INSERT INTO codesystems (codesystem_name, codesystem_id, codesystem_displayname) '
                'VALUES (%s, %s, %s)', ('OrganisationRecordClass', rec_id, displayName))
    conn.commit()
    cur.close()
    log.debug("Imported RecordClasses")

# Import the roles types and add to a dictionary
roles = tree.find('./CodeSystems/CodeSystem[@name="OrganisationRole"]')

role_types = {}

for role in roles.iter('concept'):
    role_type_id = role.attrib.get('id')
    displayName = role.attrib.get('displayName')
    log.debug(str.format("{0}: {1}",role_type_id, displayName))
    role_types[role_type_id] = displayName

    # Add the OrganisationRole to the database
    cur = conn.cursor()
    cur.execute('INSERT INTO codesystems (codesystem_name, codesystem_id, codesystem_displayname) '
                'VALUES (%s, %s, %s)', ('OrganisationRole', role_type_id, displayName))
    conn.commit()
    cur.close()
    log.debug("Imported Role Types")

# List all organisations, their roles, and their relations
for node in tree.findall('./Organisations/Organisation'):
    organisation_ref = str(uuid.uuid4())
    organisation_count += 1

    org_odscode = node.find('OrgId').attrib.get('extension')
    org_name = node.find('Name').text
    org_status = node.find('Status').attrib.get('value')
    org_recordclass = record_classes[node.attrib.get('orgRecordClass')]
    org_lastchangeddate = node.find('LastChangeDate').attrib.get('value')

    log.debug(str.format("Organisation Name: {0}", org_name))
    log.debug(str.format("Org Code: {0}", org_odscode))
    log.debug(str.format("Status: {0}", org_status))
    log.debug(str.format("Record Class: {0}", org_recordclass))
    log.debug(str.format("Last Changed Date: {0}", org_lastchangeddate))

    # List the roles for the organisation
    log.debug("Roles:")
    for role in node.find('Roles'):
        log.debug(ET.tostring(role))
        role_ref = str(uuid.uuid4())
        role_code = role.attrib.get('id')
        role_desc = role_types[role_code]
        role_unique_id = role.attrib.get('uniqueRoleId')
        primary_role = bool(role.attrib.get('primaryRole'))
        role_status = role.find('Status').attrib.get('value')

        role_legal_start_date = None
        role_legal_end_date = None
        role_operational_start_date = None
        role_operational_end_date = None

        for date in role.iter('Date'):
            log.debug(ET.tostring(date))
            if date.find('Type').attrib.get('value') == 'Legal':
                try:
                    role_legal_start_date = date.find('Start').attrib.get('value')
                except:
                    pass
                try:
                    role_legal_end_date = date.find('End').attrib.get('value')
                except:
                    pass
            elif date.find('Type').attrib.get('value') == 'Operational':
                try:
                    role_operational_start_date = date.find('Start').attrib.get('value')
                except:
                    pass
                try:
                    role_operational_end_date = date.find('End').attrib.get('value')
                except:
                    pass

        log.debug(str.format("- {0} - {2} - (Primary Role: {1})", role_desc, primary_role, role_status))
        log.debug(str.format("- Legal Dates: {0} - {1}",
                             xstr(role_legal_start_date),
                             xstr(role_legal_end_date)))
        log.debug(str.format("- Operational Dates: {0} - {1}",
                             xstr(role_operational_start_date),
                             xstr(role_operational_end_date)))

        # Add the roles to the database
        cur = conn.cursor()
        cur.execute('INSERT INTO roles (role_ref, organisation_ref, org_odscode, role_code, primary_role, '
                    'role_unique_id, role_status, role_legal_start_date, role_legal_end_date, '
                    'role_operational_start_date, role_operational_end_date) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (role_ref, organisation_ref, org_odscode, role_code, primary_role, role_unique_id, role_status,
                     role_legal_start_date, role_legal_end_date,
                     role_operational_start_date, role_operational_end_date))

        conn.commit()

        cur.close()

    log.debug("")

    for rel in node.find('Rels'):
        relationship_id = rel.attrib.get('id')
        rel_type = relationship_types[relationship_id]
        rel_target = rel.find('Target/OrgId').attrib.get('extension')
        rel_status = rel.find('Status').attrib.get('value')
        rel_unique_id = rel.attrib.get('uniqueRelId')
        log.debug(str.format("- {0} {1}", rel_type, rel_target))

        relationship_legal_start_date = None
        relationship_legal_end_date = None
        relationship_operational_start_date = None
        relationship_operational_end_date = None

        for date in rel.iter('Date'):
            log.debug(ET.tostring(date))
            if date.find('Type').attrib.get('value') == 'Legal':
                try:
                    relationship_legal_start_date = date.find('Start').attrib.get('value')
                except:
                    pass
                try:
                    relationship_legal_end_date = date.find('End').attrib.get('value')
                except:
                    pass
            elif date.find('Type').attrib.get('value') == 'Operational':
                try:
                    relationship_operational_start_date = date.find('Start').attrib.get('value')
                except:
                    pass
                try:
                    relationship_operational_end_date = date.find('End').attrib.get('value')
                except:
                    pass

        # Add the relationships to the database
        cur = conn.cursor()
        cur.execute('INSERT INTO relationships (organisation_ref, org_odscode, target_odscode, '
                    'relationship_code, relationship_legal_start_date, relationship_legal_end_date, '
                    'relationship_operational_start_date, relationship_operational_end_date, '
                    'relationship_unique_id, relationship_status) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (organisation_ref, org_odscode, rel_target, relationship_id,
                     relationship_legal_start_date, relationship_legal_end_date,
                     relationship_operational_start_date, relationship_operational_end_date, rel_unique_id, rel_status))
        conn.commit()
        cur.close()

    log.debug("")

    # Add the organisations to the database
    cur = conn.cursor()
    cur.execute('INSERT INTO organisations (org_odscode, org_name, org_status, org_recordclass, org_lastchanged, '
                'organisation_ref) '
                'VALUES (%s, %s, %s, %s, %s, %s)',
                (org_odscode, org_name, org_status, org_recordclass, org_lastchangeddate, organisation_ref))
    conn.commit()
    cur.close()

    doc = {
        'orgName': org_name,
        'orgOdsCode': org_odscode,
        'orgStatus': org_status
    }

    # add_es_document(doc)

    # log.debug a separator between each organisation record
    log.debug("========================")
    if ch.level == logging.DEBUG:
        input("Next...")

log.debug(organisation_count)

conn.close()
end = time.time()
log.info(str.format("Import took {0}s", (end - start)))
log.info("Import Complete.")
sys.exit(0)
