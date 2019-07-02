#!/usr/bin/python
import os
import argparse
import sys
from builders import get_latest_commit_id
from benchmarks import run
import utils
from config import *
from update import run_update

help = """
Manual to the script of %s, you need:
   - A benchmark's name like:

        --benchmark="web_tooling_benchmark"
        --benchmark="all"
     
     (special: "all" for run all other benchmarks one by one)
   - An id of a test machine(1 for xeon 8180, 2 for AMD 7601):
     
        --machine=1
     
     default is: 1 
   - A string of node's git commit id:
   
        --commit-id=86517c9f8f2aacf624025839ab8f03167c8d70dd
        
     or   
     
        --commit-id=86517c9f
        
     default is the latest commit id of node.
   - A bool type value:
   
        --postdata=true

     "true" for post data to data machine, "false" for not.
     default is: "false".
   - A command in terminal, you can use simple name for each config("-b" 
     for "--benchmark", "-m" for "--machine", "-i" for "--commit-id", "-p" for 
     "--postdata"):

        python dostuff.py -b xxxxxxx -m 1 -i "xxxxxxxxxxxxxxxxxxxxxxxxxx" -p false


Examples:

     python dostuff.py -b all -m 2 -p true
     python dostuff.py --benchmark=web_tooling_benchmark --machine=1 --commit-id=86517c9f8f2aacf624025839ab8f03167c8d70dd
     python dostuff.py --benchmark="node-dc-eis" -i 86517c9f
""" % __file__

REMOTE_NODE_DIR = "/home/benchmark"
NODE_SRC_PATH = "/home/benchmark/benchmarking/experimental/benchmarks/community-benchmark/node"
SAVE_NODE_PATH_DIR = "%s/out" % NODE_SRC_PATH

status = True
CURDIR = sys.path[0]

parser = argparse.ArgumentParser(description='------')
parser.usage = help
parser.add_argument('-b', '--benchmark', type=str, choices=benchs, required=True,
                    help="must set this param, any benchmark's name or 'all'. ")
# parser.add_argument('-a', '--branch', type=str, default="master", help="branch name, default: master")
parser.add_argument('-m', '--machine', type=int, default=1, choices=streams,
                    help="id of test machine in %s, default: 1" % streams)
parser.add_argument('-i', '--commit-id', type=str, default=None, help="default: latest commit id")
parser.add_argument('-p', '--postdata', type=bool, default=False, help="default: false")
parser.add_argument('-c', '--config', type=str, default=None, help="config file.")  # test machine config.

args = parser.parse_args()
MACHINE_ID = args.machine
BENCHMARK = args.benchmark
COMMIT_ID = args.commit_id
POSTDATA = args.postdata


def usage():
    print parser.format_usage()


def rsync_to_test_machine(src, dest):
    path_list = [
        (src + "/node", dest),
        # (LOCAL_BASE_DIR + "/", REMOTE_BASE_DIR),
    ]

    for path in path_list:
        create_node_dir_cmd = 'ssh %s@%s "mkdir -p %s"' % (machine["user"], machine["host"], dest)
        print create_node_dir_cmd
        os.system(create_node_dir_cmd)
        rsync_cmd = "rsync -aP %s %s@%s:%s" % (path[0], machine["user"], machine["host"], path[1])
        print rsync_cmd
        if not os.system(rsync_cmd):
            print "rsync succeed!"
        else:
            return 1
    return 0


def postdata(bench, streamid, commit_id):
    cmd = "ssh %s@%s \"cd /home/benchmark/benchmarking/experimental/benchmarks/%s ; \
        python postdata.py --machine=%s --commit-id=%s ;\"" % (machine['user'], machine['host'], bench, streamid, commit_id)
    print cmd
    ret = os.popen(cmd).read()
    if 'succeed' in ret and 'failed' not in ret:
        print "post data succeed!"
    else:
        print "post data failed!"
    print ''


def build_node():
    """build node"""
    cmd = ["python", "builders.py"]
    # cmd += "--branch=%s " % BRANCH
    if COMMIT_ID:
        cmd.append("--commit-id=%s" % COMMIT_ID)

    ret = utils.Run(cmd)
    # print cmd

    # ret = os.popen(cmd).read()
    # print ret
    if "build node succeed!" in ret:
        return 0
    else:
        return 1


