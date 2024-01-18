#!/bin/bash

echo ""
echo "Creating Python environment..."
echo ""
python3.10 -m venv generator_env
generator_env/bin/python -m pip install -r scripts/local/requirements.txt
echo ""
echo "Done!"
echo ""


echo ""
echo "Creating the env file..."
echo ""
echo '# generator component hostname
GENERATOR_HOST=127.0.0.1
# generator component port
GENERATOR_PORT=5001
# validator component hostname
VALIDATOR_HOST=127.0.0.1
# validator component port
VALIDATOR_PORT=5002 ' > .env
echo ""
echo "Done!"
echo ""

