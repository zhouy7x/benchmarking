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
            os.chdir(postit_dir)
            for i in data:
                """
                metric throughput 48.05 req/sec
                metric latency 6.257 sec
                metric pre footprint 48472
                metric post footprint 40644
                """
                bench_res_to_key = {
                    'metric throughput': 'dc ssr throughput',
                    'metric latency': 'dc ssr latency',
                    'metric pre footprint': 'dc ssr pre footprint',
                    'metric post footprint': 'dc ssr post footprint',
                }
                for name, key in bench_res_to_key.iteritems():
                    if name in i:
                        # print i
                        try:
                            value = float(i.split()[-2])
                            if name == 'metric latency':
                                value = int(value * 1000)
                            else:
                                value = int(value)
                        except Exception as e:
                            # print e
                            value = int(i.split()[-1])
    
                        # print (key, value)
    
                        cmd = "bash postit.sh %s %s %s %s" % (streamid_dict[BRANCH], benchid_dict[key], value, COMMIT_ID)
                        print cmd
                        if 'ok' in os.popen(cmd).read():
                            print 'post data %s succeed!' % str((key, value))
                        else:
                            print 'post data %s failed!' % str((key, value))
