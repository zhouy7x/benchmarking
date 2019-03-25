#!/bin/bash
LOGDIR=$HOME/logs
datename=$(date +%Y%m%d-%H%M%S)
# 1. start data-collect machine and nginx web server.
#$HOME/node-v4.4.6-linux-x64/bin/node $HOME/benchmarking/tools/acceptResults/bridge.js > $LOGDIR/acceptResults/$datename.log 2>&1 &
#TODO start nginx.

# 2. run dostuff.py.
#python dostuff.py --branch=master --benchmark=all --postdata=True > $LOGDIR/dostuff-$datename.log 2>&1

# 3. run chartcron.sh, update web image and html.
#if [ -n `cat $LOGDIR/dostuff-$datename.log | grep "all over."` ];
#then
#    echo "get keyword 'all over.', run chartcron.sh... ";
    # bash $HOME/benchmarking/tools/chartGen/chartcron.sh;
#fi


if [ -z $1 ];
#if [ 1 = 1 ] ;
then
    echo "1";
    echo -e "Stop time: `date`"

fi