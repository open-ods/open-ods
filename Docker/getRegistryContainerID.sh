#!/bin/bash

# Script based on one taken from here: http://stackoverflow.com/questions/24409846/docker-check-private-registry-image-version

# Usage:
# getRegistryContainerID.sh imageName registryhostname

HOST=$2
REGISTRY="localhost:5000"
IMAGE_NAME=$1

LATEST="`wget -qO- http://$REGISTRY/v1/repositories/$REPOSITORY/tags`"
LATEST=`echo $LATEST | sed "s/{//g" | sed "s/}//g" | sed "s/\"//g" | cut -d ' ' -f2`

if [ -z $HOST ]
then
  PREFIX=""
else
  PREFIX="--tlsverify -H $HOST:2376"
fi

IMAGE_ID=`docker $PREFIX inspect "$REGISTRY/$IMAGE_NAME" 2> /dev/null | grep Id | sed "s/\"//g" | sed "s/,//g" |  tr -s ' ' | cut -d ' ' -f3`

echo $IMAGE_ID

