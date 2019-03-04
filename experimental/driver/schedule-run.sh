#!/bin/bash

# Protocol for stopping V8onXeon:
#
# (1) If you want to stop it immediately:
#TODO
#
# (2) If you want to it to stop when possible:
#TODO

# init.
function optional() {
    if [ -z "${!1}" ]; then
        echo -n "${1} not set (ok)"
        if [ -n "${2}" ]; then
            echo -n ", default is: ${2}"
            export ${1}="${2}"
        fi
        echo ""
    fi
}
getMACHINE_THREADS=`cat /proc/cpuinfo |grep processor|tail -n1|awk {'print $3'}`
let getMACHINE_THREADS=getMACHINE_THREADS+1 #getting threads this way is 0 based. Add one
optional MACHINE_THREADS $getMACHINE_THREADS

optional RUNS 3




# 1. build a node.







# 1.1 download node git repo.
#pushd /home/benchmark/benchmarking/experimental/benchmarks/community-benchmark
#rm -rf node
#git clone http://github.com/nodejs/node.git

#check if node updated.

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
while :
do
    if [ -e /tmp/v8onxeon ]
    then
        echo "v8onxeon: /tmp/v8onxeon lock in place"
        sleep 30m
    else
        hasUpdate="false"

        # First, check node update
        pushd /home/benchmark/benchmarking/experimental/benchmarks/community-benchmark/node
        git fetch
        list=`git rev-list origin/master ^master`
        if [ -z "$list" ]; then
            echo "v8onxeon: no update"
        else

            hasUpdate="true"
            # Get every commit of v8
            for id in $list
            do
                git reset --hard -q $id && gclient sync -j10
                git log -1 --pretty=short
                commit=$id

                #build node.
                ./configure  > ../node-build.log
                make -j${MACHINE_THREADS}  >> ../node-build.log
                rm -rf node-v12.0.0-pre/bin/node
                mv out/Release/node node-v12.0.0-pre/bin

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



                python dostuff.py --config=client/hsw-nuc-x64.config $id

                #sleep 5s

                wait

                SECS=$(($(date +%s) - $STARTT))
                printf "\n++++++++++++++++ %dh:%dm:%ds ++++++++++++++++\n\n\n" $(($SECS/3600)) $(($SECS%3600/60)) $(($SECS%60))

                #sleep 10h

                popd

                pushd /home/user/work/awfy/server
                ./run-update.sh
                popd
                # count=`expr $count + 1`
                # mod5=`expr $count % 5`
                # if [ "$mod5" = "1" ]
                # then
                #   pushd /home/user/work/awfy/server
                #   ./run-update.sh
                #   popd
                # fi

                if [ -e /tmp/awfy-stop ]
                then
                    rm /tmp/awfy-daemon-v8 /tmp/awfy-stop
                    echo "awfy: Already stoped"
                    exit 0
                fi

                break
            done
        fi
        popd

#        # Second, check chromium update
#        pushd /home/user/work/repos/chrome/x64/chromium/src
#        git fetch
#        list=`git rev-list origin/master ^master | tac`
#        if [ -z "$list" ]; then
#            echo "chromium: no update"
#        else
#            for i in $list
#            do
#                # Only check v8 changed chromium
#                v8find=`git show $i | grep -P "^\+\s+.v8_revision."`
#                if [[ -n $v8find ]]; then
#                    hasUpdate="true"
#                    echo $i
#                    git reset --hard $i
#                    pushd /home/user/work/awfy/driver
#                    python dostuff.py  --config=client/machine_config/electro-x64.config
#                    python dostuff.py  --config=client/machine_config/elm-arm.config
#                    popd
#
#                    pushd /home/user/work/awfy/server
#                    bash ./run-update.sh
#                    popd
#                fi
#            done
#        fi
#        popd

        if [ "$hasUpdate" = "false" ]; then
            echo "awfy: no source update, sleep 15m"
            sleep 15m
        fi

    fi
done
rm /tmp/awfy-daemon-v8










    # 1.2 run build-node.sh.
    sh build-node.sh

# 2. run test.

