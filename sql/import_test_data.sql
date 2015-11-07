INSERT into organisations (org_odscode, org_name, org_status, org_recordclass, org_lastchanged) VALUES
('TSITE1', 'Test Site 1', 'ACTIVE', 'HSCSite', '2015-05-01'),
('TSITE2', 'Test Site 2', 'INACTIVE', 'HSCSite', '2015-05-02'),
('TORG1', 'Test Org 1', 'ACTIVE', 'HSCOrg', '2015-06-01'),
('TORG2', 'Test Org 2', 'INACTIVE', 'HSCOrg', '2015-06-02');


INSERT into relationships (organisation_ref, org_odscode, target_odscode, relationship_code) VALUES
('9821509c-ecfd-4d2e-a0a8-d65bb327cb6e', 'TSITE1', 'TORG1', 'RE2'),
('aededa1f-740a-468b-9208-fe6404b73bbd', 'TSITE2', 'TORG2', 'RE1'),
('9c544acb-8c7c-4f7f-bb0d-9bcb32599d60', 'TORG1', 'TSITE1', 'RE1'),
('1e8b85f0-823c-4e39-b2f3-d616cf89aa3d', 'TORG2', 'TSITE2', 'RE1');


INSERT into roles (organisation_ref, org_odscode, role_code, primary_role) VALUES
('9821509c-ecfd-4d2e-a0a8-d65bb327cb6e', 'TSITE1', 'RO198', TRUE),
('aededa1f-740a-468b-9208-fe6404b73bbd', 'TSITE2', 'RO108', TRUE),
('9c544acb-8c7c-4f7f-bb0d-9bcb32599d60', 'TORG1', 'RO177', TRUE),
('1e8b85f0-823c-4e39-b2f3-d616cf89aa3d', 'TORG2', 'RO57', TRUE)