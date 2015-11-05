import psycopg2, psycopg2.pool, psycopg2.extras
import logging

import openods_api.database.connection as connect

log = logging.getLogger('__name__')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)


def get_latest_org():
    conn = connect.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * from organisations order by org_lastchanged desc limit 1;")
    rows = cur.fetchall()

    for row in rows:
        print(row)
        return row


def get_org_list(offset=0, limit=1000):
    log.debug(str.format("Offset: {0} Limit: {1}", offset, limit))
    conn = connect.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = 'SELECT distinct org_odscode, org_name from organisations order by org_odscode OFFSET %s LIMIT %s;'
    log.debug(sql)
    data = (offset, limit)
    cur.execute(sql, data)
    rows = cur.fetchall()
    log.debug(str.format("{0} rows in result", len(rows)))
    result = []

    for row in rows:
        link_self_href = str.format('http://prototype.openods.co.uk/organisations/{0}', row['org_odscode'])
        item = {
            'odscode': row['org_odscode'],
            'name': row['org_name'],
            'link': {
                'rel':'self',
                'href': link_self_href
            }
        }
        result.append(item)

    return result


def get_roles():
    conn = connect.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT codesystem_displayname, codesystem_id from codesystems where codesystem_name = 'OrganisationRole' "\
                "group by codesystem_displayname, codesystem_id order by codesystem_displayname;")
    rows = cur.fetchall()
    result = []

    for row in rows:
        result.append({
            'name': row['codesystem_displayname'],
            'code': row['codesystem_id']
            }
        )

    return result


def get_org(odscode):
    conn = connect.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        sql = "SELECT * from organisations " \
              "WHERE org_odscode = %s "\
              "limit 1;"
        data = (odscode,)

        cur.execute(sql, data)
        row_org = cur.fetchone()
        print(row_org)

        if row_org is None:
            raise Exception("Record Not Found")

        organisation_ref = row_org['organisation_ref']

        sql = "SELECT r.role_code, csr.codesystem_displayname from roles r " \
            "left join codesystems csr on r.role_code = csr.codesystem_id " \
            "WHERE r.organisation_ref = %s; "
        data = (organisation_ref,)

        cur.execute(sql, data)
        rows_roles = cur.fetchall()
        print(rows_roles)

        sql = "SELECT rs.relationship_code, csr.codesystem_displayname, rs.target_odscode, o.org_name from relationships rs " \
            "left join codesystems csr on rs.relationship_code = csr.codesystem_id " \
            "left join organisations o on rs.target_odscode = o.org_odscode " \
            "WHERE rs.organisation_ref = %s; "
        data = (organisation_ref,)

        cur.execute(sql, data)
        rows_relationships = cur.fetchall()
        print(rows_relationships)

        data = row_org
        data['roles'] = rows_roles
        data['relationships'] = rows_relationships

        return data

    except psycopg2.DatabaseError as e:
        log.error(str.format("Error {0}", e))

    except Exception as e:
        log.error(e)


def get_org_doc(odscode):
    conn = connect.get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        sql = "SELECT * from register_ods_organisations " \
              "WHERE data_jsonb ->> 'code' = %s "\
              "limit 1;"
        data = (odscode,)

        cur.execute(sql, data)
        row_org = cur.fetchone()
        print(row_org)

        result = row_org['data_jsonb']

        return result

    except psycopg2.DatabaseError as e:
        log.error(str.format("Error {0}", e))