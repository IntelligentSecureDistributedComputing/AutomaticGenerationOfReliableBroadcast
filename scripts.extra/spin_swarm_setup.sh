#!/bin/bash

echo ""
echo "Compiling Swarm..."
echo ""
cd ../../Validator/utils/Swarm/Src/
make clean
make linux
echo ""
echo "Done!"
echo ""
