#!/bin/bash

# Usage:
# build.sh volumepath registryhostname targethostname

VOLUME_PATH=${1:-/docker-data/openods-postgres-data}
REGISTRY_HOST=$2
TARGET_HOST=$3

# Parameters can be set via environment variables (or locally scoped variables in the
# call to this script - e.g. `DB=blah deploy-openods.sh`), which will be passed through
# into the container
DB=${DB:-openods}
DB_USER=${DB_USER:-openods}
DB_PASSWORD=${DB_PASSWORD:-openods}
CONTAINER_NAME=${CONTAINER_NAME:-openods-postgres}
POSTGRES_IMAGE=${POSTGRES_IMAGE:-postgres:9.6}

if [ -z $TARGET_HOST ]
then
  TARGET_PREFIX=""
else
  TARGET_PREFIX="--tlsverify -H $TARGET_HOST:2376"
fi

if [ -z $REGISTRY_HOST ]
then
  # No private docker registry
  REGISTRY_PREFIX=""
  SOURCE_URL=$POSTGRES_IMAGE
else
  # Registry specified, so use it
  REGISTRY_PREFIX="--tlsverify -H $REGISTRY_HOST:2376"
  SOURCE_URL=$REGISTRY_HOST:5000/$POSTGRES_IMAGE

  echo "Ensure the postgres image is in our registry, and if not add it"
  ./populateImageIntoRegistry.sh $POSTGRES_IMAGE $REGISTRY_HOST
fi

MEMORYFLAG=750m
CPUFLAG=768

echo "Pull and run postgres"
docker $TARGET_PREFIX stop $CONTAINER_NAME
docker $TARGET_PREFIX rm $CONTAINER_NAME
docker $TARGET_PREFIX run --name $CONTAINER_NAME \
	--restart=on-failure:5 \
        -m $MEMORYFLAG \
	-c $CPUFLAG \
	-v $VOLUME_PATH:/var/lib/postgresql/data \
	-e POSTGRES_DATABASE=$DB \
	-e POSTGRES_USER=$DB_USER \
	-e POSTGRES_PASSWORD=$DB_PASSWORD \
	-e PGDATA=/var/lib/postgresql/data/pgdata \
	-d $SOURCE_URL


