#!/bin/bash
CUR_TIME=`date +%s`
wget -O result --user=V8onXeon --password=666 --no-check-certificate  "http://10.239.44.40:8080?streamid=$1&benchid=$2&time=$CUR_TIME&value=$3&cset=$4" >/dev/null 2>&1
cat result

