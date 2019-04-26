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
        with open(file_name) as f:
            data = f.readlines()
            # print data
        data = map(lambda x: x[:x.rfind('.')].split(','), data)
        print data

        if not data:
            print "no data, post data failed!"
        else:
            os.chdir(postit_dir)
            for i in data:
                if i[0] not in benchid_dict:
                    print "Unknown bench name: %s\n Exit." % i[0]
                    break
                cmd = "bash postit.sh %s %s %s %s" % (MACHINE_ID, benchid_dict[i[0]], i[1], COMMIT_ID)
                print cmd
                if 'ok' in os.popen(cmd).read():
                    print 'post data %s succeed!' % str(i)
                else:
                    print 'post data %s failed!' % str(i)
