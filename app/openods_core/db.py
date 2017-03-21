import logging

import flask_featureflags as feature
import psycopg2
import psycopg2.extras
import psycopg2.pool

import config as config
from app.openods_core import connection as connect


def remove_none_values_from_dictionary(dirty_dict):
    clean_dict = dict((k, v) for k, v in dirty_dict.items() if v is not None)
    return clean_dict


def get_org_list(offset=0, limit=20, recordclass='both',
                 primary_role_code=None, role_code=None,
                 query=None, postcode=None, active=True):
    """Retrieves a list of organisations

    Parameters
    ----------
    q = search term
    offset = the record from which to start
    limit = the maximum number of records to return
    recordclass = the type of record to return (HSCSite, HSCOrg, Both)
    primary_role_code = filter organisations to only those where this is their primary role code
    role_code = filter organisations to only those a role with this code
    postcode = filter organisations to those with a match on the postcode
    active = filter organisations by their status (active / inactive)

    Returns
    -------
    List of organisations filtered by provided parameters
    """

    logger = logging.getLogger(__name__)

    if int(limit) > 1000:
        limit = 1000

    conn = connect.get_connection()

    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    record_class_param = '%' if recordclass == 'both' else recordclass

    # Start the select statement with the field list and from clause
    sql = "SELECT odscode, name, record_class, status " \
          "FROM organisations " \
          "WHERE TRUE "

    sql_count = "SELECT COUNT(*) FROM organisations WHERE TRUE "
    data = ()

    # If a record_class parameter was specified, add that to the statement
    if recordclass:
        logger.debug('record_class parameter was provided')
        sql = str.format("{0} {1}",
                         sql,
                         "AND record_class LIKE %s ")

        sql_count = str.format("{0} {1}",
                               sql_count,
                               "AND record_class LIKE %s ")

        data = (recordclass,)

    # If a query parameter was specified, add that to the statement
    if query:
        logger.debug("q parameter was provided")

        sql = str.format("{0} {1}",
                         sql,
                         "AND UPPER(name) LIKE UPPER(%s) ")

        sql_count = str.format("{0} {1}",
                               sql_count,
                               "AND UPPER(name) LIKE UPPER(%s) ")

        search_query = str.format("%{0}%",
                                  query)

        data = data + (search_query,)

    # If a postcode parameter was specified, add that to the statement
    if postcode:
        logger.debug("postcode parameter was provided")

        new_clause = "AND UPPER(post_code) LIKE UPPER(%s) "

        sql = "{sql} {new_sql}".format(
            sql=sql, new_sql=new_clause)

        sql_count = "{sql} {new_sql}".format(
            sql=sql_count, new_sql=new_clause)

        postcode_query = str.format("%{0}%",
                                    postcode)

        data = data + (postcode_query, )

    # If the active parameter was specified, add that to the statement
    if active:
        logger.debug("active parameter was provided")

        if active in (True, 1, '1', 'True', 'true', 'TRUE', 'yes', 'Yes', 'YES'):
            active_value = 'Active'
            new_clause = "AND status = %s "
        else:
            active_value = 'Inactive'
            new_clause = "AND status = %s "

        sql = "{sql} {new_sql}".format(
            sql=sql, new_sql=new_clause)

        sql_count = "{sql} {new_sql}".format(
            sql=sql_count, new_sql=new_clause)

        data = data + (active_value, )


    # If a role_code parameter was specified, add that to the statement
    if role_code:
        logger.debug('role_code parameter was provided')

        sql = str.format("{0} {1}",
                         sql,
                         "AND UPPER(odscode) in "
                         "(SELECT org_odscode "
                         "FROM roles "
                         "WHERE status = 'Active' "
                         "AND UPPER(code) = UPPER(%s)) ")

        sql_count = str.format("{0} {1}",
                               sql_count,
                               "AND odscode in "
                               "(SELECT org_odscode "
                               "FROM roles "
                               "WHERE status = 'Active' "
                               "AND UPPER(code) = UPPER(%s)) ")

        data = data + (role_code,)

    # Or if a primary_role_code parameter was specified, add that to the statement
    elif primary_role_code:
        logger.debug('primary_role_code parameter was provided')

        sql = str.format("{0} {1}",
                         sql,
                         "AND odscode IN "
                         "(org_odscode "
                         "FROM roles "
                         "WHERE primary_role = TRUE "
                         "AND status = 'Active' "
                         "AND UPPER(code) = UPPER(%s)) ")

        sql_count = str.format("{0} {1}",
                               sql_count,
                               "AND odscode IN "
                               "(org_odscode "
                               "FROM roles "
                               "WHERE primary_role = TRUE "
                               "AND status = 'Active' "
                               "AND UPPER(code) = UPPER(%s)) ")

        data = data + (primary_role_code,)

    # Quickly get total number of query results before applying offset and limit
    cur.execute(sql_count, data)
    count = cur.fetchone()['count']

    # Lastly, add the offset and limit clauses to the main select statement
    sql = str.format("{0} {1}",
                     sql,
                     "ORDER BY name "
                     "OFFSET %s "
                     "LIMIT %s;")

    data = data + (offset, limit)

    logger.debug(sql)

    # Execute the main query
    cur.execute(sql, data)
    rows = cur.fetchall()

    logger.debug(str.format("{0} results", len(rows)))

    result = []

    for row in rows:
        link_self_href = str.format('http://{0}/organisations/{1}',
                                    config.APP_HOSTNAME,
                                    row['odscode'])

        item = {
            'odsCode': row['odscode'],
            'name': row['name'],
            'recordClass': row['record_class'],
            'status': row['status'],
            'links': [{
                'rel':'self',
                'href': link_self_href
            }]
        }
        result.append(item)

    # Return both the paged results and the count of total results
    return result, count


