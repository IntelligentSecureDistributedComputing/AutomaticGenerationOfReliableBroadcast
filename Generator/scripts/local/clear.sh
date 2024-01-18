#!/bin/bash

echo ""
echo "Deleting the python environment..."
echo ""
rm -r generator_env
echo ""
echo "Done!"
echo ""

echo ""
echo "Deleting the env file..."
echo ""
rm .env
echo ""
echo "Done!"
echo ""


echo ""
echo "Deleting the output folder..."
echo ""
rm -r output
echo ""
echo "Done!"
echo ""

echo ""
echo "Deleting the inputs..."
echo ""
rm inputs/current_generation_inputs.json
echo ""
echo "Done!"
echo ""