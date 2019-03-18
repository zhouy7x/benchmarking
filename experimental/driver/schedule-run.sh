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

python print_env.py

LOGDIR=$HOME/logs
datename=$(date +%Y%m%d-%H%M%S)
# 1. start data-collect machine and nginx web server.
#$HOME/node-v4.4.6-linux-x64/bin/node $HOME/benchmarking/tools/acceptResults/bridge.js > $LOGDIR/acceptResults/$datename.log 2>&1 &
#TODO start nginx.

# 2. run dostuff.py.
python dostuff.py --branch=master --benchmark=all --postdata=True

# 3. run chartcron.sh, update web image and html.
bash $HOME/benchmarking/tools/chartGen/chartcron.sh

# remove run lock.
rm /tmp/v8onxeon-daemon








