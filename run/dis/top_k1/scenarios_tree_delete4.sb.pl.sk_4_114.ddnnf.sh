#!/bin/bash
#SBATCH --partition=socket_C
#SBATCH --time=00:10:00
python3.8 ../topk.py 1 scenarios_tree_delete4.sb.pl.sk_4_114
