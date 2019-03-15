#!/usr/bin/python
import os
import argparse


parser = argparse.ArgumentParser(description='manual to the script of %s' % __file__)
parser.add_argument('--branch', type=str, default="master")
parser.add_argument('--commit-id', type=str, default=None)
parser.add_argument('--config', type=str, default=None)  # test machine config.

args = parser.parse_args()
BRANCH = args.branch
COMMIT_ID = args.commit_id

NODE_PATH = "/home/benchmark/benchmarking/experimental/benchmarks/community-benchmark/node"
status = True
LOG_PATH = "/home/benchmark/logs"

# def usage():
#     print parser.format_usage()

def checkout_branch():
    cmd = "git checkout %s" % BRANCH
    print cmd
    return os.system(cmd)


def use_current_commit_id():
    cmd = "git log -1 --pretty=short"
    print cmd
    return os.popen(cmd).readline().split()[1]


def get_latest_commit_id():
    cmd = "echo `git rev-list origin/master ^master` | awk '{print $1}'"
    print cmd
    try:
        commit_id = os.popen(cmd).read().split()[0]
    except Exception as e:
        print e
        commit_id = None
    # print type(commit_id)
    # print commit_id
    if not commit_id:
        commit_id = use_current_commit_id()
    return commit_id


def build_node():
    cmd = "./configure  > %s/node-build.log 2>&1 && make -j10 >> %s/node-build.log 2>&1" % (LOG_PATH, LOG_PATH)
    print cmd
    if not os.system(cmd):
        with open("%s/node-build.log" % LOG_PATH) as f:
            data = f.read()
        if "if [ ! -r node -o ! -L node ]; then ln -fs out/Release/node node; fi" in data:
            return 'ok'
    return 1


def main():
    # change path to node source.
    try:
        status = True
        os.chdir(NODE_PATH)
    except Exception as e:
        print e
        status = False
    else:
        # git checkout branch.
        if checkout_branch():
            print "error branch name!"
            status = False
        # git fetch
        if os.system("git fetch"):
            print "git fetch failed!"
            status = False
        # get a commit id to use.
        global COMMIT_ID
        if not COMMIT_ID:
            print "no commit id, use latest..."
            COMMIT_ID = get_latest_commit_id()
        print "commit-id = %s" % COMMIT_ID

        cmd = "git reset --hard -q %s" % COMMIT_ID
        print cmd
        if os.system(cmd):
            print "error commit id!"
            status = False

        if status:
            if 'ok' == build_node():
                print "build node succeed!"
                return
        print "build node failed!"


if __name__ == '__main__':
    main()
