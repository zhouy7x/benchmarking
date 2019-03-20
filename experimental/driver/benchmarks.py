#!/usr/bin/python
import os
import argparse


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
    "node-api"
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
    parser = argparse.ArgumentParser(description='manual to the script of %s' % __file__)
    parser.add_argument('--benchmark', type=str, help="must set this param, each benchmark name or 'all'. ")
    parser.add_argument('--node', type=str, default=NODE, help="default: %s. " % NODE)
    parser.add_argument('--config', type=str, default=None, help="config file.")  # test machine config.

    args = parser.parse_args()
    BENCHMARK = args.benchmark
    NODE = args.node

    # 2. check params.
    # 2.1 check NODE.
    print "node path = '%s'" % NODE
    # 2.2 check BENCHMARK.
    if not BENCHMARK:
        usage()
    else:
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
