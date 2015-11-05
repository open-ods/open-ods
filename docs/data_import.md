# Importing ODS Data Into PostgreSQL

### Pre-requisites
* Instance of PostgreSQL
* A way of running SQL queries against PostgreSQL (I use [pgAdmin](http://www.pgadmin.org/download/macosx.php))
* All setup steps in the main README completed

### Steps

1. Execute the SQL scripts in the **sql** folder of the repository in the order they are numbered.

  Make sure each script runs without errors before moving onto the next one.

2. In the terminal, navigate to the data sub-directory of the repository e.g.

    ```bash
    cd ~/Source/open-ods/data
    ```

3. Ensure that both **odsfull.xml.zip** and **import_ods_xml.py** files are present in the directory

4. Run the import script

    ```bash
    python import_ods_xml.py
    ```
