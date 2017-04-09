from openods import db


def get_organisation(ods_code):

    data = db.get_organisation_by_odscode(ods_code)

    fhir_resource = {
        'name': data['name'],
        'id': data['odsCode'],
        'active': 'true' if data['status'] == 'Active' else 'false'
    }

    address_list = []

    for address in data['addresses']:
        new_address = {}
        new_address['city'] = address['town']
        new_address['postalCode'] = address['postCode']
        new_address['country'] = address['country']
        new_address['country'] = address['country']
        new_address['line'] = []
        for line in address['addressLines']:
            new_address['line'].append(line)
        address_list.append(new_address)

    fhir_resource['address'] = address_list

    return fhir_resource

