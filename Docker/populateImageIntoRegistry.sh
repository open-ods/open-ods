#!/bin/bash

# Script based on one taken from here: http://stackoverflow.com/questions/24409846/docker-check-private-registry-image-version

# Usage:
# populateImageIntoRegistry.sh imageName registryhostname

HOST=$2
REGISTRY="localhost:5000"
IMAGE_NAME=$1

IMAGE_ID=`./getRegistryContainerID.sh $IMAGE_NAME $HOST`

if [ -z $HOST ]
then
  PREFIX=""
else
  PREFIX="--tlsverify -H $HOST:2376"
fi

if [ -z "$IMAGE_ID" ]
then
  # Image isn't in the registry, so install it from docker hub
  docker $PREFIX pull $IMAGE_NAME
  docker $PREFIX tag $IMAGE_NAME $REGISTRY/$IMAGE_NAME
  docker $PREFIX push $REGISTRY/$IMAGE_NAME
  docker $PREFIX rmi $IMAGE_NAME
else
  # The image is already in the registry, so nothing to do
  # TODO: Think about whether we want to check the image ID and updating it if a newer version (with the same tag) exists in docker hub
  echo "Image already in registry"
fi

