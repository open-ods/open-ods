ALTER TABLE roles RENAME role_start_date  TO role_operational_start_date;
ALTER TABLE roles RENAME role_end_date  TO role_operational_end_date;
ALTER TABLE roles
  ADD COLUMN role_legal_start_date date;
ALTER TABLE roles
  ADD COLUMN role_legal_end_date date;

ALTER TABLE organisations
  ADD COLUMN organisation_legal_start_date date;
ALTER TABLE organisations
  ADD COLUMN organisation_legal_end_date date;
ALTER TABLE organisations
  ADD COLUMN organisation_operational_start_date date;
ALTER TABLE organisations
  ADD COLUMN organisation_operational_end_date date;

ALTER TABLE relationships
  ADD COLUMN relationship_legal_start_date date;
ALTER TABLE relationships
  ADD COLUMN relationship_legal_end_date date;
ALTER TABLE relationships
  ADD COLUMN relationship_operational_start_date date;
ALTER TABLE relationships
  ADD COLUMN relationship_operational_end_date date;
ALTER TABLE relationships
  ADD COLUMN relationship_unique_id character varying(10);
ALTER TABLE relationships
  ADD COLUMN relationship_status character varying(10);


ALTER TABLE relationships DROP COLUMN target_ref;


ALTER TABLE addresses
  ADD COLUMN streetAddressLine3 text;
ALTER TABLE addresses
  ADD COLUMN "LocationId" character varying(12);


UPDATE settings SET value = '006' WHERE key = 'schema_version';
