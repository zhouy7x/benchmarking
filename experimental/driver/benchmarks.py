#!/usr/bin/python
import os
import argparse


help = """
Manual to the script of %s, you need:
   - An absolute path of the node build by yourself and already copied to 
     the test machine(e.g. v8onxeon-8180.sh.intel.com):

        --node="/home/benchmark/my-node-dir/node"
     
     default is: "/home/benchmark/node-v12.0.0-pre/bin/node".
   - A benchmark's name like:

        --benchmark="web_tooling_benchmark"
        --benchmark="all"
     
     (special: "all" for run all other benchmarks one by one)
   - A command in terminal, you can use simple name for each config("-b" 
     for "--benchmark", "-n" for "--node"):

        python benchmarks.py -b xxxxxxx -n "xxxxxxxxxxxxxxxxxxxxxxxxxx"


Examples:

     python benchmarks.py -b "node-dc-eis" -n "/home/benchmark/node-hre/node"
     python benchmarks.py --benchmark=octane 
     python benchmarks.py -b web_tooling_benchmark --node="/home/benchmark/node-v10.15.3-LTS/node"
""" % __file__
machine = {
    "host": "v8onxeon-8180.sh.intel.com",
    "user": "benchmark",
    }
benchs = [
    "octane",
    "web_tooling_benchmark",
    # "startup",
    "start_stop_time",
    "node-dc-ssr",
    "node-dc-eis",
    "node-api",
    "all"
]
NODE = "/home/benchmark/node-v12.0.0-pre/bin/node"


def usage():
    print parser.format_usage()


def run(bench, node):
    cmd_string = "ssh %s@%s \"cd /home/benchmark/benchmarking/experimental/benchmarks/%s ; \
        NODE=%s bash run.sh ;\"" % (machine['user'], machine['host'], bench, node)
    print cmd_string
    if not os.system(cmd_string):
        print "run test succeed!"
    else:
        print "run test failed!"


if __name__ == '__main__':
    # 1. get params.
    parser = argparse.ArgumentParser(description='------')
    parser.usage = help
    parser.add_argument('-b', '--benchmark', type=str, choices=benchs, required=True, help="must set this param, any benchmark's name or 'all'. ")
    parser.add_argument('-n', '--node', type=str, default=NODE, help="default: %s. " % NODE)
    parser.add_argument('-c', '--config', type=str, default=None, help="config file.")  # test machine config.

    args = parser.parse_args()
    BENCHMARK = args.benchmark
    NODE = args.node

    # parser.usage = usage() + "\n" + help
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
            print "BENCHMARK = %s" % BENCHMARK

            if BENCHMARK == "all":
                bench_list = benchs
            else:
                bench_list = [BENCHMARK]

            # 3. run benchmarks.
            for benchmark in bench_list:
                print "### now remote run benchmark %s ###" % benchmark
                run(benchmark, NODE)
            else:
                print "all over."
