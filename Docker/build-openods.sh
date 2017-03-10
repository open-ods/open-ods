#!/bin/bash

# Usage:
# build-openods.sh registryhostname

REGISTRY_HOST=$1
IMAGE_NAME=openods

REGISTRY_URL=$REGISTRY_HOST:5000

if [ -z $REGISTRY_HOST ]
then
  REGISTRY_PREFIX=""
else
  REGISTRY_PREFIX="--tlsverify -H $REGISTRY_HOST:2376"
fi

# Build the OpenODS container image
set -e # Stop on error
docker $REGISTRY_PREFIX build -t $IMAGE_NAME ../.

# If we are using a private registry, push the image into it
if [ ! -z $REGISTRY_HOST ]
then
	docker $REGISTRY_PREFIX tag $IMAGE_NAME $REGISTRY_URL/$IMAGE_NAME
	docker $REGISTRY_PREFIX push $REGISTRY_URL/$IMAGE_NAME
	docker $REGISTRY_PREFIX rmi $IMAGE_NAME
fi

