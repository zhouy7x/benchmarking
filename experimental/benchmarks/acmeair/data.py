#!/usr/bin/python
import sys
sys.path.insert(1, "..")
from config import *

if __name__ == '__main__':
    with open(file_name) as f:
        data = f.readlines()
        # print data

    if not data:
        print "no data, post data failed!"
    else:
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

                    print benchid_dict[key], value