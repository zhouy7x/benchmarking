#!/usr/bin/python
import os
import argparse

file_name = "report.temp"
postit_dir = "/home/benchmark/benchmarking/tools/postResults"
benchid_dict = {
    'start_stop_time': 1,
    'startup_footprint': 2,
    'require.new': 3,
    'require.cached': 4,
    'acme air throughput': 5,
    'acme air latency': 6,
    'acme air pre footprint': 7,
    'acme air post footprint': 8,
    'octane': 9,
    'dc eis latency': 10,
    'dc eis throughput': 11,
    'webtooling': 12,
    'dc eis pre footprint': 13,
    'dc eis post footprint': 14,
    'dc ssr latency': 15,
    'dc ssr throughput': 16,
    'dc ssr pre footprint': 17,
    'dc ssr post footprint': 18,
}
streamid_dict = {
    'master': 1,
    '4.x': 2,
    '0.12.x': 3,
    '6.x': 4,
    '7.x': 5,
    '8.x': 6,
    'canary': 7,
    '10.x': 8,
}

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