def main(machine_id):
    # 1. build node.
    print "### now build node ###"
    if build_node():
        print "build node failed!\nExit."
        return 1

    # move node to a named place.
    node_src = NODE_SRC_PATH + "/out/Release/node"
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
        remote_node_dir = REMOTE_NODE_DIR + "/" + node_file_name
        remote_node_path = remote_node_dir + "/node"
        cmd1 = "mkdir -p %s" % dest_node_path
        cmd2 = "mv %s %s" % (node_src, dest_node_path)
        print cmd1
        os.system(cmd1)
        print cmd2
        if os.system(cmd2):
            return 3

    # 2. rsync to test machine.
    print "### now rsync new node to test machine ###"
    if rsync_to_test_machine(dest_node_path, remote_node_dir):
        print "rsync error, exit!"
        return 4

    # 3. remote run benchmarks.
    if BENCHMARK == "all":
        bench_list = benchs[:-1]
    else:
        bench_list = [BENCHMARK]

    for benchmark in bench_list:
        print "### now remote run benchmark %s ###" % benchmark
        run(benchmark, machine, remote_node_path)
        # 4. remote run postdata.py for each benchmark.
        if POSTDATA:
            print "### now post results of benchmark %s ###" % benchmark
            postdata(benchmark, machine_id, COMMIT_ID)
    else:
        if POSTDATA:
            run_update()
        return "all over."


if __name__ == '__main__':
    # 1. check params.
    # 1.1 check BENCHMARK.
    if not BENCHMARK:
        usage()
        status = False
    else:
        if BENCHMARK not in benchs and BENCHMARK != "all":
            print "ERROR: config 'benchmark' must in %s, or input 'all' for run all benchmarks!" % str(benchs)
            status = False
        else:
            print "BENCHMARK = %s" % BENCHMARK

        # 1.2 check BRANCH.
        if not BRANCH:
            usage()
            status = False
        else:
            if BRANCH not in branchs:
                print "ERROR: config 'branch' must in %s!" % str(benchs)
                status = False
            else:
                print "BRANCH = %s" % BRANCH

            # 1.3 check COMMIT_ID.
            if status:
                with utils.FolderChanger(NODE_SRC_PATH):
                    if not COMMIT_ID:
                        COMMIT_ID = get_latest_commit_id(BRANCH)

                    if not COMMIT_ID:
                        status = False
                    print "commit-id = %s" % COMMIT_ID

    # 2. build node.
    if status:
        # os.chdir(CURDIR)
        # 2.1 build node image.
        print "### now build node ###"
        if build_node():
            print "build node failed!\nExit."
            status = False

        # 2.2 move node to a named place.
        node_src = NODE_SRC_PATH + "/out/Release/node"
        cmd = node_src + " --version"
        try:
            node_version = os.popen(cmd).read().split()[0]
            # node_version = utils.Run(cmd)
            node_file_name = "node-" + node_version
            dest_node_path = "%s/%s" % (SAVE_NODE_PATH_DIR, node_file_name)
            remote_node_dir = REMOTE_NODE_DIR + "/" + node_file_name
            remote_node_path = remote_node_dir + "/node"
            # cmd1 = "mkdir -p %s" % dest_node_path
            cmd2 = "mv %s %s" % (node_src, dest_node_path)
            utils.mkdir(dest_node_path)
            if os.system(cmd2):
                status = False
        except Exception as e:
            print e
            status = False

    # 3. rsync to each test machine.
    if status:
        machine_list = []
        if not MACHINE_ID:
            for key in streams.keys():
                if key > 0:
                    machine_list.append(key)
        else:
            machine_list.append(MACHINE_ID)

        for machine_id in machine_list:
            machine = machines[streams[machine_id]]
            print machine
            print "### now rsync new node to test machine ###"
            if rsync_to_test_machine(dest_node_path, remote_node_dir):
                print "rsync error, exit!"
                status = False

            # 4. run benchmarks.
            if status:
                if "all over." == main(machine_id):
                    print "### all over. ###"
