#!/usr/bin/python
import numpy as np
import sys
sys.path.insert(1, "..")
from config import *


if __name__ == '__main__':
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
        if res:
             bench_name = 'webtooling'
             print benchid_dict[bench_name], res
