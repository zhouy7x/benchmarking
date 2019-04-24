#!/bin/bash
#shopt -s -o nounset

start=`date +%s`
#set locations so we don't end up with lots of hard coded bits throughout script
RESOURCE_DIR=$1
REL_DIR=$(dirname $0)
ROOT_DIR=`cd "${REL_DIR}/.."; pwd`
echo "ROOT_DIR=${ROOT_DIR}"
SCRIPT_DIR=${ROOT_DIR}/acmeair
ACMEAIR_DIR=${SCRIPT_DIR}/node/acmeair-nodejs
MONGO_DIR=${SCRIPT_DIR}

echo "$SCRIPT_DIR"
echo "$ACMEAIR_DIR"
echo "$MONGO_DIR"

#these may need changing when we find out more about the machine we're running on
NODE_AFFINITY="numactl --physcpubind=0,4"
MONGO_AFFINITY="numactl --physcpubind=1,5"
JMETER_AFFINITY="numactl --physcpubind=2,6"

function usage() {
	echo "USAGE:"
	echo "Currently this script will run acmeair, including mongodb and JMeter, with the affinities as follows:"
	echo "Node : $(echo ${node_affinity})"
	echo "Mongodb : $(echo ${mongo_affinity})"
	echo "JMeter : $(echo ${jmeter_affinity})"
}

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
function remove(){
if [ -f $1 ]; then
	rm $1
fi

}
function archive_files() {
    # archive files
    echo -e "\n##BEGIN $TEST_NAME Archiving $(date)\n"
    mv $LOGDIR_TEMP/$LOGDIR_PREFIX $RESULTSDIR
    echo -e "Perf logs stored in $RESULTSDIR/$LOGDIR_PREFIX"
    echo -e "\nCleaning up"
    rm -r $LOGDIR_TEMP
    echo -e "\n## END $TEST_NAME Archiving $(date)\n"
}

function kill_bkg_processes()   # kill processes started in background
{
	echo "Killing due to : $@"    
	$MONGODB_COMMAND "stop"
	pkill node
	pkill mongod
	sleep 5
        JAVA_PID="`ps -ef|grep java|grep -v grep|grep -v slave|awk {'print $2'}`"
	if [ -n "$JAVA_PID" ]; then
           kill -9 $JAVA_PID || true
	fi
	cp=$$
	pids=$(ps -eo pid,pgid | awk -v pid=$cp '$2==pid && $1!=pid{print $1}')  # get list of all child/grandchild pids - this doesnt seem to work on nodejs benchmark machine....
	echo "Killing background processes"
	echo $pids
	if [ -n "$pids" ]; then
	   kill -9 $pids || true
	fi
	for i in $OTHERPID_LIST
	do
	   pidi="`ps -ef | grep $i |grep -v 'grep'`"
	   if [ -n "$pidi" ]; then
	      kill -9 $i || true
	   fi
	done
#	kill -9 $OTHERPID_LIST $pids || true  # avoid failing if there is nothing to kill
}

function on_exit()
{
    echo "Caught kill"
    kill_bkg_processes "caught kill"
#    kill -9 $PID_LIST  $OTHERPID_LIST
    archive_files
    exit 1
}

function timestamp()
{
    date +"%Y%m%d-%H%M%S"
}

trap on_exit SIGINT SIGQUIT SIGTERM

# VARIABLE SECTION

# define variables
declare -rx SCRIPT=${0##*/}
echo "$SCRIPT"
TEST_NAME=acmeair
echo -e "\n## TEST: $TEST_NAME ##\n"
echo -e "## OPTIONS ##\n"

optional RESULTSDIR $SCRIPT_DIR/results
optional TIMEOUT 600
RESULTSLOG=$TEST_NAME.log
SUMLOG=score_summary.txt

optional DRIVERHOST
optional NODE_FILE app.js
optional CLUSTER_MODE false
optional PORT 4000
optional DRIVERCMD ${SCRIPT_DIR}/node/Jmeter/bin/jmeter
optional DRIVERNO 25
ACMEAIR_DRIVER_PATH=${SCRIPT_DIR}/jmeter_scripts

NODE_SERVER=$(hostname -s)
NODE_SERVER=$NODE_SERVER.sh.intel.com                    

echo -e "RESULTSDIR: $RESULTSDIR"
echo -e "RESULTSLOG: $RESULTSLOG"
echo -e "TIMEOUT: $TIMEOUT"
echo -e "NODE_SERVER: $NODE_SERVER"
echo -e "PORT: $PORT"
echo -e "NETWORKTYPE: $NETWORKTYPE"
echo -e "DRIVERCMD: $DRIVERCMD"
echo -e "DRIVERNO: $DRIVERNO\n"

JMETER_LOGFILE=$ACMEAIR_DRIVER_PATH/jmeter.log
DRIVER_COMMAND="$JMETER_AFFINITY $DRIVERCMD -Jduration=240 -Jdrivers=$DRIVERNO -Jhost=$NODE_SERVER -Jport=$PORT -DusePureIDs=true -n -t $ACMEAIR_DRIVER_PATH/AcmeAir.jmx -p $ACMEAIR_DRIVER_PATH/acmeair.properties -l $JMETER_LOGFILE"

# END VARIABLE SECTION


# Date stamp for result files generated by this run
CUR_DATE=$(timestamp)

PLATFORM=`/bin/uname | cut -f1 -d_`
echo -e "Platform identified as: ${PLATFORM}\n"

case ${PLATFORM} in
	Linux)
		bash ${SCRIPT_DIR}/kill_node_linux
		;;
