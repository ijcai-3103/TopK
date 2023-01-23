#!/bin/sh

python3 compile.py $2 &
wait
python3 topk.py $1
wait
python3 run_maxsat.py $1
