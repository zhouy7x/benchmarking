#!/usr/bin/python3
import os
ITERATIONS = 50


# extract path for script we assume startNode.sh is in the
# same directory as this script
# SCRIPT_PATH=`readlink -f $0`
# SCRIPT_DIR=`dirname $SCRIPT_PATH`
def main():
    # time -o total_time -f "%e" sh $SCRIPT_DIR/startNode.sh $ITERATIONS
    cmd = "time -p bash startNode.sh %s 2>&1" % ITERATIONS
    TOTAL = os.popen(cmd).readline().split()[1]
    #TOTAL = os.popen(cmd).readline()
    print("TOTAL=%s" % TOTAL)
    cmd3 = "echo %s > total_time" % TOTAL
    if os.system(cmd3):
        print("create file named 'total_time' failed!")
        return
    # TOTAL=`cat total_time`
    # cat total_time | awk 'BEGIN{print ('$TOTAL'*1000000)/'$ITERATIONS'}'
    cmd2 = "cat total_time | awk 'BEGIN{print ('%s'*1000000)/%d}'" % (TOTAL, ITERATIONS)
    result = os.popen(cmd2).read().split()[0]
    print(result + 'us')


if __name__ == '__main__':
    main()
