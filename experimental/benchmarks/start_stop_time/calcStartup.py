#!/usr/bin/python
import os
from sys import argv

ITERATIONS = 500
NODE = argv[1] if argv[1:] else "$HOME/node/bin/node"

# extract path for script we assume startNode.sh is in the
# same directory as this script
# SCRIPT_PATH=`readlink -f $0`
# SCRIPT_DIR=`dirname $SCRIPT_PATH`
def main():
    # time -o total_time -f "%e" sh $SCRIPT_DIR/startNode.sh $ITERATIONS
    cmd = "NODE=%s time -p bash startNode.sh %s 2>&1" % (NODE, ITERATIONS)
    print cmd
    TOTAL = os.popen(cmd).readline().split()
    # TOTAL = os.popen(cmd).read()
    # print(TOTAL)
    TOTAL = TOTAL[1]

    print "TOTAL=%s" % TOTAL
    cmd3 = "echo %s > total_time" % TOTAL
    print cmd3
    if os.system(cmd3):
        print ("create file named 'total_time' failed!")
        return
    # TOTAL=`cat total_time`
    # cat total_time | awk 'BEGIN{print ('$TOTAL'*1000000)/'$ITERATIONS'}'
    cmd2 = "cat total_time | awk 'BEGIN{print ('%s'*1000000)/%d}'" % (TOTAL, ITERATIONS)
    print cmd2
    result = os.popen(cmd2).read().split()[0]
    print (result + 'us')
    if os.system("echo Score: %s > report.temp" % result):
        print "write to report.temp failed!"


if __name__ == '__main__':
    main()
