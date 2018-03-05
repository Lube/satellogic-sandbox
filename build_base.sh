#!/bin/bash

export PYTHONPATH=${PWD}

trap 'kill %1;' SIGINT
{ python3 './src/bin/terran_base.py' & python3 './src/bin/web_server.py'; } 


