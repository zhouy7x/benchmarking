#!/bin/bash
export BASEDIR=/home/benchmark
export HOME=$BASEDIR
export PATH=$BASEDIR/node/bin:$PATH
cd $BASEDIR/benchmarking/tools/acceptResults
node bridge.js "10.239.44.15" 
