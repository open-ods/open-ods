## Importing and exporting the database

If you are deploying OpenODS on a vanilla server, you may be able to run the import routine on the server itself (note the routine is RAM heavy).

If you are deploying somewhere where it is not an option to run the import on the server itself (e.g. Heroku or a low-powered VPS) then you will need to run the import on a local machine and then restore the database to your deployed instance.
 
**Remember to always make sure that the schema version of the database you are using matches the expected schema version of the deployed application (see config.py)**

### SQLite
*Note: Can't be used with Heroku deployments*
For SQLite this is really simple:

1. Run the import routine in SQLite mode - this will create the SQLite database file.

    ```bash
    $ python import.py -d sqlite -c sqlite:///openods.db --verbose
    
    Import Completed.
    ```
       
2. Upload the SQLite database file to your production machine.

3. Update the connection string of your deployed instance to point to the new database file.

4. Start / Restart OpenODS


### Postgres
You will need to ensure you have an instance of Postgres installed on the machine that you want to run the import on (Postgres.app is easy and self-contained if you are using OSX).

1. First create an 'openods' role / user on your Postgres server

    ```sql
    TODO: This command needs updating
    psql -c "CREATE ROLE openods"'
    ```
 
2. Now create an empty database (I usually call it 'openods') and set the owner to role you created in the previous step

3. Run the import routine in Postgres mode ensuring the connection string matches the database and role you just created

    ```bash
    $ python import.py -d postgres -c postgresql://openods:openods@localhost/openods --verbose
    
    Import Completed.
    ```
    
You might want to use your preferred database tool to check that the data has imported correctly. 
    
4. From a terminal, run the following command to export the database to a file. This runs an export as the Postgres master user (and so assumes that you have the permissions on the Postgres server to do this).

    ```bash
    $ pg_dump -Fc --no-acl --no-owner -h localhost -U postgres openods > openods.dump
    ```
5. You should now have a .dump (or whatever extension you specified) file containing a compressed backup of your openods database.


#### Restoring to a Heroku instance
If you are using Heroku to host your application, you will need to upload the backup file and restore it to your Postgres add-on.

*Note: This assumes that you have previously linked your local repository to your Heroku instance using Heroku Toolbelt and that you already have a Heroku Postgres add-on attached.*

1. You will first need to make the .dump file available for download over HTTP using something like Amazon S3.

2. Then in a terminal navigate to your local repo

3. Run the following command replacing *<heroku_app_name>* with the name of your heroku app and the URL with the URL of your .dump file:

    ```bash
    $ heroku pg:backups restore -a <heroku_app_name> 'https://url.to/openods.dump' DATABASE_URL
    ```
4. I'd then recommend doing a `heroku -a <heroku_app_name> restart` which will cycle your dynos


#### Restoring to a Postgres server
*Note: This assumes that you have a Postgres server setup and configured with the same role / user as used in your source database.

1. As we exported the database using the Postgres custom compressed format, we use the pg_restore command to restore the database from the file:

    ```bash
    $ pg_restore -d openods openods009.dump
    ```
    
2. You could then run the following in the terminal to confirm that the correct version of the database has been restored:

    ```bash
    $ psql -d openods -c 'SELECT * from settings;'
    
          key       | value
    ----------------+-------
     schema_version | 009
    (1 row)
    
    $
    ```