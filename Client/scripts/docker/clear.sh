#!/bin/bash

echo ""
echo "Cleaning Client docker image..."
echo ""

echo "Y" | docker system prune --volumes
docker rmi clientfaultageimage

echo ""
echo "Done!"
echo ""