-- Table: settings

-- DROP TABLE settings;

CREATE TABLE settings
(
  key character varying(20) NOT NULL,
  value character varying(200),
  CONSTRAINT settings_pkey PRIMARY KEY (key)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE settings
  OWNER TO openods;

INSERT INTO settings VALUES ('schema_version', '004');