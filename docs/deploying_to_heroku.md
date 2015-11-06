# Deploying To Heroku


### To Migrate Data to Heroku

1. Export the data from your local PostgreSQL database

  ```bash
  PGPASSWORD=dev pg_dump -Fc --no-acl --no-owner -h localhost -U dev ods > ods.dump
  ```

2. Import the data to the remote PostgreSQL database

  ```bash
  heroku pg:backups restore 'https://s3-eu-west-1.amazonaws.com/openods/ods.dump' DATABASE_URL
  ```
