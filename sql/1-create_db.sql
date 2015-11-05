-- You will need to do the following as the Postgres user (or another superuser)
CREATE ROLE dev WITH PASSWORD 'dev' LOGIN;

-- Database: ods
CREATE DATABASE ods
  WITH OWNER = dev
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_US.UTF-8'
       LC_CTYPE = 'en_US.UTF-8'
       CONNECTION LIMIT = -1;


-- Make sure you are connected to the new database you just created before installing these extensions
CREATE EXTENSION "uuid-ossp";
CREATE EXTENSION "adminpack";