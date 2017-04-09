endpoint_data = \
    {
        'notes': 'This is currently dummy data',
        'endpoints': [
            {
                'usage': 'For general communication with the organisation',
                'type': 'email',
                'correspondenceType': 'administrative',
                'value': 'email.address@nhs.net',
                'acceptsPid': False,
                'orderNo': 1
            },
            {
                'usage': 'For patient-identifiable CDA messages',
                'type': 'itk',
                'correspondenceType': 'clinical',
                'value': 'http://itk.endpoint.nhs.uk/ITK',
                'acceptsPid': True,
                'orderNo': 2
            },
            {
                'usage': 'For patient-identifiable tests results',
                'type': 'dts',
                'correspondenceType': 'clinical',
                'value': 'tests.results@dts.nhs.uk',
                'acceptsPid': True,
                'orderNo': 3
            }
        ]
    }