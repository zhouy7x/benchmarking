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

        if not data:
            print "no data, post data failed!"
        else:
            os.chdir(postit_dir)
            for i in data:
                """
                metric throughput 4448.05 
                metric latency 6.257 sec
                metric pre footprint 48472
                metric post footprint 40644
                """
                bench_res_to_key = {
                    'metric throughput': 'acme air throughput',
                    'metric latency': 'acme air latency',
                    'metric pre footprint': 'acme air pre footprint',
                    'metric post footprint': 'acme air post footprint',
                }
                for name, key in bench_res_to_key.iteritems():
                    if name in i:
                        # print i
                        try:
                            value = float(i.split()[-1])
                            if name == 'metric latency':
                                value = int(value * 1000)
                            else:
                                value = int(value)
                        except Exception as e:
                            # print e
                            value = int(i.split()[-1])
    
                        # print (key, value)
    
                        cmd = "bash postit.sh %s %s %s %s" % (MACHINE_ID, benchid_dict[key], value, COMMIT_ID)
                        print cmd
                        if 'ok' in os.popen(cmd).read():
                            print 'post data %s succeed!' % str((key, value))
                        else:
                            print 'post data %s failed!' % str((key, value))
