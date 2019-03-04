#!/bin/bash
function mandatory() {
    if [ -z "${!1}" ]; then
        echo "${1} not set"
        usage
        exit
    fi
}

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
function usage(){
echo "Usage:"

echo "This script has two use cases:"
echo "Use case 1: We want to test the impact of a PR on a branch."
echo "To run this, declare:"
echo "The script expects the following variables to be set:"
echo "CATEGORY = a category of tests to run - folders in node/benchmark/"
echo "BRANCH = the branch the test should be based off. default: master"
echo "PULL_ID = the pull request that contains changes to test. default: latest commit"
echo "-------------------------------------------------------------"
echo "The following are optional"
echo "RUNS = defaults to 3"
echo "MACHINE_THREADS - used for building node. Defaults to all threads on machine"

}

mandatory CATEGORY
optional RUNS 3
getMACHINE_THREADS=`cat /proc/cpuinfo |grep processor|tail -n1|awk {'print $3'}`
let getMACHINE_THREADS=getMACHINE_THREADS+1 #getting threads this way is 0 based. Add one
optional MACHINE_THREADS $getMACHINE_THREADS

#rm -rf node
#git clone http://github.com/nodejs/node.git

pushd node
if [ -z $BRANCH ]; then
    BRANCH='master'
fi
git checkout $BRANCH

if [ -z $PULL_ID ]; then
#PULL_ID isn't declared. Therefore we use the latest commit.
        echo "PULL_ID not defined, use the latest commit."
else
        curl https://patch-diff.githubusercontent.com/raw/nodejs/node/pull/${PULL_ID}.patch|git apply
fi

# build
./configure  > ../node-build.log
make -j${MACHINE_THREADS}  >> ../node-build.log
mv out/Release/node ./node

# run benchmark
fileName=output`date +%d%m%y-%H%M%S`.csv
rm -rf $fileName
echo "Output will be saved to $fileName"
pwd

for ((i=1;i<=$RUNS;i++));
do
    ./node benchmark/$CATEGORY/$CATEGORY.js | tee -a $fileName
done

