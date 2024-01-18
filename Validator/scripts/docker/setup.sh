#!/bin/bash

echo ""
echo "Building the Validator image ..."
echo ""

docker build -f scripts/docker/ValidatorDockerImage -t validatorfaultageimage .

echo ""
echo "Done!"
echo ""