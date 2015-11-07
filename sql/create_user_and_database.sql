-- You will need to do the following as the Postgres user (or another superuser)

-- Create the role for OpenODS login ---
CREATE USER openods WITH PASSWORD 'openods';

--- Create the OpenODS database ---
CREATE DATABASE openods OWNER openods;
