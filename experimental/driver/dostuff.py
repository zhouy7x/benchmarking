#!/usr/bin/python
import os
import argparse
import time


def usage():
    print parser.format_usage()


parser = argparse.ArgumentParser(description='manual to the script of %s' % __file__)
parser.add_argument('--benchmark', type=str, default=None)
parser.add_argument('--branch', type=str, default="master")
parser.add_argument('--commit-id', type=str, default=None)
parser.add_argument('--postdata', type=bool, default=False)
parser.add_argument('--config', type=str, default=None)  # test machine config.

args = parser.parse_args()
BRANCH = args.branch
BENCHMARK = args.benchmark
COMMIT_ID = args.commit_id
POSTDATA = args.postdata
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
BUILD_NODE_PATH = "/home/benchmark/benchmarking/experimental/benchmarks/community-benchmark/node"
SAVE_NODE_PATH_DIR = "%s/out" % BUILD_NODE_PATH

status = True
if not BENCHMARK:
    usage()
    status = False
else:
    if BENCHMARK not in benchs and BENCHMARK == "all":
        print "ERROR: config 'benchmark' must in %s, or input 'all' for run all benchmarks!" % str(benchs)
        status = False
    else:
        print "BENCHMARK = %s" % BENCHMARK
        print "BRANCH = %s" % BRANCH
        print "commit-id = %s" % COMMIT_ID


def rsync_to_test_machine(src, dest):
    path_list = [
        (src + "/node", dest),
    ]

    for path in path_list:
        rsync_cmd = "rsync -a %s %s@%s:%s" % (path[0], machine["user"], machine["host"], path[1])
        print rsync_cmd
        if not os.system(rsync_cmd):
            print "rsync succeed!"
        else:
            return 1
    return 0


def run(bench, node):
    cmd_string = "ssh %s@%s \"cd /home/benchmark/benchmarking/experimental/benchmarks/%s ; \
        NODE=%s bash run.sh ;\"" % (machine['user'], machine['host'], bench, node)
    print cmd_string
    if not os.system(cmd_string):
        print "run test succeed!"
    else:
        print "run test failed!"


def build_node():
    """build node"""
    cmd = "python builders.py "
    cmd += "--branch=%s " % BRANCH
    if COMMIT_ID:
        cmd += "--commit-id=%s " % COMMIT_ID
    print cmd

    ret = os.popen(cmd).read()
    print ret
    if "build node succeed!" in ret:
        return 0
    else:
        return 1


def postdata(bench, branch, commit_id):
    cmd = "ssh %s@%s \"cd /home/benchmark/benchmarking/experimental/benchmarks/%s ; \
        python postdata.py --branch=%s --commit-id=%s ;\"" % (machine['user'], machine['host'], bench, branch, commit_id)
    print cmd
    if 'failed' not in os.popen(cmd).read():
        print "post data succeed!"
    else:
        print "post data failed!"


def main():
    # 1. build node.
    print "### now build node ###"
    if build_node():
        print "build node failed!\nExit."
        return 1
    else:
        # move node to a named place.
        node_src = BUILD_NODE_PATH + "/out/Release/node"
        cmd = "%s --version" % node_src
        print cmd
        try:
            node_version = os.popen(cmd).read().split()[0]
        except Exception as e:
            print e
            return 2
        else:
            node_file_name = "node-" + node_version
            dest_node_path = "%s/%s" % (SAVE_NODE_PATH_DIR, node_file_name)
            cmd1 = "mkdir -p %s" % dest_node_path
            cmd2 = "mv %s %s" % (node_src, dest_node_path)
            print cmd1
            os.system(cmd1)
            print cmd2
            if os.system(cmd2):
                return 3

    # 2. rsync to test machine.
    # rsync node and benchmarks to test machine.
    print "### now rsync new node to test machine ###"
    if rsync_to_test_machine(dest_node_path, NODE):
        print "rsync error, exit!"
        return 4

    # 3. remote run benchmark.
    print "### now remote run benchmark ###"
    if BENCHMARK == "all":
        bench_list = benchs
    else:
        bench_list = [BENCHMARK]

    for benchmark in bench_list:
        run(benchmark, NODE)

        # 4. remote run postdata.py.
        if POSTDATA:
            print "### now post results of benchmark %s ###" % benchmark
            postdata(benchmark, BRANCH, COMMIT_ID)
    else:
        return "all over."


if __name__ == '__main__':
    time.sleep(1)
    if status:
        if "all over." == main():
            print "### all over. ###"
