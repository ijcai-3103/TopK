#!/bin/bash
#SBATCH --partition=socket_C
#SBATCH --time=00:10:00
python3.8 ../topk.py 50 GuidanceService2.sk_2_27
