# TopK
This tool first encodes a CNF into a dDnnf representation and then computes the topk solutions for such representations.

## Prerequisite
This code only runs on a Linux-based system. It requires Python 3 and the d4 compiler.

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

## Usage

The CNF encoding the models to be tested are located in the [in](/in) repository.

To compute the top k solutions for each model, run 

```
./run.sh k t
```
with *k* the expected number of top solutions and *t* the timeout (in seconds, 600 if not specified).

This command produces an */out* folder containing all computed dDNNF files, as well as the d4 compilation and topk computation statistics.