def get_organisation_by_odscode(odscode):

    logger = logging.getLogger(__name__)

    # Get a database connection
    conn = connect.get_connection()

    # Use the RealDictCursor to return data as a python dictionary type
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Try and retrieve the organisation record for the provided ODS code
    try:
        sql = "SELECT * " \
              "FROM organisations " \
              "WHERE UPPER(odscode) = UPPER(%s) "\
              "LIMIT 1;"

        data = (odscode,)

        cur.execute(sql, data)
        row_org = cur.fetchone()
        logger.debug(str.format("Organisation Record: {0}",
                                row_org))

        # Raise an exception if the organisation record is not found
        if row_org is None:
            raise Exception("Record Not Found")

        row_org = remove_none_values_from_dictionary(row_org)

        # Get the organisation_ref from the retrieved record
        organisation_odscode = row_org['odscode']

        # Retrieve the roles for the organisation
        try:
            sql = "SELECT r.code, csr.displayname, r.unique_id, r.status, " \
                  "r.operational_start_date, r.operational_end_date, r.legal_start_date, " \
                  "r.legal_end_date, r.primary_role " \
                  "FROM roles r " \
                  "LEFT JOIN codesystems csr on r.code = csr.id " \
                  "WHERE UPPER(r.org_odscode) = UPPER(%s);"

            data = (organisation_odscode,)

            cur.execute(sql, data)
            rows_roles = cur.fetchall()

        except Exception as e:
            raise

        # Retrieve the relationships for the organisation
        try:
            sql = "SELECT rs.code, csr.displayname, rs.unique_id, rs.target_odscode, rs.status, " \
                  "rs.operational_start_date, rs.operational_end_date, rs.legal_start_date, " \
                  "rs.legal_end_date, o.name " \
                  "FROM relationships rs " \
                  "LEFT JOIN codesystems csr on rs.code = csr.id " \
                  "LEFT JOIN organisations o on rs.target_odscode = o.odscode " \
                  "WHERE UPPER(rs.org_odscode) = UPPER(%s);"

            data = (organisation_odscode,)

            cur.execute(sql, data)
            rows_relationships = cur.fetchall()

        except Exception as e:
            raise

        # Retrieve the addresses for the organisation
        try:
            sql = "SELECT address_line1, " \
                  "address_line2, " \
                  "address_line3, " \
                  "town, county, " \
                  "post_code, " \
                  "country, uprn, " \
                  "location_id " \
                  "FROM addresses a " \
                  "WHERE UPPER(a.org_odscode) = UPPER(%s);"

            data = (organisation_odscode,)

            cur.execute(sql, data)
            rows_addresses = cur.fetchall()
            logger.debug("Addresses: %s" % rows_addresses)

        except Exception as e:
            raise

        # Retrieve the successors / predecessors for the organisation
        try:
            sql = "SELECT type, target_odscode as targetOdsCode, " \
                  "o.name as targetName, " \
                  "target_primary_role_code as targetPrimaryRoleCode, " \
                  "unique_id as uniqueId " \
                  "FROM successors s " \
                  "LEFT JOIN organisations o on s.target_odscode = o.odscode " \
                  "WHERE UPPER(s.org_odscode) = UPPER(%s);"

            data = (organisation_odscode,)

            cur.execute(sql, data)
            rows_successors = cur.fetchall()
            logger.debug("Successors: %s" % rows_successors)

        except Exception as e:
            raise

        # Create an object from the returned organisation record to hold the data to be returned
        result_data = row_org

        # Add the retrieved relationships data to the object
        relationships = []

        for relationship in rows_relationships:

            relationship = remove_none_values_from_dictionary(relationship)

            link_target_href = str.format('http://{0}/organisations/{1}',
                                          config.APP_HOSTNAME,
                                          relationship['target_odscode'])

            relationship['uniqueId'] = int(relationship.pop('unique_id'))
            relationship['relatedOdsCode'] = relationship.pop('target_odscode')
            relationship['relatedOrganisationName'] = relationship.pop('name')
            relationship['description'] = relationship.pop('displayname')
            relationship['status'] = relationship.pop('status')

            try:
                relationship['operationalStartDate'] = relationship.pop('operational_start_date').isoformat()
            except:
                pass

            try:
                relationship['legalEndDate'] = relationship.pop('legal_end_date').isoformat()
            except:
                pass

            try:
                relationship['legalStartDate'] = relationship.pop('legal_start_date').isoformat()
            except:
                pass

            try:
                relationship['operationalEndDate'] = relationship.pop('operational_end_date').isoformat()
            except:
                pass

            relationship['links'] = [{
                    'rel': 'related-organisation',
                    'href': link_target_href
                }]

            relationships.append(relationship)

        result_data['relationships'] = relationships

        # Add the retrieved roles data to the object
        roles = []

        for role in rows_roles:

            role = remove_none_values_from_dictionary(role)

            link_role_href = str.format('http://{0}/role-types/{1}',
                                        config.APP_HOSTNAME, role['code'])

            role['code'] = role.pop('code')
            role['description'] = role.pop('displayname')
            role['primaryRole'] = role.pop('primary_role')

            try:
                role['status'] = role.pop('status')
            except:
                pass

            try:
                role['uniqueId'] = int(role.pop('unique_id'))
            except:
                pass

            try:
                role['operationalStartDate'] = role.pop('operational_start_date').isoformat()
            except Exception as e:
                pass

            try:
                role['legalEndDate'] = role.pop('legal_end_date').isoformat()
            except Exception as e:
                pass

            try:
                role['legalStartDate'] = role.pop('legal_start_date').isoformat()
            except Exception as e:
                pass

            try:
                role['operationalEndDate'] = role.pop('operational_end_date').isoformat()
            except Exception as e:
                pass

            role['links'] = [{
                    'rel': 'role-type',
                    'href': link_role_href
                }]

            roles.append(role)

        result_data['roles'] = roles

        # Add the addresses to the object
        addresses = []

        for address in rows_addresses:
            address = remove_none_values_from_dictionary(address)

            address_lines = []

            try:
                address_lines.append(address.pop('address_line1'))
            except:
                pass

            try:
                address_lines.append(address.pop('address_line2'))
            except:
                pass

            try:
                address_lines.append(address.pop('address_line3'))
            except:
                pass

            if len(address_lines) > 0:
                address['addressLines'] = address_lines

            try:
                address['postCode'] = address.pop('post_code')
            except:
                pass

            addresses.append(address)

        result_data['addresses'] = addresses

        # Add the successors to the object
        successors = []

        for successor in rows_successors:
            link_successor_href = str.format('http://{0}/organisations/{1}',
                                             config.APP_HOSTNAME, successor['targetodscode'])

            successor = remove_none_values_from_dictionary(successor)

            successor['targetOdsCode'] = successor.pop('targetodscode')
            successor['targetPrimaryRoleCode'] = successor.pop('targetprimaryrolecode')
            successor['targetName'] = successor.pop('targetname')
            successor['uniqueId'] = successor.pop('uniqueid')

            successor['links'] = [{
                    'rel': str.lower(successor['type']),
                    'href': link_successor_href
                }]

            successors.append(successor)

        result_data['successors'] = successors

        # Tidy up the field names etc. in the organisation dictionary before it's returned
        result_data['odsCode'] = result_data.pop('odscode')
        result_data['lastChanged'] = result_data.pop('last_changed')
        result_data['refOnly'] = bool(result_data.pop('ref_only'))
        result_data['recordClass'] = result_data.pop('record_class')
        result_data.pop('ref')

        link_self_href = str.format('http://{0}/organisations/{1}', config.APP_HOSTNAME, result_data['odsCode'])
        result_data['links'] = [
            {'rel': 'self',
             'href': link_self_href
            }]

        try:
            result_data['operationalStartDate'] = result_data.pop('operational_start_date').isoformat()
        except:
            pass

        try:
            result_data['legalEndDate'] = result_data.pop('legal_end_date').isoformat()
        except:
            pass

        try:
            result_data['legalStartDate'] = result_data.pop('legal_start_date').isoformat()
        except:
            pass

        try:
            result_data['operationalEndDate'] = result_data.pop('operational_end_date').isoformat()
        except:
            pass

        return result_data

    except psycopg2.DatabaseError as e:
        logger.error(str.format("Error {0}", e))

    except Exception as e:
        logger.error(e)


