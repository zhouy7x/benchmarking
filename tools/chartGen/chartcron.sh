#!/bin/bash
export BASEDIR=/home/benchmark
export HOME=$BASEDIR
export PATH=$BASEDIR/node/bin:$PATH
cd $BASEDIR/benchmarking/tools/chartGen/
sh gencharts.sh
rm -rf $BASEDIR/benchmarking/www/charts/*
cp *.png $BASEDIR/benchmarking/www/charts
