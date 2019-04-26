#!/usr/bin/python
import sys
sys.path.insert(1, "..")
from config import *


if __name__ == '__main__':
        with open(file_name) as f:
            data = f.readlines()
            # print data

        if data:
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
    
                        print benchid_dict[key], value
    

