# Importing ODS Data Into OpenODS

### Pre-requisites
* SQLite or PostgreSQL (only PostgreSQL is supported by the API app currently)
* A way of running SQL queries against PostgreSQL (I use psql or [pgAdmin](http://www.pgadmin.org/download/macosx.php))
* All setup steps in the main README should be completed

### Steps

1. Activate your Python 3 virtualenv (if you are using one) and make sure the requirements are all installed

    ```bash
    $ pip install -r requirements.txt
    ```

2. From the root of your repo directory, run the database import script

    ```bash
    $ python import.py
    ```

For details of available arguments, run:

    ```bash
    $ python import.py -h
    ```
    
All of the arguments are optional, and without them the script will just use its default DBMS, file locations, and connection string.