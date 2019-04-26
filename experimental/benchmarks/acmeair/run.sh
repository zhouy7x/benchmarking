#!/bin/bash

NODEPATH=${NODE: :-5}
export PATH=$NODEPATH:/opt/jdk1.7.0/bin:$PATH
which node

# run bench
rm -f report.temp
bash run_acmeair.sh | tee report.temp


