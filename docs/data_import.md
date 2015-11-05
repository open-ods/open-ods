# Importing ODS Data Into PostgreSQL

### Pre-requisites
* Runningn instance of PostgreSQL
* A way of running SQL queries against PostgreSQL (I use psql or  [pgAdmin](http://www.pgadmin.org/download/macosx.php))
* All setup steps in the main README must have been completed

### Steps

1. Execute the SQL scripts in the **sql** folder of the repository in the order they are numbered:

  ```bash
  $ cd repo/sql

  $ psql -f 000-create_user_and_database.sql -U postgres

  $ psql -f 001_install_extensions.sql openods -U postgres

  $ psql -f 002-create_tables.sql openods -U postgres

  $ psql -f 00x-etc.sql openods -U postgres
  ```

2. In the terminal, navigate to the data sub-directory of the repository and ensure that both `odsfull.xml.zip` and `import_ods_xml.py` files are present in the directory

    ```bash
    $ cd repo/data

    $ ls
    ```

3. Run the import script:

    ```bash
    $ python import_ods_xml.py

    Starting data import
    Connected to database
    New Version Ref is: 11c4f5ed-e0b7-4b3e-9e3f-6b156333d0a6
    202637
    0.0.0.1
    2015-10-08
    116
    Full
    A full file of all organisations
    Starting import
    Import took 363.49907088279724s
    Import Complete.
    ```
