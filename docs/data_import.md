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

2. Open DataBaseSetup.py in your code editor and find the line configuring the SQL engine - configure it either for Postgres or SQLite:

    ```python
    engine = create_engine('sqlite:///openods.sqlite', echo=True)
    
    engine = create_engine(
    "postgresql://openods:openods@localhost/openods", isolation_level="READ UNCOMMITTED")
    ```


3. From the root of your repo directory, run the database import script

    ```bash
    $ python controller/DataBaseSetup.py
    
    Starting import
    Import took 00:04:12
    
    Schema version is 008
    
    $ 
    ```