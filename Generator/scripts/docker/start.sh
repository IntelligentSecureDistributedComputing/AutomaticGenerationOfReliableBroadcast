#!/bin/bash

echo ""
echo "Starting Generator docker container..."
echo ""

cd scripts/docker/
docker-compose up

echo ""
echo "Done!"
echo ""