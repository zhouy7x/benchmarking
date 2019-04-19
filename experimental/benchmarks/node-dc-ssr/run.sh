#!/bin/bash

NODEPATH=${NODE: :-5}
export PATH=$NODEPATH:$PATH
which node

# run bench
rm -f report.temp
bash run-dc-ssr.sh | tee report.temp


