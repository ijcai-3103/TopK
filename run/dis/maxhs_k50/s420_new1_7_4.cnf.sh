#!/bin/bash
#SBATCH --partition=socket_C
#SBATCH --time=00:10:00
python3.8 ../run_maxsat.py 50 s420_new1_7_4
