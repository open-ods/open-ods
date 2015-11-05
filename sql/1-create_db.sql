CREATE ROLE dev WITH PASSWORD 'dev' LOGIN;

-- Database: ods
CREATE DATABASE ods
  WITH OWNER = dev
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_US.UTF-8'
       LC_CTYPE = 'en_US.UTF-8'
       CONNECTION LIMIT = -1;

CREATE EXTENSION "uuid-ossp";