def search_organisation(search_text, offset=0, limit=1000,):

    logger = logging.getLogger(__name__)

    if limit > 1000:
        limit = 1000

    # Get a database connection
    conn = connect.get_connection()

    # Use the RealDictCursor to return data as a python dictionary type
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        search_term = str.format("%{0}%",
                                 search_text)

        sql = "SELECT * " \
              "FROM organisations " \
              "WHERE UPPER(name) LIKE UPPER(%s) " \
              "AND status = 'Active' " \
              "ORDER BY name OFFSET %s LIMIT %s;"

        data = (search_term, offset, limit)

        logger.debug("Query: {sql}".format(sql=sql))
        cur.execute(sql, data)
        rows = cur.fetchall()
        logger.debug("Number of rows retrieved: {row_count}".format(row_count=rows))

        # Raise an exception if the organisation record is not found
        if not rows:
            raise Exception("Record Not Found")

        result = []

        for row in rows:
            link_self_href = str.format('http://{0}/organisations/{1}', config.APP_HOSTNAME, row['odscode'])
            item = {
                'odsCode': row['odscode'],
                'name': row['name'],
                'recordClass': row['record_class'],
                'links': [{
                    'rel': 'self',
                    'href': link_self_href
                }]
            }
            result.append(item)

        return result

    except Exception as e:
        logger.error(e)


