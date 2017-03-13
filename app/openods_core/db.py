import logging

import flask_featureflags as feature
import psycopg2
import psycopg2.extras
import psycopg2.pool

import config as config
from app.openods_core import connection as connect

log = logging.getLogger('openods')


def remove_none_values_from_dictionary(dirty_dict):
    clean_dict = dict((k, v) for k, v in dirty_dict.items() if v is not None)
    return clean_dict


def get_org_list(offset=0, limit=20, recordclass='both', primary_role_code=None, role_code=None, query=None):
    """Retrieves a list of organisations

    Parameters
    ----------
    q = search term
    offset = the record from which to start
    limit = the maximum number of records to return
    recordclass = the type of record to return (HSCSite, HSCOrg, Both)
    primary_role_code = filter organisations to only those where this is their primary role code
    role_code = filter organisations to only those a role with this code

    Returns
    -------
    List of organisations filtered by provided parameters
    """
    log.debug(str.format("Offset: {0} Limit: {1}, RecordClass: {2}, Query: {3}", offset, limit, recordclass, query))
    conn = connect.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    record_class_param = '%' if recordclass == 'both' else recordclass

    # Start the select statement with the field list and from clause
    sql = "SELECT odscode, name, record_class from organisations WHERE TRUE "
    sql_count = "SELECT COUNT(*) from organisations WHERE TRUE "
    data = ()

    # If a record_class parameter was specified, add that to the statement
    if recordclass:
        log.debug('record_class parameter was provided')
        sql = str.format("{0} {1}", sql, "AND record_class LIKE %s ")
        sql_count = str.format("{0} {1}", sql_count, "AND record_class LIKE %s ")
        data = (recordclass,)

    # If a query parameter was specified, add that to the statement
    if query:
        log.debug("q parameter was provided")
        sql = str.format("{0} {1}", sql, "AND name like UPPER(%s) ")
        sql_count = str.format("{0} {1}", sql_count, "AND name like UPPER(%s) ")
        search_query = str.format("%{0}%", query)
        data = data + (search_query,)

    # If a role_code parameter was specified, add that to the statement
    if role_code:
        log.debug('role_code parameter was provided')
        sql = str.format("{0} {1}",
                         sql,
                         "AND odscode in "
                         "(SELECT org_odscode from roles "
                         "WHERE status = 'Active' "
                         "AND code = %s) ")
        sql_count = str.format("{0} {1}",
                         sql_count,
                         "AND odscode in "
                         "(SELECT org_odscode from roles "
                         "WHERE status = 'Active' "
                         "AND code = %s) ")
        data = data + (role_code,)

    # Or if a primary_role_code parameter was specified, add that to the statement
    elif primary_role_code:
        log.debug('primary_role_code parameter was provided')
        sql = str.format("{0} {1}",
                         sql,
                         "AND odscode in "
                         "(SELECT org_odscode from roles WHERE primary_role = TRUE "
                         "AND status = 'Active' "
                         "AND code = %s) " )
        sql_count = str.format("{0} {1}",
                         sql_count,
                         "AND odscode in "
                         "(SELECT org_odscode from roles WHERE primary_role = TRUE "
                         "AND status = 'Active' "
                         "AND code = %s) " )
        data = data + (primary_role_code,)

    # Quickly get total number of query results before applying offset and limit
    log.debug(sql_count)
    log.debug(data)
    cur.execute(sql_count, data)
    count = cur.fetchone()['count']

    # Lastly, add the offset and limit clauses to the main select statement
    sql = str.format("{0} {1}", sql, "ORDER BY name OFFSET %s LIMIT %s;")
    data = data + (offset, limit)

    log.debug(sql)
    log.debug(data)

    # Execute the main query
    cur.execute(sql, data)
    rows = cur.fetchall()
    log.debug(str.format("{0} rows in result", len(rows)))
    result = []

    for row in rows:
        link_self_href = str.format('http://{0}/organisations/{1}', config.APP_HOSTNAME, row['odscode'])
        item = {
            'odsCode': row['odscode'],
            'name': row['name'],
            'recordClass': row['record_class'],
            'links': [{
                'rel':'self',
                'href': link_self_href
            }]
        }
        result.append(item)

    # Return both the paged results and the count of total results
    return result, count


