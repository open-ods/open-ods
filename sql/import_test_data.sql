INSERT into organisations (org_odscode, org_name, org_status, org_recordclass, org_lastchanged,
                           organisation_legal_start_date, organisation_legal_end_date,
                           organisation_operational_start_date, organisation_operational_end_date) VALUES
('TSITE1', 'Test Site 1', 'ACTIVE', 'HSCSite', '2015-05-01', '2012-01-01', '2013-01-01', '2012-01-01','2014-01-01'),
('TSITE2', 'Test Site 2', 'INACTIVE', 'HSCSite', '2015-05-02', '2012-01-01', '2013-01-01', '2012-01-01','2014-01-01'),
('TORG1', 'Test Org 1', 'ACTIVE', 'HSCOrg', '2015-06-01', '2012-01-01', '2013-01-01', '2012-01-01','2014-01-01'),
('TORG2', 'Test Org 2', 'INACTIVE', 'HSCOrg', '2015-06-02', '2012-01-01', '2013-01-01', '2012-01-01','2014-01-01');


INSERT into relationships (organisation_ref, org_odscode, target_odscode, relationship_code,
                           relationship_legal_start_date, relationship_legal_end_date,
                           relationship_operational_start_date, relationship_operational_end_date) VALUES
('9821509c-ecfd-4d2e-a0a8-d65bb327cb6e', 'TSITE1', 'TORG1', 'RE2', '2012-01-01', '2013-01-01', '2012-01-01','2014-01-01'),
('aededa1f-740a-468b-9208-fe6404b73bbd', 'TSITE2', 'TORG2', 'RE1', '2012-01-01', '2013-01-01', '2012-01-01','2014-01-01'),
('9c544acb-8c7c-4f7f-bb0d-9bcb32599d60', 'TORG1', 'TSITE1', 'RE1', '2012-01-01', '2013-01-01', '2012-01-01','2014-01-01'),
('1e8b85f0-823c-4e39-b2f3-d616cf89aa3d', 'TORG2', 'TSITE2', 'RE1', '2012-01-01', '2013-01-01', '2012-01-01','2014-01-01');


INSERT into roles (organisation_ref, org_odscode, role_code, primary_role, role_status,
                   role_legal_start_date, role_legal_end_date,
                   role_operational_start_date, role_operational_end_date ) VALUES
('9821509c-ecfd-4d2e-a0a8-d65bb327cb6e', 'TSITE1', 'RO198', TRUE, 'ACTIVE' , '2012-01-01', '2013-01-01', '2012-01-01','2014-01-01'),
('aededa1f-740a-468b-9208-fe6404b73bbd', 'TSITE2', 'RO108', TRUE, 'ACTIVE' , '2012-01-01', '2013-01-01', '2012-01-01','2014-01-01'),
('9c544acb-8c7c-4f7f-bb0d-9bcb32599d60', 'TORG1', 'RO177', TRUE, 'ACTIVE' , '2012-01-01', '2013-01-01', '2012-01-01','2014-01-01'),
('1e8b85f0-823c-4e39-b2f3-d616cf89aa3d', 'TORG2', 'RO57', TRUE, 'ACTIVE' , '2012-01-01', '2013-01-01', '2012-01-01','2014-01-01')