esac

NODE=`which node`
echo "node=$NODE"
echo -e "NODE VERSION:"
$NODE --version

# build command
CMD="$NODE_AFFINITY ${NODE} ${NODE_FILE}" 
echo "$CMD"
export LOGDIR_TEMP=$RESULTSDIR/temp
. ${SCRIPT_DIR}/fp.sh
case ${PLATFORM} in
        Linux)
                HPPRETOTAL=`cat /proc/meminfo | grep HugePages_Total | sed 's/HugePages.*: *//g' | head -n 1`
                HPPREFREE=`cat /proc/meminfo | grep HugePages_Free | sed 's/HugePages.*: *//g' | head -n 2|tail -n 1`
                let HPPREINUSE=$HPPRETOTAL-$HPPREFREE
                echo "HP IN USE : " ${HPPREINUSE}
                ;;
esac

mkdir -p $LOGDIR_TEMP
DONEFILE_TEMP=$LOGDIR_TEMP/donefile.tmp
echo -e "\nDONE file: $DONEFILE_TEMP"
echo -n > $DONEFILE_TEMP

# start checking files in case things fall over before we get going
(while ! grep done $DONEFILE_TEMP &>/dev/null ; do
    sleep 3
    # Abort the run if an instance fails or if we time out
    if grep fail $DONEFILE_TEMP &>/dev/null ; then
        on_exit
    fi
done
)&
LOOKFORDONE_PID=$!

# start time clock
( sleep $TIMEOUT; echo "TIMEOUT (${TIMEOUT}s)"; echo "fail" >> $DONEFILE_TEMP; ) &
TIMEOUT_PID=$!
TIMEOUT_CHILD=`pgrep -P $TIMEOUT_PID`
export OTHERPID_LIST="$OTHERPID_LIST $TIMEOUT_CHILD $TIMEOUT_PID $LOOKFORDONE_PID"
echo "$OTHERPID_LIST"

