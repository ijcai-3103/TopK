#!/bin/bash
#SBATCH --partition=socket_C
#SBATCH --time=00:10:00
python3.8 ../run_maxsat.py 20 scenarios_lldelete1.sb.pl.sk_6_409
