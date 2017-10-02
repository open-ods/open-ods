# Importing OpenODS data to your PostgreSQL instance

## Importing an existing OpenODS database backup

#### 1. Download the ready-made OpenODS database backup file

To make it easier to get started, you can download a pre-populated
Postgres database backup file from here (hosted on AWS S3):

[Download **openods_015_sep17_001.dump** from AWS S3](https://s3.amazonaws.com/openods-assets/database_backups/openods_015_sep17_001.dump)

The number in the filename is incremented every time a new version of
the OpenODS database is created and a new backup file is generated.

_Note: The version number in the backup filename does not correspond to the
database schema version (which is used for database / code compatibility checking)._

#### 2. Create a user role and blank database
You will need to create a new role and blank database on your
Postgres instance.

You can do this by running the following command in your terminal -
run this from the project root:

```bash
psql -f sql/create_user_and_database.sql -U postgres
```

This command uses the psql command line interface to run the commands
in the specified .sql file, with the privileges of the postgres user.

The postgres user admin privileges are needed to allow the creation
of the new role and blank database.

#### 3. Restore the downloaded database backup

With the database backup file downloaded, and the blank database in place,
you can restore the database backup to your instance of Postgres.

From the terminal use the command below (replacing the filename with
the path to the downloaded database backup file):

```bash
pg_restore -d openods ~/Downloads/openods_0xx.dump
```

This command restore the contents of the database backup to your local
Postgres instance, targeting the blank database named 'openods' that was
created in the previous step.


#### Importing directly from source XML data files

To import data from the original ODS XML source files,
you can use the OpenODS Import Tool which can be found here:

[OpenODS Import Tool on Github](https://github.com/open-ods/import_tool)

_Note: The import tool is a separate codebase to the main OpenODS API, and such
it makes this step slightly more complicated than using the provided
pre-imported database backup._