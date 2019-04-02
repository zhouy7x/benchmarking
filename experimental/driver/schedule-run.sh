#!/bin/bash

# Protocol for stopping V8onXeon:
#
# (1) If you want to stop it immediately:
#TODO
#
# (2) If you want to stop it when possible:
#TODO


# check if script already run.
if [ -e /tmp/v8onxeon-daemon ]
then
  echo "v8onxeon: Already running"
  exit 0
fi

# create a run lock.
touch /tmp/v8onxeon-daemon

trap "kill 0" EXIT

pushd /home/benchmark/benchmarking/experimental/driver
#python print_env.py

LOGDIR=$HOME/logs
datename=$(date +%Y%m%d-%H%M%S)
echo -e "Start time: `date`"
# 1. start data-collect machine and nginx web server.
#$HOME/node-v4.4.6-linux-x64/bin/node $HOME/benchmarking/tools/acceptResults/bridge.js > $LOGDIR/acceptResults/$datename.log 2>&1 &
#TODO start nginx.

# 2. run dostuff.py.
python dostuff.py --branch=master --benchmark=all --postdata=True > $LOGDIR/dostuff-$datename.log 2>&1

# 3. run chartcron.sh, update web image and html.
a=`cat $LOGDIR/dostuff-$datename.log | grep "all over."` 
echo $a
if [ -n "`cat $LOGDIR/dostuff-$datename.log | grep 'all over.'`" ] ;then
    echo "get keyword 'all over.', run chartcron.sh... ";
    bash $HOME/benchmarking/tools/chartGen/chartcron.sh;
fi

# remove run lock.
rm /tmp/v8onxeon-daemon

echo -e "Stop time: `date`"







