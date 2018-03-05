#!/bin/bash

export PYTHONPATH=${PWD}

exec python './src/bin/satelite.py' "$@"

