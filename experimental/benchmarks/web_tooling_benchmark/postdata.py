#!/usr/bin/python
import os
import argparse
import numpy as np
import sys
sys.path.insert(1, "..")
from config import *

def usage():
    print parser.format_usage()

parser = argparse.ArgumentParser(description='manual to the script of %s' % __file__)
parser.add_argument('--branch', type=str, default="master")
parser.add_argument('--machine', type=int, choices=streams)
parser.add_argument('--commit-id', type=str, default=None)

args = parser.parse_args()
BRANCH = args.branch
MACHINE_ID = args.machine
COMMIT_ID = args.commit_id
status = True
if BRANCH not in streamid_dict or not COMMIT_ID:
    usage()
    status = False

if __name__ == '__main__':
    if status:
        arr = []
        f = open(file_name)
        line = f.readline()
        while line:
             if "Geometric mean" in line:
                  val = float(line.split()[-2])*100
                  print val
                  arr.append(val)
             line = f.readline()
        f.close()
        res = np.median(arr)
        if not res:
             print "no data, post data failed!"
        else:
             bench_name = 'webtooling'
             print res

             os.chdir(postit_dir)

             cmd = "bash postit.sh %s %s %s %s" % (MACHINE_ID, benchid_dict[bench_name], res, COMMIT_ID)
             print cmd
             if 'ok' in os.popen(cmd).read():
                  print 'post data %s succeed!' % bench_name
             else:
                  print 'post data %s failed!' % bench_name
