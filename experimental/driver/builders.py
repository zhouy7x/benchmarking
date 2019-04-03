#!/usr/bin/python
import os
import argparse
import utils

help = """
Manual to the script of %s, you need:
   - A name of node's branch like:
   
        --branch="master"
     
     default is: "master".
   - A string of node's git commit id:
   
        --commit-id=86517c9f8f2aacf624025839ab8f03167c8d70dd
        
     or   
     
        --commit-id=86517c9f
        
     default is the latest commit id of node.
   - A command in terminal, you can use simple name for each config("-b" 
     for "--benchmark", "-n" for "--node"):

        python builders.py -a xxxxxxx -i "xxxxxxxxxxxxxxxxxxxxxxxxxx"


Examples:

     python builders.py
     python builders.py -a master -i 86517c9f8f2aacf624025839ab8f03167c8d70dd
     python builders.py --branch="v8.x"


""" % __file__
NODE_SRC_PATH = "/home/benchmark/benchmarking/experimental/benchmarks/community-benchmark/node"
LOG_PATH = "/home/benchmark/logs"


def check_branch(foo):
    """check if it is need to checkout branch."""
    def _inside(branch, *args, **kwargs):
        try:
            os.chdir(NODE_SRC_PATH)
            branch_list = os.popen('git branch').readlines()
            for i in branch_list:
                if i.startswith("*"):
                    cur_branch = i.split()[1]
                    break
            print "current branch:", cur_branch

            if cur_branch == branch:
                print "Already on branch '%s'" % branch
            else:
                if checkout_branch(branch):
                    print "git checkout %s failed!" % branch
                    return

            return foo(branch, *args, **kwargs)
        except Exception as e:
            print e
            return 1

    return _inside


def checkout_branch(branch):
    cmd = "git checkout %s" % branch
    print cmd
    return os.system(cmd)


def use_current_commit_id():
    cmd = "git log -1 --pretty=short"
    print cmd
    return os.popen(cmd).readline().split()[1]


@check_branch
def get_latest_commit_id(branch):
    # 1. git fetch
    cmd = "git fetch"
    print cmd
    if os.system(cmd):
        print "git fetch failed!"
        return

    # 2. get latest commit id in origin.
    cmd = "echo `git rev-list origin/%s ^%s` | awk '{print $1}'" % (branch, branch)
    print cmd
    try:
        commit_id = os.popen(cmd).read().split()[0]
    except Exception as e:
        # print e
        commit_id = use_current_commit_id()

    return commit_id


def build():
    cmd = "./configure  > %s/node-build.log 2>&1 && make  >> %s/node-build.log 2>&1" % (LOG_PATH, LOG_PATH)
    print cmd
    if not os.system(cmd):
        with open("%s/node-build.log" % LOG_PATH) as f:
            data = f.read()
        if "if [ ! -r node -o ! -L node ]; then ln -fs out/Release/node node; fi" in data:
            return 'ok'
    return 1


@check_branch
def reset_node(branch, commit_id):
    # git reset.
    cmd = "git reset --hard -q %s" % commit_id
    print cmd
    return os.system(cmd)


def main(branch, commit_id=None):
    # 1. if commit id not set, get the latest commit id of branch.
    if not commit_id:
        print "no commit id, use latest..."
        commit_id = get_latest_commit_id(branch)
        if not commit_id:
            print "get latest commit id failed!"
            return

    # 2. reset node to this commit.
    if reset_node(branch, commit_id):
        print "reset node failed!"
        return
    commit_id = use_current_commit_id()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print commit_id
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
    # 3. build node.
    if 'ok' == build():
        print "build node succeed!"
        return

    print "build node failed!"


if __name__ == '__main__':
    # 1. check params.
    parser = argparse.ArgumentParser()
    parser.usage = help
    parser.add_argument('-a', '--branch', type=str, default="master", help="default: master.")
    parser.add_argument('-i', '--commit-id', type=str, default=None, help="default: latest commit id.")
    parser.add_argument('-c', '--config', type=str, default=None, help="config file.")  # test machine config.

    args = parser.parse_args()
    BRANCH = args.branch
    COMMIT_ID = args.commit_id

    # 2. run build node.
    with utils.FolderChanger(NODE_SRC_PATH):
        main(BRANCH, COMMIT_ID)
