#!/usr/bin/python
import os
import argparse
from config import *
import utils

help = """
Manual to the script of %s, you need:
   - An absolute path of the node build by yourself and already copied to 
     the test machine(e.g. v8onxeon-8180.sh.intel.com):

        --node="/home/benchmark/my-node-dir/node"
     
     default is: "/home/benchmark/node-v12.0.0-pre/bin/node"
   - An id of a test machine:
     
        --machine=1
     
     default is: 1
   - A benchmark's name like:

        --benchmark="web_tooling_benchmark"
        --benchmark="all"
     
     (special: "all" for run all other benchmarks one by one)
   - A command in terminal, you can use simple name for each config("-b" 
     for "--benchmark", "-m" for "--machine", "-n" for "--node"):

        python benchmarks.py -b xxxxxxx -m x -n "xxxxxxxxxxxxxxxxxxxxxxxxxx"


Examples:

     python benchmarks.py -b "node-dc-eis" -m 1 -n "/home/benchmark/node-hre/node"
     python benchmarks.py --benchmark=octane 
     python benchmarks.py -b web_tooling_benchmark --machine=2 --node="/home/benchmark/node-v10.15.3-LTS/node"  
""" % __file__


def usage():
    print parser.format_usage()


def run(bench, machine, node):
    cmd_string = "ssh %s@%s \"cd /home/benchmark/benchmarking/experimental/benchmarks/%s ; \
        NODE=%s bash run.sh ;\"" % (machine['user'], machine['host'], bench, node)
    print cmd_string
    os.system(cmd_string)
    print "run test %s over!" % bench
    res_string = "ssh %s@%s \"cd /home/benchmark/benchmarking/experimental/benchmarks/%s ; \
        python data.py ;\"" % (machine['user'], machine['host'], bench)
    res = utils.Shell(res_string)
    return res.splitlines()


def show_data():
    pass


if __name__ == '__main__':
    # 1. get params.
    parser = argparse.ArgumentParser(description='------')
    parser.usage = help
    parser.add_argument('-b', '--benchmark', type=str, choices=benchs, required=True,
                        help="must set this param, any benchmark's name or 'all'. ")
    parser.add_argument('-m', '--machine', type=int, default=1, choices=streams,
                        help="id of test machine in %s, default: 1" % streams)
    parser.add_argument('-n', '--node', type=str, default=NODE, help="default: %s. " % NODE)
    parser.add_argument('-c', '--config', type=str, default=None, help="config file.")  # test machine config.

    args = parser.parse_args()
    BENCHMARK = args.benchmark
    MACHINE_ID = args.machine
    NODE = args.node

    # machine = machines[streams[MACHINE_ID]]
    # print machine
    # 2. check params.
    # 2.1 check NODE.
    # 2.2 check BENCHMARK.
    if not BENCHMARK:
        usage()
    else:
        print "node path = '%s'" % NODE
        if BENCHMARK not in benchs and BENCHMARK != "all":
            print "ERROR: config 'benchmark' must in %s, or input 'all' for run all benchmarks!" % str(benchs)
        else:
            if BENCHMARK == "all":
                bench_list = benchs[:-1]
            else:
                bench_list = [BENCHMARK]
            print "bench list: %s" % bench_list

            # check machine id.
            machine_list = []
            if not MACHINE_ID:
                for key in streams.keys():
                    if key:
                        machine_list.append(key)
            else:
                machine_list.append(MACHINE_ID)
            # print 'machine_list',machine_list
            for machine_id in machine_list:
                machine = machines[streams[machine_id]]
                print machine
                # 3. run benchmarks.
                data = []
                for benchmark in bench_list:
                    print ">"*50
                    print "Begin remote run benchmark: %s" % benchmark
                    print "<"*50
                    res = run(benchmark, machine, NODE)
                    for i in res:
                        j = i.split()
                        print j
                        for key, val in benchid_dict.iteritems():
                            if str(val) == j[0]:
                                j.insert(1, key)
                                data.append(j)
                                break
                else:
                    print "all over."
                    print data
                    # show_data()
