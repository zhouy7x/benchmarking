# Run_acmeair.shm

## Intruduction

The run_acmeair script is finally used to test the performance of cpu by the jmeter tool.

## Comment

### Set locations

Define some paths according to corresponding paths in setupJmeter.sh such as acmeair path, acmeair-nodejs path.

### Bind core(s)

The three processes of node,mongdo and jmeter will be bound to run on a fixed core(s) with "numactl" tool. If running on 8180 machine, due to hyper threading technology, actually per core has two hyper threadings and one process will be bound to two hyper threadings of a core. You can also bind a process to two hyper threadings of two cores, but the performance may be drop.
For example on 8180 machine:`
NODE: "numactl --physcpubind=0,28" ---the "0,28" represent two hyper threadings of "0" core
MONGO: "numactl --physcpubind=1,29" ---the "1,29" represent two hyper threadings of "1" core
JMETER: "numactl --physcpubind=2,30" ---the "2,30" represent two hyper threadings of "2" core

### Define some functions 

function usage()
function mandatory()
function optional(): assign a value to a parameter
function remove()
function archive_files(): store the log and then remove the temporary log
function kill_bkg_processes(): before the end of the script, the processes of node, mongodb, java, related subprocess and some background prcesses are all killed
function on_exit(): When a signal to terminate the process occurs, the funciton will be run. In fact, this function calls "kill_bkg_processes()" then exit the script
function timestamp()

### Define variables

Call the function "optional()" to assign a value to a parameter
The "DRIVER_COMMAND" is the jmeter command that used to simulate the number of concurrent users to visit a website in order to testing the performance of cpu. The parameters are described as follows:
-Jduration: time of stress testing
-Jdrivers: the number of concurrent users
-Jhost: host address
-Jport: host port
-n: run jmeter in non-GUI mode
-t: the jmeter test(.jmx) file to run
-l: the file to log results

### Kill node

When the platform is identified as Linux, the kill_node_linux script will be called to kill all node-related processes.

### Build command 

After calling the kill_node_linux script, we can get the node path and build node command.

### Calculating the hugePages utilization rate

### Start checking files in case things fall over before we get going

Creating the "donefile.tmp" temporary file and Running a cycle process background to check whether errors have occurred.

### Start time clock

Running a time process background in order to check whether the script runs out of time, the defult time is 600s.

### Define various output files of logs

### Start MongoDB

The mongodb.sh script will be called. If mongodb had started beforehand, the main script will kill the mongodb process first and then restart mongodb.

### Start the server(s)

Starting node server background. If running fail, the main script will be exited.

### Run loaddb.sh

The script uses the parameter "numCustomers=10000" to simulate adding 100000 users data to database and then calculate its operation time.

### Pre "getFootprint"

Start to call the function "getFootprint". This function is to get Resident Set Size(RSS) of the process,including memory size of shared library but excluding Virtual Memory Size(VSZ) occupied by swap and get the utilization of hugePages. 

#### Start the driver(s)

It takes 240 seconds to run the jmeter pressure test background. If failed, the main script will be exited.

#### Print top output

When starting the jmeter drivers, the utilization of cpu,java,mongo and node every 5 seconds 47 times will be logged in the server_cpu.txt synchronous.

### Post "getFootprint"

### Kill processes

When the jmeter pressure test have finished running, it need to call the function "kill_bkg_processes()" to kill related processes.

### Calculate utilization

Run the cpuParse.sh script to calculate the utilization of java,node,mongodb and jmeter. For example, "idle_values" in cpuParse.sh means all idle times of cpu which is extracted from "server_cpu.txt", then, from the third idle time, add the remaining idle times and divide them by count.The result is the average value of idle time and the cpu utilization is minus the average by 100. Others and so on.

### Print throughput and latency

#### Calculate throughput

When the log file "jmeter.log" was generated after jmeter pressure test, we can use "acmeair_score.awk" to calculate throughput with it. "acmeair_score.awk" is based on counting the number of successful responses received after the first 120 seconds of the run and then dividing by the elapsed time (minus 120 seconds) to get a requests/sec score. In fact, throughput is calculated using the value taken in the next 120 seconds.

#### Calculate latency

We use "acmeair_latency.awk" to handle with "jmeter.log" to calculate latency. "acmeair_latency.awk" adds up all values of latency and then divides by count.

### Print footprint

### Call the function "archive_files()"
