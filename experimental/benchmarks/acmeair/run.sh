#!/bin/bash

NODEPATH=${NODE: :-5}
export PATH=$NODEPATH:$PATH
which node

# run bench
#bash run_acmeair.sh | tee report.temp


