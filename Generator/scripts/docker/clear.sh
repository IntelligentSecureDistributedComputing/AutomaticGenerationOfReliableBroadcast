#!/bin/bash

echo ""
echo "Cleaning Generator docker image..."
echo ""

echo "Y" | docker system prune --volumes
docker rmi ubuntu:22.10 generatorfaultageimage

echo ""
echo "Done!"
echo ""