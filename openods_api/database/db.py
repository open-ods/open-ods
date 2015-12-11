import psycopg2, psycopg2.pool, psycopg2.extras
import logging

import openods_api.database.connection as connect
import openods_api.config as config

log = logging.getLogger('openods')


def remove_none_values_from_dictionary(dirty_dict):
    clean_dict = dict((k, v) for k, v in dirty_dict.items() if v is not None)
    return clean_dict


# TODO: Is this method even needed any more?
# def get_latest_org():
#     conn = connect.get_connection()
#     cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#     cur.execute("SELECT * from organisations order by lastchanged desc limit 1;")
#     rows = cur.fetchall()
#
#     for row in rows:
#         print(row)
#         return row


def get_org_list(offset=0, limit=1000, recordclass='both', primary_role_code=None, role_code=None):
    """Retrieves a list of organisations

    Parameters
    ----------
    offset = the record from which to start
    limit = the maximum number of records to return
    recordclass = the type of record to return (HSCSite, HSCOrg, Both)
    primary_role_code = filter organisations to only those where this is their primary role code
    role_code = filter organisations to only those a role with this code

    Returns
    -------
    List of organisations
    """
    log.debug(str.format("Offset: {0} Limit: {1}, RecordClass: {2}", offset, limit, recordclass))
    conn = connect.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    record_class_param = '%' if recordclass == 'both' else recordclass

    if role_code:
        sql = "SELECT odscode, name, record_class from organisations " \
                "WHERE record_class LIKE %s AND odscode in " \
                "(SELECT org_odscode from roles " \
                "WHERE status = 'Active' " \
                "AND code = %s)" \
                "order by name OFFSET %s LIMIT %s;"
        data = (record_class_param, role_code, offset, limit)

    elif primary_role_code:
        sql = "SELECT odscode, name, record_class from organisations " \
                "WHERE record_class LIKE %s AND odscode in " \
                "(SELECT org_odscode from roles WHERE primary_role = TRUE " \
                "AND status = 'Active' " \
                "AND code = %s)" \
                "order by name OFFSET %s LIMIT %s;"
        data = (record_class_param, primary_role_code, offset, limit)

    else:
        sql = "SELECT odscode, name, record_class from organisations " \
                "WHERE record_class LIKE %s " \
                "order by name OFFSET %s LIMIT %s;"
        data = (record_class_param, offset, limit)

    log.debug(sql)
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

    return result


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
        sql = "SELECT r.code, csr.displayname, r.unique_id, r.status, " \
              "r.operational_start_date, r.operational_end_date, r.legal_start_date, " \
              "r.legal_end_date, r.primary_role from roles r " \
              "left join codesystems csr on r.code = csr.id " \
              "WHERE r.org_odscode = %s; "
        data = (organisation_odscode,)

        cur.execute(sql, data)
        rows_roles = cur.fetchall()
        log.debug(rows_roles)

        # Retrieve the relationships for the organisation
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

        try:
            # Retrieve the addresses for the organisation
            sql = "SELECT street_address_line1, " \
                  "street_address_line2, " \
                  "street_address_line3, " \
                  "town, county, " \
                  "postal_code, " \
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

        try:
            # Retrieve the successors / predecessors for the organisation
            sql = "SELECT type, target_odscode as targetOdsCode, " \
                  "target_primary_role_code as targetPrimaryRoleCode, " \
                  "unique_id as uniqueId " \
                  "FROM successors s " \
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

            relationships.append({'relationship': relationship})

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

            roles.append({'role': role})

        result_data['roles'] = roles

        # Add the addresses to the object
        addresses = []

        for address in rows_addresses:
            address = remove_none_values_from_dictionary(address)

            try:
                address['streetAddressLine1'] = address.pop('street_address_line1')
            except:
                pass

            try:
                address['streetAddressLine2'] = address.pop('street_address_line2')
            except:
                pass

            try:
                address['streetAddressLine3'] = address.pop('street_address_line3')
            except:
                pass

            try:
                address['postcalCode'] = address.pop('postal_code')
            except:
                pass

            addresses.append({'address': address})

        result_data['addresses'] = addresses

        # Add the successors to the object
        successors = []

        for successor in rows_successors:
            link_successor_href = str.format('http://{0}/organisations/{1}',
                                             config.APP_HOSTNAME, successor['targetodscode'])

            successor = remove_none_values_from_dictionary(successor)

            successor['targetOdsCode'] = successor.pop('targetodscode')
            successor['uniqueId'] = successor.pop('uniqueid')

            successor['links'] = [{
                    'rel': str.lower(successor['type']),
                    'href': link_successor_href
                }]

            successors.append({'successor': successor})

        result_data['successors'] = successors

        # Tidy up the field names etc. in the organisation dictionary before it's returned
        result_data['odsCode'] = result_data.pop('odscode')
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


def search_organisation(search_text):

    # Get a database connection
    conn = connect.get_connection()

    # Use the RealDictCursor to return data as a python dictionary type
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        search_term = str.format("%{0}%", search_text)
        sql = "SELECT * from organisations " \
              "WHERE name like UPPER(%s) and status = 'Active';"
        data = (search_term,)

        cur.execute(sql, data)
        rows = cur.fetchall()
        print(rows)

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
        result.append({
            'name': role_display_name,
            'code': role_code,
            'links': [{
                'rel':'self',
                'href': link_self_href
                }, {
                'rel':'organisations.searchByPrimaryRoleCode',
                'href': link_search_primary_role_code_href
                }, {
                'rel':'organisations.searchByRoleCode',
                'href': link_search_role_code_href
                }]
        })

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
            'rel':'searchOrganisationsWithThisPrimaryRoleType',
            'href': link_search_primary_role_code_href
            }, {
            'rel':'searchOrganisationsWithThisRoleType',
            'href': link_search_role_code_href
            }]
    }

    return result
