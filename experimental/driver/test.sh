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

# 1. build a node.


# 1.1 download node git repo.
#pushd /home/benchmark/benchmarking/experimental/benchmarks/community-benchmark
#rm -rf node
#git clone http://github.com/nodejs/node.git

#check if node updated.

: '
if [ -e /tmp/v8onxeon-daemon ]
then
  echo "v8onxeon: Already running"
  exit 0
fi

touch /tmp/v8onxeon-daemon

trap "kill 0" EXIT

python print_env.py


count=0
commit=''

if [ -e /tmp/v8onxeon ]
then
    echo "v8onxeon: /tmp/v8onxeon lock in place"
    sleep 1
else
    hasUpdate="false"

    # First, check node update
    pushd /home/benchmark/benchmarking/experimental/benchmarks/community-benchmark/node
    git fetch
    latest-commit-id=echo `git rev-list origin/master ^master` | awk '{print $!}'
    optional COMMIT-ID $latest-commit-id

    if [ -z "$COMMIT-ID" ]; then
        echo "v8onxeon: no update"
    else

        hasUpdate="true"
        # reset node.

            git reset --hard -q $COMMIT-ID
            git log -1 --pretty=short


            #build node.



            ./configure  > ../node-build.log
            make -j${MACHINE_THREADS}  >> ../node-build.log
            rm -rf out/node-v12.0.0-pre/bin/node
            mv out/Release/node out/node-v12.0.0-pre/bin

            sleep 5s


            # run benchmarks
            pushd /home/benchmark/benchmarking/experimental/benchmarks/driver

            STARTT=$(date +%s)

            # run benchmark
            fileName=output`date +%d%m%y-%H%M%S`.csv
            BENCHMARK=octane
            resultFile=result/$BENCHMARK/$fileName

            rm -rf $resultFile
            echo "Output will be saved to $resultFile"
            pwd

            for ((i=1;i<=$RUNS;i++));
            do
                ./node benchmark/$CATEGORY/$CATEGORY.js | tee -a $fileName
            done



'