def get_role_types():

    logger = logging.getLogger(__name__)

    conn = connect.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT displayname, id "
                "FROM codesystems "
                "WHERE name = 'OrganisationRole' "\
                "ORDER BY displayname;")

    rows = cur.fetchall()
    result = []

    for row in rows:
        role_code = row['id']
        role_display_name = row['displayname']
        link_self_href = str.format('http://{0}/role-types/{1}', config.APP_HOSTNAME, role_code)
        link_search_primary_role_code_href = str.format('http://{0}/organisations?primaryRoleCode={1}', config.APP_HOSTNAME, role_code)
        link_search_role_code_href = str.format('http://{0}/organisations?roleCode={1}', config.APP_HOSTNAME, role_code)
        result_data = {
            'name': role_display_name,
            'code': role_code,
            'links': [{
                'rel':'self',
                'href': link_self_href
                }, {
                'rel':'organisations.searchByRoleCode',
                'href': link_search_role_code_href
                }]
        }

        if not feature.is_active('SuppressPrimaryRoleSearchLink'):

            result_data['links'].append({
                'rel':'organisations.searchByPrimaryRoleCode',
                'href': link_search_primary_role_code_href
                })

        result.append(result_data)

    logger.debug("Returning: {result}".format(result=result))

    return result


def get_role_type_by_id(role_id):

    sql = "SELECT displayname, id " \
          "FROM codesystems " \
          "WHERE name = 'OrganisationRole' " \
          "AND UPPER(id) = UPPER(%s);"

    data = (role_id,)

    cur = connect.get_cursor()
    cur.execute(sql, data)

    returned_row = cur.fetchone()

    role_code = returned_row['id']
    role_display_name = returned_row['displayname']
    link_self_href = str.format('http://{0}/role-types/{1}', config.APP_HOSTNAME, role_code)
    link_search_primary_role_code_href = str.format('http://{0}/organisations?primaryRoleCode={1}', config.APP_HOSTNAME, role_code)
    link_search_role_code_href = str.format('http://{0}/organisations?roleCode={1}', config.APP_HOSTNAME, role_code)
    result = {
        'name': role_display_name,
        'code': role_code,
        'links': [{
            'rel':'self',
            'href': link_self_href
            }, {
            'rel':'searchOrganisationsWithThisRole',
            'href': link_search_role_code_href
            }]
    }

    if not feature.is_active('SuppressPrimaryRoleSearchLink'):

        result['links'].append({
            'rel': 'organisations.searchByPrimaryRoleCode',
            'href': link_search_primary_role_code_href
        })

    return result


def get_primary_role_scope():

    sql = "SELECT * FROM codesystems where name = 'PrimaryRoleScope';"
    cur = connect.get_cursor()
    cur.execute(sql)

    primary_role_scope_rows = cur.fetchall()
    return primary_role_scope_rows

def get_dataset_info():

    sql = "SELECT * FROM versions;"

    cur = connect.get_cursor()
    cur.execute(sql)

    row_settings = cur.fetchone()

    result = {
        'importDate': row_settings['import_timestamp'],
        'fileVersion': row_settings['file_version'],
        'publicationDate': row_settings['publication_date'],
        'publicationSource': row_settings['publication_source'],
        'publicationType': row_settings['publication_type'],
        'publicationSeqNo': row_settings['publication_seqno'],
        'FileCreationDate': row_settings['file_creation_date'],
        'recordCount': row_settings['record_count'],
        'contentDescription': row_settings['content_description'],
        'primaryRoleScope': get_primary_role_scope()
    }

    print(result)

    return result
