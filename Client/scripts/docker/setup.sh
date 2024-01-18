#!/bin/bash

echo ""
echo "Building the Client image ..."
echo ""

docker build -f scripts/docker/ClientDockerImage -t clientfaultageimage .

echo ""
echo "Done!"
echo ""