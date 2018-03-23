#!/bin/bash

export PYTHONPATH=${PWD}

trap 'pkill -P $$' EXIT
echo 'Lanzando constelacion de 100 satelites!'
for run in {1..100}
do
  python3 './src/bin/satelite.py'&>/dev/null &
done&>/dev/null
wait
echo 'Deorbitando constelacion!'



