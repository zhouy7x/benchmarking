#!/bin/bash

# Protocol for stopping V8onXeon:
#
# (1) If you want to stop it immediately:
#TODO
#
# (2) If you want to stop it when possible:
#TODO

# init.
function optional() {
    if [ -z "${!1}" ]; then
        echo -n "${1} not set (ok)"
        if [ -n "${2}" ]; then
            echo -n ", default is: ${2}"
            export ${1}="${2}"
        fi
    else
        echo -n "${1} set to "${!1}""
    fi
        echo ""
}
getMACHINE_THREADS=`cat /proc/cpuinfo |grep processor|tail -n1|awk {'print $3'}`
let getMACHINE_THREADS=getMACHINE_THREADS+1   # getting threads this way is 0 based. Add one
echo $MACHINE_THREADS
optional MACHINE_THREADS $getMACHINE_THREADS
optional RUNS 3


# download node git repo.
#pushd /home/benchmark/benchmarking/experimental/benchmarks/community-benchmark
#rm -rf node
#git clone http://github.com/nodejs/node.git



if [ -e /tmp/v8onxeon-daemon ]
then
  echo "v8onxeon: Already running"
  exit 0
fi

touch /tmp/v8onxeon-daemon

trap "kill 0" EXIT

python print_env.py


#check if node updated.
if [ -e /tmp/v8onxeon ]
then
    echo "v8onxeon: /tmp/v8onxeon lock in place"
    sleep 1
else

    # First, check node update
    pushd /home/benchmark/benchmarking/experimental/benchmarks/community-benchmark/node
    git fetch
    latest-commit-id=echo `git rev-list origin/master ^master` | awk '{print $!}'
    optional COMMIT-ID $latest-commit-id

    if [ -z "$COMMIT-ID" ]; then
        echo "v8onxeon: no update"
    else

        python dostuff.py --commit-id=$COMMIT-ID

        # build node.
        pwd
        python build_node.py --commit-id=$COMMIT-ID

            git reset --hard -q $COMMIT-ID | tee reset-node.log

            git log -1 --pretty=short


            #build node.
            TODO

            #dostuff



rm /tmp/awfy-daemon-v8








