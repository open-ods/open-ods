# Importing ODS Data Into OpenODS

### Pre-requisites
* Runningn instance of PostgreSQL
* A way of running SQL queries against PostgreSQL (I use psql or  [pgAdmin](http://www.pgadmin.org/download/macosx.php))
* All setup steps in the main README must have been completed

### Steps

1. Execute the SQL scripts,  which can be found in the sql sub-directory,  from the root folder of your repository as follows:

  ```bash
  $ psql -f sql/create_user_and_database.sql -U postgres
  
  $ psql -d openods -f sql/run_migration_scripts.sql -U postgres
  ```

2. In the terminal, navigate to the data sub-directory of the repository and ensure that both `odsfull.xml.zip` and `import_ods_xml.py` files are present in the directory

    ```bash
    $ ls -l
    
    -rw-r--r--@ 1 matt  staff  19885585  3 Nov 14:56 odsfull.xml.zip
    -rw-r--r--  1 matt  staff  6930  7 Nov 17:53 import_ods_xml.py
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
