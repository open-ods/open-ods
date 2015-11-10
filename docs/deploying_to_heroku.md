# Deploying To Heroku [IN PROGRESS]

The following instructions will get you set up with a Heroku app running open-ods building automatically when you do a 
`git push heroku master` from your local git repository.

## Pre-requisites

* You already have the open-ods repository cloned onto your dev machine
* You already have open-ods running locally on your dev machine
* You have the Heroku Toolbelt CLI installed and working on your dev machine

## Creating a Heroku deployment of open-ods

1. In your Heroku dashboard, create a new app and give it a meaningful name (e.g. openods-test)

2. Link your local repository to your Heroku app with:

        heroku git:remote -a <heroku_app_name>

3. Next step...


### Migrating your Postgres database to your Heroku app

1. Export the data from your local PostgreSQL database

    ```bash
    pg_dump -Fc --no-acl --no-owner -h localhost -U postgres openods > openods.dump
    ```

2. Upload the dump file to a web server which can be accessed from Heroku (e.g. Amazon S3)

3. Import the data to the remote PostgreSQL database from the URL using the Heroku Toolbelt CLI

    ```bash
    heroku pg:backups restore 'https://s3.amazonaws.com/openods-assets/database_backups/openods006.dump' DATABASE_URL
    ```
