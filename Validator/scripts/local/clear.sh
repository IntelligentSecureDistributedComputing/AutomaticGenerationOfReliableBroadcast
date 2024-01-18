#!/bin/bash

echo ""
echo "Deleting the python environment..."
echo ""
rm -r validator_env
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
echo "Deleting the inputs..."
echo ""
rm inputs/current_validation_inputs.json
echo ""
echo "Done!"
echo ""

echo ""
echo "Deleting the models..."
echo ""
rm services/Promela/Validation_Tests/*
echo ""
echo "Done!"
echo ""