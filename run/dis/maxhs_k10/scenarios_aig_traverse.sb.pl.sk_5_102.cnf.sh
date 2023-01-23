#!/bin/bash
#SBATCH --partition=socket_C
#SBATCH --time=00:10:00
python3.8 ../run_maxsat.py 10 scenarios_aig_traverse.sb.pl.sk_5_102