def get_organisation_by_odscode(odscode):

    # Get a database connection
    conn = connect.get_connection()

    # Use the RealDictCursor to return data as a python dictionary type
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Try and retrieve the organisation record for the provided ODS code
    try:
        sql = "SELECT * from organisations " \
              "WHERE odscode = %s "\
              "limit 1;"
        data = (odscode,)

        cur.execute(sql, data)
        row_org = cur.fetchone()
        log.debug(str.format("Organisation Record: {0}", row_org))

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
                  "r.legal_end_date, r.primary_role from roles r " \
                  "left join codesystems csr on r.code = csr.id " \
                  "WHERE r.org_odscode = %s; "
            data = (organisation_odscode,)

            cur.execute(sql, data)
            rows_roles = cur.fetchall()
            log.debug(rows_roles)

        except Exception as e:
            raise

        # Retrieve the relationships for the organisation
        try:
            sql = "SELECT rs.code, csr.displayname, rs.unique_id, rs.target_odscode, rs.status, " \
                  "rs.operational_start_date, rs.operational_end_date, rs.legal_start_date, " \
                  "rs.legal_end_date, o.name from relationships rs " \
                "left join codesystems csr on rs.code = csr.id " \
                "left join organisations o on rs.target_odscode = o.odscode " \
                "WHERE rs.org_odscode = %s; "
            data = (organisation_odscode,)

            cur.execute(sql, data)
            rows_relationships = cur.fetchall()
            log.debug(rows_relationships)

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
                  "WHERE a.org_odscode = %s;"
            data = (organisation_odscode,)

            cur.execute(sql, data)
            rows_addresses = cur.fetchall()
            log.debug("Addresses: %s" % rows_addresses)

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
                  "WHERE s.org_odscode = %s;"
            data = (organisation_odscode,)

            cur.execute(sql, data)
            rows_successors = cur.fetchall()
            log.debug("Successors: %s" % rows_successors)

        except Exception as e:
            raise

        # Create an object from the returned organisation record to hold the data to be returned
        result_data = row_org

        # Add the retrieved relationships data to the object
        relationships = []

        for relationship in rows_relationships:

            relationship = remove_none_values_from_dictionary(relationship)

            link_target_href = str.format('http://{0}/organisations/{1}',
                                          config.APP_HOSTNAME, relationship['target_odscode'])

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
        log.error(str.format("Error {0}", e))

    except Exception as e:
        log.error(e)


def search_organisation(search_text, offset=0, limit=1000,):

    # Get a database connection
    conn = connect.get_connection()

    # Use the RealDictCursor to return data as a python dictionary type
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        search_term = str.format("%{0}%", search_text)
        sql = "SELECT * from organisations " \
              "WHERE name like UPPER(%s) and status = 'Active' " \
              "ORDER BY name OFFSET %s LIMIT %s;;"
        data = (search_term, offset, limit)

        cur.execute(sql, data)
        rows = cur.fetchall()
        log.debug("Number of rows retrieved: {row_count}".format(row_count=rows))

        # Raise an exception if the organisation record is not found
        if rows == []:
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
        log.error(e)


def get_role_types():

    conn = connect.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT displayname, id from codesystems "
                "where name = 'OrganisationRole' "\
                "order by displayname;")
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
    log.debug("Returning: {result}".format(result=result))
    return result


def get_role_type_by_id(role_id):

    sql = "SELECT displayname, id from codesystems " \
          "where name = 'OrganisationRole' AND id = %s;"
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


def get_dataset_info():

    sql = "SELECT * from versions; "

    cur = connect.get_cursor()
    cur.execute(sql)

    row_settings = cur.fetchone()

    result = {
        'importTimestamp': row_settings['import_timestamp'],
        'fileVersion': row_settings['file_version'],
        'publicationSeqNo': row_settings['publication_seqno'],
        'publicationDate': row_settings['publication_date'],
        'publicationType': row_settings['publication_type']
    }

    return result
