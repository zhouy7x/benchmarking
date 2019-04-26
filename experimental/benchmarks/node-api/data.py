#!/usr/bin/python
import sys
sys.path.insert(1, "..")
from config import *


if __name__ == '__main__':
        with open(file_name) as f:
            data = f.readlines()
            # print data
        data = map(lambda x: x[:x.rfind('.')].split(','), data)
        print data

        if not data:
            print "no data, post data failed!"
        else:
            for i in data:
                if i[0] not in benchid_dict:
                    print "Unknown bench name: %s\n Exit." % i[0]
                    break
                print benchid_dict[i[0]], i[1]
