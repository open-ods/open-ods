#!/bin/sh

FILE="/data/data.sql"

if [ "$DROP_EXISTING" = "true" ]
then
  echo "Dropping existing DB"
  PGPASSWORD=$DB_PASSWORD dropdb -U $DB_USER -h openods-postgres $DB
  echo "Create DB"
  PGPASSWORD=$DB_PASSWORD createdb -U $DB_USER -h openods-postgres $DB
fi

# If we were importing a SQL dump we could use this:
#PSQL="psql -U $USER -h openods-postgres"
#cat $FILE | PGPASSWORD=$PASSWORD $PSQL $DB
#echo "Importing data into Postgres from $FILE"

# Using a raw postgres DB dump, use this:
echo "Importing data into DB: $DB with user: $DB_USER"
PGPASSWORD=$DB_PASSWORD pg_restore -U $DB_USER -h openods-postgres -d $DB $FILE
echo "Import complete"
