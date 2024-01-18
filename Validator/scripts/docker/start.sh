#!/bin/bash

echo ""
echo "Starting Validator docker container..."
echo ""

cd scripts/docker/
docker-compose up

echo ""
echo "Done!"
echo ""