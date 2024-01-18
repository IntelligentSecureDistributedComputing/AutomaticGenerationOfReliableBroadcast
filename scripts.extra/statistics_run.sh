#!/bin/bash

cd ..
cloc --by-file --exclude-ext=pyc --exclude-dir=node_modules,__pycache__,docker,misc,react-src,.github .