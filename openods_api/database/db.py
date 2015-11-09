import psycopg2, psycopg2.pool, psycopg2.extras
import logging

import openods_api.database.connection as connect
import openods_api.config as config

log = logging.getLogger('openods')


def get_latest_org():
    conn = connect.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * from organisations order by org_lastchanged desc limit 1;")
    rows = cur.fetchall()

    for row in rows:
        print(row)
        return row


def get_org_list(offset=0, limit=1000, recordclass='both', primary_role_code=None):
    log.debug(str.format("Offset: {0} Limit: {1}, RecordClass: {2}", offset, limit, recordclass))
    conn = connect.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    record_class_param = '%' if recordclass == 'both' else recordclass

    if primary_role_code:
        sql = "SELECT org_odscode, org_name, org_recordclass from organisations_primary_roles " \
                "WHERE org_recordclass LIKE %s AND role_code = %s " \
                "order by org_name OFFSET %s LIMIT %s;"
        data = (record_class_param, primary_role_code, offset, limit)

    else:
        sql = "SELECT org_odscode, org_name, org_recordclass from organisations " \
                "WHERE org_recordclass LIKE %s " \
                "order by org_name OFFSET %s LIMIT %s;"
        data = (record_class_param, offset, limit)

    log.debug(sql)
    cur.execute(sql, data)
    rows = cur.fetchall()
    log.debug(str.format("{0} rows in result", len(rows)))
    result = []

    for row in rows:
        link_self_href = str.format('http://{0}/organisations/{1}', config.APP_HOSTNAME, row['org_odscode'])
        item = {
            'odsCode': row['org_odscode'],
            'name': row['org_name'],
            'recordClass': row['org_recordclass'],
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
              "WHERE org_odscode = %s "\
              "limit 1;"
        data = (odscode,)

        cur.execute(sql, data)
        row_org = cur.fetchone()
        log.debug(str.format("Organisation Record: {0}", row_org))

        # Raise an exception if the organisation record is not found
        if row_org is None:
            raise Exception("Record Not Found")

        # Get the organisation_ref from the retrieved record
        organisation_ref = row_org['organisation_ref']

        # Retrieve the roles for the organisation
        sql = "SELECT r.role_code, csr.codesystem_displayname, r.role_unique_id, r.role_status, " \
              "r.role_start_date, r.role_end_date from roles r " \
              "left join codesystems csr on r.role_code = csr.codesystem_id " \
              "WHERE r.organisation_ref = %s; "
        data = (organisation_ref,)

        cur.execute(sql, data)
        rows_roles = cur.fetchall()
        log.debug(rows_roles)

        # Retrieve the relationships for the organisation
        sql = "SELECT rs.relationship_code, csr.codesystem_displayname, rs.target_odscode, o.org_name from relationships rs " \
            "left join codesystems csr on rs.relationship_code = csr.codesystem_id " \
            "left join organisations o on rs.target_odscode = o.org_odscode " \
            "WHERE rs.organisation_ref = %s; "
        data = (organisation_ref,)

        cur.execute(sql, data)
        rows_relationships = cur.fetchall()
        log.debug(rows_relationships)

        # Create an object from the returned organisation record to hold the data to be returned
        result_data = row_org

        # Add the retrieved relationships data to the object
        relationships = []

        for relationship in rows_relationships:

            link_target_href = str.format('http://{0}/organisations/{1}',
                                        config.APP_HOSTNAME, relationship['target_odscode'])

            relationship['targetOdsCode'] = relationship.pop('target_odscode')
            relationship['relationshipCode'] = relationship.pop('relationship_code')
            relationship['targetOrganisationName'] = relationship.pop('org_name')
            relationship['relationshipDescription'] = relationship.pop('codesystem_displayname')

            relationship['links'] = [{
                    'rel': 'target',
                    'href': link_target_href
                }]

            relationships.append({'relationship': relationship})

        result_data['relationships'] = relationships

        # Add the retrieved roles data to the object
        roles = []

        for role in rows_roles:
            link_role_href = str.format('http://{0}/role-types/{1}',
                                        config.APP_HOSTNAME, role['role_code'])

            role['roleTypeCode'] = role.pop('role_code')
            role['roleTypeName'] = role.pop('codesystem_displayname')

            try:
                role['roleStatus'] = role['role_status']
                del role['role_status']
            except:
                pass

            try:
                role['roleUniqueId'] = role['role_unique_id']
                del role['role_unique_id']
            except:
                pass

            try:
                role['roleStartDate'] = role['role_start_date'].isoformat()
                del role['role_start_date']
            except:
                pass

            try:
                role['roleEndDate'] = role['role_end_date'].isoformat()
                del role['role_end_date']
            except:
                pass

            role['links'] = [{
                    'rel': 'role-type',
                    'href': link_role_href
                }]

            roles.append({'role': role})

        result_data['roles'] = roles

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
              "WHERE org_name like UPPER(%s) and org_status = 'ACTIVE';"
        data = (search_term,)

        cur.execute(sql, data)
        rows = cur.fetchall()
        print(rows)

        # Raise an exception if the organisation record is not found
        if rows == []:
            raise Exception("Record Not Found")

        result = []

        for row in rows:
            link_self_href = str.format('http://{0}/organisations/{1}', config.APP_HOSTNAME, row['org_odscode'])
            item = {
                'code': row['org_odscode'],
                'name': row['org_name'],
                'recordClass': row['org_recordclass'],
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
    cur.execute("SELECT codesystem_displayname, codesystem_id from codesystems "
                "where codesystem_name = 'OrganisationRole' "\
                "order by codesystem_displayname;")
    rows = cur.fetchall()
    result = []

    for row in rows:
        role_code = row['codesystem_id']
        role_display_name = row['codesystem_displayname']
        link_self_href = str.format('http://{0}/role-types/{1}', config.APP_HOSTNAME, role_code)
        link_search_href = str.format('http://{0}/organisations?primaryRoleCode={1}', config.APP_HOSTNAME, role_code)
        result.append({
            'name': role_display_name,
            'code': role_code,
            'links': [{
                'rel':'self',
                'href': link_self_href
                }, {
                'rel':'organisations.searchByRoleCode',
                'href': link_search_href
                }]
        })

    return result


def get_role__type_by_id(role_id):

    sql = "SELECT codesystem_displayname, codesystem_id from codesystems " \
          "where codesystem_name = 'OrganisationRole' AND codesystem_id = %s;"
    data = (role_id,)

    cur = connect.get_cursor()
    cur.execute(sql, data)

    returned_row = cur.fetchone()

    role_code = returned_row['codesystem_id']
    role_display_name = returned_row['codesystem_displayname']
    link_self_href = str.format('http://{0}/role-types/{1}', config.APP_HOSTNAME, role_code)
    link_search_href = str.format('http://{0}/organisations?primaryRoleCode={1}', config.APP_HOSTNAME, role_code)
    result = {
        'name': role_display_name,
        'code': role_code,
        'links': [{
            'rel':'self',
            'href': link_self_href
            }, {
            'rel':'searchOrganisationsWithThisRoleType',
            'href': link_search_href
            }]
    }

    return result
