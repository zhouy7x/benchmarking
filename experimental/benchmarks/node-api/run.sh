#!/bin/bash

NODEPATH=${NODE: :-5}
export PATH=$NODEPATH:$PATH
which node

# run bench
rm -f report.temp
node --max_old_space_size=4096 require/require.perf.js | tee report.temp
