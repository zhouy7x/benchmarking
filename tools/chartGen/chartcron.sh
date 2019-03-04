#!/bin/bash
export BASEDIR=/home/benchmark
export HOME=$BASEDIR
export PATH=$BASEDIR/node/bin:$PATH
cd $BASEDIR/benchmarking/tools/chartGen/
sh gencharts.sh
rm $BASEDIR/benchmarking/www/charts/* -rf
cp *.png $BASEDIR/benchmarking/www/charts
