#!/usr/bin/python
import os
import sys
import argparse
import time
from collections import namedtuple

status = False

def usage():
    print """
    ERROR: Must set config "benchmark" & "commit-id"! 
    e.g. python dostuff.py --benchmark=xxxxx --commit-id=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    Exit!
    """

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--benchmark', type=str, default=None)
parser.add_argument('--branch', type=str, default="master")
parser.add_argument('--commit-id', type=str, default=None)
parser.add_argument('--config', type=str, default=None)  # test machine config.

args = parser.parse_args()
BRANCH = args.branch
BENCHMARK = args.benchmark
COMMIT_ID = args.commit_id
machine = {
    "host": "v8onxeon-8180.sh.intel.com",
    "user": "benchmark",

    }

if not BENCHMARK or not COMMIT_ID:
    usage()
    status = False
else:
    print "BENCHMARK = %s" % BENCHMARK
    print "commit-id = %s" % COMMIT_ID
    status = True


def rsync_to_test_machine():
    path_list = [
        ("/home/benchmark/benchmarking/experimental/benchmarks/community-benchmark/node/node-v12.0.0-pre/", "/home/benchmark/"),
    ]

    for path in path_list:
        rsync_cmd = "rsync -r %s %s@%s:%s" % (path[0], machine["user"], machine["host"], path[1])
        if not os.system(rsync_cmd):
            print "rsync succeed!"
        else:
            return 1

    return 0


def run():
    cmd_string = "ssh %s@%s \"cd /home/benchmark/benchmarking/experimental/benchmarks/%s ; bash run.sh;\"" % (machine['user'], machine['host'], BENCHMARK)
    print cmd_string
    if not os.system(cmd_string):
        print "run test succeed!"
    else:
        print "run test failed!"


def main():
    # run_3_bench_list = ['octane']
    bench_list = ['octane', 'web_tooling_benchmark', 'start_stop_time', 'node-dc-eis', 'node-dc-ssr']
    if BENCHMARK not in bench_list:
        print "error benchmark name!\nExit!"
        return

    # rsync node and benchmarks to test machine.
    # if rsync_to_test_machine():
    #     print "rsync error, exit!"
    #     return

    # remote run test benchmark.
    run()


if __name__ == '__main__':
    time.sleep(3)
    if status:
        main()
