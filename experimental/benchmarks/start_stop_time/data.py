#!/usr/bin/python
import sys
sys.path.insert(1, "..")
from config import *


if __name__ == '__main__':
        with open(file_name) as f:
            data = f.readlines()
            # print data

        if data:
            if "Score" in data[-1]:
                bench_name = 'start_stop_time'
                res = int(data[-1].split()[-1])
                print benchid_dict[bench_name], res
