## Deploying to Heroku [IN PROGRESS]

The following instructions will get you set up with a Heroku app running open-ods building automatically when you do a 
`git push heroku master` from your local git repository.

### Pre-requisites

* You already have the OpenODS repository cloned onto your dev machine
* You already have OpenODS service running locally on your dev machine
* You have the Heroku Toolbelt CLI installed and working on your dev machine

### Creating a Heroku deployment of OpenODS

1. In your Heroku dashboard, create a new app and give it a meaningful name (e.g. openods-test)

2. Link your local repository to your Heroku app with:

        heroku git:remote -a <heroku_app_name>

3. Next step...


### Migrating your Postgres database to your Heroku app

The easiest way of getting your database deployed to your Heroku app is to following the steps in the [Import Tool - Database Exports](https://github.com/open-ods/import_tool/blob/master/database_exports.md) document.