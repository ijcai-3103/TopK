#!/usr/bin/env python
# coding: utf-8

# # Multithread prototype

# In[1]:

import sys
import os
import subprocess
import time
import json
import math
import random
import argparse

k = int(sys.argv[1])

def save_dict(dic,path,indent=4):
    with open(path, 'w') as fp:
        json.dump(dic, fp, indent=indent)

def load_dict(path):
    if os.path.exists(path):
        with open(path, 'r') as fp:
            return json.load(fp)
    return {}

def enumOpt(file_in,nb_var,nb,limit,timeout):
    timeStarted = time.time()
    process = subprocess.Popen(["java","-Xmx512g","-cp","prog/WINSTON.jar","xps.jss.ddnnf.ComputeTopKSolStats",file_in,str(nb_var),str(nb),str(limit)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        process.wait(timeout=timeout)
        stdout, stderr = process.communicate()
        out = stdout.decode()
        stats = {}
        stats["parsing"] = float(out.split("Parsing time: ")[1].split("\n")[0])
        stats["smoothing"] = float(out.split("Smoothing time: ")[1].split("\n")[0])
        stats["top"] = float(out.split("Top time: ")[1].split("\n")[0])
        stats["total"] = time.time()-timeStarted
        return stats
    except:
        print("Error")
        print("%s:\n%s\n%s" % (file_in,stdout.decode(),stderr.decode()))
        return {"total":"TIMEOUT"}




in_path = os.path.join('out','dDNNF')
compilation_stats_path = os.path.join("out","d4_compilation_stats")
timeout = 2*60



for limit in [1000000]:
    stat_data_path = os.path.join("out","top%s_config_jddnnf" % k)
    if not os.path.exists(stat_data_path):
        os.makedirs(stat_data_path)

    print("limit: %s" % limit)
    for filename in [x.split('.ddnnf')[0] for x in os.listdir(in_path)]:
        print("%s" % filename)
        ddnnf_path = os.path.join(in_path,"%s.ddnnf" % filename)
        cs_path = os.path.join(compilation_stats_path,"%s.json" % filename)
        dest = os.path.join(stat_data_path,"%s.json" % (filename))
        if os.path.exists(ddnnf_path) and os.path.exists(cs_path) and not os.path.exists(dest):
            nb_variables = load_dict(cs_path)["Number of variables"]
            data = {}
            for ite in range(5):
                data[ite] = enumOpt(ddnnf_path,nb_variables,k,limit,timeout)
            save_dict(data, dest)
