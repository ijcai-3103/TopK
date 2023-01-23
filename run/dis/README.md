# TopK
This tool first encodes a CNF into a dDnnf representation and then computes the topk solutions for such representations.

## Prerequisite
This code only runs on a Linux-based system. It requires Python 3 and the d4 compiler.

### Get d4

1. Clone the repository.
2. Download the source code of the [d4 Compiler](https://github.com/crillab/d4).
3. Move to the downloaded folder and compile the d4 source code using the following commands 

```
make -j8
./d4 --help
```

If you are facing issues during the compilation, you are probably missing some required dependencies.
Install these dependencies based on compilation error messages. In particular, running the following command may help :

```
sudo apt-get install libboost-all-dev libgmp-dev libz-dev
```

Once compiled, move the d4 executable file to the [prog](/prog) repository.

### Setup

Run the following command to create necessary symbolic links 

```
mkdir -p out ; for i in compilation `ls -d maxhs_k* top_k*`; do cd $i; ln -s ../out out; ln -s ../in in; ln -s ../prog prog; cd .. ; done
```

## Usage
To distribute jobs over the cluster, you can rely on [Slurm](https://slurm.schedmd.com/documentation.html) and run

```
sbatch -p partition_name script_name.sh (partition_name dépend du cluster).
````

where *partition_name* has to match the related cluster name.

This command produces an */out* folder containing all computed dDNNF files, as well as the d4 compilation and topk computation statistics.
