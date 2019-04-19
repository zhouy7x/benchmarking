#!/bin/bash

NODEPATH=${NODE: :-5}
export PATH=$NODEPATH:$PATH
which node

# run bench
bash run-dc-eis.sh | tee report.temp


