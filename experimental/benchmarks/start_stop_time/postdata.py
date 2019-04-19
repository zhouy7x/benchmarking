#!/usr/bin/python
import os
import argparse
import sys
sys.path.insert(1, "..")
from config import *

def usage():
    print parser.format_usage()

parser = argparse.ArgumentParser(description='manual to the script of %s' % __file__)
parser.add_argument('--branch', type=str, default="master")
parser.add_argument('--commit-id', type=str, default=None)

args = parser.parse_args()
BRANCH = args.branch
COMMIT_ID = args.commit_id
status = True
if BRANCH not in streamid_dict or not COMMIT_ID:
    usage()
    status = False

if __name__ == '__main__':
    if status:
        with open(file_name) as f:
            data = f.readlines()
            # print data

        if not data:
            print "no data, post data failed!"
        else:
            if "Score" in data[-1]:
                bench_name = 'start_stop_time'
                res = int(data[-1].split()[-1])
                print res

                os.chdir(postit_dir)

                cmd = "bash postit.sh %s %s %s %s" % (streamid_dict[BRANCH], benchid_dict[bench_name], res, COMMIT_ID)
                print cmd
                if 'ok' in os.popen(cmd).read():
                    print 'post data %s succeed!' % bench_name
                else:
                    print 'post data %s failed!' % bench_name
            else:
                print "do not find data, post data failed!"
