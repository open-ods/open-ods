-- Column: primary_role

-- ALTER TABLE roles DROP COLUMN primary_role;

ALTER TABLE roles ADD COLUMN primary_role boolean;
ALTER TABLE roles ALTER COLUMN primary_role SET NOT NULL;


-- View: active_organisations_primary_roles

-- DROP VIEW active_organisations_primary_roles;

CREATE OR REPLACE VIEW organisations_primary_roles AS
 SELECT o.org_name,
    o.org_odscode,
    r.role_code,
    cs.codesystem_displayname,
    o.org_recordclass
   FROM roles r
     JOIN codesystems cs ON r.role_code::text = cs.codesystem_id::text
     JOIN organisations o ON r.organisation_ref = o.organisation_ref
  WHERE r.primary_role IS TRUE
  ORDER BY o.org_name;

ALTER TABLE organisations_primary_roles
  OWNER TO openods;