LOGDIR_PREFIX=$PRODUCT/$DATE/$CUR_DATE
LOGDIR_PREFIX=${LOGDIR_PREFIX##*/}
SUMFILE=$LOGDIR_TEMP/$LOGDIR_PREFIX/$SUMLOG
STDOUT_SERVER=$LOGDIR_TEMP/$LOGDIR_PREFIX/server.out
STDOUT_CLIENT=$LOGDIR_TEMP/$LOGDIR_PREFIX/client.out
STDOUT_RESULTS=$LOGDIR_TEMP/$LOGDIR_PREFIX/jmeter.log
STDOUT_DB=$LOGDIR_TEMP/$LOGDIR_PREFIX/db.out
OUT_LIST="$OUT_LIST $LOGDIR_PREFIX/$SUMLOG $LOGDIR_PREFIX/server.out $LOGDIR_PREFIX/client.out $LOGDIR_PREFIX/db.out $LOGDIR_PREFIX/jmeter.log"

echo "$LOGDIR_PREFIX"
echo "$SUMFILE"
echo "$STDOUT_SERVER"
echo "$STDOUT_CLIENT"
echo "$STDOUT_RESULTS"
echo "$STDOUT_DB"
echo "$OUT_LIST"

echo -e "\n*** SUMMARY FILE  $SUMFILE ***\n"

echo -e "\n##START TEST INSTANCES $(date)\n"

echo
echo "*** BEGIN RUN ***"
LOGDIR_SHORT=$LOGDIR_PREFIX
LOGDIR_LONG=$LOGDIR_TEMP/$LOGDIR_SHORT
echo "$LOGDIR_SHORT"
echo "$LOGDIR_LONG"
mkdir -p $LOGDIR_LONG
LOGFILE=$LOGDIR_LONG/$RESULTSLOG
echo "$LOGFILE"
rm -f $LOGFILE
echo "$LOGFILE"
OUT_LIST="$OUT_LIST $LOGDIR_SHORT/$RESULTSLOG"
echo "$OUT_LIST"
echo "*** LOGFILE  $LOGFILE ***"

# Start MongoDB
MONGODB_COMMAND="${MONGO_DIR}/mongodb.sh"
echo -e "\n## STARTING MONGODB ##" 2>&1 | tee -a $LOGFILE
echo -e " $MONGODB_COMMAND start" | tee -a $LOGFILE
$MONGO_AFFINITY $MONGODB_COMMAND start
sleep 5     # give it a chance to start up

# Start the server(s)
echo -e "\n## SERVER COMMAND ##" 2>&1 | tee -a $LOGFILE
echo -e " $CPUAFFINITY $CMD" 2>&1 | tee -a $LOGFILE
echo -e "## BEGIN TEST ##\n" 2>&1 | tee -a $LOGFILE

(
    pushd $ACMEAIR_DIR
    $CPUAFFINITY $CMD > $STDOUT_SERVER 2>&1
    echo -e "\n## Server no longer running ##"   
    echo "fail" >> $DONEFILE_TEMP   
    popd
) &
sleep 10 # give server some time to start up

echo "${SCRIPT_DIR}/loaddb.sh localhost ${PORT}"
db_start=`date +%s.%N`
${SCRIPT_DIR}/loaddb.sh localhost ${PORT}
db_end=`date +%s.%N`
db_start_s=$(echo $db_start | cut -d . -f1)
db_start_ns=$(echo $db_start | cut -d . -f2)
db_end_s=$(echo $db_end | cut -d . -f1)
db_end_ns=$(echo $db_end | cut -d . -f2)
let res=$(((10#$db_end_s - 10#$db_start_s) * 1000 + (10#$db_end_ns / 1000000 - 10#$db_start_ns / 1000000)))
echo -e "\nload time: $res ms"

sleep 5
pre=`getFootprint`
echo -n "Pre run Footprint in kb : $pre"

# Start the driver(s)
echo -e "\n## DRIVER COMMAND ##" 2>&1 | tee -a $LOGFILE
echo -e "$DRIVER_COMMAND"|tee -a $LOGFILE

(
	t1=`date +%s`
    if (exec $DRIVER_COMMAND > jmeter.log 2>&1 ) ; then
        echo "Drivers have finished running" 2>&1 | tee -a $LOGFILE
        echo "done" >> $DONEFILE_TEMP
        echo "done" >> server_cpu.txt
    else
        echo "ERROR: driver failed or killed" 2>&1 | tee -a $LOGFILE
        echo "fail" >> $DONEFILE_TEMP
    fi
	t2=`date +%s`
	let td=$t2-$t1
	echo "driver time: $td s"
) &
sleep 5 #sometimes java takes a little longer to get going, so we miss cpu profile
remove server_cpu.txt
PIDS="`ps -ef|grep java|grep -v grep|grep -v slave|awk {'print $2'}`"
PIDS="$PIDS `ps -ef|grep mongod|grep -v grep|awk {'print $2'}`"
PIDS="$PIDS `ps -ef|grep node|grep -v grep|awk {'print $2'}`"
PIDS_COMMA=`echo $PIDS|sed 's/ /,/g'`
#print top output every 5 seconds 47 times = 48*5  - minus 1 measure so we don't end up with a low last number= 240 = length of jmeter run
SERVER_CPU_COMMAND="top -b -d 5 -n 47 -p $PIDS_COMMA"
$SERVER_CPU_COMMAND >> server_cpu.txt &
CPU_PID=$!
export OTHERPID_LIST="$OTHERPID_LIST $CPU_PID"
while ! grep done $DONEFILE_TEMP &>/dev/null ; do
    sleep 3
    # Abort the run if an instance fails or if we time out
    if grep fail $DONEFILE_TEMP &>/dev/null ; then
        on_exit
    fi
done
post=`getFootprint`

echo -n "Runtime Footprint in kb : $post" 
let difference=$post-$pre
kill_bkg_processes "Should be finished"

echo -e "\n## END RUN ##"

for log in server 
do
	echo "sh $SCRIPT_DIR/cpuParse.sh ${log}_cpu.txt $log"
	sh ${SCRIPT_DIR}/cpuParse.sh ${log}_cpu.txt $log
	mv ${log}_cpu.txt $LOGDIR_TEMP/$LOGDIR_PREFIX
	export OUT_LIST="$OUT_LIST $LOGDIR_PREFIX/${log}_cpu.txt"
done

# print output
echo -e "\n##BEGIN $TEST_NAME OUTPUT $(date)\n" 2>&1 | tee -a $SUMFILE
echo metric throughput $(cat $JMETER_LOGFILE | awk -f ${SCRIPT_DIR}/acmeair_score.awk) 2>&1 | tee -a $SUMFILE
echo metric latency $(cat $JMETER_LOGFILE | awk -f ${SCRIPT_DIR}/acmeair_latency.awk) 2>&1 | tee -a $SUMFILE
mv $JMETER_LOGFILE $LOGDIR_TEMP/$LOGDIR_PREFIX
export OUT_LIST="$OUT_LIST $LOGDIR_PREFIX/jmeter.log"
echo "metric pre footprint $pre"
echo "metric post footprint $post"
echo "metric footprint increase $difference"
echo -e "\n## TEST COMPLETE ##\n" 2>&1 | tee -a $SUMFILE
echo -e "\n## END $TEST_NAME OUTPUT $(date)\n\n" 2>&1 | tee -a $SUMFILE

end=`date +%s`
let elapsed=$end-$start
echo "Elapsed time : $elapsed"

archive_files
