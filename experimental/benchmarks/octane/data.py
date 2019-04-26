#!/usr/bin/python
import sys
sys.path.insert(1, "..")
from config import *


if __name__ == '__main__':
        arr = []
        f = open(file_name)
        line = f.readline()
        while line:
             if "Score" in line:
                  val = int(line.split()[-1])
                  arr.append(val)
             line = f.readline()
        f.close()
        res = max(arr)
        bench_name = 'octane'
        if res:
            print benchid_dict[bench_name], res
