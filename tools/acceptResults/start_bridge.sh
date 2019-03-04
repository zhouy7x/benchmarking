#!/bin/bash
export BASEDIR=/home/benchmark

cd $BASEDIR/benchmarking/tools/acceptResults

$BASEDIR/node-v4.4.6-linux-x64/bin/node bridge.js > $BASEDIR/logs/accept.log
