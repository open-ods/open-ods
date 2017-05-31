#!/bin/bash

# Usage:
# deploy-openods.sh registryhostname targethostname

# The registryhostname and targethostname can be left blank if not being used
REGISTRY_HOST=$1
TARGET_HOST=$2
IMAGE_NAME=openods

# Parameters can be set via environment variables (or locally scoped variables in the
# call to this script - e.g. `DB=blah deploy-openods.sh`), which will be passed through
# into the container

# Database Settings
DATA_CONTAINER=${DATA_CONTAINER:-openods-postgres}
DB=${DB:-openods}
DB_USER=${DB_USER:-openods}
DB_PASSWORD=${DB_PASSWORD:-openods}
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DATA_CONTAINER:5432/$DB

# App Settings
CACHE_TIMEOUT=${CACHE_TIMEOUT:-30}
LIVE_DEPLOYMENT=${LIVE_DEPLOYMENT:-FALSE}
INSTANCE_NAME=${INSTANCE_NAME:-Development}
APP_HOSTNAME=${APP_HOSTNAME:-localhost:8080/api}
API_URL=${API_URL:-/api}


CONTAINER_NAME=${CONTAINER_NAME:-openods}

if [ -z $TARGET_HOST ]
then
  TARGET_PREFIX=""
else
  TARGET_PREFIX="--tlsverify -H $TARGET_HOST:2376"
fi

if [ -z $REGISTRY_HOST ]
then
  REGISTRY_PREFIX=""
  SOURCE_URL=$IMAGE_NAME
else
  REGISTRY_PREFIX="--tlsverify -H $REGISTRY_HOST:2376"
  SOURCE_URL=$REGISTRY_HOST:5000/$IMAGE_NAME
  docker $TARGET_PREFIX pull $SOURCE_URL
fi

MEMORYFLAG=750m
CPUFLAG=768

echo "Pull and run OpenODS"
docker $TARGET_PREFIX stop $CONTAINER_NAME
docker $TARGET_PREFIX rm $CONTAINER_NAME
docker $TARGET_PREFIX run -p 8083:8080 --name $CONTAINER_NAME \
	--restart=on-failure:5 \
        -m $MEMORYFLAG \
	-c $CPUFLAG \
	--link $DATA_CONTAINER:$DATA_CONTAINER \
	-e "DATABASE_URL=$DATABASE_URL" \
	-e "LIVE_DEPLOYMENT=$LIVE_DEPLOYMENT" \
	-e "INSTANCE_NAME=$INSTANCE_NAME" \
	-e "API_PATH=$API_PATH" \
	-e "APP_HOSTNAME=$APP_HOSTNAME" \
        -e "FT_SUPPRESSPRIMARYROLESEARCHLINK=$FT_SUPPRESSPRIMARYROLESEARCHLINK" \
	-d $SOURCE_URL

