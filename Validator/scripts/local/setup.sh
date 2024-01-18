#!/bin/bash

echo "Creating Python environment..."
echo ""
python3.10 -m venv validator_env
validator_env/bin/python -m pip install -r scripts/local/requirements.txt
echo ""
echo "Done!"
echo ""

echo ""
echo "Installing Spin..."
echo ""
sudo apt-get install spin
echo ""
echo "Done!"
echo ""

echo ""
echo "Creating the env file..."
echo ""
echo '# generator component hostname
GENERATOR_HOST = 127.0.0.1
# generator component port
GENERATOR_PORT = 5001
# validator component hostname
VALIDATOR_HOST = 127.0.0.1
# validator component port
VALIDATOR_PORT = 5002
# validation process data
SPIN_DVECTORSZ = 50000
# BFS validation process data
SPIN_BFS_NUMBER_OF_CORES = 1
SPIN_BFS_HASH_TABLE_SIZE = 28
# DFS validation process data
SPIN_DFS_DMEMLIM = 8000
SPIN_DFS_DVMAX = 3064
SPIN_DFS_DNCORE = 6
# SWARM validation process data
SPIN_SWARM_CORES=6' > .env