#!/bin/bash

function optional() {
    if [ -z "${!1}" ]; then
        echo -n "${1} not set (ok)"
        if [ -n "${2}" ]; then
            echo -n ", default is: ${2}"
            export ${1}="${2}"
        fi
        echo ""
    fi
}

NODEPATH=${NODE: :-5}
export PATH=$NODEPATH:$PATH
which node

optional RUNS 3
rm -f report.temp

for ((i=1;i<=$RUNS;i++));
do
    node web_tooling_benchmark.js | tee -a report.temp
    echo ""
    sleep 1
done
