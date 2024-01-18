#!/bin/bash

echo ""
echo "Creating client python environment..."
echo ""
python3.10 -m venv client_env
client_env/bin/python -m pip install -r scripts/local/requirements.txt
echo ""
echo "Done!"
echo ""

echo ""
echo "Creating the client env file..."
echo ""
echo '# generator component hostname
GENERATOR_HOST = 127.0.0.1
# generator component port
GENERATOR_PORT = 5001
# validator component hostname
VALIDATOR_HOST = 127.0.0.1
# validator component port
VALIDATOR_PORT = 5002
# client component hostname
CLIENT_HOST=127.0.0.1
# client component port
CLIENT_PORT=5003' > .env
echo ""
echo "Done!"
echo ""