#!/bin/sh

import os
import sys
import subprocess
import time
import json
import math
import random
import argparse

pathGitkeep = os.path.join('in','.gitkeep')
if os.path.exists(pathGitkeep):
    os.remove(pathGitkeep)

def save_dict(dic,path,indent=4):
    with open(path, 'w') as fp:
        json.dump(dic, fp, indent=indent)

def load_dict(path):
    if os.path.exists(path):
        with open(path, 'r') as fp:
            return json.load(fp)
    return {}

def compile(file_in,file_out,timeout):
    timeStarted = time.time()
    process = subprocess.Popen(["./prog/d4","-dDNNF","-out=%s" % file_out,file_in], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        process.wait(timeout=timeout)
        stdout, stderr = process.communicate()
        out = stdout.decode()
        var = int(out.split("Number of variables: ")[1].split("\n")[0])
        cl = int(out.split("Number of clauses: ")[1].split("\n")[0])
        lit = int(out.split("Number of literals: ")[1].split("\n")[0])
        delta = time.time()-timeStarted
        nb = out.split("\ns ")[1].split('\n')[0]
        return (var,cl,lit,delta,nb)
    except subprocess.TimeoutExpired:
        process.terminate()
        stdout, stderr = process.communicate()
        print("%s:\n%s" % (file_in,stderr.decode()))
        process.wait()
        if os.path.exists(file_out):
            os.remove(file_out)
        return "NaN"

if len(sys.argv) > 1:
    timeout = int(sys.argv[1])
else:
    timeout = 20*60
print ("timeout: %s seconds" % timeout)

out_path = os.path.join('out','dDNNF')
if not os.path.exists(out_path):
    os.makedirs(out_path)
stat_data_path = os.path.join("out","d4_compilation_stats")
if not os.path.exists(stat_data_path):
    os.makedirs(stat_data_path)


for filename in [x.split('.cnf')[0] for x in os.listdir('./in')]:
    if not os.path.exists(os.path.join(stat_data_path,"%s.json" % filename)):
        data={}
        file_in = os.path.join('./in',"%s.cnf"%filename)
        file_out = os.path.join(out_path,"%s.ddnnf" % filename)
        if not os.path.exists(file_out):
            (var,cl,lit,delta,count) = compile(file_in,file_out,timeout)
            data["Number of variables"] = var
            data["Number of clauses"] = cl
            data["Number of literals"] = lit
            data["Compilation time"] = delta
            data["Number of models"] = count
            save_dict(data,os.path.join(stat_data_path,"%s.json" % filename))
