#!/usr/bin/env python

import os
import io
import sys
import random
import math
from threading import Timer
import json
import time, subprocess

k = int(sys.argv[1])

def save_dict(dic,path,indent=4):
    with open(path, 'w') as fp:
        json.dump(dic, fp, indent=indent)

def load_dict(path):
    if os.path.exists(path):
        with open(path, 'r') as fp:
            return json.load(fp)
    return {}

def runMaxHS(file_in, timeout):
    timeStarted = time.time()
    process = subprocess.Popen(["./prog/maxhs","-printSoln",file_in], stdout=subprocess.PIPE)
    timer = Timer(timeout, process.kill)
    try:
        res = "UNSATISFIABLE"
        sol = ""
        timer.start()
        out = io.TextIOWrapper(process.stdout)
        for line in out:
            if line.startswith("s "):
                res = line.split("s ")[1].split("\n")[0]
            if line.startswith("v "):
                sol = line
        timer.cancel()
        process.kill()
        process.wait()
        delta = time.time()-timeStarted
        if res == "UNSATISFIABLE":
            return (delta,[])
        if res == "UNKNOWN":
            return (delta,"UNKNOWN")
        
        sol = sol.split("v ")[1].split("\n")[0]
        sol = [x+1 for x in range(0,len(sol)) if sol[x]=="1"]+[-(x+1) for x in range(0,len(sol)) if sol[x]=="0"]
        sol = [" ".join([str(x) for x in sol])]
        delta = time.time()-timeStarted
        return (delta,sol)
    except Exception as e:
        print("Exception: %s" % e)
        process.kill()
        process.wait()
        return (time.time()-timeStarted,"NaN")



    
solvers = {"maxhs":runMaxHS}

def generate_weights_for_computation(nbvar,weights,limit):
    res = {x:v for x,v in weights.items()}
    for i in range(1,nbvar+1):
        if i not in res:
            res[i]=random.randint(1,limit)
        if -i not in res:
            res[-i]=random.randint(1,limit)

    return res


def create_min_wcnf(nbvar,hard_clauses,output_file,weights):
    top = math.ceil(sum(weights.values()))+1

    new_clauses =  ["%d %s\n" %(top,x.strip()) for x in hard_clauses if "0" in x]
    new_clauses = ["%d %d 0\n" % (weights[x],x) for x in weights] + new_clauses

    new_command = "p wcnf %d %d %d" % (nbvar,len(new_clauses),top)    
    with open(output_file,'w') as f:
        f.write("%s\n" % new_command)
        for x in new_clauses:
            f.write("%s" % x)
    
    return output_file

def sol_to_clause(sol):
    children = set()
    for s in sol:
        for v in s.split(" "):
            if v!="0":
                if v[0]=="-":
                    children.add(v[1:])
                else:
                    children.add("-%s" % v)
    return " ".join(children)

#benchmark = sys.argv[2]
benchmark = "in"

for solver in solvers:
    stat_data_path = os.path.join("out","top%s_config_%s" % (k,solver))
    if not os.path.exists(stat_data_path):
        os.makedirs(stat_data_path)


    for filename in [sys.argv[2]]:
        print("Solving %s/%s with solver %s" % (benchmark,filename,solver))
        model = "%s/%s.cnf" % (benchmark,filename)
        tmp_file = "out/tmp_maxsat_%s_%d.wcnf" % (benchmark,random.randint(1,1000000000))

        limit = 1000000
        for i in range(1): 
            data = {}
            ite = 0
            if os.path.exists(os.path.join(stat_data_path,"%s.json" % (filename))):
                data = load_dict(os.path.join(stat_data_path,"%s.json" % (filename)))  
                ite = max([int(x) for x in data.keys()])+1
                if ite>=5:
                    break

            timeout = 10*60
            timeStarted = time.time()
                
            sentence = open(model).readlines()
            sentence = [x for x in sentence if not x.startswith('c')]
            problem = [x for x in sentence if x.startswith('p')][0]
            var = int(problem.split(" ")[2])
            clauses = [x for x in sentence if not x.startswith('p')]
            weights = generate_weights_for_computation(var,{},limit)

    

            data[ite] = []
            for i in range(k):
                create_min_wcnf(var,clauses,tmp_file,weights)
                (delta,sol) = runMaxHS(tmp_file,timeout)
                timeout = max([0,timeout-delta])
                if sol == "UNKNOWN":
                    data[ite].append("UNKNOWN")
                    break
                if sol == "NaN":
                    data[ite].append("NaN")
                    break
                if len(sol)!=0:
                    data[ite].append(time.time()-timeStarted)
                if len(sol)==0:
                    data[ite].append(time.time()-timeStarted)
                    data[ite].append("UNSAT")
                    break
                if timeout == 0:
                    data[ite].append("TimeOut")
                    break
                       
                clauses.append("%s 0\n" % sol_to_clause(sol))
            
            tmp = load_dict(os.path.join(stat_data_path,"%s.json" % (filename))) 
            if ite not in tmp:
                tmp[ite] = data[ite]
                data = tmp                       
            os.remove(tmp_file)
            save_dict(data,os.path.join(stat_data_path,"%s.json" % (filename)))



