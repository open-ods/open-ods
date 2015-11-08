ALTER TABLE roles
  ADD COLUMN role_unique_id character varying(10);
ALTER TABLE roles
  ADD COLUMN role_status character varying(10);
ALTER TABLE roles
  ADD COLUMN role_start_date date;
ALTER TABLE roles
  ADD COLUMN role_end_date date;
UPDATE settings SET value = '005' WHERE key = 'schema_version';
