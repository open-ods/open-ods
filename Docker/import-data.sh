#!/bin/bash

# Usage:
# import-data.sh sql_data_dump_file

# Note: This is a script to load an exported set of ODS data into the database - it does not use the importer!
# This script should be run directly on the target host running the postgres container

DATA_FILE=$1

DB_CONTAINER_NAME=${DB_CONTAINER_NAME:-openods-postgres}
DB=${DB:-openods}
DB_USER=${DB_USER:-openods}
DB_PASSWORD=${DB_PASSWORD:-openods}
DROP_EXISTING=${DROP_EXISTING:-true}

echo "Importing data into database"
cp $DATA_FILE ./dataloader/data.sql
docker build -t openods-data-import dataloader/.
rm ./dataloader/data.sql

docker run -it \
	--link $DB_CONTAINER_NAME:openods-postgres \
	-e "DB=$DB" \
	-e "DB_USER=$DB_USER" \
	-e "DB_PASSWORD=$DB_PASSWORD" \
	-e "DROP_EXISTING=$DROP_EXISTING" \
	openods-data-import

