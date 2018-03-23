#!/bin/bash

export PYTHONPATH=${PWD}

exec python3 './src/bin/satelite.py' "$@"

