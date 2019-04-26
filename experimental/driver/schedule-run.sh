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
accept_pid="`ps aux | grep bridge.js | grep "/node " | grep -v grep | awk {'print $2'}`"
echo $accept_pid
if [ -z "$accept_pid" ] ;then
    echo "start bridge.js...";
    $HOME/node-v4.4.6-linux-x64/bin/node $HOME/benchmarking/tools/acceptResults/bridge.js > $LOGDIR/acceptResults/$datename.log 2>&1 &
else
    echo -e "bridge.js already exists, pid: $accept_pid";
fi
#TODO start nginx.

# 2. run dostuff.py.
python dostuff.py --machine=0 --benchmark=all --postdata=true > $LOGDIR/dostuff-$datename.log 2>&1

# 3. run chartcron.sh, update web image and html.
if [ -n "`cat $LOGDIR/dostuff-$datename.log | grep 'all over.'`" ] ;then
    echo "get keyword 'all over.', run chartcron.sh... ";
    bash $HOME/benchmarking/tools/chartGen/chartcron.sh;
fi

# remove run lock.
rm /tmp/v8onxeon-daemon

echo -e "Stop time: `date`"







