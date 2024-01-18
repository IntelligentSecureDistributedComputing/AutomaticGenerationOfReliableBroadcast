#!/bin/bash

echo ""
echo "Cleaning Validator docker image..."
echo ""

echo "Y" | docker system prune --volumes
docker rmi validatorfaultageimage

echo ""
echo "Done!"
echo ""