#!/bin/bash

mv out/Release/node ./node-master

# build pr
case $USE_CASE in
1)
        curl https://patch-diff.githubusercontent.com/raw/nodejs/node/pull/${PULL_ID}.patch|git apply
        ;;
2)
        git checkout $TARGET
        ;;
esac
./configure > ../node-pr-build.log
make -j${MACHINE_THREADS} >> ../node-pr-build.log
mv out/Release/node ./node-pr
if [ -n "$FILTER" ]; then
        FILTER="--filter ${FILTER}"
fi
if [ -n "$RUNS" ]; then
        RUNS="--runs ${RUNS}"
fi
# run benchmark
fileName=output`date +%d%m%y-%H%M%S`.csv
echo "Output will be saved to $fileName"
pwd
./node-master benchmark/compare.js --old ./node-master --new ./node-pr $FILTER $RUNS -- $CATEGORY | tee $fileName

cat $fileName | Rscript benchmark/compare.R
mv $fileName $startDir

