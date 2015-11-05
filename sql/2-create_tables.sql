-- Table: versions

-- DROP TABLE versions;

CREATE TABLE versions
(
  version_ref uuid NOT NULL,
  import_timestamp timestamp with time zone NOT NULL,
  publication_date date,
  publication_seqno integer,
  file_version character varying(10),
  publication_type character varying(10),
  CONSTRAINT versions_pk PRIMARY KEY (version_ref)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE versions
  OWNER TO dev;



-- Table: roles

-- DROP TABLE roles;

CREATE TABLE roles
(
  version_ref uuid NOT NULL,
  organisation_ref uuid NOT NULL,
  role_ref uuid NOT NULL DEFAULT uuid_generate_v4(),
  role_code character varying(10) NOT NULL,
  org_odscode character varying(10),
  CONSTRAINT roles_pk PRIMARY KEY (role_ref)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE roles
  OWNER TO dev;



-- Table: relationships

-- DROP TABLE relationships;

CREATE TABLE relationships
(
  version_ref uuid NOT NULL,
  organisation_ref uuid NOT NULL,
  target_ref uuid,
  relationship_code character varying(10),
  relationship_ref uuid NOT NULL DEFAULT uuid_generate_v4(),
  target_odscode character varying(10),
  org_odscode character varying(10),
  CONSTRAINT relationships_pk PRIMARY KEY (relationship_ref)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE relationships
  OWNER TO dev;



-- Table: register_ods_organisations

-- DROP TABLE register_ods_organisations;

CREATE TABLE register_ods_organisations
(
  seq_no serial NOT NULL,
  data_jsonb jsonb,
  CONSTRAINT pk PRIMARY KEY (seq_no)
)
WITH (
  OIDS=TRUE
);
ALTER TABLE register_ods_organisations
  OWNER TO dev;

-- Index: json_idx

-- DROP INDEX json_idx;

CREATE INDEX json_idx
  ON register_ods_organisations
  USING gin
  ((data_jsonb -> 'code'::text));




-- Table: organisations

-- DROP TABLE organisations;

CREATE TABLE organisations
(
  version_ref uuid NOT NULL,
  organisation_ref uuid NOT NULL DEFAULT uuid_generate_v4(),
  org_odscode character varying(10),
  org_name character varying(200),
  org_status character varying(10),
  org_recordclass character varying(10),
  org_lastchanged date,
  CONSTRAINT organisations_pk PRIMARY KEY (organisation_ref)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE organisations
  OWNER TO dev;



-- Table: codesystems

-- DROP TABLE codesystems;

CREATE TABLE codesystems
(
  codesystem_ref uuid NOT NULL DEFAULT uuid_generate_v4(),
  codesystem_name character varying(50),
  codesystem_id character varying(10),
  codesystem_displayname character varying(200),
  version_ref uuid NOT NULL,
  CONSTRAINT codesystems_pk PRIMARY KEY (codesystem_ref)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE codesystems
  OWNER TO dev;



-- Table: addresses

-- DROP TABLE addresses;

CREATE TABLE addresses
(
  version_ref uuid NOT NULL,
  address_ref uuid NOT NULL DEFAULT uuid_generate_v4(),
  organisation_ref uuid NOT NULL,
  "streetAddressLine1" text,
  "streetAddressLine2" text,
  town text,
  county text,
  postal_code text,
  country text,
  CONSTRAINT addresses_pk PRIMARY KEY (address_ref)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE addresses
  OWNER TO dev;
