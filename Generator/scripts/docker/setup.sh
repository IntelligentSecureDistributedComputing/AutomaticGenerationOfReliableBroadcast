#!/bin/bash

echo ""
echo "Building the Generator image ..."
echo ""

docker build -f scripts/docker/GeneratorDockerImage -t generatorfaultageimage .

echo ""
echo "Done!"
echo ""